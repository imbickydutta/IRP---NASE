# Session 2 After-Session Notes: Add Database Layer + Data Modeling

## What We Built Today

Today we replaced the in-memory Python list from Session 1 with a persistent SQLite database using SQLModel as the ORM.

Specifically, we added:

- `app/database.py` — SQLite engine, `create_db_and_tables()` startup function, and `get_session()` dependency generator
- Updated `app/models.py` — `Ticket` redefined as a `SQLModel` table class (`table=True`) with proper field types, a primary key, and timestamp fields using `default_factory`
- Updated `app/main.py` — startup event calling `create_db_and_tables()`, all 5 endpoints refactored to use `db: Session = Depends(get_session)` with proper ORM operations
- `tickets.db` — the SQLite database file created on first run at the project root

All 5 endpoints now persist to disk:

- `POST /tickets` — uses `db.add()`, `db.commit()`, `db.refresh()`
- `GET /tickets` — uses `db.exec(select(Ticket)).all()`
- `GET /tickets/{id}` — uses `db.get(Ticket, ticket_id)`, returns 404 if not found
- `PUT /tickets/{id}` — uses `db.get()`, `model_dump(exclude_unset=True)`, `setattr` loop, `db.add()`, `db.commit()`, `db.refresh()`
- `DELETE /tickets/{id}` — uses `db.get()`, `db.delete()`, `db.commit()`, returns 204

---

# Why This Feature Matters for Production Systems

In-memory storage is a development convenience, not an architecture decision. Any backend that stores application state in a process-level variable — a Python list, a dictionary, a class variable — loses all state the moment the process exits. In production environments, processes exit constantly: deployments restart workers, auto-scalers terminate idle instances, servers crash and recover, and health checks cycle processes. A backend that loses its data on any of these events is not a backend — it is a calculator.

The database layer introduced in Session 2 is the first genuinely production-credible component of this project. It separates application state from application process. The `tickets.db` file exists independently of any running uvicorn instance. You can stop the server, update the code, restart, and all previously created tickets are intact. This separation is the foundational contract that every subsequent feature depends on: authentication needs to look up persistent user records, LLM classification needs to read ticket content and write back results, vector search needs stable ticket IDs to associate with embeddings.

From an engineering standpoint, the ORM pattern we adopted with SQLModel is worth understanding deeply. SQLModel's combination of SQLAlchemy and Pydantic into a single class definition means the `Ticket` model is simultaneously the database schema, the API input validator, and the API response serializer. Any change to the field definitions propagates through all three layers. This is a significant DX win for a project of this scope, and it is the reason SQLModel has become the idiomatic choice for FastAPI-based backends. The trade-off is that SQLModel does not give you fine-grained control over the underlying SQL — for complex analytical queries or performance-critical read paths, you may need to drop down to raw SQLAlchemy expressions or even raw SQL via `text()`. For CRUD operations, it is the right abstraction.

---

# System Architecture Flow

The full project architecture grows with each session. After Session 2:

```
Session 1 (Core Backend):
HTTP Request --> FastAPI Router --> Pydantic Validation --> In-Memory List --> HTTP Response

Session 2 (Database Layer) — current:
HTTP Request --> FastAPI Router --> Pydantic Validation --> Depends(get_session) --> SQLModel ORM --> SQLite (tickets.db) --> HTTP Response

Session 3 (Auth — coming next):
HTTP Request --> FastAPI Router --> JWT Decode (OAuth2PasswordBearer) --> Depends(get_current_user) --> SQLModel ORM --> SQLite (tickets.db + users table) --> HTTP Response

Session 4 (LLM Classification — planned):
HTTP Request --> FastAPI Router --> JWT Auth --> SQLModel ORM --> Gemini API (gemini-1.5-flash) (classify ticket) --> SQLModel ORM (write classification back) --> SQLite --> HTTP Response

Session 5 (RAG / Vector Search — planned):
HTTP Request --> FastAPI Router --> JWT Auth --> SQLModel ORM --> sentence-transformers embeddings --> ChromaDB (vector store) --> Similarity Results --> HTTP Response

Session 6+ (LangGraph Agent — planned):
HTTP Request --> FastAPI Router --> JWT Auth --> LangGraph Agent (multi-step) --> SQLModel + Gemini API (gemini-1.5-flash) + ChromaDB --> HTTP Response with resolution
```

Every layer from Session 3 onwards depends on the database being available. The decision to add persistence in Session 2 — before auth, before LLM integration — is deliberate architecture sequencing.

---

# Technical Deep-Dive: Database Modeling, ORM, and Persistence

## What an ORM Does and Why It Matters

