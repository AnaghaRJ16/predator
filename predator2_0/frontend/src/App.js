import React from 'react';
import Navbar from './components/Navbar/Navbar';
import Home from './containers/home/home';
import Chatbot from './containers/chatbot/chatbot';


const App = () => {
  return (
    <div>
      <nav>
      <div className="App">
      <div className="gradient__bg">

        <Navbar />
        <Home />
        <Chatbot />
      </div>
      </div>
      </nav>
    </div>
  );
}

export default App;