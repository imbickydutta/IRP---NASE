# Session 8 Instructor File: Deployment, Demo, System Design, and Mock Interview

## Session Title

Deployment, Demo, System Design, and Mock Interview

## Duration

2 hours

## Project

AI Support Ticket Resolution Copilot

## Session 8 Objective

By the end of Session 8, students will have a fully deployed, documented, and demo-ready AI Support Ticket Resolution Copilot running live on Railway (or Render). They will be able to explain the complete system — data flow, AI pipeline, design decisions, and trade-offs — to a technical interviewer with confidence.

This is the final session. There is no new feature to build. The work is: polish, ship, document, and explain.

## Session 8 Deliverable

Students will complete the following by end of session:

1. Clean `requirements.txt` generated from `pip freeze` with pinned versions
2. `.env.example` file with all required environment variable keys and placeholder values
3. `README.md` with project overview, architecture diagram, API reference, setup instructions, AI features, limitations, and future improvements
4. Text-based or Mermaid architecture diagram embedded in README
5. Backend deployed to Railway (or Render) — live URL accessible
6. Swagger UI accessible at `<live-url>/docs`
7. 3-minute demo script covering one complete ticket lifecycle
8. System design explanation rehearsed and interview-ready

---

## Strict Scope Control

### Include

- `requirements.txt` cleanup and pinning via `pip freeze`
- `.env.example` with all environment variable keys and placeholder values
- `README.md` with: project overview, architecture diagram, API list, setup instructions, AI features description, limitations, future improvements
- Text-based or Mermaid architecture diagram in Markdown
- Railway (or Render) free-tier deployment: connect GitHub repo, set environment variables in dashboard, push-to-deploy
- Verify Swagger UI is accessible on live URL at `/docs`
- 3-minute demo script: one complete ticket lifecycle (create → classify → retrieve → suggest → resolve)
- System design explanation covering data flow, AI pipeline, trade-offs
- Mock viva practice using the interview questions in this file

### Do Not Include

- Docker (mention as a future improvement only — do not build a Dockerfile)
- Kubernetes, ECS, Cloud Run, or any container orchestration
- AWS, GCP, or Azure deployment
- CI/CD pipelines (GitHub Actions, CircleCI)
- Frontend UI of any kind
- New AI features (no new LLM calls, embeddings, or LangGraph nodes)
- Database migration scripts for production (SQLite is acceptable for this project)
- Load balancing, reverse proxy, or nginx configuration
- Refresh token rotation or OAuth
- Rate limiting middleware
- Alembic migrations (out of scope — SQLModel creates tables on startup for this project)

---

# Instructor Framing

## Opening Message

In Sessions 1 through 7, we built one complete AI backend system from scratch. We have a FastAPI server with JWT auth, a ticket CRUD API backed by SQLModel, an LLM classifier, a RAG knowledge base using ChromaDB, a LangGraph agentic workflow, custom evals, guardrails, and pytest coverage.

Today we are not adding any new feature. Today we are doing what separates a side project from a portfolio-ready product: we are going to document it, deploy it, and explain it like engineers do in real job interviews.

By the end of this session, your backend will be live on a public URL, your README will describe the system like a real engineering team wrote it, and you will be able to walk a technical interviewer through the entire architecture without looking at your notes.

## Key Philosophy

Shipping matters. A working system with no README, no deployment, and no explanation has zero interview value. A deployed, documented system that the student can explain confidently is worth far more than a locally-running project no one else can access.

Students should treat this session as a technical interview simulation. Every step — writing the README, explaining the architecture, answering viva questions — is practice for the real thing.

## Repeated Instructor Line

Interviewers do not run your code. They ask you to explain it. Your job today is to become the expert on the system you built.

---

# Session Flow

## 0–10 min: Opening and Session 7 Recap

### Instructor Goal

Establish the "final session" mindset. Students should feel the weight of shipping something real.

### Recap Session 7 State

Confirm students have the following from Session 7:

