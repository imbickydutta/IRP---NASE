# Session 6 Instructor File: Add LangGraph Agentic Workflow

## Session Title

Add LangGraph Agentic Workflow

## Duration

2 hours

## Project

AI Support Ticket Resolution Copilot

## Session 6 Objective

By the end of Session 6, students should have a working LangGraph StateGraph that processes a support ticket end-to-end through four nodes — classify, retrieve, generate, and route — and exposes the complete workflow result through a FastAPI endpoint. Students should understand the conceptual and practical difference between an agent, a chain, and a pipeline, and be able to explain why LangGraph's explicit state model matters in production AI systems.

## Session 6 Deliverable

Students will add a LangGraph agentic workflow to the existing FastAPI backend that:

1. Defines a `TicketState` TypedDict with fields: `ticket_id`, `ticket_text`, `classification`, `retrieved_docs`, `suggested_response`, `confidence_score`, `needs_human_review`
2. Implements four nodes: `classify_node`, `retrieve_node`, `generate_node`, `confidence_router`
3. Uses a conditional edge on `confidence_score` to route to human review or suggest a response
4. Reuses the LLM classifier from Session 4 and the RAG retrieval function from Session 5
5. Exposes the full workflow result via `POST /tickets/{id}/resolve`
6. Returns a JSON response containing `suggested_response`, `confidence_score`, `needs_human_review`, and `classification`

---

## Strict Scope Control

### Include

- `TicketState` TypedDict with all seven specified fields
- `StateGraph` from `langgraph.graph`
- Four nodes: `classify_node`, `retrieve_node`, `generate_node`, `confidence_router`
- One conditional edge based on `confidence_score < 0.7`
- Reuse of Session 4 `classify_ticket()` function and Session 5 `retrieve_docs()` function
- FastAPI `POST /tickets/{id}/resolve` endpoint
- Return of full workflow state: `suggested_response`, `confidence_score`, `needs_human_review`, `classification`
- Basic error handling for missing ticket and workflow failure
- Code comments explaining each node's responsibility and state mutation

### Do Not Include

- Fully autonomous response sending to customers (human approval is always required)
- Complex multi-agent subgraphs or nested graphs
- External tool calls beyond classify/retrieve/generate (no web search, no email, no ticketing system writes)
- Streaming workflow output (do not use `astream` or `astream_events`)
- LangSmith tracing integration (mention as a concept only, do not wire up)
- More than five nodes
- Refresh tokens or any auth changes
- New database tables or schema migrations
- New embeddings or changes to the ChromaDB collection from Session 5
- Async LangGraph execution with `ainvoke` (use synchronous `invoke` for now)

---

# Instructor Framing

## Opening Message

We have been building one product across six sessions. In Session 1 we built CRUD for tickets. In Session 2 we added the database layer with SQLModel. In Session 3 we added JWT authentication and role-based access. In Session 4 we added an LLM classifier that labels each ticket. In Session 5 we added a RAG knowledge base with ChromaDB that retrieves relevant docs and generates a suggested response.

Today we connect all of those pieces into one orchestrated workflow using LangGraph. This is where the codebase stops being a collection of endpoints and starts behaving like an agent. Each node in the graph does one job. State flows through every node. A conditional edge decides at runtime whether the workflow can suggest a response or whether a human must review. This is the architecture used by production AI systems at companies shipping LLM-powered features at scale.

## Key Philosophy

Students are not expected to have memorized LangGraph's API. They are expected to:

- understand what a state machine is and why LangGraph implements one
- guide an AI coding tool with a precise, scoped prompt
- read and trace the generated graph node by node
- test the endpoint and verify the state fields in the response
- explain the agent vs chain distinction in interview language
- understand the human-in-the-loop design pattern and why it exists

## Repeated Instructor Line

AI can generate the graph. You must be able to trace the state through every node and explain the routing decision.

---

# Session Flow

## 0–10 min: Opening and Session 5 Recap

### Instructor Goal

Orient students in the codebase before introducing LangGraph. They should recall exactly what exists from Session 5.

### Recap the Current Code State

Open the project and point to these files:

- `app/routes/tickets.py` — CRUD endpoints + `POST /tickets/{id}/suggest` from Session 5
- `app/services/classifier.py` — `classify_ticket(ticket_text: str) -> dict` from Session 4
- `app/services/rag.py` — `retrieve_docs(query: str) -> list[str]` and `generate_response(ticket_text: str, docs: list[str]) -> str` from Session 5
- `app/models.py` — `Ticket` SQLModel, `User` SQLModel
- `app/auth.py` — JWT utilities from Session 3

### Ask Students

Walk through Session 5 quickly. What does `POST /tickets/{id}/suggest` do?

Expected flow from students:

- Fetch ticket from DB
- Call `retrieve_docs()` to get relevant knowledge base chunks
- Call `generate_response()` with the ticket text and retrieved docs
- Return a suggested response

### Set Up the Gap

Ask: what is missing from that flow? Elicit: there is no classification step integrated, no confidence score, no routing logic, no decision about whether to send the response or flag for human review. The endpoint is a static chain. It runs the same steps in the same order every time regardless of confidence.

### Transition

Today we replace that static chain with a dynamic graph.

---

## 10–20 min: Architecture Breakdown — What We Are Adding and Why

### Instructor Goal

Draw the LangGraph workflow on the whiteboard or share a diagram before any code is written.

### Diagram to Draw

```
Ticket ID (input)
      |
      v
[classify_node]  -->  state.classification set
      |
      v
[retrieve_node]  -->  state.retrieved_docs set
      |
      v
[generate_node]  -->  state.suggested_response + state.confidence_score set
      |
      v
[confidence_router]  (conditional edge)
      |                        |
confidence >= 0.7     confidence < 0.7
      |                        |
      v                        v
END (suggest response)    needs_human_review = True --> END
```

### Explain Each Component

**TicketState TypedDict** — This is not a Pydantic model. It is a plain Python TypedDict that LangGraph uses as the schema for shared state across all nodes. Every node receives the full state dict and returns a partial dict with only the fields it changed.

**classify_node** — Calls the existing `classify_ticket()` from Session 4. Reads `state["ticket_text"]`, returns `{"classification": result}`.

**retrieve_node** — Calls the existing `retrieve_docs()` from Session 5. Reads `state["ticket_text"]`, returns `{"retrieved_docs": docs}`.

**generate_node** — Calls `generate_response()` from Session 5 plus an LLM call to produce a `confidence_score`. Returns `{"suggested_response": response, "confidence_score": score}`.

**confidence_router** — This is the conditional edge function, not a node. It reads `state["confidence_score"]`. If below 0.7, it sets `needs_human_review = True` and routes to END. If above or equal to 0.7, it routes to END with `needs_human_review = False`.

### Key Distinction to Make

A LangGraph graph is not the same as a LangChain LCEL chain. In a chain, every step runs in order with no branching. In a graph, edges can be conditional. The routing decision is made at runtime based on state. That is what makes it an agent pattern rather than a pipeline.

---

## 20–35 min: Build the Feature Using Antigravity

### Instructor Goal

Use Prompt 1 from the student pre-session file to generate the LangGraph workflow. Run this live, share screen, and narrate what the AI is doing.

### What to Watch For in Generated Code

- Is `TicketState` defined as a `TypedDict` (not a Pydantic model)?
- Are all four node functions defined with signature `(state: TicketState) -> dict`?
- Is `StateGraph(TicketState)` used as the graph constructor?
- Are nodes added with `graph.add_node("classify", classify_node)`?
- Is the conditional edge added with `graph.add_conditional_edges()`?
- Is the graph compiled with `graph.compile()` before being called?
- Is `graph.invoke(initial_state)` called inside the FastAPI route handler?
- Does the endpoint return a response that includes all four fields?

### Instructor Control Rule

Do not let students start improving or extending the prompt during the initial build. Run Prompt 1 first, get a working endpoint, then run Prompt 2 for cleanup.

### Common AI Generation Mistakes to Catch

- AI may generate an async graph (`ainvoke`) — catch this and change to `invoke` for simplicity
- AI may define `TicketState` as a Pydantic `BaseModel` — LangGraph requires a `TypedDict`
- AI may add LangSmith tracing boilerplate — remove it, it is out of scope
- AI may add extra nodes beyond the four specified — prune these out

