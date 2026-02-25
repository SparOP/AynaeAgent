# question_generator.py
# Purpose: Handles dynamic prompt construction and Gemini API integration for generating
# reframed conceptual questions based on topic and adaptation mode.
# Primary Owner: Soumodeep Das

# llm/question_generator.py

from .gemini_client import ask_gemini, USE_OFFLINE_MODE


# ==============================
# NORMAL QUESTION
# ==============================

def normal_question(topic: str) -> str:
    if USE_OFFLINE_MODE:
        return ask_gemini("", mode="normal")

    prompt = f"""
Ask a clear conceptual question to test understanding of {topic}.
Avoid yes/no questions.
Focus on explanation.
"""
    return ask_gemini(prompt)


# ==============================
# REFRAMED QUESTION (illusion breaker)
# ==============================

def reframed_question(topic: str) -> str:
    if USE_OFFLINE_MODE:
        return ask_gemini("", mode="reframed")

    prompt = f"""
Ask a differently framed conceptual question about {topic}.

Use ONE of:
- Analogy
- Real-world example
- Simplified explanation

Do not repeat textbook definitions.
"""
    return ask_gemini(prompt)


# ==============================
# FUNDAMENTAL PROBE (low score)
# ==============================

def fundamental_probe(topic: str) -> str:
    if USE_OFFLINE_MODE:
        return ask_gemini("", mode="fundamental")

    prompt = f"""
The student may have a weak understanding of {topic}.

Ask a very simple foundational question.
Focus on intuition and simplicity.
Avoid technical jargon.
"""
    return ask_gemini(prompt)


# ==============================
# CLARIFICATION PROBE (mid score)
# ==============================

def clarification_probe(topic: str) -> str:
    if USE_OFFLINE_MODE:
        return ask_gemini("", mode="clarification")

    prompt = f"""
Ask a clarifying conceptual question about {topic}.
Reframe the idea using alternative wording.
Goal: Check conceptual flexibility.
"""
    return ask_gemini(prompt)


# ==============================
# ADVANCED PROBE (high score)
# ==============================

def advanced_probe(topic: str) -> str:
    if USE_OFFLINE_MODE:
        return ask_gemini("", mode="advanced")

    prompt = f"""
Ask an advanced conceptual question about {topic}.

Include:
- Edge cases OR
- Limitations OR
- Deeper reasoning

Avoid basic definitions.
"""
    return ask_gemini(prompt)


# ==============================
# UNIFIED INTERFACE (TEAM USES THIS)
# ==============================

def generate_question(topic: str, mode: str = "normal") -> list:

    mode_map = {
        "normal": normal_question,
        "reframed": reframed_question,
        "fundamental_probe": fundamental_probe,
        "clarification_probe": clarification_probe,
        "advanced": advanced_probe,
    }

    if mode not in mode_map:
        mode = "normal"

    return [mode_map[mode](topic)]