- `tests/` directory with at least 3 pytest tests covering ticket creation, classification, and guardrail behavior
- `app/guardrails.py` with a prompt-based guardrail function that rejects off-topic or adversarial input
- `app/evals/` directory with a custom eval script that runs against a golden test set
- All routes protected by JWT middleware in `app/auth.py`
- LangGraph workflow in `app/graph.py` with at minimum: classify node, retrieve node, suggest node
- ChromaDB collection populated via `app/knowledge_base.py`
- `.env` file with: `OPENAI_API_KEY`, `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`

### Ask Students Before Moving On

"Can you hit POST /tickets on localhost and get a 201? Can you hit GET /tickets/{id}/suggest and get an AI-generated suggestion back? If yes, you are ready for today."

If any student cannot confirm these two endpoints work, pair them with another student for the first 20 minutes and come back to fix it after deployment setup is done for the group.

### Set the Session Agenda

Write on the board or share screen:

1. Clean requirements.txt and .env.example (10 min)
2. Write the README with architecture diagram (25 min)
3. Deploy to Railway (20 min)
4. Rehearse demo script (15 min)
5. System design explanation (15 min)
6. Mock viva practice (20 min)
7. Final wrap-up and demo run (15 min)

---

## 10–20 min: Architecture Breakdown — What Are We Documenting and Why

### Instructor Goal

Help students see the full system they built before they write about it. Students often cannot write a README because they do not have a mental model of the whole system.

### Draw or Display the Architecture

Present this data flow on whiteboard or shared screen:

```
Client (Swagger / curl / Postman)
        |
        v
FastAPI Router (app/main.py)
        |
    [JWT Middleware] (app/auth.py)
        |
        v
   Route Handlers
   (app/routes/tickets.py, users.py)
        |
        v
   SQLModel ORM (app/models.py)
        |
        v
   SQLite Database (support.db)
        |
        v
   LLM Classifier (app/classifier.py)
   --> OpenAI API (gpt-4o-mini)
        |
        v
   RAG Retriever (app/knowledge_base.py)
   --> ChromaDB (local vector store)
   --> OpenAI Embeddings API
        |
        v
   LangGraph Agent (app/graph.py)
   --> Classify Node --> Retrieve Node --> Suggest Node
        |
        v
   Guardrails (app/guardrails.py)
   --> Prompt-based filter before LLM calls
        |
        v
   Evals (app/evals/)
   --> Offline eval runner against golden test set
```

### Explain Each Layer in One Sentence

Go through each layer. Ask students: "What does this layer do? Who calls it? What does it return?" Students should answer from memory. This is oral exam practice.

### Instructor Explanation

Every component we built has a specific job. The README needs to describe these jobs clearly — not for you, but for the next engineer who wants to run your project or for the interviewer evaluating whether you understand what you built.

---

## 20–35 min: Build — requirements.txt, .env.example, and README

### Instructor Goal

Use Claude Code or Cursor to generate the documentation files. Show students how to prompt an AI coding assistant for documentation tasks, not just code tasks.

### Step 1: Generate requirements.txt

In the project terminal:

```bash
pip freeze > requirements.txt
```

Open the file and scan for anything that should not be there (system packages, local editable installs). Ask Claude Code to clean it up if needed.

### Step 2: Generate .env.example

Create a new file `.env.example` at the project root. Manually list every key from the current `.env` but replace actual values with descriptive placeholders. Never commit the real `.env` file.

Confirm the following keys are present in `.env.example`:

