# Session 4 Instructor File: Add LLM Ticket Classifier

## Session Title

Add LLM Ticket Classifier

## Duration

2 hours

## Project

AI Support Ticket Resolution Copilot

## Session 4 Objective

By the end of Session 4, students should have a working LLM-powered ticket classification system integrated into the ticket creation flow. When a support ticket is submitted via `POST /tickets`, the backend calls an LLM (Gemini 1.5 Flash), receives structured JSON output, stores the classification in a dedicated `TicketClassification` table, and returns it alongside the ticket in the API response. The system must degrade gracefully — if the LLM call fails, the ticket still saves successfully.

## Session 4 Deliverable

Students will extend the existing FastAPI backend to include:

1. A `TicketClassification` SQLModel table linked to `Ticket` via a foreign key
2. An `llm_classifier.py` service module that calls the Gemini 1.5 Flash API with a structured system prompt requesting JSON output
3. A low-temperature classification call returning: `category`, `priority`, `sentiment`, `urgency_score`, `summary`, `suggested_team`
4. Integration of the classifier into the `POST /tickets` route — classification runs after the ticket is saved
5. Graceful error handling so that an LLM failure or malformed JSON response does not cause a 500 error or prevent ticket creation
6. Updated ticket response schema that includes the classification fields
7. Passing pytest tests covering the happy path and the LLM failure fallback

## Strict Scope Control

### Include

- Gemini 1.5 Flash API call (`google-generativeai` Python library, `model.generate_content`)
- `response_mime_type="application/json"` in `GenerationConfig` to enforce structured output
- `temperature=0.1` or lower for deterministic classification
- A well-designed system prompt that specifies all six output fields with allowed values
- `TicketClassification` SQLModel table with `ticket_id` foreign key
- Classification stored in DB immediately after the LLM call
- Classification returned in the `POST /tickets` response body
- `try/except` block around the LLM call — ticket saves even if classification fails
- API key loaded from environment variable (`GEMINI_API_KEY`) via `os.environ` or `python-dotenv`
- pytest tests mocking the Gemini model with `unittest.mock.patch`

### Do Not Include

- Streaming responses (`stream=True`) — not needed for classification
- Multiple LLM providers simultaneously or provider switching logic
- Fine-tuning or model training of any kind
- Multi-turn conversation or chat history — this is a single-shot classification call
- LangChain, LangGraph, or any agent framework — Session 5 and Session 6 handle those
- RAG or vector search — Session 5
- Refresh token logic or changes to the existing JWT auth system
- Any new user-facing routes beyond the updated `POST /tickets` response
- Celery, background tasks, or async LLM calls — keep it synchronous for now
- Pydantic v2 model_validator or complex validators — keep response models simple

Session 4 adds exactly one AI integration point: ticket creation triggers a single LLM classification call.

---

# Instructor Framing

## Opening Message

In Session 3 we added JWT authentication and role-based access control. The codebase now has:

- `app/routes/tickets.py` with protected CRUD routes — `POST /tickets` requires a valid JWT
- `app/routes/auth.py` with `/auth/login` and `/auth/register`
- `app/models/user.py` with `User` and `UserRole` enum
- `app/models/ticket.py` with `Ticket`, `TicketCreate`, `TicketRead` SQLModel schemas
- `app/core/auth.py` with `get_current_user` dependency and role checking
- `app/db/session.py` with `get_session` dependency
- JWT tokens with `sub`, `role`, and `exp` claims
- All ticket routes protected — only authenticated users can create/read tickets

Today we add the first real intelligence to the backend. When a user submits a ticket, the backend will silently call Gemini 1.5 Flash, classify that ticket, and return the classification with the response. The user gets a richer response. The support team gets structured metadata. No manual triaging needed.

## Key Philosophy

Students at this stage can read and write FastAPI code. The challenge today is not the syntax — it is understanding why each design decision was made: why we use JSON mode instead of free-text, why temperature is low for classification, why we wrap the LLM call in a try/except, and why we store the classification separately in its own table rather than adding columns to the Ticket table.

Students are expected to:

- guide the AI coding tool with a precise, scoped prompt
- read and audit the generated code critically
- understand each part well enough to explain it in a technical interview
- test both the happy path and the failure path
- make conscious design decisions, not just accept AI output

## Repeated Instructor Line

The AI generated the code. You are responsible for understanding why every line exists, testing every code path, and explaining every design decision.

---

# Session Flow

## 0–10 min: Opening — Recap of Session 3 and Current Codebase State

### Instructor Goal

Anchor students in the current project state before introducing new scope.

### Codebase Recap Steps

Open the project and walk through these files on screen:

1. `app/routes/tickets.py` — show the `POST /tickets` route, point out the `current_user: User = Depends(get_current_user)` dependency
2. `app/models/ticket.py` — show `Ticket`, `TicketCreate`, `TicketRead` models
3. `app/routes/auth.py` — show `/auth/login` returning a JWT token
4. Open Swagger UI at `http://localhost:8000/docs` — demonstrate that `POST /tickets` now returns 401 if no Bearer token is passed
5. Show a successful authenticated request: get a token from `/auth/login`, paste it into Swagger, create a ticket, and get back a 201 response

Ask students: "What does the ticket response currently contain?"

Expected answer: `id`, `title`, `description`, `status`, `created_at`, `user_id` — no classification data yet.

### Transition Statement

Today we add classification. After Session 4, the same `POST /tickets` call will also return `category`, `priority`, `sentiment`, `urgency_score`, `summary`, and `suggested_team`.

---

## 10–20 min: Architecture Breakdown — What Are We Adding and Why

### Instructor Goal

Students must understand the architecture before running any prompt.

### Draw or Display This Flow on Whiteboard/Screen

```
POST /tickets
     |
     v
[Validate Request Body] --> 422 if invalid
     |
     v
[Save Ticket to DB] --> tickets table
     |
     v
[Call LLM Classifier] --> Gemini API (api.generativeai.google.com)
     |
     +-- success --> [Parse JSON Response]
     |                    |
     |                    v
     |               [Save TicketClassification to DB]
     |
     +-- failure --> [Log warning, classification is None]
     |
     v
[Return Ticket + Classification in Response]
```

### Key Design Questions to Ask the Class

1. Why do we save the ticket before calling the LLM? — So that the ticket is not lost if the LLM call fails or times out.
2. Why a separate `TicketClassification` table instead of columns on `Ticket`? — Separation of concerns: ticket data is always present, classification data is optional and may arrive later or be recomputed.
3. Why `temperature=0.1` for classification? — Classification has a fixed output space. Low temperature reduces randomness and keeps the model close to the most probable answer. This improves consistency across identical inputs.
4. Why `response_mime_type="application/json"` in `GenerationConfig`? — This forces the Gemini model to return valid JSON instead of prose, markdown, or partial JSON. Eliminates the need for regex parsing.
5. Why store the API key in an environment variable? — Hardcoding API keys in source code is a security vulnerability — they get committed to git. Environment variables keep secrets out of the codebase.

### Scope Warning

Tell students explicitly: "We are not adding LangChain, streaming, agents, RAG, or multiple LLM providers today. One LLM call, one structured response, one new table."

---

## 20–35 min: Build the Feature Using Antigravity

### Instructor Goal

Use the main build prompt from the student pre-session file to generate the feature via an AI coding tool.

### Instructor Steps

1. Open Antigravity in the project root
2. Paste the main build prompt (Prompt 1 from the student file) exactly as written
3. Do not modify the prompt before generating — let students observe what the raw prompt produces
4. Let generation complete fully before reading or modifying
5. Point out which files the AI created or modified:
   - `app/models/ticket_classification.py` (new)
   - `app/services/llm_classifier.py` (new)
   - `app/routes/tickets.py` (modified)
   - `app/schemas/ticket.py` or response models (modified)
   - possibly `app/db/session.py` or `alembic` migration (review with class)
6. Do not run the code yet — that happens in the walkthrough block

### What to Watch For in Generated Code

- Does the system prompt clearly specify all six output fields and their allowed values?
- Is `response_mime_type="application/json"` present in the `GenerationConfig`?
- Is `temperature` set to 0.1 or lower?
- Is the LLM call inside a `try/except`?
- Is the `TicketClassification` model a proper SQLModel with `ticket_id` as a `ForeignKey`?
- Does the `POST /tickets` route return both ticket and classification fields?
- Is `GEMINI_API_KEY` loaded from environment, not hardcoded?

---

## 35–50 min: Instructor Code Walkthrough — Read Generated Code, Explain Each Part

### Instructor Goal

Every student should understand every meaningful line of the generated code.

### Walk Through Each File in Order

**`app/models/ticket_classification.py`**
- Show the SQLModel class definition with `table=True`
- Explain `ticket_id: int = Field(foreign_key="ticket.id")` — this is the FK linking classification to its ticket
- Point out the nullable fields (`Optional[str]`) — classification might not exist if LLM fails
- Explain the allowed values for each field (category, priority, sentiment enum values)

**`app/services/llm_classifier.py`**
- Walk through the `classify_ticket(title: str, description: str)` function signature
- Read the system prompt aloud — ask students: "Is this prompt specific enough? Does it tell the model exactly what JSON structure to return?"
- Point out `model="gemini-1.5-flash"` — explain why we use a smaller, faster model for classification
- Point out `temperature=0.1` and explain the reasoning
- Point out `response_mime_type="application/json"` in the `GenerationConfig` — explain this is how Gemini enforces JSON output
- Show `json.loads(response.text)` — this is where we parse the string response into a Python dict
- Show the `try/except` block and what it returns on failure (e.g., `None` or a default dict)

