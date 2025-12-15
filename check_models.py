import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# We call the Google API directly to list available models
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    response = requests.get(url)
    data = response.json()
    
    print("--- 📋 AVAILABLE MODELS FOR YOU ---")
    if 'models' in data:
        for m in data['models']:
            # We only care about models that support 'generateContent'
            if "generateContent" in m.get("supportedGenerationMethods", []):
                # We strip 'models/' because the OpenAI client adds it automatically sometimes
                clean_name = m['name'].replace("models/", "")
                print(f"✅ {clean_name}")
    else:
        print("❌ No models found. Response:", data)
        
except Exception as e:
    print(f"Error: {e}")