```
OPENAI_API_KEY=sk-your-openai-api-key-here
DATABASE_URL=sqlite:///./support.db
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### Step 3: Use the README Prompt from the Student File

Show the student the Prompt 1 from their pre-session file and run it in Claude Code. Walk through the generated README section by section as it is produced.

### What to Watch For in Generated README

- Architecture diagram must be present (Mermaid or text-based with arrows)
- API table must list all 8-10 endpoints with method, path, auth required, and description
- Setup instructions must reference `.env.example` not `.env`
- AI features section must name the specific models used (gpt-4o-mini, text-embedding-3-small)
- Limitations section must be honest (SQLite not production-grade, no async DB driver, no horizontal scaling)

### Instructor Control Rule

Do not let students spend more than 8 minutes on README cosmetics. The content matters more than the formatting for interview purposes.

---

## 35–50 min: Instructor Code Walkthrough — README, Architecture Diagram, .env.example

### Instructor Goal

Read the generated files with the class. Confirm accuracy of each section. Correct any technical inaccuracies that Claude Code introduces.

### Walk Through README Section by Section

1. **Project Overview** — Does it accurately describe the system? Is it clear what problem it solves?
2. **Architecture Diagram** — Does the diagram show all 6 layers: FastAPI, Auth, SQLModel, LLM, RAG, LangGraph?
3. **API Reference Table** — Are all endpoints listed? Is the auth requirement accurate for each?
4. **Setup Instructions** — Can a stranger follow these steps and get the app running in under 10 minutes?
5. **AI Features** — Are the model names specific (not just "OpenAI")? Are embeddings mentioned?
6. **Limitations** — Is SQLite's limitation mentioned? Is the missing async DB driver mentioned?
7. **Future Improvements** — Are concrete improvements listed (PostgreSQL, Docker, async SQLAlchemy)?

### Ask During Walkthrough

- "In the API table, is POST /tickets protected by JWT? How do you know?"
- "What is the embedding model we are using and why does the dimension matter?"
- "What does the LangGraph graph actually do? Can you describe the node sequence?"
- "Why is SQLite a limitation in production?"

### Common Inaccuracy Claude Code Will Introduce

Claude Code sometimes lists endpoints that do not exist or omits real endpoints. Cross-check the API table against `app/routes/tickets.py` and `app/routes/users.py` with students in real time.

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students independently:

1. Run `pip freeze > requirements.txt` in their project terminal
2. Create `.env.example` manually based on their `.env`
3. Run the README prompt in Claude Code and generate their README
4. Insert or adjust the architecture diagram for their specific project state
5. Add a `.gitignore` entry for `.env` and `support.db` if not already present

### Instructor Support Areas

Help students with:

- `pip freeze` including unrelated packages from their global Python environment (advise using a virtual environment; if not already using one, do not set it up live — just note it as a limitation and move on)
- README that is missing the architecture diagram (paste the text diagram from the board if needed)
- `.env.example` missing keys (compare against `app/config.py` or wherever env vars are loaded)
- `.gitignore` missing `.env` (this is a security issue — emphasize it)
- README having incorrect endpoint descriptions

### If Student README Build Fails

Do not block the class. The student should use the instructor's README as a reference and customize it after session. The deployment step is more important than README perfection.

---

## 65–80 min: Deploy to Railway

### Instructor Goal

Get every student's backend live on a public URL within 15 minutes.

### Pre-Condition

The project must be pushed to a GitHub repository. If any student has not done this, they should push now:

```bash
git init
git add .
git commit -m "final project: AI support ticket resolution copilot"
git remote add origin <their-github-url>
git push -u origin main
```

Confirm `.env` is NOT committed. Check with `git status` before pushing.

### Railway Deployment Steps (Walk Through Live)

1. Go to railway.app and sign in with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select the project repository
4. Railway will detect Python. It will try to run `python main.py` by default — this will fail for FastAPI.
5. In Railway settings, set the Start Command to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Go to "Variables" tab and add every key from `.env.example` with real values
7. Click "Deploy"
8. Wait 60-90 seconds. Watch the build logs.
9. Once deployed, Railway gives a public URL. Open `<url>/docs` to confirm Swagger is live.

### Common Railway Errors

- `ModuleNotFoundError: No module named 'app'` — Start command path is wrong. Verify it matches the actual file path (`app/main.py`).
- `Port binding error` — The app must use `$PORT` env var from Railway. Add `--port $PORT` in the start command.
- `No such file or directory: support.db` — SQLite file path is relative. Confirm `DATABASE_URL=sqlite:///./support.db` is set in Railway variables.
- Build fails with `pip install` error — A package in `requirements.txt` has an incompatible version for the Railway Python version. Check the build log for the specific package.

### Instructor Control Rule

