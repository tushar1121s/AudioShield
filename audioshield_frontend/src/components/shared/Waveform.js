import React from 'react';
import './Waveform.css';

const Waveform = () => {
  return (
    <div className="waveform-container">
      {Array.from({ length: 20 }).map((_, i) => (
        <div 
          key={i} 
          className="wave-bar" 
          style={{ animationDelay: `${i * 0.05}s` }} 
        />
      ))}
    </div>
  );
};

export default Waveform;