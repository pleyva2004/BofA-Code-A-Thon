import React from 'react';

interface ResourceCardProps {
  title: string;
  description: string;
  category: string;
  link?: string;
}

const ResourceCard: React.FC<ResourceCardProps> = ({ title, description, category, link }) => {
  return (
    <div className="resource-card">
      <span className="resource-category">{category}</span>
      <h3>{title}</h3>
      <p>{description}</p>
      {link && (
        <a 
          href={link} 
          target="_blank" 
          rel="noopener noreferrer"
          style={{
            display: 'inline-block',
            marginTop: '1rem',
            color: '#4285f4',
            fontWeight: 500,
            textDecoration: 'none',
            fontSize: '0.9rem'
          }}
        >
          Learn more →
        </a>
      )}
    </div>
  );
};

const FeaturedResources: React.FC = () => {
  const resources = [
    {
      title: 'LinkedIn Profile Optimization',
      description: 'Learn how to create a compelling LinkedIn profile that attracts recruiters.',
      category: 'Networking',
      link: '#'
    },
    {
      title: 'Technical Interview Preparation',
      description: 'Strategies and practice resources for acing technical interviews.',
      category: 'Interviews',
      link: '#'
    },
    {
      title: 'Personal Project Portfolio',
      description: 'How to build and showcase personal projects to stand out to employers.',
      category: 'Portfolio',
      link: '#'
    },
    {
      title: 'Resume Building Workshop',
      description: 'Templates and tips for creating a resume that gets past ATS systems.',
      category: 'Resume',
      link: '#'
    },
    {
      title: 'Networking for Introverts',
      description: 'Effective networking strategies for those who find networking challenging.',
      category: 'Soft Skills',
      link: '#'
    },
    {
      title: 'Industry Mentorship Programs',
      description: 'Connect with experienced professionals in your field for guidance.',
      category: 'Mentorship',
      link: '#'
    }
  ];

  return (
    <div style={{ padding: '0 1.5rem 1.5rem', overflow: 'auto' }}>
      <h2 style={{ 
        textAlign: 'left', 
        margin: '1.5rem 0', 
        fontSize: '1.5rem',
        fontWeight: 600, 
        color: '#333' 
      }}>
        Featured Resources for Students
      </h2>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
        gap: '1.5rem' 
      }}>
        {resources.map((resource, index) => (
          <ResourceCard 
            key={index}
            title={resource.title}
            description={resource.description}
            category={resource.category}
            link={resource.link}
          />
        ))}
      </div>
    </div>
  );
};

export default FeaturedResources; 