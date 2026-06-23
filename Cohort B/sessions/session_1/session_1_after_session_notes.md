# Session 1 After-Session Notes: Build Core Backend — Ticket CRUD API

## What We Built Today

Today we built the REST API foundation of the AI Support Ticket Resolution Copilot.

The application exposes 5 endpoints:

- `POST /tickets` — create a new support ticket, returns 201 with the full ticket including server-generated `id` and `created_at`
- `GET /tickets` — list all tickets with optional filtering by `status`, `priority`, `category`, returns 200
- `GET /tickets/{id}` — retrieve a single ticket by UUID, returns 200 or 404
- `PATCH /tickets/{id}` — partially update a ticket (typically the `status`), returns 200 or 404
- `DELETE /tickets/{id}` — remove a ticket, returns 204 No Content or 404

The application uses:

- FastAPI with `APIRouter` for route organization
- Pydantic `BaseModel` subclasses (`TicketCreate`, `TicketUpdate`, `TicketResponse`) for input validation and response serialization
- Python's `uuid` module for server-generated ticket identifiers
- Python's `datetime` module for server-generated `created_at` timestamps
- An in-memory `list[dict]` as temporary storage
- Auto-generated Swagger UI at `http://localhost:8000/docs`

Project structure after Session 1:

```
ai-support-copilot/
├── main.py               ← FastAPI app, router registration, health check
├── models.py             ← Pydantic schemas: TicketCreate, TicketUpdate, TicketResponse
└── routes/
    ├── __init__.py
    └── tickets.py        ← APIRouter with all 5 endpoint handlers, tickets_db list
```

---

# Why This Feature Matters for Production Systems

The REST API layer is the public contract of the system. Every other component — the database, authentication, AI features, and the frontend — communicates through this contract. When the API contract is well-designed from the start, adding layers is a matter of swapping internals without changing the interface.

Pydantic validation at the API boundary is a production-critical pattern. Without it, bad data from clients can propagate into your database, corrupt your embeddings, or cause your LLM prompts to behave unexpectedly. Catching invalid data at the edge — before it reaches any storage or business logic — is far cheaper than debugging it downstream. This is particularly important in an AI-powered system where malformed input can cause silent failures in LLM calls or semantic search.

In-memory storage is not production-viable, but the discipline of defining a clean data model first (what fields a ticket needs, which are client-controlled vs server-controlled) is. The `TicketCreate` / `TicketResponse` split enforced today directly prevents a class of security bugs: clients cannot submit their own `id`, override `created_at`, or inject a custom `status` on creation. This separation of client input from server output is a pattern we maintain across every session.

---

# System Architecture Flow

The full system we are building across 8 sessions, showing how each session adds to the stack:

```
Session 1 — REST API (TODAY)
HTTP Client
    |
    v
FastAPI app (main.py)  →  APIRouter /tickets (routes/tickets.py)
    |
    v
Pydantic Validation → 422 on bad input, pass-through on valid input
    |
    v
In-memory list (tickets_db)
    |
    v
TicketResponse JSON

    ↓ Session 2 replaces in-memory list with:

Session 2 — Database Layer
SQLModel ORM → SQLite (dev) / PostgreSQL (prod)
    |
    v
Ticket table, DB session dependency, Alembic migrations

    ↓ Session 3 wraps all routes with:

Session 3 — Authentication
OAuth2PasswordBearer → JWT decode → Current user dependency
    |
    v
Protected routes, User model, role-based access

    ↓ Session 4 adds a new endpoint and background processing:

Session 4 — LLM Auto-categorization
POST /tickets/{id}/analyze → OpenAI Chat API
    |
    v
Structured JSON response → update ticket category, priority, suggested_solution

    ↓ Session 5 adds a new data layer:

Session 5 — Semantic Search
OpenAI text-embedding-3-small → ChromaDB collection
    |
    v
POST /tickets/{id}/similar → top-k similar past tickets

    ↓ Session 6 adds retrieval-augmented generation:

Session 6 — RAG Solution Retrieval
LangChain → ChromaDB retriever → OpenAI LLM chain
    |
    v
POST /tickets/{id}/suggest-solution → cited solution from knowledge base

    ↓ Session 7 adds an autonomous agent:

Session 7 — LangGraph Resolution Agent
LangGraph StateGraph:
  classify_node → search_similar_node → draft_solution_node → escalate_node
    |
    v
POST /tickets/{id}/resolve → agent runs workflow, updates ticket status

    ↓ Session 8 wraps the whole system:

Session 8 — Deployment and Monitoring
Docker → Cloud platform (Render / Railway / GCP)
    |
    v
Health checks, structured logging, environment config, CI/CD
```

