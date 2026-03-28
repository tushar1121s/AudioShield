import React from 'react';
import './Home.css';

const Home = ({ onStart }) => {
  return (
    <div className="home-container page-transition">
      <div className="hero-section">
        <div className="badge-container">
          <div className="pulse-dot"></div>
          <span className="badge-text">AUDIO-ENCRYPTED FILE SHARING</span>
        </div>
        
        <h1 className="hero-title">
          Your Audio is <br />
          Your <span className="text-gradient">Password.</span>
        </h1>
        
        <p className="hero-subtitle">
          The world's first "Zero-Knowledge" file vault that uses the unique 
          frequency of sound to generate 256-bit encryption keys. No passwords stored. 
          No backdoors. Just pure signal.
        </p>
        
        <div className="cta-group">
          <button className="btn-main" onClick={() => onStart()}>
            Start Securing
          </button>
          <div className="stat-row">
            <div className="stat-item">
              <span className="stat-val">AES-256</span>
              <span className="stat-lab">Encryption</span>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <span className="stat-val">0.0s</span>
              <span className="stat-lab">Data Retained</span>
            </div>
          </div>
        </div>
      </div>

      <div className="preview-grid">
        <div className="preview-card">
          <div className="preview-icon">🔒</div>
          <h3>Bit-Perfect Security</h3>
          <p>We hash the raw bytes of your audio. Even a 1ms difference in sound results in a completely different key.</p>
        </div>
        <div className="preview-card">
          <div className="preview-icon">🕊️</div>
          <h3>Ephemeral Storage</h3>
          <p>Files are automatically wiped by "The Janitor" after 24 hours. Your data never stays longer than it needs to.</p>
        </div>
      </div>
    </div>
  );
};

export default Home;