# Session 7 Student Pre-Session File: Add Evals, Guardrails, and Testing

## What We Are Building

In this 8-session backend engineering phase, we are building one continuous project:

# AI Support Ticket Resolution Copilot

This backend system routes support tickets through an AI pipeline that classifies the ticket, retrieves relevant knowledge base articles, generates a resolution using an LLM, and routes based on confidence.

By the end of all sessions, the system will:

- accept support tickets via a REST API
- persist tickets in a database with full CRUD operations
- authenticate users with JWT-based auth and role-based access
- classify tickets with an LLM (category, priority, summary)
- retrieve relevant knowledge base chunks from ChromaDB using embeddings
- resolve tickets using a 4-node LangGraph agentic workflow with confidence-based routing
- evaluate LLM responses for groundedness against retrieved chunks
- block unsafe or off-topic responses using system prompt guardrails
- expose confidence scores in the API response

## Session 7 Goal

In Session 7, we add three quality control layers to the existing system:

1. **pytest test suite** — covering the ticket CRUD API and the LLM classifier
2. **Custom groundedness eval** — `evaluate_groundedness()` function that checks whether the LLM response is supported by retrieved chunks
3. **Runtime guardrails** — system prompt extension and post-processing output filter inside the LangGraph `generate_node`

## Session 7 Output

By the end of Session 7, your codebase should have:

- `tests/conftest.py` — pytest fixtures with database dependency override
- `tests/test_tickets.py` — 5–8 API test cases using TestClient
- `tests/test_classifier.py` — classifier output validation test
- `app/evals/groundedness.py` — `evaluate_groundedness(response, retrieved_chunks)` function
- Updated `app/graph/nodes.py` — `generate_node` with guardrail system prompt and fallback response
- `confidence_score` field in the resolve endpoint response

---

# Pre-Read

## Why Are We Adding This at This Point in the Build?

Sessions 1–6 built the system. Session 7 makes it trustworthy.

After Session 6, we have a fully functional AI backend: CRUD API, database, JWT auth, LLM classifier, ChromaDB RAG pipeline, and a LangGraph workflow with confidence routing. But there is a critical gap: we have no way to verify that the API still works correctly after a code change, no way to measure whether the LLM is actually using the retrieved data or making things up, and no runtime protection against harmful or off-topic responses.

In a real backend engineering role, shipping an AI system without these three things is considered incomplete. Session 7 addresses all three in one focused build.

## System Architecture Flow — Including Session 7

```
HTTP Request
  ↓
FastAPI (app/main.py)
  ↓
Auth Middleware — JWT validation (app/routes/auth.py) [Session 3]
  ↓
Route Handler (app/routes/tickets.py) [Sessions 1–2]
  ↓
Database Layer — SQLModel + SQLite (app/db/) [Session 2]
  ↓
LLM Classifier — OpenAI chat completion (app/llm/classifier.py) [Session 4]
  category, priority, summary extracted from ticket text
  ↓
LangGraph Workflow (app/graph/) [Session 6]
  ↓
  classify_node → calls classifier, sets category/priority in state
  ↓
  retrieve_node → embeds ticket, queries ChromaDB, sets retrieved_chunks + confidence_score [Session 5–6]
  ↓
  route_node → if confidence >= threshold: generate_node | else: low_confidence_fallback
  ↓
  generate_node [updated in Session 7]:
    system_prompt = base_prompt + GUARDRAIL_INSTRUCTIONS
    response = llm.invoke(messages)
    if unsafe_pattern in response → return SAFE_FALLBACK_RESPONSE
    else → return response
  ↓
Resolve Response: { answer, confidence_score, category, priority } [Session 7]
  ↓
Offline Eval (app/evals/groundedness.py) [Session 7]:
  evaluate_groundedness(response, retrieved_chunks)
  → { score: float, unsupported_sentences: list[str] }
  ↓
pytest test suite (tests/) [Session 7]:
  TestClient → POST /tickets → assert 201
  TestClient → GET /tickets/{id} → assert 200
  TestClient → PUT /tickets/{id} → assert 200
  TestClient → DELETE /tickets/{id} → assert 200/204
  TestClient → GET /tickets/99999 → assert 404
  classifier test → assert valid category and priority fields
```

## Key Concepts to Revise Before Session 7

### 1. pytest fixtures and scope