**`app/routes/tickets.py`**
- Show how `classify_ticket` is imported and called after `session.add(ticket)`
- Show that `session.commit()` for the ticket happens before the LLM call
- Show how the classification result is persisted to DB in a second `session.add` / `session.commit`
- Show the updated return value — classification fields included in response

**Response Schema**
- Show `TicketReadWithClassification` (or equivalent) — a Pydantic/SQLModel response model that includes classification fields
- Ask: "Why do we not just return the raw dict from the LLM? Why define a typed response model?"

### Ask During Walkthrough

- Where exactly does the LLM call happen in the request lifecycle?
- What happens to the route if `google.api_core.exceptions.ServiceUnavailable` is raised?
- What does the DB state look like if the LLM call fails — is there a row in `ticket_classification`?

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run the main build prompt in their own Antigravity session and build their version of the feature.

### Setup Check Before Students Begin

Ensure every student has:

1. `GEMINI_API_KEY` set in their `.env` file (free key from aistudio.google.com — no credit card required)
2. `google-generativeai` package installed: `pip install google-generativeai`
3. `python-dotenv` installed: `pip install python-dotenv`
4. The project running without errors from Session 3 (`uvicorn app.main:app --reload` starts cleanly)
5. Their `.env` file NOT committed to git — verify `.gitignore` includes `.env`

### Instructor Support Areas

Help students with:

- `google.api_core.exceptions.PermissionDenied` — means `GEMINI_API_KEY` is missing or wrong
- `ModuleNotFoundError: No module named 'google.generativeai'` — means `google-generativeai` package is not installed: `pip install google-generativeai`
- SQLModel table already exists error on startup — direct to alembic migration or `SQLModel.metadata.create_all(engine)` call
- `422 Unprocessable Entity` on `POST /tickets` — response schema changed, Pydantic validation is failing on the new response model
- JSON decode error from LLM — the `try/except` should catch this; if not, the generated code is missing it
- Rate limit on free tier — add `time.sleep(2)` between calls; Gemini free tier is 15 RPM

### If Student Setup Fails

Do not block the class. The student pairs with a neighbor or follows the instructor screen. The build prompt and code will be available after the session.

---

## 65–80 min: Test and Improve — Run Tests, Test in Swagger, Handle Edge Cases

### Instructor Goal

Demonstrate the full working feature in Swagger and identify one thing to improve.

### Steps

1. Start the server: `uvicorn app.main:app --reload`
2. Open Swagger at `http://localhost:8000/docs`
3. Authenticate: call `POST /auth/login`, copy the token, click "Authorize" in Swagger
4. Create a ticket with a realistic description, e.g.:

```json
{
  "title": "Cannot login to my account",
  "description": "I have been trying to login for the past two days but keep getting an authentication error. I urgently need access to complete a billing task."
}
```

5. Show the response — point out the classification fields
6. Ask the class: "Does the classification look correct? Is the priority what you'd expect? Is the sentiment right?"
7. Create a second ticket with a very different description — show that classification varies
8. Check the DB directly: `SELECT * FROM ticketclassification;` in SQLite browser or psql
9. Improvement to make: if the system prompt is returning inconsistent values for the `category` field, tighten the prompt — add explicit enumeration: `"category must be exactly one of: Billing, Technical, Account, General"`

### Run pytest

```bash
pytest tests/ -v
```

If tests are not yet written, skip to the next block and write them in the error handling section.

---

## 80–95 min: Error Handling and Edge Cases

### Instructor Goal

Teach students to think about what can go wrong with an external API dependency.

### Walk Through These Failure Scenarios

**Scenario 1: GEMINI_API_KEY is missing or invalid**
- Expected behavior: `google.api_core.exceptions.PermissionDenied` is raised
- The `try/except` should catch it, log a warning, and return `None` for classification
- The ticket still saves with a 201 response — classification fields are `null` in the response
- Demonstrate this by temporarily removing the API key from `.env`

**Scenario 2: LLM returns malformed JSON (rare with response_mime_type json, but possible)**
- The `try/except` around `json.loads()` catches `json.JSONDecodeError`
- Ticket still saves, classification is `null`
- Demonstrate by temporarily monkey-patching the LLM response to return `"Not valid JSON"`

**Scenario 3: LLM returns valid JSON but missing a required field**
- e.g., model returns `{"category": "Billing", "priority": "High"}` without `urgency_score`
- Show that `TicketClassification` model should use `Optional` fields with defaults
- Or add a post-parse validation step that fills in defaults

