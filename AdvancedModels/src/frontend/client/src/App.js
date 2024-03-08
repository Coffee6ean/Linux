import React from "react";
import Navbar from "./components/Nav/Navbar";
import AppRouter from "./routes/AppRouter";

function App() {
  return (
    <div className="App">
      <Navbar/>
      <AppRouter/> 
    </div>
  );
}

export default App;
