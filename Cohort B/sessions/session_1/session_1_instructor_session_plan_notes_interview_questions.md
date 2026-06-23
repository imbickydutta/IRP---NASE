# Session 1 Instructor File: Build Core Backend — Ticket CRUD API

## Session Title

Build Core Backend — Ticket CRUD API

## Duration

2 hours

## Project

AI Support Ticket Resolution Copilot

## Session 1 Objective

By the end of Session 1, students should have a fully functional FastAPI backend that exposes 5 REST endpoints for support ticket management. The API must handle request validation via Pydantic, return correct HTTP status codes, store data in-memory, and auto-generate interactive Swagger documentation at `/docs`.

This backend becomes the foundation for every subsequent session:

- Session 2 will replace in-memory storage with SQLModel + SQLite/PostgreSQL
- Session 3 will add JWT authentication middleware
- Session 4 will add OpenAI-powered auto-categorization
- Session 5 will add embeddings + ChromaDB for semantic search
- Session 6 will add LangChain RAG for solution retrieval
- Session 7 will add a LangGraph agent for autonomous ticket resolution
- Session 8 will add deployment, monitoring, and final polish

## Session 1 Deliverable

Students will build a FastAPI application with the following structure:

```
ai-support-copilot/
├── main.py
├── models.py
└── routes/
    └── tickets.py
```

The application must expose these 5 endpoints:

1. `POST /tickets` — create a new ticket, returns 201
2. `GET /tickets` — list all tickets, returns 200
3. `GET /tickets/{id}` — get a single ticket by ID, returns 200 or 404
4. `PATCH /tickets/{id}` — update ticket status, returns 200 or 404
5. `DELETE /tickets/{id}` — delete a ticket, returns 204 or 404

Ticket model fields: `id` (UUID or int), `title` (str), `description` (str), `category` (str), `priority` (str), `status` (str), `created_at` (datetime).

Pydantic models: `TicketCreate` (input validation) and `TicketResponse` (output shape).

All endpoints must be testable through Swagger at `http://localhost:8000/docs`.

## Strict Scope Control

### Include

- FastAPI application with APIRouter for tickets
- Pydantic `BaseModel` for `TicketCreate` and `TicketResponse`
- In-memory list (`tickets_db: list[dict]`) as temporary storage
- `uuid` module for generating ticket IDs
- `datetime` module for `created_at` timestamps
- Proper HTTP status codes: 201 (created), 200 (ok), 404 (not found), 422 (validation error — automatic from Pydantic), 204 (no content)
- HTTPException for 404 responses
- FastAPI `status` module for status code constants
- Auto-generated Swagger at `/docs` and ReDoc at `/redoc`
- Clean separation: `main.py` mounts the router, `models.py` defines Pydantic schemas, `routes/tickets.py` contains endpoint logic
- `Optional` fields in `TicketUpdate` for partial PATCH support

### Do Not Include

- Any database (SQLite, PostgreSQL, SQLModel) — that is Session 2
- Any authentication or JWT tokens — that is Session 3
- Any OpenAI or LLM calls — that is Session 4
- Any ChromaDB or vector embeddings — that is Session 5
- Background tasks (`BackgroundTasks`) — out of scope for Session 1
- WebSockets — out of scope
- Custom exception middleware or exception handlers — keep error handling simple with HTTPException
- Dependency injection patterns beyond basic usage — keep it simple
- Alembic migrations — no database yet
- Docker or deployment configuration — that is Session 8
- Refresh tokens, OAuth2, or any auth scaffold — that is Session 3
- Multiple routers beyond `tickets.py` — keep the structure simple

Session 1 is only about building the REST API foundation cleanly.

---

# Instructor Framing

## Opening Message

Over the next 8 sessions, we are building one production-grade AI Support Ticket Resolution Copilot. Every session adds one new layer to the same codebase. We do not throw away code — we extend it.

Today we build the backend foundation: a FastAPI application that handles support tickets. This API is the single source of truth that the frontend, authentication layer, and AI features will all talk to. If this API is not clean, every future session becomes harder.

This session covers no AI. That is intentional. Production AI systems are built on top of solid backend infrastructure. We build the plumbing before we add the intelligence.

## Key Philosophy

