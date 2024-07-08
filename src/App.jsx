import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Home from './pages/Home'
import About from './pages/About'
import AddCar from './pages/AddCar'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from './Layout';


function App() {
  const [count, setCount] = useState(0)

  return (
    <BrowserRouter>
     <Routes>
       <Route path='/' element={<Layout />}>
          <Route path='/' element={<Home />} />
          <Route path='/about' element={<About />} />
          <Route path='/addcar 'element={<AddCar/>} />
        </Route>
     </Routes>
   </BrowserRouter>
  )
}

export default App
