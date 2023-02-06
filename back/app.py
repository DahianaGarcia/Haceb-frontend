import json
import time
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import cv2
import numpy as np
import imutils
from waitress import serve
import socket

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/plantillas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['threaded'] = True

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('', 50001)

# sock.bind(server_address)

# Listen for incoming connections
# sock.listen(1)

global plantilla_seleccionada

plantilla_seleccionada = None
tol = 10
puntos_filtro = [(40, 50), (45, 55), (69, 80)]
global puntos_f
puntos_f = []
global puntos
puntos = []
hsv_blue_min = np.array([50, 100, 20], np.uint8)
hsv_blue_max = np.array([90, 255, 255], np.uint8)


class Plantilla(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True)
    nombre = db.Column(db.String(50), unique=True)
    puntos = db.relationship('Punto', backref='post')

    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    def toJSON(self):
        puntos = Punto.query.filter_by(plantilla=self.codigo).all()
        plantilla = {"id": self.id,
                     "codigo": self.codigo, "nombre": self.nombre,
                     "puntos": [p.toJSON() for p in puntos]}
        return plantilla


class Punto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    validado = db.Column(db.Boolean)
    tol = db.Column(db.Integer)
    plantilla = db.Column(db.Integer, db.ForeignKey('plantilla.codigo'))
    tiempo = db.Column(db.Integer)

    def __init__(self, coor, plantilla, tol=10, tiempo=2):
        if isinstance(coor, tuple):
            self.coordenadas = coor
            self.x = coor[0]
            self.y = coor[1]
            self.validado = False
            self.tol = tol
            self.plantilla = plantilla

            self.tiempo = tiempo
            self.adentro = False

    def toJSON(self):
        punto = {"id": self.id, "x": self.x, "y": self.y,
                 "validado": self.validado, "tol": self.tol, "plantilla": self.plantilla}
        return punto


def isInArea(punto, x, y):
    RMaX = punto.x+punto.tol
    RMaY = punto.y+punto.tol

    RMeX = punto.x-punto.tol
    RMeY = punto.y-punto.tol
    return((x > RMeX) and (y > RMeY) and (x < RMaX) and (y < RMaY))


def validaTiempo(punto):
    global start_time
    global time_count
    if (not punto.adentro):
        time_count = 0
        start_time = time.time()
        punto.adentro = True
    else:
        end_time = time.time()
        time_count = end_time - start_time
    if(time_count >= punto.tiempo):
        validaTiempo.adentro = False
        return True


# cap = cv2.VideoCapture('rtsp://192.168.10.54:8554/cam1')
# cap = cv2.VideoCapture('rtsp://admin:admin123*@10.2.169.72:554/Streaming/Channels/401')
cap = cv2.VideoCapture(0)


def agrega_punto(x, y, tol):
    nuevoPunto = Punto((x, y), plantilla_seleccionada, tol)
    global puntos_f
    puntos_f.append(nuevoPunto)


def dibuja_puntos(image):
    for punto in puntos:
        if (punto.validado):
            cv2.circle(image, (punto.x, punto.y), punto.tol, (255, 0, 0), -1)
        else:
            cv2.circle(image, (punto.x, punto.y), punto.tol, (0, 0, 255), 2)


def validar_punto(puntoActual):

    global puntos
    puntos = Punto.query.filter_by(plantilla=plantilla_seleccionada).all()
    for punto in puntos:
        if isInArea(punto, puntoActual[0], puntoActual[1]):
            if (validaTiempo(punto)):
                punto.validado = True
                db.session.commit()
        else:
            punto.adentro = False
        puntosOK = Punto.query.filter_by(
            plantilla=plantilla_seleccionada, validado=True).all()

        if (len(puntosOK) == len(puntos)):
            for punto in puntosOK:
                punto.validado = False
                db.session.commit()
                punto.adentro = False