If deployment is taking more than 15 minutes for any individual student, move them to using Render as an alternative (same process, slightly different UI). Do not let one student's deployment block the group from reaching the demo and viva sections.

---

## 80–95 min: Test and Demo Script Rehearsal

### Instructor Goal

Confirm the deployed system works end-to-end and teach students to do a structured 3-minute demo.

### Verify Deployed Endpoints

On the live Railway URL, walk through these in Swagger:

1. POST /auth/register — create a test user
2. POST /auth/token — get JWT
3. Authorize in Swagger with the JWT
4. POST /tickets — create a ticket with subject "My payment failed"
5. GET /tickets — confirm the ticket is returned
6. GET /tickets/{id} — confirm the ticket fields
7. POST /tickets/{id}/classify — confirm category label is returned
8. GET /tickets/{id}/suggest — confirm AI suggestion is returned
9. PATCH /tickets/{id}/resolve — confirm status changes to "resolved"

### Teach the 3-Minute Demo Structure

Walk students through this structure:

```
0:00 – 0:30  Introduce the system: "This is an AI Support Ticket Resolution Copilot.
              It takes customer support tickets and uses a RAG pipeline and LangGraph
              agent to classify, retrieve context, and suggest resolutions automatically."

0:30 – 1:00  Create a ticket: POST /tickets with a realistic payload.
              Show the 201 response. Point out ticket_id, status: "open".

1:00 – 1:30  Classify the ticket: POST /tickets/{id}/classify.
              Show the category label. Explain: "This calls an LLM with a system prompt
              that classifies into billing, technical, account, or general."

1:30 – 2:00  Retrieve context and suggest: GET /tickets/{id}/suggest.
              Show the AI suggestion. Explain: "This triggers the LangGraph agent —
              the retrieve node queries ChromaDB using the ticket description as a query,
              and the suggest node passes the retrieved context to the LLM."

2:00 – 2:30  Resolve the ticket: PATCH /tickets/{id}/resolve.
              Show status change to "resolved".

2:30 – 3:00  Summarize: "The full pipeline runs in under 2 seconds for a single ticket.
              Auth is handled by JWT. Every endpoint is role-protected."
```

### Student Task

Students rehearse the demo once silently using their deployed URL. Instructor calls on 2-3 students to do a live demo run for the group.

---

## 95–105 min: Concept Pause — System Design Vocabulary

### Instructor Goal

Teach students the vocabulary they need to explain this system in a system design interview. This is not about theory — it is about applying terms to the system they built.

### Explain Each Term With a Direct Reference to the Project

**Scalability**
"Our current system uses SQLite, which cannot handle concurrent writes. If we had 1000 users, the DB would become a bottleneck. We would scale by replacing SQLite with PostgreSQL and using an async DB driver like asyncpg."

**Bottleneck**
"The LLM API call in the suggest endpoint is our biggest latency bottleneck. Every GET /tickets/{id}/suggest makes a synchronous HTTP call to OpenAI. We could cache suggestion results in Redis to avoid repeated LLM calls for the same ticket."

**Trade-off**
"We chose SQLite over PostgreSQL because it requires zero infrastructure for development and demo purposes. The trade-off is that it cannot handle concurrent writes and is not suitable for production load."

**Stateless vs Stateful**
"Our FastAPI server is stateless — it does not hold any user session in memory. Authentication state is encoded in the JWT token, which the client sends with every request. This makes the server horizontally scalable."

**Vector Store**
"ChromaDB stores ticket embeddings as high-dimensional vectors. When a new ticket comes in, we embed the description and perform a cosine similarity search to find the most relevant past resolutions or knowledge base articles."

**Agent vs Chain**
"A LangChain chain is a fixed sequence of steps. A LangGraph agent has nodes that can conditionally route based on state. We used LangGraph because the workflow needed to branch: if a ticket is classified as 'billing', the retrieve node queries a billing-specific collection."

### Student Writing Task

Ask every student to write 2-3 sentences:

"What is the biggest technical limitation of the system you built, and how would you fix it in production?"

Expected answer direction: SQLite concurrency, synchronous LLM calls blocking the event loop, no caching layer, ChromaDB not suitable for millions of vectors.

