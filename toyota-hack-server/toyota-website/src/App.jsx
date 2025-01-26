import React, { useState, useEffect } from 'react';

function App() {
  const [sessionId, setSessionId] = useState('');
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  useEffect(() => {
    // Initialize session on component mount
    fetch('http://localhost:5000/start_session', { method: 'POST' })
      .then(res => res.json())
      .then(data => setSessionId(data.session_id));
  }, []);

  const sendMessage = async () => {
    const response = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message }),
    });

    const data = await response.json();
    setChatHistory([...chatHistory, { user: message, bot: data.response }]);
    setMessage('');
  };

  return (
    <div>
      <div>
        {chatHistory.map((msg, idx) => (
          <div key={idx}>
            <p>User: {msg.user}</p>
            <p>Bot: {msg.bot}</p>
          </div>
        ))}
      </div>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;