Students at this stage know Python. They know FastAPI exists. What they often lack is the discipline to build a clean, well-structured API before adding features. The AI coding tools (Claude Code, Cursor) are powerful but will happily generate bloated, scope-creeping code if not given tight constraints.

The job of the instructor in Session 1 is:

- enforce scope discipline — keep it to 5 endpoints and in-memory storage
- make students read and explain generated code before moving on
- connect every line of code to an interview question they will face
- ensure Swagger works end-to-end before the session ends

## Repeated Instructor Line

AI can generate the route handler, but you need to know why it returns 201 and not 200, and what Pydantic does before your function even runs.

---

# Session Flow

## 0–10 min: Opening and Project Architecture Overview

### Instructor Goal

Establish the full project vision and explain where Session 1 fits in the 8-session arc. Students should know exactly what they are building today and why.

### Explain the Full Project Vision

The final application will include:

- REST API for ticket CRUD
- PostgreSQL database with SQLModel
- JWT authentication
- OpenAI-powered auto-categorization
- Semantic search with ChromaDB embeddings
- LangChain RAG for solution lookup
- LangGraph agent for autonomous resolution
- Deployed to a cloud platform

### Session 1 Deliverable

By the end of today, your API should accept a support ticket via POST, store it, let you retrieve it, update its status, and delete it. Swagger should document all five endpoints interactively.

### Ask the Room

What is the difference between `POST` and `PUT`? What does 422 mean? What does Pydantic do before your route handler runs?

These are not warm-up questions — they are interview questions. We will answer all of them by the end of the session.

---

## 10–20 min: Architecture Breakdown — Whiteboard/Diagram

### Instructor Goal

Before any code is written, draw the architecture on a whiteboard or shared screen. Students should understand each layer of today's build before they prompt the AI.

### Draw the API Request Flow

```
HTTP Client (Swagger / curl / frontend)
        |
        v
FastAPI Application (main.py)
        |
        v
APIRouter — /tickets (routes/tickets.py)
        |
        v
Pydantic Validation (models.py)
     422 if invalid  |  pass-through if valid
                     v
            Route Handler Function
                     |
                     v
          In-Memory List (tickets_db)
                     |
                     v
        TicketResponse (Pydantic serialization)
                     |
                     v
             JSON HTTP Response
```

### Explain Each Layer

1. FastAPI receives the raw HTTP request.
2. Pydantic validates the request body against `TicketCreate` before your function runs — if validation fails, FastAPI returns 422 automatically without calling your function.
3. The route handler performs the business logic (create, fetch, update, delete).
4. Data is stored in a module-level list for now — `tickets_db`.
5. The response is serialized using `TicketResponse` and returned as JSON.

### Ask Students

Where would a database query go in this flow? (Between the route handler and the in-memory list — Session 2 will swap that layer.)

Where would JWT auth go? (Before Pydantic validation, as a dependency — Session 3.)

This builds architectural intuition before any code is generated.

---

## 20–35 min: Build the Feature Using Claude Code or Cursor

### Instructor Goal

Demonstrate the correct way to use an AI coding tool — give it precise, scoped instructions, then review the output critically before accepting it.

### Live Demonstration

Open Claude Code or Cursor in the `ai-support-copilot` directory. Use the Main Build Prompt from the student pre-session file. Paste the prompt, run generation, and narrate your observations aloud:

- Does it create the correct file structure (`main.py`, `models.py`, `routes/tickets.py`)?
- Does it use `APIRouter` or put everything in `main.py`?
- Does `TicketCreate` and `TicketResponse` both exist in `models.py`?
- Is the `POST /tickets` endpoint returning 201 or 200?
- Is `HTTPException(status_code=404)` being raised for missing tickets?
- Does `main.py` include the `include_router` call?

### Instructor Narration Rule

Do not silently accept generated code. Say out loud what you see: "It generated the router correctly. But I notice it is not using `status.HTTP_201_CREATED` — let me check whether that is just a style choice or a bug."

### If the AI Generates Scope-Creeping Code

If the AI adds SQLModel, auth scaffolding, or a database connection — stop immediately. Run the Improvement Prompt to strip it back. This teaches students that prompt engineering includes scope control.

---

## 35–50 min: Instructor Code Walkthrough — Read and Explain Every Part

### Instructor Goal

Every student must understand what was generated before they build their own version.

### Walk Through `models.py`