An Object-Relational Mapper (ORM) is a layer of abstraction that maps database rows to Python objects and SQL operations to method calls. Without an ORM, reading a row from a database requires executing a raw SQL string, receiving a tuple of values, and manually constructing the Python object from those values. With SQLModel, the mapping is defined once in the class definition and handled automatically: `db.get(Ticket, 1)` issues `SELECT * FROM ticket WHERE id = 1`, maps the row to a `Ticket` instance, and returns it with all fields populated. The value of this abstraction is not just developer convenience — it is type safety, query composition (`.where()` clauses chain as Python method calls rather than string concatenation), and integration with the validation layer. The `Ticket` class is a single source of truth for both the database schema and the API contract.

SQLModel's specific design choice — inheriting from both `SQLModel` (for SQLAlchemy) and Pydantic — means you get both ORM behavior and Pydantic validation in one class. When you call `Ticket.model_validate(ticket_in)`, Pydantic validates and coerces the input data, then SQLAlchemy tracks the resulting object for persistence. When FastAPI serializes the `Ticket` instance returned from an endpoint into JSON, Pydantic handles the serialization. This dual behavior is what makes SQLModel the right choice for FastAPI projects: the alternative — separate SQLAlchemy `DeclarativeBase` models and Pydantic schemas — requires maintaining two parallel class hierarchies and writing conversion logic between them.

## Session Lifecycle and the Transaction Model

The database session is the most important concept to understand in Session 2. A `Session` in SQLAlchemy (and SQLModel) is a unit of work. It maintains an identity map — a registry of all Python objects that have been loaded from or staged for the database within that session. When you call `db.add(ticket)`, SQLAlchemy places the `Ticket` object into the identity map and marks it as "pending." No SQL is executed. When you call `db.commit()`, SQLAlchemy flushes all pending objects: it issues `BEGIN`, sends the `INSERT` or `UPDATE` statements, and issues `COMMIT`. After commit, the Python object's in-memory state may be out of sync with the database — for example, the database assigned `id = 42` during the `INSERT`, but the Python object still has `id = None`. `db.refresh(ticket)` issues a `SELECT WHERE id = 42` and updates the Python object with the database's current state. This three-step sequence — `add`, `commit`, `refresh` — is the canonical pattern for creating or updating records in SQLModel/SQLAlchemy.

The session lifecycle in FastAPI is managed by the `get_session` generator dependency. The generator runs up to the `yield`, hands the session to FastAPI, which injects it into the endpoint. After the endpoint function returns (normally or by exception), FastAPI resumes the generator past the `yield`, triggering the `with Session(engine) as session:` block's `__exit__`. If no commit was issued and an exception was raised, `__exit__` issues a `ROLLBACK`. This behavior means exceptions are automatically safe — a failed endpoint will never leave the database in a partially-written state. If a commit was already issued before the exception (not typical in these endpoints), the committed data persists and the exception propagates as expected.

## SQLite vs PostgreSQL: Making the Right Production Decision

SQLite is the correct database for Session 2 because it eliminates setup friction and lets us focus on the SQLModel patterns. Its file-based nature is both its strength and its limitation. A single-process FastAPI server with low write concurrency runs perfectly on SQLite — reads are fast, writes are transactional, and the database is portable (copy the `.db` file, copy the database). The limitation appears at scale: SQLite uses a writer lock on the entire database file. If two requests try to write simultaneously (e.g., two concurrent `POST /tickets` calls with multiple uvicorn workers), the second writer will receive `OperationalError: database is locked`. In a production deployment with `uvicorn --workers 4`, this is a real failure mode. The migration to PostgreSQL requires changing exactly one line — the `DATABASE_URL` — plus installing `psycopg2-binary` and configuring a connection pool. SQLModel's abstraction makes this migration trivially easy from a code perspective. The operational complexity (managing a Postgres server, connection strings, credentials) is the real migration cost.

---

# What Students Should Understand

1. The in-memory list from Session 1 is lost on every server restart. The SQLite database persists to disk. This is the fundamental reason to add a database layer.

2. `table=True` in `class Ticket(SQLModel, table=True)` is the flag that registers the class as a database table. Without it, the class is a pure Pydantic model with no database representation.

3. `id: Optional[int] = Field(default=None, primary_key=True)` — the `Optional[int]` is required because the ID does not exist before the row is inserted. SQLite assigns it on `INSERT`. `db.refresh()` reads it back into the Python object.

4. The three-step ORM write pattern: `db.add(obj)` stages, `db.commit()` persists to disk, `db.refresh(obj)` syncs the Python object with the database-assigned values. Skipping `commit()` means the data is never written. Skipping `refresh()` means the response object may have stale or `None` fields.

