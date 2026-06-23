# Session 8 Student Pre-Session File: Deployment, Demo, System Design, and Mock Interview

## What We Are Building

Over 8 sessions, we built one complete AI backend system:

## AI Support Ticket Resolution Copilot

A production-style FastAPI backend that accepts customer support tickets, classifies them using an LLM, retrieves relevant resolution context from a vector knowledge base, and generates AI-powered suggestions through a LangGraph agentic workflow.

Here is the complete feature set by session:

- Session 1: FastAPI CRUD API — POST/GET/PATCH for tickets
- Session 2: SQLModel + SQLite data layer with ORM models
- Session 3: JWT authentication and role-based access control
- Session 4: LLM ticket classifier (OpenAI, gpt-4o-mini)
- Session 5: RAG knowledge base using ChromaDB and OpenAI embeddings
- Session 6: LangGraph agentic workflow — classify, retrieve, suggest nodes
- Session 7: pytest test suite, custom evals against a golden dataset, prompt-based guardrails
- Session 8: Deploy to Railway, write README with architecture diagram, demo script, system design rehearsal

## Session 8 Goal

Session 8 has no new feature to build. The goal is to ship, document, and explain the system you already built.

By the end of Session 8, you will have:

- A live public URL where your backend runs (Railway or Render)
- Swagger UI accessible at `<live-url>/docs`
- A professional README with architecture diagram, API table, setup instructions, and limitations
- A clean `requirements.txt` and a `.env.example` file
- A rehearsed 3-minute demo script for the full ticket lifecycle
- Vocabulary and explanation ready for a system design interview

## Session 8 Output

At the end of Session 8:

1. Share your live Railway URL in the group channel
2. Your GitHub repo has: `README.md`, `requirements.txt`, `.env.example`, `.gitignore` (with `.env` excluded)
3. You can do the 3-minute demo from memory on the live deployed URL
4. You can explain every layer of your system without looking at notes

---

# Pre-Read

## Why Are We Adding This at This Point in the Build?

You have built a complete AI backend. But a backend that only runs on your laptop is not a portfolio piece. It is a homework assignment.

Deployment is the act of making your system accessible to anyone in the world. Documentation is the act of communicating what your system does and how to run it. Both are professional engineering responsibilities — not optional extras.

More importantly: in a technical interview, no one runs your code. They ask you to explain it. If you cannot describe the data flow of your own system in two minutes, the working code on your laptop does not help you. This session turns your working system into a demonstrable, explainable product.

There is also a practical reason to do this last. Deployment requires that all features are working and stable. If we deployed in Session 3, every subsequent session would require redeployment. By deploying in the final session, we deploy once with the complete system.

## System Architecture Flow — Complete Backend

This is the full data flow of the system you built across all 8 sessions:

```
HTTP Request (Swagger / curl / Postman / frontend)
        |
        v
FastAPI Application (app/main.py)                      [Session 1]
        |
    JWT Middleware                                      [Session 3]
    (app/auth.py → decode token → extract user role)
        |
        v
Route Handlers                                         [Sessions 1–4]
    app/routes/tickets.py   (CRUD + classify + suggest + resolve)
    app/routes/users.py     (register + login)
        |
        v
SQLModel ORM (app/models.py)                           [Session 2]
    Ticket model, User model, session management
        |
        v
SQLite Database (support.db)                           [Session 2]
        |
        v
Guardrail Check (app/guardrails.py)                    [Session 7]
    LLM meta-prompt filters adversarial/off-topic input
        |
        v
LLM Ticket Classifier (app/classifier.py)              [Session 4]
    OpenAI gpt-4o-mini → category: billing / technical / account / general
        |
        v
LangGraph Agent (app/graph.py)                         [Session 6]
    StateGraph with 3 nodes:
        classify node → retrieve node → suggest node
        |
        v
RAG Retriever (app/knowledge_base.py)                  [Session 5]
    Ticket description → OpenAI text-embedding-3-small → 1536-dim vector
    → ChromaDB cosine similarity search → top-3 relevant documents
        |
        v
LLM Suggestion Generator                               [Session 6]
    Retrieved context + ticket description → gpt-4o-mini → resolution suggestion
        |
        v
HTTP Response (JSON)
        |
        v
Eval Runner (app/evals/)                               [Session 7]
    Offline: golden dataset → classify pipeline → accuracy report
```

## Key Concepts to Revise Before Session 8

### 1. Environment Variables and `python-dotenv`

