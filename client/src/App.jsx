import './App.css'
import ImageUpload from './ImageUpload';
import Header from './Header'
import Canvas from './Canvas';

import { useState } from 'react';

function App() {
  const [mode, setMode] = useState(true);  //true is file upload

  const handleToggle = (id) => {
    setMode(id);
  }

  return (
    <div className='flex flex-col items-center justify-evenly h-[100vh] text-white bg-[#EEEEEE] '>
      <div className='absolute top-0 w-full flex flex-col'>
        <div className=' pb-3 bg-[#222831]'>
          <Header />
        </div>
        <div className='flex justify-evenly bg-black-white-gradient cursor-pointer'>
          <div onClick={() => handleToggle(true)} className={`w-full h-[60px] p-3 flex justify-center transition-all duration-[250ms]
                                                              items-center text-md
                                                              ${mode ? 
                                                              'bg-[#EEEEEE] border-[#EEEEEE] shadow-inner-shadow w-[125%] text-xl text-[#222831] rounded-t-xl' 
                                                              : 
                                                              'bg-[#222831] text-[#EEEEEE] rounded-br-xl'}`}>
            File Upload
          </div>
          <div onClick={() => handleToggle(false)} className={`w-full h-[60px] p-3 flex justify-center transition-all duration-[250ms]
                                                              items-center text-md
                                                              ${mode ? 
                                                              'bg-[#222831] text-[#EEEEEE] rounded-bl-xl' 
                                                              : 
                                                              'bg-[#EEEEEE] border-[#EEEEEE] shadow-inner-shadow w-[125%] text-xl text-[#222831] rounded-t-xl'}`}>
            Canvas
          </div>
        </div>
      </div>
        
      {mode ? (
        <ImageUpload />
      ) : (
        <Canvas />
      )}
    </div>
  );
}

export default App;