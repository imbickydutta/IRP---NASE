# Session 7 Instructor File: Add Evals, Guardrails, and Testing

## Session Title

Add Evals, Guardrails, and Testing

## Duration

2 hours

## Project

AI Support Ticket Resolution Copilot

## Session 7 Objective

By the end of Session 7, students will have added three layers of quality control to the AI Support Ticket Resolution Copilot: a pytest suite covering the CRUD API and LLM classifier, a custom groundedness evaluation function for the RAG pipeline, and a system prompt guardrail layer inside the LangGraph generate node that blocks unsafe or off-topic responses.

Students will understand the difference between unit testing, AI evaluation, and runtime guardrails — and why all three are required in production AI systems.

## Session 7 Deliverable

Students will add to the existing FastAPI + LangGraph project:

1. `tests/test_tickets.py` — pytest test file using FastAPI TestClient covering create, get, update, and delete ticket endpoints (5–8 test cases)
2. `tests/test_classifier.py` — pytest test verifying the LLM classifier returns a valid category, priority, and summary
3. `app/evals/groundedness.py` — `evaluate_groundedness(response: str, retrieved_chunks: list[str]) -> dict` function that returns a score and a list of unsupported sentences
4. Guardrail logic added inside `app/graph/nodes.py` in the `generate_node` — a system prompt addition that instructs the LLM not to leak personal data, not to invent policy, and not to respond to off-topic questions, plus a fallback response pattern when the guardrail triggers
5. `confidence_score` field computed from retrieval similarity scores and stored in the ticket response

---

## Strict Scope Control

### Include

- pytest with `TestClient` for CRUD endpoint tests (5–8 test cases across create, get, update, delete)
- `pytest` fixture using an in-memory SQLite database or test database override
- LLM classifier test that mocks or calls the classifier and asserts field types and valid enum values
- `evaluate_groundedness()` using sentence-level string overlap or cosine similarity on embeddings (without RAGAS)
- Guardrail system prompt appended to the existing generate node system prompt
- Fallback response string returned when guardrail condition is detected post-generation
- `confidence_score` derived from the top retrieval similarity score already returned by ChromaDB
- Clear inline comments in all new files explaining what each assertion or check does

### Do Not Include

- RAGAS library installation or usage
- LangSmith tracing or remote eval dashboards
- A second LLM judge call to score faithfulness (too expensive per call)
- CI/CD pipeline configuration (GitHub Actions, Docker testing)
- Load testing or performance benchmarks
- Property-based testing with hypothesis
- Refresh token rotation or any new auth changes
- New LangGraph nodes or changes to the 4-node graph topology
- New API endpoints beyond what already exists
- Any frontend changes or Swagger customization

---

# Instructor Framing

## Opening Message

In the previous six sessions, we built a complete AI backend: a FastAPI CRUD API with JWT auth, a database layer with SQLModel, an LLM classifier, a RAG knowledge base with ChromaDB, and a 4-node LangGraph agentic workflow with confidence-based routing.

Today we are not adding a new AI feature. We are making the existing system trustworthy.

There are three things that make an AI system production-ready beyond the happy path: tests that verify the API behaves correctly under code changes, eval functions that verify the AI output is actually grounded in retrieved data, and guardrails that prevent the LLM from generating harmful or incorrect responses at runtime.

These are not optional. Any backend engineer deploying an AI system to real users must have all three.

## Key Philosophy

Writing code is not enough. Writing code you can verify, evaluate, and protect is what separates a student project from a production system. Today we will add verification, evaluation, and protection as first-class engineering concerns — not afterthoughts.

## Repeated Instructor Line

An AI system with no tests, no evals, and no guardrails is not a product. It is a prototype.

---

# Session Flow

## 0–10 min: Opening and Recap of Session 6

### Instructor Goal

Reestablish the current codebase state and frame today's session as the quality layer, not a new feature layer.

### Recap Session 6 State

Walk through the codebase briefly and confirm the following are in place from Session 6:

- `app/graph/nodes.py` — four nodes: `classify_node`, `retrieve_node`, `generate_node`, `route_node`
- `app/graph/graph.py` — the compiled LangGraph StateGraph with conditional edges based on confidence routing
- `app/graph/state.py` — `TicketState` TypedDict with fields: `ticket_text`, `category`, `priority`, `retrieved_chunks`, `confidence`, `response`
- `app/routes/tickets.py` — CRUD routes plus the `/tickets/{id}/resolve` endpoint that invokes the graph
- `app/routes/auth.py` — JWT login and protected routes
- `app/db/models.py` — `Ticket` SQLModel table with `status`, `category`, `priority`, `summary` fields
- `app/db/database.py` — SQLite engine and session dependency

