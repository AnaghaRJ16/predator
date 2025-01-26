import React from 'react';
import { Navbar } from './components'; 
import { Home } from './containers';
import { Weather } from './containers';
import { Chatbot } from './containers';
import { About } from './containers';
import { Contact } from './containers';


const App = () => {
  return (
    <div>
      <nav>
      <div className="App">
      <div className="gradient__bg">

        <Navbar />
        <Home />
        <Weather />
        <Chatbot />
        <About />
        <Contact />
      </div>
      </div>
      </nav>
    </div>
  );
}

export default App;