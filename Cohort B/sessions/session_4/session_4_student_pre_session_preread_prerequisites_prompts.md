# Session 4 Student Pre-Session File: Add LLM Ticket Classifier

## What We Are Building

Across these 8 sessions, we are building one continuous backend system:

# AI Support Ticket Resolution Copilot

This system is a production-grade FastAPI backend that handles support ticket creation, classification, resolution, and agent-driven follow-up using AI.

By the end of all sessions, the backend will:

- accept and persist support tickets with a full CRUD API
- enforce JWT authentication and role-based access (user vs. admin)
- classify every ticket automatically using an LLM
- search a vector knowledge base for relevant past resolutions (RAG)
- use LangGraph agents to suggest and execute resolution steps
- expose a complete, deployable API with auth, AI, and background tasks

## What Is Already Built

By the end of Session 3, your project has:

- `app/main.py` — FastAPI app setup, router registration, DB table creation on startup
- `app/db/session.py` — SQLAlchemy engine and `get_session` dependency
- `app/models/ticket.py` — `Ticket` SQLModel table, `TicketCreate`, `TicketUpdate`, `TicketRead` schemas
- `app/models/user.py` — `User` SQLModel table, `UserRole` enum (`user`, `admin`)
- `app/routes/tickets.py` — Protected CRUD routes: `POST /tickets`, `GET /tickets`, `GET /tickets/{id}`, `PATCH /tickets/{id}`, `DELETE /tickets/{id}`
- `app/routes/auth.py` — `POST /auth/register`, `POST /auth/login` returning JWT tokens
- `app/core/auth.py` — `get_current_user` dependency, `require_admin` dependency, JWT encode/decode logic
- `app/core/config.py` — Settings loaded from environment variables
- `tests/` — pytest tests for ticket CRUD and auth routes

## Session 4 Goal

Add LLM-powered ticket classification to the `POST /tickets` flow.

When a ticket is created, the backend:
1. Saves the ticket to the DB
2. Calls an LLM (Gemini 1.5 Flash) with the ticket content
3. Receives structured JSON classification output
4. Stores the classification in a new `TicketClassification` table
5. Returns the classification alongside the ticket in the response

## Session 4 Output

By the end of Session 4, `POST /tickets` should return a response like:

```json
{
  "id": 1,
  "title": "Cannot login to my account",
  "description": "I have been locked out for two days...",
  "status": "open",
  "created_at": "2026-06-23T09:00:00",
  "user_id": 3,
  "classification": {
    "category": "Technical",
    "priority": "High",
    "sentiment": "Frustrated",
    "urgency_score": 8,
    "summary": "User locked out of account for two days.",
    "suggested_team": "Tech Support"
  }
}
```

If the LLM call fails, the response returns with `"classification": null` and the ticket is still saved.

---

# Pre-Read

## Why Are We Adding This Feature at This Point?

The first three sessions built a stable, authenticated ticket CRUD backend. The data model is solid, auth is working, and the DB layer is tested. This is the right moment to add AI because:

1. We have a stable integration point — `POST /tickets` is already working and tested. Adding the LLM call as a post-save step is low-risk.
2. The classification metadata we generate (`category`, `priority`, `urgency_score`) will be needed by the RAG system in Session 5 for filtering and ranking results.
3. This is the simplest possible AI integration — one LLM call, one structured response, no conversation history, no agents. It is the right place to learn the fundamentals of LLM API integration before we add LangChain (Session 5) and LangGraph agents (Session 6).

## System Architecture Flow — Full Backend (Session 1 Through Session 4)

```
Client Request
     |
     v
[FastAPI App: app/main.py]
     |
     v
[JWT Auth Middleware: app/core/auth.py]
  - Decodes Bearer token
  - Extracts user id + role from token claims
  - Injects current_user via Depends(get_current_user)
     |
     v
[Route Handler: app/routes/tickets.py]
  POST /tickets
     |
     v
[Pydantic Validation: TicketCreate schema]
  - 422 returned immediately if body is invalid
     |
     v
[DB Write: SQLModel session]
  - Ticket row inserted into tickets table
  - session.commit() --> ticket.id is assigned
     |
     v
[LLM Classifier: app/services/llm_classifier.py]  <-- NEW in Session 4
  - Gemini 1.5 Flash API called via google-generativeai
  - System prompt requests structured JSON
  - response_mime_type="application/json" in GenerationConfig
  - temperature=0.1
     |
     +-- success --> [Parse JSON] --> [Save TicketClassification row]
     |
     +-- failure --> [Log warning] --> [classification = None]
     |
     v
[Response: TicketReadWithClassification]
  - Returns 201 with ticket + classification fields

     |
     v (Session 5 will add this)
[RAG Knowledge Base: ChromaDB]
  - Embed ticket description
  - Search for similar past resolutions

     |
     v (Session 6 will add this)
[LangGraph Agent]
  - Use classification + RAG results to suggest resolution steps
```