### State Check Command

Tell students to run `pytest --collect-only` and confirm no test files exist yet. Then run `uvicorn app.main:app --reload` and hit `/docs` to confirm the app is running.

### Frame Session 7

Today we add three things in parallel tracks:
1. API tests with pytest and TestClient
2. RAG eval with a custom groundedness function
3. Runtime guardrails inside the generate node

---

## 10–20 min: Architecture Breakdown — What Are We Adding and Why

### Instructor Goal

Draw the three quality layers clearly on a whiteboard or shared screen before touching code.

### Whiteboard Diagram — Three Quality Layers

```
Layer 1: pytest (test time)
  TestClient → POST /tickets → assert status 201, assert id in response
  TestClient → GET /tickets/{id} → assert ticket returned
  TestClient → LLM classifier mock → assert category in ["billing", "technical", "account", "general"]

Layer 2: RAG Eval (evaluation time)
  evaluate_groundedness(response, retrieved_chunks)
    → splits response into sentences
    → checks each sentence against retrieved chunks (overlap or similarity)
    → returns {"score": 0.75, "unsupported_sentences": [...]}

Layer 3: Guardrails (runtime, inside generate_node)
  system_prompt += guardrail_instructions
  LLM generates response
  post-check: if "personal data" or "we guarantee" or off-topic marker detected
    → return SAFE_FALLBACK_RESPONSE
  else → return response
```

### Key Teaching Points

- Layer 1 (pytest) catches regressions in API behavior. It runs before deployment.
- Layer 2 (groundedness eval) tells you whether the LLM is making up answers or actually using the retrieved context. It runs offline as an eval pass.
- Layer 3 (guardrails) is a runtime safety net. It runs every time a user sends a message.
- All three serve different purposes. Replacing one with another is a mistake.

### Ask Students

Why can't pytest catch a hallucination? Why can't a guardrail catch a regression in the delete endpoint? Pause for answers. These are the exact questions that appear in system design interviews.

---

## 20–35 min: Build the Feature Using Antigravity

### Instructor Goal

Use Prompt 1 from the student pre-session file to generate the full feature using Antigravity. Instructor runs this live on screen.

### Pre-Prompt Checklist

Before running the prompt, confirm with students:
- The file structure matches what the prompt expects (`app/graph/nodes.py`, `app/routes/tickets.py`, etc.)
- `pytest` and `httpx` are installed (`pip install pytest httpx`)
- A `tests/` directory exists or will be created by the prompt

### What to Watch For During Generation

- Does the test file import `TestClient` from `fastapi.testclient`?
- Does the conftest.py or fixture override the database dependency correctly?
- Does `evaluate_groundedness` return a `dict` with `score` (float) and `unsupported_sentences` (list)?
- Is the guardrail added as a string appended to the existing system prompt, not as a replacement?
- Is there a `SAFE_FALLBACK_RESPONSE` constant defined?
- Does the confidence score computation use the distance or score value from ChromaDB results?

### Instructor Control Rule

Do not let AI generate a full CI/CD pipeline, RAGAS imports, or a second LLM judge. If the prompt produces these, show students how to identify and remove out-of-scope additions.

---

## 35–50 min: Instructor Code Walkthrough — Read Generated Code, Explain Each Part

### Instructor Goal

Walk through every generated file and explain the technical reasoning behind each decision.

### Walkthrough: tests/conftest.py

- Show the `pytest.fixture` that creates a fresh in-memory SQLite engine
- Explain `app.dependency_overrides[get_session] = override_get_session`
- This is the FastAPI dependency injection override pattern — it replaces the real DB session with a test session for all routes during testing
- Ask: why do we use a separate database for tests and not the real one?

### Walkthrough: tests/test_tickets.py

- Show the `TestClient(app)` initialization
- Walk through each test: `test_create_ticket`, `test_get_ticket`, `test_update_ticket`, `test_delete_ticket`
- Point out `assert response.status_code == 201` for create and `assert response.status_code == 200` for get
- Point out that the test for delete checks `status_code == 204` or `200` depending on implementation
- Show the `test_get_nonexistent_ticket` test asserting `status_code == 404`

### Walkthrough: app/evals/groundedness.py

