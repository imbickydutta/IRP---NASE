# Session 3 Student Pre-Session File: Add Auth + Role-Based Access

## What We Are Building

Across 8 sessions, we are building one continuous production-grade project:

# AI Support Ticket Resolution Copilot

A backend API that allows users to submit support tickets, which are automatically classified by an LLM, matched against a knowledge base using semantic search, and resolved by a LangGraph-powered agent.

By the end of all sessions, the system will:

- accept ticket submissions from authenticated users
- store tickets in a relational database
- classify ticket category and priority using an OpenAI LLM call
- search for similar past resolutions using embeddings + ChromaDB
- suggest resolutions via RAG (Retrieval-Augmented Generation)
- route complex tickets through a LangGraph resolution agent
- expose a fully protected API with JWT-based auth and role-based access control

## Session 3 Goal

In Session 3, we are adding the authentication and authorization layer.

Right now, our API from Session 2 is completely open — any HTTP client can create, read, update, or delete any ticket. We will close that gap today.

By the end of Session 3, the API will:

- allow users to sign up and log in with email and password
- issue a signed JWT token on successful login
- require a valid JWT on every ticket endpoint
- return only the requesting user's own tickets (for regular users)
- allow admin users to view all tickets and update any ticket status
- reject unauthenticated requests with 401 and unauthorized actions with 403

## Session 3 Output

At the end of this session you should have:

1. A `User` SQLModel table in your SQLite database with email, hashed_password, and role
2. `POST /auth/signup` and `POST /auth/login` endpoints working in Swagger
3. A valid JWT returned by the login endpoint
4. All ticket endpoints returning 401 when called without a token
5. `PATCH /tickets/{id}` returning 403 for non-admin users
6. pytest tests passing for signup, login, and protected route access

---

# Pre-Read

## Why Are We Adding This Feature at This Point in the Build?

We have a working database-backed API. Before we add AI features — the LLM classifier, the embedding search, the LangGraph agent — we need to know who is using the API. Every future feature will depend on the user context:

- The LLM classifier needs to tag a ticket with the owner's user_id
- The RAG search results may be scoped per user or per role
- The LangGraph agent will operate on behalf of an authenticated user
- The admin dashboard (Session 8) needs admin-only routes to be enforced from the start

Adding auth now means every feature we add in Sessions 4–8 is already secured. Adding auth at the end means retrofitting security into every route — which is error-prone and expensive.

## System Architecture Flow (Sessions 1–3 and Beyond)

```
HTTP Request (JSON body + Authorization: Bearer <token>)
  ↓
FastAPI Router (app/main.py)
  ↓
Auth Middleware / Depends(get_current_user)     ← SESSION 3 ADDS THIS
  ↓ (401 if token missing/invalid)
  ↓ (403 if role insufficient)
  ↓
Route Handler (app/routes/tickets.py or auth.py)
  ↓
SQLModel Session (app/database.py) → SQLite DB  ← SESSION 2 ADDED THIS
  ↓
[SESSION 4 WILL ADD: OpenAI API call for ticket classification]
  ↓
[SESSION 5 WILL ADD: Embedding generation + ChromaDB vector search]
  ↓
[SESSION 6 WILL ADD: RAG resolution suggestion via LangChain]
  ↓
[SESSION 7 WILL ADD: LangGraph agent for complex resolution routing]
  ↓
HTTP Response (JSON)
```

## Key Concepts to Revise Before Session

Revise these before class. You should be able to explain each at a code level, not just a definition level.

### 1. HTTP Status Codes: 200, 201, 400, 401, 403, 404, 422

401 and 403 are both "you can't do this" but they mean different things. Know which one to use and when.

### 2. FastAPI Dependency Injection — Depends()

You used `Depends(get_db)` in Session 2 to inject a database session into your route handlers. Auth dependencies follow the same pattern. Know how `Depends()` composes: a route can have a dependency that itself has a dependency.

### 3. Pydantic BaseModel for Request/Response Schemas

You have used Pydantic models for ticket schemas. The signup and login request bodies will also be Pydantic models. Understand how `response_model` excludes fields like `hashed_password` from responses.

### 4. Python-jose — JWT encoding/decoding

JWT has three parts: header, payload (claims), and signature. The `iat`, `exp`, and `sub` claims are standard. `jwt.encode()` creates a token; `jwt.decode()` verifies and returns the payload. `JWTError` is raised for any verification failure.

### 5. passlib — CryptContext and bcrypt

