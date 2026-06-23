# Session 3 After-Session Notes: Add Auth + Role-Based Access

## What We Built Today

Today we added the authentication and authorization layer to the AI Support Ticket Resolution Copilot.

The components added:

- `User` SQLModel table — id, email, hashed_password, role (user/admin)
- `POST /auth/signup` — creates a new user, hashes password with bcrypt, returns user details (never returns hashed_password)
- `POST /auth/login` — verifies credentials, issues a signed JWT with sub (user_id), role, and exp claims
- `app/auth/utils.py` — `hash_password()` and `verify_password()` using passlib CryptContext with bcrypt scheme
- `app/auth/jwt.py` — `create_access_token()` and `decode_access_token()` using python-jose, SECRET_KEY from environment variable
- `app/auth/dependencies.py` — `get_current_user` dependency (extracts and validates JWT, returns User), `require_admin` dependency (checks role == "admin", raises 403 otherwise)
- Updated `app/routes/tickets.py` — all endpoints now require `Depends(get_current_user)`; GET /tickets filters by owner_id for regular users; PATCH /tickets/{id} requires `Depends(require_admin)`
- Updated `app/models.py` — Ticket model now has `owner_id` foreign key to the User table

The codebase now enforces: every request must prove identity (authentication), and every sensitive action must prove permission (authorization).

---

# Why This Feature Matters for Production Systems

Every API that handles user data requires a boundary between who can read and who can write. Without authentication, any HTTP client can access any resource. Without authorization, any authenticated user can access any other user's data. Both failures are common causes of data breaches and compliance violations.

In the support ticket context specifically: a company's ticket queue may contain sensitive customer information — account details, billing disputes, security incidents. Users must only see their own tickets. Support agents (admin role) must be able to see and update all tickets. If this boundary is missing, a malicious actor with network access to the API can read every customer's ticket history with a single GET request.

The auth pattern we built — JWT stateless tokens, bcrypt-hashed passwords, role-embedded claims, FastAPI dependency injection — is the industry-standard approach for Python API backends. Every backend engineering interview at companies using Python/FastAPI stacks will include questions on exactly these concepts. Understanding this implementation deeply is directly transferable.

---

# System Architecture Flow (Sessions 1 Through 3 and Forward)

```
HTTP Request (JSON body + optional Authorization: Bearer <token>)
  ↓
FastAPI Router — app/main.py
  ↓ (routes registered: /auth, /tickets)
  ↓
Auth Dependency Chain — app/auth/dependencies.py      ← SESSION 3
  OAuth2PasswordBearer extracts token from header
  ↓
  jwt.decode() verifies signature with SECRET_KEY
  ↓
  SELECT * FROM user WHERE id = <sub>
  ↓
  Returns User object OR raises 401/403
  ↓
Route Handler — app/routes/tickets.py or auth.py
  ↓
SQLModel DB Session — app/database.py                 ← SESSION 2
  SELECT/INSERT/UPDATE/PATCH on tickets or users table
  ↓
  SQLite (tickets.db)
  ↓

[SESSION 4 — LLM Classifier will add:]
  On POST /tickets → OpenAI API call → category + priority written to Ticket row

[SESSION 5 — Embeddings + ChromaDB will add:]
  On POST /tickets → embed ticket text → store in ChromaDB
  On GET /tickets/search → embed query → ChromaDB similarity search

[SESSION 6 — RAG will add:]
  LangChain retriever queries ChromaDB → augments prompt → OpenAI generates resolution suggestion

[SESSION 7 — LangGraph Agent will add:]
  Complex tickets routed through LangGraph graph → multi-step reasoning → structured resolution output

[SESSION 8 — Deployment will add:]
  Docker container, environment secrets via cloud provider, HTTPS, production DB

  ↓
HTTP Response (JSON)
```

---

# Technical Deep-Dive: Authentication vs Authorization, JWT, Password Hashing, Protected Routes

