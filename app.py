# app.py
import streamlit as st
import time
from question_engine import generate_questions   

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AyenaeAgent",
    layout="wide"
)

# ---------------- TITLE SECTION ----------------
st.title("🧠 AyenaeAgent")
st.markdown("""
### Adaptive Agentic System for Concept Stability Evaluation  
Detecting Illusion of Understanding using Multi-Framed Questioning
""")

# ---------------- SESSION STATE INITIALIZATION ----------------
if "mode" not in st.session_state:
    st.session_state.mode = "normal"

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "csi" not in st.session_state:
    st.session_state.csi = None

if "evaluated" not in st.session_state:
    st.session_state.evaluated = False

if "topic" not in st.session_state:
    st.session_state.topic = ""

# =====================================================
# ---------------- STEP 3: TOPIC INPUT ----------------
# =====================================================

st.divider()
st.header("📘 Enter Topic")

topic = st.text_input("Enter a topic you studied:")

generate_btn = st.button("Generate Questions")

# =====================================================
# ---------------- STEP 4: GENERATE QUESTIONS ---------
# =====================================================

if generate_btn:

    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:
        try:
            with st.spinner("Generating multi-framed questions..."):
                questions = generate_questions(topic, st.session_state.mode)
                time.sleep(1)

            st.session_state.questions = questions
            st.session_state.topic = topic
            st.session_state.evaluated = False

        except Exception as e:
            st.error("Question generation failed. Please try again.")
# Purpose: Main Streamlit entry point for AynaeAgent. Handles user interaction, topic input,
# answer collection, and connects all backend modules (LLM, embeddings, scoring, decision).
# Primary Owner: Soumojeet Dutta and Soumodeep Das