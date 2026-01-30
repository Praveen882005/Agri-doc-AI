from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import json
import os
import io

# Import chatbot router
from chatbot import router as chatbot_router

app = FastAPI(title="Agri Doctor Backend")

# --- CORS Setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load AI Model ---
MODEL_PATH = "model/plant_disease_model.h5"
CLASS_INDICES_PATH = "model/class_indices.json"

model = None
idx2class = {}

try:
    if os.path.exists(MODEL_PATH) and os.path.exists(CLASS_INDICES_PATH):
        print("🔄 Loading model...")
        model = load_model(MODEL_PATH)
        
        with open(CLASS_INDICES_PATH) as f:
            class_indices = json.load(f)
        idx2class = {int(v): k for k, v in class_indices.items()}
        
        print("✅ Model Loaded Successfully!")
        print(f"📊 Model Summary:")
        print(f"   - Input shape: {model.input_shape}")
        print(f"   - Output shape: {model.output_shape}")
        print(f"   - Number of classes: {len(class_indices)}")
        print(f"   - Classes: {list(class_indices.keys())}")
        
        # Test model with dummy data
        test_input = np.random.random((1, 224, 224, 3))
        test_pred = model.predict(test_input, verbose=0)
        print(f"   - Test prediction shape: {test_pred.shape}")
        
    else:
        print("❌ Model files not found!")
        if not os.path.exists(MODEL_PATH):
            print(f"   Missing: {MODEL_PATH}")
        if not os.path.exists(CLASS_INDICES_PATH):
            print(f"   Missing: {CLASS_INDICES_PATH}")

except Exception as e:
    print(f"❌ Error loading model: {str(e)}")
    model = None

@app.get("/")
def root():
    return {"message": "Agri Doctor Backend Running"}

# --- Enhanced Disease Prediction Logic ---
def predict_disease(image: Image.Image):
    if model is None:
        return {"disease": "Model Error", "confidence": 0, "suggestion": "AI model not loaded properly."}

    try:
        # Convert and resize image
        image = image.convert("RGB")
        
        # Get model's expected input shape
        target_size = (224, 224)  # Default size, adjust if your model uses different
        if model.input_shape[1] is not None:
            target_size = (model.input_shape[1], model.input_shape[2])
        
        print(f"🔍 Resizing image to: {target_size}")
        
        image = image.resize(target_size)
        img_array = np.array(image) / 255.0  # Normalize to [0,1]
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        print(f"📐 Final input shape: {img_array.shape}")
        
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        pred_array = predictions[0]
        
        print(f"🎯 Raw predictions: {pred_array}")
        
        # Get top prediction
        predicted_idx = np.argmax(pred_array)
        confidence = float(pred_array[predicted_idx]) * 100
        disease = idx2class.get(predicted_idx, "Unknown")
        
        print(f"🏆 Predicted: {disease} with {confidence:.2f}% confidence")
        
        # Get top 3 predictions for debugging
        top_3_idx = np.argsort(pred_array)[-3:][::-1]
        top_3 = [(idx2class.get(idx, "Unknown"), float(pred_array[idx]) * 100) 
                for idx in top_3_idx]
        
        print(f"📊 Top 3 predictions: {top_3}")
        
        # Enhanced suggestions
        suggestions = {
            # Potato Diseases
            "Potato_Early_blight": {
                "treatment": "Apply Chlorothalonil (Bravo) or Mancozeb fungicides every 7-10 days.",
                "prevention": "Remove infected leaves, improve air circulation, avoid overhead watering.",
                "organic": "Use copper-based fungicides and practice crop rotation."
            },
            "Potato_healthy": {
                "treatment": "No treatment needed! Your plant is healthy.",
                "prevention": "Continue current practices. Monitor regularly for early signs.",
                "organic": "Maintain organic practices with proper spacing and soil health."
            },
            "Potato_Late_blight": {
                "treatment": "Apply metalaxyl-based fungicides. Destroy severely infected plants.",
                "prevention": "Use certified disease-free seed potatoes. Avoid planting in wet areas.",
                "organic": "Apply copper sprays preventatively and ensure good drainage."
            },
            
            # Tomato Diseases  
            "Tomato_Bacterial_spot": {
                "treatment": "Apply copper-based bactericides early in the morning.",
                "prevention": "Use disease-free seeds, avoid working with wet plants.",
                "organic": "Copper sprays and resistant varieties work best."
            },
            "Tomato_Early_blight": {
                "treatment": "Apply Chlorothalonil or Mancozeb fungicides weekly.",
                "prevention": "Remove lower leaves, practice 3-year crop rotation.",
                "organic": "Use copper fungicides and improve plant spacing."
            },
            "Tomato_healthy": {
                "treatment": "No treatment needed! Your tomato plant is thriving.",
                "prevention": "Maintain consistent watering and proper fertilization.",
                "organic": "Continue organic practices with regular monitoring."
            },
            "Tomato_Late_blight": {
                "treatment": "Apply fungicides containing chlorothalonil or mancozeb immediately.",
                "prevention": "Destroy infected plants, avoid overhead irrigation.",
                "organic": "Use copper-based products and resistant varieties."
            }
        }
        
        disease_info = suggestions.get(disease, {
            "treatment": "Consult local agricultural expert for specific recommendations.",
            "prevention": "Practice crop rotation and maintain plant health.",
            "organic": "Use integrated pest management approaches."
        })
        
        # Add confidence threshold - if too low, be cautious
        if confidence < 60:
            return {
                "disease": "Uncertain - Low Confidence",
                "confidence": round(confidence, 2),
                "suggestion": "The AI is not very confident about this prediction. Please try:\n• Take a clearer photo with good lighting\n• Ensure the entire leaf/plant is visible\n• Upload multiple angles\n• Consult with agricultural expert",
                "warning": "low_confidence",
                "top_predictions": [
                    {"disease": d.replace('_', ' '), "confidence": round(c, 2)}
                    for d, c in top_3
                ]
            }
        
        return {
            "disease": disease.replace('_', ' '),
            "confidence": round(confidence, 2),
            "suggestion": disease_info["treatment"],
            "prevention": disease_info["prevention"],
            "organic": disease_info["organic"],
            "top_predictions": [
                {"disease": d.replace('_', ' '), "confidence": round(c, 2)}
                for d, c in top_3
            ]
        }
        
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        return {"disease": "Error", "confidence": 0, "suggestion": f"Prediction failed: {str(e)}"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        result = predict_disease(image)
        return result
    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

# --- Include Chatbot ---
app.include_router(chatbot_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)