Authentication and authorization are frequently conflated but are distinct operations that happen at different points in the request lifecycle. Authentication is identity verification — "who are you?" It happens at `POST /auth/login` when the server checks the submitted password against the stored bcrypt hash and issues a JWT. Every subsequent request carries that JWT as proof of identity. The server re-verifies this proof on every request inside `get_current_user`. Authorization is permission checking — "what are you allowed to do?" It happens after authentication, inside route-specific logic or dedicated dependencies like `require_admin`. A request can fail authentication (401) without ever reaching the authorization check. A request can pass authentication and still fail authorization (403). Keeping these two as separate dependency functions is important for maintainability and testability.

JWT (JSON Web Token) is a compact, self-contained way to transmit claims between parties. A JWT has three dot-separated sections, each Base64url-encoded. The header specifies the signing algorithm (`{"alg": "HS256", "typ": "JWT"}`). The payload holds claims — in our implementation: `sub` (the user's id as a string, by convention the "subject" of the token), `role` (the user's role embedded at login time), `exp` (Unix timestamp after which the token is invalid), and `iat` (Unix timestamp of when the token was issued). The signature is `HMAC-SHA256(base64url(header) + "." + base64url(payload), SECRET_KEY)`. Because HMAC is a keyed hash, only the server holding `SECRET_KEY` can produce a valid signature. If an attacker modifies the payload (e.g., changes `"role": "user"` to `"role": "admin"`), the signature will no longer match the modified payload and `jwt.decode()` will raise `JWTError`. The payload is NOT encrypted — it is only encoded. Never put sensitive data (PII, tokens, secrets) in a JWT payload.

Password hashing with bcrypt works as follows: `passlib.CryptContext.hash(plain_password)` generates a random 16-byte salt, runs the bcrypt algorithm with a configurable cost factor (default 12), and returns a string like `$2b$12$<22-char-salt><31-char-hash>`. The salt is embedded in the output string. `CryptContext.verify(plain_password, stored_hash)` re-runs bcrypt with the salt extracted from `stored_hash` and compares the result in constant time (preventing timing attacks). Because the salt is random per hash, two users with identical passwords produce completely different stored hash strings. The cost factor means each hash computation takes approximately 100ms — trivial for legitimate logins but prohibitive for bulk brute-force attacks. The one-way nature means even a complete database leak does not immediately expose passwords. FastAPI's `Depends(get_current_user)` integrates auth cleanly with route handlers. `OAuth2PasswordBearer` is a FastAPI utility that reads the `Authorization: Bearer <token>` header and returns the raw token string. When declared as a dependency inside `get_current_user`, it automatically returns 401 if the header is absent — no manual header parsing needed.

---

# What Students Should Understand

After Session 3, students should be able to articulate:

1. Authentication is identity verification (login, token issuance). Authorization is permission checking (role guard, ownership filter). These are separate operations, implemented in separate dependency functions.

2. A JWT token contains a header (algorithm), payload (sub, role, exp, iat claims), and an HMAC signature. The signature prevents payload tampering but does NOT encrypt the payload — do not put sensitive data in claims.

3. bcrypt produces a salted, slow one-way hash. The salt prevents rainbow table attacks. The cost factor prevents brute-force attacks. `passlib.CryptContext` handles both automatically. You never reverse a bcrypt hash — you only verify against it.

4. `Depends(get_current_user)` runs before the route handler. If it raises an HTTPException, the route handler never executes. This is the correct FastAPI pattern for auth — not middleware, not manual header parsing in the handler.

5. A 401 response means the request failed authentication — no valid credentials were provided. A 403 response means the request passed authentication but the user lacks permission for the action.

6. `SECRET_KEY` must be a long random string stored in an environment variable. If it is hardcoded or committed to version control, any token can be forged with access to the key.

7. JWT is stateless — the server issues tokens but does not store them. This scales horizontally. The trade-off is that tokens cannot be individually revoked before expiry.

8. The `sub` claim holds the user's id (as a string). The `role` claim holds the user's role. Embedding role in the JWT avoids a DB query on every request but means role changes do not take effect until the current token expires.

9. The login endpoint must return the same error message for "email not found" and "wrong password." Different messages enable account enumeration attacks.

10. `owner_id` as a foreign key on the Ticket table is the database-level enforcement of ticket ownership. The application-level enforcement (filtering in GET /tickets) builds on top of this schema design.

---

# Interview-Ready Explanation

