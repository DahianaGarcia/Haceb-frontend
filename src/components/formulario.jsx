import React, { useContext } from "react";
import { PlantillaContext } from "../context/context";

const Formulario = () => {
  const { tolerancia, setTolerancia, codigo, setCodigo, nombre, setNombre, crearPlantilla } =
    useContext(PlantillaContext);

  return (
    <div className="float-right absolute top-60 bottom-15 mt-80  mr-10  ml-10 right-0 w-full max-w-md h-20  mr-0 ml-5">
      <div className="flex min-h-full items-center justify-center py-5 px-4 sm:px-6 md:ml-10 mr-10 lg:px-8">
        <div className="w-full max-w-md space-y-8">
          <div className="mt-8 space-y-6">
            <div className="-space-y-px rounded-md shadow-sm">
              <div>
                <input
                  id="codigo"
                  name="codigo"
                  type="text"
                  required
                  className="relative block w-full appearance-none rounded-none rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="Código"
                  onChange={(e) => {
                    setCodigo(e.target.value);
                  }}
                  value={codigo}
                />
              </div>
              <div>
                <input
                  id="nombre"
                  name="nombre"
                  type="text"
                  required
                  className="relative block w-full appearance-none rounded-none rounded-b-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="Nombre"
                  onChange={(e) => {
                    setNombre(e.target.value);
                  }}
                  value={nombre}
                />
                <input
                  id="minmax-range"
                  type="range"
                  min="10"
                  max="50"
                  defaultValue={tolerancia}
                  onChange={(e) => setTolerancia(e.target.value)}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
                ></input>

                <label className="block mb-2 text-sm font-medium text-white">
                  Tolerancia={tolerancia}
                </label>
                <button
                  className="bg-orange-400 rounded-md  pr-5 pl-5 text-white"
                  onClick={crearPlantilla}
                >
                  Crear Plantilla
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Formulario;
