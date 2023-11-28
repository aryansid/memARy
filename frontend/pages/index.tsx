import { Inter } from 'next/font/google'
import Navbar from '@/components/navbar'
import Camera from 'react-html5-camera-photo'

const inter = Inter({ subsets: ['latin'] });

export default function Home() {
  return (
    <main className="flex-col">
      <h1>
        home page
      </h1>
      <div className="flex justify-center">
        <Camera/>
      </div>
    </main>
  )
}