---

# Technical Deep-Dive: FastAPI REST API Design, Pydantic Validation, and HTTP Status Codes

## FastAPI Request Lifecycle

When a FastAPI application receives an HTTP request, it goes through a deterministic processing pipeline. The ASGI server (uvicorn) accepts the raw TCP connection and constructs an ASGI `scope`, `receive`, and `send` interface. Starlette's routing layer matches the request path and method against registered routes. If a match is found, FastAPI inspects the route handler's function signature using Python's `inspect` module — this happens at startup, not per-request. FastAPI builds a "dependency tree" from the signature: path parameters, query parameters, request body, and injected dependencies. For request bodies typed as Pydantic `BaseModel` subclasses, FastAPI deserializes the raw JSON into the Pydantic model at runtime using `model.model_validate(data)`. If this raises a `ValidationError`, FastAPI's `RequestValidationError` handler intercepts it and returns a 422 response with a detailed error body — the route handler function is never invoked. If validation passes, FastAPI calls the handler with fully typed, validated arguments.

## Why Pydantic Models Are Not Just Validation

Pydantic models serve three distinct purposes in this API. First, they define the API contract — `TicketCreate` is documentation that tells every client exactly what fields are required and what their types are. Second, they enforce server-side data ownership — `id`, `status`, and `created_at` are in `TicketResponse` but not in `TicketCreate`, which means the server unilaterally controls resource identity and lifecycle state. This is a security property: without this separation, a malicious client could create a ticket with `id="admin"` or `status="resolved"` before the support team even sees it. Third, `model_dump(exclude_unset=True)` provides precise semantics for partial updates — it returns only the fields the client explicitly sent, not defaults for fields they omitted. This makes the difference between "client wants to change this field to None" and "client did not send this field" explicit and machine-readable, which is the correct implementation of HTTP PATCH.

## HTTP Status Codes as a Communication Protocol

HTTP status codes are not just numbers — they are a communication protocol between the server and every client including browsers, API gateways, load balancers, and monitoring systems. A 201 Created response tells caching proxies and clients that a new resource exists and where to find it (via the `Location` header, which we can add in a later session). A 204 No Content tells HTTP clients not to attempt to parse a response body — some HTTP clients will throw a parse error if you return 200 with an empty body on DELETE. A 422 Unprocessable Entity is semantically distinct from 400 Bad Request: 400 means the HTTP request itself is malformed (e.g., invalid JSON), while 422 means the HTTP request is structurally valid but the business-level data is invalid (e.g., `priority` has a value not in the allowed set). Using the wrong status code does not break the API in development but causes real problems in production: monitoring systems alert on 5xx not on 4xx, API gateways retry on different status codes, and client SDKs branch their error handling based on the numeric code.

---

# What Students Should Understand

After Session 1, every student should be able to explain or demonstrate the following without notes:

1. The 5 endpoints built today: their HTTP methods, URL patterns, request bodies, and success status codes — POST returns 201, GET returns 200, PATCH returns 200, DELETE returns 204, 404 for missing resources in GET/PATCH/DELETE.

2. The role of each file in the project: `main.py` creates and configures the app, `models.py` defines the data contracts, `routes/tickets.py` contains the HTTP handler logic and in-memory storage.

3. Why `TicketCreate` and `TicketResponse` are separate models: the client controls input fields (`title`, `description`, `category`, `priority`) and the server controls output-only fields (`id`, `status`, `created_at`).

4. The exact sequence of events when a POST request with an invalid body arrives: JSON deserialization succeeds → Pydantic model construction fails → `ValidationError` raised → FastAPI returns 422 with error detail → route handler never called.

5. Why `model_dump(exclude_unset=True)` is required in the PATCH handler: without it, every unset field in `TicketUpdate` would overwrite the stored value with `None`.

6. Why `GET /tickets` with no tickets returns `200 []` and not `404`: an empty collection is a valid response; 404 means the resource itself does not exist, not that the collection is empty.

7. The `app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])` pattern: this is how routes in a separate file become accessible on the main application, and the prefix is added to every route on that router.

8. Two concrete production limitations of in-memory storage: data is lost on server restart; data is not shared across multiple worker processes, so `uvicorn --workers 4` gives inconsistent results.

