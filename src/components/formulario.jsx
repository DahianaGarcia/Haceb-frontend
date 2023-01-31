
function  Formulario() {
  return (
  


<div className="float-right absolute top-50 bottom-40 mr-10 right-0 w-full max-w-md space-y-8 border-2 border-orange-600">
     
<div className="flex min-h-full items-center justify-center py-5 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md space-y-8">
        <form className="mt-8 space-y-6" action="#" method="POST">
          <div className="-space-y-px rounded-md shadow-sm">
              <div>
              <input
                  id="codigo"
                  name="codigo"
                  type="number"
                required
                  className="relative block w-full appearance-none rounded-none rounded-t-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
                  placeholder="Código"
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
                />
                <input id="minmax-range" type="range" min="10" max="50" defaultValue class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"></input>
                <label class="block mb-2 text-sm font-medium text-white">Tolerancia=20</label>
             <button className="bg-orange-400 rounded-md  pr-5 pl-5 text-white">Crear Plantilla</button>
   
             </div>
              

          </div>
          
          </form>
          </div>
          </div>
          </div>


 
      
 
    

  
    
  )
};



export default Formulario;