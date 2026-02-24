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


# ---------------- SAFE EXECUTION WRAPPER ----------------
def safe_generate(topic, mode):
    try:
        return generate_questions(topic, mode)
    except Exception as e:
        st.error("⚠️ Question engine failed.")
        st.exception(e)
        return []


# =====================================================
# STEP 3 – TOPIC INPUT
# =====================================================

st.divider()
st.header("📘 Enter Topic")

topic = st.text_input("Enter a topic you studied:")
generate_btn = st.button("Generate Questions")


# =====================================================
# STEP 4 – GENERATE QUESTIONS (MODIFIED CORRECTLY)
# =====================================================

if generate_btn:

    if topic.strip() == "":
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Generating multi-framed questions..."):
            time.sleep(1)
            st.session_state.questions = safe_generate(topic, st.session_state.mode)
            st.session_state.topic = topic
            st.session_state.evaluated = False


# =====================================================
# STEP 5 – DISPLAY QUESTIONS (STABILITY LAYER)
# =====================================================

st.divider()
st.subheader("Generated Questions")

if st.session_state.questions:
    for i, q in enumerate(st.session_state.questions, 1):
        st.markdown(f"**Q{i}:** {q}")
else:
    st.info("No questions generated yet.")