Your application loads secrets (API keys, database URLs, signing keys) from a `.env` file using `python-dotenv`. The `load_dotenv()` call in `app/config.py` or `app/main.py` reads this file and populates `os.environ`. The `.env.example` file is a template that shows what keys are needed without exposing real values. The rule is: `.env` is never committed to version control; `.env.example` always is.

### 2. `pip freeze` and `requirements.txt`

`pip freeze` lists every installed package in the current Python environment with its exact pinned version. Running `pip freeze > requirements.txt` captures the exact dependency state of your project. When Railway (or any CI/CD system) deploys your project, it runs `pip install -r requirements.txt` to recreate this exact environment. If a package is missing from `requirements.txt`, the deployed app will fail with `ModuleNotFoundError`.

### 3. ASGI and the `$PORT` Environment Variable

FastAPI is an ASGI framework. It is served by `uvicorn`, an ASGI server. When Railway deploys your app, it assigns a random port and passes it as the `$PORT` environment variable. Your start command must use this variable: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. If you hardcode port 8000, Railway's load balancer cannot reach your app and deployment will fail with a port binding error.

### 4. SQLite Limitations and Production Trade-offs

SQLite stores the entire database in a single file. It handles one write at a time (serialized writes). On Railway's ephemeral filesystem, the SQLite file is reset every time the service redeploys. This means your database state (tickets, users) does not persist across deployments. For the demo, you will re-seed the database after each deploy. For production, the fix is PostgreSQL with a persistent managed database service.

### 5. ChromaDB Persistence on Ephemeral Filesystems

ChromaDB persists vector data to a local directory (e.g., `./chroma_db`). On Railway's ephemeral filesystem, this directory is wiped on each redeploy. Your knowledge base setup script (from Session 5) must be re-run after each deployment to repopulate ChromaDB. A production fix is to use a hosted vector store (Pinecone, Weaviate) that persists independently of the compute layer.

### 6. System Design Vocabulary You Must Know

These terms will come up in interviews. Know what they mean in the context of your project specifically:

- **Stateless server**: Your FastAPI server holds no session state in memory. Auth state is in the JWT token. This means you can run multiple server instances without sticky sessions.
- **Bottleneck**: The LLM API call is the slowest part of the suggest pipeline — it adds 500ms to 2s of latency per request.
- **Trade-off**: SQLite is simpler but cannot scale; PostgreSQL scales but requires infrastructure. This is a deliberate trade-off for a demo project.
- **Vector similarity search**: ChromaDB converts the query into a vector and finds documents whose vectors are closest by cosine distance — not keyword match.
- **Agentic workflow**: LangGraph routes between nodes based on state, unlike a linear chain that always runs the same steps.

### 7. Mermaid Diagrams in Markdown

GitHub renders Mermaid diagrams natively in README files. A Mermaid diagram is written inside a fenced code block with the language tag `mermaid`. Example:

```
graph TD
    A[Client] --> B[FastAPI]
    B --> C[JWT Auth]
    C --> D[Route Handler]
```

If Mermaid does not render on your platform, use a text-based diagram with arrows (as shown in the architecture flow above).

### 8. Writing a README for a Technical Audience

A good README for a backend project contains: project description, architecture diagram, prerequisites, installation steps, environment variable reference, how to run the app locally, API reference, known limitations, and future improvements. It does not contain: marketing language, vague descriptions, or missing setup steps. Write it as if you are explaining the project to a senior engineer who has never seen it before.

---

# Prerequisites: Setup Before Session 8

## Your Code State from Session 7

Confirm the following before Session 8:

- `app/main.py` — FastAPI app with all routes registered
- `app/models.py` — `Ticket` and `User` SQLModel models
- `app/auth.py` — JWT creation and `get_current_user` dependency
- `app/routes/tickets.py` — CRUD endpoints, `/classify`, `/suggest`, `/resolve`
- `app/routes/users.py` — `/auth/register` and `/auth/token`
- `app/classifier.py` — LLM classification function
- `app/knowledge_base.py` — ChromaDB setup and knowledge base population
- `app/graph.py` — LangGraph StateGraph with classify, retrieve, suggest nodes
- `app/guardrails.py` — guardrail function using LLM meta-prompt
- `app/evals/` — custom eval script with golden dataset
- `tests/` — at least 3 pytest tests passing
- `.env` — with all required keys

Verify these two endpoints work before Session 8:

