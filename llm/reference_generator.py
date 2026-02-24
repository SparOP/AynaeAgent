# reference_generator.py
# Purpose: Generates a concise ideal reference explanation for a given topic
# using Gemini API. This reference is used for semantic alignment scoring
# to improve validity beyond cross-answer consistency.
# Primary Owner: Soumodeep Das

# llm/reference_builder.py

from .gemini_client import ask_gemini, USE_OFFLINE_MODE


def build_reference(topic: str) -> str:
    """
    Generates a concise gold-standard explanation.
    Called once per session.
    """

    if USE_OFFLINE_MODE:
        return ask_gemini("", mode="reference")

    prompt = f"""
Explain the concept of {topic} clearly and concisely in 3 sentences.

Include:
- Core idea
- How it works
- Why it matters

Avoid fluff. Be educational and precise.
"""

    return ask_gemini(prompt)
