import os
try:
    from langchain_groq import ChatGroq
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "Missing dependency 'langchain_groq'. Install it with:\n\n"
        "  python3 -m pip install langchain-groq\n"
    ) from e
from langchain_core.messages import HumanMessage

# Some environments still attempt ASCII encoding for logs/output.
# Replace uncommon Unicode line separators with normal newlines.
def _sanitize_text(text: str) -> str:
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    return text.replace("\u2028", "\n").replace("\u2029", "\n")

# --------------------------------
# GROQ LLM CONFIG (UPDATED MODEL)
# --------------------------------
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError(
        "Environment variable GROQ_API_KEY is not set. "
        "Create a Groq API key and export GROQ_API_KEY before running the app."
    )

llm = ChatGroq(
    model="llama-3.1-8b-instant",  # ✅ supported model
    temperature=0.3,
    api_key=api_key,
)

# --------------------------------
# AI DECIDES NEXT QUESTION STAGE
# --------------------------------
def decide_next_stage(idea, answers):
    prompt = f"""
You are a senior product manager.

Startup idea:
{idea}

Answers collected so far:
{answers}

From the following stages, decide the NEXT most important stage to ask:
- domain
- problem
- user
- solution
- priority

If all stages are sufficiently covered, reply with:
DONE

Reply with ONLY ONE WORD.
"""
    response = llm.invoke(prompt)
    return _sanitize_text(response.content).strip().lower()

# --------------------------------
# PRD GENERATOR
# --------------------------------
def generate_prd(all_inputs):
    prompt = f"""
You are a senior product manager.

Create a professional PRODUCT REQUIREMENTS DOCUMENT (PRD)
using the following information:

Startup Idea:
{all_inputs['idea']}

Refined Inputs:
{all_inputs['refinements']}

The PRD must include:
1. Product Overview
2. Problem Statement
3. Target Users
4. Core Features
5. Success Metrics
6. Risks & Assumptions

Write in a clear, structured, professional tone.
Use bullet points where appropriate.
"""
    response = llm.invoke(prompt)
    return _sanitize_text(response.content)

# --------------------------------
# BRD GENERATOR
# --------------------------------
def generate_brd(all_inputs):
    prompt = f"""
You are a business analyst.

Create a professional BUSINESS REQUIREMENTS DOCUMENT (BRD)
using the following information:

Startup Idea:
{all_inputs['idea']}

Refined Inputs:
{all_inputs['refinements']}

The BRD must include:
1. Business Objectives
2. Stakeholders
3. Project Scope
4. Key KPIs
5. Constraints & Dependencies

Write in a formal business style.
"""
    response = llm.invoke(prompt)
    return _sanitize_text(response.content)