---

## 105–115 min: Interview Discussion and Technical Viva Practice

### Instructor Goal

Run a rapid-fire mock viva using the questions from this file. Call on students by name. Do not let any student be a passive observer.

### Format

Pick 6-8 questions from the Questions to Discuss section below. For each:

1. Ask the question out loud
2. Give the student 30 seconds to think
3. Student answers (1-2 minutes)
4. Instructor adds or corrects

### Questions to Prioritize for This Block

Prioritize questions 6, 8, 10, 12, and 14 — these are the questions most likely to appear in a real technical interview for a backend/AI engineer role at a startup.

### Instructor Observation

Watch for students who answer with vague language like "it calls the AI" or "it does the classification." Push them to be specific: "Which model? What prompt? What does the response look like? What happens if the API returns an error?"

---

## 115–120 min: Wrap-Up and Final Project Reflection

### Instructor Closing

In 8 sessions, you went from zero to a deployed AI backend system. Let us count what you built:

- Session 1: FastAPI CRUD API for support tickets
- Session 2: SQLModel + SQLite data layer with proper ORM models
- Session 3: JWT authentication with role-based access control
- Session 4: LLM ticket classifier using OpenAI
- Session 5: RAG knowledge base using ChromaDB and embeddings
- Session 6: LangGraph agentic workflow
- Session 7: Pytest coverage, custom evals, and guardrails
- Session 8: Deployed, documented, and interview-ready

This is a real AI backend system. Not a tutorial clone. Not a toy project. You designed the data model, you wrote the auth layer, you integrated the LLM, you built the agent. Today you shipped it and you can explain every line.

### Final Instruction

Add the live Railway URL to your README. Push the final README and requirements.txt to GitHub. Share the live URL with the instructor.

---

# Instructor Notes

## What to Emphasize

1. The README is part of the engineering deliverable — it is not optional documentation. Every professional project has one.
2. `.env.example` is a security best practice. Students who commit their `.env` file to a public GitHub repo will expose their OpenAI API key. Emphasize this strongly.
3. Railway's `$PORT` environment variable must be used in the start command — this is the single most common deployment failure.
4. The architecture diagram is the most useful interview preparation tool in the whole README. Interviewers often ask students to "walk me through the architecture."
5. The demo script is a rehearsed narrative — not improvised. Students should know the exact sequence of API calls and what to say at each step.
6. System design vocabulary (bottleneck, trade-off, scalability, stateless) should be applied to this specific project — not recited as abstract definitions.
7. Students will be tempted to add new features in this session (a frontend, a new LLM feature, Docker). Redirect them firmly: ship and document what exists, improve after.
8. The `pip freeze` output may include system-level packages or packages from other projects if the student is not using a virtual environment. Flag this as a best practice issue but do not block deployment over it.

## Common Student Mistakes

1. **Committing `.env` to GitHub** — Student runs `git add .` and pushes the real `.env` file. Their OpenAI API key is now public. Fix: add `.env` to `.gitignore` before the first commit. If already committed, rotate the key immediately in the OpenAI dashboard.

2. **Railway start command error: `uvicorn: command not found`** — Student's `requirements.txt` is missing `uvicorn`. Fix: confirm `uvicorn[standard]` is in `requirements.txt`. Railway installs from this file, so if uvicorn is missing, the server cannot start.

3. **`ModuleNotFoundError: No module named 'app'`** — Student's start command is `uvicorn main:app` instead of `uvicorn app.main:app`. This happens when the FastAPI app is inside an `app/` package. Fix: check the actual file path and adjust the start command.

4. **ChromaDB persistence path fails on Railway** — `CHROMA_PERSIST_DIRECTORY=./chroma_db` works locally but Railway's ephemeral filesystem resets on each deploy, meaning the ChromaDB data is lost. Fix: for demo purposes, populate the knowledge base on startup using a seeding script. Long-term fix: use a hosted vector store.

5. **SQLite concurrency error on Railway: `OperationalError: database is locked`** — Multiple requests hitting the SQLite database simultaneously can cause this. Fix: use `check_same_thread=False` in the SQLite connect args, or switch to PostgreSQL for the deployed version.