## Key Concepts to Revise Before Session 4

**1. Gemini API (`google-generativeai` Python library)**

The `google-generativeai` library provides the `genai` module. The key pattern is:

```python
import google.generativeai as genai
import json, os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config=genai.GenerationConfig(
        response_mime_type="application/json",
        temperature=0.1
    )
)
response = model.generate_content(prompt)
result = json.loads(response.text)  # response.text is the JSON string
```

Know this call pattern. Know that `response.text` is a string, not a dict — you must call `json.loads()` on it.

**2. JSON Output Mode (`response_mime_type="application/json"`)**

Setting `response_mime_type="application/json"` inside `genai.GenerationConfig` forces the Gemini model to return valid JSON. Without it, the model might wrap the JSON in markdown (` ```json ... ``` `), add prose before the JSON, or return partial JSON. `json.loads()` on any of those would raise a `json.JSONDecodeError`. Setting `response_mime_type` eliminates this class of failure. The system prompt should still say "return JSON" somewhere for best results.

**3. Temperature in LLMs**

Temperature is a float parameter (typically 0–2) that controls randomness in token sampling. Low temperature (0–0.2) makes the model near-deterministic — it picks the highest-probability token almost every time. High temperature (0.7–1.0) adds randomness, generating more varied responses. For classification tasks — where you want the same input to consistently produce the same output — use `temperature=0.1` or lower. In Gemini, this is set inside `genai.GenerationConfig(temperature=0.1)`.

**4. System Prompts and Prompt Engineering for Classification**

With the Gemini API, the full prompt (system instructions + user content) is passed as a single string to `model.generate_content(prompt)`. For classification:
- Establish a role: "You are a support ticket classifier"
- Specify exact output structure with field names
- Enumerate allowed values for categorical fields
- Specify types for numeric fields ("integer between 1 and 10")
- Add a format constraint: "Return only the JSON object, no explanation"

A well-designed prompt removes ambiguity and reduces the chance of out-of-distribution outputs.

**5. SQLModel Foreign Keys**

A one-to-one relationship between `Ticket` and `TicketClassification` is expressed via a foreign key:

```python
class TicketClassification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_id: int = Field(foreign_key="ticket.id", unique=True)
    category: Optional[str] = None
    priority: Optional[str] = None
    # ...
```

`Field(foreign_key="ticket.id")` tells SQLAlchemy to create a `FOREIGN KEY (ticket_id) REFERENCES ticket(id)` constraint. The `unique=True` enforces one classification per ticket.

**6. Graceful Degradation Pattern**

An external API call can fail for many reasons: network timeout, invalid key, rate limit, quota exhaustion, malformed response. Graceful degradation means your core feature (ticket creation) does not fail because of a non-critical enhancement (classification). Implementation:

```python
try:
    classification_data = classify_ticket(ticket.title, ticket.description)
except Exception as e:
    logger.warning(f"Classification failed: {e}")
    classification_data = None
```

The ticket is committed to DB before this block. The block can fail without affecting the ticket.

**7. Environment Variables and `python-dotenv`**

Never hardcode API keys. Store them in a `.env` file:

```
GEMINI_API_KEY=your-key-here
```

Load them at startup:

```python
from dotenv import load_dotenv
import os
load_dotenv()
```

Add `.env` to `.gitignore`. After `load_dotenv()`, access the key with `os.environ["GEMINI_API_KEY"]` and pass it to `genai.configure(api_key=os.environ["GEMINI_API_KEY"])`. Get a free Gemini API key at aistudio.google.com — no credit card required.

**8. `unittest.mock.patch` for Testing External APIs**

When writing pytest tests for code that calls the Gemini API, you must mock the API call — you do not want real API calls in your test suite. Use `unittest.mock.patch` to replace `google.generativeai.GenerativeModel.generate_content` with a `MagicMock` that returns a controlled response object (with a `.text` attribute). This keeps tests fast, deterministic, and runnable without API keys.

---

# Prerequisites: Setup Before Session 4