```text
In Session 3, I added JWT-based authentication and role-based access control to the support ticket API. Users register with email and password — the password is hashed with bcrypt using passlib before storage. On login, the server verifies the password against the stored hash and issues a signed JWT containing the user's id and role as claims. All ticket endpoints are protected by a FastAPI Depends() chain that decodes and verifies the JWT on every request — unauthenticated requests return 401, and requests from a user without admin role attempting to update ticket status return 403. The key design decision was embedding the user's role in the JWT token at login time to avoid a database lookup on every request, accepting the trade-off that role changes do not propagate until the current token expires.
```

---

# What Happens When POST /auth/login Is Called

```text
1. FastAPI matches POST /auth/login to the login route handler in app/routes/auth.py.

2. Pydantic deserializes and validates the JSON body as LoginRequest(email, password).
   If validation fails (missing field, invalid email format), FastAPI returns 422 before the handler runs.

3. Inside the handler: session.exec(select(User).where(User.email == request.email)).first()
   This runs: SELECT * FROM user WHERE email = 'submitted@email.com' LIMIT 1

4. If the user is not found (returns None): raise HTTPException(status_code=401, detail="Incorrect email or password")
   The same message is used whether the email does not exist or the password is wrong — intentional.

5. If user is found: verify_password(request.password, user.hashed_password)
   This calls pwd_context.verify() which re-runs bcrypt on the submitted password using the stored salt
   and compares in constant time. Returns True or False.

6. If verify returns False: raise HTTPException(status_code=401, detail="Incorrect email or password")

7. If verify returns True: create_access_token({"sub": str(user.id), "role": user.role})
   This calls jwt.encode({"sub": str(user.id), "role": user.role, "exp": now + timedelta(minutes=30)}, SECRET_KEY, algorithm="HS256")
   Returns a dot-separated JWT string: header.payload.signature

8. Return: {"access_token": token, "token_type": "bearer"} with HTTP 200

The client stores this token and sends it as Authorization: Bearer <token> on every subsequent request.
```

---

# What AI Was Used For + What Engineers Must Still Do

## What AI Was Used For

- Generating the full `app/auth/` module structure including utils, jwt, and dependencies files
- Writing the `CryptContext` setup, `hash_password`, and `verify_password` function bodies
- Writing the `create_access_token` and `decode_access_token` implementations with correct claim structure
- Writing the `get_current_user` and `require_admin` dependency function bodies
- Writing the signup and login route handlers with Pydantic schemas
- Updating the tickets router to add `Depends(get_current_user)` to all endpoints
- Generating the pytest test stubs for signup, login, and protected routes

## What Engineers Must Still Do

- Verify that `SECRET_KEY` is never hardcoded and is loaded from environment — AI sometimes generates hardcoded fallback values that are insecure
- Confirm that `hashed_password` is excluded from all response models — AI may accidentally include it in UserResponse
- Test the 401 vs 403 scenarios explicitly in Swagger — AI does not test your running server
- Confirm the error message is identical for "email not found" and "wrong password" — AI may generate two different messages
- Verify the GET /tickets filter is actually applied — run as a regular user and confirm you cannot see another user's tickets
- Confirm the DB schema change (owner_id foreign key on Ticket) was applied — delete tickets.db and restart to recreate if needed
- Understand every decision: algorithm choice, claim structure, dependency chain — you must explain these in interviews
- Write and run the pytest tests — AI generates stubs but you must confirm they pass on your actual implementation

---

# Common Issues and Fixes

## Issue 1: POST /auth/login returns 422 Unprocessable Entity

Error in terminal:
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for OAuth2PasswordRequestForm
  username: Field required
```

Root cause: The login handler is using `OAuth2PasswordRequestForm = Depends()` which expects `application/x-www-form-urlencoded` data, but the client is sending a JSON body. Swagger's "Try it out" may also send form data by default for this form type.

Fix: Replace `OAuth2PasswordRequestForm` with a Pydantic model:

```python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

async def login(request: LoginRequest, db: Session = Depends(get_db)):
    ...