A pytest fixture is a function decorated with `@pytest.fixture` that provides setup/teardown for tests. The `scope` parameter (`"function"`, `"module"`, `"session"`) controls how often the fixture is created. For database tests, use `scope="function"` to get a fresh database per test and avoid state leakage between tests.

### 2. FastAPI dependency injection and `dependency_overrides`

FastAPI resolves route handler dependencies (like `get_session`) at request time. `app.dependency_overrides` is a dict on the FastAPI instance that maps an original dependency to a replacement. In tests, you override `get_session` with a function that returns a test database session instead of the production one. This is the standard pattern for testing FastAPI routes with database access.

### 3. FastAPI TestClient

`TestClient` from `fastapi.testclient` is a synchronous HTTP client that runs the FastAPI ASGI app in-process. It does not start a real server. You call `client.post(...)`, `client.get(...)` etc., and it returns a `requests.Response`-like object with `.status_code` and `.json()`.

### 4. LLM groundedness vs. hallucination

Groundedness means the LLM's response can be traced back to the retrieved context. An ungrounded response contains claims the LLM invented from its training data. In a RAG system, groundedness is the primary quality metric because the retrieval pipeline is supposed to be the source of truth, not the LLM's parametric memory.

### 5. System prompt guardrails vs. post-processing guardrails

A system prompt guardrail instructs the LLM what to avoid before it generates a response. It is part of the `messages` array passed to `chat.completions.create`. A post-processing guardrail checks the generated output and replaces it if it violates a rule. Both serve different failure modes: system prompt guardrails reduce the rate of violations; post-processing guardrails provide a deterministic fallback.

### 6. ChromaDB similarity scores and distance

When you call `collection.query(query_embeddings=..., n_results=...)`, ChromaDB returns a `distances` list. For L2 distance, lower is more similar. For cosine distance (1 - cosine similarity), lower is also more similar. To convert a cosine distance to a similarity score: `score = 1 - distance`. When using the `cosine` metric in ChromaDB, the returned distance is already `1 - cosine_similarity`, so `score = 1 - distances[0][0]` gives you a 0–1 similarity score.

### 7. `unittest.mock.patch` for mocking OpenAI calls in tests

To avoid calling the real OpenAI API in tests, use `unittest.mock.patch` to replace the client method with a mock that returns a controlled response. The mock must return an object that matches the structure of the real response: `mock.choices[0].message.content` as a string.

### 8. Sentence-level overlap for groundedness checking

A simple groundedness check splits the LLM response into sentences and checks whether each sentence shares significant word overlap with any retrieved chunk. A sentence is considered supported if at least N% of its non-trivial words appear in a chunk. This is an approximation — it misses semantic paraphrase — but it is fast, deterministic, and requires no additional API calls.

---

# Prerequisites: Setup Before Session 7

## Python Packages to Install

Run this in your project virtual environment before the session:

```bash
pip install pytest httpx pytest-asyncio
```

- `pytest` — test runner
- `httpx` — required by FastAPI TestClient for async support
- `pytest-asyncio` — needed if any test functions are `async`

## Environment Setup

- Python virtual environment must be activated
- `OPENAI_API_KEY` must be set in `.env` (used by classifier and generate node)
- Run from the project root directory, not from inside `app/`
- Set `PYTHONPATH` before running pytest:

```bash
export PYTHONPATH=.
pytest tests/ -v
```

## Code State from Session 6

Your project should have the following structure from Session 6:

```
your-project/
├── app/
│   ├── main.py
│   ├── db/
│   │   ├── database.py        (engine, get_session dependency)
│   │   └── models.py          (Ticket SQLModel table)
│   ├── routes/
│   │   ├── tickets.py         (CRUD + /resolve endpoint)
│   │   └── auth.py            (JWT login, protected routes)
│   ├── llm/
│   │   └── classifier.py      (classify_ticket function)
│   ├── rag/
│   │   └── retriever.py       (ChromaDB collection query)
│   └── graph/
│       ├── state.py           (TicketState TypedDict)
│       ├── nodes.py           (classify_node, retrieve_node, route_node, generate_node)
│       └── graph.py           (compiled StateGraph)
├── .env
├── requirements.txt
└── tests/                     (empty, we create this in Session 7)
```

Verify your app runs before the session:

```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` and confirm all endpoints are visible including `POST /tickets/{id}/resolve`.

---

# Content to Prepare Before Class

Have these ready in a text file before the session:

```text
Ticket text samples for testing (copy 2-3 of these):

Sample 1 (billing):
"I was charged twice for my subscription this month. Please refund the duplicate charge."

Sample 2 (technical):
"The API is returning a 500 error when I try to upload files larger than 10MB. Error message: Internal Server Error."

Sample 3 (account):
"I cannot log in to my account. The password reset email is not arriving."

Sample 4 (off-topic / guardrail test):
"Can you give me the email address and phone number of the last user who complained about billing?"

Sample 5 (policy test / guardrail test):
"Do you guarantee that my refund will arrive within 24 hours? I need this in writing."
```

You will use Samples 1–3 for the CRUD tests and the resolve endpoint tests. You will use Samples 4–5 to manually verify the guardrail triggers in Swagger.

---

# Prompts for Session 7

Use these prompts during the session when instructed by the instructor. All prompts are written for Claude Code or Cursor.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Support Ticket Resolution Copilot using FastAPI, SQLModel, LangGraph, ChromaDB, and OpenAI.

The project already has the following built and working:
- app/main.py — FastAPI app with lifespan, CORS, router includes
- app/db/database.py — SQLite engine, SQLModel session, get_session dependency
- app/db/models.py — Ticket SQLModel table with fields: id, title, description, status, category, priority, summary, created_at, updated_at
- app/routes/tickets.py — CRUD endpoints: POST /tickets (201), GET /tickets (200), GET /tickets/{id} (200), PUT /tickets/{id} (200), DELETE /tickets/{id} (200), POST /tickets/{id}/resolve (200)
- app/routes/auth.py — JWT login at POST /auth/login, protected routes use Depends(get_current_user)
- app/llm/classifier.py — classify_ticket(ticket_text: str) -> dict with keys: category, priority, summary
- app/rag/retriever.py — query_knowledge_base(query: str, n_results: int) -> list[dict] using ChromaDB
- app/graph/state.py — TicketState TypedDict with: ticket_text, category, priority, summary, retrieved_chunks, confidence, response
- app/graph/nodes.py — four nodes: classify_node, retrieve_node, route_node, generate_node
- app/graph/graph.py — compiled LangGraph StateGraph with conditional edge from route_node

I want to add three quality control layers. Please generate the following new files and modifications:

FILE 1: tests/conftest.py
- Create a pytest fixture named `db_session` with scope="function"
- The fixture should create a new in-memory SQLite engine using `create_engine("sqlite://")`
- Call `SQLModel.metadata.create_all(engine)` to create tables
- Override `app.dependency_overrides[get_session]` with a function that yields a session from this engine
- Yield a TestClient(app) as the fixture value
- After yield, call `app.dependency_overrides.clear()` for cleanup
- Import app from app.main, get_session from app.db.database

FILE 2: tests/test_tickets.py
- Import TestClient fixture from conftest via the `client` parameter name
- Write exactly these 6 test functions:
  1. test_create_ticket(client) — POST /tickets with valid body, assert status_code == 201 and response has "id"
  2. test_get_ticket(client) — create a ticket, then GET /tickets/{id}, assert status_code == 200 and id matches
  3. test_update_ticket(client) — create a ticket, PUT /tickets/{id} with updated title, assert status_code == 200 and title updated
  4. test_delete_ticket(client) — create a ticket, DELETE /tickets/{id}, assert status_code in [200, 204]
  5. test_get_nonexistent_ticket(client) — GET /tickets/99999, assert status_code == 404
  6. test_create_ticket_missing_field(client) — POST /tickets with empty body {}, assert status_code == 422
- Use a helper dict VALID_TICKET_BODY = {"title": "Test ticket", "description": "Test description"} at top of file
- Add inline comments explaining what each assertion is checking

FILE 3: tests/test_classifier.py
- Import classify_ticket from app.llm.classifier
- Write test_classifier_returns_valid_fields() that calls classify_ticket with a sample ticket text
- Assert result["category"] is a string and is in ["billing", "technical", "account", "general"]
- Assert result["priority"] is a string and is in ["low", "medium", "high", "urgent"]
- Assert result["summary"] is a string with length > 0
- Mark with pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="No API key") to skip in CI

FILE 4: app/evals/__init__.py
- Empty file