6. **`422 Unprocessable Entity` on POST /tickets after deploy** — Student is sending JSON without the `Content-Type: application/json` header in Swagger, or the request body schema has changed and the frontend/test client is sending the old schema. Fix: use Swagger UI to inspect the exact expected schema.

7. **JWT 401 on deployed app but not locally** — The `SECRET_KEY` in Railway variables is different from the local `.env`. Tokens signed with one key cannot be verified with another. Fix: copy the exact `SECRET_KEY` value to Railway variables.

8. **`requirements.txt` includes `pkg-resources==0.0.0`** — This is a common artifact of `pip freeze` on Ubuntu/Debian systems. It causes `pip install` to fail on Railway. Fix: remove `pkg-resources==0.0.0` from `requirements.txt` manually.

9. **LangGraph import error on Railway: `ImportError: cannot import name 'StateGraph' from 'langgraph'`** — The `langgraph` version in `requirements.txt` is pinned to an old version that has a different API. Fix: ensure the version pinned in `requirements.txt` matches the version that was used locally during Session 6.

10. **README architecture diagram is missing or incorrect** — Claude Code sometimes generates a high-level diagram that omits ChromaDB or LangGraph. Walk students through cross-checking every component in the diagram against the actual codebase.

## How to Control the Session

Use this rule: deployment and demo are the non-negotiable outcomes of this session. README and viva practice are high-priority but can be completed after class. If time runs out, every student must have a live deployed URL and a rehearsed 3-minute demo.

## Setup Rule

Do not spend more than 5 minutes live on any single student's setup issue. The student follows the instructor screen and fixes their specific issue after class.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What did you build in this project?

Expected answer:

I built an AI Support Ticket Resolution Copilot — a FastAPI backend that allows users to create support tickets and uses an LLM pipeline to automatically classify them, retrieve relevant knowledge base context using RAG, and generate resolution suggestions. The system includes JWT authentication with role-based access, a SQLModel/SQLite data layer, a ChromaDB vector store, a LangGraph agentic workflow, and a pytest test suite with custom evals and guardrails.

### Q2. Who is the intended user of this system?

Expected answer:

The system has two types of users: support agents (authenticated users with agent role) who can create and resolve tickets, and admins who can access all tickets across the system. In a real deployment, customers would submit tickets through a frontend or webhook, and the AI pipeline would run automatically on ticket creation.

### Q3. What problem does the RAG component solve?

Expected answer:

Without RAG, the LLM generates suggestions based only on its training data, which does not include our company's specific knowledge base, past resolutions, or product documentation. RAG retrieves the most relevant documents from ChromaDB — which we populated with curated knowledge base articles — and injects them as context into the LLM prompt. This produces suggestions that are grounded in our specific domain rather than generic responses.

### Q4. Why did you use LangGraph instead of a simple LangChain chain?

Expected answer:

A LangChain chain is a fixed linear sequence: step A always calls step B. LangGraph allows conditional routing between nodes based on the current state. In our workflow, the retrieve node behavior can differ based on the ticket category returned by the classify node — for example, routing billing tickets to a billing-specific ChromaDB collection. LangGraph also makes the agent state explicit and inspectable, which is important for debugging and evals.

### Q5. How does JWT authentication work in your system?

Expected answer:

When a user calls POST /auth/token with their username and password, the server verifies the credentials against the database, then creates a JWT token signed with the `SECRET_KEY` using the HS256 algorithm. The token payload contains the user's username and role. For every protected route, the `get_current_user` dependency decodes and validates the token. If the token is expired, tampered with, or missing, FastAPI returns a 401 Unauthorized before the route handler is called.

---

## Technical Deep-Dive Questions

### Q6. Walk me through what happens when POST /tickets/{id}/classify is called.

Expected answer:

The request hits the FastAPI router in `app/routes/tickets.py`. The JWT dependency runs first — it decodes the Authorization header, verifies the token signature with `SECRET_KEY`, and extracts the user identity. The route handler fetches the ticket from SQLite using SQLModel's session and the ticket ID. It constructs a classification prompt using the ticket's subject and description, then calls `openai.chat.completions.create` with the `gpt-4o-mini` model. The system prompt instructs the model to return exactly one of: billing, technical, account, or general. The LLM response is parsed, and the ticket's `category` field is updated in the database. The route returns the updated ticket object with the new category.

### Q7. How does the RAG retrieval work at the code level?

Expected answer:

When GET /tickets/{id}/suggest is called, the LangGraph agent is invoked. In the retrieve node, the ticket's description is embedded using `openai.embeddings.create` with the `text-embedding-3-small` model, which returns a 1536-dimensional float vector. This vector is passed to ChromaDB's `collection.query()` method with `n_results=3`. ChromaDB performs a cosine similarity search and returns the 3 most similar documents from the knowledge base. These documents are concatenated into a context string and stored in the LangGraph state, where the suggest node uses them to build the final LLM prompt.

### Q8. What does your SQLModel data model look like for a ticket?

Expected answer:

The `Ticket` model in `app/models.py` inherits from `SQLModel` with `table=True`. Fields include: `id` (Optional[int], primary key), `subject` (str), `description` (str), `category` (Optional[str], nullable — populated after classification), `status` (str, default "open"), `created_by` (int, foreign key to User.id), `created_at` (datetime, default to `datetime.utcnow`), and `resolved_at` (Optional[datetime], nullable — set when PATCH /tickets/{id}/resolve is called). The `User` model has a one-to-many relationship with `Ticket` via the `created_by` foreign key.

### Q9. How does your guardrail function work?

Expected answer:

The guardrail in `app/guardrails.py` runs before any LLM call in the classify or suggest pipeline. It calls the LLM with a meta-prompt that asks the model to classify whether the input ticket description is a legitimate support request or an adversarial/off-topic input (prompt injection, nonsensical text, attempts to override system instructions). If the guardrail LLM returns a rejection signal, the route handler raises an `HTTPException` with a 400 status code and a message indicating the input was rejected. The design intentionally uses a separate LLM call rather than input regex filtering because LLM-based guardrails can catch semantic attacks that regex cannot.

### Q10. How did you structure your pytest tests?

Expected answer:

Tests live in the `tests/` directory. We use a `conftest.py` that creates a fresh SQLite in-memory database and a `TestClient` from FastAPI's test utilities for each test session. Test fixtures create a test user and return an auth token so that protected routes can be tested without a real login flow. Tests cover: ticket creation returning 201 with correct fields, classification updating the category field, the guardrail rejecting a clearly adversarial input, and the suggest endpoint returning a non-empty suggestion string. We also have a custom eval script in `app/evals/` that runs the classify pipeline against a golden dataset of 10 labeled tickets and reports accuracy.

---

## System Design and Trade-off Questions

### Q11. What is the biggest scalability bottleneck in your current system?

Expected answer:

There are two primary bottlenecks. First, SQLite does not support concurrent writes — under load, multiple simultaneous POST requests will result in `OperationalError: database is locked`. The fix is to migrate to PostgreSQL with an async driver like `asyncpg` and use SQLModel's async session. Second, every call to GET /tickets/{id}/suggest makes a synchronous HTTP request to the OpenAI API, which adds 500ms to 2s of latency per request and blocks the FastAPI event loop if not handled with `asyncio`. The fix is to make LLM calls async using the `openai` library's async client or to cache suggestion results in Redis for tickets that have already been processed.

### Q12. Why is SQLite acceptable for this project but not for production?

Expected answer:

SQLite stores the entire database in a single file on disk. It serializes write operations, meaning only one write can happen at a time. For a demo or single-user development environment, this is perfectly acceptable — it requires no infrastructure, no connection pooling, and no separate database server. In production with multiple concurrent users, the write serialization causes `database is locked` errors and makes horizontal scaling (running multiple API server instances) impossible because each instance would have its own SQLite file. PostgreSQL solves both problems: it handles concurrent connections natively and runs as a separate networked service that multiple server instances can connect to.

