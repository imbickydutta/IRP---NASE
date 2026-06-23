# Session 8 After-Session Notes: Deployment, Demo, System Design, and Mock Interview

## What We Built Today

In Session 8, we shipped the complete AI Support Ticket Resolution Copilot as a deployable, documented, portfolio-ready system.

Specific deliverables completed:

- `requirements.txt` — generated from `pip freeze`, pinned versions for reproducible installs
- `.env.example` — template file with all required environment variable keys and placeholder values; committed to version control so collaborators know what keys to populate
- `README.md` — full engineering README with project overview, Mermaid architecture diagram, API reference table, local setup instructions, environment variable documentation, AI features section, limitations, and future improvements
- Deployed backend on Railway — live public URL, Swagger UI accessible at `/docs`
- 3-minute demo script — one complete ticket lifecycle on the live deployed URL
- System design explanation — verbal walkthrough of the full architecture practiced in mock viva format

No new Python code was written. The work of Session 8 was documentation, deployment, and communication — which are engineering deliverables equal in importance to writing code.

---

# Why This Feature Matters for Production Systems

Every backend system that gets deployed to a real environment requires the same four things: working code, reproducible environment setup, a deployment target, and documentation that lets another engineer (or your future self) understand and run it. Without these, the working code has no operational value.

Deployment matters because a locally-running project has a zero-person audience. Once deployed to Railway, your system has a public URL that anyone in the world can hit. That URL can be in your portfolio, your resume, shared in an interview, and tested live by a recruiter or hiring manager. The difference between "I built this locally" and "here is the live URL" is the difference between a claim and evidence.

Documentation matters because you will not remember how this system works in six months. More importantly, the README is what a technical interviewer reads before they talk to you. If your README clearly describes the architecture, the API, and the limitations, the interviewer starts the conversation already believing you built something real. The architecture diagram alone communicates more about your engineering competence than a verbal explanation of equal length.

Environment variable management matters for security. A committed `.env` file with a real Gemini API key exposed on GitHub can be scraped by bots in under 60 seconds. The `.env.example` pattern is a standard professional practice — the template is version-controlled, the secrets never are.

---

# System Architecture Flow — Complete Flow from Session 1 Through Session 8

This is the complete data flow of the system, with each component annotated by the session in which it was added:

```
HTTP Request (Swagger / curl / Postman)
        |
        v
FastAPI Application Entry Point                        [Added: Session 1]
  app/main.py
  - registers ticket and user routers
  - calls SQLModel.metadata.create_all() on startup
  - mounts CORS middleware
        |
    JWT Middleware                                      [Added: Session 3]
    app/auth.py
    - decodes Authorization: Bearer <token> header
    - verifies HS256 signature using SECRET_KEY
    - extracts username and role from token payload
    - raises HTTP 401 if token missing, expired, or invalid
        |
        v
Route Handlers                                         [Added: Session 1 + Session 3]
  app/routes/tickets.py      — ticket CRUD + classify + suggest + resolve
  app/routes/users.py        — register + login (token issuance)
        |
        v
SQLModel ORM Session                                   [Added: Session 2]
  app/models.py
  - Ticket model: id, subject, description, category, status, created_by, created_at, resolved_at
  - User model: id, username, hashed_password, role
  - Session from SQLModel engine (sqlite:///./support.db)
        |
        v
SQLite Database (support.db)                           [Added: Session 2]
        |
        v
Guardrail Check                                        [Added: Session 7]
  app/guardrails.py
  - LLM meta-prompt: "Is this a legitimate support ticket? Yes or No."
  - Raises HTTP 400 if input is adversarial, off-topic, or contains prompt injection
        |
        v
LLM Ticket Classifier                                  [Added: Session 4]
  app/classifier.py
  - System prompt: classify into billing / technical / account / general
  - Model: gemini-1.5-flash
  - Returns: category string
  - Updates ticket.category in database
        |
        v
LangGraph StateGraph Agent                             [Added: Session 6]
  app/graph.py
  - StateGraph with TypedDict state: {ticket_id, description, category, context, suggestion}
  - Node 1: classify_node — calls classifier.py, writes category to state
  - Node 2: retrieve_node — calls knowledge_base.py, writes context to state
  - Node 3: suggest_node — calls Gemini with ticket + context, writes suggestion to state
  - Edges: classify_node → retrieve_node → suggest_node → END
        |
        v
RAG Retriever                                          [Added: Session 5]
  app/knowledge_base.py
  - sentence-transformers all-MiniLM-L6-v2: ticket description → 384-dim float vector
  - ChromaDB collection.query(): cosine similarity search → top-3 documents
  - Returns: list of document strings (knowledge base articles / past resolutions)
        |
        v
LLM Suggestion Generator                               [Added: Session 6]
  Inside suggest_node in app/graph.py
  - Prompt: system prompt (support agent role) + ticket description + retrieved context
  - Model: gemini-1.5-flash
  - Returns: resolution suggestion string
        |
        v
HTTP Response (JSON)
  - GET /tickets/{id}/suggest returns: {"suggestion": "<text>"}
        |
        v
Eval Runner (offline — not in request path)            [Added: Session 7]
  app/evals/run_evals.py
  - Loads golden_dataset.json (10 labeled ticket examples)
  - Runs classifier on each example
  - Computes accuracy: correct_labels / total_examples
  - Prints classification report
        |
        v
Deployed on Railway                                    [Added: Session 8]
  - GitHub repo → Railway build (pip install -r requirements.txt)
  - Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
  - Environment variables set in Railway Variables tab
  - Public URL: https://<app-name>.up.railway.app
  - Swagger UI: https://<app-name>.up.railway.app/docs
```