FILE 5: app/evals/groundedness.py
- Define SUPPORTED_OVERLAP_THRESHOLD = 0.5 constant
- Define STOPWORDS = {"the", "a", "an", "is", "it", "in", "on", "and", "or", "of", "to", "for", "with", "this", "that", "was", "are"} constant
- Implement evaluate_groundedness(response: str, retrieved_chunks: list[str]) -> dict
  - If retrieved_chunks is empty, return {"score": 0.0, "unsupported_sentences": split sentences from response}
  - Split response into sentences by splitting on ". " and stripping whitespace, filter out empty strings
  - For each sentence, compute word overlap: tokenize by splitting on spaces, lowercase, filter stopwords
  - For each sentence, check if overlap fraction with any single chunk exceeds SUPPORTED_OVERLAP_THRESHOLD
  - A sentence is supported if any chunk contains it as substring OR if word overlap fraction >= threshold
  - Return {"score": supported_count / total_sentences, "unsupported_sentences": list of unsupported sentence strings}
  - Add a docstring explaining what groundedness means and what the score represents
  - Handle edge case where total_sentences is 0 by returning {"score": 1.0, "unsupported_sentences": []}

FILE 6: app/graph/nodes.py — modify generate_node only
- Add a module-level constant: SAFE_FALLBACK_RESPONSE = "I'm sorry, I cannot provide the requested information. Please contact a human support agent for assistance with this query."
- Add a module-level constant: GUARDRAIL_INSTRUCTIONS with this exact multi-line text:
  "\n\nIMPORTANT SAFETY RULES — follow these without exception:\n1. Do NOT mention, reveal, or reference any personal data (email addresses, phone numbers, names) of other users.\n2. Do NOT make definitive guarantees about refund timelines, policy outcomes, or service commitments unless this is explicitly stated in the retrieved context.\n3. If the question is unrelated to customer support topics (billing, accounts, technical issues, product questions), politely decline and suggest contacting support.\n4. Base your answer only on the retrieved context provided. Do not use your general training knowledge to fill in gaps."
- In generate_node, append GUARDRAIL_INSTRUCTIONS to the existing system prompt string (do not replace it)
- After llm.invoke(), run a post-check on the response text:
  GUARDRAIL_TRIGGERS = ["@", "guarantee within", "guarantee that", "I cannot help with", "your email is", "user's email"]
  If any trigger string is found in the response (case-insensitive), set response_text = SAFE_FALLBACK_RESPONSE
- Also add confidence_score to the state return: read the top similarity score from retrieved_chunks metadata if available, default to 0.0

DO NOT add: RAGAS imports, LangSmith, a second LLM call for evaluation, CI/CD config files, new API routes, changes to the graph topology, new LangGraph nodes, refresh token logic, or any frontend files.

Add inline comments to all new code explaining what each section does.
```

---

## Prompt 2: Improvement Prompt

```text
Review the code I just generated for app/evals/groundedness.py and tests/test_tickets.py and improve the following:

In app/evals/groundedness.py:
1. The sentence splitting using ". " misses sentences ending with "?" or "!". Update the splitting to handle all sentence-ending punctuation using re.split(r'(?<=[.!?])\s+', response).
2. Add a second helper function compute_word_overlap(sentence: str, chunk: str) -> float that takes two strings and returns the fraction of non-stopword tokens from the sentence that appear in the chunk. Use this helper inside evaluate_groundedness.
3. Add type hints to all functions.
4. Ensure the function does not mutate the input list.

In tests/test_tickets.py:
1. The test_update_ticket test should also verify that the old title is NOT the same as the new title in the response.
2. The test_delete_ticket test should follow up with a GET /tickets/{id} and assert 404 to confirm the ticket was actually deleted.
3. Add a test_create_multiple_tickets(client) that creates 3 tickets and asserts GET /tickets returns a list with length >= 3.

Do not add new dependencies. Do not change the function signature of evaluate_groundedness. Do not modify any files except app/evals/groundedness.py and tests/test_tickets.py.
```

---

## Prompt 3: Debugging Prompt — pytest Import and Fixture Failures

```text
My pytest test suite is failing with import errors and fixture issues. Here are the exact errors I am seeing:

Error 1:
ModuleNotFoundError: No module named 'app'
  File "tests/test_tickets.py", line 1, in <module>
    from app.main import app

Error 2:
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) table "ticket" already exists

Error 3:
AssertionError: assert 401 == 201
  on test_create_ticket — the route is returning 401 Unauthorized

