# AI Support Ticket Resolution Copilot

## Cohort B — New Age Software Engineering Program — Interview Preparation Phase

---

## Program Overview

The Interview Preparation Phase (IRP) of the New Age Software Engineering (NASE) program is a focused, project-driven sprint designed to bridge the gap between learning and job-readiness. Students who have completed the 6–7 month AI, No-Code, and GenAI curriculum enter this phase to build a real, deployable full-stack AI application that they can speak to confidently in technical interviews. Each cohort is assigned a distinct project so that learning stays fresh and portfolio work remains unique. Cohort B builds the **AI Support Ticket Resolution Copilot** — an intelligent backend service that combines traditional REST API design with modern RAG-based retrieval and agentic AI workflows.

---

## Project Overview

The AI Support Ticket Resolution Copilot is a backend API service that allows support agents and end-users to submit tickets, automatically classify and route them, retrieve relevant knowledge base articles via semantic search, and generate AI-drafted resolution responses — all within a governed LangGraph workflow. Unresolved or low-confidence tickets are escalated automatically, and every resolution attempt is scored by an LLM-as-judge evaluator to drive continuous improvement.

This project is an outstanding portfolio piece because it touches every layer of a modern AI-powered product: database design, REST API authoring, vector search, agentic AI orchestration, evaluation frameworks, and production-grade testing. It demonstrates to interviewers that the student can design end-to-end systems, not just call an LLM API. The codebase is small enough to explain fully in a 30-minute interview yet rich enough to generate two hours of deep technical conversation.

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.11+ | Core application runtime |
| API Framework | FastAPI | REST endpoint definition, request validation, OpenAPI docs |
| ORM / Schema | SQLModel | Combines SQLAlchemy models with Pydantic validation |
| Database | PostgreSQL | Persistent storage for users, tickets, and resolution history |
| Migrations | Alembic | Schema versioning and safe database upgrades |
| Auth | JWT (python-jose) | Stateless token-based authentication and route protection |
| Vector Store | ChromaDB | Embedding storage and semantic similarity search |
| Embeddings | sentence-transformers | Local, offline-capable text embedding generation |
| AI Workflow | LangGraph | Stateful agentic graph: classify → retrieve → respond → escalate |
| LLM | OpenAI / Anthropic API | Resolution generation and LLM-as-judge evaluation |
| Testing | pytest + pytest-cov | Unit and integration test suite with coverage reporting |
| Containerisation | Docker + docker-compose | Single-command local environment and deployment-ready packaging |
| Logging | Python structlog | Structured, machine-readable application logs |

---

## 8-Session Overview

| # | Session Title | What Gets Built | Key Concept |
|---|---|---|---|
| 1 | Project Setup + FastAPI Foundation | FastAPI skeleton, SQLModel connection, Alembic config, PostgreSQL integration, folder scaffold | Project architecture and layered design |
| 2 | Auth + User Management | User model, registration and login endpoints, JWT token issuance, protected route dependency | Stateless authentication and security |
| 3 | Ticket CRUD + Data Modeling | Full ticket lifecycle (create / read / update / close), status enum, pagination, query filtering | REST resource design and data integrity |
| 4 | RAG Knowledge Base | ChromaDB setup, sentence-transformer embedding pipeline, document ingestion script, semantic search endpoint | Retrieval-Augmented Generation fundamentals |
| 5 | LangGraph AI Resolution Engine | LangGraph state graph, four nodes (classify, retrieve, respond, escalate), integration with ticket API | Agentic workflow design and state management |
| 6 | Evaluation + Quality Metrics | LLM-as-judge prompt, resolution quality scoring, score persistence, eval dashboard endpoint | AI evaluation methodology and quality loops |
| 7 | Testing + LLMOps | pytest suite for auth, CRUD, RAG, and graph nodes; coverage report; structured logging; health check | Production readiness and observability |
| 8 | Demo Day Prep | Codebase polish, environment variable hardening, docker-compose, interview Q&A rehearsal, live demo run | Communication, system narrative, interview readiness |

---

## Folder Structure