- Walk through the `evaluate_groundedness` function signature: `(response: str, retrieved_chunks: list[str]) -> dict`
- Show the sentence splitting using `response.split(".")` or a simple regex
- Show the overlap check: for each sentence, check if any significant substring appears in any chunk
- Explain the score: `supported_count / total_sentence_count`
- Explain why this is approximate but useful without a second LLM call

### Walkthrough: app/graph/nodes.py — generate_node changes

- Show the guardrail system prompt addition as a multi-line string appended to the existing system prompt
- Show the `SAFE_FALLBACK_RESPONSE` constant
- Show the post-generation check that looks for trigger phrases in the LLM output
- Explain that this is a post-processing guardrail, not a pre-filtering guardrail

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run Prompt 1 from the pre-session file in their own Antigravity environment and generate the same feature.

### Instructor Support Areas

Watch for and help with:

- Import error: `ModuleNotFoundError: No module named 'httpx'` — fix with `pip install httpx`
- Import error: `from app.main import app` fails because `PYTHONPATH` is not set — fix with `export PYTHONPATH=.` or run `pytest` from the project root
- Database fixture not overriding correctly — check that `app.dependency_overrides` is being set before `TestClient` is initialized
- `evaluate_groundedness` imported incorrectly into test or route — check the `app/evals/__init__.py` is present
- Guardrail system prompt accidentally replacing the original system prompt instead of appending to it

### If Student Setup Fails

Do not block the class. The student should follow the instructor screen, note what was generated, and replicate after the session using the prompts.

---

## 65–80 min: Test and Improve — Run Tests, Test in Swagger, Handle Edge Cases

### Instructor Goal

Run the full pytest suite live and iterate on failures in real time.

### Run Commands

```bash
export PYTHONPATH=.
pytest tests/ -v
```

### Expected Output

```
tests/test_tickets.py::test_create_ticket PASSED
tests/test_tickets.py::test_get_ticket PASSED
tests/test_tickets.py::test_update_ticket PASSED
tests/test_tickets.py::test_delete_ticket PASSED
tests/test_tickets.py::test_get_nonexistent_ticket PASSED
tests/test_classifier.py::test_classifier_returns_valid_fields PASSED
```

### If Tests Fail

Walk through failure messages live. Common failures:
- `AssertionError: assert 422 == 201` — the request body is missing a required field. Check the Pydantic schema.
- `AssertionError: assert 401 == 201` — the test is hitting an auth-protected route without a token. Either add a login fixture or mark the test endpoint as exempt.
- `sqlalchemy.exc.OperationalError: table tickets already exists` — the test fixture is not creating a fresh engine per test. Fix the fixture scope to `function`.

### Test in Swagger

Start the app and open `/docs`. Hit the `/tickets/{id}/resolve` endpoint and inspect the response for the `confidence_score` field. Show students how to manually verify the guardrail by submitting a ticket that asks for a user's personal email address.

---

## 80–95 min: Error Handling and Edge Cases

### Instructor Goal

Add robustness to the new eval and guardrail code.

### Edge Cases to Cover

1. `evaluate_groundedness` called with an empty `retrieved_chunks` list — should return `{"score": 0.0, "unsupported_sentences": [all sentences]}`
2. `evaluate_groundedness` called with a single-word response — should not crash on sentence splitting
3. Guardrail triggered by a partially unsafe response — the full response is blocked, not just the unsafe sentence
4. Classifier test called when `GEMINI_API_KEY` is not set — should fail gracefully with a clear error, not a silent `None` return
5. `confidence_score` is `None` when ChromaDB returns zero results — handle with `score = 0.0` default
6. TestClient sending a `POST /tickets` with an empty body — assert `422 Unprocessable Entity`
7. TestClient sending a `GET /tickets/99999` where that ID does not exist — assert `404 Not Found`

### Improvement Prompt

Use Prompt 2 from the student file to refactor the groundedness function and add missing edge case handling.

---

## 95–105 min: Concept Pause — LLM Evaluation, Groundedness, Guardrails, and pytest for AI Systems

### Instructor Goal

Convert the implementation into clear interview-ready mental models.

### Explain the Four Concepts

**pytest for AI Systems**

pytest with TestClient tests the API contract. It verifies that the HTTP layer behaves correctly: status codes, response shapes, and database side effects. It does not test whether the AI output is good — only that the endpoints work. This is the same as testing any REST API.

**Groundedness**

Groundedness measures whether the LLM response is supported by the retrieved context. A grounded response uses facts from the chunks. An ungrounded response invents facts. We measure this by checking how many sentences in the response can be found in or are semantically similar to the retrieved chunks. A score of 1.0 means every sentence is supported. A score of 0.0 means the response is entirely made up.