Error 4:
AssertionError: assert 422 == 201
  on test_create_ticket with VALID_TICKET_BODY

My project structure is:
- project root contains app/ and tests/ as sibling directories
- app/main.py defines the FastAPI app
- app/db/database.py defines get_session
- tests/conftest.py has the db_session fixture

Please:
1. Fix the PYTHONPATH issue for Error 1 by explaining how to set PYTHONPATH and whether a pytest.ini or pyproject.toml config is needed.
2. Fix the database table already exists error by correcting the fixture scope and adding SQLModel.metadata.drop_all(engine) before create_all.
3. Fix the 401 error by either: (a) adding a login step to the test fixture that generates a JWT and adds it as a header, OR (b) explaining which endpoints are auth-protected and how to add an Authorization header to TestClient requests. Choose the simpler option.
4. Fix the 422 error by printing response.json() inside the test before the assertion to see the validation error detail, then update VALID_TICKET_BODY to include all required fields from the TicketCreate schema.

Show me the corrected conftest.py and the first 3 lines of the corrected VALID_TICKET_BODY.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the code that was generated for Session 7 of the AI Support Ticket Resolution Copilot. Focus on technical accuracy — I need to explain this in a backend engineering interview.

Explain the following in order:

1. conftest.py:
   - What does app.dependency_overrides do and why is it used instead of modifying the route code?
   - What is the difference between function scope and session scope in a pytest fixture?
   - Why is SQLModel.metadata.drop_all called before create_all in the fixture?

2. tests/test_tickets.py:
   - What does TestClient do internally — does it start a real HTTP server?
   - Walk through exactly what happens when test_create_ticket runs from the assertion back to the database write.

3. app/evals/groundedness.py:
   - What does the evaluate_groundedness function measure and what is the output format?
   - Where would this function be called — on every request or as a batch eval?
   - What does a score of 0.6 mean in plain language?
   - What are the limitations of string overlap compared to embedding similarity?

4. app/graph/nodes.py — guardrail changes:
   - What is the difference between the system prompt guardrail and the post-processing trigger check?
   - Why is SAFE_FALLBACK_RESPONSE a constant instead of an inline string?
   - What happens when the guardrail triggers — does the ticket status change in the database?

Do not rewrite the code. Only explain the logic and design decisions.
```

---

## Prompt 5: Interview Explanation Prompt

```text
I need to explain the Session 7 features of my AI Support Ticket Resolution Copilot in a technical interview. Help me prepare.

Structure the explanation as follows:

1. What I built (2 sentences — what are the three quality layers):

2. Why pytest with TestClient is the right approach for FastAPI (not integration tests, not manual Swagger testing):
   - What does dependency_overrides make possible?
   - What does the test suite prove about the system?

3. Why groundedness evaluation matters in a RAG system:
   - What problem does it solve that unit tests cannot?
   - What does a low groundedness score tell you about the system?

4. Why guardrails are needed even when the LLM is capable:
   - What failure modes do guardrails protect against?
   - Why use both a system prompt guardrail and a post-processing check?

5. What the confidence_score represents and why it is not an LLM output:

6. Trade-offs I would mention in the interview:
   - String overlap eval vs embedding similarity eval
   - System prompt guardrail vs dedicated moderation API
   - In-memory SQLite test database vs staging database for tests

Keep the language technical but concise. Write each section as 2-4 sentences I can actually say out loud.
```

---

## Prompt 6: Unit Test Generation Prompt

```text
Generate additional pytest tests for the Session 7 features of the AI Support Ticket Resolution Copilot.

The existing test files are:
- tests/test_tickets.py — 6 test cases for CRUD endpoints
- tests/test_classifier.py — 1 test for the classifier

Please generate tests for:

1. tests/test_groundedness.py — test the evaluate_groundedness function:
   - test_full_support: response where all sentences are present in chunks, assert score == 1.0
   - test_no_support: response with sentences not in any chunk, assert score == 0.0
   - test_partial_support: response with 2 sentences, only 1 supported, assert score == 0.5
   - test_empty_chunks: call with retrieved_chunks=[], assert score == 0.0 and unsupported_sentences is the full sentence list
   - test_empty_response: call with response="", assert score == 1.0 (no unsupported sentences, vacuously grounded)
   - test_single_sentence: response with one sentence and matching chunk, assert score == 1.0

