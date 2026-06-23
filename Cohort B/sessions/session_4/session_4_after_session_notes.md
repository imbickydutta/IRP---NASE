# Session 4 After-Session Notes: Add LLM Ticket Classifier

## What We Built Today

In Session 4 we extended the AI Support Ticket Resolution Copilot backend with LLM-powered ticket classification.

The new components built today:

- `app/models/ticket_classification.py` — SQLModel table `TicketClassification` with `ticket_id` foreign key, storing `category`, `priority`, `sentiment`, `urgency_score`, `summary`, and `suggested_team`
- `app/services/llm_classifier.py` — `classify_ticket(title, description)` function that calls the OpenAI Chat Completions API with a structured system prompt, `response_format={"type": "json_object"}`, and `temperature=0.1`
- Updated `app/routes/tickets.py` — `POST /tickets` now saves the ticket, calls the classifier, saves the classification, and returns both in the response
- Updated response schema — `TicketReadWithClassification` Pydantic model with an optional nested `ClassificationOut` model
- pytest tests using `unittest.mock.patch` to mock the OpenAI client, covering the success path and the graceful degradation path

The feature degrades gracefully: if the LLM call fails for any reason, the ticket saves successfully and the classification fields in the response are `null`.

---

# Why This Feature Matters for Production Systems

Manual ticket triaging is a hidden operational cost. In a support team handling hundreds of tickets per day, agents spend 20–30% of their time classifying and routing tickets before any resolution work begins. An LLM classifier that runs automatically on ticket creation eliminates this overhead — every ticket arrives at the queue already categorized, prioritized, and routed to the correct team.

The design choices made in Session 4 reflect real production engineering concerns. The classifier runs synchronously in the ticket creation flow because Session 4 is a learning context — but the `try/except` wrapper and separate DB table are already production-correct patterns. The `TicketClassification` table as a separate entity (not columns on `Ticket`) means classification can be regenerated, versioned, or updated without touching the ticket record. The use of JSON mode and explicit system prompt constraints means the output is machine-readable without regex parsing, making it safe to store and forward to downstream systems.

From a business perspective, `urgency_score` and `priority` enable queue ordering — the highest urgency tickets appear at the top for human agents. `suggested_team` enables automatic routing. `sentiment` enables escalation triggers — a ticket with `sentiment: Angry` and `priority: Critical` might automatically page an on-call engineer. None of this requires human classification. It all depends on the structured output we built today being reliable and consistent.

---

# System Architecture Flow — Session 1 Through Session 4

```
Client Request: POST /tickets (Bearer token in Authorization header)
     |
     v
[FastAPI App: app/main.py]                               [Session 1]
  - Router registration
  - SQLModel.metadata.create_all(engine) on startup
     |
     v
[JWT Auth Middleware: app/core/auth.py]                  [Session 3]
  - Authorization header decoded
  - JWT verified with SECRET_KEY
  - sub (user_id) and role extracted from token claims
  - get_current_user dependency injects current user into route
  - 401 returned if token is missing, expired, or invalid
     |
     v
[Pydantic Validation: TicketCreate schema]               [Session 2]
  - Request body validated
  - 422 returned if required fields are missing or wrong type
     |
     v
[DB Write — Ticket: app/db/session.py]                   [Session 2]
  - Ticket SQLModel instance created
  - current_user.id assigned as user_id
  - session.add(ticket) → session.commit() → session.refresh(ticket)
  - ticket.id is now assigned (DB-generated integer)
     |
     v
[LLM Classifier: app/services/llm_classifier.py]         [Session 4 — NEW]
  - classify_ticket(title, description) called
  - OpenAI client initialized (reads OPENAI_API_KEY from env)
  - chat.completions.create() sends HTTP POST to api.openai.com
    with model, temperature=0.1, response_format=json_object, messages
  - response.choices[0].message.content is a JSON string
  - json.loads() parses it to dict
  - try/except catches all failures → returns None on any error
     |
     +-- success path:
     |   [DB Write — TicketClassification]                [Session 4 — NEW]
     |     - TicketClassification instance created
     |     - ticket_id = ticket.id (FK reference)
     |     - session.add(classification) → session.commit()
     |
     +-- failure path:
         - Warning logged
         - classification = None
         - Route continues without blocking
     |
     v
[Response: TicketReadWithClassification]                 [Session 4 — NEW]
  - 201 returned with ticket fields + classification fields
  - classification fields are null if LLM call failed
     |
     v
[RAG Knowledge Base: ChromaDB]                           [Session 5 — coming next]
  - Ticket description embedded as a vector
  - ChromaDB queried for semantically similar past resolutions
  - Relevant knowledge articles attached to response
     |
     v
[LangGraph Resolution Agent]                             [Session 6 — coming later]
  - Classification + RAG results used as agent context
  - Agent suggests and executes resolution steps
```

