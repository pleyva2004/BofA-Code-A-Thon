import React, { useState } from 'react';
import './App.css';
import MindMap from './components/MindMap';
import MindMapBE from './components/MindMapBE';
import MindMapAI from './components/MindMapAI';
import Navbar from './components/Navbar';
import ResourceSidebar from './components/ResourceSidebar';
//import SearchBar from './components/SearchBar';
import FeaturedResources from './components/FeaturedResources';
import SkillProgress from './components/SkillProgress';

function App() {
  //const [searchQuery, setSearchQuery] = useState('');
  const [activeView, setActiveView] = useState<'mindmap' | 'mindmapbe' | 'mindmapai' | 'resources' | 'skills'>('mindmap');
  /*
  const handleSearch = (query: string) => {
    setSearchQuery(query);
    console.log('Searching for:', query);
  };
*/
  return (
    <div className="App">
      <Navbar />
      <div className="background">
        <div className="view-toggle">
          <button 
            className={`toggle-btn ${activeView === 'mindmap' ? 'active' : ''}`}
            onClick={() => setActiveView('mindmap')}
          >
            Front End Developer
          </button>
          <button 
            className={`toggle-btn ${activeView === 'mindmapbe' ? 'active' : ''}`}
            onClick={() => setActiveView('mindmapbe')}
          >
            Back End Developer
          </button>
          <button 
            className={`toggle-btn ${activeView === 'mindmapai' ? 'active' : ''}`}
            onClick={() => setActiveView('mindmapai')}
          >
            AI/ML Engineer
          </button>
        </div>
        <div className="card">
          <div className="app-container">
            <ResourceSidebar /> {/*left section of website, commenting the tag out will remove that sections*/}
            <div className="main-content">
              {/*
              <SearchBar onSearch={handleSearch} />
              */} 
              {activeView === 'mindmap' && <MindMap />}
              {activeView === 'mindmapbe' && <MindMapBE />}
              {activeView === 'mindmapai' && <MindMapAI />}
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