```bash
# From your project directory with the server running:
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"subject": "Payment failed", "description": "My payment is failing at checkout"}'
# Expected: 201 with ticket JSON

curl http://localhost:8000/tickets/1/suggest \
  -H "Authorization: Bearer <your-jwt-token>"
# Expected: 200 with suggestion string
```

If either of these fails, fix it before Session 8 starts.

## Python Packages to Confirm

These should already be installed. Confirm with `pip show <package>`:

```
fastapi
uvicorn[standard]
sqlmodel
python-jose[cryptography]
passlib[bcrypt]
python-dotenv
openai
chromadb
langchain
langgraph
langchain-openai
pytest
httpx
```

## Environment Setup

Ensure your virtual environment is active before Session 8:

```bash
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

Ensure your `.env` file has all required keys:

```
OPENAI_API_KEY=sk-...
DATABASE_URL=sqlite:///./support.db
SECRET_KEY=<random string, min 32 chars>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## GitHub Repository

Your project must be in a GitHub repository before Session 8. If it is not:

```bash
git init
git add .
git commit -m "complete AI support ticket resolution copilot"
```

Then create a new repository on github.com and push:

```bash
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

Critical: verify `.env` is in your `.gitignore` before running `git add .`:

```bash
cat .gitignore   # should contain: .env, __pycache__/, *.pyc, support.db, chroma_db/
```

---

# Content to Prepare Before Class

Prepare these items in a text file or document before Session 8 starts:

```text
1. GitHub Repository URL:
   https://github.com/<your-username>/<repo-name>

2. All environment variable keys your project uses (not the values):
   OPENAI_API_KEY
   DATABASE_URL
   SECRET_KEY
   ALGORITHM
   ACCESS_TOKEN_EXPIRE_MINUTES
   CHROMA_PERSIST_DIRECTORY

3. Your project's complete file structure (run `find . -name "*.py" -not -path "*/.*"`):
   app/
     main.py
     models.py
     auth.py
     classifier.py
     knowledge_base.py
     graph.py
     guardrails.py
     routes/
       tickets.py
       users.py
     evals/
       run_evals.py
   tests/
     conftest.py
     test_tickets.py
   requirements.txt
   .env
   .env.example   (to be created in session)
   README.md      (to be created in session)

4. A one-sentence description of your project for the README intro:
   "A FastAPI backend that uses LLM classification, ChromaDB RAG, and a LangGraph
    agentic workflow to automatically classify and resolve customer support tickets."

5. Your Railway or Render account (create one at railway.app before class):
   Email used: ___________________
```

---

# Prompts for Session 8

Use these prompts in Claude Code or Cursor during the session when instructed. All prompts target an AI coding assistant — paste them as-is.

---

## Prompt 1: README Generation Prompt

```text
I have a FastAPI backend project called "AI Support Ticket Resolution Copilot".
The project is located in the current directory with this structure:
  app/main.py                   - FastAPI app entry point, registers all routers
  app/models.py                 - SQLModel models: Ticket, User
  app/auth.py                   - JWT authentication: token creation, get_current_user dependency
  app/classifier.py             - LLM ticket classifier using OpenAI gpt-4o-mini
  app/knowledge_base.py         - ChromaDB collection setup, document ingestion, similarity search
  app/graph.py                  - LangGraph StateGraph: classify node, retrieve node, suggest node
  app/guardrails.py             - Prompt-based guardrail function to reject adversarial inputs
  app/routes/tickets.py         - Ticket CRUD routes + /classify, /suggest, /resolve endpoints
  app/routes/users.py           - /auth/register and /auth/token endpoints
  app/evals/run_evals.py        - Custom eval runner against a golden ticket dataset
  tests/conftest.py             - pytest fixtures: test DB, test client, auth token
  tests/test_tickets.py         - pytest tests for ticket CRUD, classification, guardrails

The API endpoints are:
  POST   /auth/register                - Register a new user (public)
  POST   /auth/token                   - Login and get JWT token (public)
  POST   /tickets                      - Create a ticket (requires JWT)
  GET    /tickets                      - List all tickets for current user (requires JWT)
  GET    /tickets/{ticket_id}          - Get a single ticket (requires JWT)
  POST   /tickets/{ticket_id}/classify - Run LLM classifier on ticket (requires JWT)
  GET    /tickets/{ticket_id}/suggest  - Run LangGraph agent, return AI suggestion (requires JWT)
  PATCH  /tickets/{ticket_id}/resolve  - Mark ticket as resolved (requires JWT)

