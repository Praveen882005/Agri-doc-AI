import React, { useState } from "react";
import axios from "axios";
import "./ImageUploader.css";

function ImageUploader() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [preview, setPreview] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
      setResult(null); // Clear previous results
    }
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select an image first!");

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", formData);
      setResult(res.data);
    } catch (error) {
      alert(
        "⚠️ Error uploading image: " +
          (error.response?.data?.error || error.message)
      );
    } finally {
      setLoading(false);
    }
  };

  const resetUpload = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
  };

  return (
    <div className="uploader-card">
      <h2>🌿 Plant Disease Detection</h2>
      <p>
        Upload clear images of potato or tomato leaves for accurate diagnosis
      </p>

      {!file ? (
        <div className="upload-area">
          <label htmlFor="file-upload" className="file-upload-label">
            <div className="upload-placeholder">
              <span className="upload-icon">📁</span>
              <p>Click to select plant image</p>
              <small>Supports JPG, PNG, WebP (Max 5MB)</small>
            </div>
          </label>
          <input
            id="file-upload"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="file-input"
          />
        </div>
      ) : (
        <div className="image-preview-container">
          <div className="image-preview">
            <img src={preview} alt="Preview" />
            <button onClick={resetUpload} className="remove-btn">
              ✕
            </button>
          </div>

          <div className="action-buttons">
            <button
              onClick={handleUpload}
              disabled={loading}
              className="predict-btn"
            >
              {loading ? "🔍 Analyzing..." : "📤 Upload & Predict"}
            </button>
            <button onClick={resetUpload} className="cancel-btn">
              Choose Different Image
            </button>
          </div>
        </div>
      )}

      {result && !result.error && (
        <div
          className={`result ${
            result.confidence > 70
              ? "high-confidence"
              : result.confidence > 50
              ? "medium-confidence"
              : "low-confidence"
          }`}
        >
          <h3>🔍 Diagnosis: {result.disease}</h3>

          {result.warning === "low_confidence" && (
            <div className="warning-banner">⚠️ Low Confidence Prediction</div>
          )}

          <div className="confidence-display">
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{ width: `${result.confidence}%` }}
              ></div>
            </div>
            <p>
              AI Confidence: <strong>{result.confidence}%</strong>
            </p>
          </div>

          {result.top_predictions && result.top_predictions.length > 1 && (
            <div className="alternative-predictions">
              <h4>Other possibilities:</h4>
              {result.top_predictions.slice(1).map((pred, index) => (
                <div key={index} className="alternative-pred">
                  {pred.disease}: {pred.confidence}%
                </div>
              ))}
            </div>
          )}

          <div className="recommendations">
            <div className="recommendation-card">
              <h4>💊 Immediate Treatment</h4>
              <p>{result.suggestion}</p>
            </div>

            {result.prevention && (
              <div className="recommendation-card">
                <h4>🛡️ Prevention</h4>
                <p>{result.prevention}</p>
              </div>
            )}

            {result.organic && (
              <div className="recommendation-card">
                <h4>🌱 Organic Options</h4>
                <p>{result.organic}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {result && result.error && (
        <div className="result error">
          <h3>❌ Error</h3>
          <p>{result.error}</p>
        </div>
      )}
    </div>
  );
}

export default ImageUploader;
