# Session 7 After-Session Notes: Add Evals, Guardrails, and Testing

## What We Built Today

In Session 7, we added three quality control layers to the AI Support Ticket Resolution Copilot.

**Layer 1 — pytest API test suite:**
- `tests/conftest.py` — pytest fixture using `app.dependency_overrides` to replace the production database session with an in-memory SQLite engine for isolated test execution
- `tests/test_tickets.py` — 6+ test cases using `TestClient` covering `POST /tickets` (201), `GET /tickets/{id}` (200), `PUT /tickets/{id}` (200), `DELETE /tickets/{id}` (200/204), `GET /tickets/99999` (404), and `POST /tickets` with empty body (422)
- `tests/test_classifier.py` — test that calls `classify_ticket()` and asserts the returned dictionary has `category`, `priority`, and `summary` fields with valid values

**Layer 2 — Custom groundedness evaluation:**
- `app/evals/__init__.py` — package marker
- `app/evals/groundedness.py` — `evaluate_groundedness(response: str, retrieved_chunks: list[str]) -> dict` function that splits the response into sentences, checks word-level overlap against retrieved chunks, and returns `{"score": float, "unsupported_sentences": list[str]}`

**Layer 3 — Runtime guardrails:**
- Updated `app/graph/nodes.py` — `generate_node` now appends `GUARDRAIL_INSTRUCTIONS` to the existing system prompt and runs a post-generation trigger check that returns `SAFE_FALLBACK_RESPONSE` when violation patterns are detected
- `confidence_score` is now surfaced in the resolve endpoint response

---

# Why This Feature Matters for Production Systems

An AI system without tests, evals, and guardrails is a prototype, not a product. Here is what each layer protects against:

**Tests** catch regressions. When a developer changes the ticket schema, renames a field, or modifies a route handler, the pytest suite will fail within seconds and prevent a broken deployment. Without tests, a breaking change might only be discovered when a user reports a bug in production.

**Evals** catch quality degradation. When you upgrade the Gemini model, change the system prompt, add new documents to ChromaDB, or modify the retrieval chunk size, the groundedness score can drop significantly — meaning the LLM starts generating responses from its training data instead of from the retrieved context. Unit tests cannot detect this. Only an eval function that measures the semantic relationship between the response and the retrieved chunks can.

**Guardrails** catch unsafe runtime behavior. Even a well-tuned LLM can produce harmful output under adversarial input, unusual ticket text, or edge cases the system prompt did not anticipate. Guardrails provide a deterministic safety net that does not depend on the LLM's own judgment about whether its output is safe.

---

# System Architecture Flow — Sessions 1 Through 7