---

# Technical Deep-Dive: LLM API Integration, Structured JSON Output, and Prompt Engineering

The OpenAI Chat Completions API (`chat.completions.create`) accepts a list of messages where each message has a `role` (`system`, `user`, or `assistant`) and `content` (a string). The `system` message sets the persistent instruction context for the model — everything in it is treated as the model's operating instructions, not as user input. For classification, the system message does the heavy lifting: it defines the task, the output structure, and the constraints. The `user` message contains the actual ticket content to classify. The model processes both and generates a response that satisfies the system instructions applied to the user content. Setting `response_format={"type": "json_object"}` is a strict API-level guarantee — the model's output will be a valid JSON string that can be parsed with `json.loads()` without catching `json.JSONDecodeError` from structural issues. Note that JSON mode only guarantees syntactic validity, not semantic correctness — the model can still return `"category": "Payment"` (wrong value) even if the JSON is valid. That is why explicit enumeration of allowed values in the system prompt, combined with post-parse validation in Python, is the production-correct approach.

Temperature deserves careful treatment because it is frequently misunderstood. The raw value is a divisor applied to the model's logit scores before the softmax that converts logits to probabilities. A lower temperature sharpens the probability distribution — the highest-probability token becomes even more dominant relative to alternatives. At `temperature=0`, the model becomes fully deterministic (always greedy): it picks the single most probable token at every step. At `temperature=1`, the raw logit-derived probabilities are used unchanged. For a classification task with four categories — Billing, Technical, Account, General — the probability gap between the correct category and the next most likely one is typically large if the ticket description is clear. Low temperature ensures we always pick the dominant answer rather than occasionally sampling a lower-probability alternative. The practical effect: with `temperature=0.1`, ten identical requests should produce identical responses. With `temperature=0.9`, there will be variance across repeated calls for ambiguous inputs.

Graceful degradation is an architectural principle: the core feature must not fail because of an enhancement. In this implementation, the ticket commit happens before the LLM call — this is not accidental, it is intentional. If the LLM call and classification commit were inside a single DB transaction with the ticket, a LLM failure would roll back the ticket insert. That would be catastrophic for a support system — a customer submits a ticket and it disappears because OpenAI had a brief outage. By committing the ticket first and treating the LLM call as a best-effort post-commit step, we guarantee that every submitted ticket is persisted. The `try/except` wrapper around the LLM call converts any exception into a `None` return, which the route handler treats as "no classification available." The response model declares classification as `Optional`, so Pydantic serializes `None` as `null` in the JSON response rather than raising a `ValidationError`. Every layer of this chain was designed with the degradation scenario in mind.

---

# What Students Should Understand

1. The `openai` Python library v1.x uses `OpenAI()` client instantiation, not `openai.ChatCompletion.create()`. Any code using the old style will fail with `AttributeError` or `ImportError`. Check the installed version with `pip show openai`.

2. `response_format={"type": "json_object"}` guarantees syntactically valid JSON from the model. It does not guarantee the JSON contains the expected fields or expected values. System prompt design and post-parse validation in Python are still required.