---

## 35–50 min: Instructor Code Walkthrough — Read the Generated Code Node by Node

### Instructor Goal

Every student must be able to trace state through the graph before they run it.

### Walkthrough Areas

**1. `app/services/agent.py` (or wherever the graph is defined)**

Open the file. Read `TicketState`. Ask: why TypedDict and not Pydantic? Because LangGraph merges partial dicts into state — Pydantic models do not support partial updates the same way. TypedDict is a plain dict with type hints, so LangGraph can merge `{"classification": "billing"}` into a state object that already has other keys set.

**2. `classify_node` function**

Read the function. Show that it receives the full state, calls `classify_ticket(state["ticket_text"])`, and returns only the changed fields. Ask: why does it not return the full state? Because LangGraph merges the returned dict into the existing state — you do not replace the whole state, you patch it.

**3. `retrieve_node` function**

Read the function. Point out it reuses `retrieve_docs()` from Session 5 directly. This is the payoff of having service functions separated from routes — they are reusable by both endpoint handlers and graph nodes.

**4. `generate_node` function**

Read the function. Show how it uses both `state["ticket_text"]` and `state["retrieved_docs"]`. Ask: what happens if `retrieved_docs` is an empty list? Discuss: the node should handle this gracefully, either falling back to no-context generation or setting `confidence_score = 0.0`.

**5. `confidence_router` function**

This is the conditional edge function. Show it does not return state — it returns a string that tells LangGraph which edge to follow. Show the string must match the keys in `graph.add_conditional_edges()`.

**6. `StateGraph` assembly**

Walk through node registration, edge registration, the `START` import, and `graph.compile()`. Explain that `compile()` validates the graph structure — missing edges or disconnected nodes will raise an error here.

**7. FastAPI route in `app/routes/tickets.py`**

Show how `graph.invoke()` is called with the initial state dict. Show the fields extracted from the final state and returned as JSON.

### Ask During Walkthrough

- Where does `ticket_text` enter the graph?
- What does `classify_node` return?
- What is the routing condition?
- What does the caller receive if `needs_human_review` is True?

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run Prompt 1 on their own codebase. They should generate the LangGraph workflow and verify:

- `app/services/agent.py` exists with `TicketState` and all four nodes
- `app/routes/tickets.py` has `POST /tickets/{id}/resolve` added
- `langgraph` is in `requirements.txt`

### Instructor Support Areas

Help students with:

- `ModuleNotFoundError: No module named 'langgraph'` — run `pip install langgraph`
- TypedDict import: `from typing import TypedDict` not from Pydantic
- `graph.compile()` errors — usually caused by disconnected nodes or missing edges to END
- DB session not passed into nodes — students may try to pass `db: Session` through LangGraph state, which is wrong; the DB lookup should happen in the route handler before calling `graph.invoke()`
- Ticket not found before graph is invoked — the route handler must do `db.get(Ticket, id)` and raise 404 before constructing the initial state

### If Student Setup Fails

Do not block the class. The student should follow the instructor screen and apply fixes after the session using the shared completed code.

---

## 65–80 min: Test and Improve — Run Tests, Test in Swagger, Handle Edge Cases

### Instructor Goal

Test the endpoint in Swagger and show the full JSON response for two cases: high confidence and low confidence.

### Test Case 1: High Confidence (Swagger)

1. Create a ticket with a clear technical issue (e.g., "I cannot reset my password, the link is broken")
2. Call `POST /tickets/{id}/resolve` with a valid JWT
3. Expected response:

```json
{
  "ticket_id": 1,
  "classification": "account",
  "suggested_response": "...",
  "confidence_score": 0.85,
  "needs_human_review": false
}
```

### Test Case 2: Low Confidence (Swagger)

1. Create a ticket with an ambiguous or unusual issue (e.g., "it doesn't work")
2. Call `POST /tickets/{id}/resolve`
3. Expected response:

```json
{
  "ticket_id": 1,
  "classification": "unknown",
  "suggested_response": null,
  "confidence_score": 0.45,
  "needs_human_review": true
}
```

### Run Prompt 2

