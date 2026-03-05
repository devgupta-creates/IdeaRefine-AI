REQUIRED_STAGES = ["domain", "problem", "user", "solution", "priority"]
import streamlit as st

from prompts import QUESTION_BANK
from ai_engine import decide_next_stage, generate_prd, generate_brd

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Startup Idea Refiner",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 AI Startup Idea Refiner")
st.caption("Turn a raw startup idea into a structured PRD & BRD")

st.divider()

# -------------------------------
# SESSION STATE (APP MEMORY)
# -------------------------------
if "idea" not in st.session_state:
    st.session_state.idea = ""

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "current_stage" not in st.session_state:
    st.session_state.current_stage = None

# -------------------------------
# STEP 1: IDEA INPUT SCREEN
# -------------------------------
if st.session_state.idea == "":
    st.subheader("💡 Enter your startup idea")

    idea_input = st.text_area(
        "Describe your startup idea in 2–3 lines",
        height=120,
        placeholder="Example: A platform that helps college students find affordable PGs near campuses."
    )

    if st.button("Start Refinement →"):
        if idea_input.strip() == "":
            st.warning("Please enter your idea first.")
        else:
            st.session_state.idea = idea_input
            st.rerun()

# -------------------------------
# STEP 2: AI-DRIVEN QUESTION FUNNEL
# -------------------------------
else:
    # ✅ CHECK IF ALL QUESTIONS ARE ANSWERED
    if len(st.session_state.answers) >= len(REQUIRED_STAGES):

        st.success("✅ Idea refinement completed")

        all_inputs = {
            "idea": st.session_state.idea,
            "refinements": st.session_state.answers
        }

        if st.button("Generate PRD & BRD"):
            with st.spinner("Generating documents..."):
                prd = generate_prd(all_inputs)
                brd = generate_brd(all_inputs)

            st.subheader("📄 Product Requirements Document (PRD)")
            st.markdown(prd)

            st.subheader("📄 Business Requirements Document (BRD)")
            st.markdown(brd)

    else:
        # 🔹 ASK NEXT QUESTION
        if st.session_state.current_stage is None:
            stage = decide_next_stage(
                st.session_state.idea,
                st.session_state.answers
            )

            # SAFETY: avoid repeating answered stages
            if stage in st.session_state.answers:
                stage = next(
                    s for s in REQUIRED_STAGES
                    if s not in st.session_state.answers
                )

            st.session_state.current_stage = stage

        stage = st.session_state.current_stage
        q_data = QUESTION_BANK[stage]

        st.subheader(f"Refining: {stage.capitalize()}")
        st.write(q_data["question"])

        selected = st.radio(
            "Select one option:",
            q_data["options"],
            key=stage
        )

        if st.button("Next →"):
            st.session_state.answers[stage] = selected
            st.session_state.current_stage = None
            st.rerun()