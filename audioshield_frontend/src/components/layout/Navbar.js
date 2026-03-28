import React from 'react';
import './Navbar.css';

const Navbar = ({ setPage, activePage }) => {
  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'sender', label: 'Send' },
    { id: 'receiver', label: 'Receive' },
    { id: 'features', label: 'Features' },
    { id: 'about', label: 'About' }
  ];

  return (
    <nav className="navbar">
      <div className="nav-logo" onClick={() => setPage('home')}>
        <div className="logo-icon">🛡</div>
        <span className="logo-text">Audio<span>Shield</span></span>
      </div>
      
      <div className="nav-links">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`nav-link ${activePage === item.id ? 'active' : ''}`}
            onClick={() => setPage(item.id)}
          >
            {item.label}
          </button>
        ))}
      </div>
    </nav>
  );
};

export default Navbar;