5. `Depends(get_session)` is FastAPI's dependency injection mechanism. It creates a fresh `Session` per request, yields it to the endpoint, and closes it after the response is sent. Never use a global session shared across requests.

6. `db.get(Ticket, ticket_id)` returns `None` if the row does not exist. Every endpoint that uses a path parameter `ticket_id` must guard with `if not ticket: raise HTTPException(status_code=404)`.

7. `model_dump(exclude_unset=True)` in the PUT endpoint returns only the fields the client explicitly sent. Without this, unset optional fields are included as `None`, overwriting existing data in the database.

8. `SQLModel.metadata.create_all(engine)` is idempotent — safe to call on every startup. It creates tables that do not exist and leaves existing tables untouched. It cannot alter existing tables (add/remove columns).

9. SQLite is correct for development and single-process deployments. PostgreSQL is required for multi-worker production deployments where concurrent writes are expected.

10. The database layer enables all future sessions: Session 3 (User table, FK from tickets to users), Session 4 (write LLM classification results back to ticket rows), Session 5 (use ticket IDs as ChromaDB document IDs).

---

# Interview-Ready Explanation

```text
In Session 2 I replaced the in-memory Python list from Session 1 with a persistent SQLite database using SQLModel as the ORM. I defined a Ticket class with table=True that serves as both the SQLAlchemy table and the Pydantic validation model — one class for both the database schema and the API contract. I added a get_session dependency function that FastAPI injects into each endpoint via Depends(), creating an isolated session per request that is automatically closed after the response is sent. All 5 CRUD endpoints now use proper ORM operations — add, commit, refresh, get, exec, delete — and data survives server restarts, which is the minimum requirement for any production backend.
```

---

# What Happens When POST /tickets Is Called

```text
1. FastAPI receives the HTTP POST request with a JSON body.
2. The TicketCreate Pydantic model validates and deserializes the body. If required fields are missing or types are wrong, FastAPI returns 422 before the endpoint runs.
3. FastAPI calls get_session(), opens a Session(engine) context manager, and injects the session into the endpoint as `db`.
4. Ticket.model_validate(ticket_in) creates a Ticket SQLModel instance from the validated input. At this point, id is None, created_at and updated_at are set by default_factory=datetime.utcnow.
5. db.add(db_ticket) places the Ticket object into the session's identity map as a pending INSERT. No SQL has been sent to the database yet.
6. db.commit() flushes the pending INSERT to SQLite: executes "INSERT INTO ticket (title, description, status, priority, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)" and commits the transaction to disk.
7. db.refresh(db_ticket) issues "SELECT * FROM ticket WHERE id = ?" using the newly assigned primary key, and updates the db_ticket Python object with the database-assigned id and any server-side values.
8. The endpoint returns db_ticket. FastAPI serializes it using the TicketResponse schema and returns HTTP 201 with the JSON body including the assigned integer id.
9. After the response is sent, FastAPI resumes the get_session() generator past the yield, triggering the Session context manager's __exit__, which closes the connection.
```

---

# What AI Was Used For + What Engineers Must Still Do

## What AI Generated in Session 2

- The `Ticket` SQLModel class with correct field types and `Field()` definitions
- The `database.py` file with engine, `create_db_and_tables()`, and `get_session()` generator
- The refactored endpoints with ORM operations replacing list operations
- The startup event handler calling `create_db_and_tables()`
- The `exclude_unset=True` PUT pattern with the `setattr` loop
- The 404 guard pattern for endpoints that accept a `ticket_id`

## What Engineers Must Still Do

- Verify that `tickets.db` is actually created after startup (check the file exists in the project root)
- Verify data persistence: restart uvicorn and confirm GET /tickets returns previously created tickets
- Verify each endpoint returns the correct HTTP status code (201, 200, 204, 404)
- Confirm the PUT endpoint does NOT overwrite unset fields with None (test by updating only `status` and checking that `title` is unchanged)
- Add `tickets.db` to `.gitignore` so the database file is not committed to version control
- Understand why `connect_args={"check_same_thread": False}` is needed for SQLite with FastAPI's threaded request handling
- Be able to explain the difference between `db.commit()` and `db.refresh()` without reading the code
- Know when to switch from SQLite to PostgreSQL and what the migration requires
- Be able to write pytest tests that override `get_session` to use an in-memory database for test isolation

---

# Common Issues and Fixes

## Issue 1: Ticket appears in POST response but GET /tickets/{id} returns 404

Error observed: POST /tickets returns 201 with `{"id": 1, "title": "...", ...}` but GET /tickets/1 returns `{"detail": "Ticket not found"}`.