## Python Packages to Install

```bash
pip install google-generativeai
pip install python-dotenv
```

Verify the google-generativeai package is installed:

```bash
python -c "import google.generativeai as genai; print('google-generativeai installed')"
```

Get a free Gemini API key at aistudio.google.com (no credit card required).

## Environment Setup

Create or update your `.env` file in the project root:

```
GEMINI_API_KEY=your-gemini-api-key-here
SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///./tickets.db
```

Verify `.env` is in your `.gitignore`:

```bash
grep ".env" .gitignore
# Should output: .env
```

If it is not there, add it now:

```bash
echo ".env" >> .gitignore
```

## Getting a Free Gemini API Key

1. Go to aistudio.google.com
2. Sign in with a Google account
3. Click "Get API key" → "Create API key"
4. Copy the key and paste it into your `.env` file as `GEMINI_API_KEY=your-key-here`

The free tier allows 15 requests per minute and 1 million tokens per day — more than sufficient for this session.

## Code State from Session 3

Your project should start cleanly with no import errors:

```bash
uvicorn app.main:app --reload
# Should print: INFO: Application startup complete.
```

Run existing tests:

```bash
pytest tests/ -v
# All existing tests should pass before you begin Session 4
```

If any tests are failing from Session 3, fix them before the session starts.

## Project Directory Structure Expected

```
project-root/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── auth.py
│   │   └── config.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   │   ├── ticket.py
│   │   └── user.py
│   ├── routes/
│   │   ├── tickets.py
│   │   └── auth.py
│   └── services/          <-- you may need to create this directory
├── tests/
│   ├── test_tickets.py
│   └── test_auth.py
├── .env                   <-- NOT committed to git
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Content to Prepare Before Class

Have the following ready in a text file before the session starts:

```text
A realistic support ticket — title and description — for each of these scenarios:

1. Billing dispute:
   Title: ...
   Description: ...

2. Technical problem (login, API, error):
   Title: ...
   Description: ...

3. Account management request:
   Title: ...
   Description: ...

4. General inquiry:
   Title: ...
   Description: ...
