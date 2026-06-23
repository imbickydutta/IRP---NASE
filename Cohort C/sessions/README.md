# AI Systems Interview Portfolio
## Cohort C — New Age Software Engineering Program

---

## Program Overview

An 8-session AI engineering interview prep curriculum. Each session produces one standalone Python module. Together, these modules form an **AI Systems Interview Portfolio** that demonstrates real AI engineering skills to hiring managers and technical interviewers.

Students leave with a GitHub repository containing 8 working Python modules, each solving a distinct AI engineering problem — from prompt engineering and LLMOps to RAG pipelines, agents, and vision models.

---

## Why a Portfolio (Not a Single App)

Cohort C students are AI engineers, not web developers. The portfolio format has three advantages:

1. **Concept isolation** — Each module demonstrates a specific AI concept cleanly, without web dev overhead obscuring the AI logic.
2. **Interview versatility** — Students can walk through any single module during a technical screen without needing the full stack running.
3. **Progressive complexity** — Modules build on each other (Session 4 RAG feeds Session 5 evaluation, Session 6 agent), so the portfolio tells a coherent engineering story.

---

## Technology Stack

| Component | Tool | Notes |
|---|---|---|
| LLM | Gemini 1.5 Flash (`google-generativeai`) | Free tier — get key at [aistudio.google.com](https://aistudio.google.com) |
| Embeddings | `sentence-transformers` all-MiniLM-L6-v2 | Local, no API key required |
| Vector DB | ChromaDB | Local persistent, no server needed |
| Language | Python 3.10+ | Standard library + pip packages only |
| Dev Tools | Claude Code / Cursor | AI-assisted development throughout |
| Cost | **Zero** | All free tier — no credit card required |

---

## 8-Session Overview Table

| # | Module | Deliverable | Main Topic |
|---|---|---|---|
| 1 | Structured Output Prompt Engine | `structured_output_engine.py` + `output_examples.json` | Prompt engineering |
| 2 | LLM Logging and Evaluation Tracker | `llm_logger.py` + `llm_logs.csv` + `eval_summary.json` | LLMOps basics |
| 3 | Serverless-Style AI Function | `ai_handler.py` + `.env.example` + local test output | Serverless architecture thinking |
| 4 | Basic RAG Pipeline | `rag_pipeline.py` + `chroma_db/` folder (local persistent) | Embeddings and retrieval |
| 5 | RAG Evaluation and Improvement | `rag_evaluator.py` + `rag_eval_report.csv` + before/after comparison output | RAG evaluation |
| 6 | Simple Agent Router | `agent_router.py` + test_queries output showing intent → tool → result for each | Agent vs chatbot distinction |
| 7 | Vision/OCR Mini Module | `vision_ocr_module.py` + `sample_image.png/jpg` + `ocr_output.json` | Vision-language models |
| 8 | Final System Design and Interview Demo | `README.md` + `architecture_diagram.md` + `demo_script.md` + `viva_prep.md` + `module_summary.md` | AI system design explanation |

---

## Portfolio Module Map

```
Session 1: structured_output_engine.py
    |
    v
Session 2: llm_logger.py  (wraps any LLM call, including Session 1)
    |
    v
Session 3: ai_handler.py  (serverless wrapper pattern, standalone)
    |
    v
Session 4: rag_pipeline.py  ──────────────────────┐
    |                                               |
    v                                               v
Session 5: rag_evaluator.py          Session 6: agent_router.py
(evaluates Session 4 output)         (imports rag_pipeline as one tool)
    |
    v
Session 7: vision_ocr_module.py  (standalone, adds multimodal layer)
    |
    v
Session 8: Final Interview Demo  (ties all modules together into a design narrative)
```

Key dependency: **Session 4 feeds Session 5 and Session 6.** Students must complete Session 4 before starting either of those. All other sessions are otherwise independently runnable.

---

## Final Student Pitch

The 4-sentence portfolio explanation students should deliver in interviews:

> "I built an 8-module AI engineering portfolio covering the full stack of modern LLM systems — from structured prompt engineering and LLMOps logging, to a production-style RAG pipeline with evaluation, a multi-tool agent router, and a vision OCR module. Every module is a standalone Python script using Gemini 1.5 Flash and open-source tools like ChromaDB and sentence-transformers, so there is no cloud lock-in and no ongoing cost. I can walk you through any module end-to-end — the retrieval logic, the evaluation metrics, or the agent routing decision tree — depending on what your team works on. The portfolio is on GitHub and every script runs from a single terminal command."

---

## Setup Guide

### 1. Get a free Gemini API key
Go to [aistudio.google.com](https://aistudio.google.com), sign in with a Google account, and create an API key. The free tier is sufficient for all 8 sessions.

### 2. Create a `.env` file
In the root of your sessions folder (or in each session folder), create a `.env` file:
```
GEMINI_API_KEY=your_key_here
```
Never commit this file to GitHub. Each session folder includes a `.env.example` as a safe template.

### 3. Install dependencies
```bash
pip install google-generativeai sentence-transformers chromadb python-dotenv pillow
```

### 4. Verify the install
```bash
python -c "import google.generativeai as genai; print(genai.__version__)"
python -c "from sentence_transformers import SentenceTransformer; print('OK')"
python -c "import chromadb; print(chromadb.__version__)"
```

All three commands should print a version string or "OK" with no errors.

---

## Instructor Usage Guide

1. **Run sessions in order** — Sessions 4, 5, and 6 have a hard dependency chain. Always deliver Session 4 before 5 or 6.
2. **Use the session plan notes** — Each `session_X/` folder contains an instructor session plan with interview questions. Read it before the session, not during.
3. **Do not extend scope mid-session** — If a student asks to add a feature not in the deliverables table, log it as a stretch goal for after Session 8. Scope creep is the primary cause of incomplete portfolios.
4. **Treat every module as interview prep** — After each session, ask the student to explain the module out loud as if in a technical screen. Use the interview questions in the session notes.
5. **Push to GitHub after each session** — Students should commit and push the session deliverable the same day it is built. A stale local repo is a portfolio that does not exist.
6. **Flag API key issues immediately** — If a student cannot authenticate with Gemini in the first 5 minutes of a session, stop and resolve it before building anything. All 8 sessions require a working API key.

---

## Student Usage Guide

1. **Complete the pre-read before each session** — Each `session_X/` folder contains a pre-read document. Skimming it takes 10 minutes and saves 30 minutes of confusion during the session.
2. **Run the deliverable before marking a session done** — A module that does not run from a clean terminal is not a deliverable. Test with `python session_X/module_name.py` from the sessions root.
3. **Commit after every session** — Use a simple commit message like `Add Session 4: RAG pipeline`. Your commit history is part of the portfolio.
4. **Keep your `.env` out of Git** — Add `.env` to your `.gitignore` immediately. If you accidentally push your API key, rotate it at aistudio.google.com right away.
5. **Do not combine modules into one file** — The portfolio value comes from each module being clean and independently readable. Avoid the urge to merge them.
6. **Practice the 4-sentence pitch** — Deliver it out loud after Session 8. Record yourself if needed. Interviewers will ask "tell me about your projects" within the first 5 minutes.

---

## Execution Rules

1. Each session produces exactly the deliverables listed in the 8-Session Overview Table — no more, no less.
2. Every Python module must run from a single terminal command with no arguments required (use hardcoded sample inputs or defaults for demo runs).
3. All LLM calls go through Gemini 1.5 Flash via `google-generativeai`. No other LLM provider is used in any module.
4. API keys are loaded from `.env` via `python-dotenv`. Hard-coded API keys in source files are not permitted.
5. No web framework (Flask, FastAPI, Streamlit, Gradio) is used in any module. All I/O is terminal or file-based.
6. Session 4 (`rag_pipeline.py`) must be fully working before Session 5 or Session 6 begins.
7. Each module must include a `if __name__ == "__main__":` block that demonstrates the module's core function end-to-end when run directly.
8. Output files (`llm_logs.csv`, `rag_eval_report.csv`, `ocr_output.json`, etc.) are written to the session's own folder, not to a shared output directory.

---

## Scope Control Rules

1. **No UI work** — If a feature requires a browser, a server, or a GUI, it is out of scope for Cohort C. Redirect to the terminal-first deliverable.
2. **No new dependencies mid-session** — The approved stack is `google-generativeai`, `sentence-transformers`, `chromadb`, `python-dotenv`, `pillow`. Any additional package requires instructor sign-off before installation.
3. **One module per session** — A session ends when the listed deliverable runs cleanly. Starting the next session's module in the same sitting is not permitted.
4. **Stretch goals go in a `stretch_notes.md`** — Good ideas that are out of scope for the session deliverable are recorded in a `stretch_notes.md` file in that session's folder, not implemented.
5. **No refactoring previous sessions during a new session** — If Session 6 reveals a bug in Session 4, log it and fix Session 4 separately. Do not patch across sessions during active build time.
6. **Session 8 is documentation and design, not new code** — No new Python modules are written in Session 8. The deliverables are Markdown files only.

---

## Folder Structure

```
sessions/
├── README.md                          <- This file
├── session_1/
│   ├── structured_output_engine.py
│   ├── output_examples.json
│   ├── .env.example
│   ├── session_1_student_pre_session_preread_prerequisites_prompts.md
│   ├── session_1_instructor_session_plan_notes_interview_questions.md
│   └── session_1_after_session_notes.md
├── session_2/
│   ├── llm_logger.py
│   ├── llm_logs.csv
│   ├── eval_summary.json
│   ├── .env.example
│   ├── session_2_student_pre_session_preread_prerequisites_prompts.md
│   ├── session_2_instructor_session_plan_notes_interview_questions.md
│   └── session_2_after_session_notes.md
├── session_3/
│   ├── ai_handler.py
│   ├── .env.example
│   ├── session_3_student_pre_session_preread_prerequisites_prompts.md
│   ├── session_3_instructor_session_plan_notes_interview_questions.md
│   └── session_3_after_session_notes.md
├── session_4/
│   ├── rag_pipeline.py
│   ├── chroma_db/                     <- Local persistent ChromaDB (auto-created on first run)
│   ├── .env.example
│   ├── session_4_student_pre_session_preread_prerequisites_prompts.md
│   ├── session_4_instructor_session_plan_notes_interview_questions.md
│   └── session_4_after_session_notes.md
├── session_5/
│   ├── rag_evaluator.py
│   ├── rag_eval_report.csv
│   ├── .env.example
│   ├── session_5_student_pre_session_preread_prerequisites_prompts.md
│   ├── session_5_instructor_session_plan_notes_interview_questions.md
│   └── session_5_after_session_notes.md
├── session_6/
│   ├── agent_router.py
│   ├── .env.example
│   ├── session_6_student_pre_session_preread_prerequisites_prompts.md
│   ├── session_6_instructor_session_plan_notes_interview_questions.md
│   └── session_6_after_session_notes.md
├── session_7/
│   ├── vision_ocr_module.py
│   ├── sample_image.png
│   ├── ocr_output.json
│   ├── .env.example
│   ├── session_7_student_pre_session_preread_prerequisites_prompts.md
│   ├── session_7_instructor_session_plan_notes_interview_questions.md
│   └── session_7_after_session_notes.md
├── session_8/
│   ├── README.md
│   ├── architecture_diagram.md
│   ├── demo_script.md
│   ├── viva_prep.md
│   └── module_summary.md
└── qc/
    ├── session_checklist.md           <- Per-session QC checklist for instructors
    ├── portfolio_review_rubric.md     <- Final portfolio grading rubric
    └── common_errors.md               <- Known issues and fixes across all sessions
```

---

## Reuse Guide

To run this curriculum for a new cohort, edit two variables at the top of the workflow orchestration script:

```python
SESSIONS_FOLDER = "/path/to/new/cohort/sessions"
COHORT = "Cohort D"  # or whichever cohort label applies
```

All session plan files, deliverable templates, and QC checklists in this folder structure are cohort-agnostic. No other changes are required to reuse the full 8-session curriculum for a new group of students.