1. Show the import of `BaseModel` from `pydantic` and `Optional` from `typing`.
2. Explain `TicketCreate` — this is what the client sends. Title and description are required. Category, priority are optional with defaults.
3. Explain `TicketResponse` — this is what the server returns. It includes `id`, `status`, `created_at` which the client does not send.
4. Explain `TicketUpdate` — used for PATCH, all fields are `Optional` so the client can update only what they want to change.

### Walk Through `routes/tickets.py`

1. Show the `router = APIRouter()` declaration and the `prefix="/tickets"` parameter.
2. Walk through `POST /tickets`: Pydantic converts the request body into a `TicketCreate` object. The handler generates a UUID, sets `status="open"`, sets `created_at=datetime.utcnow()`, builds a dict, appends to `tickets_db`, and returns the full ticket with `status_code=201`.
3. Walk through `GET /tickets`: Returns the entire `tickets_db` list. Ask — what happens when there are no tickets? It returns an empty list `[]` with 200. Is that correct? Yes — 404 is for when a resource does not exist, not for an empty collection.
4. Walk through `GET /tickets/{id}`: Shows path parameter extraction, linear search through the list, and `HTTPException(404)` when not found.
5. Walk through `PATCH /tickets/{id}`: Explain `exclude_unset=True` on the Pydantic update model — this means only the fields the client explicitly sent are updated.
6. Walk through `DELETE /tickets/{id}`: Explain 204 No Content — the response body is empty on success.

### Walk Through `main.py`

1. Show `app = FastAPI(title="AI Support Ticket Copilot")`.
2. Show `app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])`.
3. Explain that the prefix in `include_router` is combined with any prefix already on the router — watch for double `/tickets/tickets` bugs.

### Ask During Walkthrough

- Why does `TicketResponse` have `created_at` but `TicketCreate` does not?
- What would happen if we forgot `status_code=status.HTTP_201_CREATED` in the POST endpoint?
- What is the difference between a 404 and a 422?
- Why do we use `exclude_unset=True` in the PATCH handler?

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run the Main Build Prompt (Prompt 1 from the student pre-session file) in Claude Code or Cursor inside their own `ai-support-copilot` project directory. They should then start the server and verify Swagger loads at `http://localhost:8000/docs`.

### Instructor Support Areas

Move around the room (or monitor screens) for:

- `ModuleNotFoundError: No module named 'fastapi'` — student forgot to run `pip install fastapi uvicorn`
- Server not starting because `app.include_router` is called before the router is imported
- Swagger not showing because `main.py` is not the entry point passed to `uvicorn`
- Double prefix issue: router has `prefix="/tickets"` AND `include_router` also has `prefix="/tickets"`
- AI generated `app.run()` instead of `uvicorn.run()` — this is Flask syntax

### If Student Build Fails

Do not block the class for individual setup failures. The student should:

- follow the instructor's live screen
- pair with a neighbouring student
- receive the reference implementation code after the session
- use the Debugging Prompt (Prompt 3) to fix their own version post-session

### Command to Start Server

```bash
uvicorn main:app --reload
```

---

## 65–80 min: Test and Improve — Swagger, curl, and Edge Cases

### Instructor Goal

Test every endpoint in Swagger. Demonstrate what correct and incorrect requests look like.

### Test Sequence in Swagger (`http://localhost:8000/docs`)

1. `POST /tickets` with valid body — confirm 201 response and UUID in response.
2. `POST /tickets` with missing `title` field — confirm 422 response with Pydantic error detail.
3. `GET /tickets` — confirm the created ticket is in the list.
4. `GET /tickets/{id}` with the UUID from step 1 — confirm 200.
5. `GET /tickets/{id}` with a fake UUID — confirm 404 with error detail.
6. `PATCH /tickets/{id}` with `{"status": "in_progress"}` — confirm 200 and updated status.
7. `DELETE /tickets/{id}` — confirm 204 No Content.
8. `GET /tickets/{id}` on the deleted ticket — confirm 404.

### Teach While Testing

When Pydantic returns 422, show the error response body — it tells the client exactly which field failed and why. This is one of the strongest arguments for using Pydantic over manual dict parsing.

When GET /tickets returns `[]` on an empty list, emphasize: 404 is "the resource does not exist," not "the list is empty." An empty collection is a valid 200 response.

