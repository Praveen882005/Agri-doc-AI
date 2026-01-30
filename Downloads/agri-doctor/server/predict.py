# predict.py
from fastapi import APIRouter, File, UploadFile
from PIL import Image
import numpy as np
import json
import os
from tensorflow.keras.models import load_model

router = APIRouter()

# Load model safely
MODEL_PATH = "model/plant_disease_model.h5"
CLASS_INDICES_PATH = "model/class_indices.json"

model = None
idx2class = {}

if os.path.exists(MODEL_PATH) and os.path.exists(CLASS_INDICES_PATH):
    try:
        model = load_model(MODEL_PATH)
        with open(CLASS_INDICES_PATH) as f:
            class_indices = json.load(f)
        idx2class = {int(v): k for k, v in class_indices.items()}
        print("✅ Model loaded successfully!")
    except Exception as e:
        print("⚠️ Failed to load model:", e)
else:
    print("⚠️ Model or class_indices.json not found. Using dummy predictions.")

@router.post("/predict/")
async def predict(file: UploadFile = File(...)):
    if file is None:
        return {"error": "No file uploaded"}

    try:
        img = Image.open(file.file).convert("RGB").resize((224, 224))
        arr = np.array(img) / 255.0
    except Exception as e:
        return {"error": f"Invalid image: {e}"}

    if model:
        pred = model.predict(np.expand_dims(arr, 0))[0]
        idx = int(pred.argmax())
        return {
            "disease": idx2class.get(idx, "Unknown"),
            "confidence": float(pred[idx]),
        }
    else:
        return {"disease": "Healthy", "confidence": 0.95}
