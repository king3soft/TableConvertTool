import React from 'react'
import Window from "./window";

class App extends React.Component {
  render() {
    return(
      <div style={{position: "relative", width:"100%", height: "100%"}}>
        <Window/>
      </div>
    )
  }
}

export  default App