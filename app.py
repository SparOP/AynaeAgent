# app.py
# Purpose: Main Streamlit entry point for AynaeAgent. Handles user interaction, topic input,
# answer collection, and connects all backend modules (LLM, embeddings, scoring, decision).
# Primary Owner: Soumojeet Dutta and Soumodeep Das 

# app.py
# Main UI for AyenaeAgent

import streamlit as st
import time
from llm.question_generator import generate_question

from storage.database import DatabaseManager

db = DatabaseManager()


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AyenaeAgent",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🧠 AyenaeAgent")
st.markdown("""
### Adaptive Agentic System for Concept Stability Evaluation  
Detecting Illusion of Understanding using Multi-Framed Questioning
""")

# ---------------- SESSION STATE ----------------
defaults = {
    "mode": "normal",
    "questions": [],
    "topic": "",
    "generated": False
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ---------------- SAFE WRAPPER ----------------
def safe_generate(topic, mode):
    try:
        return generate_question(topic, mode)
    except Exception as e:
        st.error("⚠️ Gemini failed")
        st.exception(e)
        return []


# =====================================================
# TOPIC INPUT
# =====================================================
st.divider()
st.header("📘 Enter Topic")

topic_input = st.text_input(
    "Enter a topic you studied:",
    placeholder="Example: Operating System Scheduling"
)

generate_btn = st.button("🚀 Generate Questions")


# ================= GENERATE =================
if generate_btn:
    if topic_input.strip() == "":
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Generating multi-framed questions..."):
            time.sleep(1)

            qs = safe_generate(topic_input, st.session_state.mode)

            # ---- SAFETY GUARD ----
            if isinstance(qs, str):
                qs = [qs]
            elif qs is None:
                qs = []

            st.session_state.questions = qs
            st.session_state.topic = topic_input
            st.session_state.generated = True


# ================= SHOW QUESTIONS =================
st.divider()
st.subheader("🧠 Generated Questions")

if st.session_state.generated:
    if st.session_state.questions:
        st.success(f"Topic: {st.session_state.topic}")

        for i, q in enumerate(st.session_state.questions, 1):
            st.markdown(f"**Q{i}.** {q}")
    else:
        st.warning("No questions generated.")
else:
    st.info("Enter a topic and click Generate.")