def generate_frames():

    while True:
        ret, frame = cap.read()
        if not ret:
            return "algo salio mal"
        else:
            frame = imutils.resize(frame, width=1280)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, hsv_blue_min, hsv_blue_max)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            cnts = cv2.findContours(
                mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            centro = None
            dibuja_puntos(frame)
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((_, _), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                centro = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                if radius > 7:
                    cv2.circle(frame, centro, 3, (0, 0, 255), -1)
                    validar_punto(centro)
                    _, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def event_barcode():

    while True:

        connection, client_address = sock.accept()
        try:
            while True:
                data = connection.recv(50)
                datoStr = data.decode('UTF-8').replace('\n', '')
                datoStr = datoStr.replace('\r', '')
                plantilla_seleccionada = datoStr[4:18]
                print("Filtrado", plantilla_seleccionada)
                yield 'data: %s\n\n' % plantilla_seleccionada

        finally:
            connection.close()


def detectar():
    print("Detectando...")


@app.route('/add_plantilla', methods=['POST'])
def add_plantilla():
    try:
        cod = request.json['codigo']
        nombre = request.json['nombre']
        nuevaPlantilla = Plantilla(codigo=cod, nombre=nombre)
        db.session.add(nuevaPlantilla)
        db.session.commit()
        global plantilla_seleccionada
        plantilla_seleccionada = nuevaPlantilla.codigo
        return Response(json.dumps({"message": "Plantilla Creada"}), 200)
    except Exception as e:
        return Response(json.dumps({"message": str(e)}), 400)


@app.route('/datos')
def home():
    global tol
    global plantilla_seleccionada
    plantillas = Plantilla.query.all()
    datos = {"message": "Exitoso",
             "plantillas": [p.toJSON() for p in plantillas],
             "tol": tol,
             "plantilla_seleccionada": plantilla_seleccionada
             }
    return Response(json.dumps(datos), 200)


@app.route("/plantilla_seleccionada")
def get_plantilla():
    global plantilla_seleccionada
    return Response(json.dumps({"plantilla_seleccionada": plantilla_seleccionada}))


@app.route("/puntos/<plantilla>")
def get_puntos(plantilla):
    puntos = Punto.query.filter_by(plantilla=plantilla).all()
    dataJson = {"message": "Exitoso", "puntos": [ps.toJSON() for ps in puntos]}
    return Response(json.dumps(dataJson), 200)


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/select_plantilla/<codigo>")
def select_plantilla(codigo):
    global plantilla_seleccionada
    plantilla = Plantilla.query.filter_by(codigo=codigo).first()
    if (plantilla):
        plantilla_seleccionada = codigo
        detectar()
    else:
        plantilla_seleccionada = None

        return Response(json.dumps({"message": "Codigo no Existe"}), 400)

    return Response(json.dumps({"message": "Exitoso"}), 200)


@app.errorhandler(404)
def page_not_found(e):

    return Response(json.dumps({"message": "No Encontro la Pagina"}), 404)


@app.route('/add_punto', methods=['POST'])
def add_punto():
    global plantilla_seleccionada
    global tol
    if (plantilla_seleccionada == None):
        #flash("Debe seleccionar una plantilla", 'danger')
        # return redirect(url_for('home'))
        return Response(json.dumps({"message": "Debe Seleccionar una Plantilla"}), 400)

    x = request.args.get('x', default=1, type=int)
    y = request.args.get('y', default=1, type=int)
    tol = request.args.get('tol', default=3, type=int)

    nuevoPunto = Punto((x, y), plantilla=plantilla_seleccionada, tol=tol)
    db.session.add(nuevoPunto)
    db.session.commit()
    return Response(json.dumps({"message": "Exitoso"}), 200)


@app.route('/delete_puntos/<codigo>', methods=["DELETE"])
def delete_puntos(codigo):
    Punto.query.filter_by(plantilla=codigo).delete()
    db.session.commit()
    return Response(json.dumps({"message": "Punto Eliminado"}), 200)


@app.route('/delete_plantilla/<codigo>', methods=['DELETE'])
def delete_plantilla(codigo):
    global puntos
    global plantilla_seleccionada
    puntos = []
    elimina = Plantilla.query.filter_by(codigo=codigo).first()
    if(elimina):
        plantilla_seleccionada = codigo
        Punto.query.filter_by(plantilla=codigo).delete()
        Plantilla.query.filter_by(codigo=codigo).delete()
        db.session.commit()
        return Response(json.dumps({"message": "Plantilla Eliminada"}), 200)
    else:
        plantilla_seleccionada = None
        return Response(json.dumps({"message": "Plantilla No Encontrada"}), 400)


if __name__ == '__main__':
     app.run(debug=True, port=5000, host='0.0.0.0')
    # http_server = WSGIServer(('0.0.0.0', 5000), app)
    # http_server.serve_forever()
    #print("POR FAVOR NO CERRAR ESTA VENTANA!!")
   #serve(app, host="0.0.0.0", port=5000, threads=6)