Use the improvement prompt from the student pre-session file to clean up the generated code — add docstrings, tighten error handling, ensure `confidence_score` defaults to `0.0` if not set.

---

## 80–95 min: Error Handling and Edge Cases

### Instructor Goal

Ensure the workflow handles failure states gracefully. This is a production-readiness discussion.

### Edge Cases to Cover

**1. Ticket not found**

The route handler must look up the ticket before calling `graph.invoke()`. If `db.get(Ticket, id)` returns `None`, raise `HTTPException(status_code=404, detail="Ticket not found")` before the graph runs.

**2. LLM call failure in a node**

Wrap LLM calls in try/except inside the node. On failure, return `{"confidence_score": 0.0, "needs_human_review": True}` so the graph degrades gracefully rather than raising an unhandled 500.

**3. Empty retrieval result**

`retrieve_docs()` may return an empty list if the ChromaDB collection has no relevant docs. `generate_node` must check for this and handle it — either by generating without context or by setting `confidence_score = 0.0`.

**4. `confidence_score` missing from state**

If `generate_node` fails to set `confidence_score`, the `confidence_router` will raise a `KeyError`. Use `state.get("confidence_score", 0.0)` defensively.

**5. `graph.compile()` raising validation errors**

Show students what happens when a node is added but not connected to an edge — LangGraph will raise a `GraphValidationError` at compile time, not at runtime. This is by design and is a feature.

### Add Prompt 7

Run the edge case hardening prompt from the student pre-session file to add try/except blocks inside each node and ensure all state fields have safe defaults.

---

## 95–105 min: Concept Pause — LangGraph State Machines + Nodes + Conditional Edges + Agent vs Chain Distinction

### Instructor Goal

Convert the implementation into interview-ready conceptual understanding.

### Explain the Core Distinction

Ask the class: what is the difference between a chain and an agent?

A chain is a fixed sequence of steps. Input goes in, each step transforms it, output comes out. There is no branching, no decision-making, no state. LangChain's LCEL is a chain model — you compose functions with `|` and every call runs the same path.

An agent is a program that observes state, makes decisions, and selects its next action based on what the state contains. LangGraph models this explicitly: state is a TypedDict that flows through the graph, each node can read any part of the state, and conditional edges allow the graph to branch based on runtime values.

The difference in practice: a chain always runs the same four functions. An agent in Session 6 might skip human review for 80% of tickets (high confidence path) and route the other 20% to a human review queue. That routing decision is made by the `confidence_router` at runtime — the chain model cannot do this.

### Explain the State Model

Every LangGraph node must be a pure function with the signature `(state: TicketState) -> dict`. It reads from state and writes partial updates back. It does not mutate the state object directly. LangGraph merges the returned dict into the current state. This means nodes are stateless and composable — they can be tested in isolation without a running graph.

### Explain Human-in-the-Loop

The `needs_human_review` flag is not decorative. In a production system, when this flag is True, the ticket is placed in a human review queue and the suggested response is NOT sent to the customer. The human reviews the response, modifies it if needed, and approves it. This is the human-in-the-loop design pattern. It is the correct default for any AI system that generates customer-facing communications.

### Ask Students to Write

Every student writes a 2–3 line answer:

What does the confidence_router do and why is it a conditional edge instead of a node?

Expected answer: The `confidence_router` reads `confidence_score` from the state and returns a routing string that tells LangGraph which path to follow. It is a conditional edge function — not a node — because it does not produce new state; it only selects the next graph step based on existing state.

---

## 105–115 min: Interview Discussion and Technical Viva Practice

### Instructor Goal

Use the interview questions section below to conduct a rapid-fire viva. Pick 3–4 questions per student depending on time. Mix basic, deep-dive, and trade-off questions.

### Format

- Instructor asks question
- Student answers
- Instructor adds technical depth using the expected answers below
- Repeat

---

## 115–120 min: Wrap-Up and Session 7 Preview

### Instructor Closing

Today we connected Session 4 and Session 5 into a LangGraph workflow. The codebase now has a true agentic layer: state flows through nodes, a conditional edge makes a runtime decision, and the result includes enough information for a human reviewer to act on. The endpoint returns not just a response, but confidence and routing metadata.

