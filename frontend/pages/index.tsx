import { Inter } from 'next/font/google'
import Navbar from '@/components/navbar'
const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  return (
    <main
      className={`flex-col`}
    >
      <h1>
        home page
      </h1>
      <Navbar/>
    </main>
  )
}