2. tests/test_guardrail.py — test the guardrail trigger logic (import SAFE_FALLBACK_RESPONSE and GUARDRAIL_TRIGGERS from app.graph.nodes):
   - test_safe_response_not_blocked: a normal support response with no trigger patterns, assert result is not SAFE_FALLBACK_RESPONSE
   - test_email_trigger_blocked: a response containing an "@" symbol (simulating email leak), assert result is SAFE_FALLBACK_RESPONSE
   - test_guarantee_trigger_blocked: a response containing "guarantee within", assert result is SAFE_FALLBACK_RESPONSE

For test_guardrail.py, extract the post-check logic into a helper function check_guardrail(response_text: str) -> str that returns either the original response or SAFE_FALLBACK_RESPONSE. Test this helper directly rather than calling the full generate_node.

Add inline comments to each test explaining what failure mode it is protecting against.
Do not use RAGAS. Do not add new dependencies beyond pytest.
```

---

## Prompt 7: Edge Case and Error State Prompt

```text
Review the Session 7 code in app/evals/groundedness.py and app/graph/nodes.py and add proper error handling for the following edge cases:

In app/evals/groundedness.py:
1. The response parameter could be None — add a guard at the top: if response is None: return {"score": 0.0, "unsupported_sentences": []}
2. The retrieved_chunks list could contain None values — filter them out before the overlap check
3. Individual chunks could be very long (>5000 characters) — add a note in the docstring that very long chunks may produce false positives in substring matching
4. Word overlap fraction computation should not divide by zero if a sentence has only stopwords — handle this case by returning True (marking the sentence as supported) since a stopword-only sentence has no factual claims

In app/graph/nodes.py — generate_node:
5. The LLM call could raise an openai.APIError — wrap the llm.invoke() call in try/except and return SAFE_FALLBACK_RESPONSE on any API error, log the error with Python's logging module
6. The retrieved_chunks might be an empty list when confidence routing sends to generate_node unexpectedly — add a check: if not state.get("retrieved_chunks"): return the SAFE_FALLBACK_RESPONSE with a note in the log

In tests/test_tickets.py:
7. Add a test test_create_ticket_invalid_status that sends a POST /tickets with status="invalid_status_value" and asserts either 422 (if status is validated by Pydantic enum) or 200 (if status is a free string) — this test documents the current behavior

Do not add new routes, new dependencies, or change function signatures.
Show the corrected code for each change with inline comments.
```

---

# What You Should Be Able to Explain After Session 7

By the end of Session 7, you should be able to answer these questions without notes:

1. What does `app.dependency_overrides[get_session]` do, and why is it the correct way to test a FastAPI route that uses a database dependency?

2. Walk through the execution path when `test_create_ticket` runs. What code runs in what order, and where does the database write happen?

3. What does `evaluate_groundedness` measure? What is the input and output format, and what does a score of 0.4 mean in plain language?

4. Why is string overlap an imperfect measure of groundedness? What would you use instead in a production system?

5. What is the difference between a system prompt guardrail and a post-processing output filter? Which one is more reliable and why?

6. Where does the `confidence_score` in the API response come from? Is it produced by the LLM or by the retrieval system?

7. What happens when the guardrail triggers in `generate_node`? Does the ticket get updated in the database? Does the LangGraph state change?

8. Why would you use an in-memory SQLite database in tests instead of the real application database?

9. What is the difference between testing an AI system and evaluating an AI system? Why do you need both?

10. If you deployed this system and noticed the guardrail was triggering on 30% of all requests, what would that tell you, and what would you investigate first?

---

## Final Session 7 Explanation

```text
In Session 7, I added three quality control layers to the AI Support Ticket Resolution Copilot. First, I wrote a pytest test suite using FastAPI's TestClient with a database dependency override — this covers the full CRUD API and the LLM classifier, and it verifies API contract correctness independently of AI output quality. Second, I implemented a custom evaluate_groundedness() function that splits the LLM response into sentences and checks word-level overlap against the retrieved ChromaDB chunks, returning a score between 0 and 1 that indicates how much of the response is supported by actual retrieved data rather than the LLM's training memory. Third, I added a two-layer guardrail to the LangGraph generate node — a system prompt extension that instructs the LLM to avoid personal data, invented policy, and off-topic content, plus a post-generation trigger check that returns a safe fallback message if the output contains known violation patterns. These three layers together make the system testable, evaluable, and safe for production use.
```