**Guardrails**

A guardrail is a constraint added to the LLM interaction that prevents specific categories of bad output. System prompt guardrails instruct the LLM what not to do before generation. Post-processing guardrails check the output after generation and replace it if it violates a rule. We use both: the system prompt tells the LLM to avoid personal data and invented policy, and the post-check catches anything that slipped through.

**Confidence Score**

The confidence score in our system comes from the ChromaDB retrieval similarity score — specifically the cosine similarity between the query embedding and the top retrieved chunk embedding. A high score (close to 1.0) means the retrieved chunk is very similar to the question. A low score means the retrieval was uncertain. In the LangGraph workflow from Session 6, this score is already used for routing. Now we surface it in the API response so users can see how confident the system is.

### System Flow Diagram

```
POST /tickets/{id}/resolve
  ↓
Auth middleware (JWT)
  ↓
LangGraph graph.invoke(ticket_state)
  ↓
  classify_node → category, priority, summary
  ↓
  retrieve_node → retrieved_chunks, confidence_score (from ChromaDB similarity)
  ↓
  route_node → high confidence: generate_node | low confidence: fallback
  ↓
  generate_node:
    system_prompt = base_prompt + guardrail_instructions
    llm_response = llm.invoke(messages)
    if unsafe_pattern in llm_response:
        return SAFE_FALLBACK_RESPONSE
    return llm_response
  ↓
response includes: answer, confidence_score, category, priority
  ↓
evaluate_groundedness(response, retrieved_chunks) — called offline in eval pass
```

### Student Writing Task

Ask every student to write in 2–3 sentences: what is the difference between a guardrail and a unit test? What does each one protect against?

---

## 105–115 min: Interview Discussion and Technical Viva Practice

### Instructor Goal

Use the interview questions section below. Pick 4–5 questions per session depending on group speed. Focus on the technical deep-dive questions for this cohort.

### Delivery Method

Ask the question, wait 30 seconds, ask one student, correct and add detail, ask the group if they agree.

---

## 115–120 min: Wrap-Up and Session 8 Preview

### Instructor Closing

Today we added the three quality layers that make a production AI system trustworthy. We have tests that verify the API contract, an eval function that measures whether the LLM is actually using the retrieved data, and guardrails that protect users from harmful or incorrect responses at runtime.

In Session 8, we will deploy this application. We will containerize the FastAPI backend with Docker, configure environment variables for production, deploy to a cloud platform, and conduct a full system design walkthrough and mock interview covering all 7 sessions of the build.

---

# Instructor Notes

## What to Emphasize

Session 7 is the quality and safety session. Emphasize:

1. pytest with TestClient is the standard pattern for testing FastAPI — students should be comfortable with `app.dependency_overrides`, fixture scoping, and asserting status codes
2. The `evaluate_groundedness` function is intentionally simple — it uses string overlap, not a full embedding similarity pipeline. Make sure students understand why this is a reasonable trade-off for a student project and where it would break in production
3. The guardrail is not magic — it is a carefully worded system prompt plus a post-check. Students should understand the difference between pre-generation guardrails (system prompt) and post-generation guardrails (output filter)
4. `confidence_score` comes from ChromaDB's similarity score, not from the LLM. This is a critical distinction that will come up in interviews
5. Pytest fixtures with dependency override are one of the most commonly tested FastAPI patterns in backend interviews
6. The `SAFE_FALLBACK_RESPONSE` should be a constant, not hardcoded strings scattered across the generate node
7. Students should know the difference between `distance` and `score` in ChromaDB — lower distance = higher similarity, or the collection may return scores directly depending on configuration

## Common Student Mistakes

1. **`ModuleNotFoundError: No module named 'app'` when running pytest** — students run `pytest` from inside the `app/` directory instead of the project root. Fix: `cd` to project root and run `export PYTHONPATH=.` before pytest.

2. **`AssertionError: assert 422 == 201` on `test_create_ticket`** — the test POST body is missing a required field defined in the Pydantic `TicketCreate` schema. Students need to check the schema and update the test request body to include all required fields.

3. **`AssertionError: assert 401 == 201` on `test_create_ticket`** — the route is protected by JWT auth and the test is not sending an `Authorization` header. Fix: create a test login fixture that generates a token, or temporarily test with a route that does not require auth (document the trade-off).