```
HTTP Request (POST /tickets/{id}/resolve)
  ↓
FastAPI app (app/main.py) — lifespan, CORS, router registration [Session 1]
  ↓
JWT Auth Middleware — validates Bearer token, extracts user from claims [Session 3]
  app/routes/auth.py → Depends(get_current_user) → decode JWT → load user from DB
  ↓
Route Handler (app/routes/tickets.py) [Sessions 1–2]
  GET /tickets, POST /tickets, PUT /tickets/{id}, DELETE /tickets/{id} — CRUD
  POST /tickets/{id}/resolve — triggers LangGraph workflow
  ↓
Database Layer (app/db/) [Session 2]
  SQLModel ORM → SQLite via SQLAlchemy engine
  get_session() dependency → yields Session
  Ticket table: id, title, description, status, category, priority, summary, created_at, updated_at
  ↓
LLM Classifier (app/llm/classifier.py) [Session 4]
  classify_ticket(ticket_text) → Gemini API (gemini-1.5-flash) generate_content with structured prompt
  Returns: {"category": str, "priority": str, "summary": str}
  ↓
LangGraph Workflow (app/graph/) [Session 6]
  graph.invoke(TicketState) — runs the 4-node compiled StateGraph
  ↓
  classify_node:
    calls classify_ticket() → sets state["category"], state["priority"], state["summary"]
  ↓
  retrieve_node:
    embeds ticket_text with sentence-transformers (all-MiniLM-L6-v2)
    queries ChromaDB collection → returns top N chunks + distances [Session 5]
    sets state["retrieved_chunks"], state["confidence"] (from similarity score)
  ↓
  route_node:
    if state["confidence"] >= CONFIDENCE_THRESHOLD → go to generate_node
    else → set state["response"] = LOW_CONFIDENCE_MESSAGE, END
  ↓
  generate_node [updated in Session 7]:
    system_prompt = BASE_SYSTEM_PROMPT + GUARDRAIL_INSTRUCTIONS
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": ticket_text + retrieved_chunks}]
    llm_response = llm.invoke(messages)
    if any(trigger in llm_response.lower() for trigger in GUARDRAIL_TRIGGERS):
        state["response"] = SAFE_FALLBACK_RESPONSE
    else:
        state["response"] = llm_response
    state["confidence_score"] = computed from ChromaDB distance
  ↓
Resolve Response: {answer, confidence_score, category, priority, summary}
  ↓
Offline Eval (app/evals/groundedness.py) [Session 7 — batch, not per-request]:
  evaluate_groundedness(response, retrieved_chunks)
  → {"score": 0.0–1.0, "unsupported_sentences": [...]}
  ↓
pytest test suite (tests/) [Session 7 — runs before deployment]:
  test_create_ticket → POST /tickets → assert 201
  test_get_ticket → GET /tickets/{id} → assert 200
  test_update_ticket → PUT /tickets/{id} → assert 200
  test_delete_ticket → DELETE /tickets/{id} → assert 200/204
  test_get_nonexistent_ticket → GET /tickets/99999 → assert 404
  test_create_ticket_missing_field → POST /tickets {} → assert 422
  test_classifier_returns_valid_fields → classify_ticket() → assert field types and enum values
```

---

# Technical Deep-Dive: LLM Evaluation, Groundedness, Guardrails, and pytest for AI Systems

## pytest with TestClient for FastAPI

FastAPI's `TestClient` wraps the ASGI app in a synchronous interface backed by `httpx`. When you call `client.post("/tickets", json={...})`, it passes the request through the entire FastAPI middleware and route handling stack without starting a real HTTP server. This means Pydantic validation, dependency injection, route logic, and exception handlers all execute exactly as they would in production. The key enabler is `app.dependency_overrides` — a dictionary on the FastAPI app instance where you can substitute any dependency with a replacement. By mapping `get_session` to a function that yields a session from an in-memory SQLite engine, you get full route coverage in isolated, reproducible tests that do not touch the production database. The fixture must use `scope="function"` and call `SQLModel.metadata.drop_all(engine)` before `create_all` to ensure each test starts with a clean schema. Forgetting this causes the second test to fail with `OperationalError: table already exists`.

## evaluate_groundedness — What It Measures and How

Groundedness is the property of an LLM response being traceable back to a specific piece of source material — in our case, the chunks retrieved from ChromaDB. The `evaluate_groundedness(response: str, retrieved_chunks: list[str]) -> dict` function operates at the sentence level because sentence-level attribution is the minimal meaningful unit for fact-checking. The function splits the response using sentence-boundary detection (period, question mark, exclamation mark followed by whitespace), removes stopwords from both the sentence and each chunk, and computes a word overlap fraction. A sentence is marked as supported if any chunk contains it as a direct substring or if the word overlap fraction exceeds `SUPPORTED_OVERLAP_THRESHOLD` (default 0.5). The final score is `supported_count / total_sentences`. A score of 1.0 means every sentence in the response is traceable to a retrieved chunk. A score of 0.3 means 70% of the response was generated from the LLM's parametric training data — which is a serious quality problem in a support system where policy accuracy is critical. The limitation of this approach is that it cannot handle semantic paraphrase: if the LLM rephrases a chunk sentence in different words, the overlap will be low even though the sentence is correctly grounded. Production systems replace this with embedding cosine similarity between each response sentence and each chunk, or use an NLI entailment model.

## Guardrails — System Prompt Layer and Post-Processing Layer

