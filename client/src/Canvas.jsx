import Loader from './Loader';
import { useEffect, useRef, useState } from 'react';

const Canvas = () => {
    const canvasRef = useRef(null);
    const [isDrawing, setIsDrawing] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [predictedClass, setPredictedClass] = useState(null);

    const startDrawing = (e) => {
        const { offsetX, offsetY } = e.nativeEvent;
        const context = canvasRef.current.getContext('2d');
        context.strokeStyle = 'white';
        context.lineWidth = 5;
        context.lineCap = 'round';
        context.beginPath();
        context.moveTo(offsetX, offsetY);
        setIsDrawing(true);
    };

    const draw = (e) => {
        if (!isDrawing) {
        return;
        }
        const { offsetX, offsetY } = e.nativeEvent;
        const context = canvasRef.current.getContext('2d');
        context.lineTo(offsetX, offsetY);
        context.stroke();
    };

    const finishDrawing = () => {
        const context = canvasRef.current.getContext('2d');
        context.closePath();
        setIsDrawing(false);
    };

    const clearCanvas = () => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.fillStyle = 'black';
        context.fillRect(0, 0, context.canvas.width, context.canvas.height);
    };

    const sendImage = async () => {
        setIsLoading(true);
        const canvas = canvasRef.current;
        canvas.toBlob(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'canvas-image.png');
            fetch('http://127.0.0.1:5000/uploads', {
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
        }, 'image/png');
    }

    useEffect(() => {
        const context = canvasRef.current.getContext('2d');
        context.fillStyle = 'black';
        context.fillRect(0, 0, context.canvas.width, context.canvas.height);
      }, []);
      
    
  return (
    <div className='flex justify-evenly items-center w-3/4'>
        <div className='flex flex-col gap-[20px]'>
            <canvas 
                className='border-2 border-[#00ADB5] rounded-xl' 
                ref={canvasRef}
                width="320" height="320"
                onMouseDown={startDrawing}
                onMouseMove={draw}
                onMouseUp={finishDrawing}
                onMouseLeave={finishDrawing}
            />
            <div className='flex justify-evenly'>
                <div className='cursor-pointer bg-[#00ADB5] text-white font-bold py-2 px-4 rounded 
                                hover:bg-[#51787a] focus:outline-none focus:shadow-outline shadow-md
                                hover:shadow-xl transittion-all duration-200 text-lg'
                    onClick={sendImage}   
                >
                    Predict
                </div>
                <div className='cursor-pointer bg-[#00ADB5] text-white font-bold py-2 px-4 rounded 
                                hover:bg-[#51787a] focus:outline-none focus:shadow-outline shadow-md
                                hover:shadow-xl transittion-all duration-200 text-lg'
                    onClick={clearCanvas}
                >
                    Clear
                </div>
            </div>
        </div>
        <div className='flex flex-col gap-6'>
            {isLoading ? (
            <Loader />
            ) : (<div>
                    {predictedClass && (
                        <div className='flex flex-col gap-6 items-center'>
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
  )
}

export default Canvas