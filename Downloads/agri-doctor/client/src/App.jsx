import React from "react";
import "./App.css";
import ImageUploader from "./components/ImageUploader";
import Chatbot from "./components/Chatbot";

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>🌾 Agri Doctor</h1>
        <p className="subtitle">
          AI-Powered Plant Disease Detection & Farming Assistant
        </p>
        <p>
          Upload an image to detect plant disease or chat with our multilingual
          Agri Doctor bot.
        </p>
      </header>

      <main className="app-main">
        <ImageUploader />
      </main>

      <Chatbot />
    </div>
  );
}

export default App;
