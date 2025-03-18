import React from 'react';

const Navbar: React.FC = () => {
  return (
    <div style={{
      backgroundColor: 'white',
      padding: '1rem 2rem',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
      width: '90%',
      maxWidth: '1400px',
      borderRadius: '8px',
      position: 'relative',
      zIndex: 1000
    }}>
      <h1 style={{
        margin: 0,
        color: '#333',
        fontSize: '1.5rem',
        fontWeight: 'bold'
      }}>
        Paths
      </h1>
      <button
        style={{
          backgroundColor: '#4285f4',
          color: 'white',
          border: 'none',
          padding: '0.5rem 1rem',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '0.9rem',
          fontWeight: '500',
          transition: 'background-color 0.2s'
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.backgroundColor = '#3367d6';
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.backgroundColor = '#4285f4';
        }}
        onClick={() => {
          // Add sign out logic here
          console.log('Sign out clicked');
        }}
      >
        Sign Out
      </button>
    </div>
  );
};

export default Navbar; 