AI features used:
  - LLM model: gpt-4o-mini (classification and suggestion generation)
  - Embedding model: text-embedding-3-small (1536 dimensions) for RAG retrieval
  - Vector store: ChromaDB (local persistence)
  - Agent framework: LangGraph (StateGraph with classify, retrieve, suggest nodes)
  - Guardrails: prompt-based meta-classifier to reject off-topic or adversarial input

Technology stack:
  FastAPI, SQLModel, SQLite, python-jose (JWT), passlib (bcrypt), OpenAI Python SDK,
  ChromaDB, LangChain, LangGraph, pytest, httpx, python-dotenv, uvicorn

Write a complete, professional README.md for this project. Include:

1. Project title and one-paragraph description
2. Architecture diagram — use Mermaid syntax (graph TD) showing all layers:
   Client → FastAPI → JWT Auth → Route Handler → SQLModel/SQLite → Guardrail →
   LLM Classifier → LangGraph Agent → ChromaDB RAG → OpenAI API
3. API Reference table with columns: Method | Endpoint | Auth Required | Description
4. Setup instructions — these must be exact and runnable:
   a. Clone the repo
   b. Create and activate virtual environment
   c. pip install -r requirements.txt
   d. Copy .env.example to .env and fill in values
   e. uvicorn app.main:app --reload
   f. Open http://localhost:8000/docs
5. Environment Variables section — list every key from .env.example with a one-line description
6. AI Features section — describe each AI feature with the specific model and purpose
7. Limitations section — be technically honest:
   - SQLite not suitable for production concurrent writes
   - ChromaDB data is ephemeral on cloud platforms without persistent storage
   - LLM calls are synchronous and add latency to the request path
   - No async database driver (uses synchronous SQLModel sessions)
8. Future Improvements section — list 5 concrete technical improvements:
   - PostgreSQL with asyncpg
   - Redis caching for suggestion results
   - Hosted vector store (Pinecone or Weaviate)
   - Background task queue for async LLM processing
   - Docker and docker-compose for local development

Do NOT include any frontend code or instructions.
Do NOT add any new Python files.
Output only the README.md content.
```

---

## Prompt 2: Architecture Diagram Prompt

```text
I need a detailed text-based system architecture diagram for my FastAPI backend:
"AI Support Ticket Resolution Copilot"

Generate TWO diagrams:

Diagram 1: Request flow for GET /tickets/{ticket_id}/suggest (the most complex endpoint)
Show every component that is touched when this endpoint is called:
- HTTP request with Authorization header
- JWT decode in get_current_user dependency (app/auth.py)
- Route handler in app/routes/tickets.py
- SQLModel session query to fetch ticket (app/models.py)
- Guardrail check (app/guardrails.py) — LLM meta-call
- LangGraph agent invocation (app/graph.py)
- Inside LangGraph: classify node → retrieve node → suggest node
- In retrieve node: OpenAI embeddings API call → ChromaDB similarity query
- In suggest node: OpenAI chat completion call with retrieved context
- Return suggestion string in JSON response

Use this arrow format:
Component (file: app/xxx.py)
    |
    v
Next component

Diagram 2: Component dependency map
Show which files import which files using arrows:
app/main.py → app/routes/tickets.py, app/routes/users.py
app/routes/tickets.py → app/models.py, app/auth.py, app/classifier.py, app/graph.py, app/guardrails.py
app/graph.py → app/knowledge_base.py
app/knowledge_base.py → chromadb, openai
app/classifier.py → openai
app/auth.py → app/models.py, python-jose, passlib

Format as a clean text block suitable for a GitHub README.
Do NOT generate any Python code.
```

---

## Prompt 3: Deployment Prompt

```text
I need step-by-step instructions to deploy my FastAPI application to Railway (railway.app).

Project details:
- FastAPI app entry point: app/main.py
- App instance: `app` (the FastAPI object in app/main.py)
- Correct uvicorn start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
- The app uses SQLite (support.db) — this file should NOT be committed to git
- The app uses ChromaDB with local persistence in ./chroma_db/
- All configuration is via environment variables loaded from .env using python-dotenv

Required environment variables to set in Railway dashboard:
  OPENAI_API_KEY
  DATABASE_URL=sqlite:///./support.db
  SECRET_KEY
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  CHROMA_PERSIST_DIRECTORY=./chroma_db