3. The ticket must be committed to the database before the `TicketClassification` row can be inserted. SQLite and PostgreSQL both enforce foreign key constraints — inserting a `TicketClassification` row with a `ticket_id` that does not yet exist in the `ticket` table raises `IntegrityError`.

4. API keys must never be hardcoded in source files. The `openai` library reads `OPENAI_API_KEY` from the process environment automatically. `python-dotenv` with `load_dotenv()` populates the environment from a `.env` file that is excluded from git via `.gitignore`.

5. `temperature=0.1` is appropriate for classification because consistency across identical inputs is more important than output variety. High temperature is appropriate for creative tasks; low temperature is appropriate for deterministic tasks with a fixed output space.

6. `TicketClassification` as a separate table — not columns on `Ticket` — is a deliberate normalization and extensibility decision. It reflects that classification is optional, recomputable, and may grow with new fields independently of the core ticket entity.

7. `json.loads()` on the model response is always required. `response.choices[0].message.content` is always a Python `str`. JSON mode guarantees it is a valid JSON string, but it is still a string — not a dict.

8. The `try/except` block in `classify_ticket` should catch specific OpenAI exceptions (`openai.AuthenticationError`, `openai.RateLimitError`, `openai.APIConnectionError`) before a broad `except Exception`. Specific exception types make log messages more actionable and allow different recovery strategies per error type.

9. Mocking the OpenAI client in pytest with `unittest.mock.patch` is the standard approach for testing LLM-integrated code in CI pipelines. Tests that make real API calls are slow, expensive, non-deterministic, and will fail in environments without API access.

10. Urgency score type coercion is necessary in practice. LLMs sometimes return numeric values as strings (`"8"` instead of `8`) despite explicit type instructions in the system prompt. Adding `int(float(result.get("urgency_score", 5)))` with range clamping is a one-line defense against this class of type inconsistency.

---

# Interview-Ready Explanation

```text
In Session 4, I integrated LLM-powered ticket classification into the POST /tickets endpoint of a FastAPI backend. When a ticket is created, the backend calls the OpenAI Chat Completions API with a structured system prompt and response_format=json_object, which forces the model to return a valid JSON object containing six classification fields: category, priority, sentiment, urgency_score, summary, and suggested_team. The classification result is stored in a dedicated TicketClassification SQLModel table linked to the ticket via a foreign key, and returned alongside the ticket in the 201 response. The entire LLM call is wrapped in a try/except block, and the ticket is committed to the database before the LLM call executes, so a classifier failure never blocks ticket creation — this is the graceful degradation pattern.
```

---

# What Happens When POST /tickets Is Called

```text
When POST /tickets is called with a valid Bearer token and a valid request body:

1. FastAPI parses the Authorization header and calls get_current_user, which decodes the JWT, extracts the user id, and queries the DB for the User. If the token is invalid or expired, a 401 is returned immediately.

2. The request body is deserialized into a TicketCreate Pydantic model. If any required field is missing or has the wrong type, a 422 is returned with field-level error details.

3. A Ticket SQLModel instance is created with the validated data and current_user.id as user_id. session.add(ticket) and session.commit() write the row to the ticket table. session.refresh(ticket) loads the DB-assigned ticket.id back into the Python object.

4. classify_ticket(ticket.title, ticket.description) is called. Inside, the OpenAI client sends a POST request to https://api.openai.com/v1/chat/completions with model="gpt-4o-mini", temperature=0.1, response_format={"type": "json_object"}, and a messages list containing the system prompt and user message with the ticket content.

5. The API responds with a JSON body. response.choices[0].message.content is extracted as a string and passed to json.loads(), producing a Python dict with category, priority, sentiment, urgency_score, summary, and suggested_team.

6. A TicketClassification instance is created with ticket_id=ticket.id and all six classification fields. session.add(classification) and session.commit() write it to the ticket_classification table.

7. If any step in 4–6 raises an exception, it is caught, a warning is logged, and classification is set to None. The ticket row written in step 3 is unaffected.

8. The route handler constructs a TicketReadWithClassification response, combining ticket fields and classification fields (or null classification). HTTP 201 is returned.
```