9. How Swagger docs are generated: FastAPI inspects route decorators, type annotations, and Pydantic models at startup and builds an OpenAPI JSON schema, which Swagger UI renders interactively at `/docs`.

10. The `Literal["open", "in_progress", "resolved", "closed"]` pattern in `TicketUpdate.status`: restricts the field to an enumerated set of values and returns a 422 automatically if an invalid string is sent.

---

# Interview-Ready Explanation

```text
I built the REST API layer of an AI Support Ticket Resolution Copilot using FastAPI. The API defines five CRUD endpoints for support tickets — create with POST returning 201, list and retrieve with GET, partial update with PATCH using Pydantic's exclude_unset for correct partial update semantics, and delete with DELETE returning 204. Pydantic models enforce a clean separation between client-controlled input fields and server-controlled output fields like the UUID and timestamp, which prevents clients from injecting their own resource identifiers. The project uses an in-memory list for storage in this session, which is intentionally replaced with a SQLModel database in the next session — the API contract does not change, only the storage layer does.
```

---

# What Happens When POST /tickets Is Called

```text
1. uvicorn receives the HTTP request and passes it to FastAPI's ASGI handler.
2. Starlette's router matches "POST /tickets" to the create_ticket handler in routes/tickets.py.
3. FastAPI reads the request body as raw bytes and deserializes it as JSON.
4. FastAPI calls TicketCreate.model_validate(json_body). If any field fails — missing required field, wrong type, value constraint violation — Pydantic raises ValidationError and FastAPI returns HTTP 422 with a detail array listing each field error. The create_ticket function is never called.
5. If validation passes, FastAPI calls create_ticket(ticket: TicketCreate) with a fully validated TicketCreate instance.
6. The handler generates a new UUID4 string with str(uuid.uuid4()).
7. The handler sets status = "open" and created_at = datetime.utcnow().isoformat().
8. The handler builds a dict from ticket.model_dump() plus the server-generated fields.
9. The dict is appended to the module-level tickets_db list.
10. The handler returns a TicketResponse constructed from the new ticket dict, with status_code=201.
11. FastAPI serializes the TicketResponse to JSON using Pydantic's model_dump() and writes it as the HTTP response body with Content-Type: application/json and HTTP/1.1 201 Created.
No database query is executed. No LLM call is made. This is pure API layer logic.
```

---

# What AI Was Used For + What Engineers Must Still Do

## What AI Generated in Session 1

- The initial project folder structure and all three files
- Pydantic model class definitions with correct field types and Optional patterns
- APIRouter setup with all 5 route decorators and correct HTTP methods
- In-memory list search pattern using `next((t for t in tickets_db if t["id"] == id), None)`
- `exclude_unset=True` usage in the PATCH handler
- `Response(status_code=204)` for the DELETE endpoint
- `app.include_router()` call in `main.py`
- Type annotations on all route handler signatures

## What Engineers Must Still Do

Even with AI-generated code, you are responsible for:

1. **Verifying the API contract is complete**: Does every endpoint return the correct status code on both success and failure? Is 201 used for POST and not 200? Does DELETE return 204 with no body?

2. **Catching scope creep in generated code**: AI will often add SQLModel imports, auth middleware, or database connection boilerplate even when not asked. You must read the generated code and strip anything outside scope.

3. **Testing all paths through Swagger**: Happy path (valid input), missing required field (expect 422), non-existent ID (expect 404), delete then get (expect 404). AI cannot run your server.

4. **Understanding the `exclude_unset=True` pattern**: AI generates it but you need to explain why — without it, PATCH becomes a partial PUT and overwrites unset fields with None.

5. **Catching the double prefix bug**: AI sometimes sets `prefix="/tickets"` in both `APIRouter()` and `include_router()`. You must read `main.py` and `routes/tickets.py` together to catch this.

6. **Explaining every design decision in interview language**: Why REST? Why Pydantic? Why separate models? Why 201 for POST? AI generates working code — you must generate the reasoning.

7. **Writing and running the test suite**: AI can generate pytest tests but you must run them, interpret failures, and fix root causes.

---

# Common Issues and Fixes

## Issue 1: Server starts but all ticket endpoints return 404

This usually means `app.include_router()` was not called in `main.py`, or the router import failed silently.

Verify by checking `main.py` for this line:
```python
from routes.tickets import router as tickets_router
app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
```

Also check for the double prefix bug — if `APIRouter(prefix="/tickets")` and `include_router(prefix="/tickets")` are both set, endpoints appear at `/tickets/tickets/{id}`.

