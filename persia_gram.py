import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL_NAME = "gemini-2.5-flash-lite" 

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def analyze_page_stats(niche, followers, likes, stories, complaint):
    """
    Analyzes Instagram stats and gives a diagnosis.
    """
    system_prompt = (
        "You are Dr. Faloo, a senior Instagram Growth Strategist in Tehran. "
        "Your Tone: Professional but 'Khodemooni' (Friendly/Colloquial). "
        "Structure of answer (Use these Farsi headers): "
        "1. 📊 **آنالیز وضعیت** (Analysis): Comment on Engagement Rate. "
        "2. 🩺 **تشخیص مشکل** (Diagnosis): Why is this happening? "
        "3. 💊 **نسخه عملی** (Prescription): Give 3 actionable steps. "
        "Write 100% in Persian. Use formatting like **bold** and bullet points."
    )

    user_prompt = (
        f"DATA REPORT:\n"
        f"- Niche: {niche}\n"
        f"- Followers: {followers}\n"
        f"- Avg Likes: {likes}\n"
        f"- Avg Stories: {stories}\n"
        f"- User Complaint: {complaint}\n\n"
        "Please diagnose my page."
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def create_persian_caption(topic, details):
    """
    Writes a viral caption.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are Faloo. Write a viral Persian caption (Mohavere) with hashtags. Be witty."},
                {"role": "user", "content": f"Topic: {topic}. Details: {details}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"