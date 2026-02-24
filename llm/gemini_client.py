# llm/gemini_client.py

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

USE_OFFLINE_MODE = False  # toggle manually if needed

# ==============================
# OFFLINE RESPONSES (Fallback)
# ==============================

OFFLINE_RESPONSES = {
    "reference": {
        "recursion": "Recursion is a programming technique where a function calls itself to solve smaller instances of a problem. It requires a base case to stop infinite calls."
    },
    "questions": {
        "normal": "Can you explain recursion in your own words?",
        "reframed": "Can you describe recursion using a real-life example?",
        "fundamental": "What does it mean when a function calls itself?",
        "clarification": "How is recursion different from loops?",
        "advanced": "What problems are better suited for recursion than iteration, and why?",
    },
}

# ==============================
# GEMINI CLIENT (NEW SDK)
# ==============================

client = None

if not USE_OFFLINE_MODE:
    try:
        API_KEY = os.getenv("GEMINI_API_KEY")
        if not API_KEY:
            raise ValueError("Missing GEMINI_API_KEY in .env")

        client = genai.Client(api_key=API_KEY)
        print("✅ Gemini initialized")

    except Exception as e:
        print("❌ Gemini init failed:", e)
        USE_OFFLINE_MODE = True


# ==============================
# MAIN FUNCTION
# ==============================

def ask_gemini(prompt: str, mode: str = None) -> str:
    """Call Gemini or fallback"""

    if USE_OFFLINE_MODE or client is None:
        if mode == "reference":
            return OFFLINE_RESPONSES["reference"]["recursion"]
        if mode:
            return OFFLINE_RESPONSES["questions"].get(mode, "Explain the concept.")
        return "Explain the concept clearly."

    try:
        print("🔥 Calling Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip()

    except Exception as e:
        print("❌ Gemini runtime error:", e)
        return "Explain the concept clearly."