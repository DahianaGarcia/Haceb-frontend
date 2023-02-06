import React from "react";
import logoHtg from "../img/logo-HTG-blanco.png";
import logohaceb from "../img/logo-haceb.png";
import {  useContext } from "react";
import { PlantillaContext } from "../context/context";

export default function TablaPlantillas() {

  const {plantillas, seleccionarPlantilla, agregarPunto, eliminaPlantilla, eliminaPuntos} = useContext(PlantillaContext)

  return (
    <div>
      <div className="bg-gradient-to-r  from-orange-400	to-indigo-900">
        <div className="flex justify-start">
          <img src={logoHtg} alt="logo-htg-blanco" className="h-40 pb-5"></img>
          <img src={logohaceb} alt="logo-haceb" className="h-40"></img>
        </div>
        <div>
          <div
            className="bg-white-200 h-96 w-3/5 ml-5 border-x-2 border-t-2 border-indigo-900"
            onClick={(e) => {
              agregarPunto(e);
            }}
          >
            {/* <img src="/video" alt="video" /> */}
          </div>
        </div>
        <div className="bg-white-200 h-96 w-3/5 ml-5 border-r-2 border-l-2 border-indigo-900"></div>
        <table className="ml-5 mr-10 mt-20 float-right absolute top-20  right-0">
          <thead className="border-y-4 divide-y divide-slate-200">
            <tr>
              <th className="pl-5 pr-5 text-white">Código</th>
              <th className="pl-5 pr-5 text-white">Nombre</th>
              <th className="pl-5 pr-5 text-white">Puntos</th>
            </tr>
          </thead>

          <tbody>
            {plantillas.map((plantilla, index) => {
              return (
                <tr
                  className="border-y-4 divide-y divide-slate-200"
                  key={index}
                  onClick={() => seleccionarPlantilla(plantilla.codigo)}
                >
                  <td className="text-center pl-5 text-white border-y-4 divide-y divide-slate-200">
                    {plantilla.codigo}
                  </td>
                  <td className="text-center text-white border-y-4 divide-y divide-slate-200">
                    {plantilla.nombre}
                  </td>
                  <td className="text-center text-white">
                    {plantilla.puntos.length}
                    <button
                      onClick={() => eliminaPuntos(plantilla.codigo)}
                      className="rounded-t-lg  rounded-b bg-sky-600 float-right pl-2 pr-2 pb-2 mr-5  text-white"
                    >
                      x
                    </button>
                  </td>
                  <td>
                    <button
                      onClick={() => {
                        eliminaPlantilla(plantilla.codigo);
                      }}
                      className="rounded-md bg-red-500 float-right pl-5 pr-5  text-white"
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
    
      
      