---

# What AI Was Used For + What Engineers Must Still Do

## What the AI Coding Tool Generated

- The `TicketClassification` SQLModel table with all fields and FK constraint
- The `classify_ticket` function body including the `OpenAI` client initialization, the `chat.completions.create` call, and `json.loads`
- The initial system prompt content
- The `try/except` structure around the LLM call
- The updated `POST /tickets` route handler with classification integration
- The `TicketReadWithClassification` and `ClassificationOut` Pydantic response models
- The pytest test file with mocked OpenAI calls

## What Engineers Are Still Responsible For

1. **Reviewing the system prompt critically** — Is it specific enough? Are all six fields documented? Are allowed values enumerated? Does it say "return only JSON"? The AI generates a reasonable first version; the engineer must audit it against real ticket samples.

2. **Verifying the commit order** — The ticket commit must happen before the LLM call. AI tools sometimes generate code that wraps everything in one transaction. Verify manually that `session.commit()` for the ticket precedes `classify_ticket()`.

3. **Testing graceful degradation explicitly** — Set `OPENAI_API_KEY` to an invalid value and verify that `POST /tickets` still returns 201 with `null` classification. This is not tested automatically by the AI-generated tests unless you asked for it.

4. **API key security audit** — Check every file the AI modified or created. Verify no key is hardcoded anywhere. Verify `.env` is in `.gitignore`. Run `git status` to confirm `.env` is not tracked.

5. **Reviewing exception specificity** — AI tools tend to generate `except Exception` as a catch-all. Replace it with specific OpenAI exception types (`openai.AuthenticationError`, `openai.RateLimitError`, `openai.APIConnectionError`) for more informative logs.

6. **Adding urgency_score type coercion** — AI-generated code may trust the model to return an integer. Production code should coerce and clamp: `max(1, min(10, int(float(val))))`.

7. **Validating allowed values post-parse** — AI-generated code may skip this. Add explicit validation that `category`, `priority`, `sentiment`, and `suggested_team` contain values from the allowed sets, with fallbacks for unexpected values.

8. **Testing with real ticket content** — Run the live endpoint with diverse ticket descriptions. Verify the classifier returns correct and consistent categories across multiple runs. Identify prompt weaknesses from real outputs.

---

# Common Issues and Fixes

## Issue 1: `ImportError: cannot import name 'OpenAI' from 'openai'`

This means `openai` version 0.28.x or older is installed. The v1.x package introduced the `OpenAI()` client class. Code using `openai.ChatCompletion.create(...)` is the old style.

What to ask AI:

```text
I am getting "ImportError: cannot import name 'OpenAI' from 'openai'". My installed version is 0.28.x.

Update my app/services/llm_classifier.py to use the openai v1.x client API style. The new style uses:

from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(...)

Replace any old-style openai.ChatCompletion.create() calls with the new pattern. Also update requirements.txt to specify openai>=1.0.0.
```

## Issue 2: `sqlalchemy.exc.IntegrityError: FOREIGN KEY constraint failed` on TicketClassification insert

The TicketClassification row is being inserted with a `ticket_id` that does not yet exist in the `ticket` table. This happens when `classify_ticket` is called before `session.commit()` for the ticket, or when `ticket.id` is `None` because the ticket was not refreshed after commit.

What to ask AI:

```text
I am getting "sqlalchemy.exc.IntegrityError: FOREIGN KEY constraint failed" when saving the TicketClassification in my POST /tickets route.

Here is my current route handler code: [paste the relevant section]

Fix the commit order so that:
1. session.add(ticket) is called
2. session.commit() is called — this writes the ticket row and assigns ticket.id
3. session.refresh(ticket) is called — this loads ticket.id into the Python object
4. classify_ticket(ticket.title, ticket.description) is called AFTER step 3
5. If classification succeeds, TicketClassification is created with ticket_id=ticket.id
6. session.add(classification) and session.commit() are called

Show me the corrected route handler with comments marking each step.
```

