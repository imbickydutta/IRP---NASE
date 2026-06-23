# Session 6 After-Session Notes: Add LangGraph Agentic Workflow

## What We Built Today

In Session 6, we added a LangGraph agentic workflow to the AI Support Ticket Resolution Copilot.

The additions were:

- `TicketState` TypedDict in `app/services/agent.py` with seven fields: `ticket_id`, `ticket_text`, `classification`, `retrieved_docs`, `suggested_response`, `confidence_score`, `needs_human_review`
- Four nodes in a `StateGraph`: `classify_node`, `retrieve_node`, `generate_node`, and the conditional edge function `confidence_router`
- `StateGraph(TicketState)` assembled with `add_node`, `add_edge`, `add_conditional_edges`, and compiled with `graph.compile()`
- `POST /tickets/{id}/resolve` endpoint in `app/routes/tickets.py` that fetches the ticket from DB, invokes the compiled graph, and returns the full workflow result
- Response payload: `ticket_id`, `classification`, `suggested_response`, `confidence_score`, `needs_human_review`

The session 4 `classify_ticket()` function and the Session 5 `retrieve_docs()` and `generate_response()` functions were reused without modification.

---

# Why This Feature Matters for Production Systems

In production, AI features that run in a fixed sequence without state visibility are fragile. If one step fails or produces low-quality output, the system has no mechanism to detect it or route around it. The static `POST /tickets/{id}/suggest` endpoint from Session 5 always ran the same three steps (fetch, retrieve, generate) and always returned a response — even if the response was low quality, off-topic, or generated without any relevant context documents.

LangGraph's StateGraph model changes this in three ways:

First, state is explicit and observable. After invoking the graph, the caller has access to every intermediate value — what the ticket was classified as, which docs were retrieved, what response was generated, and how confident the system was. This is essential for debugging, logging, and compliance in production systems handling customer data.

Second, routing is dynamic. The `confidence_router` makes a runtime decision based on the output of `generate_node`. Tickets with high confidence proceed toward a suggested response. Tickets with low confidence are flagged for human review. This means the system behaves differently for different inputs — it is not a static pipeline, it is a conditional state machine.

Third, the architecture scales. Because every node is a pure function that reads from and writes to a typed state dict, new nodes can be inserted, existing nodes can be replaced, and the graph topology can change without rewriting service logic. The `classify_ticket()`, `retrieve_docs()`, and `generate_response()` functions from Sessions 4 and 5 are completely unchanged — LangGraph uses them as-is.

---

# System Architecture Flow

Complete backend flow as of Session 6, showing what was added in each session:

```
Session 1: Ticket CRUD
  POST /tickets        → Create ticket in memory
  GET  /tickets        → List all tickets
  GET  /tickets/{id}   → Get one ticket
  PATCH /tickets/{id}  → Update ticket
  DELETE /tickets/{id} → Delete ticket

Session 2: Database Layer
  app/models.py       → Ticket, User as SQLModel tables
  app/database.py     → SQLite engine, get_db() session dependency
  All routes now read/write via SQLModel ORM instead of in-memory dict

Session 3: Auth + RBAC
  POST /auth/register  → Hash password, create User in DB
  POST /auth/login     → Verify password, return JWT
  app/auth.py          → create_access_token(), verify_token(), get_current_user()
  Protected routes now require: Authorization: Bearer <JWT>

Session 4: LLM Classifier
  POST /tickets/{id}/classify  → Call Gemini API, return category + confidence
  app/services/classifier.py   → classify_ticket(ticket_text: str) -> dict

Session 5: RAG Knowledge Base
  POST /docs/upload          → Embed doc chunks into ChromaDB
  POST /tickets/{id}/suggest → retrieve_docs() + generate_response() → suggested response
  app/services/rag.py        → retrieve_docs(), generate_response()

Session 6: LangGraph Agentic Workflow
  POST /tickets/{id}/resolve  → Full workflow via StateGraph
  app/services/agent.py       → TicketState TypedDict, 4 nodes, conditional edge

  Full flow:
  HTTP Request → FastAPI Route → JWT Verify → DB Ticket Fetch
      ↓
  LangGraph StateGraph
      ↓
  [classify_node] → classify_ticket() → state.classification
      ↓
  [retrieve_node] → retrieve_docs() → state.retrieved_docs
      ↓
  [generate_node] → generate_response() + confidence → state.suggested_response, state.confidence_score
      ↓
  [confidence_router] (conditional edge)
      ├── score >= 0.7 → needs_human_review = False → END
      └── score < 0.7  → needs_human_review = True  → END
      ↓
  JSON Response: {ticket_id, classification, suggested_response, confidence_score, needs_human_review}
```

