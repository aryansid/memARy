import { Inter } from 'next/font/google'
import Navbar from '@/components/navbar'
import { useRef, useState } from 'react';
import {Camera} from "react-camera-pro";
//@ts-ignore


const inter = Inter({ subsets: ['latin'] });

export default function Home() {
  const camera = useRef(null);
  const [image, setImage] = useState(null);
  
  return (
    <main className="flex-col">
      <h1>
        home page
      </h1>
      <div className="flex justify-center">
        <Camera ref={camera} errorMessages={{
          noCameraAccessible: 'no camera accessible',
          permissionDenied: 'permission denied',
          switchCamera: 'switch cameras',
          canvas: 'canvas',
        }} />
      </div>
    </main>
  )
}