The guardrail in `generate_node` operates in two phases. The first phase is pre-generation: `GUARDRAIL_INSTRUCTIONS` is appended to the existing system prompt, not replacing it. This is important — the base system prompt defines the agent's role and context; the guardrail only adds constraints. The instructions tell the LLM to avoid referencing personal data of other users, to avoid making policy guarantees not supported by the retrieved context, and to decline off-topic requests. This reduces the probability of violations but does not eliminate it, because instruction-following is probabilistic in language models. The second phase is post-generation: after `llm.invoke()` returns, the output is scanned for trigger patterns stored in `GUARDRAIL_TRIGGERS`. These are deterministic string patterns (like `"@"` for email addresses, `"guarantee within"` for unsupported policy claims) that the LLM should not produce in a safe response. If any trigger is found, the entire response is replaced with `SAFE_FALLBACK_RESPONSE` — a constant defined at module level so it can be imported and tested independently. The `SAFE_FALLBACK_RESPONSE` replacement does not update the ticket status or write to the database; it only affects the HTTP response body returned to the caller. This is intentional: the database state should reflect what was attempted, not what the guardrail intercepted.

---

# What Students Should Understand

1. `app.dependency_overrides` is the canonical FastAPI pattern for replacing injected dependencies in tests — it works for databases, authentication, external service clients, or any other dependency

2. `TestClient` runs the full FastAPI stack in-process without a server — status codes, Pydantic validation errors (422), auth failures (401), and not-found errors (404) all work exactly as in production

3. `evaluate_groundedness` is an offline batch eval tool, not a per-request function — calling it on every request would add latency and it is not a hard blocker for the user response

4. The score returned by `evaluate_groundedness` is an approximation — string overlap misses semantic equivalence, which is why production systems use embedding similarity or NLI entailment models

5. The `confidence_score` in the API response comes from the ChromaDB retrieval similarity, not from the LLM — it is a measure of how well the retrieved documents match the question, not of how confident the LLM is about its answer

6. The two-layer guardrail (system prompt + post-processing) covers two different failure modes — prompt instruction failures and pattern-based violations — and neither layer alone is sufficient

7. `SAFE_FALLBACK_RESPONSE` must be a module-level constant so it can be tested deterministically — hardcoding it inline makes it impossible to assert in unit tests

8. Pytest fixture scope matters: `scope="function"` creates a fresh database per test; `scope="module"` reuses the database across a test module — using the wrong scope causes test interdependence and non-deterministic failures

9. The classifier test uses `pytest.mark.skipif` to conditionally skip when `GEMINI_API_KEY` is not set — this is the correct pattern for tests that depend on external services that may not be available in all environments

10. Session 7 features do not change the LangGraph graph topology, API routes, or database schema — they add a testing layer, an eval layer, and a safety layer on top of the existing architecture

---

# Interview-Ready Explanation

```text
In Session 7, I added three quality control layers to the AI Support Ticket Resolution Copilot. I wrote a pytest test suite using FastAPI's TestClient with a database dependency override that replaces the production SQLite session with an in-memory engine, giving me isolated, reproducible tests for all CRUD endpoints and the LLM classifier. I also implemented a custom evaluate_groundedness() function that splits LLM responses into sentences and checks word-level overlap against the retrieved ChromaDB chunks, returning a 0-to-1 score indicating how much of the response is supported by retrieved data rather than the model's training memory. Finally, I added a two-layer guardrail to the LangGraph generate node — a system prompt extension that instructs the LLM to avoid personal data, invented policy, and off-topic content, plus a deterministic post-processing check that replaces the response with a safe fallback message when trigger patterns are detected in the output.
```

---

# What Happens When POST /tickets/{id}/resolve Is Called