**Scenario 4: Gemini API rate limit or timeout**
- `google.api_core.exceptions.ResourceExhausted` or `google.api_core.exceptions.DeadlineExceeded`
- Both should be caught by the broad `except Exception` or by specific exception types
- Free tier is 15 RPM — add `time.sleep(2)` between calls during classroom demos
- Demonstrate adding specific exception clauses

### Code Fix to Make Live

If the generated code uses a bare `except Exception`, improve it:

```python
from google.api_core import exceptions as google_exceptions
import json

try:
    result = classify_ticket(title, description)
except google_exceptions.PermissionDenied as e:
    logger.warning(f"Gemini auth failed: {e}")
    result = None
except google_exceptions.ResourceExhausted as e:
    logger.warning(f"Gemini rate limit hit: {e}")
    result = None
except google_exceptions.DeadlineExceeded as e:
    logger.warning(f"Gemini request timed out: {e}")
    result = None
except google_exceptions.ServiceUnavailable as e:
    logger.warning(f"Gemini service unavailable: {e}")
    result = None
except json.JSONDecodeError as e:
    logger.warning(f"LLM returned non-JSON: {e}")
    result = None
except Exception as e:
    logger.warning(f"LLM classification failed: {e}")
    result = None
```

Ask students: "Why is it better to catch specific exceptions first?"

---

## 95–105 min: Concept Pause — LLM API Integration, Structured JSON Output, and Prompt Engineering

### Instructor Goal

Convert implementation experience into interview-ready technical understanding.

### Explain the Full LLM Call Lifecycle

```
Client sends POST /tickets
     |
     v
FastAPI route handler receives TicketCreate body
     |
     v
Ticket saved to DB (id is now assigned)
     |
     v
classify_ticket(title, description) called
     |
     v
model.generate_content(prompt) sends HTTP request to Gemini API
     |
     v
Request is configured with:
  - model: "gemini-1.5-flash"
  - temperature: 0.1
  - response_mime_type: "application/json"
  - prompt: system instructions + ticket text
     |
     v
Gemini returns: {"category": "...", "priority": "...", ...}
     |
     v
json.loads(response.text) converts string to Python dict
     |
     v
TicketClassification row written to DB
     |
     v
Route returns 201 with ticket + classification
```

### Three Core Concepts to Explain

**Concept 1 — Why JSON mode matters:**
Without `response_mime_type="application/json"` in the `GenerationConfig`, the model might return: "Sure! Here is the classification: `{"category": "Billing"}` ..." — wrapped in prose. `json.loads()` would fail. Setting `response_mime_type` guarantees the entire response is valid JSON. This eliminates an entire class of parsing failures.

**Concept 2 — Why temperature matters for classification:**
Temperature controls how much randomness the model injects during sampling. At `temperature=0`, the model always picks the most probable next token — fully deterministic. At `temperature=1`, significant randomness is introduced. For classification with a small fixed output space (e.g., 4 categories), we want consistency. `temperature=0.1` in the Gemini `GenerationConfig` gives near-deterministic outputs while allowing the model to handle ambiguous inputs sensibly.

**Concept 3 — Graceful degradation:**
An external API is an unreliable dependency. Network failures, rate limits, invalid keys, and quota exhaustion are all real production scenarios. The ticket creation feature must not fail because of the classifier. The classifier is an enhancement — the ticket is the core data. Separating them (different table, wrapped in try/except, committed independently) reflects this priority.

### Student Writing Task

Ask every student to write 2–3 sentences:

"What happens when `POST /tickets` is called and the Gemini API is down?"

Expected answer: The ticket is saved to the database and a 201 response is returned. The classification fields in the response will be `null`. The LLM failure is logged as a warning but does not raise an exception to the caller.

---

## 105–115 min: Interview Discussion and Technical Viva Practice

### Instructor Goal

Prepare students to speak fluently about the technical decisions made today.

Use the interview questions section below. Run rapid-fire Q&A with 3–4 students per question.

Focus on questions 6–10 for this block — these require code-level understanding.

---

## 115–120 min: Wrap-Up and Session 5 Preview

### Instructor Closing

Today we added LLM-powered ticket classification to the backend. The feature calls Gemini 1.5 Flash, parses structured JSON output, stores the result in a dedicated table, and degrades gracefully on failure.

In Session 5, we will add a RAG Knowledge Base. The backend will store support articles and past resolutions in ChromaDB (a vector store). When a ticket is created, the backend will embed the ticket description, search for semantically similar past resolutions, and attach relevant knowledge articles to the ticket response. This will allow the system to suggest resolution steps automatically.

Before Session 5, students should:
1. Read the pre-session file for Session 5
2. Understand what embeddings are and why cosine similarity is used for semantic search
3. Have ChromaDB installed: `pip install chromadb`

---

# Instructor Notes

## What to Emphasize

Session 4 is the first time students integrate an external AI API into a production-grade backend flow. The key emphasis areas are:

1. **API key security** — Environment variables are not optional. `GEMINI_API_KEY` hardcoded in source code is a CVE-level mistake in a real job. Emphasize this strongly.
2. **JSON mode vs. free-text parsing** — Students often assume they can just `eval()` or regex-parse LLM output. Explain why this fails in production and why `response_mime_type="application/json"` in the Gemini `GenerationConfig` is the correct solution.
3. **Temperature semantics** — Students confuse temperature with "creativity". Reframe: temperature controls the width of the probability distribution over the next token. Low = narrow = consistent. High = wide = variable.
4. **Graceful degradation as a first-class design requirement** — The LLM is an enhancement, not a dependency. Ticket creation must succeed regardless of LLM status. This is a real system design principle.
5. **Table separation** — `TicketClassification` as a separate table (not columns on `Ticket`) is the right design because classification can be null, can be regenerated, and may expand with new fields. This is a normalization and extensibility decision.
6. **The difference between `session.add()` and `session.commit()`** — Students sometimes do a single commit at the end. Emphasize: commit the ticket first, then attempt classification, then commit classification. The ticket commit must not be inside the LLM try/except.

## Common Student Mistakes

1. **`google.api_core.exceptions.PermissionDenied`** — Student forgot to set `GEMINI_API_KEY` in `.env` or forgot to call `load_dotenv()` before `genai.configure()` is called. Fix: ensure `load_dotenv()` is called at module import time in `app/core/config.py` or `app/main.py`, and that `genai.configure(api_key=os.environ["GEMINI_API_KEY"])` runs before any model calls.

2. **`ModuleNotFoundError: No module named 'google.generativeai'`** — Student has not installed the package. Fix: `pip install google-generativeai`.

3. **`json.JSONDecodeError: Expecting value`** — Student is not using `response_mime_type="application/json"` in the `GenerationConfig` and the model returned prose. Fix: add `generation_config=genai.GenerationConfig(response_mime_type="application/json", temperature=0.1)` to the `genai.GenerativeModel(...)` call and ensure the system prompt includes "respond only with JSON".

4. **`sqlalchemy.exc.IntegrityError: FOREIGN KEY constraint failed`** — Student is inserting a `TicketClassification` row with a `ticket_id` before the ticket has been committed (so the ticket `id` is not yet in the DB). Fix: always `session.commit()` the ticket before creating the classification object.

5. **`422 Unprocessable Entity` on `POST /tickets` after adding classification fields** — The response model (`response_model` in the route decorator) was not updated to include classification fields. Pydantic is trying to serialize a field that does not exist in the declared response model. Fix: update or create a `TicketReadWithClassification` response schema.

6. **`AttributeError: 'NoneType' object has no attribute 'category'`** — Student is trying to access `classification.category` in the route handler but `classification` is `None` because the LLM call failed. Fix: check `if classification is not None` before accessing fields, or use `getattr(classification, 'category', None)`.

7. **LLM returning `urgency_score` as a string `"7"` instead of integer `7`** — The system prompt did not specify the type. Fix: add explicit type specifications in the system prompt: `"urgency_score: integer between 1 and 10"`. Also add `int()` conversion in the parsing step.

8. **Model outputting values outside the allowed set** — e.g., `"category": "Payment"` instead of `"Billing"`. The system prompt was not restrictive enough. Fix: enumerate exact allowed values in the prompt: `"category must be exactly one of: Billing, Technical, Account, General — no other values are allowed"`.

9. **`google.api_core.exceptions.ResourceExhausted` crashing the entire endpoint** — The `try/except` block is present but does not include the Gemini rate-limit exception. Fix: add `except google_exceptions.ResourceExhausted` explicitly, or add a broad `except Exception` as fallback. On the free tier (15 RPM), add `time.sleep(2)` between calls during classroom demos.

10. **API key committed to git** — Student added `GEMINI_API_KEY=...` directly to `app/core/config.py` or similar. Fix immediately. Add `.env` to `.gitignore`. If already committed: rotate the key on aistudio.google.com, then remove it from git history or at minimum invalidate it.

## How to Control the Session

Use this rule: if a modification is not needed for the `POST /tickets` classification flow, it does not happen in Session 4.

Students will want to:
- add a separate `GET /tickets/{id}/classify` endpoint to reclassify existing tickets — not today
- switch to async LLM calls with `asyncio` — not today
- add streaming — not today
- add LangChain — Session 6
- add a frontend — not in this program

Keep every digression with: "That is a valid extension. Write it down. We will not build it today because it is out of Session 4 scope."

## Setup Rule

Do not spend more than 5 minutes on environment setup during live class time.

If `GEMINI_API_KEY` is missing, the student gets a free key immediately from aistudio.google.com (no credit card required, takes under 2 minutes). If network access is blocked, the student follows the instructor screen and builds their own version after the session using the recorded build and the prompts from the student file.

