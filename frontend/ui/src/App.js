import React, { useEffect } from 'react';
import io from 'socket.io-client';
import './App.css';

// Connect to the backend. Make sure the URL is correct.
const socket = io('http://localhost:8000', {
  transports: ['websocket'],
});

function App() {

  useEffect(() => {
    // Listen for the 'connect' event
    socket.on('connect', () => {
      console.log('Connected to backend! Socket ID:', socket.id);
    });

    // Clean up the connection when the component is unmounted
    return () => {
      socket.off('connect');
    };
  }, []);

  const handleSosClick = () => {
    console.log("Sending 'panic' event to backend...");
    socket.emit('panic', { message: "User needs help!" });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Community Guardian</h1>
        <p>In case of emergency, press the button below.</p>
      </header>
      <button className="sos-button" onClick={handleSosClick}>
        SOS
      </button>
    </div>
  );
}

export default App;