`CryptContext(schemes=["bcrypt"])` gives you `hash()` and `verify()` methods. `verify(plain, hashed)` runs the hash and compares in constant time. The salt is automatically embedded in the bcrypt hash string itself.

### 6. OAuth2PasswordBearer

FastAPI's built-in scheme for extracting Bearer tokens from the `Authorization` header. Declare it at module level: `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")`. It raises 401 automatically if the header is absent.

### 7. SQLModel Relationships and Foreign Keys

The `Ticket` model will need an `owner_id: int = Field(foreign_key="user.id")` field added. Understand how SQLModel/SQLAlchemy handles foreign key constraints at the database level.

### 8. Environment Variables and python-dotenv

Your `SECRET_KEY` must not be hardcoded in source code. Use `os.getenv("SECRET_KEY")` and load from a `.env` file via `python-dotenv`. Know why this matters for version control and deployment security.

## Technical Explanation

A request to a protected FastAPI endpoint goes through the dependency graph before the route handler executes. When `get_current_user` is declared as a dependency, FastAPI calls it first. It uses `OAuth2PasswordBearer` to extract the token string from the `Authorization` header, then calls `jwt.decode()` with the server's SECRET_KEY and the expected algorithm. If the token signature is invalid or the token is expired, `python-jose` raises a `JWTError`. The dependency catches this and raises `HTTPException(status_code=401)` — the route handler never runs.

If the token is valid, the `sub` claim is extracted. This is the user's id as a string. A database query fetches the User record. The User object is returned from the dependency and injected into the route handler as `current_user`. The route handler can then use `current_user.id` and `current_user.role` to apply business logic — filter tickets, check permissions, set owner_id.

---

# Prerequisites: Setup Before Session

## Python Packages to Install

Activate your existing project virtualenv, then run:

```bash
pip install "python-jose[cryptography]" "passlib[bcrypt]" python-dotenv
```

Add these to your `requirements.txt`:

```
python-jose[cryptography]
passlib[bcrypt]
python-dotenv
```

## Environment Setup

Create a `.env` file in your project root (same level as `main.py` or the `app/` directory):

```
SECRET_KEY=your-very-long-random-secret-key-here-do-not-commit-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a strong SECRET_KEY with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Add `.env` to your `.gitignore`. Never commit it.

## Code State from Session 2

Your project should currently look like this:

```
app/
  __init__.py
  main.py               — FastAPI app, includes tickets router
  models.py             — Ticket(SQLModel, table=True): id, title, description, status, created_at
  database.py           — engine, SQLite, get_db Depends
  routes/
    __init__.py
    tickets.py          — GET /tickets, POST /tickets, GET /tickets/{id},
                          PATCH /tickets/{id}, DELETE /tickets/{id}
tests/
  test_tickets.py       — pytest tests using TestClient and in-memory SQLite
.env                    — (create this now if it does not exist)
requirements.txt
```

If your codebase from Session 2 does not match this structure, fix it before the session.

## Content to Prepare Before Class

Have the following ready in a text file or clipboard before class:

```
Test user credentials to use during Swagger testing:

Regular user:
  email: testuser@example.com
  password: TestPass123!

Admin user:
  email: admin@example.com
  password: AdminPass456!

