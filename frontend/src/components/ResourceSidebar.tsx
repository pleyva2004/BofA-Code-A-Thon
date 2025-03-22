import React from 'react';

interface ResourceItemProps {
  icon: string;
  text: string;
}

const ResourceItem: React.FC<ResourceItemProps> = ({ icon, text }) => {
  return (
    <div className="resource-item">
      <span className="resource-item-icon">{icon}</span>
      <span className="resource-item-text">{text}</span>
    </div>
  );
};

const ResourceSidebar: React.FC = () => {
  return (
    <div className="sidebar">
      <div>
        <h2 className="sidebar-title">Explore Resources</h2>
        <div className="tag-container">
          <span className="tag active">All</span>
          <span className="tag">Tutorials</span>
          <span className="tag">Projects</span>
          <span className="tag">Communities</span>
          <span className="tag">Interviews</span>
        </div>
      </div>
      
      <div>
        <h2 className="sidebar-title">Top Resources</h2>
        <div className="resource-list">
          <ResourceItem icon="📚" text="Learning Paths" />
          <ResourceItem icon="💼" text="Resume Templates" />
          <ResourceItem icon="🎯" text="Interview Prep" />
          <ResourceItem icon="🌐" text="Network Opportunities" />
          <ResourceItem icon="📝" text="Skill Assessments" />
          <ResourceItem icon="🔍" text="Job Search Strategies" />
        </div>
      </div>
      
      <div>
        <h2 className="sidebar-title">Career Levels</h2>
        <div className="resource-list">
          <ResourceItem icon="🎓" text="Student" />
          <ResourceItem icon="🚀" text="Entry Level" />
          <ResourceItem icon="⚙️" text="Mid-Career" />
          <ResourceItem icon="👑" text="Senior/Lead" />
          <ResourceItem icon="🏆" text="Management" />
        </div>
      </div>
      
      <div>
        <h2 className="sidebar-title">Latest Articles</h2>
        <div className="resource-card">
          <span className="resource-category">Career Growth</span>
          <h3>Top Skills for 2024</h3>
          <p>Discover which skills are most in-demand for tech professionals this year.</p>
        </div>
        <div className="resource-card">
          <span className="resource-category">Development</span>
          <h3>Learning Paths for Beginners</h3>
          <p>Step-by-step guides to help you navigate your career journey.</p>
        </div>
      </div>
    </div>
  );
};

export default ResourceSidebar; 