import { createContext, useState, useEffect } from "react";

export const PlantillaContext = createContext();

export function PlantillaContextProvider(props) {
  const [plantillas, setPlantillas] = useState([]);
  const [tolerancia, setTolerancia] = useState(20);
  const [codigo, setCodigo] = useState("");
  const [nombre, setNombre] = useState("");

  const getPlantillas = () => {
    fetch("/datos").then((response) => {
      response.json().then((texto) => {
        setPlantillas(texto.plantillas);
      });
    });
  };

  const eliminaPuntos = (plantilla) => {
    const url = `/delete_puntos/${plantilla}`;
    fetch(url, { method: "DELETE" }).then((response) => {
      if (response.status === 200) {
        getPlantillas();
      } else {
        alert("Ocurrio un error");
      }
    });
  };

  const eliminaPlantilla = (plantilla) => {
    var acepto = window.confirm(
      `Esta seguro de eliminar la plantilla ${plantilla}`
    );
    if (!acepto) return;
    const url = `/delete_plantilla/${plantilla}`;
    fetch(url, { method: "DELETE" }).then((response) => {
      response.json().then((dataJson) => {
        getPlantillas();
      });
    });
  };

  const agregarPunto = (event) => {
    // fetch("/plantilla_seleccionada").then((response) => {
    //   response.json().then((dataJson) => {
    //     if (dataJson.plantilla_seleccionada == null) {
    //       alert("Debe seleccionar una plantilla");
    //       return;
    //     }
    //   });
    // });
    const localX = event.clientX - event.target.offsetLeft;
    const localY = event.clientY - event.target.offsetTop;

    const url = `/add_punto?x=${localX}?y=${localY}?tol=${tolerancia}`;
    fetch(url, { method: "POST" }).then((response) => {
      response.json().then((dataJson) => {
        if (dataJson.message !== "Exitoso") {
          alert(dataJson.message);
        }
      });
      getPlantillas()
    });
  };

  const seleccionarPlantilla = (plantilla) => {
    const url = `/select_plantilla/${plantilla}`;
    fetch(url).then((response) => {});
  };

  useEffect(() => {
    getPlantillas();
  }, []);

  const crearPlantilla = () => {
    if (nombre.length <= 0 || codigo.length <= 0) {
      alert("Complete todos los campos");
      return;
    }
    var datos = JSON.stringify({
      nombre: nombre,
      codigo: codigo,
    });
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: datos,
    };
    fetch("/add_plantilla", requestOptions).then((response) => {
      let estado = response.status;
      if (estado !== 200) {
        alert("Ocurrio un error");
      } else {
        response.json().then((datoJson) => {
          if (datoJson.hasOwnProperty("message")) {
            setCodigo("");
            setNombre("");
          }
        });
      }
    });
    getPlantillas()
  };

  return (
    <PlantillaContext.Provider
      value={{
        nombre,
        setNombre,
        codigo,
        setCodigo,
        plantillas,
        setPlantillas,
        tolerancia,
        setTolerancia,
        crearPlantilla,
        eliminaPlantilla,
        agregarPunto,
        eliminaPuntos,
        seleccionarPlantilla,
      }}
    >
      {props.children}
    </PlantillaContext.Provider>
  );
}
