import './App.css'
import Loader from './Loader';
import { useState } from 'react';

function ImageUpload() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [predictedClass, setPredictedClass] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (e.type === "dragenter" || e.type === "dragover") {
        setDragActive(true);
      } else if (e.type === "dragleave") {
        setDragActive(false);
      }
    };

    const handleDrop = (e) => {
      e.preventDefault();
      e.stopPropagation();
      setDragActive(false);
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        console.log(e.dataTransfer.files);
        const fileEvent = {
          target: {
              files: e.dataTransfer.files
          }
        };
        handleFileChange(fileEvent);
      }
    };

    const handleFileChange = async (e) => {
      if (e.target.files[0]){
        setIsLoading(true);
      }

      const file = e.target.files[0];
      setSelectedFile(file);

      const tempImageUrl = URL.createObjectURL(file);
      setImageUrl(tempImageUrl);

      const formData = new FormData();
      formData.append('image', file);

      console.log(...formData);

      fetch('https://sinhala-recognition.onrender.com/uploads', {
          method: 'POST',
          body: formData,
      })
      .then(res => res.json())
      .then(response => {
          setIsLoading(false);
          console.log(response);
          const predictedClass = response.class;
          setPredictedClass(predictedClass);
      })
      .catch(error => {
          console.log("Error: ", error);
          setIsLoading(false);
      });
  };

  return (
    <div className='flex justify-evenly items-center w-3/4'>

      <div className='flex flex-col items-center gap-6'>
        
        <div
          className={`drop-zone text-gray-600 border-2 border-dashed bg-gray-200 rounded-xl p-[100px]
                     border-gray-400 flex flex-col gap-5 transition-all text-2xl duration-400 shadow-lg
                    ${dragActive ? "active bg-gray-500 text-white border-white" : ""}`}
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
        >
          <div className='flex flex-col items-center justify-center'>
            <label htmlFor="imageUpload" className="cursor-pointer bg-[#00ADB5] text-white font-bold py-2 px-4 rounded 
                                                  hover:bg-[#51787a] focus:outline-none focus:shadow-outline shadow-md
                                                    hover:shadow-xl transittion-all duration-200 text-lg">
                <i className="fas fa-upload"></i> Upload Image
            </label>
            <input
                type="file"
                id="imageUpload"
                accept="image/*"
                onChange={handleFileChange}
                className="hidden"
            />
          </div>
          <div className='flex justify-center items-center'>
            or
          </div>
          <div>
            Drag and drop files here
          </div>
        </div>
        
        
        {selectedFile && (
          <span className='text-sm text-gray-600 mt-2'>Selected file: {selectedFile.name}</span>
        )}
      </div>

      
      <div className='flex flex-col gap-6 justify-center items-center'>
          {imageUrl && (
            <div>
              <img src={imageUrl} alt="Uploaded" style={{ maxWidth: '100%', maxHeight: '300px' }} />
            </div>
          )}
        
        {isLoading ? (
          <Loader />
          ) : (<div>
                  {predictedClass && (
                      <div className='flex flex-col gap-6'>
                          <div className='text-center text-3xl font-sinhala text-black'>
                              Prediction: {predictedClass}
                          </div>
                          <div className='cursor-pointer bg-[#00ADB5] text-white font-bold py-2 px-4 rounded 
                                        hover:bg-[#51787a] focus:outline-none focus:shadow-outline shadow-md
                                        hover:shadow-xl transittion-all duration-200 text-lg
                                        flex items-center justify-center max-w-fit text-center'
                              onClick={() => navigator.clipboard.writeText(predictedClass)}
                          >
                              Copy to Clipboard
                          </div>
                      </div>
                  )}
                </div>
          )}
      </div>
    </div>
  );
}

export default ImageUpload;