```

What to ask AI:

```text
My POST /auth/login returns 422. I am sending {"email": "...", "password": "..."} as JSON.
The handler currently uses OAuth2PasswordRequestForm. Replace it with a Pydantic LoginRequest
model that accepts email and password as JSON. Show the updated handler signature and the
LoginRequest class definition.
```

---

## Issue 2: All requests return 401 even with a valid token

Error in Swagger: `{"detail": "Could not validate credentials"}`

Root cause (most common): Token was created with a different `SECRET_KEY` than the one currently loaded in `app/auth/jwt.py`. This happens when the `.env` file is missing, when `python-dotenv` was not loaded before `os.getenv`, or when the environment variable is set differently in the shell vs `.env`.

Fix steps:
1. Add `print(os.getenv("SECRET_KEY"))` in `decode_access_token` temporarily
2. Add `print(os.getenv("SECRET_KEY"))` in `create_access_token` temporarily
3. Confirm they print the same value
4. Confirm `load_dotenv()` is called at the top of `app/auth/jwt.py` or in `app/main.py` before any module imports that use the env var

What to ask AI:

```text
My GET /tickets returns 401 even when I provide a valid Bearer token from POST /auth/login.
My jwt.py uses os.getenv("SECRET_KEY") for both create_access_token and decode_access_token.
Add debug prints to both functions to confirm the SECRET_KEY is the same value at encode and decode time.
Also confirm that load_dotenv() is called before os.getenv in the module. Show the corrected jwt.py.
```

---

## Issue 3: GET /tickets returns all tickets for a regular user instead of only their own

Error: No exception — silent data leak. Regular user receives tickets belonging to other users.

Root cause: The filter condition in the GET /tickets handler was not applied. Either the `if`/`else` block was written incorrectly, or the `.where(Ticket.owner_id == current_user.id)` clause was forgotten in the regular user branch.

Fix: Confirm the handler contains:

```python
if current_user.role == "admin":
    tickets = session.exec(select(Ticket)).all()
else:
    tickets = session.exec(select(Ticket).where(Ticket.owner_id == current_user.id)).all()
```

Test by: creating two users, each creating one ticket, logging in as user 1 and calling GET /tickets — the response should contain exactly one ticket.

What to ask AI:

```text
My GET /tickets endpoint is returning all tickets to a regular (non-admin) user.
The handler should filter tickets by current_user.id for non-admin users.
Show me the corrected GET /tickets handler using SQLModel's select().where() syntax.
Include the admin check and the filtered query for regular users. Also show a pytest test
that verifies a regular user cannot see another user's tickets.
```

---

# Key Takeaways

1. Authentication and authorization are separate concerns — implement them in separate dependency functions. `get_current_user` handles identity; `require_admin` handles permission. Mixing them into a single function makes the code harder to reuse, test, and explain.

2. JWT statelessness is a trade-off, not a pure advantage. The benefit is horizontal scalability with no shared session store. The cost is inability to revoke individual tokens before expiry. For this project with 30-minute token lifetimes, the trade-off is acceptable. For production systems with sensitive data, short token lifetimes plus a Redis-backed revocation list is the standard approach.

3. Never trust input to produce the correct error differentiation automatically — test it explicitly. Confirm that your login endpoint returns the same HTTP status and message for a missing email as it does for a wrong password. Silent information leaks through error messages are a common auth vulnerability.

4. The dependency chain `Depends(require_admin)` → `Depends(get_current_user)` → `Depends(get_db)` illustrates FastAPI's composability. Each dependency only does one thing. This makes each piece independently testable and makes the route signatures self-documenting — you can read the signature and know exactly what guardrails are in place before the handler body runs.

---

# Session 4 Preview

In Session 4, we will add the first AI feature:

## LLM Ticket Classifier

When a user submits a new ticket via `POST /tickets`, the API will send the ticket's title and description to the OpenAI Chat Completions API and automatically classify:

- **Category**: billing / technical / account / general
- **Priority**: low / medium / high

The Ticket model will be extended with `category` and `priority` fields. The classification will happen synchronously at ticket creation time and be stored in the same database row as the ticket.

Main AI/technical concept: Structured output from LLMs — using a Pydantic response model with `response_format` or function calling to force the LLM to return JSON instead of free text.

The auth layer from Session 3 will be fully in place — the classifier will run on behalf of the authenticated user and the classified ticket will be owned by `current_user.id`.