### Ask the Room

What HTTP status code should we return if someone tries to PATCH a ticket with an invalid status value — say `"banana"` instead of `"open"` or `"closed"`? (422 from Pydantic if we use a string enum, or we can validate manually and raise 422.)

---

## 80–95 min: Error Handling and Edge Cases

### Instructor Goal

Go beyond the happy path. Teach students to think about what can go wrong and how FastAPI handles it.

### Edge Cases to Cover

1. What if `title` is an empty string? By default Pydantic allows it — add a `min_length=1` validator to `TicketCreate.title` to prevent blank titles.
2. What if the client sends extra fields not in `TicketCreate`? By default Pydantic v2 ignores extra fields — mention `model_config = ConfigDict(extra="forbid")` as an option if the team wants strict contracts.
3. What happens with concurrent writes to `tickets_db`? With a single-threaded server it works, but with multiple workers the in-memory list is not shared. This is why we replace it with a database in Session 2.
4. What if the client sends a PATCH body with zero fields? With `exclude_unset=True`, nothing is updated and the original ticket is returned — that is acceptable behavior.
5. What if two tickets get the same UUID? UUID4 collision probability is astronomically low, but worth mentioning — the database in Session 2 will enforce uniqueness via a primary key constraint.

### Add One Enhancement Live

Show students how to add a `status` field validator to `TicketCreate` or `TicketUpdate` using Pydantic's `Literal` type:

```python
from typing import Literal, Optional

class TicketUpdate(BaseModel):
    status: Optional[Literal["open", "in_progress", "resolved", "closed"]] = None
```

This makes Pydantic reject any invalid status value with a 422 automatically — no extra validation logic in the route handler.

---

## 95–105 min: Concept Pause — REST API Design, Pydantic, and HTTP Status Codes

### Instructor Goal

Convert the implementation into transferable technical knowledge. Students need to explain these concepts in interviews, not just use them in code.

### Explain REST API Design Principles

REST stands for Representational State Transfer. The key principles relevant to this session:

1. Resources are nouns, not verbs — `/tickets` not `/createTicket` or `/getTickets`.
2. HTTP methods carry the action — GET to read, POST to create, PATCH to partially update, PUT to fully replace, DELETE to remove.
3. URLs identify resources — `/tickets/{id}` identifies a specific ticket.
4. Stateless — each request carries all the information the server needs; the server does not store client session state (the `tickets_db` list stores data, not session state).

### Explain Pydantic Validation

Pydantic models are Python classes that define the shape and constraints of data. When FastAPI receives a request, it passes the JSON body to the Pydantic model's constructor. If any field fails validation — wrong type, missing required field, value out of range — Pydantic raises a `ValidationError` and FastAPI converts it to a 422 HTTP response with a detailed error body. This happens before your route function even runs. The benefit is that by the time your code executes, you are guaranteed to have valid, type-safe data.

### Explain HTTP Status Codes in This Project

- 200 OK: Request succeeded, response body contains the result.
- 201 Created: POST succeeded, a new resource was created. The convention is to return the created resource in the body.
- 204 No Content: DELETE succeeded, no response body.
- 404 Not Found: The requested resource does not exist.
- 422 Unprocessable Entity: The request is syntactically valid JSON but semantically invalid — Pydantic validation failed.

### Student Writing Task

Ask every student to write a 2–3 line answer:

What is the difference between a 404 and a 422 error in this API?

Expected answer: A 404 means the ticket ID does not exist in the data store. A 422 means the request body failed Pydantic validation — for example, the `title` field was missing or had the wrong type. The 422 is returned automatically by FastAPI before the route handler runs.

---

## 105–115 min: Interview Discussion and Technical Viva Practice

### Instructor Goal

Prepare students to discuss this project in a technical interview. Use the questions from the Questions section below. Ask 3–4 questions to the group, cold-call individuals, and require complete technical sentences — not one-word answers.

### Recommended Questions for This Block

Use Q1, Q4, Q7, Q10, Q12 from the Questions section. These cover the widest range of concepts.

Insist that students say the words: Pydantic, APIRouter, HTTPException, status_code, include_router. If they wave their hands and say "FastAPI does the validation," ask them to be more specific.

---

## 115–120 min: Wrap-Up and Session 2 Preview

### Instructor Closing