In Session 7 we will add evals, guardrails, and testing. We will write pytest tests for the graph nodes, add input validation guardrails before tickets enter the workflow, and run systematic evals against known ticket/response pairs to measure response quality. The agent becomes trustworthy only when we can measure how well it performs.

---

# Instructor Notes

## What to Emphasize

Session 6 is the architectural inflection point of the project. Every previous session built one layer in isolation. Session 6 connects them. Emphasize the following:

- The session 4 and session 5 service functions are reused without modification — this is the direct payoff of keeping business logic in service modules, not inside route handlers
- `TicketState` as a TypedDict is a deliberate design choice, not an accident — LangGraph's partial dict merge only works with dict-like objects
- Nodes are pure functions — state in, partial dict out — this constraint makes them unit-testable in isolation
- `graph.compile()` validates graph structure at import time, not at request time — failing fast is a feature
- The human-in-the-loop pattern is the responsible default for AI-generated customer communications
- `confidence_score` is an approximation, not a guarantee — students should understand its limitations

## Common Student Mistakes

1. **Defining `TicketState` as a Pydantic `BaseModel`** — LangGraph's `StateGraph` requires a TypedDict. The error will be: `TypeError: Expected TypedDict but got BaseModel`. Fix: change `class TicketState(BaseModel)` to `class TicketState(TypedDict)` and import from `typing`.

2. **Calling `graph.invoke()` before `graph.compile()`** — Students may forget `compiled_graph = graph.compile()`. The error will be `AttributeError: 'StateGraph' object has no attribute 'invoke'`. Fix: always call `compile()` and store the result.

3. **Trying to pass `db: Session` through the graph state** — Students may add `db` as a field on `TicketState`. This will cause SQLAlchemy session lifecycle issues inside nodes. Fix: do the DB lookup in the route handler, pass only primitive data (strings, ints) into the graph's initial state.

4. **Missing `from langgraph.graph import START, END`** — The `START` and `END` constants are required to anchor the graph. Omitting them causes `GraphValidationError: Graph has no entry point`. Fix: add the import and `graph.add_edge(START, "classify")`.

5. **Confidence router returning wrong string values** — The router function must return strings that exactly match the keys passed to `graph.add_conditional_edges()`. A mismatch causes a `KeyError` at runtime. Students often return `True`/`False` instead of `"suggest"` / `"human_review"` or whatever string keys are used.

6. **Nodes returning the full state dict instead of partial updates** — If a node returns the complete `TicketState` dict, fields set by previous nodes may be overwritten with `None`. Fix: nodes return only the fields they modify — e.g., `classify_node` returns `{"classification": result}`, not the full state.

7. **`generate_node` crashing on empty `retrieved_docs`** — If `retrieve_docs()` returns `[]` and the node does not handle this, the Gemini API call may fail or produce a low-quality response. Fix: add a check `docs = state.get("retrieved_docs") or []` and handle the empty case.

8. **Forgetting to add the ticket lookup before `graph.invoke()`** — If the ticket ID does not exist, calling `graph.invoke({"ticket_id": id, "ticket_text": None})` will propagate `None` through all nodes and produce confusing errors. Fix: always do `ticket = db.get(Ticket, id)` and `if not ticket: raise HTTPException(404)` before constructing the initial state.

9. **`confidence_score` not a float** — If the LLM returns confidence as a string (e.g., `"0.85"`), the comparison `score < 0.7` will raise `TypeError: '<' not supported between instances of 'str' and 'float'`. Fix: explicitly cast to float: `float(state.get("confidence_score", 0.0))`.

10. **Not calling `pip install langgraph` before the session** — `ModuleNotFoundError: No module named 'langgraph'` will appear immediately. This is a pre-session requirement. Remind students to install before class.

## How to Control the Session

Use this rule: if a student wants to add a feature beyond the four specified nodes, the answer is: add it in Session 7 or after graduation. The graph for Session 6 has exactly four nodes. Every additional node added today is a debugging session that eats into interview prep time.

## Setup Rule

Do not spend more than five minutes on environment issues during live class. If `langgraph` installation fails, the student follows along conceptually and catches up after the session using the shared codebase.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What did you build in Session 6?

