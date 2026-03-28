import React, { useState } from 'react';
import './Sender.css';
import { uploadFile } from '../../services/api';
import Waveform from '../../components/shared/Waveform';

const Sender = () => {
  const [file, setFile] = useState(null);
  const [audio, setAudio] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file || !audio) {
      setError("Both payload and audio key are required.");
      return;
    }
    setError("");
    setLoading(true);

    try {
      const data = await uploadFile(file, audio);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return (
      <div className="sender-container page-transition">
        <div className="success-card glass-card">
          <div className="success-icon">🔥</div>
          <h2 className="success-title">Vault Secured</h2>
          <p className="success-subtitle">Your file is encrypted and ready for pickup.</p>
          
          <div className="result-display">
            <label>ROOM CODE</label>
            <div className="code-value">{result.room_code}</div>
          </div>

          <div className="qr-box">
            <img src={`data:image/png;base64,${result.qr_code}`} alt="QR Code" />
            <p>Scan to auto-fill receiver page</p>
          </div>

          <button className="btn-secondary" onClick={() => window.location.reload()}>
            Send Another
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="sender-container page-transition">
      <div className="section-header">
        <h1 className="page-title">Encrypt <span className="text-gradient">Vault</span></h1>
        <p className="page-subtitle">// Step 01: Payload + Step 02: Audio Key</p>
      </div>

      <div className="sender-grid">
        {/* Step 1: File Selection */}
        <div className={`upload-card glass-card ${file ? 'selected' : ''}`}>
          <div className="card-tag">01</div>
          <h3>Select Payload</h3>
          <div className="drop-zone">
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            <div className="icon">{file ? "📄" : "📁"}</div>
            <p className="file-name">{file ? file.name : "Click to browse files"}</p>
          </div>
        </div>

        {/* Step 2: Audio Key */}
        <div className={`upload-card glass-card ${audio ? 'selected' : ''}`}>
          <div className="card-tag">02</div>
          <h3>Audio Key</h3>
          <div className="drop-zone">
            <input type="file" accept="audio/*" onChange={(e) => setAudio(e.target.files[0])} />
            <div className="icon">{audio ? "🎵" : "🎤"}</div>
            <p className="file-name">{audio ? audio.name : "Upload your key"}</p>
          </div>
          {audio && <Waveform />}
        </div>
      </div>

      {error && <div className="error-msg">{error}</div>}

      <div className="action-area">
        <button 
          className="btn-main" 
          onClick={handleUpload} 
          disabled={!file || !audio || loading}
        >
          {loading ? "INITIALIZING AES-256..." : "LOCK & UPLOAD"}
        </button>
      </div>
    </div>
  );
};

export default Sender;