If the existing Session 3 codebase has broken tests or import errors that were not present at Session 3 end, do not debug them live — have the student clone the Session 3 reference repo and continue from there.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What did you build in Session 4?

Expected answer:

In Session 4 I integrated an LLM-powered ticket classifier into the `POST /tickets` endpoint. When a ticket is created, the backend calls the Gemini 1.5 Flash API using `google-generativeai` with a structured system prompt and `response_mime_type="application/json"` in the `GenerationConfig`. The model returns a JSON object with six fields: `category`, `priority`, `sentiment`, `urgency_score`, `summary`, and `suggested_team`. This result is stored in a `TicketClassification` table linked to the ticket via a foreign key and returned in the API response. If the LLM call fails for any reason, the ticket still saves successfully and the classification fields are null.

### Q2. Why did you add this feature at this stage of the project?

Expected answer:

By Session 4 the backend already had a working DB layer, data models, and JWT-authenticated routes from Sessions 1–3. The ticket creation flow was already stable, which made it safe to add the LLM call as an enhancement without risking core functionality. Adding classification before RAG (Session 5) also made sense architecturally: the classification metadata — particularly `priority`, `category`, and `urgency_score` — will be useful for filtering and ranking RAG results in Session 5. Building features in this order means each session's output is useful to the next session.

### Q3. What is the `TicketClassification` table and why is it separate from the `Ticket` table?

Expected answer:

`TicketClassification` is a SQLModel table with columns for `id`, `ticket_id` (FK to `ticket.id`), `category`, `priority`, `sentiment`, `urgency_score`, `summary`, and `suggested_team`. It is separate from `Ticket` because classification is optional — a ticket can exist without a classification if the LLM call failed. Keeping classification in its own table avoids nullable columns on the core `Ticket` entity, makes it easier to add new classification fields later, and allows classification to be regenerated or updated without touching the ticket record. This is standard normalization practice: do not add optional computed metadata as columns on a primary entity table.

### Q4. How does the API key get loaded? Why not hardcode it?

Expected answer:

The API key is loaded from the `GEMINI_API_KEY` environment variable, typically via `python-dotenv` calling `load_dotenv()` which reads a `.env` file that is excluded from version control via `.gitignore`. `genai.configure(api_key=os.environ["GEMINI_API_KEY"])` is called at module import time to initialise the Gemini client with the key. Hardcoding API keys in source code is a serious security vulnerability because the key gets committed to git history, visible to anyone with repo access and on public repositories to automated scanners that harvest exposed keys. Rotating a leaked key is possible but disruptive and sometimes costly if the key was used fraudulently.

### Q5. What does the system prompt look like for this classifier?

Expected answer:

The system prompt instructs the model to act as a support ticket classifier, specifies the exact JSON structure to return, enumerates the allowed values for each categorical field, specifies the type and range for `urgency_score`, and explicitly states to return only JSON with no prose or markdown. For example: "You are a support ticket classification system. Given a ticket title and description, return a JSON object with exactly these fields: category (one of: Billing, Technical, Account, General), priority (one of: Low, Medium, High, Critical), sentiment (one of: Neutral, Frustrated, Angry, Satisfied), urgency_score (integer 1–10), summary (one sentence under 20 words), suggested_team (one of: Billing Support, Tech Support, Account Team). Return only the JSON object. No explanation, no markdown."

---

## Technical Deep-Dive Questions

### Q6. Why is `temperature=0.1` used for classification rather than the default?

Expected answer:

The default temperature for most LLM configurations is around 0.7–1.0. Temperature controls how the model samples from the probability distribution over possible next tokens. A high temperature flattens the distribution, making lower-probability tokens more likely — this increases variety but reduces consistency. For classification with a fixed, small output space (four categories, four priority levels, four sentiment values), consistency is more important than variety. Two identical tickets should always produce the same classification. Setting `temperature=0.1` in the Gemini `GenerationConfig` means the model almost always picks the highest-probability token, which for a well-prompted classification task will be the correct label. Setting it to exactly 0 is also valid and fully deterministic.

### Q7. What is `response_mime_type="application/json"` in `GenerationConfig` and why is it needed?

Expected answer:

`response_mime_type="application/json"` is the JSON output parameter for the Gemini API, set inside a `genai.GenerationConfig` object passed to `genai.GenerativeModel(...)`. When set, the API guarantees that the model's response will be a valid JSON string — it will not include prose, markdown code fences, apologies, or explanations wrapping the JSON. Without it, the model might return a response like: "Here is the classification:\n```json\n{...}\n```" — which fails `json.loads()` because of the surrounding text. Setting `response_mime_type` removes this entire class of parsing failure. The system prompt should still mention that a JSON object is expected — this improves consistency. The result is accessed via `response.text`, which is the full response string, already guaranteed to be valid JSON.

