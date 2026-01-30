import React, { useState, useRef, useEffect } from "react";
import "./Chatbot.css";

function Chatbot() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "🌱 Hello! I am Agri Doctor. I can help with potato and tomato diseases, farming advice, and organic solutions. How can I assist you today?",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    const newMessages = [...messages, { sender: "user", text: userMessage }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });
      const data = await res.json();
      setMessages([...newMessages, { sender: "bot", text: data.reply }]);
    } catch {
      setMessages([
        ...newMessages,
        {
          sender: "bot",
          text: "⚠️ Sorry, I'm having trouble connecting. Please check your internet connection and try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  const quickQuestions = [
    "Potato diseases?",
    "Tomato treatment?",
    "Organic solutions?",
    "Watering tips",
  ];

  return (
    <>
      {/* Chatbot Toggle Button */}
      {!isOpen && (
        <button className="chatbot-toggle" onClick={() => setIsOpen(true)}>
          💬 Agri Doctor
        </button>
      )}

      {/* Chatbot Container */}
      {isOpen && (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <div className="chatbot-title">
              <span>🌾 Agri Doctor</span>
              <small>Farming Assistant</small>
            </div>
            <button className="close-btn" onClick={() => setIsOpen(false)}>
              ✕
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
            {loading && (
              <div className="message bot loading">⏳ Thinking...</div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Questions */}
          {messages.length <= 2 && (
            <div className="quick-questions">
              <p>Quick questions:</p>
              <div className="quick-buttons">
                {quickQuestions.map((question, index) => (
                  <button
                    key={index}
                    className="quick-btn"
                    onClick={() => {
                      setInput(question);
                      setTimeout(sendMessage, 100);
                    }}
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="chatbot-input">
            <input
              type="text"
              value={input}
              placeholder="Ask about plant diseases, treatments, or farming advice..."
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              disabled={loading}
            />
            <button onClick={sendMessage} disabled={loading || !input.trim()}>
              {loading ? "⏳" : "📤"}
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default Chatbot;
