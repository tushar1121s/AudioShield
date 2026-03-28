import React from 'react';
import './Background.css';

const Background = () => {
  return (
    <div className="bg-wrapper">
      <div className="noise-overlay" />
      <div className="glow-orb orb-primary" />
      <div className="glow-orb orb-secondary" />
      <div className="glow-orb orb-tertiary" />
    </div>
  );
};

export default Background;