---

# Technical Deep-Dive: LangGraph State Machines, Nodes, Conditional Edges, and Agent vs Chain

## What LangGraph Is and Why It Exists

LangGraph is a graph execution framework built on top of LangChain's primitives. It addresses a specific limitation of the chain model: chains are linear and stateless. When you compose functions with LangChain's LCEL pipe operator (`step1 | step2 | step3`), you get a composable callable that passes output from one step to the input of the next. This works well for simple transforms but breaks down when you need to branch on output values, accumulate state across multiple steps, or allow external checkpoints (like human review) between steps. LangGraph solves this by modelling the workflow as a directed graph with explicit shared state. The state is a TypedDict that all nodes can read from and write partial updates to. The graph is compiled once at module load time and invoked at request time.

## How State Flows Through Nodes

The fundamental contract of LangGraph nodes is: receive the full state dict, return a partial dict with only the fields you modified. LangGraph merges your partial return into the current state using a shallow dict update (`{**current_state, **node_return}`). This means `classify_node`, which only knows about `ticket_text` → `classification`, cannot accidentally overwrite `retrieved_docs` set later by `retrieve_node`. It also means nodes are fully isolated — `classify_node` does not know `generate_node` exists. Each node is a pure function in the functional programming sense: given the same state input, it produces the same output (modulo external API nondeterminism). This makes nodes unit-testable in complete isolation. You can call `classify_node({"ticket_text": "billing issue", ...})` in a pytest test with a mocked `classify_ticket()` and assert on `{"classification": "billing"}` without a running graph, database, or network.

## Conditional Edges and Why They Make This an Agent Pattern

A conditional edge is different from a normal edge in one critical way: the target node is not known at compile time. `graph.add_conditional_edges("generate", confidence_router, {"suggest": END, "human_review": END})` tells LangGraph: after `generate_node` runs, call `confidence_router(state)` and use the returned string to look up the next step in the mapping. The routing function runs at request time, with access to the live state. This is what makes LangGraph a tool for building agents rather than pipelines. An agent, in the academic sense, is a system that observes state and selects its next action based on that observation. The `confidence_router` observes `confidence_score` in state and selects between two action paths. A LangChain LCEL chain cannot do this — it has no mechanism for runtime branching. A plain Python `if/else` inside a route handler can do something similar, but it is not composable, not observable, and not extensible to loops or multi-step human approval flows.

---

# What Students Should Understand

1. `TicketState` is a TypedDict, not a Pydantic model. TypedDict provides dict-like merge semantics that LangGraph relies on for partial state updates. Pydantic models support validation and serialization but do not merge the same way.

2. Every LangGraph node must have the signature `(state: TicketState) -> dict`. The returned dict must contain only the fields the node modifies. Returning the full state risks overwriting fields set by previous nodes.

3. `graph.compile()` validates the graph structure at module load time. Disconnected nodes, missing edges, and undefined routing strings all raise `GraphValidationError` at compile time, not at the first request. This is a feature — it makes graph topology errors fail fast.

4. The DB lookup must happen in the FastAPI route handler before `graph.invoke()` is called. Passing a SQLAlchemy `Session` object through LangGraph state would cause session lifecycle errors — SQLAlchemy sessions are not meant to be serialized or held open across graph node boundaries.

5. `confidence_router` is an edge function, not a node. It does not modify state. It returns a routing string. The routing string must exactly match the keys in `add_conditional_edges()`.

6. The human-in-the-loop pattern means the system produces a candidate response and flags it for human review when confidence is low. The response is NOT sent to the customer automatically. A human agent reviews, approves, or modifies it before any customer communication happens.

7. `classify_ticket()` from Session 4 and `retrieve_docs()` / `generate_response()` from Session 5 are reused by graph nodes without any modification. This is the payoff of keeping business logic in service modules (`app/services/`) rather than embedding it in route handlers.

8. `confidence_score` is a float between 0 and 1 that approximates the LLM's certainty. It can be produced by asking the LLM to self-rate its confidence or by using a heuristic. LLM self-reported confidence is imperfectly calibrated — a model can produce a high confidence score for a factually incorrect response.

9. LangGraph's `invoke()` returns the final state dict after all nodes have run. The route handler reads fields from this dict to construct the JSON response. Fields that were not modified by any node retain their initial values (which should be `None` for optional fields).

10. Session 6 represents the architectural inflection point of the project: all prior sessions built isolated capabilities, and Session 6 connects them into a single observable, routable, testable workflow.

