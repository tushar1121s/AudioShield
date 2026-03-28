import React, { useState, useEffect } from 'react';
import './App.css'; 

// Layout Components
import Background from './components/ui/Background';
import Navbar from './components/layout/Navbar';

// Page Components
import Home from './pages/Home/Home';
import Sender from './pages/Sender/Sender';
import Receiver from './pages/Receiver/Receiver';
import Features from './pages/Features/Features';
import About from './pages/About/About';

function App() {
  const [currentPage, setCurrentPage] = useState('home');

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('room')) setCurrentPage('receiver');
  }, []);

  const renderPage = () => {
    switch (currentPage) {
      case 'home': 
        return <Home onStart={() => setCurrentPage('sender')} />;
      case 'sender': 
        return <Sender />;
      case 'receiver': 
        return <Receiver />;
      case 'features': 
        return <Features />;
      case 'about': 
        return <About />;
      default: 
        return <Home onStart={() => setCurrentPage('sender')} />;
    }
  };

  return (
    <div className="app-container">
      <Background />
      <Navbar setPage={setCurrentPage} activePage={currentPage} />
      <main className="content">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;