What to ask AI:

```text
My FastAPI server starts without errors but all requests to /tickets return 404. Here is my main.py and routes/tickets.py. Find the issue — specifically check whether app.include_router is present, whether there is a double prefix on the router and include_router, and whether the router import succeeds. Show the fix.
```

---

## Issue 2: 422 Unprocessable Entity on a request that looks valid

Actual error message from FastAPI 422 body:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "title"],
      "msg": "Field required",
      "input": {"description": "Login broken"}
    }
  ]
}
```

Most common causes: `title` is missing from the request body, or `priority` was sent as an integer (`1`) when the model expects a string (`"high"`), or `status` was sent in the POST body but `TicketCreate` does not have a `status` field and `extra="forbid"` is set on the model config.

What to ask AI:

```text
I am getting a 422 error on POST /tickets. Here is the exact 422 response body: [paste the full JSON detail array]. Here is my TicketCreate model: [paste models.py]. Identify which field is failing validation, why it is failing, and show me how to fix either the request body or the model depending on which is wrong.
```

---

## Issue 3: PATCH updates one field but sets all other fields to None

This happens when `model_dump()` is used instead of `model_dump(exclude_unset=True)` in the PATCH handler. When `TicketUpdate` is constructed with only `{"status": "closed"}`, all other fields default to `None`. `model_dump()` returns `{"status": "closed", "title": None, "description": None, ...}`. When this is applied to the stored ticket dict with `ticket.update(...)`, all fields are overwritten including `None` values.

What to ask AI:

```text
My PATCH endpoint is wiping all ticket fields except the one I updated. For example, PATCH with {"status": "closed"} returns the ticket with title=None and description=None. Here is my PATCH handler: [paste the handler]. The bug is related to how model_dump is called. Show me the fix using exclude_unset=True and explain why this argument changes the output.
```

---

# Key Takeaways

1. **The API contract is the most important design decision in this project.** The choice of fields in `TicketCreate` vs `TicketResponse`, the HTTP methods, and the status codes we set today will be referenced by every future session. Changing the contract later means updating the database schema, the auth middleware, and every LLM prompt that formats ticket data. Design it carefully on day one.

2. **Pydantic validation is a security boundary, not just a convenience.** Separating `TicketCreate` from `TicketResponse` is not a style preference — it prevents clients from setting server-owned fields like `id` and `status`. As this system grows to include JWT user IDs, role-based permissions, and AI-generated categorizations, keeping the input/output model separation sharp becomes increasingly important.

3. **In-memory storage is a deliberate, documented trade-off.** The `tickets_db` list works perfectly for a single-process, non-persistent demo. Its limitations — data loss on restart, no cross-process sharing — are the exact motivation for Session 2's database layer. Good engineers name their trade-offs explicitly; do not pretend the list is a production database.

4. **FastAPI's automatic behavior (Swagger, 422 handling, Pydantic integration) saves significant boilerplate, but you must understand what it does.** When you can explain that FastAPI generates OpenAPI JSON from type annotations at startup, and converts Pydantic `ValidationError` to 422 before your handler runs, you are demonstrating backend engineering depth — not just framework usage. That distinction is what interviewers are testing.

---

# Session 2 Preview

In Session 2, we will replace the in-memory `tickets_db` list with a real database using SQLModel and SQLite (with a path toward PostgreSQL for production).

We will add:

- `database.py` — SQLite engine, `create_db_and_tables()` function, and a `get_session` dependency using `Session(engine)`
- A `Ticket` SQLModel table class with the same fields as `TicketResponse` plus SQLModel column decorators
- Updated route handlers in `routes/tickets.py` that accept `session: Session = Depends(get_session)` and use SQLModel queries: `session.add()`, `session.commit()`, `session.refresh()`, `session.exec(select(Ticket))`, `session.get(Ticket, id)`, `session.delete()`
- A startup event in `main.py` that calls `create_db_and_tables()` on application start

The API contract will not change — the same 5 endpoints, the same Pydantic models, the same status codes. Only the internal storage mechanism changes. If your Session 1 Swagger tests pass, your Session 2 Swagger tests will pass with the same inputs and expected outputs.

The key new concept in Session 2 is the FastAPI dependency injection pattern for database sessions — understanding why `Depends(get_session)` exists and how FastAPI manages the session lifecycle per-request is critical preparation for Session 3's JWT auth dependency.