4. **`sqlalchemy.exc.OperationalError: table "ticket" already exists`** — the pytest fixture is creating the database once and not resetting between tests. Fix: use `function` scope on the fixture and call `SQLModel.metadata.drop_all(engine)` before `create_all`.

5. **Guardrail system prompt replaces original system prompt** — students write `system_prompt = guardrail_instructions` instead of `system_prompt = base_prompt + "\n\n" + guardrail_instructions`. The original context gets erased and the LLM stops knowing what it is supposed to do.

6. **`evaluate_groundedness` crashes on single-sentence responses** — `response.split(".")` on `"OK."` returns `["OK", ""]`, and the empty string causes a false unsupported sentence. Fix: filter out empty strings after splitting.

7. **`confidence_score` is a ChromaDB distance, not a similarity** — ChromaDB with L2 distance returns lower values for more similar documents. Students may invert the interpretation. If using `cosine` metric, values closer to 1.0 are more similar. Clarify which metric the collection was created with in Session 5.

8. **The classifier test calls the real Gemini API** — if `GEMINI_API_KEY` is not set in the test environment, the test raises an authentication error. Fix: either mock the Gemini client with `unittest.mock.patch` or use `pytest.mark.skipif` when the key is not present.

9. **`evaluate_groundedness` not called in any route** — students implement it but never wire it into the resolve endpoint or leave it only as a standalone script. Clarify that it is an offline eval function, not a per-request call, and show how to run it as a batch eval script.

10. **Test file imports fail because `tests/__init__.py` is missing** — `from app.routes.tickets import router` fails inside the test if Python cannot resolve the package. Fix: ensure `tests/__init__.py` exists (can be empty) and the project root is in `PYTHONPATH`.

## How to Control the Session

Use this rule:

If a feature is not listed in the Include scope, do not build it in Session 7. RAGAS, LangSmith, a second LLM judge, and CI/CD pipelines are explicitly excluded. If a student asks, acknowledge the topic, explain why it is out of scope for today, and note it as a production extension.

Do not spend more than 15 minutes debugging a single student's setup issue during the follow-along block. Pair them with another student or point them to the shared code.

## Setup Rule

Students must have `pytest`, `httpx`, and `pytest-asyncio` installed before the session. These should have been installed during the pre-session prerequisites. Do not spend live class time on package installation.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What did you add in Session 7 of the AI Support Ticket Resolution Copilot?

Expected answer:

In Session 7, I added three layers of quality control. First, I wrote a pytest test suite using FastAPI's TestClient to cover the ticket CRUD endpoints — testing create, read, update, and delete operations with proper status code assertions, and a test for the LLM classifier that validates the returned fields. Second, I implemented a custom `evaluate_groundedness()` function in `app/evals/groundedness.py` that takes an LLM response and a list of retrieved chunks, splits the response into sentences, checks whether each sentence is supported by the retrieved content, and returns a score between 0.0 and 1.0 along with a list of unsupported sentences. Third, I added a guardrail layer inside the `generate_node` in `app/graph/nodes.py` — a system prompt extension that instructs the LLM to avoid leaking personal data, inventing policy, or answering off-topic questions, and a post-generation check that returns a safe fallback message if the response violates those rules.

### Q2. What is the TestClient in FastAPI and why is it used for testing?

Expected answer:

`TestClient` is a synchronous HTTP client provided by FastAPI (built on top of `requests` and Starlette's test utilities) that allows you to send HTTP requests to the FastAPI application without starting a real server. It runs the ASGI app in-process, so tests are fast and isolated. The key advantage is that it participates in FastAPI's dependency injection system — you can override `get_session` or any other dependency using `app.dependency_overrides` to replace the production database with an in-memory test database. This means you can test the full request-response cycle including route logic, Pydantic validation, and database interactions without touching a real database or running a server.

### Q3. What is groundedness in the context of a RAG system?

Expected answer:

Groundedness refers to whether the LLM's generated response is actually supported by the retrieved context chunks. A grounded response contains claims that can be traced back to the retrieved documents. An ungrounded response contains claims the LLM invented from its training data, which is particularly dangerous in a support system where inventing policy or procedures can mislead users. The `evaluate_groundedness()` function I built measures this by splitting the response into sentences and checking each sentence for overlap with the retrieved chunks. A sentence is considered supported if significant token overlap exists between it and any chunk. The final score is the fraction of supported sentences out of total sentences in the response.

### Q4. What is a guardrail in an LLM system and how did you implement one?

Expected answer:

A guardrail is a constraint on LLM behavior that prevents specific categories of harmful, incorrect, or off-topic output. I implemented two types. The first is a system prompt guardrail — I appended instructions to the existing system prompt in the `generate_node` telling the LLM not to mention personal data from other users, not to make definitive guarantees about policies it is uncertain about, and to politely decline if the question is unrelated to the support domain. The second is a post-processing guardrail — after the LLM generates a response, I check the output for trigger patterns like personal email addresses, policy guarantee phrases, and known off-topic markers. If any trigger is detected, the function returns a `SAFE_FALLBACK_RESPONSE` constant instead of the generated response. This two-layer approach catches both LLM-level violations and edge cases the prompt instructions miss.

### Q5. Where does the confidence score come from in your system?

Expected answer:

The confidence score comes from ChromaDB's retrieval similarity score, not from the LLM. When the `retrieve_node` calls `collection.query()` with the ticket embedding, ChromaDB returns a distances or scores list alongside the documents. If the collection uses cosine similarity, the score for the top result is a float between -1.0 and 1.0 where values close to 1.0 indicate high similarity between the query and the retrieved chunk. I normalize this to a 0.0–1.0 range and store it as `confidence_score` in the `TicketState`. The `route_node` from Session 6 already uses this value to decide whether to go to `generate_node` or return a low-confidence fallback. In Session 7, I surface it in the API response so the caller can see how confident the retrieval was.

---

## Technical Deep-Dive Questions

### Q6. How does `app.dependency_overrides` work in FastAPI and what happens if you forget to reset it between tests?

Expected answer:

`app.dependency_overrides` is a dictionary on the FastAPI application instance that maps a dependency callable to a replacement callable. When FastAPI processes a request, instead of calling the original dependency (e.g., `get_session`), it calls the override instead. In tests, we use this to replace the real SQLite or PostgreSQL session with a test-only session backed by an in-memory engine. The standard pattern is to set the override in a pytest fixture with function scope, yield the client, then clear `app.dependency_overrides` in the fixture teardown. If you forget to clear it, the override persists across test modules in the same pytest session. This can cause tests in a later module to use the wrong database engine, leading to subtle failures where tests pass individually but fail when run together. The correct teardown is `app.dependency_overrides.clear()` or `del app.dependency_overrides[get_session]` after the yield.

### Q7. Walk through the exact code path that executes when `test_create_ticket` runs and asserts `status_code == 201`.

Expected answer:

When `client.post("/tickets", json={...})` is called, the `TestClient` passes the request to the FastAPI ASGI app. FastAPI matches the route to the `create_ticket` handler in `app/routes/tickets.py`. The route function receives the request body as a `TicketCreate` Pydantic model — if validation fails (missing field or wrong type), FastAPI returns a 422 before the handler runs. Assuming validation passes, the handler calls `get_session()`, but because `app.dependency_overrides[get_session]` is set, it receives the test database session instead. The handler creates a `Ticket` SQLModel instance, adds it to the session, commits, refreshes, and returns a `TicketRead` response with `status_code=201`. The `TestClient` deserializes the response body, and the test asserts `response.status_code == 201` and optionally checks `response.json()["id"]` is not None. If the `return` in the route handler uses `Response(status_code=201)` or `JSONResponse(status_code=201, content=...)`, the assertion passes.

### Q8. Explain the `evaluate_groundedness` function in detail. What are the limitations of the string overlap approach?

Expected answer:

The `evaluate_groundedness(response: str, retrieved_chunks: list[str]) -> dict` function works by first splitting the response into individual sentences using a period-based split or regex. For each sentence, it checks whether a meaningful portion of the sentence's tokens appear in any of the retrieved chunks by doing a substring search or word-level overlap calculation. A sentence is marked as supported if the overlap exceeds a threshold (e.g., 50% of non-stopword tokens appear in at least one chunk). The function returns a dictionary with `score` (float: supported / total) and `unsupported_sentences` (list of sentence strings). The limitations are significant: string overlap cannot detect paraphrase or semantic similarity, so a response sentence that conveys the same meaning as a chunk in different words will be marked unsupported. It also cannot handle multi-sentence reasoning chains where no single sentence maps to a chunk but the conclusion follows logically. In production, you would use embedding cosine similarity between each sentence and each chunk, or a dedicated NLI (natural language inference) model to check entailment. RAGAS provides a more rigorous faithfulness metric using an LLM judge, but that adds cost and latency per eval run.

### Q9. Why is the guardrail added as a system prompt extension rather than a separate LLM call, and what are the trade-offs?

Expected answer:

The guardrail is added to the existing system prompt rather than as a separate LLM call to avoid the cost and latency of a second API call per user request. A separate LLM judge call would at least double the response latency and cost. Adding it to the system prompt means the same single LLM call handles both the response generation and the constraint following. The trade-off is that the guardrail is only as reliable as the LLM's instruction-following ability — a less capable model or an adversarially crafted user input may bypass the system prompt instructions. The post-processing check in the generate node provides a second layer of defense that does not rely on the LLM's compliance, but it requires manually defined trigger patterns which can miss novel violations. In production, a dedicated content moderation API (like Google's Perspective API or a custom classifier) would be the correct approach for the post-processing layer, giving deterministic pattern matching for known violation categories at very low cost.

### Q10. How would you mock the Gemini client in `test_classifier.py` so the test does not make a real API call?

Expected answer:

You would use `unittest.mock.patch` to replace the Gemini client's `generate_content` method with a mock that returns a pre-defined response object. The standard approach in pytest is to use the `monkeypatch` fixture or a `@patch` decorator. For example: `with patch("app.llm.classifier.model.generate_content") as mock_generate:` followed by `mock_generate.return_value = MagicMock(text='{"category": "billing", "priority": "high", "summary": "test"}')`. The test then calls `classify_ticket(ticket_text)` and asserts the returned dictionary has the correct structure. This pattern tests the classifier's parsing and validation logic — the Pydantic model instantiation, the JSON parsing, the field value assertions — without calling the real API. The test is therefore fast, deterministic, and does not require a valid `GEMINI_API_KEY` in the test environment.

---

## System Design and Trade-off Questions

### Q11. Why do AI systems need evaluation (evals) in addition to unit tests? What does a unit test miss?

Expected answer:

Unit tests verify the API contract and code behavior — they check that the endpoint returns the correct status code, that the Pydantic model validates correctly, that the database write succeeds. What they cannot verify is the quality of the AI output. A unit test can confirm that `POST /tickets/{id}/resolve` returns `200` with a response field, but it cannot tell you whether the response is accurate, whether it is grounded in the retrieved documents, whether it is safe to show to a user, or whether the retrieval returned the right chunks. Evals are a separate class of quality measurement that operates on the semantic content of AI outputs, not the structural correctness of API responses. As AI systems evolve — model upgrades, prompt changes, new documents added to the knowledge base — evals catch regressions in output quality that unit tests are completely blind to. In production, you run evals on a labeled dataset of ticket-response pairs and track the groundedness score over time to detect quality drift.

### Q12. What are the trade-offs between a system prompt guardrail and a post-processing output filter?

Expected answer:

A system prompt guardrail is proactive — it instructs the LLM before generation and leverages the model's instruction-following capability to prevent bad output from being produced in the first place. It is effectively free in terms of latency and cost since no additional API call is needed. The trade-off is reliability: the LLM may not follow the instructions perfectly, particularly for edge cases or adversarial inputs, and there is no guarantee of compliance. A post-processing output filter is reactive — it checks the generated output against rules after the LLM has already produced text and replaces violations with a safe fallback. It is deterministic and more reliable for known violation patterns, but it requires manual enumeration of violation patterns which does not scale to all possible harmful outputs. The correct production architecture combines both: the system prompt reduces the frequency of violations, and the output filter provides a deterministic safety net for known categories. For high-stakes applications, a dedicated moderation model (e.g., a fine-tuned classifier) would replace the pattern-matching filter.

### Q13. How would you design a groundedness evaluation system at scale for a production support copilot?

Expected answer:

At scale, the string overlap approach I built would be replaced with a sentence-level embedding similarity check. For each sentence in the response, you would compute its embedding and compare it against the embeddings of all retrieved chunks using cosine similarity. A sentence is considered grounded if its maximum similarity score to any chunk exceeds a threshold, typically 0.75 or higher. This handles paraphrase and semantic equivalence that string overlap misses. For even higher accuracy, you would use a dedicated NLI model (e.g., a fine-tuned DeBERTa) to check whether each response sentence is entailed by the retrieved chunks — this is the approach RAGAS uses for its faithfulness metric. The evaluation would run as a batch job on a sample of production conversations, not on every request, because the additional inference cost is not acceptable at real-time. You would track groundedness score over time in a monitoring dashboard (LangSmith, W&B, or a custom metrics store) and trigger an alert when the score drops below a threshold, indicating either a model regression or a knowledge base gap.

### Q14. How does the LangGraph confidence routing from Session 6 relate to the confidence score surfaced in Session 7?

Expected answer:

In Session 6, the `route_node` checks the `confidence` field in `TicketState` and decides whether to invoke `generate_node` or return a low-confidence fallback response. The confidence value is computed in `retrieve_node` from the ChromaDB similarity score. In Session 7, I surface this same value in the API response as `confidence_score` so the API caller can see the retrieval confidence alongside the answer. This enables downstream applications to make their own decisions — for example, a frontend might show a disclaimer like "This answer is based on a low-confidence retrieval, please verify with a human agent" when `confidence_score < 0.5`. The key design point is that the score is computed once in the retrieve node and flows through the entire graph state; it is not recomputed or estimated by the LLM. This makes it a reliable, deterministic signal — the LLM cannot inflate or deflate it.

### Q15. If this system were deployed to production with 10,000 tickets per day, what would you add to the testing and evaluation infrastructure?

Expected answer:

At 10,000 tickets per day, the evaluation infrastructure would need to move from offline scripts to automated pipelines. I would add: a nightly batch eval job that runs `evaluate_groundedness` on a random sample of 200–500 production responses and writes scores to a metrics table; a Grafana or custom dashboard that plots groundedness score, guardrail trigger rate, and confidence score distributions over time; a regression test suite that runs on every code push and checks a labeled golden dataset of 50–100 known ticket-response pairs to catch prompt regression; alerting when the guardrail trigger rate spikes (which would indicate either a prompt injection attack or a change in user behavior); and A/B testing infrastructure to safely compare prompt variations before full rollout. The pytest suite would grow to include integration tests against a staging database and load tests to verify the LangGraph pipeline meets latency SLAs. LangSmith traces would be added to the generate node to capture full prompt-response pairs for offline analysis. The `evaluate_groundedness` function would be upgraded to use embedding similarity rather than string overlap to reduce false negatives from paraphrase.

---

# Session 7 Completion Checklist

Students should complete the following by the end of the session:

- [ ] `tests/conftest.py` exists with a pytest fixture that overrides `get_session` with an in-memory SQLite engine using `app.dependency_overrides`
- [ ] `tests/test_tickets.py` exists with at least 5 test cases covering `POST /tickets` (assert 201), `GET /tickets/{id}` (assert 200), `PUT /tickets/{id}` (assert 200), `DELETE /tickets/{id}` (assert 200 or 204), and `GET /tickets/99999` (assert 404)
- [ ] `tests/test_classifier.py` exists with a test that calls the classifier function (real or mocked) and asserts `category` is one of the valid enum values and `priority` is not None
- [ ] `pytest tests/ -v` runs without collection errors and all tests pass
- [ ] `app/evals/__init__.py` exists (can be empty)
- [ ] `app/evals/groundedness.py` exists with `evaluate_groundedness(response: str, retrieved_chunks: list[str]) -> dict` implemented and returning `{"score": float, "unsupported_sentences": list[str]}`
- [ ] `evaluate_groundedness` handles empty `retrieved_chunks` without raising an exception (returns score 0.0)
- [ ] `app/graph/nodes.py` `generate_node` includes a `SAFE_FALLBACK_RESPONSE` constant and appends guardrail instructions to the system prompt (does not replace the original system prompt)
- [ ] `generate_node` includes a post-generation check that returns `SAFE_FALLBACK_RESPONSE` when a guardrail trigger pattern is detected in the LLM output
- [ ] `confidence_score` is present in the resolve endpoint response (verify in Swagger at `/docs`)
- [ ] Swagger `/docs` shows a valid 200 response with `answer`, `confidence_score`, `category`, and `priority` fields when `POST /tickets/{id}/resolve` is called
- [ ] Student can explain in 2–3 sentences what groundedness means and why it is different from a unit test

---

# Instructor Backup Plan

If Antigravity generation fails or takes too long during the live session:

1. Instructor continues the live build on screen using the prompts manually, showing each file being created.
2. Students follow conceptually and note the file structure and function signatures.
3. Share the completed Session 7 code repository link after the session.
4. Students use the prompts from the pre-session file to regenerate and fix their own version after class.
5. Do not skip the concept pause (95–105 min) or the interview questions (105–115 min) — these are the highest-value segments for placement preparation.
6. If pytest is failing for all students due to a PYTHONPATH or import issue, resolve it in the first 2 minutes with `export PYTHONPATH=.` and move on.