Expected answer:

In Session 6, I added a LangGraph agentic workflow to the AI Support Ticket Resolution Copilot. I defined a `TicketState` TypedDict with seven fields — `ticket_id`, `ticket_text`, `classification`, `retrieved_docs`, `suggested_response`, `confidence_score`, and `needs_human_review` — and built a four-node `StateGraph` that processes a support ticket end-to-end. The four nodes are `classify_node`, `retrieve_node`, `generate_node`, and a conditional edge function called `confidence_router`. The workflow is exposed as a `POST /tickets/{id}/resolve` FastAPI endpoint that returns the full workflow result including the routing decision.

### Q2. What is the `TicketState` TypedDict and why is it used?

Expected answer:

`TicketState` is a `TypedDict` that defines the shared state schema for the LangGraph workflow. Every node in the graph receives the full state and returns a partial dict with only the fields it modifies. LangGraph merges these partial updates into the running state. A TypedDict is used instead of a Pydantic model because LangGraph's state merging relies on dict-like objects — Pydantic models do not support the same partial update semantics. TypedDict also keeps the state schema simple and lightweight since it does not carry validation logic.

### Q3. What does the `confidence_router` do?

Expected answer:

`confidence_router` is a conditional edge function — not a node. It reads `state["confidence_score"]` and returns a routing string. If the confidence score is below 0.7, it sets `needs_human_review = True` in the state and routes to END. If the confidence score is 0.7 or above, it routes to END with `needs_human_review = False`. The routing string must match the keys in `graph.add_conditional_edges()` exactly. This function enables the graph to take different paths at runtime based on output quality, which is the core difference between a conditional graph and a static chain.

### Q4. What does `POST /tickets/{id}/resolve` return?

Expected answer:

The endpoint returns a JSON object containing four fields from the final workflow state: `classification` (the ticket category from Session 4's classifier), `suggested_response` (the RAG-generated response from Session 5's generate function), `confidence_score` (a float between 0 and 1), and `needs_human_review` (a boolean). When `needs_human_review` is True, the `suggested_response` field may be null or set but should not be automatically sent to the customer — it requires human approval first. The endpoint also returns the `ticket_id` for traceability.

### Q5. How does Session 6 reuse code from Sessions 4 and 5?

Expected answer:

The `classify_node` reuses `classify_ticket(ticket_text: str) -> dict` from `app/services/classifier.py`, which was built in Session 4. The `retrieve_node` reuses `retrieve_docs(query: str) -> list[str]` from `app/services/rag.py`, which was built in Session 5. The `generate_node` reuses `generate_response(ticket_text: str, docs: list[str]) -> str` also from Session 5. These functions were defined as standalone service functions — not embedded inside route handlers — which makes them directly importable by graph nodes without any refactoring. This is the architectural payoff of separating business logic from routing logic.

---

## Technical Deep-Dive Questions

### Q6. Why must LangGraph nodes be pure functions — state in, partial dict out?

Expected answer:

LangGraph's execution model depends on nodes returning only the state fields they modify. When a node runs, LangGraph merges the returned dict into the current state using a shallow merge. If a node returned the full state, it could accidentally overwrite fields set by previous nodes with `None` or stale values. By constraining nodes to return only what they changed, LangGraph ensures that each node is independent and composable — `classify_node` cannot accidentally clear `retrieved_docs` set by a previous run of `retrieve_node`. This constraint also makes nodes unit-testable in isolation: you call `classify_node({"ticket_text": "..."})` and assert on `{"classification": "..."}` without needing a full graph.

### Q7. What happens at `graph.compile()` and why is it important?

Expected answer:

`graph.compile()` validates the StateGraph's structure and returns a `CompiledGraph` object that has the `invoke()` and `stream()` methods. During compilation, LangGraph checks that every node added with `add_node()` has at least one incoming and one outgoing edge, that conditional edges reference valid node names, and that the graph has a defined entry point (connected from `START`) and at least one path to `END`. If any of these constraints are violated, `compile()` raises a `GraphValidationError` immediately. This fail-fast behavior at compile time (which happens at module import time if the graph is defined at module level) means graph structure errors are caught when the server starts, not when the first ticket is processed.