```
sessions/
├── README.md                          ← this file
│
├── session_1/
│   ├── session_1_instructor_session_plan_notes_interview_questions.md
│   ├── session_1_student_pre_session_preread_prerequisites_prompts.md
│   └── session_1_after_session_notes.md
│
├── session_2/
│   ├── session_2_instructor_session_plan_notes_interview_questions.md
│   ├── session_2_student_pre_session_preread_prerequisites_prompts.md
│   └── session_2_after_session_notes.md
│
├── session_3/
│   ├── session_3_instructor_session_plan_notes_interview_questions.md
│   ├── session_3_student_pre_session_preread_prerequisites_prompts.md
│   └── session_3_after_session_notes.md
│
├── session_4/
│   ├── session_4_instructor_session_plan_notes_interview_questions.md
│   ├── session_4_student_pre_session_preread_prerequisites_prompts.md
│   └── session_4_after_session_notes.md
│
├── session_5/
│   ├── session_5_instructor_session_plan_notes_interview_questions.md
│   ├── session_5_student_pre_session_preread_prerequisites_prompts.md
│   └── session_5_after_session_notes.md
│
├── session_6/
│   ├── session_6_instructor_session_plan_notes_interview_questions.md
│   ├── session_6_student_pre_session_preread_prerequisites_prompts.md
│   └── session_6_after_session_notes.md
│
├── session_7/
│   ├── session_7_instructor_session_plan_notes_interview_questions.md
│   ├── session_7_student_pre_session_preread_prerequisites_prompts.md
│   └── session_7_after_session_notes.md
│
└── session_8/
    ├── session_8_instructor_session_plan_notes_interview_questions.md
    ├── session_8_student_pre_session_preread_prerequisites_prompts.md
    └── session_8_after_session_notes.md
```

Each session folder contains exactly three files:
- **Instructor plan** — session agenda, live-coding checkpoints, discussion prompts, and interview questions the instructor can fire at the student.
- **Student pre-session** — pre-reads, prerequisite checks, setup steps, and AI-assisted coding prompts the student completes before arriving.
- **After-session notes** — what was built, blockers encountered, carry-over tasks, and reflection questions.

---

## Setup Guide

Follow these steps to get the project running locally from scratch. Complete them once before Session 1 begins.

**Step 1 — Clone or create the project folder**

```bash
mkdir ai-support-copilot && cd ai-support-copilot
```

**Step 2 — Create and activate a Python virtual environment**

```bash
python3.11 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

**Step 3 — Install base dependencies**

```bash
pip install fastapi uvicorn sqlmodel alembic psycopg2-binary \
            python-jose[cryptography] passlib[bcrypt] \
            chromadb sentence-transformers \
            langgraph openai \
            structlog pytest pytest-cov httpx python-dotenv
pip freeze > requirements.txt
```

**Step 4 — Configure environment variables**

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/support_copilot
SECRET_KEY=your-jwt-secret-key-at-least-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=sk-...
CHROMA_PERSIST_DIR=./chroma_db
```

**Step 5 — Create the PostgreSQL database**

```bash
psql -U postgres -c "CREATE DATABASE support_copilot;"
```

**Step 6 — Initialise Alembic and run the first migration**

```bash
alembic init alembic
# Edit alembic/env.py to import your SQLModel metadata and read DATABASE_URL from .env
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

**Step 7 — Start the development server**

```bash
uvicorn app.main:app --reload --port 8000
```

The API and interactive docs are now available at `http://localhost:8000/docs`.

---

## Instructor Usage Guide

- **Read the instructor plan before each session.** The instructor file contains a timed agenda, live-coding checkpoints, and a bank of interview-style questions to fire at the student mid-session to simulate real interview pressure. Skim it the night before so the session flows naturally.

- **Use the pre-session file to set homework.** Send the student their pre-session file 24–48 hours before the session. It contains pre-reads and setup tasks that free up live session time for building and discussion rather than installation and orientation.

- **Run checkpoints, not lectures.** Each session has marked checkpoints (e.g., "server starts with no errors", "JWT token returned by /login"). Pause at each one, ask the student to explain what they just built, and only move forward when the checkpoint passes. This mirrors the explain-your-code dynamic of technical interviews.

- **Use the after-session notes to track carry-over.** If a checkpoint is not reached, record it in the after-session notes file and prioritise it at the start of the next session. Never skip a checkpoint silently — incomplete foundations cause compounding problems in later sessions.

- **Adapt the AI tool guidance deliberately.** Students are proficient with Cursor and Antigravity. For Sessions 1–3, encourage them to type foundational boilerplate themselves rather than generate it entirely with AI, so they own the mental model. From Session 4 onward, AI-assisted scaffolding is appropriate and encouraged.