Today we built a clean FastAPI backend with 5 REST endpoints, Pydantic validation, proper HTTP status codes, and auto-generated Swagger docs. The data is in memory — which means it disappears when the server restarts.

In Session 2, we will replace the in-memory list with a real database using SQLModel and SQLite. We will create a `Ticket` table, write a database session dependency, and migrate all 5 endpoint handlers to use SQLModel queries instead of list operations. The API contract — the same 5 endpoints, the same Pydantic models — will not change. Only the storage layer changes. That is the value of a well-structured API.

---

# Instructor Notes

## What to Emphasize

Session 1 is not about FastAPI syntax memorization.

Session 1 is about teaching students to:

- think in terms of HTTP verbs and resources before writing code
- write precise, scoped AI prompts for backend code generation
- read and explain generated FastAPI code at a line-by-line level
- understand the request lifecycle in FastAPI (routing → Pydantic validation → handler → response)
- use Swagger as a first-class testing tool, not an afterthought
- connect HTTP status codes to real scenarios in the API
- structure a Python backend project cleanly from the first session
- explain design decisions as trade-offs, not just implementation choices

## Common Student Mistakes

Students at this level will hit specific, predictable errors. Prepare for each:

1. **Double prefix bug**: Student sets `prefix="/tickets"` on `APIRouter()` AND passes `prefix="/tickets"` to `app.include_router()`. Result: all endpoints are at `/tickets/tickets/{id}`. Fix: set prefix in only one place — convention is to set it in `include_router`.

2. **`app.run()` instead of `uvicorn main:app --reload`**: Students with Flask background may try `app.run()`. This will silently do nothing or throw an `AttributeError`. Fix: always start FastAPI apps with `uvicorn`.

3. **422 on valid-looking request**: Student sends a POST body where `priority` is an integer (`1`) but the model expects a string (`"high"`). Pydantic's coercion rules matter — in v2, strict mode does not coerce int to str. Fix: check the Pydantic model type annotation.

4. **Returning 200 instead of 201 from POST**: AI sometimes generates `@router.post("/")` without `status_code=status.HTTP_201_CREATED`. The endpoint works but returns incorrect status code. Fix: add `status_code=status.HTTP_201_CREATED` to the decorator.

5. **Missing `include_router` call**: Student builds the router in `routes/tickets.py` but forgets to call `app.include_router(tickets_router)` in `main.py`. FastAPI starts without error but the endpoints return 404. Fix: verify `main.py` imports and mounts the router.

6. **PATCH replacing the entire ticket**: Student uses `ticket.update(update_data.model_dump())` instead of `ticket.update(update_data.model_dump(exclude_unset=True))`. Result: PATCH with `{"status": "closed"}` sets all other fields to `None`. Fix: always use `exclude_unset=True` for partial update patterns.

7. **DELETE returning 200 with empty body vs 204 No Content**: AI sometimes returns `{}` with 200 instead of a proper 204. In HTTP spec, 204 must have no response body. Fix: use `status_code=status.HTTP_204_NO_CONTENT` and `return None`.

8. **In-memory list not shared across requests in multi-worker mode**: A student runs `uvicorn main:app --workers 4`. Different requests go to different worker processes, each with their own copy of `tickets_db`. Tickets created in one request may not appear in another. Fix: this is the exact reason we add a database in Session 2 — flag it as a known limitation of in-memory storage.

9. **`TicketResponse` not inheriting from `BaseModel`**: AI occasionally generates `TicketResponse` as a TypedDict or a plain dataclass. FastAPI will not serialize it correctly for all edge cases. Fix: ensure `TicketResponse(BaseModel)`.

10. **Router prefix conflict when using both `prefix` on `APIRouter` and in `include_router`**: Related to mistake 1, but a subtler version — the student sees `/tickets/` working but `/tickets/{id}` returning 404. Root cause: the path in the router is `/{id}` but the combined prefix is `/tickets//tickets/{id}` due to double slash. FastAPI sometimes silently handles the double slash, sometimes not. Fix: standardize prefix location.

## How to Control the Session

Use this rule: if a student's question requires explaining Session 2 content (database, ORM, migrations), answer it with "that is exactly what we tackle in Session 2 — for now, note the limitation of in-memory storage." Do not let the session drift into SQLModel or SQLAlchemy.

