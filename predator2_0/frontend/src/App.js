import React from "react";
import "./App.css";

import { Footer } from "./containers"; 
  
import { Navbar } from "./components";

const App = () => {
  return (
    <div className="App">
      <div className="gradient__bg">
        <Navbar />
        
      </div>      
      

      <Footer />
     
    </div>
  );
};

export default App;