```

You will use these to test that the classifier correctly identifies the `category` for each type. Having real test cases ready makes the testing block much more productive.

---

# Prompts for Session 4

Use these prompts when instructed during the session. All prompts are written for Antigravity coding assistant.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Support Ticket Resolution Copilot using FastAPI, SQLModel, and SQLAlchemy with a SQLite database. The project is a backend-only API with no frontend.

Current project state (already built in Sessions 1–3):
- app/main.py: FastAPI app, includes routers, calls SQLModel.metadata.create_all(engine) on startup
- app/db/session.py: SQLAlchemy engine, SessionLocal, get_session dependency
- app/models/ticket.py: Ticket (table=True), TicketCreate, TicketUpdate, TicketRead SQLModel schemas. Fields: id, title, description, status (default "open"), created_at, user_id
- app/models/user.py: User (table=True), UserRole enum (user/admin), hashed_password field
- app/routes/tickets.py: Protected CRUD routes. POST /tickets, GET /tickets, GET /tickets/{id}, PATCH /tickets/{id}, DELETE /tickets/{id}. All routes use Depends(get_current_user).
- app/routes/auth.py: POST /auth/register and POST /auth/login. Login returns {"access_token": "...", "token_type": "bearer"}
- app/core/auth.py: create_access_token(), decode_token(), get_current_user dependency, require_admin dependency
- app/core/config.py: Settings loaded from environment using python-dotenv. Includes SECRET_KEY, DATABASE_URL, GEMINI_API_KEY
- tests/: pytest tests for auth and ticket CRUD

Task for Session 4: Add LLM-powered ticket classification to the POST /tickets flow.

Create the following new files and modify the specified existing files:

NEW FILE: app/models/ticket_classification.py
- SQLModel class TicketClassification with table=True
- Fields: id (Optional[int], primary_key), ticket_id (int, foreign_key="ticket.id", unique=True), category (Optional[str]), priority (Optional[str]), sentiment (Optional[str]), urgency_score (Optional[int]), summary (Optional[str]), suggested_team (Optional[str]), created_at (datetime, default=datetime.utcnow)
- No relationships defined on this model (keep it simple)

NEW FILE: app/services/llm_classifier.py
- Function: classify_ticket(title: str, description: str) -> Optional[dict]
- Uses google-generativeai: import google.generativeai as genai
- Calls genai.configure(api_key=os.environ["GEMINI_API_KEY"]) — do NOT hardcode the key
- Creates model with genai.GenerativeModel("gemini-1.5-flash", generation_config=genai.GenerationConfig(response_mime_type="application/json", temperature=0.1))
- System prompt must instruct the model to return a JSON object with exactly these fields:
    category: one of Billing, Technical, Account, General
    priority: one of Low, Medium, High, Critical
    sentiment: one of Neutral, Frustrated, Angry, Satisfied
    urgency_score: integer between 1 and 10
    summary: one sentence description under 20 words
    suggested_team: one of Billing Support, Tech Support, Account Team
- System prompt must say "Return only the JSON object. No explanation, no markdown."
- Prompt should include the ticket title and description clearly labeled
- Calls model.generate_content(prompt) and parses with json.loads(response.text)
- Wraps the entire API call and json.loads() in try/except
- On any exception: logs a warning with the error details and returns None
- On success: returns the parsed dict

MODIFY: app/routes/tickets.py
- Import classify_ticket from app.services.llm_classifier
- Import TicketClassification from app.models.ticket_classification
- In the POST /tickets route handler:
    1. Validate and save the Ticket to DB first (session.add, session.commit, session.refresh)
    2. After commit, call classify_ticket(ticket.title, ticket.description)
    3. If result is not None, create a TicketClassification instance and save it (session.add, session.commit)
    4. Update the response to include classification data
- The POST /tickets route must return HTTP 201 even if classify_ticket returns None

MODIFY or CREATE: app/schemas/ticket.py (or update app/models/ticket.py)
- Create TicketReadWithClassification: a Pydantic BaseModel (not SQLModel table) that includes all TicketRead fields plus an optional ClassificationOut nested model
- ClassificationOut should have: category, priority, sentiment, urgency_score, summary, suggested_team — all Optional[str] or Optional[int]
- Use this as the response_model for POST /tickets

Constraints:
- Do NOT add streaming
- Do NOT add LangChain, LangGraph, or any agent framework
- Do NOT add a separate /classify endpoint
- Do NOT add async LLM calls or background tasks
- Do NOT add multiple LLM providers or provider switching
- Do NOT modify the JWT auth system or any existing auth logic
- Do NOT add Alembic migrations — rely on SQLModel.metadata.create_all(engine) for table creation
- Do NOT use the openai package — use google-generativeai exclusively

Add clear inline comments explaining:
- Why the ticket is committed before the LLM call
- Why response_mime_type="application/json" is used in the GenerationConfig
- Why temperature is set low
- What the try/except block is protecting against
- How the classification is linked to the ticket via ticket_id
```

---

## Prompt 2: Improvement Prompt

```text
Review the LLM classifier code in app/services/llm_classifier.py and the POST /tickets route in app/routes/tickets.py.

Apply these specific improvements:

1. In llm_classifier.py:
   - Replace bare "except Exception" with specific exception handling in this order:
     a. except google.api_core.exceptions.PermissionDenied
     b. except google.api_core.exceptions.ResourceExhausted
     c. except google.api_core.exceptions.DeadlineExceeded
     d. except google.api_core.exceptions.ServiceUnavailable
     e. except json.JSONDecodeError
     f. except Exception (catch-all last)
   - Each except block should log a warning with the specific error type and message
   - Add type hints to the return value: -> Optional[dict]
   - Add input validation: if title and description are both empty strings, return None immediately without calling the API

2. In app/routes/tickets.py:
   - Add a helper function build_classification_response(ticket, classification) that constructs the response dict cleanly, separate from the route handler logic
   - Ensure the response model correctly handles None classification — classification fields should be null in the JSON response, not missing

3. Add urgency_score type coercion after json.loads():
   - Convert urgency_score to int with int(result.get("urgency_score", 5)) and clamp it: max(1, min(10, value))
   - This handles cases where the LLM returns "7" as a string instead of integer 7

Do not change the system prompt, the model name, or the temperature value.
Do not add new routes or new tables.
Do not add LangChain or any agent framework.
```

---

## Prompt 3: Debugging Prompt — LLM Call Returns 422 or Classification Is Null Unexpectedly