---

# Interview-Ready Explanation

```text
I added a LangGraph agentic workflow to the AI Support Ticket Resolution Copilot. I defined a TicketState TypedDict that flows through four nodes — classify, retrieve, generate, and a conditional router. Each node reads from the shared state, calls the relevant service function, and writes only its output fields back. The confidence_router function reads the confidence_score from state after generate_node runs and routes the ticket to either a suggested-response path or a human-review path based on a 0.7 threshold. This gives the system dynamic, state-driven routing at runtime, which is what distinguishes a LangGraph agent from a static LangChain chain or a plain Python pipeline. The entire workflow is exposed as POST /tickets/{id}/resolve and reuses the classifier and RAG functions from Sessions 4 and 5 without modification.
```

---

# What Happens When POST /tickets/{id}/resolve Is Called

```text
1. The FastAPI route handler receives the request with a valid JWT in the Authorization header.

2. get_current_user() dependency calls verify_token() from app/auth.py, decodes the JWT using python-jose, and returns the authenticated user. If the token is invalid or expired, HTTPException(401) is raised.

3. The handler calls db.get(Ticket, id) using the SQLModel session dependency. If no ticket with that ID exists, HTTPException(404, "Ticket not found") is raised before any graph code runs.

4. The handler constructs the initial state dict with ticket_id and ticket_text populated. ticket_text is assembled as f"{ticket.title}. {ticket.body}". All other state fields are set to None.

5. ticket_graph.invoke(initial_state) is called. LangGraph executes the graph synchronously:
   a. classify_node runs: calls classify_ticket(state["ticket_text"]) via Gemini API (gemini-1.5-flash), returns {"classification": "billing"}. State is now: {..., "classification": "billing"}.
   b. retrieve_node runs: calls retrieve_docs(state["ticket_text"]) via ChromaDB cosine similarity search, returns {"retrieved_docs": ["doc chunk 1", "doc chunk 2"]}. State is now: {..., "retrieved_docs": [...]}.
   c. generate_node runs: calls generate_response(ticket_text, retrieved_docs) via Gemini API (gemini-1.5-flash), prompts LLM for confidence rating, returns {"suggested_response": "...", "confidence_score": 0.85}. State is now: {..., "suggested_response": "...", "confidence_score": 0.85}.
   d. confidence_router runs: reads float(state.get("confidence_score", 0.0)) = 0.85. 0.85 >= 0.7, returns "suggest". LangGraph follows the "suggest" edge to END, setting needs_human_review = False.

6. graph.invoke() returns the final state dict. The handler extracts ticket_id, classification, suggested_response, confidence_score, needs_human_review.

7. The handler returns HTTP 200 with JSON: {"ticket_id": 1, "classification": "billing", "suggested_response": "...", "confidence_score": 0.85, "needs_human_review": false}.
```

---

# What AI Was Used For and What Engineers Must Still Do

## What AI Generated

- `TicketState` TypedDict field definitions
- Node function scaffolding with state read/write patterns
- `StateGraph` assembly boilerplate (add_node, add_edge, add_conditional_edges, compile)
- FastAPI route handler for `POST /tickets/{id}/resolve`
- try/except error handling blocks inside nodes
- pytest test scaffolding for nodes and the route

## What Engineers Must Still Do

- Verify that `TicketState` fields match the actual data produced by service functions (types and keys)
- Confirm that `classify_ticket()`, `retrieve_docs()`, and `generate_response()` function signatures are exactly as expected by node code — AI may generate calls with wrong argument names or order
- Decide on the confidence threshold (0.7 is a starting point — it must be tuned against real ticket data)
- Decide how `confidence_score` is actually produced — the method matters for calibration (LLM self-rating vs retrieval heuristic)
- Test the low-confidence path explicitly with ambiguous tickets — do not assume the routing works based on reading the code
- Understand the graph topology and be able to trace state through all four nodes without running the code
- Understand why the DB lookup happens in the route handler, not in a node, and be able to explain this design decision
- Verify that `needs_human_review = True` truly means the response is not sent automatically — if there is an auto-send path anywhere in the codebase, it must be removed or gated

---

# Common Issues and Fixes

## Issue 1: `AttributeError: 'StateGraph' object has no attribute 'invoke'`

This happens when the route handler imports and calls `graph.invoke()` directly on the `StateGraph` object instead of calling it on the compiled graph. `StateGraph` does not have `invoke()` — only the compiled graph returned by `graph.compile()` does.

What to ask AI:

```text
I am getting AttributeError: 'StateGraph' object has no attribute 'invoke' in app/routes/tickets.py when calling the POST /tickets/{id}/resolve endpoint.

The code in app/services/agent.py defines: graph = StateGraph(TicketState)
And the route handler imports: from app.services.agent import graph

Fix this by ensuring graph.compile() is called in agent.py and its result is stored as ticket_graph = graph.compile(). Update the import in tickets.py to import ticket_graph (the compiled graph) and call ticket_graph.invoke(initial_state) in the route handler. Explain what graph.compile() does.
```

## Issue 2: `langgraph.errors.GraphValidationError` on startup

This happens when the graph cannot be validated at compile time. Common sub-causes: a node was added with `add_node()` but has no outgoing edge, `graph.add_edge(START, "classify")` is missing so the graph has no entry point, or a conditional edge routing string does not match any registered node name.

What to ask AI:

```text
I am getting langgraph.errors.GraphValidationError when my FastAPI app starts. The error appears to be in app/services/agent.py where the StateGraph is compiled.

Please check the following in the StateGraph assembly:
1. Is graph.add_edge(START, "classify") present?
2. Do all nodes added with graph.add_node() have at least one outgoing edge?
3. Do the string keys in graph.add_conditional_edges() exactly match registered node names or the END constant?
4. Is graph.compile() called and its result stored?

Fix any issues and explain what each validation check does.
```

## Issue 3: `KeyError: 'confidence_score'` inside `confidence_router` at runtime

This happens when `generate_node` fails silently or returns without setting `confidence_score`, leaving it as `None` in state. The router then tries to compare `None < 0.7` or access a key that does not exist.

What to ask AI:

```text
I am getting KeyError: 'confidence_score' or TypeError: '<' not supported between instances of 'NoneType' and 'float' inside the confidence_router function in app/services/agent.py.

The root cause is that generate_node may fail without setting confidence_score, or it may set it as None.

Fix confidence_router to use: score = float(state.get("confidence_score") or 0.0) before the comparison.

Also ensure generate_node catches all exceptions and returns {"suggested_response": None, "confidence_score": 0.0} on failure rather than propagating the exception.

Explain how LangGraph propagates node exceptions and why safe defaults in nodes are important.
```

---

# Key Takeaways

1. **LangGraph enables conditional, state-driven workflows that chains cannot model.** The `confidence_router` making a runtime routing decision based on `confidence_score` is the core capability that distinguishes this from a static LCEL chain or a plain Python function sequence. Know the distinction and when each applies.

2. **Node purity is a constraint that enables testability and composability.** Every node taking `(state: TypedDict) -> dict` and returning only partial updates means nodes can be unit-tested in isolation with mocked dependencies. This is not just a LangGraph convention — it is the same principle as pure functions in functional programming applied to an AI workflow context.

3. **Human-in-the-loop is the responsible default, not an optional add-on.** The `needs_human_review` flag exists because LLM-generated responses can be confidently wrong. Production AI systems that generate customer-facing text must have a human approval step unless the quality of the output has been proven against labeled ground-truth data. The threshold that triggers review (0.7) should be treated as a hyperparameter, not a hardcoded value, and tuned as real ticket data accumulates.

4. **Service layer separation from Sessions 4 and 5 pays off directly in Session 6.** `classify_ticket()`, `retrieve_docs()`, and `generate_response()` are imported and called by LangGraph nodes without any modification. If these functions had been written inline inside route handlers, Session 6 would have required a refactor before the agent could be built. The architectural decision to isolate business logic in `app/services/` is validated by this session.

---

# Session 7 Preview

In Session 7, we will add evals, guardrails, and testing to the AI Support Ticket Resolution Copilot.

We will write pytest tests for the LangGraph graph nodes in `tests/test_agent.py` using mocked service functions. We will add input guardrails that validate ticket text before it enters the graph — rejecting empty tickets, overly short texts, or tickets that contain personally identifiable information patterns. We will run systematic evals against a set of known ticket/response pairs to measure response quality using an LLM-as-judge approach, and we will record pass/fail results per ticket category.

The main AI and technical concept for Session 7 is: how do you measure whether an LLM-powered system is working? What is an eval, what is a guardrail, and how are they different from unit tests? How do you write a pytest test for a node that calls a Gemini API without making real API calls? How do you use LLM-as-judge to evaluate response quality at scale?

By the end of Session 7, the AI Support Ticket Resolution Copilot will have test coverage for its agent workflow and a documented quality measurement process — which is what separates a prototype from a production-ready AI system.