(You will create both via POST /auth/signup during class,
then manually update the admin user's role in the DB or via a seeder script.)
```

---

# Prompts for Session 3

Use these prompts during the session when instructed. All prompts are written for Claude Code or Cursor AI.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Support Ticket Resolution Copilot using FastAPI and SQLModel.

Current codebase state after Session 2:
- app/main.py: FastAPI app instance, includes the tickets router with prefix "/tickets"
- app/models.py: Ticket SQLModel table with fields: id (int, primary key), title (str), description (str), status (str, default "open"), created_at (datetime, default utcnow)
- app/database.py: SQLite engine pointed at "tickets.db", SQLModel.metadata.create_all, get_db dependency yielded from Session
- app/routes/tickets.py: All 5 CRUD endpoints — GET /tickets, POST /tickets, GET /tickets/{id}, PATCH /tickets/{id}, DELETE /tickets/{id} — all using SQLModel session via Depends(get_db)
- requirements.txt: fastapi, uvicorn, sqlmodel, pytest, httpx

Task: Add JWT-based authentication and role-based access control.

Add the following — follow this exact file structure:

1. app/models.py — Add a User SQLModel table with fields:
   - id: int (primary key, auto-increment)
   - email: str (unique index)
   - hashed_password: str
   - role: str (default "user")
   Also add owner_id: Optional[int] = Field(default=None, foreign_key="user.id") to the Ticket model.

2. app/auth/__init__.py — empty file

3. app/auth/utils.py — Password hashing utilities:
   - Import: from passlib.context import CryptContext
   - pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
   - def hash_password(password: str) -> str
   - def verify_password(plain: str, hashed: str) -> bool

4. app/auth/jwt.py — JWT token logic:
   - Read SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES from environment variables using os.getenv
   - def create_access_token(data: dict) -> str: encode with exp claim added, algorithm=ALGORITHM
   - def decode_access_token(token: str) -> dict: decode, raise HTTPException 401 on JWTError

5. app/auth/dependencies.py — FastAPI auth dependencies:
   - oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
   - async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
       decode token, get user_id from "sub" claim, query DB, raise 401 if user not found
   - async def require_admin(current_user: User = Depends(get_current_user)) -> User:
       raise HTTPException 403 if current_user.role != "admin", else return current_user

6. app/routes/auth.py — Auth endpoints:
   - POST /auth/signup: accept SignupRequest(email, password), check for duplicate email (raise 400 if exists), hash password, create User, return UserResponse (id, email, role — no hashed_password), status 201
   - POST /auth/login: accept LoginRequest(email, password) as JSON body (NOT OAuth2PasswordRequestForm), query user by email, verify password (raise 401 with message "Incorrect email or password" for both wrong email and wrong password), call create_access_token({"sub": str(user.id), "role": user.role}), return {"access_token": token, "token_type": "bearer"}, status 200

7. app/routes/tickets.py — Update existing routes:
   - All endpoints: add current_user: User = Depends(get_current_user) to function signature
   - POST /tickets: set ticket.owner_id = current_user.id before saving
   - GET /tickets: if current_user.role == "admin", return all tickets; else return only tickets where owner_id == current_user.id
   - GET /tickets/{id}: return 403 if ticket.owner_id != current_user.id and current_user.role != "admin"
   - PATCH /tickets/{id}: add _: User = Depends(require_admin) — admin only
   - DELETE /tickets/{id}: allow only if ticket.owner_id == current_user.id or current_user.role == "admin"

8. app/main.py — Register the auth router:
   - from app.routes.auth import router as auth_router
   - app.include_router(auth_router, prefix="/auth", tags=["auth"])

9. Pydantic schemas (can be in app/schemas.py or inline in the route file):
   - SignupRequest: email: EmailStr, password: str (min length 8)
   - LoginRequest: email: EmailStr, password: str
   - UserResponse: id: int, email: str, role: str (Config orm_mode = True or model_config)
   - TokenResponse: access_token: str, token_type: str

Constraints:
- Do NOT add refresh tokens, token revocation, OAuth2 social login, email verification, forgot-password, sessions, cookies, or rate limiting
- Do NOT use OAuth2PasswordRequestForm — use a Pydantic JSON body for login
- Do NOT use Alembic migrations — use SQLModel.metadata.create_all(engine) only
- Do NOT add any LLM calls, embeddings, or AI features — this session is auth only
- Load SECRET_KEY from environment variable using os.getenv, never hardcode it
- Add comments on every non-trivial function explaining what it does and why

Use: fastapi, sqlmodel, python-jose[cryptography], passlib[bcrypt], python-dotenv, pydantic[email]
Python version: 3.11+
```

---

## Prompt 2: Improvement Prompt

```text
Review the auth implementation just generated and apply these improvements:

1. In app/auth/dependencies.py, add a credentials_exception variable at module level:
   credentials_exception = HTTPException(
       status_code=status.HTTP_401_UNAUTHORIZED,
       detail="Could not validate credentials",
       headers={"WWW-Authenticate": "Bearer"},
   )
   Use this exception consistently everywhere instead of inline HTTPException calls in the auth module.

2. In app/routes/auth.py, add response_model=UserResponse to the signup endpoint so the hashed_password field is never accidentally serialized in any response.

3. In app/auth/jwt.py, wrap the os.getenv calls with a startup validation: if SECRET_KEY is None or len(SECRET_KEY) < 32, raise a RuntimeError at import time with a clear message. This prevents silent misconfiguration.

4. In app/routes/tickets.py GET /tickets, refactor the filter logic to use SQLModel's select().where() cleanly:
   - For admin: session.exec(select(Ticket)).all()
   - For regular user: session.exec(select(Ticket).where(Ticket.owner_id == current_user.id)).all()

5. In app/schemas.py, add a validator on SignupRequest.password that raises a ValueError if the password is less than 8 characters or contains no digit. Use a @field_validator (Pydantic v2) or @validator (Pydantic v1) depending on the installed version.

6. In app/routes/auth.py signup handler, use a single DB round-trip to check existence and create the user using a try/except on IntegrityError rather than a separate SELECT before INSERT — this prevents a race condition on concurrent signups.

Do not change any route paths, response structures, or dependency names. Apply only the improvements listed above and add a brief inline comment for each change.
```

---

## Prompt 3: Debugging Prompt — JWT Decode Error and 422 on Login

```text
I am hitting two bugs in my FastAPI auth implementation. Help me diagnose and fix both.

Bug 1: POST /auth/login returns 422 Unprocessable Entity
  - I am sending: {"email": "user@test.com", "password": "secret123"} as JSON in the request body via Swagger or httpx
  - The server returns 422 with a validation error
  - My login route handler signature is: async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db))
  - Diagnosis: OAuth2PasswordRequestForm expects application/x-www-form-urlencoded, not JSON
  - Fix: Replace OAuth2PasswordRequestForm with a Pydantic model: class LoginRequest(BaseModel): email: EmailStr; password: str
  - Update the handler signature to: async def login(request: LoginRequest, db: Session = Depends(get_db))

Bug 2: GET /tickets returns 401 "Could not validate credentials" even with a valid token
  - I just logged in and received an access_token
  - I set Authorization: Bearer <token> in the header
  - The server still returns 401
  - Possible causes to check in order:
    1. Print the decoded payload in get_current_user — is the "sub" claim present?
    2. Was the token created with create_access_token({"sub": str(user.id)}) — sub must be a string
    3. Is SECRET_KEY the same value at token creation time and decode time? Print os.getenv("SECRET_KEY") in both jwt.py functions
    4. Is the ALGORITHM consistent — "HS256" in both encode and decode calls?
    5. Is the token being passed with the "Bearer " prefix? Swagger adds it automatically; curl/httpx requires it explicitly
  - Fix each cause found and explain what was wrong

After fixing both bugs, show the corrected code for login route handler and get_current_user dependency.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the auth implementation in this FastAPI project at an interview-preparation level.

I want to understand the following — use correct technical terminology, assume I know Python and FastAPI:

1. What is the full lifecycle of a POST /auth/login request? Trace it from the HTTP request arriving at FastAPI to the JWT being returned in the response. Include: route matching, Pydantic validation, DB query, passlib verify, jwt.encode, response serialization.

2. What is inside the JWT token we generate? Explain the header, payload claims (sub, role, exp, iat), and signature. What is the difference between encoding and encryption in this context?

3. How does get_current_user work as a FastAPI dependency? Why does it raise HTTPException instead of returning None when the token is invalid?

4. What is the exact chain of function calls when a request hits GET /tickets? Show the dependency resolution order: get_db → get_current_user → route handler.

5. Why does PATCH /tickets/{id} have two dependencies — get_current_user (via require_admin) and get_db? Could we consolidate them? What are the trade-offs?

6. What would break if we stored the user's role in the DB and looked it up on every request instead of embedding it in the JWT?

7. What is the difference between the 401 and 403 responses in this codebase? Which dependency raises each one?

Do not rewrite the code. Only explain it.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Help me prepare to explain the Session 3 auth feature in a backend engineering interview.

Structure the explanation as follows:

1. What problem does this feature solve? (2-3 sentences — business and technical context)

2. What did you build? (list the components: User model, auth routes, JWT utils, dependencies)

3. How does JWT authentication work in your implementation? (explain the flow: login → token → protected request → dependency → route handler)

4. How does role-based access control work? (explain the difference between authentication and authorization, how the role is stored, how it is checked)

5. What are the security decisions you made and why? (password hashing algorithm, error message vagueness on login, JWT statelessness trade-off, SECRET_KEY from environment)

6. What are the limitations of this implementation? (no refresh tokens, no token revocation, role staleness if changed after token issue)

7. What would you add if this were going to production? (refresh tokens, Redis blocklist, rate limiting, audit logs)

Keep the explanation technically precise. I should be able to say this in 3-4 minutes in an interview.
```

---

## Prompt 6: Unit Test Generation Prompt

```text
Generate pytest tests for the Session 3 auth feature in this FastAPI project.

Project structure:
- app/main.py: FastAPI app
- app/database.py: get_db dependency, SQLite engine
- app/models.py: User, Ticket SQLModel tables
- app/routes/auth.py: POST /auth/signup, POST /auth/login
- app/routes/tickets.py: GET /tickets, POST /tickets, PATCH /tickets/{id} — all protected

Write tests in tests/test_auth.py using pytest and FastAPI's TestClient.

Use a test database fixture that:
- creates an in-memory SQLite database for tests (not the real tickets.db)
- overrides the get_db dependency using app.dependency_overrides
- creates all tables using SQLModel.metadata.create_all
- tears down after each test

Write the following test functions:

1. test_signup_success: POST /auth/signup with valid email and password → expect 201, response has id, email, role="user", no hashed_password field

2. test_signup_duplicate_email: call signup twice with same email → second call expects 400 "Email already registered"

3. test_login_success: create user via signup, then POST /auth/login → expect 200, response has access_token and token_type="bearer"

4. test_login_wrong_password: create user, login with wrong password → expect 401

5. test_login_nonexistent_email: POST /auth/login with email that was never signed up → expect 401

6. test_get_tickets_unauthenticated: GET /tickets with no Authorization header → expect 401

7. test_get_tickets_authenticated: signup, login, create a ticket, GET /tickets → expect 200, only own ticket returned

8. test_patch_ticket_as_regular_user: signup, login, create ticket, PATCH /tickets/{id} → expect 403

9. test_patch_ticket_as_admin: create an admin user directly (insert into DB with role="admin"), login as admin, create ticket, PATCH /tickets/{id} with {"status": "closed"} → expect 200

10. test_expired_token: generate a token with exp in the past using create_access_token directly, use it on GET /tickets → expect 401

Include helper functions: create_test_user(db, email, password, role="user") and get_auth_headers(client, email, password) → {"Authorization": "Bearer <token>"}.

Do not use mocking for the database — use the real in-memory SQLite with dependency override.
```

---

## Prompt 7: Edge Case and Error State Prompt

```text
Review the current auth implementation and add proper handling for these edge cases and error states:

1. POST /auth/signup with a password shorter than 8 characters → return 422 with message "Password must be at least 8 characters"

2. POST /auth/signup with an invalid email format (e.g., "notanemail") → return 422, Pydantic's EmailStr validator handles this automatically — confirm it is working

3. POST /auth/login with a valid email that belongs to a user whose record was deleted from the DB after the token was issued → get_current_user should raise 401 "User not found" rather than returning None or crashing with AttributeError

4. GET /tickets/{id} where the ticket exists but belongs to a different user and the requester is not admin → return 403 "Access denied", not 404 (do not reveal whether the ticket exists to unauthorized users — this prevents resource enumeration)

5. PATCH /tickets/{id} with an invalid status value (e.g., status="invalid_value") → return 422 with a clear validation error. Add a Pydantic validator or a Literal type constraint: status: Literal["open", "in_progress", "closed"]

6. Any protected route called with a JWT signed by a different SECRET_KEY (e.g., token from a different environment) → ensure 401 is returned, not 500. The JWTError must be caught in decode_access_token.

7. Token where the "sub" claim is not a valid integer (e.g., sub="notanumber") → get_current_user must catch ValueError when calling int(payload["sub"]) and raise 401, not 500.

For each case: show the current behavior, explain the fix, and show the corrected code snippet.
```

---

# What You Should Be Able to Explain After Session 3

By the end of the session, you should be able to answer these questions without looking at notes:

1. What is the difference between authentication and authorization? Give a specific example from your API for each.

2. What does a JWT contain? What are the header, payload, and signature, and what is the role of each?

3. Why do we use bcrypt instead of SHA-256 for password hashing?

4. What is the `sub` claim in your JWT payload, and why is it a string rather than an integer?

5. What happens when a request arrives at `GET /tickets` — trace the full dependency chain before the route handler executes.

6. Why does `POST /auth/login` return the same error message for "email not found" and "wrong password"?

7. What is the difference between a 401 and a 403 HTTP response? When does each appear in your API?

8. What would happen if the SECRET_KEY was changed on the server after users had already logged in?

9. Why is the JWT payload not encrypted? What should you never put in a JWT claim?

10. What is the trade-off of embedding the user's role in the JWT instead of fetching it from the database on every request?

---

## Final Session 3 Explanation

```text
In Session 3, I added JWT-based authentication and role-based access control to the support ticket API. Users sign up with email and password — the password is hashed with bcrypt and stored in a User table. On login, the server verifies the password against the hash and issues a signed JWT containing the user's id and role. All ticket endpoints are protected by a FastAPI dependency that decodes and verifies the JWT on every request. Regular users can only create and view their own tickets; admin users can view all tickets and update any ticket status via PATCH /tickets/{id}. Unauthenticated requests return 401; authenticated but unauthorized requests return 403.
```
