import React from 'react'

export default function InputCard({setHumanMessage,saySomething}) {
  return (
    <div>
        
        <input onChange={(e)=>setHumanMessage(e.target.value)}></input>
        <button onClick={() => saySomething()}>chat</button>


    
    </div>
  )
}
