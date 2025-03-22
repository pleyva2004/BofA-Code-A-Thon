import React from 'react';

interface SkillBarProps {
  skill: string;
  progress: number;
  color?: string;
}

const SkillBar: React.FC<SkillBarProps> = ({ skill, progress, color = '#4285f4' }) => {
  return (
    <div style={{ marginBottom: '1.2rem' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between',
        marginBottom: '0.5rem'
      }}>
        <span style={{ fontWeight: 500, fontSize: '0.95rem', color: '#444' }}>{skill}</span>
        <span style={{ fontSize: '0.85rem', color: '#666' }}>{progress}%</span>
      </div>
      <div style={{ 
        height: '8px', 
        backgroundColor: '#f1f3f4', 
        borderRadius: '4px',
        overflow: 'hidden'
      }}>
        <div style={{ 
          width: `${progress}%`, 
          height: '100%', 
          backgroundColor: color,
          borderRadius: '4px'
        }} />
      </div>
    </div>
  );
};

const SkillProgress: React.FC = () => {
  const frontendSkills = [
    { skill: 'HTML/CSS', progress: 85, color: '#4285f4' },
    { skill: 'JavaScript', progress: 70, color: '#34a853' },
    { skill: 'React', progress: 65, color: '#ea4335' },
    { skill: 'UI/UX Design', progress: 55, color: '#fbbc05' }
  ];

  const backendSkills = [
    { skill: 'Node.js', progress: 60, color: '#4285f4' },
    { skill: 'Databases', progress: 45, color: '#34a853' },
    { skill: 'API Design', progress: 50, color: '#ea4335' }
  ];

  const softSkills = [
    { skill: 'Communication', progress: 75, color: '#4285f4' },
    { skill: 'Teamwork', progress: 80, color: '#34a853' },
    { skill: 'Problem Solving', progress: 70, color: '#ea4335' }
  ];

  return (
    <div style={{ 
      padding: '1.5rem', 
      backgroundColor: 'white', 
      borderRadius: '12px',
      boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)'
    }}>
      <h2 style={{ 
        fontSize: '1.3rem', 
        fontWeight: 600, 
        marginTop: 0,
        marginBottom: '1.5rem',
        color: '#333'
      }}>
        Your Skill Progress
      </h2>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
        gap: '2rem' 
      }}>
        <div>
          <h3 style={{ 
            fontSize: '1.1rem', 
            fontWeight: 500, 
            marginBottom: '1.2rem',
            color: '#4285f4'
          }}>
            Frontend Development
          </h3>
          {frontendSkills.map((item, index) => (
            <SkillBar 
              key={index} 
              skill={item.skill} 
              progress={item.progress} 
              color={item.color} 
            />
          ))}
        </div>

        <div>
          <h3 style={{ 
            fontSize: '1.1rem', 
            fontWeight: 500, 
            marginBottom: '1.2rem',
            color: '#34a853'
          }}>
            Backend Development
          </h3>
          {backendSkills.map((item, index) => (
            <SkillBar 
              key={index} 
              skill={item.skill} 
              progress={item.progress} 
              color={item.color} 
            />
          ))}
        </div>

        <div>
          <h3 style={{ 
            fontSize: '1.1rem', 
            fontWeight: 500, 
            marginBottom: '1.2rem',
            color: '#ea4335'
          }}>
            Soft Skills
          </h3>
          {softSkills.map((item, index) => (
            <SkillBar 
              key={index} 
              skill={item.skill} 
              progress={item.progress} 
              color={item.color} 
            />
          ))}
        </div>
      </div>

      <div style={{ 
        display: 'flex',
        justifyContent: 'center',
        marginTop: '2rem'
      }}>
        <button style={{
          backgroundColor: '#4285f4',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          padding: '0.7rem 1.5rem',
          fontSize: '0.95rem',
          fontWeight: '500',
          cursor: 'pointer',
          transition: 'background-color 0.2s ease'
        }}>
          Update Skills Assessment
        </button>
      </div>
    </div>
  );
};

export default SkillProgress; 