Write deployment instructions covering:
1. Confirming .env is in .gitignore (include the command to verify)
2. Pushing the final project to GitHub (include git commands)
3. Signing into Railway and connecting the GitHub repo
4. Setting the start command in Railway (exact command)
5. Adding all environment variables in the Railway Variables tab (one by one)
6. Triggering the deploy and reading the build logs
7. Accessing the live URL and verifying Swagger at <url>/docs
8. Seeding the knowledge base after first deploy (explain why this is needed)
9. Common errors and fixes:
   - ModuleNotFoundError: No module named 'app'
   - Port binding failed
   - pkg-resources==0.0.0 causing pip install failure
   - ChromaDB collection empty after deploy

Also write a fallback section: if Railway does not work, how to deploy to Render.com with the same settings.

Do NOT write Python code.
Do NOT suggest Docker.
Output as a structured Markdown guide.
```

---

## Prompt 4: Demo Script Prompt

```text
I need a timed 3-minute demo script for my deployed "AI Support Ticket Resolution Copilot" backend.

The demo uses Swagger UI at <live-url>/docs.

The demo must cover one complete ticket lifecycle:
  create ticket → classify ticket → retrieve context and suggest resolution → resolve ticket

My live URL is: <replace with your Railway URL>

Write a word-for-word narrated demo script in this format:

[TIME: 0:00 – 0:30] SETUP AND INTRODUCTION
  What to say: (exact narration text)
  What to do on screen: (exact Swagger/browser actions)

[TIME: 0:30 – 1:00] CREATE A TICKET
  What to say:
  What to do on screen:
  Payload to paste: (exact JSON)
  Expected response: (show the JSON fields to point out)

[TIME: 1:00 – 1:30] CLASSIFY THE TICKET
  What to say:
  What to do on screen:
  Expected response:

[TIME: 1:30 – 2:15] GET AI SUGGESTION (most important section)
  What to say: (explain what is happening technically: LangGraph agent, ChromaDB retrieval, LLM call)
  What to do on screen:
  Expected response:

[TIME: 2:15 – 2:45] RESOLVE THE TICKET
  What to say:
  What to do on screen:
  Expected response:

[TIME: 2:45 – 3:00] WRAP-UP
  What to say: (one strong closing sentence mentioning auth, RAG, LangGraph)

Use a realistic ticket: subject "Payment not going through", description "I have been trying to complete my subscription payment for 2 days. The payment fails at the final step with error code 4002."

Do NOT include any frontend code.
Do NOT add any new features.
Output only the demo script.
```

---

## Prompt 5: System Design Explanation Prompt

```text
Help me prepare a 3-minute system design explanation for a technical interview.

I built this system:
- FastAPI backend for AI-powered customer support ticket resolution
- JWT auth with role-based access (agent and admin roles)
- SQLModel with SQLite for ticket and user persistence
- LLM ticket classifier using OpenAI gpt-4o-mini
- RAG pipeline: ticket description → text-embedding-3-small → ChromaDB cosine similarity → top-3 documents → injected as LLM context
- LangGraph StateGraph with 3 nodes: classify node, retrieve node, suggest node
- Prompt-based guardrail that rejects adversarial or off-topic inputs before LLM calls
- pytest test suite with fixtures, test DB, and custom eval runner

Write a structured verbal explanation that covers:
1. What the system does (1-2 sentences, problem and solution)
2. Architecture walkthrough — describe data flow from HTTP request to HTTP response
3. Why each major design decision was made:
   - Why FastAPI over Flask
   - Why LangGraph over a simple LangChain chain
   - Why ChromaDB for vector storage
   - Why SQLite (and what the production alternative would be)
   - Why prompt-based guardrails instead of input regex filtering
4. Trade-offs and limitations (honest technical assessment)
5. What you would change at scale (2-3 specific improvements)

Format as a spoken script, not bullet points.
Use precise technical vocabulary: ASGI, cosine similarity, embedding, StateGraph, JWT claims, foreign key, bcrypt, tokenizer.
Length: approximately 3 minutes when spoken aloud (400-500 words).
```

---

## Prompt 6: Mock Viva Prompt

```text
I am preparing for a technical interview. I built this FastAPI backend:
"AI Support Ticket Resolution Copilot"

Stack: FastAPI, SQLModel, SQLite, JWT (python-jose), passlib (bcrypt), OpenAI (gpt-4o-mini, text-embedding-3-small), ChromaDB, LangGraph, LangChain, pytest, httpx, python-dotenv, uvicorn, Railway deployment.

Generate 15 technical viva questions with detailed model answers.

