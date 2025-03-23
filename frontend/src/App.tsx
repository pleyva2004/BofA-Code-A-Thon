import React, { useState } from 'react';
import './App.css';
import MindMap from './components/MindMap';
import MindMapBE from './components/MindMapBE';
import MindMapAI from './components/MindMapAI';
import MindMapCyber from './components/MindMapCyber';
import MindMapGD from './components/MindMapGD';
import MindMapDS from './components/MindMapDS';

import Navbar from './components/Navbar';
import ResourceSidebar from './components/ResourceSidebar';
//import SearchBar from './components/SearchBar';
import FeaturedResources from './components/FeaturedResources';
import SkillProgress from './components/SkillProgress';
import UniversitySelector from './components/UniversitySelector';
import CourseDataFetcher from './components/CourseDataFetcher';

function App() {
  // Existing active view state
  const [activeView, setActiveView] = useState<'mindmap' | 'mindmapbe' | 'mindmapai' | 'mindmapcyber'| 'mindmapgd' | 'mindmapds' | 'resources' | 'skills'>('mindmap');
  
  // Lift state for the selected university.
  const [selectedUniversity, setSelectedUniversity] = useState("New Jersey Institute of Technology");

  // For simplicity, we hardcode a career here.
  const [career, setCareer] = useState("AI Engineer");

  return (
    <div className="App">
      <Navbar />

      {/* University selector placed after the Navbar.
          It now receives the selectedUniversity value and a setter function so that any change here updates the lifted state */}
      <UniversitySelector 
        selectedUniversity={selectedUniversity} 
        setSelectedUniversity={setSelectedUniversity} 
      />

      {/*THIS FEATURE DOESNT WORK CAUSE IT NEEDS TO SEND THE NAME TO THE BACKEND AND I COULDNT IMPLEMENT A BACKEND
      CAUSE I WAS SO BURNT AND COOKED, NOW BUSY
       CourseDataFetcher uses the shared state.
          When the user clicks the fetch button, it will use the selectedUniversity and career to trigger your backend processing */}
      <CourseDataFetcher 
        universityName={selectedUniversity} 
        career={career} 
      />

      <div className="background">
        <div className="view-toggle">
          <button 
            className={`toggle-btn ${activeView === 'mindmap' ? 'active' : ''}`}
            onClick={() => setActiveView('mindmap')}
          >
            Frontend Developer
          </button>
          <button 
            className={`toggle-btn ${activeView === 'mindmapbe' ? 'active' : ''}`}
            onClick={() => setActiveView('mindmapbe')}
          >
            Backend Developer
          </button>
          <button 
            className={`toggle-btn ${activeView === 'mindmapai' ? 'active' : ''}`}
            onClick={() => setActiveView('mindmapai')}
          >
            AI Engineer
          </button>
          <button 
            className={`toggle-btn ${activeView === 'mindmapcyber' ? 'active' : ''}`}
            onClick={() => setActiveView('mindmapcyber')}
          >
            Cybersecurity
          </button>
          <button 
            className={`toggle-btn ${activeView === 'mindmapgd' ? 'active' : ''}`}
            onClick={() => setActiveView('mindmapgd')}
          >
            Game Development
          </button>
          <button 
            className={`toggle-btn ${activeView === 'mindmapds' ? 'active' : ''}`}
            onClick={() => setActiveView('mindmapds')}
          >
            Data Science
          </button>
        </div>
        <div className="card">
          <div className="app-container">
            <ResourceSidebar /> {/* Left section */}
            <div className="main-content">
              {/* 
              <SearchBar onSearch={handleSearch} />
              */}
              {activeView === 'mindmap' && <MindMap />}
              {activeView === 'mindmapbe' && <MindMapBE />}
              {activeView === 'mindmapai' && <MindMapAI />}
              {activeView === 'mindmapcyber' && <MindMapCyber />}
              {activeView === 'mindmapgd' && <MindMapGD />}
              {activeView === 'mindmapds' && <MindMapDS />}

              {activeView === 'resources' && <FeaturedResources />}
              {activeView === 'skills' && <SkillProgress />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
