import React from 'react';
import './Features.css';

const Features = () => {
  const techs = [
    { title: "AES-256-GCM", desc: "Military-grade authenticated encryption ensuring data privacy and integrity.", icon: "💎" },
    { title: "SHA-256 Hashing", desc: "Audio files are transformed into unique cryptographic fingerprints.", icon: "🧬" },
    { title: "Zero-Storage", desc: "The Janitor wipes expired rooms every 24 hours. We store nothing permanently.", icon: "🧹" },
    { title: "Python Flask", desc: "High-performance backend managing the cryptographic pipeline.", icon: "🐍" }
  ];

  return (
    <div className="features-container page-transition">
      <div className="section-header">
        <h1 className="page-title">Technical <span className="text-gradient">Specs</span></h1>
        <p className="page-subtitle">// How AudioShield protects your data</p>
      </div>
      <div className="features-grid">
        {techs.map((t, i) => (
          <div key={i} className="feature-card glass-card">
            <div className="feat-icon">{t.icon}</div>
            <h3>{t.title}</h3>
            <p>{t.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Features;