## Issue 3: `POST /tickets` returns 201 but `classification` key is missing from the response body

The response model (`response_model` on the route decorator) is still set to the old `TicketRead` schema, which does not include classification fields. Pydantic serializes only the fields declared in the response model and silently drops everything else.

What to ask AI:

```text
My POST /tickets endpoint returns 201 successfully, but the response JSON does not include a "classification" key at all — not even as null.

I have a TicketReadWithClassification Pydantic model that includes an optional ClassificationOut field. But the route decorator still has response_model=TicketRead.

Update the POST /tickets route decorator to use response_model=TicketReadWithClassification. Also ensure the route handler constructs and returns a TicketReadWithClassification instance, not a plain Ticket SQLModel instance. Show me the corrected route decorator and the last few lines of the route handler where the response is built and returned.
```

---

# Key Takeaways

1. **JSON mode is mandatory for structured LLM output in production.** Free-text parsing of LLM responses using regex or string splitting is fragile and breaks on minor model updates. `response_format={"type": "json_object"}` is a guaranteed contract at the API level. Combine it with a tightly-written system prompt that enumerates allowed values and specifies types — and add post-parse validation in Python for defense-in-depth.

2. **Commit order is a correctness requirement, not just a style preference.** In any multi-step database flow where rows reference each other via foreign keys, the parent row must be committed before the child row is inserted. In the Session 4 flow, Ticket is the parent and TicketClassification is the child. Getting this order wrong causes an `IntegrityError` that is misleading to debug if you do not understand the FK constraint being violated.

3. **Graceful degradation requires deliberate design at every layer.** It is not enough to add a `try/except` block. The ticket commit must be outside the error handler, the response model must declare classification as `Optional`, and the route handler must handle `None` classification without raising a `KeyError` or `AttributeError`. Each of these is a distinct decision, and each must be implemented correctly for the degradation to actually work.

4. **Prompt engineering is iterative, version-controlled work.** The first version of the system prompt you write is not the production-ready version. Log the actual LLM outputs for 20–30 real tickets. Identify the failure modes: wrong category values, out-of-range urgency scores, incorrect priority assignments, vague summaries. Update the prompt based on observed failures. Treat the system prompt as a versioned artifact stored in code, not a string buried in a function. In production systems, prompt versions are tracked alongside code changes so that classification behavior changes are auditable.

---

# Session 5 Preview

In Session 5 we will add the RAG Knowledge Base.

The backend will maintain a vector store (ChromaDB) containing support articles, past ticket resolutions, and internal documentation. When a ticket is created, the ticket description will be embedded using OpenAI's `text-embedding-3-small` model, and ChromaDB will be queried for the most semantically similar knowledge entries. The top results will be attached to the ticket response as `suggested_resolutions`.

Session 5 will introduce:
- `chromadb` Python client and collection management
- OpenAI Embeddings API (`embeddings.create`)
- Cosine similarity and why it is the right distance metric for semantic search
- ChromaDB `collection.query(query_embeddings=..., n_results=3)` return structure
- A new `KnowledgeArticle` SQLModel table for storing article metadata
- Embedding stored per article at insert time, queried at ticket creation time
- Updated `POST /tickets` response with a `suggested_resolutions` list

The classification fields built in Session 4 — particularly `category` and `priority` — will be used in Session 5 as metadata filters in the ChromaDB query: `where={"category": classification.category}`. This will narrow the semantic search to knowledge articles relevant to the same category as the ticket, improving the precision of RAG results.

Before Session 5:
- Read the Session 5 pre-session file
- Understand what an embedding vector is and why higher-dimensional vectors capture more semantic meaning
- Install ChromaDB: `pip install chromadb`
- Understand cosine similarity conceptually: two vectors are similar if the angle between them is small, regardless of their magnitude