Root cause: `db.commit()` was not called before `db.refresh()`. SQLAlchemy generates a placeholder identity for the object in the session's identity map (so `id` appears non-None in the response), but the row was never written to disk. After the session closes, the row does not exist in the database.

What to ask AI:

```text
My POST /tickets endpoint returns a 201 response with an id field, but when I call GET /tickets/{id} with that same id I get 404. My endpoint code is:

    db_ticket = Ticket.model_validate(ticket)
    db.add(db_ticket)
    db.refresh(db_ticket)
    return db_ticket

Identify the exact bug, explain why the 201 response shows an id despite the bug, and show the corrected endpoint. Explain in 2-3 sentences what db.commit() does at the SQL level and why it is required before db.refresh().
```

## Issue 2: `sqlalchemy.exc.OperationalError: no such table: ticket`

Error observed: On the first request after starting the server, any endpoint returns 500 with `OperationalError: no such table: ticket`.

Root cause: `create_db_and_tables()` was not called at startup, or it was called before the `Ticket` class was imported, so `SQLModel.metadata` did not include the `Ticket` table when `create_all` ran.

What to ask AI:

```text
I am getting "sqlalchemy.exc.OperationalError: no such table: ticket" on every request. My database.py creates the engine and defines create_db_and_tables() which calls SQLModel.metadata.create_all(engine). My main.py has a startup event. Show me the correct import order and startup handler to ensure the Ticket table is created before any endpoint is called. The Ticket model is defined in app/models.py.
```

## Issue 3: PUT /tickets/{id} overwrites title and description with None

Error observed: PUT /tickets/1 with body `{"status": "in_progress"}` returns 200 but the title and description fields in the response are now null or empty.

Root cause: The update endpoint is using `model_dump()` without `exclude_unset=True`. The `TicketUpdate` model has all fields as `Optional` with `None` defaults, so `model_dump()` returns `{"title": None, "description": None, "status": "in_progress", "priority": None}`. The `setattr` loop then sets `ticket.title = None`.

What to ask AI:

```text
My PUT /tickets/{id} endpoint is overwriting existing title and description fields with None when the client only sends {"status": "in_progress"}. My update handler uses:

    ticket_data = ticket_update.model_dump()
    for key, value in ticket_data.items():
        setattr(ticket, key, value)

Fix this so that only the fields explicitly provided in the request body are updated. The existing title and description should remain unchanged. Explain what exclude_unset=True does at the Pydantic level.
```

---

# Key Takeaways

1. **Persistence is not optional.** In-memory state is destroyed on every process restart. Any real backend must store state in a durable medium — a relational database, an object store, or at minimum a filesystem — that exists independently of the application process. Session 2 makes the AI Support Copilot backend production-credible for the first time.

2. **SQLModel is the right ORM for FastAPI projects at this scale.** The dual Pydantic + SQLAlchemy inheritance means one class definition drives both the database schema and the API contract. This eliminates the duplication of maintaining separate SQLAlchemy models and Pydantic schemas. The trade-off — less control over SQL generation — is acceptable for standard CRUD operations. For complex analytical queries, you would use SQLAlchemy Core expressions or raw `text()`.

3. **The session lifecycle (add → commit → refresh) is a testable, explainable unit.** Students must be able to state, without code reference, what SQL operation each step triggers and what happens if a step is omitted. This is a standard backend interview question and a real source of production bugs when missed.

4. **The architecture decision made in Session 2 has downstream consequences.** The choice of SQLite vs PostgreSQL, synchronous vs async sessions, `create_all` vs Alembic — these decisions are not permanent, but they carry cost to change later. Knowing when and why to change each is as important as knowing how to implement the initial choice.

---

# Session 3 Preview

In Session 3, we will add JWT-based authentication and role-based access control.

We will add:

- A `User` SQLModel table with `id`, `email`, `hashed_password`, `role` (admin vs user)
- A `POST /auth/register` endpoint to create users
- A `POST /auth/login` endpoint that validates credentials and returns a signed JWT access token
- `OAuth2PasswordBearer` and a `get_current_user` dependency that decodes the JWT on every protected request
- Protected ticket endpoints: only authenticated users can create or modify tickets
- Role-based guard: only admins can delete tickets

The database layer from Session 2 is what makes this possible — the `User` table will be a new SQLModel table in the same SQLite database, and tickets will have a `user_id` foreign key linking each ticket to its creator.

The session lifecycle pattern, the dependency injection pattern, and the `create_all` startup pattern all stay the same in Session 3. We are adding one new table and a new authentication middleware layer on top of the existing architecture.
