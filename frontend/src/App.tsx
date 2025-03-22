import React, { useState } from 'react';
import './App.css';
import MindMap from './components/MindMap';
import Navbar from './components/Navbar';
import ResourceSidebar from './components/ResourceSidebar';
import SearchBar from './components/SearchBar';
import FeaturedResources from './components/FeaturedResources';
import SkillProgress from './components/SkillProgress';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeView, setActiveView] = useState<'mindmap' | 'resources' | 'skills'>('mindmap');
  
  const handleSearch = (query: string) => {
    setSearchQuery(query);
    console.log('Searching for:', query);
  };

  return (
    <div className="App">
      <Navbar />
      <div className="background">
        <div className="view-toggle">
          <button 
            className={`toggle-btn ${activeView === 'mindmap' ? 'active' : ''}`}
            onClick={() => setActiveView('mindmap')}
          >
            Career Mind Map
          </button>
          <button 
            className={`toggle-btn ${activeView === 'resources' ? 'active' : ''}`}
            onClick={() => setActiveView('resources')}
          >
            Featured Resources
          </button>
          <button 
            className={`toggle-btn ${activeView === 'skills' ? 'active' : ''}`}
            onClick={() => setActiveView('skills')}
          >
            Skill Tracker
          </button>
        </div>
        <div className="card">
          <div className="app-container">
            <ResourceSidebar />
            <div className="main-content">
              <SearchBar onSearch={handleSearch} />
              {activeView === 'mindmap' && <MindMap />}
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
