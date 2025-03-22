import React from 'react';

const Navbar: React.FC = () => {
  return (
    <div style={{
      backgroundColor: 'white',
      padding: '0.75rem 1.5rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      boxShadow: '0 2px 10px rgba(0, 0, 0, 0.05)',
      width: '100%',
      zIndex: 1000
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
      }}>
        <h1 style={{
          margin: 0,
          color: '#333',
          fontSize: '1.5rem',
          fontWeight: 'bold'
        }}>
          Career<span style={{ color: '#4285f4' }}>Paths</span>
        </h1>
      </div>
      
      <div style={{
        display: 'flex',
        gap: '1.5rem',
        alignItems: 'center'
      }}>
        <NavItem active>Home</NavItem>
        <NavItem>Resources</NavItem>
        <NavItem>Skills</NavItem>
        <NavItem>Career Paths</NavItem>
        <button style={{
          backgroundColor: '#4285f4',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          padding: '0.5rem 1.2rem',
          fontSize: '0.9rem',
          fontWeight: '500',
          cursor: 'pointer',
          transition: 'background-color 0.2s ease',
          marginLeft: '0.8rem'
        }}>
          Get Started
        </button>
      </div>
    </div>
  );
};

interface NavItemProps {
  children: React.ReactNode;
  active?: boolean;
}

const NavItem: React.FC<NavItemProps> = ({ children, active }) => {
  return (
    <div style={{
      fontSize: '0.95rem',
      fontWeight: active ? '600' : '500',
      color: active ? '#4285f4' : '#555',
      padding: '0.5rem 0.2rem',
      cursor: 'pointer',
      borderBottom: active ? '2px solid #4285f4' : '2px solid transparent',
      transition: 'all 0.2s ease'
    }}>
      {children}
    </div>
  );
};

export default Navbar; 