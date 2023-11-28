import { useRef, useState } from "react";
import {Camera} from "react-camera-pro";

export default function MainCamera() {
  const camera = useRef(null);
  const [image, setImage] = useState(null);
  
  return (
  <div className="flex flex-col lg:justify-between items-center h-[50rem]">
    <div className="flex self-center h-[60%] w-[80%] m-4">
      <Camera 
        ref={camera} 
        facingMode='environment'
        aspectRatio={16/9} 
        errorMessages={
          {
            noCameraAccessible: 'no camera accessible',
            permissionDenied: 'permission denied',
            switchCamera: 'switch cameras',
            canvas: 'canvas',
          }
        } 
      />
    </div>
    <div className="flex flex-row">
      <button
        className="w-14 h-4 bg-white text-black m-4 text-sm	"
        onClick={() => {
          //@ts-ignore
          camera.current.switchCamera();
        }}
      >
        Switch Camera
      </button>
      <button onClick={
        () => {
          //@ts-ignore
          setImage(camera.current.takePhoto());
          console.log("photo taken");
          console.log(image);
        }
      }>
        Take photo
      </button>
    </div>
  </div>
  )
};