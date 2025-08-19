import { useState } from 'react'
import './App.css'

import InputCard from './componets/InputCard/InputCard.jsx'

function App() {
  const [messages,setMessages] = useState([])
  const [humanMessage,setHumanMessage] = useState("")
  const [id,SetID] = useState(null)
  
  async function saySomething() {
    setMessages(prev => [...prev, humanMessage])

    try {
      console.log(import.meta.env.VITE_BACKEND_URL)
    const res = await fetch(import.meta.env.VITE_BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: humanMessage,id}),
    });
    
    const data = await res.json();
      SetID(data.id)
      setMessages(prev => [...prev, data.response])


    
  } catch (err) {
    console.error("Error:", err);
  }

  }




  return (
    <>
    
    

     {messages.map((message, index) => (
        <p key={index}>{message}</p>
      ))}

      <InputCard setHumanMessage = {setHumanMessage} saySomething = {saySomething}/>


    
    </>
  )
}

export default App
