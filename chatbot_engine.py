import google.generativeai as genai
import os

# Set your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY") or "AIzaSyCYxIylA_VW4NHYQTb4uuZ-6963QPP78Fw")

# Use an available model
MODEL_NAME = "models/gemini-2.5-flash"  # You can also try "models/gemini-flash-latest"

model = genai.GenerativeModel(MODEL_NAME)

def get_response(user_input):
    try:
        prompt = f"The user said: '{user_input}'. Respond helpfully and naturally."
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "⚠️ No response from model."
    except Exception as e:
        return f"⚠️ Error generating response: {e}"