### Q13. How would you add caching to the suggestion endpoint?

Expected answer:

I would add Redis as a caching layer. When GET /tickets/{id}/suggest is called, the server first checks Redis with the ticket ID as the key. If a cached suggestion exists and the ticket has not been modified since the cache was written, it returns the cached value immediately without calling the LLM or ChromaDB. If no cache hit, it runs the full LangGraph pipeline, stores the result in Redis with a TTL (e.g., 1 hour), and returns the result. In FastAPI, this can be implemented as a dependency or middleware. The `redis-py` library is used for synchronous calls; `aioredis` for async. The trade-off is cache staleness: if the knowledge base is updated, the cached suggestion may no longer reflect the best answer.

### Q14. How would you explain the difference between a chain and an agent to a non-AI interviewer?

Expected answer:

A chain is a script — it runs the same steps in the same order every time, regardless of what the data says. An agent is a decision-maker — it looks at the current state and decides what to do next. In our system, the LangGraph agent reads the ticket state after each node and can route differently based on the classification result. For example, if the classify node returns "billing", the retrieve node queries the billing ChromaDB collection; if it returns "technical", it queries the technical collection. This conditional behavior is why we chose LangGraph. The practical interview answer is: use a chain when your workflow is always the same; use an agent when the workflow needs to branch based on data.

### Q15. What would you change about this architecture if you had to handle 10,000 tickets per day?

Expected answer:

Several changes would be required at that scale. First, replace SQLite with PostgreSQL and use async SQLAlchemy with a connection pool. Second, move LLM calls off the synchronous request path — instead of calling OpenAI inline, push ticket IDs to a task queue (Celery + Redis or AWS SQS) and process classification and suggestion asynchronously. The API would return immediately with a "processing" status, and a webhook or polling endpoint would deliver the result when ready. Third, replace the local ChromaDB instance with a hosted vector database like Pinecone or Weaviate that supports horizontal scaling and replication. Fourth, add structured logging with correlation IDs so every ticket's processing pipeline can be traced end-to-end.

---

# Session 8 Completion Checklist

Students should complete the following by the end of the session:

- [ ] `requirements.txt` exists at project root and is generated from `pip freeze` with pinned versions
- [ ] `.env.example` exists at project root with all required keys and placeholder values (no real secrets)
- [ ] `.env` is listed in `.gitignore` and is NOT present in the GitHub repository
- [ ] `README.md` exists with: project overview, architecture diagram, API table, setup steps, AI features, limitations, future improvements
- [ ] Architecture diagram in README shows all layers: FastAPI, Auth, SQLModel, LLM Classifier, ChromaDB RAG, LangGraph, Guardrails
- [ ] Backend is deployed to Railway (or Render) and accessible via a public URL
- [ ] Swagger UI is accessible at `<live-url>/docs` and returns the full API schema
- [ ] POST /tickets returns 201 on the live deployed URL
- [ ] GET /tickets/{id}/suggest returns a non-empty AI suggestion on the live deployed URL
- [ ] Student can walk through a complete ticket lifecycle in under 3 minutes without notes
- [ ] Student can explain the RAG pipeline (embed → query ChromaDB → inject context → LLM) verbally
- [ ] Student can answer "What is the biggest limitation of your system?" with a specific technical answer

---

# Instructor Backup Plan

If Railway deployment fails or blocks more than 30 minutes of the session:

1. Switch to Render.com — the process is nearly identical (connect GitHub, set environment variables, set start command, deploy).
2. If both Railway and Render fail due to network or account issues, skip live deployment and focus the remaining time on README walkthrough, demo script rehearsal, and mock viva practice.
3. The live deployment is important for portfolio value but not required for interview success. A well-documented README and a confident system design explanation are more directly useful in an interview than a running URL.
4. Share a reference deployed URL (instructor's own deployment) so students can see what the end state looks like.
5. Students who cannot deploy live must complete deployment as a post-session task within 48 hours and share the URL in the group channel.
6. Do not sacrifice the viva practice block under any circumstances. The mock interview practice in minutes 105-115 is the highest-value activity in this session.