Questions must cover:
- Q1–Q4: Basic project understanding (what it does, who uses it, why each component)
- Q5–Q8: Code-level implementation details (specific to FastAPI, SQLModel, JWT, OpenAI SDK)
- Q9–Q11: AI/ML concepts applied to this project (RAG, embeddings, LangGraph nodes)
- Q12–Q13: System design and trade-offs (scalability, bottlenecks, production readiness)
- Q14–Q15: Debugging and error handling (specific FastAPI/Python errors)

For each question:
  Question: (the question text)
  Model Answer: (3-5 sentences, technically precise, uses correct terminology)

Include questions about:
- What happens when the JWT token is expired (which exception, which HTTP status)
- Why bcrypt is used instead of MD5 or SHA-256 for password hashing
- What the 1536 in text-embedding-3-small represents
- What `check_same_thread=False` does in SQLite connection args
- How LangGraph state is passed between nodes
- What a 422 Unprocessable Entity means in FastAPI

Do NOT generate any code.
Output only the questions and answers.
```

---

## Prompt 7: Code Review and Polish Prompt

```text
Review the full codebase of my FastAPI project "AI Support Ticket Resolution Copilot".

File structure:
  app/main.py, app/models.py, app/auth.py, app/classifier.py,
  app/knowledge_base.py, app/graph.py, app/guardrails.py,
  app/routes/tickets.py, app/routes/users.py,
  app/evals/run_evals.py, tests/conftest.py, tests/test_tickets.py

Check for the following issues and list findings with file name and line reference:

1. Hardcoded secrets or API keys (any string that looks like a key not loaded from os.environ)
2. Missing error handling:
   - OpenAI API calls with no try/except around openai.APIError or openai.RateLimitError
   - ChromaDB queries with no fallback for empty results
   - SQLModel queries that assume a record exists without checking for None
3. Security issues:
   - Password stored in plaintext
   - JWT secret loaded as a hardcoded string
   - SQL injection via string formatting (less likely with SQLModel but check raw SQL)
4. Missing HTTP status codes (routes returning 200 for creation instead of 201)
5. Inconsistent response schemas (routes returning raw SQLModel objects instead of Pydantic response models)
6. Any import that will cause a circular import error
7. Any route that is missing the JWT dependency but should have it based on the route's purpose

For each finding, write:
  File: (filename)
  Issue: (description)
  Fix: (one-sentence fix)

Do NOT rewrite the entire codebase.
Do NOT add new features.
Only identify and fix the specific issues listed above.
After listing findings, apply only the fixes that involve missing try/except blocks and missing None checks.
```

---

# What You Should Be Able to Explain After Session 8

By the end of Session 8, you should be able to answer all of the following without notes:

1. What does this system do, and what problem does it solve for a support team?
2. Walk me through the data flow when GET /tickets/{id}/suggest is called — every component that runs, in order.
3. What is the role of ChromaDB in this system, and how does cosine similarity search work at a high level?
4. Why does the LangGraph agent produce better results than a single LLM call with the ticket description?
5. What is stored in the JWT token payload, and how does the server verify it on each request?
6. Why is SQLite used in this project, and what would you replace it with in a production system with 100 concurrent users?
7. What does the guardrail do, and why is a prompt-based approach more robust than regex filtering for adversarial inputs?
8. What happens when you call `collection.query()` in ChromaDB — what does it return, and how is it used in the suggest node?
9. What is the biggest latency bottleneck in your system, and how would you reduce it?
10. If a colleague forked your GitHub repo and wanted to run it locally, what would they need to do — step by step?

---

## Final Session 8 Explanation

Prepare this explanation. You should be able to say this from memory in a technical interview:

```text
I built an AI Support Ticket Resolution Copilot using FastAPI as the backend framework
with SQLModel for the data layer and JWT for authentication. The system takes customer
support tickets and runs them through a LangGraph agentic workflow: a classify node
calls gpt-4o-mini to label the ticket category, a retrieve node embeds the ticket
description using text-embedding-3-small and queries ChromaDB for the most relevant
knowledge base documents, and a suggest node passes the retrieved context to gpt-4o-mini
to generate a resolution suggestion. A prompt-based guardrail filters adversarial inputs
before any LLM call. The system is deployed on Railway with pytest test coverage and a
custom eval runner that measures classification accuracy against a golden dataset.
The main production limitation is SQLite — it cannot handle concurrent writes and would
need to be replaced with PostgreSQL for a real support team deployment.
```