```text
I am debugging my POST /tickets endpoint after adding the LLM classifier in Session 4 of my FastAPI project.

Current symptoms (describe which applies):

SYMPTOM A: POST /tickets returns 422 Unprocessable Entity after I added the classification fields to the response.
- The request body is valid (same body that worked before Session 4 changes)
- The error response body contains validation errors about the response model

SYMPTOM B: POST /tickets returns 201 but the classification fields are always null, even though GEMINI_API_KEY is set correctly.
- Running classify_ticket() directly in a Python shell works fine
- The issue is in how classify_ticket is called from the route handler

SYMPTOM C: Server crashes with "sqlalchemy.exc.IntegrityError: FOREIGN KEY constraint failed" when creating a ticket.
- The ticket_classification table was created
- The error happens during the classification save step

For SYMPTOM A: Check the response_model parameter on the POST /tickets route decorator. The response_model must be set to TicketReadWithClassification (or equivalent), not TicketRead. Show me the current route decorator and fix it.

For SYMPTOM B: Check whether classify_ticket is being called before session.commit() for the ticket. If classify_ticket is called before the commit, ticket.id may be None or the ticket may not exist in DB yet when the classification tries to reference it. Show me the order of operations in the route handler and fix it.

For SYMPTOM C: The TicketClassification row is being inserted before the parent Ticket row is committed. Fix the commit order: session.add(ticket) → session.commit() → session.refresh(ticket) → [LLM call] → create TicketClassification with ticket_id=ticket.id → session.add(classification) → session.commit().

Show me exactly what to change in app/routes/tickets.py and app/services/llm_classifier.py to fix the reported symptom.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the Session 4 implementation in technical language suitable for a backend engineering interview.

Walk through these files:
- app/services/llm_classifier.py
- app/models/ticket_classification.py
- The updated POST /tickets handler in app/routes/tickets.py
- The TicketReadWithClassification response schema

For each file, explain:
1. The purpose of the module and its responsibilities
2. The key design decisions and why they were made
3. How it fits into the overall request-response lifecycle
4. What could go wrong and how the code handles it

Specific questions to answer in the explanation:
- Why is response_format={"type": "json_object"} used instead of just parsing free-text output?
- Why is temperature set to 0.1 for this task?
- Why is TicketClassification a separate table rather than extra columns on Ticket?
- What is the commit order for the ticket and classification, and why does it matter?
- What happens to the POST /tickets response if classify_ticket raises an exception?

Do not rewrite the code. Explain it as if preparing for a technical interview where the interviewer will ask follow-up questions.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Help me explain the Session 4 LLM ticket classifier feature to a technical interviewer.

Structure the explanation as follows:

1. What the feature does (2-3 sentences, implementation-level)
2. Why this design was chosen over alternatives (e.g., why synchronous vs. async, why separate table vs. columns on Ticket, why JSON mode vs. free-text)
3. The key technical components: the system prompt, temperature setting, response_format, error handling
4. The DB design: TicketClassification table, foreign key relationship, commit order
5. Trade-offs and limitations of the current implementation (what would you change for production at scale?)
6. What you would add next (naturally leads into Session 5 RAG)

Keep it concise — each section should be 2-3 sentences. Assume the interviewer knows Python and FastAPI. Use correct technical terminology: json.loads(), response_format, temperature, graceful degradation, foreign key, Pydantic response model.
```

---

## Prompt 6: Unit Test Generation Prompt

```text
Generate pytest unit tests for the Session 4 LLM ticket classifier feature in my FastAPI project.

Project context:
- app/services/llm_classifier.py contains classify_ticket(title: str, description: str) -> Optional[dict]
- app/routes/tickets.py contains the POST /tickets route
- Tests should go in tests/test_classifier.py (new file) and tests/test_tickets.py (extend existing)

Generate the following tests:

tests/test_classifier.py:
1. test_classify_ticket_success: Mock google.generativeai.GenerativeModel.generate_content to return a MagicMock with .text set to a valid JSON string with all six fields. Assert that classify_ticket returns a dict with correct values.
2. test_classify_ticket_returns_none_on_auth_error: Mock the API call to raise google.api_core.exceptions.PermissionDenied. Assert that classify_ticket returns None (does not raise).
3. test_classify_ticket_returns_none_on_rate_limit: Mock to raise google.api_core.exceptions.ResourceExhausted. Assert returns None.
4. test_classify_ticket_returns_none_on_malformed_json: Mock the API to return a MagicMock where .text is "not valid json". Assert returns None.
5. test_classify_ticket_returns_none_for_empty_input: Call classify_ticket("", "") directly (no mock needed if input validation returns None early). Assert returns None.

tests/test_tickets.py (add to existing file):
6. test_post_ticket_with_classification: Mock classify_ticket to return a valid classification dict. Call POST /tickets with a valid auth token. Assert response is 201, response body includes "classification" key with correct fields.
7. test_post_ticket_classification_null_when_llm_fails: Mock classify_ticket to return None. Call POST /tickets. Assert response is still 201, response body has "classification": null.

Use unittest.mock.patch for all mocks. Target "google.generativeai.GenerativeModel.generate_content" as the patch path. Use the existing conftest.py fixtures for the FastAPI test client and auth tokens. Add comments explaining what each test is verifying and why.

Do NOT add tests that make real API calls. Do NOT add integration tests that require a running database for the mock tests.
```

