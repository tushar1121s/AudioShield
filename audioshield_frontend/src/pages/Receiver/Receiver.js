import React, { useState, useEffect } from 'react';
import './Receiver.css';
import { downloadFile } from '../../services/api';
import Waveform from '../../components/shared/Waveform';

const Receiver = () => {
  const [roomCode, setRoomCode] = useState("");
  const [audio, setAudio] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const room = params.get("room");
    if (room) setRoomCode(room.toUpperCase());
  }, []);

  const handleDownload = async () => {
    if (!roomCode || !audio) {
      setError("Room code and audio key are both required.");
      return;
    }
    setError(""); setSuccess(""); setLoading(true);

    try {
      const res = await downloadFile(roomCode, audio);
      
      const blob = await res.blob();
      const disposition = res.headers.get("Content-Disposition");
      let filename = "decrypted_file";
      
      if (disposition) {
        const match = disposition.match(/filename="?([^"]+)"?/);
        if (match) filename = match[1];
      }

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      
      setSuccess(`Success! "${filename}" decrypted.`);
    } catch (err) {
      setError(err.message || "Invalid audio key or expired room.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="receiver-container page-transition">
      <div className="section-header">
        <h1 className="page-title">Unlock <span className="text-gradient">Vault</span></h1>
        <p className="page-subtitle">// Input Room Code + Provide Audio Key</p>
      </div>

      <div className="receiver-card glass-card">
        <div className="input-group">
          <label>ROOM CODE</label>
          <input 
            type="text" 
            placeholder="E.G. AX9-K32"
            value={roomCode}
            onChange={(e) => setRoomCode(e.target.value.toUpperCase())}
            maxLength={8}
          />
        </div>

        <div className="input-group">
          <label>AUDIO KEY</label>
          <div className={`audio-drop ${audio ? 'active' : ''}`}>
            <input type="file" accept="audio/*" onChange={(e) => setAudio(e.target.files[0])} />
            <div className="drop-content">
              <span>{audio ? audio.name : "Drop the exact audio key here"}</span>
              {audio && <Waveform />}
            </div>
          </div>
        </div>

        {error && <div className="error-alert">⚠ {error}</div>}
        {success && <div className="success-alert">✓ {success}</div>}

        <button 
          className="btn-main" 
          onClick={handleDownload} 
          disabled={loading || !roomCode || !audio}
        >
          {loading ? "DECRYPTING..." : "UNLOCK & DOWNLOAD"}
        </button>
      </div>
    </div>
  );
};

export default Receiver;