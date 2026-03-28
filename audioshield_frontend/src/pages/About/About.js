import React from 'react';
import './About.css';

const About = () => {
  return (
    <div className="about-container page-transition">
      <div className="about-content glass-card">
        <h1 className="page-title">The <span className="text-gradient">Mission</span></h1>
        <p>
          AudioShield was born out of a simple question: <strong>"Can sound be a key?"</strong> 
          Traditional passwords are stolen, leaked, or guessed. But a specific audio recording 
          is a unique physical artifact.
        </p>
        <p>
          Our platform combines the fluidity of sound with the rigidity of 
          modern cryptography. By using the raw binary data of an audio file, 
          we create an encryption key that exists only when you provide the source.
        </p>
        <div className="about-footer">
          <div className="badge">SECURE</div>
          <div className="badge">PRIVATE</div>
          <div className="badge">SOUND-DRIVEN</div>
        </div>
      </div>
    </div>
  );
};

export default About;