If students are ahead, use the extra time on the edge case section (80–95 min) and have them add Pydantic `Literal` validators for the `status` and `priority` fields.

## Setup Rule

Do not spend more than 5 minutes of live class on environment setup.

Students must have Python 3.11+, `pip install fastapi uvicorn` working, and a code editor open before class. If setup fails, the student follows along and uses the reference implementation code post-session.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What did you build in Session 1?

Expected answer:

I built the REST API layer of an AI Support Ticket Resolution Copilot using FastAPI. The API exposes 5 endpoints for CRUD operations on support tickets: POST to create, GET to list all, GET by ID to retrieve one, PATCH to update status, and DELETE to remove. Data is stored in an in-memory Python list for this session, with Pydantic models handling request and response validation. The API auto-generates Swagger documentation at `/docs`. This is the foundation that future sessions will extend with a real database, JWT authentication, and AI-powered features.

### Q2. What is the Ticket data model and why did you choose those fields?

Expected answer:

The `Ticket` model has seven fields: `id` (UUID, server-generated), `title` (str, required, the short summary of the issue), `description` (str, required, the full problem description), `category` (str, e.g., "billing", "technical"), `priority` (str, e.g., "low", "high", "critical"), `status` (str, defaults to "open"), and `created_at` (datetime, server-generated). The fields map directly to what a support system needs to triage and route a ticket. The `id` and `created_at` fields are not in `TicketCreate` because the client should not set them — the server controls resource identity and creation timestamps.

### Q3. What Python packages does this project use and what does each do?

Expected answer:

`fastapi` is the web framework that handles routing, dependency injection, and response serialization. `uvicorn` is the ASGI server that actually listens for HTTP connections and passes them to FastAPI. `pydantic` ships with FastAPI and handles request body parsing, type coercion, and validation — when a field fails validation, Pydantic raises a `ValidationError` which FastAPI converts to a 422 response. The `uuid` module from the standard library generates UUID4 identifiers for each ticket. The `datetime` module generates UTC timestamps for `created_at`. No external database driver is needed in Session 1 because storage is in-memory.

### Q4. How does Swagger documentation get generated in FastAPI?

Expected answer:

FastAPI generates OpenAPI-compliant JSON at `/openapi.json` by inspecting route decorators, path parameters, request body type annotations, and response model annotations at startup. Swagger UI at `/docs` and ReDoc at `/redoc` are both served automatically using that JSON schema — no additional configuration is required. The `response_model` parameter on route decorators tells FastAPI what shape to document and use for serialization. The `tags` parameter on `include_router` groups endpoints in the Swagger UI. This zero-configuration documentation is one of the core productivity advantages of FastAPI over Flask.

### Q5. What is the project folder structure and why is it structured that way?

Expected answer:

The project uses `main.py` as the application entry point that creates the FastAPI app and mounts routers. `models.py` contains all Pydantic schemas — `TicketCreate`, `TicketResponse`, and `TicketUpdate`. `routes/tickets.py` contains the `APIRouter` with all five ticket endpoint handlers. This separation follows the single responsibility principle: main.py handles app configuration, models.py handles data contracts, and routes/tickets.py handles HTTP logic. It also makes the codebase easy to extend — Session 2 will add `database.py` and `routes/tickets.py` will import the DB session without touching `main.py`.

---

## Technical Deep-Dive Questions

### Q6. What is the difference between `TicketCreate`, `TicketUpdate`, and `TicketResponse`?

Expected answer:

`TicketCreate` defines the fields that the client must provide when creating a ticket — `title`, `description`, `category`, and `priority`. It does not include `id`, `status`, or `created_at` because those are server-controlled. `TicketUpdate` is used for the PATCH endpoint and all its fields are `Optional` — this allows the client to send only the fields they want to change, and we use `exclude_unset=True` to ensure we do not overwrite unchanged fields with `None`. `TicketResponse` defines the full shape of a ticket as returned by the API — it includes all fields including server-generated ones. Using separate models prevents the client from setting fields they should not control and gives the server explicit ownership of resource identity.

### Q7. Why does `POST /tickets` return 201 instead of 200?

Expected answer:

HTTP 201 Created is semantically correct for a POST endpoint that creates a new resource. It signals to the client that a new resource was created on the server, and by convention the response body contains the representation of the created resource including its server-assigned `id`. Returning 200 OK would technically work but is semantically wrong — 200 means the request succeeded and here is some data, while 201 specifically communicates that a new resource now exists in the system. In FastAPI, the status code is set via `status_code=status.HTTP_201_CREATED` in the route decorator. If you forget this, FastAPI defaults to 200 for all successful responses.

### Q8. How does Pydantic validation work in the request lifecycle?

Expected answer:

When FastAPI receives a POST request, it reads the raw JSON body and attempts to construct a `TicketCreate` instance from it. This happens in FastAPI's request handling pipeline before the route handler function is called. Pydantic's `__init__` method performs type coercion (e.g., converting a JSON string to a Python `str`) and constraint validation (e.g., `min_length=1` on `title`). If any field fails — missing required field, wrong type, constraint violation — Pydantic raises `ValidationError`. FastAPI catches this and returns a 422 Unprocessable Entity response with a JSON body that lists each field error with its location, message, and type. The route handler function is never called. This means you can trust that all parameters reaching your function are type-safe and validated.

### Q9. How does the PATCH endpoint avoid overwriting fields that the client did not send?

Expected answer:

The PATCH handler accepts a `TicketUpdate` Pydantic model where all fields are `Optional`. When we call `update_data.model_dump(exclude_unset=True)`, Pydantic returns only the fields that were explicitly set in the request body, not all fields including `None` defaults. For example, if the client sends `{"status": "closed"}`, `exclude_unset=True` gives `{"status": "closed"}` — not `{"status": "closed", "title": None, "priority": None}`. We then call `ticket.update(update_data.model_dump(exclude_unset=True))` on the in-memory dict, which only overwrites the keys present in the update dict. This is the correct implementation of HTTP PATCH semantics — partial update, not full replacement. If we used `model_dump()` without `exclude_unset=True`, we would accidentally null out all the fields the client did not send.

### Q10. What does `app.include_router` do and what happens if you forget it?

Expected answer:

`app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])` registers all routes defined on the `APIRouter` instance with the main FastAPI application. Without this call, FastAPI has no knowledge that the routes in `routes/tickets.py` exist, and any request to `/tickets/` will return a 404 Not Found. The `prefix` parameter prepends `/tickets` to all routes on the router — so a route decorated with `@router.get("/{id}")` in the router file becomes accessible at `/tickets/{id}` in the running app. The `tags` parameter groups these routes in the Swagger UI under a "tickets" heading. A common mistake is setting `prefix="/tickets"` both in `APIRouter(prefix="/tickets")` and in `include_router(prefix="/tickets")`, which results in double-prefixed paths like `/tickets/tickets/{id}`.

---

## System Design and Trade-off Questions

### Q11. Why use in-memory storage in Session 1 instead of starting with a database immediately?

Expected answer:

In-memory storage lets us focus entirely on the API contract and request/response lifecycle without introducing the complexity of database connections, ORM session management, migration tooling, and connection pooling. This is a deliberate pedagogical choice, but it also mirrors a legitimate engineering practice: when prototyping a new API, in-memory storage lets you validate the data model and endpoint design quickly before committing to a schema. The trade-off is obvious — data is lost on server restart and the storage is not thread-safe across multiple workers. These exact limitations motivate Session 2's database integration. The key point is that the API contract (URLs, methods, request/response models) does not change between Session 1 and Session 2 — only the storage layer changes.

### Q12. What are the trade-offs of using Pydantic for request validation vs manual dict parsing?

Expected answer:

With Pydantic, you declare the expected shape of data as a Python class with type annotations, and all validation, type coercion, and error reporting happens automatically before your function runs. Manual dict parsing requires you to write `if "title" not in body: return 400` style checks for every field, handle type conversion yourself, and format error responses manually. Pydantic is dramatically more maintainable — a change to the `TicketCreate` model immediately affects validation, documentation, and IDE autocomplete. The trade-off is that Pydantic v2 is strict about types in a way that can surprise developers: for example, a JSON integer will not automatically coerce to a Python string in strict mode. There is also a small runtime overhead for model construction, which is negligible for typical API workloads but relevant at extremely high throughput.

### Q13. How would you explain the REST API design decisions in this project to a senior engineer?

Expected answer:

The API follows REST conventions: resources are nouns (`/tickets`), HTTP verbs carry the action semantics, and the URL structure reflects resource hierarchy (`/tickets/{id}` for a specific ticket). We chose PATCH over PUT for the update endpoint because support tickets are partially updated — typically only the `status` changes, and the client should not need to resend the entire ticket. We return 201 on POST to distinguish resource creation from generic success responses. We return 204 with no body on DELETE rather than 200 with a confirmation message, which aligns with HTTP spec and prevents clients from accidentally parsing an empty response body. The `TicketResponse` model is separate from `TicketCreate` to enforce server-side control of `id` and `created_at` — this is a security and correctness concern, not just a style choice.

### Q14. What are the concurrency limitations of the in-memory storage approach?

Expected answer:

The in-memory `tickets_db` list is stored in the Python interpreter's memory for a single process. If `uvicorn` is run with `--workers 4`, four separate processes each have their own copy of `tickets_db`, and a ticket created by one worker will not be visible to another. Within a single worker, FastAPI uses `asyncio` for concurrency — if two coroutines attempt to append to `tickets_db` concurrently, there is a risk of a race condition, though CPython's GIL makes simple list appends thread-safe in practice. For a production system, shared mutable state in-process is never acceptable. The correct solution is to store state in a process-external database — which is exactly what Session 2 addresses. This limitation is a feature of Session 1's design: it creates a clear, motivating reason to introduce a database.

### Q15. If a client sends a `POST /tickets` request without the `title` field, what exactly happens at each layer?

Expected answer:

FastAPI reads the raw HTTP body and attempts to deserialize it as JSON — this succeeds. It then passes the JSON dict to `TicketCreate.__init__()` for Pydantic model construction. Pydantic detects that `title` is a required field (no default value) and is missing from the input. Pydantic raises a `ValidationError` internally with the error detail: field "title" is required. FastAPI's request handling middleware catches the `ValidationError` before the route handler is called and converts it to an HTTP 422 Unprocessable Entity response. The response body is a JSON object with a `detail` array, each element describing one validation failure with keys `loc` (field location), `msg` (human-readable message), and `type` (Pydantic error type string). The route handler function `create_ticket()` is never invoked. This entire process takes under one millisecond.

---

# Session 1 Completion Checklist

Students should meet all of the following by the end of the session:

- [ ] Project directory exists: `ai-support-copilot/` with `main.py`, `models.py`, `routes/__init__.py`, `routes/tickets.py`
- [ ] `uvicorn main:app --reload` starts without errors
- [ ] Swagger UI loads at `http://localhost:8000/docs` and shows all 5 endpoints
- [ ] `POST /tickets` with valid body returns HTTP 201 and includes `id` and `created_at` in response
- [ ] `POST /tickets` with missing `title` returns HTTP 422 with a Pydantic error detail body
- [ ] `GET /tickets` returns HTTP 200 and a list containing the created ticket
- [ ] `GET /tickets` on empty store returns HTTP 200 with an empty array `[]`, not 404
- [ ] `GET /tickets/{id}` with valid UUID returns HTTP 200 and the correct ticket
- [ ] `GET /tickets/{id}` with non-existent UUID returns HTTP 404 with error detail
- [ ] `PATCH /tickets/{id}` with `{"status": "in_progress"}` returns HTTP 200 with updated status only
- [ ] `DELETE /tickets/{id}` returns HTTP 204 with no response body
- [ ] `DELETE /tickets/{id}` followed by `GET /tickets/{id}` returns HTTP 404
- [ ] Student can explain what `exclude_unset=True` does in the PATCH handler

---

# Instructor Backup Plan

If Claude Code or Cursor generation fails or produces severely out-of-scope code:

1. Instructor continues live build on screen, typing code manually or using a pre-prepared reference implementation.
2. Students follow conceptually and take notes on the architecture diagram.
3. Share the reference `session_1_complete/` code directory with students after the session via the course repository.
4. Students use the prompts from the student pre-session file to regenerate their version post-session.
5. Do not sacrifice the Concept Pause (95–105 min) or the Interview Discussion (105–115 min) blocks — these are the highest-value segments for student outcomes.
6. If Swagger is not loading due to a server error, switch to testing with `curl` or `httpie` to demonstrate the endpoint behavior while the student fixes their setup asynchronously.
