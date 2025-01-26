import React, { useState } from 'react';
import './style/ChatBot.css';



const ChatBot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const handleSend = () => {
        if (input.trim()) {
            setMessages([...messages, { text: input, sender: 'user' }]);
            setInput('');

            // Add logic to handle bot response
            setTimeout(() => {
                setMessages(prevMessages => [
                    ...prevMessages,
                    { text: 'TERA: This is a bot response', sender: 'bot' }
                ]);
            }, 1000); // Simulate a delay for the bot response
        }
    };

    return (
        <div className="chatbot-container">
            <div className="chatbot-messages">
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.sender}`}>
                        {message.text}
                    </div>
                ))}
            </div>
            <div className="chatbot-input">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                />
                <button onClick={handleSend}>Send</button>
            </div>
        </div>

        
    );
};

export default ChatBot;