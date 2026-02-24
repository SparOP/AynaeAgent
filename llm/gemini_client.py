# llm/gemini_client.py

import os

USE_OFFLINE_MODE = False  # 🔥 Toggle this if API fails

try:
    import google.generativeai as genai
except:
    USE_OFFLINE_MODE = True


# ==============================
# OFFLINE RESPONSES (Fallback)
# ==============================

OFFLINE_RESPONSES = {
    "reference": {
        "recursion": "Recursion is a programming technique where a function calls itself to solve smaller instances of a problem. It requires a base case to stop infinite calls. It is useful for problems that can be broken into similar subproblems.",
    },
    "questions": {
        "normal": "Can you explain recursion in your own words?",
        "reframed": "Can you describe recursion using a real-life example or analogy?",
        "fundamental": "What does it mean when a function calls itself?",
        "clarification": "How is recursion different from using loops?",
        "advanced": "What problems are better suited for recursion than iteration, and why?",
    },
}


# ==============================
# GEMINI SETUP
# ==============================

if not USE_OFFLINE_MODE:
    try:
        API_KEY = os.getenv("GEMINI_API_KEY")  # safer than hardcoding
        genai.configure(api_key=API_KEY)

        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={"temperature": 0.5},
        )
    except:
        USE_OFFLINE_MODE = True


# ==============================
# MAIN FUNCTION
# ==============================

def ask_gemini(prompt: str, mode: str = None) -> str:
    """
    mode is used only for offline fallback
    """

    if USE_OFFLINE_MODE:
        if mode == "reference":
            return OFFLINE_RESPONSES["reference"]["recursion"]
        if mode:
            return OFFLINE_RESPONSES["questions"].get(mode, "Explain the concept.")
        return "Explain the concept clearly."

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini error, switching to fallback:", e)
        return "Explain the concept clearly."