- **Treat Session 8 as a dress rehearsal, not a coding session.** No new features should be introduced in Session 8. The instructor's role is to act as a tough interviewer: ask system design questions, probe for trade-off reasoning, and give feedback on how the student narrates their project. Record the session if possible so the student can review their own delivery.

---

## Student Usage Guide

- **Complete your pre-session file before every session without exception.** The pre-session file is not optional homework — it is the prerequisite for the live session. If you arrive without completing it, the session cannot proceed as planned and you fall behind irreversibly.

- **Build every line of code yourself.** You may use Cursor or Antigravity to assist, but you must be able to explain every line that ends up in your codebase. If you cannot explain it, delete it and rewrite it until you can. Interviewers will ask you to walk through specific functions.

- **Run the server after every checkpoint.** Do not accumulate 30 minutes of changes before testing. Run `uvicorn app.main:app --reload` after each logical unit of work and confirm the endpoint behaves as expected. Debugging a small change is fast; debugging an hour of changes is painful.

- **Write the after-session notes in your own words immediately after each session.** Do not copy the instructor's notes. Write what you built, what confused you, and what you would do differently. This reflection loop accelerates learning and produces material you can use directly in interviews when asked about challenges you faced.

- **Commit to Git after every session.** Create a clean Git commit at the end of each session with a meaningful message. Your commit history is a visible signal of disciplined engineering practice to technical interviewers who review your GitHub profile.

- **Prepare two-minute verbal answers for every session's key concepts.** At the start of each session, your instructor may ask you to explain the previous session's concepts from scratch. Practice explaining JWT authentication, RAG retrieval, and LangGraph state graphs out loud — not just in your head — because verbal fluency is what interviews test.

---

## Execution Rules

1. **Scope is fixed.** The project scope is defined at the start and does not change mid-program. Feature ideas outside the defined scope are logged for personal exploration after the IRP ends, never introduced mid-sprint. Scope creep destroys demo-day readiness.

2. **AI tools accelerate, they do not replace understanding.** Use Cursor and Antigravity to move faster, generate boilerplate, and debug syntax errors. Never use them to bypass understanding a concept. If the AI generates a solution you cannot explain, treat that as a gap to close, not a shortcut to keep.

3. **Every session has a hard stop.** Sessions run for a defined duration. Work not completed within the session is tracked in the after-session notes and addressed at the start of the next session. Extended sessions erode student energy and instructor scheduling.

4. **No skipping sessions.** Each session builds directly on the previous one. Missing or skipping a session requires a make-up before the cohort continues. There is no mechanism for catching up by reading notes alone — the live building experience is mandatory.

5. **PostgreSQL runs locally, not on a shared cloud instance.** Each student maintains their own local database. This avoids shared-state bugs, teaches environment ownership, and mirrors real developer workflows. Students are responsible for their own data.

6. **Tests must pass before Session 7 wraps up.** The pytest suite is not cosmetic. If tests fail at the end of Session 7, the student fixes them before Session 8 begins. A passing test suite is a non-negotiable entry ticket to Demo Day prep.

7. **Demo Day is a real interview simulation.** Session 8 is conducted as if the instructor is a technical interviewer who has never seen the project. The student must introduce the system, walk through the architecture, answer adversarial questions, and run a live demo without referring to notes. Preparation is the student's responsibility.

8. **Reflections are written, not verbal.** After-session notes must be written in the session notes file, not verbally summarised and forgotten. The written record is what enables the student to reconstruct their learning arc during interview prep and what enables the instructor to identify patterns across cohorts.

---

## Reuse Guide

This session framework is designed to be cohort-portable. To adapt it for a new cohort or a new project, replace the project name and technology stack in this README, create a fresh `sessions/` folder with eight numbered session subdirectories, and regenerate the three standard files per session (instructor plan, student pre-session, after-session notes) using the same naming convention: `session_N_instructor_session_plan_notes_interview_questions.md`, `session_N_student_pre_session_preread_prerequisites_prompts.md`, and `session_N_after_session_notes.md`. The eight-session arc — foundation, auth, data layer, AI integration, orchestration, evaluation, testing, demo prep — is intentionally generic and maps cleanly onto any full-stack AI backend project. The execution rules, instructor usage guide, and student usage guide in this README require no edits between cohorts; they describe process, not project. The technology stack table and session overview table are the only sections that need to be rewritten for a new project. Retain the folder structure, file naming convention, and three-file-per-session discipline across all cohorts so that session content remains searchable, comparable, and easy to hand off between instructors.

---

*Last updated: June 2026 — Cohort B, IRP - NASE*
