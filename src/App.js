
import './App.css';
import Formulario from './components/formulario';
import './index.css';
import logoHtg from './img/logo-HTG-blanco.png'
import logohaceb from './img/logo-haceb.png'
function App() {
  return (
    <div>
      <div className="bg-gradient-to-r  from-orange-400	to-indigo-900">
        <div  className='flex justify-start'>
      <img src={logoHtg} alt='logo-htg-blanco' className='h-40 pb-5'></img>
      <img src={logohaceb}alt='logo-haceb'className='h-40'></img>
    </div>
   <div>
      <div className="bg-white h-96 w-3/5 ml-5 border-x-2 border-t-2 border-indigo-900">
        </div>
        </div>
        <div className="bg-white h-96 w-3/5 ml-5 border-r-2 border-l-2 border-indigo-900">
        </div>
        <table className=" ml-5 mr-10 mt-20 float-right absolute top-20  right-0">
          <thead className="border-y-4 divide-y divide-slate-200">
            <tr>
              <th className='pl-5 pr-5 text-white'>Código</th>
              <th className='pl-5 pr-5 text-white'>Nombre</th>
              <th className='pl-5 pr-5 text-white'>Puntos</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-y-4 divide-y divide-slate-200">
              <td className="text-center pl-5 text-white border-y-4 divide-y divide-slate-200">
                32574398765432
              </td>
              <td className="text-center text-white border-y-4 divide-y divide-slate-200">
                Test
              </td>
              <td className="text-center text-white">
                7
                <button className="rounded-t-lg  rounded-b bg-sky-600 float-right pl-2 pr-2 pb-2 mr-5  text-white">x</button>

              </td>
              <td className="text-center text-white border-y-4 divide-y divide-slate-200">
              </td>
              <td>
                <button className='rounded-md bg-red-500 float-right pl-5 pr-5  text-white'>Eliminar</button>
              </td>
            </tr>
            <tr className="border-y-4 divide-y divide-slate-200">
              <td className="text-center text-white pl-5 border-y-4 divide-y divide-slate-200">
                123456789
              </td>
              <td className="text-center text-white border-y-4 divide-y divide-slate-200">
                Otra2
              </td>
              <td className="text-center text-white">
                5
                <button className="rounded-t-lg  rounded-b bg-sky-600 float-right pl-2 pr-2 pb-2 mr-5 text-white">x</button>

              </td>
              <td className="text-center text-white border-y-4 divide-y divide-slate-200">

              </td>
              <td>
                <button className='rounded-md bg-red-500 float-right pl-5 pr-5  text-white'>Eliminar</button>
              </td>
            </tr>
            <tr className="border-y-4 divide-y divide-slate-200">
              <td className="text-center text-white pl-5 border-y-4 divide-y divide-slate-200">
                077043534222818
              </td>
              <td className="text-center text-white border-y-4 divide-y divide-slate-200">
                Nevera1
              </td>
              <td className="text-center text-white">
                9
                <button className="rounded-t-lg  rounded-b bg-sky-600 float-right pl-2 pr-2 pb-2 mr-5  text-white">x</button>

              </td>
              <td className="text-center text-white border-y-4 divide-y divide-slate-200">

              </td>
              <td>
                <button className='rounded-md bg-red-500 float-right pl-5 pr-5  text-white'>Eliminar</button>
              </td>
            </tr>
            <tr className="border-y-4 divide-y divide-slate-200">
              <td className="text-center text-white  pl-5 border-y-4 divide-y divide-slate-200">
                432
              </td>
              <td className="text-center text-white border-y-4 divide-y divide-slate-200">
                Tes
              </td>
              <td className="text-center text-white">
                5
                <button className="rounded-t-lg  rounded-b bg-sky-600 float-right pl-2 pr-2 pb-2 mr-5 text-white">x</button>

              </td>
              <td className="text-center border-y-4 divide-y divide-slate-200">

              </td>
              <td>
                <button className='rounded-md bg-red-500 float-right pl-5 pr-5  text-white'>Eliminar</button>
              </td>
            </tr>

          </tbody>
        </table>

        <Formulario />
      </div>
      </div>
      
    
  );
}

export default App;