```text
1. The request hits FastAPI's auth middleware, which validates the JWT Bearer token. If invalid or missing, a 401 is returned immediately.

2. The route handler in app/routes/tickets.py loads the ticket from the database by ID using the SQLModel session. If the ticket does not exist, it returns 404.

3. The handler builds a TicketState TypedDict with ticket_text set to the ticket's description (and optionally title).

4. app.graph.graph.invoke(ticket_state) runs the compiled LangGraph StateGraph:
   a. classify_node calls classify_ticket(ticket_text) — a Gemini API (gemini-1.5-flash) generate_content call with a structured prompt — and sets category, priority, and summary in state.
   b. retrieve_node embeds the ticket text using sentence-transformers (all-MiniLM-L6-v2), calls collection.query() on the ChromaDB collection, retrieves the top N chunks, and computes confidence_score from the top document's cosine similarity score (1 - distance).
   c. route_node checks if confidence_score >= threshold. If yes, it routes to generate_node. If no, it sets a low-confidence fallback response and ends the graph.
   d. generate_node constructs messages with system_prompt = BASE_SYSTEM_PROMPT + GUARDRAIL_INSTRUCTIONS, calls llm.invoke() with the ticket text and retrieved chunks, checks the output for guardrail trigger patterns, and either returns the LLM response or SAFE_FALLBACK_RESPONSE.

5. The graph returns the final TicketState. The handler extracts the response, confidence_score, category, and priority.

6. The handler optionally updates the ticket record in the database with the resolved status, category, and priority.

7. The handler returns a JSON response with: answer, confidence_score, category, priority, summary.
```

---

# What AI Was Used For + What Engineers Must Still Do

## What AI (Antigravity) Was Used For

- Generating the `tests/conftest.py` fixture with the correct `dependency_overrides` pattern
- Generating the full `tests/test_tickets.py` test file with correctly scoped assertions
- Generating `app/evals/groundedness.py` with sentence splitting and word overlap logic
- Generating the `GUARDRAIL_INSTRUCTIONS` string content
- Generating the post-processing trigger check pattern in `generate_node`
- Suggesting the `SUPPORTED_OVERLAP_THRESHOLD` constant and `STOPWORDS` set

## What Engineers Must Still Do

- Verify that `app.dependency_overrides` is being cleared after each test — if not, test state leaks across modules
- Run `pytest tests/ -v` and read every failure message — AI-generated tests often use wrong field names or missing required fields that only become visible when the tests actually run
- Tune `SUPPORTED_OVERLAP_THRESHOLD` based on actual response quality — the default 0.5 may be too loose or too strict for the specific knowledge base content
- Define the actual `GUARDRAIL_TRIGGERS` list based on domain knowledge — AI will generate generic patterns; the engineer must add domain-specific violation patterns relevant to the support use case
- Decide when to call `evaluate_groundedness` — AI will not make this architectural decision; the engineer must determine whether it runs as a nightly batch job, on sampled traffic, or on flagged tickets
- Ensure `SAFE_FALLBACK_RESPONSE` wording is reviewed by a product or legal stakeholder before production deployment
- Verify the `confidence_score` computation is correct for the specific ChromaDB metric used (L2 vs. cosine) — the distance-to-score conversion differs between them
- Write the `tests/test_classifier.py` skipif condition with the correct environment variable name used by the project

---

# Common Issues and Fixes

## Issue 1: `ModuleNotFoundError: No module named 'app'` when running pytest

This happens when pytest is run from inside the `app/` directory or when the project root is not in `PYTHONPATH`. Python cannot resolve `from app.main import app` because it cannot find the `app` package relative to the current working directory.

Fix: Run pytest from the project root with `PYTHONPATH` set:

```bash
export PYTHONPATH=.
pytest tests/ -v
```

Alternatively, add a `pytest.ini` or `pyproject.toml` at the project root with `pythonpath = .` under `[tool.pytest.ini_options]` so you do not need to export `PYTHONPATH` each time.

What to ask AI:

```text
My pytest tests fail with ModuleNotFoundError: No module named 'app'. My project structure has app/ and tests/ as siblings at the project root. How do I configure PYTHONPATH correctly? Show me the correct pytest.ini or pyproject.toml configuration to fix this permanently. Do not suggest moving files.
```

---

## Issue 2: `AssertionError: assert 422 == 201` on `test_create_ticket`

This happens when the `VALID_TICKET_BODY` dictionary in the test is missing a required field from the `TicketCreate` Pydantic schema. FastAPI validates the request body before calling the route handler and returns a 422 Unprocessable Entity if validation fails.

Fix: Print `response.json()` in the test before the assertion to see the exact validation error:

```python
print(response.json())  # shows {"detail": [{"loc": ["body", "title"], "msg": "field required", ...}]}
assert response.status_code == 201
```

Then update `VALID_TICKET_BODY` to include all required fields listed in the validation error. Common missing fields: `title`, `description`.

What to ask AI:

```text
My test_create_ticket is returning 422 instead of 201. The response body is: [paste response.json() output here]. My TicketCreate schema is in app/db/models.py. Please identify which fields are required and show me the corrected VALID_TICKET_BODY dictionary for the test.
```

---

## Issue 3: Guardrail system prompt replaces the original system prompt

This happens when the `generate_node` code sets `system_prompt = GUARDRAIL_INSTRUCTIONS` instead of appending to the existing prompt. The original base system prompt that defines the agent's role and context is overwritten, causing the LLM to only see the guardrail instructions and producing off-topic or confused responses.

Symptom: The resolve endpoint returns valid JSON but the `answer` field contains a meta-response like "I am a customer support AI and cannot..." instead of an actual resolution.

Fix: Change the assignment from replacement to concatenation:

```python
# Wrong:
system_prompt = GUARDRAIL_INSTRUCTIONS

# Correct:
system_prompt = base_system_prompt + "\n\n" + GUARDRAIL_INSTRUCTIONS
```

Where `base_system_prompt` is the original prompt string already defined in `generate_node`.

What to ask AI:

```text
My generate_node guardrail is overwriting the original system prompt instead of appending to it. The LLM now returns generic responses about being a support AI instead of actual resolutions. Show me how to correctly append GUARDRAIL_INSTRUCTIONS to the existing base_system_prompt variable without replacing it. The existing system prompt is defined as a multi-line string in generate_node.
```

---

# Key Takeaways

1. **Tests, evals, and guardrails serve different failure modes and cannot substitute for each other.** A passing pytest suite only means the API contract is correct. It says nothing about the quality or safety of the LLM output. Evals measure output quality. Guardrails enforce runtime safety. All three are required.

2. **Groundedness is the primary quality metric for RAG systems, not accuracy.** In a retrieval-augmented system, the model should not use its training knowledge to answer questions — it should use the retrieved documents. A grounded response can be verified against source material. An ungrounded response cannot be audited or corrected because its source is unknown. This is why `evaluate_groundedness` is more meaningful than measuring BLEU score or response length.

3. **FastAPI's dependency injection system makes the app testable by design.** The `app.dependency_overrides` pattern is not a hack — it is the intended mechanism for test isolation in FastAPI applications. Any dependency (database session, auth user, external client) can be replaced in tests without modifying route code. This is a direct benefit of designing with dependency injection rather than global state.

4. **Confidence score and guardrail trigger rate are the two most important operational metrics for this system.** A declining confidence score indicates knowledge base gaps or retrieval degradation. A rising guardrail trigger rate indicates either adversarial input patterns or a regression in the LLM's instruction-following behavior. Both should be tracked in a monitoring dashboard before production deployment.

---

# Session 8 Preview

In Session 8, we will deploy the AI Support Ticket Resolution Copilot and conduct the final system design walkthrough and mock interview.

**Session 8 includes:**

- Containerizing the FastAPI backend with Docker — writing a `Dockerfile` and `docker-compose.yml`
- Configuring production environment variables (`.env` management, secrets handling)
- Deploying to a cloud platform (Railway, Render, or similar)
- Final end-to-end system verification on the deployed URL
- Full system design walkthrough covering all 7 sessions of the build — architecture decisions, trade-offs, and what you would change in a production system
- Mock interview: 10–15 technical questions covering the complete project from CRUD to guardrails

**What to prepare before Session 8:**

- Review your `requirements.txt` — ensure all dependencies are pinned with versions
- Know your project's entry point command (`uvicorn app.main:app --host 0.0.0.0 --port 8000`)
- Be ready to explain every component of the system in 60 seconds or less
- Review Session 7 interview questions, especially Q11–Q15 (system design trade-offs)

Session 8 is the final session. By the end of it, you will have a live deployed AI backend with a public URL that you can reference in interviews and add to your portfolio.
