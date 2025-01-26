import React from 'react';
import { Navbar } from './components'; 
import { Home } from './containers';
import { Weather } from './containers';
import { ChatBot } from './containers';
import { About } from './containers';
import { Contact } from './containers';


const App = () => {
  return (
    <div>
      <nav>
        <p>
          <a href="#home">Home</a>
        </p>
        <p>
          <a href="#weather">Weather Forecasting</a>
        </p>
        <p>
          <a href="#chatbot">ChatBot</a>
        </p>
        <p>
          <a href="#aboutus">About Us</a>
        </p>
        <p>
          <a href="#contactus">Contact Us</a>
        </p>
      </nav>

      <div id="home">
        <home />
      </div>
      <div id="weather">
        <weather />
      </div>
      <div id="chatbot">
        <chatBot />
      </div>
      <div id="about">
        <About />
      </div>
      <div id="contact">
        <Contact />
      </div>
    </div>
  );
};

export default App;