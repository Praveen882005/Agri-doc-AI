from fastapi import APIRouter, Request
from googletrans import Translator

router = APIRouter()
translator = Translator()

# 🌾 Enhanced Agri Knowledge Base for Potato & Tomato
responses = {
    "hi": "Hello! 👋 I'm Agri Doctor. How can I help with your potatoes or tomatoes today?",
    "hello": "Hi there! 🌾 Ask me about potato or tomato diseases, fertilizers, or pests.",
    
    # Potato specific
    "potato": "For potatoes: Watch for Early Blight (dark spots) and Late Blight (white mold).",
    "potato blight": "For Potato Blight: Use copper-based fungicides and remove infected plants.",
    "potato disease": "Common potato diseases: Early Blight, Late Blight. Upload an image for diagnosis!",
    
    # Tomato specific  
    "tomato": "For tomatoes: Common issues include Bacterial Spot, Early Blight, and Late Blight.",
    "tomato spot": "For Tomato Bacterial Spot: Use copper sprays and avoid wet foliage.",
    "tomato disease": "Common tomato diseases: Bacterial Spot, Early Blight, Late Blight. Send a photo for analysis!",
    
    # General agriculture
    "fertilizer": "Use balanced NPK fertilizer. For potatoes: higher potassium. For tomatoes: higher phosphorus.",
    "pest": "For pests: Use neem oil or organic pesticides. Monitor regularly.",
    "water": "Water early morning. Potatoes need consistent moisture, tomatoes prefer deep watering.",
    "soil": "Well-draining soil with pH 5.5-6.5 for potatoes, 6.0-6.8 for tomatoes.",
    "help": "I can help with: 🔍 Disease detection - upload plant images\n💬 Farming advice - ask about potatoes/tomatoes\n🌱 Organic solutions - natural remedies",
    
    "thanks": "You're welcome! 😊 Happy farming!",
    "bye": "Goodbye! 👋 Take care of your crops!"
}

@router.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return {"reply": "Please type a message..."}

        # Detect language and translate to English for processing
        detected_lang = translator.detect(user_message).lang
        translated = translator.translate(user_message, dest="en").text.lower()

        # Find matching response
        reply = "I specialize in potato and tomato diseases. Could you tell me more about your specific issue with these crops?"
        for key, value in responses.items():
            if key in translated:
                reply = value
                break

        # Translate reply back to user's language
        if detected_lang != "en":
            translated_reply = translator.translate(reply, dest=detected_lang).text
        else:
            translated_reply = reply

        return {"reply": translated_reply}
    
    except Exception as e:
        return {"reply": "Sorry, I'm having trouble responding. Please try again."}