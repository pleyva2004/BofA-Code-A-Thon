import React from 'react';
import './App.css';
import MindMap from './components/MindMap';
import Navbar from './components/Navbar';

function App() {
  return (
    <div className="App">
      
      <div className="background">
        <Navbar />
        <div className="card">
          <MindMap />
        </div>
      </div>
    </div>
  );
}

export default App;