---

## Prompt 7: Edge Case and Error State Prompt

```text
Review my Session 4 implementation and add proper handling for these specific edge cases in app/services/llm_classifier.py and app/routes/tickets.py:

Edge Case 1: LLM returns a category value not in the allowed set
- e.g., {"category": "Payment", "priority": "High", ...}
- Add a post-parse validation step: if category not in ["Billing", "Technical", "Account", "General"], replace it with "General"
- Do the same for priority (allowed: Low, Medium, High, Critical → fallback: "Medium"), sentiment (allowed: Neutral, Frustrated, Angry, Satisfied → fallback: "Neutral"), suggested_team (allowed: Billing Support, Tech Support, Account Team → fallback: "Tech Support")

Edge Case 2: urgency_score is returned as a string or float
- Add: urgency_score = max(1, min(10, int(float(result.get("urgency_score", 5)))))
- This handles "7", 7.5, and missing urgency_score

Edge Case 3: LLM returns extra keys not in our schema
- After json.loads(), only extract the six expected keys. Ignore all other keys.
- Use: result = {k: result.get(k) for k in ["category", "priority", "sentiment", "urgency_score", "summary", "suggested_team"]}

Edge Case 4: Very long ticket description (over 2000 characters)
- Add a character limit: truncate description to 1500 characters before including it in the user message
- This prevents token limit errors and keeps classification costs predictable

Edge Case 5: ticket.title is None or empty string
- If title is None or empty, use "Untitled ticket" as the title in the user message

Do not change the system prompt content, the model, the temperature, or the response_format setting.
Do not add new routes, tables, or schemas.
Show exactly which lines to add or change in each file.
```

---

# What You Should Be Able to Explain After Session 4

After the session, prepare your own answers to these questions. No answers are given here — the point is to explain them in your own words, at a technical level.

1. What is the Gemini API call structure for this classifier? What parameters are being set and why?

2. What is the difference between `response_mime_type="application/json"` in the `GenerationConfig` and simply telling the model to "respond in JSON" in the system prompt?

3. Why is `temperature=0.1` appropriate for a classification task? What would happen at `temperature=0.9`?

4. What is the exact commit order for the Ticket and TicketClassification rows, and why does that order matter for data integrity?

5. What happens to the `POST /tickets` endpoint if `GEMINI_API_KEY` is set to an expired key and `google.api_core.exceptions.PermissionDenied` is raised?

6. Why is `TicketClassification` a separate SQLModel table rather than additional nullable columns on the `Ticket` table?

7. If a student runs `pytest tests/ -v` and the test for `test_post_ticket_with_classification` fails with `KeyError: 'classification'`, what is the most likely cause?

8. What is the risk of not including `response_mime_type="application/json"` in the Gemini `GenerationConfig`, and how would `json.JSONDecodeError` surface in the current code?

9. How would you change the architecture if classification needed to happen asynchronously after ticket creation, without blocking the HTTP response?

10. What information would you include in the system prompt to improve classification accuracy for a multilingual support system where tickets arrive in English, Hindi, and Spanish?

## Final Session 4 Explanation

```text
In Session 4, I added LLM-powered ticket classification to the POST /tickets endpoint of the AI Support Ticket Resolution Copilot. When a ticket is created, the backend calls the Gemini 1.5 Flash API via the google-generativeai library with a structured prompt and response_mime_type="application/json" in the GenerationConfig, which guarantees the model returns valid JSON containing category, priority, sentiment, urgency_score, summary, and suggested_team fields. The classification result is stored in a dedicated TicketClassification table linked to the ticket via a foreign key, and returned alongside the ticket in the 201 response. If the LLM call fails for any reason — invalid key, rate limit, malformed response — the ticket still saves successfully and the classification fields are null, which is a graceful degradation pattern that ensures the core ticket creation feature is never blocked by an optional AI enhancement.
```