### Q8. What is the difference between a LangGraph conditional edge and a normal edge?

Expected answer:

A normal edge (`graph.add_edge("classify", "retrieve")`) unconditionally routes from one node to another after the first node completes. A conditional edge (`graph.add_conditional_edges("generate", confidence_router, {...})`) calls a routing function after the source node completes and uses the function's return value to determine which next node to route to. The routing function receives the current state and returns a string key. `add_conditional_edges()` maps these string keys to node names. This means the graph can take different paths through the node graph at runtime depending on the values in state — which is what gives LangGraph workflows their dynamic, agentic character.

### Q9. How would you write a unit test for `classify_node` in isolation?

Expected answer:

Since `classify_node` is a pure function with the signature `(state: TicketState) -> dict`, it can be tested without running the full graph. A pytest test would construct a minimal `TicketState` dict with `ticket_text` set, call `classify_node()` directly, and assert that the returned dict contains a `classification` key with a valid string value. The test would mock the `classify_ticket()` call using `unittest.mock.patch` to avoid real Gemini API calls. For example: `with patch("app.services.classifier.classify_ticket") as mock_classify: mock_classify.return_value = {"category": "billing"}; result = classify_node({"ticket_id": 1, "ticket_text": "..."})`. This test is fast, isolated, and does not require a running database or LLM.

### Q10. What is the human-in-the-loop design pattern and why is it the correct default for customer-facing AI?

Expected answer:

Human-in-the-loop is a design pattern where an AI system produces a candidate output but does not act on it autonomously — instead, it routes the output to a human for review and approval before any real-world action is taken. In the Session 6 workflow, when `confidence_score < 0.7`, the graph sets `needs_human_review = True` and returns the suggested response as a candidate, not as a sent message. A human support agent sees the ticket, the classification, the retrieved docs, and the suggested response in a review queue. They approve, edit, or reject the response before it reaches the customer. This pattern is the correct default because LLM-generated responses can be confidently wrong — a high confidence score does not guarantee factual accuracy or tone appropriateness. The threshold can be tuned as the system accumulates labeled data.

---

## System Design and Trade-off Questions

### Q11. What is the difference between a LangGraph agent, a LangChain LCEL chain, and a plain Python pipeline? When would you use each?

Expected answer:

A plain Python pipeline is a sequence of function calls with no framework: `result1 = step1(input); result2 = step2(result1)`. It is readable and simple but has no branching, no state schema, no retry logic, and no observability hooks. A LangChain LCEL chain (`step1 | step2 | step3`) adds composability and streaming support but still runs linearly — every invocation runs every step in the same order. A LangGraph StateGraph adds explicit state, conditional routing, and the ability to model loops and human-in-the-loop checkpoints. Use a pipeline when steps are fixed and trivial. Use LCEL when you need composable streaming transforms. Use LangGraph when you need conditional branching, state persistence between steps, or human approval checkpoints. The Session 6 use case requires conditional routing based on confidence, which mandates LangGraph.

### Q12. What are the trade-offs of putting `confidence_score` in the LangGraph state versus computing it outside the graph?

Expected answer:

Putting `confidence_score` in the state means the routing decision happens inside the graph, which keeps the workflow self-contained and auditable — the final state returned by `graph.invoke()` includes the confidence score that drove the routing decision. If confidence were computed outside the graph, the FastAPI route handler would need to apply routing logic itself, splitting the workflow logic between the graph and the handler and making it harder to test and reason about. The trade-off is that `confidence_score` in state must be serializable (a plain float), which constrains how it is computed and stored. For more complex routing criteria — for example, combining confidence with ticket priority — you would add additional fields to `TicketState` rather than compute them externally.

### Q13. How would you make the LangGraph workflow persistent across API calls — for example, to resume a human review after the agent pauses?

Expected answer:

LangGraph supports checkpointing through a `MemorySaver` or database-backed checkpointer. When a checkpointer is attached to the compiled graph with `graph.compile(checkpointer=MemorySaver())`, the graph saves its state at each node completion. Each graph run is identified by a `thread_id` passed in the `config` dict to `invoke()`. If the graph is interrupted — for example, by a human-in-the-loop pause — the state is persisted and the run can be resumed later by calling `invoke()` again with the same `thread_id`. In the Session 6 workflow, this would allow a human reviewer to approve or modify the suggested response in a subsequent API call, and the graph would continue from where it paused. This is not in scope for Session 6 but is the natural extension toward a production human-in-the-loop system.

### Q14. What happens to the `POST /tickets/{id}/resolve` endpoint if the Gemini API is down? How would you make it resilient?

Expected answer:

If the Gemini API is down, the LLM calls inside `classify_node` and `generate_node` will raise a `google.api_core.exceptions.ServiceUnavailable` or similar network/quota error. Without error handling, this propagates as an unhandled exception through the node, through `graph.invoke()`, and surfaces as a 500 Internal Server Error on the FastAPI endpoint. A resilient design wraps LLM calls inside each node with try/except. On failure, the node returns a degraded state: `classify_node` returns `{"classification": "unknown"}`, `generate_node` returns `{"confidence_score": 0.0, "needs_human_review": True}`. The graph then routes to human review automatically. The endpoint returns 200 with `needs_human_review: true` rather than 500, and the ticket enters the human review queue as a fallback. This pattern is called graceful degradation.

### Q15. If you needed to add a fifth node — for example, a `sentiment_node` that detects customer anger and escalates to a senior agent — where would you add it in the graph and what changes would be needed?

Expected answer:

A `sentiment_node` would read `state["ticket_text"]`, call a sentiment analysis function, and return `{"sentiment": "angry", "escalate": True}` or similar. It would be added after `classify_node` and before `retrieve_node` since classification and sentiment are both input analysis steps. You would add `sentiment` and `escalate` fields to `TicketState`. The `confidence_router` would need to be updated or supplemented with a second conditional edge after `generate_node` that checks both `confidence_score` and `escalate`. If `escalate` is True, the ticket routes to a different queue regardless of confidence. This requires adding `escalate_queue` as a new terminal node or routing string. The key principle is that state schema changes (new TypedDict fields) require updating all nodes and routing functions that need to read those fields, and the graph must be recompiled. LangGraph does not allow adding fields to state at runtime.

---

# Session 6 Completion Checklist

Students should complete the following by the end of the session:

- [ ] `langgraph` is installed and present in `requirements.txt`
- [ ] `TicketState` is defined as a `TypedDict` in `app/services/agent.py` with all seven fields
- [ ] `classify_node`, `retrieve_node`, `generate_node`, and `confidence_router` are all implemented
- [ ] `classify_node` calls `classify_ticket()` from `app/services/classifier.py`
- [ ] `retrieve_node` calls `retrieve_docs()` from `app/services/rag.py`
- [ ] `generate_node` calls `generate_response()` from `app/services/rag.py` and produces a `confidence_score`
- [ ] `StateGraph(TicketState)` is assembled with all nodes, edges, and `graph.compile()` called
- [ ] `POST /tickets/{id}/resolve` endpoint is added to `app/routes/tickets.py`
- [ ] Endpoint returns `ticket_id`, `classification`, `suggested_response`, `confidence_score`, `needs_human_review`
- [ ] Swagger returns 200 for `POST /tickets/{id}/resolve` with a valid ticket ID and valid JWT
- [ ] Swagger returns 404 for `POST /tickets/{id}/resolve` with a non-existent ticket ID
- [ ] Low-confidence ticket (ambiguous text) sets `needs_human_review: true` in response
- [ ] Student can trace the state through all four nodes without looking at the code

---

# Instructor Backup Plan

If code generation fails or students hit blocking environment errors:

1. Instructor continues the live build on screen, narrating each step.
2. Students follow the graph architecture conceptually — tracing state on the whiteboard.
3. The concept pause and interview Q&A sections are non-negotiable — do not cut them.
4. Share the completed Session 6 codebase after the session.
5. Students use Prompt 1 from the pre-session file to regenerate their version after class.
6. If only the `langgraph` installation fails, demonstrate `graph.invoke()` output using a pre-run result pasted into the console.
7. Do not sacrifice the interview explanation section under any circumstances — this is what students need for placement.