### Q8. Walk through the exact sequence of DB operations in `POST /tickets` after Session 4.

Expected answer:

First, `TicketCreate` is validated by Pydantic when the request body is parsed — a `422` is returned immediately if the body is invalid. Second, a `Ticket` SQLModel instance is created from the validated data and the `current_user.id` is assigned as `user_id`. Third, `session.add(ticket)` stages the ticket for insertion. Fourth, `session.commit()` writes the ticket row to the `ticket` table and assigns it a DB-generated `id`. Fifth, `session.refresh(ticket)` loads the generated `id` back into the Python object. Sixth, `classify_ticket(ticket.title, ticket.description)` is called — this makes the HTTP request to the Gemini API. Seventh, if classification succeeds, a `TicketClassification` instance is created with `ticket_id=ticket.id` and all classification fields, then `session.add(classification)` and `session.commit()` write it to the `ticket_classification` table. Eighth, the route handler builds the response object combining ticket and classification fields and returns it with HTTP 201.

### Q9. How do you write a pytest unit test for the LLM classifier when you do not want to make real API calls?

Expected answer:

We use `unittest.mock.patch` to replace the `google.generativeai.GenerativeModel.generate_content` method with a `MagicMock` that returns a predetermined response. For example:

```python
from unittest.mock import patch, MagicMock
import json

def test_classify_ticket_success():
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "category": "Technical",
        "priority": "High",
        "sentiment": "Frustrated",
        "urgency_score": 8,
        "summary": "User cannot login.",
        "suggested_team": "Tech Support"
    })
    with patch("google.generativeai.GenerativeModel.generate_content",
               return_value=mock_response):
        result = classify_ticket("Login error", "I cannot login to my account.")
    assert result["category"] == "Technical"
    assert result["urgency_score"] == 8
```

This approach tests the parsing and error handling logic of `classify_ticket` without making network requests, making the test fast, deterministic, and safe to run in CI pipelines without API keys.

### Q10. What happens if the LLM returns a valid JSON object but with a `category` value that is not in the allowed set, for example `"category": "Payment"`?

Expected answer:

With the current implementation, the value would be stored as-is in the `TicketClassification` table if `category` is defined as a plain `Optional[str]` field. This is a data quality problem: downstream consumers of the classification API would receive an unexpected value. The correct fix depends on how strict we want to be. Option 1: define `category` as a Python `Enum` in the SQLModel — Pydantic will raise a `ValidationError` if the value does not match, which we can catch and treat as a classification failure. Option 2: add a post-parse validation step that maps unknown values to a fallback (e.g., `"General"`). Option 3: tighten the system prompt to enumerate allowed values explicitly and add a note that no other values are permitted. In production, a combination of prompt tightening and Pydantic enum validation is the most robust approach. This is a good example of why free-text LLM output requires defense-in-depth validation — even JSON mode does not guarantee semantic correctness.

---

## System Design and Trade-off Questions

### Q11. Why is the LLM classification call synchronous in this implementation? What are the trade-offs of making it async?

Expected answer:

In Session 4, the LLM call is synchronous — the HTTP request to the Gemini API blocks the FastAPI route handler until the response arrives, typically 500ms–2s. This is the simplest implementation and acceptable for a learning context. The trade-off is that high ticket creation throughput will saturate the FastAPI worker threads because each thread is blocked waiting for the API response. The correct production approach is to either: (a) make the LLM call async using the `google-generativeai` async methods with `await`, which allows FastAPI's async event loop to handle other requests while waiting; or (b) push the classification to a background job queue (e.g., Celery with Redis) so the `POST /tickets` response returns immediately with a `classification_status: "pending"` field, and the classification is written to the DB when the background worker completes. The background queue approach also provides retry logic for transient LLM failures. Both are valid; the right choice depends on the SLA for classification results.

### Q12. What would you change about this design if the system needed to support multiple LLM providers (Gemini, Ollama, Anthropic)?

Expected answer:

I would extract the LLM call behind an abstract interface — a Python `Protocol` or abstract base class `TicketClassifier` with a `classify(title: str, description: str) -> dict` method. Each provider would implement this interface: `GeminiClassifier`, `OllamaClassifier`, `AnthropicClassifier`. The route handler would depend on the interface, not the concrete implementation. The active provider would be selected via a configuration value (e.g., `LLM_PROVIDER=gemini` in `.env`). This pattern is sometimes called the Strategy pattern. It allows switching providers without touching the route or the DB logic. For Session 4, a single provider is correct because premature abstraction adds complexity without value. But in a production system with vendor risk, multi-provider support via this pattern is important.

### Q13. How would you redesign the classification system if classification needed to happen after ticket creation (asynchronously) rather than during the request?