---

# Technical Deep-Dive: Deployment, Documentation, and System Design Communication

## Deployment Architecture for a FastAPI Application

Railway and Render are Platform-as-a-Service (PaaS) providers that abstract away server provisioning. When you push a Git commit, the platform pulls the code, runs `pip install -r requirements.txt` to install dependencies, and executes your configured start command. The key configuration detail for FastAPI on Railway is the `$PORT` environment variable: the platform assigns a random port to your container and exposes it externally; your uvicorn process must bind to this port via `--port $PORT`. If you hardcode port 8000, the platform's health check cannot reach your app and marks the deployment as failed.

FastAPI is an ASGI (Asynchronous Server Gateway Interface) application. Unlike WSGI applications (Flask, Django in default mode), ASGI servers handle each request in a non-blocking coroutine, which means a single uvicorn worker can handle many concurrent requests. However, this benefit is nullified if your route handlers make synchronous blocking calls — like synchronous SQLModel sessions or synchronous Gemini API calls — because these block the event loop and prevent other corequests from running. In our current system, all database and LLM calls are synchronous. This is acceptable for low traffic but becomes a bottleneck at scale. The production fix is to use SQLAlchemy's async session with `asyncpg` and the `google-generativeai` library's async client.

The SQLite ephemeral filesystem problem on Railway is a common source of confusion for students deploying for the first time. Railway's compute containers do not have persistent storage by default — every redeploy starts with a fresh filesystem. This means any SQLite `.db` file written during runtime is lost on the next deploy, and the ChromaDB `./chroma_db/` directory is also wiped. For the demo, this is acceptable: we re-create the database tables on startup (via `SQLModel.metadata.create_all(engine)`) and re-run the knowledge base seeding script. For production, persistent storage requires either Railway's volume service or migrating to external managed services — PostgreSQL (e.g., Railway's own PostgreSQL plugin or Supabase) and a hosted vector store (Pinecone, Weaviate, or Qdrant).

## What a README Communicates to a Technical Audience

A README serves two audiences simultaneously: a new engineer who needs to run the project, and a technical interviewer or reviewer who wants to evaluate what was built and how well the builder understands it. For the first audience, the critical sections are prerequisites, environment setup, and exact run commands. For the second audience, the architecture diagram and limitations sections are most revealing. A limitations section that honestly names SQLite concurrency issues, synchronous LLM call latency, and ChromaDB's ephemeral behavior signals that the engineer understands not just what they built but where it would break. An absent limitations section signals the opposite.

The architecture diagram is the single most information-dense element in a technical README. A well-drawn diagram that shows all six layers — HTTP, auth, route handler, ORM, LLM, and vector store — communicates the system's design in under 30 seconds. Interviewers will often start with "walk me through your architecture" and use the diagram as a shared reference. Students who draw the diagram themselves (rather than asking AI to generate it without understanding it) will be able to answer follow-up questions about any layer.

---

# What Students Should Understand

1. `pip freeze > requirements.txt` captures the exact installed package versions in the current Python environment. Deploying without a `requirements.txt` or with a partial one causes `ModuleNotFoundError` failures on the deployment platform.

2. `.env.example` is a security and onboarding pattern. The real `.env` is in `.gitignore` and never committed. The `.env.example` shows what keys are needed without exposing values. Any public GitHub repository without this pattern risks key exposure.

3. Railway's `$PORT` environment variable must be used in the uvicorn start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. This is the most common Railway deployment failure for FastAPI students.

4. The JWT `SECRET_KEY` in Railway's Variables tab must match the `SECRET_KEY` used to generate tokens. Tokens signed with one key cannot be verified with a different key — this causes 401 errors on the deployed app even when the same credentials work locally.

5. The complete GET /tickets/{id}/suggest pipeline touches: JWT middleware → SQLModel query → guardrail LLM call → LangGraph invocation → classify node (LLM) → retrieve node (sentence-transformers local embedding + ChromaDB query) → suggest node (LLM). This is 2 Gemini API calls and 1 local embedding per request — explaining this clearly in an interview shows deep understanding of the system.

6. LangGraph's `StateGraph` passes a typed state dictionary between nodes. Each node receives the current state, performs its computation, and returns a dict of updates to merge into the state. The node sequence is defined by `add_edge()` calls. This is fundamentally different from a simple function call chain because state is explicit and inspectable at each step.

7. ChromaDB's `collection.query(query_embeddings=[[...]], n_results=3)` returns the top-k most similar documents by cosine distance. The embedding vector is a 384-dimensional float array produced by sentence-transformers `all-MiniLM-L6-v2` (local, no API key). Cosine similarity measures the angle between vectors — documents with semantically similar meaning have vectors that point in similar directions.

8. The `check_same_thread=False` argument in SQLite connection args is required when using SQLite from multiple threads (which FastAPI does via its default threadpool executor for synchronous route handlers). Without this, SQLite raises `ProgrammingError: SQLite objects created in a thread can only be used in that same thread`.

9. Railway and Render both support push-to-deploy from a connected GitHub repository. Every `git push` to the configured branch triggers a new build and deployment. The build log shows `pip install` output — reading this log is the first diagnostic step when deployment fails.

10. The 3-minute demo structure (introduce → create → classify → suggest → resolve) maps directly to the ticket lifecycle that the system was designed to automate. Being able to narrate this demo fluently, with technical commentary at each step, is a complete portfolio demonstration.

---

# Interview-Ready Explanation

```text
I built an AI Support Ticket Resolution Copilot — a FastAPI backend that automates
the classification and resolution suggestion pipeline for customer support tickets.
The system uses a LangGraph StateGraph with three nodes: a classify node that calls
gemini-1.5-flash to label the ticket category, a retrieve node that embeds the ticket
description using all-MiniLM-L6-v2 (sentence-transformers) and queries ChromaDB for relevant knowledge
base documents, and a suggest node that calls gemini-1.5-flash with the retrieved context
to generate a resolution suggestion. Auth is handled by JWT with role-based access,
and the data layer uses SQLModel over SQLite. A prompt-based guardrail runs before
any LLM call to filter adversarial inputs. The system is deployed on Railway, has
pytest coverage with a custom eval runner, and the main production limitation is
SQLite — which would need to be replaced with PostgreSQL at any meaningful scale.
```

---

# What Happens When GET /tickets/{id}/suggest Is Called

```text
1. The HTTP request arrives at FastAPI with an Authorization: Bearer <token> header.

2. The get_current_user dependency (app/auth.py) decodes the JWT using python-jose:
     jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
   If the token is expired, tampered with, or missing, a JWTError is raised and
   FastAPI returns HTTP 401 before the route handler runs.

3. The route handler in app/routes/tickets.py uses a SQLModel session to fetch the ticket:
     ticket = session.get(Ticket, ticket_id)
   If ticket is None, HTTP 404 is returned.

4. The guardrail function in app/guardrails.py calls gemini-1.5-flash with a meta-prompt:
   "Is this input a legitimate customer support ticket? Respond Yes or No."
   If the model returns No, HTTP 400 is returned with a rejection message.

5. The LangGraph agent in app/graph.py is invoked with initial state:
     {"ticket_id": id, "description": ticket.description, "category": None, "context": [], "suggestion": ""}

6. The classify_node calls the classifier function (app/classifier.py):
   - Builds a prompt: "Classify this ticket into: billing, technical, account, general."
   - Calls the Gemini API with model="gemini-1.5-flash"
   - Returns the category string, which is written to state["category"]

7. The retrieve_node calls ChromaDB retrieval (app/knowledge_base.py):
   - Uses SentenceTransformer("all-MiniLM-L6-v2").encode(description) (local, no API key)
   - Gets a 384-dimensional float vector
   - Calls collection.query(query_embeddings=[vector], n_results=3)
   - Returns list of 3 document strings, written to state["context"]

8. The suggest_node builds a prompt:
   - System: "You are a support agent. Use the following context to suggest a resolution."
   - Context: the 3 retrieved documents concatenated
   - User: the ticket description
   - Calls the Gemini API with model="gemini-1.5-flash"
   - Returns the suggestion string, written to state["suggestion"]

9. The LangGraph graph reaches END. The route handler reads state["suggestion"].

10. The route returns HTTP 200 with JSON: {"suggestion": "<suggestion text>"}

Total Gemini API calls per request: 2 (guardrail + classify + suggest combined; guardrail uses gemini-1.5-flash, suggest node uses gemini-1.5-flash, classify node uses gemini-1.5-flash = 3 total)
Total local embedding calls per request: 1 (retrieve node — sentence-transformers, no API key)
Total database queries per request: 1 (SQLModel session.get)
```

---

# What AI Was Used For + What Engineers Must Still Do

## What AI (Antigravity) Was Used For in This Session

- Generating the initial README.md structure and content from a detailed prompt
- Generating the Mermaid architecture diagram based on the described component list
- Writing the `.env.example` template from the environment variable list
- Generating the deployment guide for Railway with step-by-step instructions
- Generating the demo script narrative with timed sections
- Generating mock viva questions and model answers for interview preparation
- Reviewing the codebase for missing error handling and hardcoded values

## What Engineers Must Still Do

- Cross-check the generated README API table against the actual routes in `app/routes/tickets.py` — Antigravity will sometimes invent endpoints that do not exist or omit real ones
- Verify that the architecture diagram includes every actual component (ChromaDB, LangGraph, guardrails) and does not add components that were not built
- Manually create and verify `.env.example` by checking every `os.getenv()` call in the codebase — an AI assistant cannot know your actual env var names unless the code is read
- Test every step in the deployment guide on a real Railway account — generated deployment instructions occasionally reference UI elements that have changed or use incorrect config syntax
- Rehearse the demo script on the live deployed URL — the script must be tested against the real system, not just read
- Apply judgment on which code review findings from the polish prompt are genuine issues versus false positives — not every flagged pattern is actually a bug
- Explain every part of the system during the mock viva — AI-generated model answers are a starting point, not a substitute for genuine understanding

---

# Common Issues and Fixes

## Issue 1: Railway deploy fails with `ModuleNotFoundError: No module named 'app'`

This means the start command is wrong. Railway is running `uvicorn main:app` (treating `main.py` as a top-level module) instead of `uvicorn app.main:app` (treating `main.py` inside the `app/` package). This happens because Railway auto-detects Python projects and guesses the start command.

Fix: In the Railway project settings, manually override the start command to:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

What to ask AI:

```text
My FastAPI app is deployed on Railway. It fails with:
ModuleNotFoundError: No module named 'app'

My file structure is:
  app/main.py   (FastAPI app is defined here as: app = FastAPI())
  requirements.txt

My current start command on Railway is: uvicorn main:app --port $PORT

What should the correct start command be?
Also check if there is a missing __init__.py in the app/ directory that would
cause this import error.
```

---

## Issue 2: Deployed app returns 401 on all protected routes, but local app works

The JWT `SECRET_KEY` in Railway's Variables tab does not match the `SECRET_KEY` in the local `.env` file. Tokens issued by the local server are signed with the local key; the deployed server uses a different key and cannot verify them. This also happens if the student generated a new token on the deployed server but the `SECRET_KEY` variable was set incorrectly.

Fix: Copy the exact `SECRET_KEY` value from the local `.env` file to the Railway Variables tab. Then generate a fresh token using POST /auth/token on the deployed URL before testing protected endpoints.

What to ask AI:

```text
My FastAPI app deployed on Railway returns HTTP 401 Unauthorized for all
protected routes. The same endpoints work fine locally.

I use JWT authentication with python-jose:
  jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

What are all the reasons a JWT token could fail verification on the deployed
server but work on the local server? What should I check in Railway's Variables
tab?
```

---

## Issue 3: GET /tickets/{id}/suggest returns 500 on Railway but 200 locally

The most common cause is that ChromaDB has no data on Railway — the knowledge base was not seeded after deployment because the `./chroma_db/` directory is reset on each deploy. The ChromaDB `collection.query()` call returns an empty result, and the suggest node has no context to pass to the LLM — but if the code does not handle an empty `documents` list, a `KeyError` or `IndexError` causes an unhandled exception and FastAPI returns 500.

Fix step 1: Run the knowledge base seeding script after each Railway deployment:
```bash
# Trigger the seeding via an endpoint or by running the script locally against the deployed DB
```

Fix step 2: Add a fallback in the retrieve node for empty ChromaDB results:
```python
results = collection.query(query_embeddings=[embedding], n_results=3)
documents = results.get("documents", [[]])[0]
if not documents:
    context = ["No relevant knowledge base articles found."]
else:
    context = documents
```

What to ask AI:

```text
My FastAPI endpoint GET /tickets/{id}/suggest returns HTTP 500 on Railway.
It works locally.

The endpoint triggers a LangGraph agent. The retrieve_node calls:
  results = collection.query(query_embeddings=[embedding], n_results=3)
  context = results["documents"][0]

I think the ChromaDB collection is empty on Railway because the ephemeral
filesystem is reset on each deploy.

1. How do I add a safe fallback when ChromaDB returns no results?
2. How should I structure the knowledge base seeding so it runs on app startup
   if the collection is empty?
Show only the changes to the retrieve_node function and app startup code.
Do not rewrite the entire graph.py or main.py.
```

---

# Key Takeaways

1. **Deployment is not the last step — it is the first step of the system's real life.** A backend that runs only on localhost has no portfolio value and cannot be demonstrated in an interview. The 15 minutes spent on Railway deployment converts weeks of local development into a shareable, testable artifact. Every engineer should be able to deploy their own backend. This is a baseline professional skill, not an advanced topic.

2. **Documentation is an engineering deliverable, not optional commentary.** The README, `.env.example`, and architecture diagram are as much a part of the project as the Python files. A well-written README with an accurate architecture diagram communicates engineering competence immediately. A missing README communicates that the engineer considers documentation someone else's problem — which is a red flag in any team environment.

3. **Understanding trade-offs is what separates junior from senior engineers.** Every design decision in this system has a trade-off: SQLite is simpler but cannot scale; synchronous LLM calls are easier to write but block the event loop; ChromaDB is fast to set up but ephemeral on PaaS platforms. Being able to name these trade-offs precisely — with the specific failure mode and the specific production fix — is the answer that senior engineers give. Students who memorize "SQLite is bad for production" without knowing why it breaks (serialized writes, `database is locked` error, no network access for multiple instances) will fail follow-up questions.

4. **System design vocabulary must be applied to your own system, not recited abstractly.** Saying "scalability means handling more users" is a junior answer. Saying "my current bottleneck for scalability is that SQLite serializes writes, so under concurrent load POST /tickets will return `OperationalError: database is locked`. I would replace SQLite with PostgreSQL and use an async connection pool via asyncpg to handle 100 concurrent writes" is a senior answer. Every vocabulary term — stateless, bottleneck, trade-off, embedding, cosine similarity — should be explained using examples from the system you built.

---

# Final Project Summary and Demo Checklist

## Final Project Summary

You built and deployed an AI Support Ticket Resolution Copilot — a complete FastAPI backend system that demonstrates:

- **Backend Engineering**: FastAPI routes, SQLModel ORM, SQLite persistence, Pydantic schemas, HTTP status codes
- **Authentication and Authorization**: JWT with HS256 signing, role-based access control, bcrypt password hashing
- **LLM Integration**: Gemini API (gemini-1.5-flash for chat completions), sentence-transformers (all-MiniLM-L6-v2 for embeddings), prompt engineering, structured output parsing
- **RAG Pipeline**: ChromaDB vector store, cosine similarity retrieval, context injection into LLM prompts
- **Agent Architecture**: LangGraph StateGraph, multi-node conditional workflows, explicit state management
- **Testing and Evaluation**: pytest with fixtures and test DB isolation, custom eval runner, prompt-based guardrails
- **Deployment and Documentation**: Railway deployment, requirements management, environment variable security, README with architecture diagram

This is a real AI backend system built from scratch across 8 sessions. It is not a tutorial clone. You designed the data model, implemented the auth layer, integrated the LLM pipeline, built the agent, wrote the tests, and deployed the system.

## Final Demo Checklist

Before the final demo, confirm all items:

- [ ] Railway URL is accessible (not returning 502 or 503)
- [ ] Swagger UI loads at `<railway-url>/docs`
- [ ] POST /auth/register creates a user (201 response)
- [ ] POST /auth/token returns a JWT token (200 response with `access_token` field)
- [ ] Swagger Authorize button is used with the JWT token
- [ ] POST /tickets creates a ticket with subject and description (201 response)
- [ ] POST /tickets/{id}/classify returns a category field ("billing", "technical", "account", or "general") (200 response)
- [ ] GET /tickets/{id}/suggest returns a non-empty `suggestion` string (200 response)
- [ ] PATCH /tickets/{id}/resolve changes ticket status to "resolved" (200 response)
- [ ] README on GitHub has: architecture diagram, API table, setup instructions, limitations section
- [ ] `.env` is NOT visible in the GitHub repository
- [ ] Student can explain the suggest endpoint pipeline from memory in under 2 minutes