Expected answer:

The `POST /tickets` route would save the ticket to the DB and return immediately with `HTTP 201`, including the ticket id but no classification fields (or with `classification_status: "pending"`). The classification would be triggered by publishing a message to a message queue — for example, `ticket.created` event to a Redis stream or Celery queue — containing the ticket id, title, and description. A worker process would consume the event, call the LLM, and write the `TicketClassification` row to the DB. Clients that need the classification would either poll `GET /tickets/{id}` until `classification_status` changes to `"complete"`, or subscribe to a webhook. This architecture is more complex but has significant advantages: the `POST /tickets` latency does not depend on the LLM (which might be slow or unavailable), and the classifier can be scaled independently, retried with exponential backoff, and monitored separately from the ticket creation service.

### Q14. What is graceful degradation in the context of this feature, and how is it implemented?

Expected answer:

Graceful degradation means the system continues to provide its core functionality (ticket creation and storage) even when a non-critical dependent subsystem (the LLM classifier) fails. Implementation requires three things: First, the ticket must be committed to the DB before the LLM call, not after — so a LLM failure cannot roll back the ticket. Second, the LLM call must be wrapped in a `try/except` that catches all relevant exceptions (`google.api_core.exceptions.PermissionDenied`, `google.api_core.exceptions.ResourceExhausted`, `json.JSONDecodeError`, network errors) and converts them into a logged warning rather than a raised exception. Third, the route handler must handle a `None` classification result gracefully — the response model must allow null classification fields. The result is that from the client's perspective, `POST /tickets` always returns 201 (unless the request body itself is invalid). The LLM failure is an internal concern, visible only in server logs and monitoring.

### Q15. What are the prompt engineering decisions you made for the classifier, and why do those decisions matter in production?

Expected answer:

Four key decisions: First, the role instruction — "You are a support ticket classification system" — establishes the task context and reduces off-topic responses. Second, explicit enumeration of allowed output values — "category must be exactly one of: Billing, Technical, Account, General" — constrains the output space and makes the model's job easier (it does not need to invent category names). This directly reduces out-of-distribution outputs. Third, the output format instruction — "return only the JSON object, no explanation, no markdown" — is necessary even with JSON mode because JSON mode prevents non-JSON output but does not prevent the model from adding keys or nesting the response. Fourth, type specifications — "urgency_score: integer between 1 and 10" — prevent the model from returning a float or a string. In production, prompt engineering is iterative: you log the actual LLM outputs, identify failure modes (wrong category, out-of-range scores, extra fields), and tighten the prompt based on observed data. Treating the system prompt as a versioned artifact (stored in code, not hardcoded as a string in a function) makes this iteration auditable.

---

# Session 4 Completion Checklist

Students should complete the following by the end of the session:

- [ ] `app/models/ticket_classification.py` exists with a valid SQLModel class and `ticket_id` foreign key
- [ ] `app/services/llm_classifier.py` exists with a `classify_ticket(title, description)` function
- [ ] The system prompt in `llm_classifier.py` specifies all six output fields with allowed values
- [ ] `response_mime_type="application/json"` is present in the Gemini `GenerationConfig`
- [ ] `temperature` is set to 0.1 or lower in the `GenerationConfig`
- [ ] `GEMINI_API_KEY` is loaded from environment variable, not hardcoded in source
- [ ] `.env` is in `.gitignore` — verify with `git status` showing `.env` is untracked
- [ ] `POST /tickets` in Swagger returns HTTP 201 with both ticket and classification fields populated
- [ ] `POST /tickets` still returns HTTP 201 when `GEMINI_API_KEY` is set to an invalid value (graceful degradation — classification fields are null)
- [ ] `SELECT * FROM ticketclassification;` shows a row linked to the created ticket
- [ ] `pytest tests/ -v` passes with at least one test for the LLM classifier using a mock
- [ ] Student can explain in 2 sentences what happens when the Gemini API is unreachable

---

# Instructor Backup Plan

If Gemini API access fails for the majority of students (key issues, quota exhaustion, network block):

1. Direct students to get a free Gemini API key at aistudio.google.com — it takes under 2 minutes and requires no credit card. This is the primary resolution path.
2. If aistudio.google.com is blocked on the network, switch to mock mode. Create a `MOCK_LLM=true` environment variable. In `llm_classifier.py`, check this flag and return hardcoded classification JSON without making an API call. Students build the full integration code and test the DB storage and response schema, even without a live LLM.
3. Continue the code walkthrough and interview prep regardless. The concepts — JSON mode via `response_mime_type`, temperature, graceful degradation, table separation — can be discussed from the code without running it.
4. Share the completed Session 4 reference code after the session so students can run it with their own keys.
5. Do not sacrifice the interview explanation and Q&A block. That section does not depend on the API working.
