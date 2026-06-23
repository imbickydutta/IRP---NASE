# Session 6 Student Pre-Session File: Add LangGraph Agentic Workflow

## What We Are Building

Over 8 sessions, we are building one continuous backend product:

# AI Support Ticket Resolution Copilot

This is a production-style FastAPI backend that receives support tickets, classifies them, searches a knowledge base, generates suggested responses, and routes them for human review or auto-resolution.

By the end of all sessions, the backend will:

- accept and persist support tickets via REST API (Session 1)
- store tickets in a SQLite database using SQLModel ORM (Session 2)
- authenticate users and enforce role-based access with JWT (Session 3)
- classify tickets into categories using an OpenAI LLM (Session 4)
- retrieve relevant knowledge base docs via ChromaDB and generate RAG responses (Session 5)
- orchestrate the full workflow as a LangGraph StateGraph with conditional routing (Session 6)
- evaluate response quality and add guardrails with pytest evals (Session 7)
- deploy the backend as a containerised API (Session 8)

## Session 6 Goal

In Session 6, we replace the static `POST /tickets/{id}/suggest` endpoint from Session 5 with a full LangGraph agentic workflow that processes a ticket end-to-end through four nodes, makes a routing decision based on confidence, and returns the complete workflow result.

## Session 6 Output

By the end of Session 6, your backend should have:

- A `TicketState` TypedDict with seven fields tracking the full ticket processing state
- A `StateGraph` with four nodes: `classify_node`, `retrieve_node`, `generate_node`, and a conditional edge via `confidence_router`
- A `POST /tickets/{id}/resolve` FastAPI endpoint that invokes the graph and returns the result
- A response payload containing `classification`, `suggested_response`, `confidence_score`, and `needs_human_review`

---

# Pre-Read

## Why Are We Adding This Feature at This Point in the Build?

Sessions 4 and 5 built the core AI capabilities of the backend in isolation: Session 4 gave us an LLM classifier, Session 5 gave us a RAG retrieval and response generator. Both were exposed as independent endpoints. The problem is that a real ticket resolution system does not run these steps independently — they are part of one continuous process, and the system needs to make a decision based on the output of all steps combined.

LangGraph gives us the infrastructure to express this as an explicit state machine. The `TicketState` TypedDict is the contract between nodes. Each node reads from state, performs its function, and writes back only what it changed. A conditional edge decides at runtime whether the workflow has produced a response confident enough to present to a human reviewer, or whether the ticket needs escalation. This is the architectural step from "a backend with AI endpoints" to "an AI system with a backend."

## System Architecture Flow

This is the full backend flow as of Session 6:

```
HTTP Client (Swagger / Frontend)
      |
      | POST /tickets/{id}/resolve
      | Authorization: Bearer <JWT>
      v
FastAPI Route Handler (app/routes/tickets.py)
      |
      | Verify JWT (app/auth.py)
      | Fetch Ticket from DB (SQLModel Session, app/models.py)
      |
      v
LangGraph StateGraph (app/services/agent.py)
      |
      | Initial state: {ticket_id, ticket_text}
      v
[classify_node]
      | calls classify_ticket() from app/services/classifier.py
      | OpenAI Chat Completion (GPT-4 / GPT-3.5)
      | returns {"classification": "billing"}
      v
[retrieve_node]
      | calls retrieve_docs() from app/services/rag.py
      | ChromaDB similarity search (cosine distance)
      | returns {"retrieved_docs": ["doc1", "doc2", "doc3"]}
      v
[generate_node]
      | calls generate_response() from app/services/rag.py
      | OpenAI Chat Completion with retrieved docs as context
      | produces confidence_score via LLM or heuristic
      | returns {"suggested_response": "...", "confidence_score": 0.85}
      v
[confidence_router] (conditional edge function)
      |
      +-- confidence_score >= 0.7 --> needs_human_review = False --> END
      |
      +-- confidence_score < 0.7  --> needs_human_review = True  --> END
      v
FastAPI Route Handler
      |
      | Extract fields from final state
      v
JSON Response:
{
  "ticket_id": 1,
  "classification": "billing",
  "suggested_response": "...",
  "confidence_score": 0.85,
  "needs_human_review": false
}
```

## Key Concepts to Revise

Before Session 6, make sure you are comfortable with the following:

**1. Python TypedDict (`typing.TypedDict`)**

A TypedDict is a dict subclass with type annotations. It behaves like a regular Python dict but provides type hints for static checkers and documentation. LangGraph uses TypedDict for workflow state because it needs dict-like merge semantics — you can update individual keys without replacing the entire object. Know how to define one: `class TicketState(TypedDict): ticket_id: int; ticket_text: str`.

**2. LangGraph StateGraph**

`StateGraph` from `langgraph.graph` is the core graph object. You instantiate it with a state schema: `graph = StateGraph(TicketState)`. You register nodes with `graph.add_node("name", function)`. You register edges with `graph.add_edge("source", "target")`. You compile it with `compiled = graph.compile()`. You invoke it with `result = compiled.invoke(initial_state_dict)`.

**3. LangGraph Nodes as Pure Functions**

Every node must have the signature `(state: TicketState) -> dict`. It reads fields from `state`, performs some computation, and returns a partial dict containing only the fields it modifies. LangGraph merges this partial dict into the running state. A node that returns `{"classification": "billing"}` does not touch any other state field.

**4. Conditional Edges**

`graph.add_conditional_edges("source_node", routing_function, {"route_a": "node_a", "route_b": "node_b"})` adds an edge from a source node whose target is determined at runtime by `routing_function`. The routing function receives the current state and returns a string key. That string key is looked up in the mapping to find the next node name.

**5. `START` and `END` in LangGraph**

`from langgraph.graph import START, END` — `START` is a virtual entry node. `graph.add_edge(START, "classify")` tells LangGraph where the graph begins. `END` is a virtual terminal node. Any path that reaches `END` terminates the graph execution.

**6. Agent vs Chain vs Pipeline**

A pipeline is a fixed function sequence with no framework. A chain (like LangChain LCEL) is a composable sequence that runs linearly. An agent (like LangGraph StateGraph) models explicit state, supports conditional branching, and can loop or pause for human input. The difference matters in interviews — know which one to reach for and why.

**7. Human-in-the-Loop Pattern**

A design pattern where an AI system produces a candidate output but does not act on it autonomously until a human approves it. In Session 6, the `needs_human_review` flag signals that the suggested response requires human approval before being sent to a customer. This is the responsible default for AI systems generating customer-facing text.

**8. OpenAI Chat Completions and Confidence Estimation**

The `generate_node` needs to produce a `confidence_score`. This can be done by prompting the LLM to rate its own confidence as a float (e.g., "Rate your confidence in this response from 0.0 to 1.0"), or by using a heuristic like response length or retrieval match count. Understand the limitations: LLM self-reported confidence is calibrated imperfectly — a confident-sounding model may still be wrong.

---

# Prerequisites

## Python Packages to Install Before Class

Run this in your project virtual environment before the session:

```bash
pip install langgraph
pip install langgraph-checkpoint
```

Verify the installation:

```bash
python -c "from langgraph.graph import StateGraph, START, END; print('LangGraph OK')"
```

If this prints `LangGraph OK`, you are ready.

## Environment Setup

Your `.env` file should already have these from Sessions 4 and 5:

```
OPENAI_API_KEY=sk-...
DATABASE_URL=sqlite:///./support_tickets.db
SECRET_KEY=your-jwt-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

No new environment variables are required for Session 6.

## Code State from Last Session

Your project from Session 5 should have this structure:

```
app/
  __init__.py
  main.py
  models.py           # Ticket, User SQLModel definitions
  database.py         # engine, get_db session dependency
  auth.py             # create_access_token, verify_token, get_current_user
  routes/
    __init__.py
    tickets.py        # CRUD routes + POST /tickets/{id}/suggest
    auth.py           # POST /auth/register, POST /auth/login
  services/
    __init__.py
    classifier.py     # classify_ticket(ticket_text: str) -> dict
    rag.py            # retrieve_docs(query: str) -> list[str]
                      # generate_response(ticket_text: str, docs: list[str]) -> str
requirements.txt
.env
```

If your `app/services/` directory does not have `classifier.py` and `rag.py` as separate files with standalone functions, refactor them now before Session 6. The graph nodes will import these functions directly.

## Content to Prepare Before Class

Have a few test tickets ready to use in Swagger during the session. Create these in your DB using `POST /tickets` before class:

```text
Ticket 1 (high confidence expected):
Subject: Cannot reset password
Body: I have been trying to reset my password for the last two days. The reset email arrives but the link says it has expired immediately. I need access to my account urgently.

Ticket 2 (low confidence expected — ambiguous):
Subject: Problem
Body: It doesn't work. Please help.

Ticket 3 (billing category):
Subject: Charged twice this month
Body: I see two charges of $29.99 on my credit card statement from your company this month. I only have one subscription. Please refund the duplicate charge.
```

---

# Prompts for Session 6

Use these prompts during the session when instructed. All prompts are written for Claude Code or Cursor AI.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Support Ticket Resolution Copilot using FastAPI, SQLModel, LangGraph, and OpenAI.

Current project structure:
- app/main.py — FastAPI app, router includes
- app/models.py — Ticket (SQLModel, fields: id, title, body, status, created_at), User (SQLModel, fields: id, email, hashed_password, role)
- app/database.py — SQLite engine, get_db session dependency
- app/auth.py — create_access_token(), verify_token(), get_current_user() dependency using JWT (python-jose)
- app/routes/tickets.py — GET /tickets, POST /tickets, GET /tickets/{id}, PATCH /tickets/{id}, DELETE /tickets/{id}, POST /tickets/{id}/suggest
- app/routes/auth.py — POST /auth/register, POST /auth/login
- app/services/classifier.py — classify_ticket(ticket_text: str) -> dict (returns {"category": str, "confidence": float})
- app/services/rag.py — retrieve_docs(query: str) -> list[str], generate_response(ticket_text: str, docs: list[str]) -> str

Task: Add a LangGraph agentic workflow to process a support ticket end-to-end.

Create app/services/agent.py with the following:

1. Define TicketState as a TypedDict (from typing import TypedDict, Optional) with these fields:
   - ticket_id: int
   - ticket_text: str
   - classification: Optional[str]
   - retrieved_docs: Optional[list[str]]
   - suggested_response: Optional[str]
   - confidence_score: Optional[float]
   - needs_human_review: Optional[bool]

2. Implement classify_node(state: TicketState) -> dict:
   - Import and call classify_ticket() from app.services.classifier
   - Read state["ticket_text"]
   - Return {"classification": result["category"]}
   - Handle exceptions: on failure, return {"classification": "unknown"}

3. Implement retrieve_node(state: TicketState) -> dict:
   - Import and call retrieve_docs() from app.services.rag
   - Read state["ticket_text"]
   - Return {"retrieved_docs": docs}
   - Handle exceptions: on failure, return {"retrieved_docs": []}

4. Implement generate_node(state: TicketState) -> dict:
   - Import and call generate_response() from app.services.rag
   - Read state["ticket_text"] and state["retrieved_docs"] (default to [] if None)
   - Produce a confidence_score by prompting the LLM to rate confidence as a float between 0.0 and 1.0
   - Return {"suggested_response": response, "confidence_score": float(score)}
   - Handle exceptions: on failure, return {"suggested_response": None, "confidence_score": 0.0}

5. Implement confidence_router(state: TicketState) -> str:
   - Read state.get("confidence_score", 0.0) as a float
   - If score < 0.7, return "human_review"
   - Otherwise, return "suggest"

6. Assemble the StateGraph:
   - from langgraph.graph import StateGraph, START, END
   - graph = StateGraph(TicketState)
   - Add nodes: "classify", "retrieve", "generate"
   - Add edges: START -> "classify" -> "retrieve" -> "generate"
   - Add conditional edge from "generate" using confidence_router:
     - "human_review" -> END (also set needs_human_review = True in this path)
     - "suggest" -> END (also set needs_human_review = False in this path)
   - Note: since conditional edges cannot set state, handle needs_human_review inside generate_node or add a thin node for each terminal path
   - Compile: ticket_graph = graph.compile()

7. In app/routes/tickets.py, add:
   - POST /tickets/{id}/resolve endpoint
   - Requires: valid JWT via get_current_user dependency
   - Fetches ticket from DB using db.get(Ticket, id), raises HTTPException(404) if not found
   - Constructs initial state: {"ticket_id": id, "ticket_text": f"{ticket.title}. {ticket.body}", "classification": None, "retrieved_docs": None, "suggested_response": None, "confidence_score": None, "needs_human_review": None}
   - Calls ticket_graph.invoke(initial_state)
   - Returns JSON: {"ticket_id": id, "classification": ..., "suggested_response": ..., "confidence_score": ..., "needs_human_review": ...}

Constraints:
- Use TypedDict from typing, NOT Pydantic BaseModel for TicketState
- Do NOT use async graph execution (ainvoke) — use synchronous invoke()
- Do NOT add LangSmith tracing
- Do NOT add more than four nodes
- Do NOT stream graph output
- Do NOT add new database tables or schema changes
- Do NOT send responses automatically to customers — return result only
- Add code comments to every node explaining: what it reads from state, what it calls, what it returns

Update requirements.txt to include langgraph.
```

---

## Prompt 2: Improvement Prompt

```text
Review the LangGraph workflow in app/services/agent.py and the POST /tickets/{id}/resolve endpoint in app/routes/tickets.py.

Apply the following improvements:

1. Add docstrings to every node function explaining its inputs from TicketState, the external function it calls, and the fields it writes to state.

2. Ensure all state reads use .get() with safe defaults to prevent KeyError:
   - state.get("retrieved_docs") or []
   - float(state.get("confidence_score") or 0.0)
   - state.get("classification") or "unknown"

3. Add logging at the start and end of each node using Python's logging module (INFO level):
   - Log the ticket_id from state at the start of classify_node
   - Log classification result at the end of classify_node
   - Log retrieved_docs count at the end of retrieve_node
   - Log confidence_score at the end of generate_node

4. In the FastAPI route handler for POST /tickets/{id}/resolve:
   - Add a try/except around graph.invoke() that catches Exception
   - On failure, raise HTTPException(status_code=500, detail="Workflow execution failed: {str(e)}")
   - Ensure the 404 check for missing ticket happens BEFORE graph.invoke()

5. Return a consistent response schema — if needs_human_review is True, still return suggested_response (it may be null), do not omit the field.

Do not add new nodes, do not change the graph structure, do not add LangSmith tracing.
```

---

## Prompt 3: Debugging Prompt — KeyError in Node or Graph Validation Error

```text
I am getting an error in my LangGraph workflow for the AI Support Ticket Resolution Copilot.

The error is one of the following — diagnose and fix:

Case A: GraphValidationError at startup
Error: langgraph.errors.GraphValidationError: ...
Likely cause: a node is added but not connected by an edge, or START / END is not properly wired.
Please check the StateGraph assembly in app/services/agent.py, verify all nodes have incoming and outgoing edges, confirm graph.add_edge(START, "classify") is present, and confirm every path reaches END.

Case B: KeyError inside a node at runtime
Error: KeyError: 'retrieved_docs' inside generate_node
Likely cause: the node is reading state["retrieved_docs"] directly instead of using state.get("retrieved_docs") or [].
Please replace all direct state key access with .get() and safe defaults throughout all four node functions.

Case C: TypeError: '<' not supported between instances of 'str' and 'float'
Error: inside confidence_router when comparing confidence_score
Likely cause: the LLM returned confidence_score as a string "0.85" instead of float 0.85.
Please add explicit float() casting: float(state.get("confidence_score") or 0.0) in confidence_router.

Case D: AttributeError: 'StateGraph' object has no attribute 'invoke'
Error: when calling ticket_graph.invoke(initial_state) in the route handler
Likely cause: graph.compile() was never called, or the result of compile() was not stored.
Please check that ticket_graph = graph.compile() is present in agent.py and that the route handler imports ticket_graph (the compiled graph), not graph (the uncompiled StateGraph).

Fix whichever case applies and explain what was wrong.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the LangGraph workflow in app/services/agent.py in technical language suitable for backend engineering interview preparation.

Cover the following:

1. What is TicketState TypedDict? Why is TypedDict used instead of a Pydantic BaseModel here?

2. What does classify_node do? What does it read from state? What does it return? Why does it return only a partial dict?

3. What does retrieve_node do? What external function does it call? Where does that function come from?

4. What does generate_node do? How is confidence_score produced? What is the limitation of LLM self-reported confidence?

5. What is confidence_router? Is it a node or an edge function? What does it return and how does LangGraph use that return value?

6. Walk through StateGraph assembly: add_node, add_edge, add_conditional_edges, compile. What does compile() do?

7. What happens when ticket_graph.invoke(initial_state) is called? Trace the execution step by step, showing which state fields are populated after each node.

8. What is the POST /tickets/{id}/resolve endpoint doing before and after calling graph.invoke()?

Do not rewrite the code. Explain it clearly using the terminology I need for interviews.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Explain the LangGraph agentic workflow feature of the AI Support Ticket Resolution Copilot as if I am in a backend engineering interview.

Use this structure:

1. What is the feature? What problem does it solve?

2. What is LangGraph and why did you use it instead of a simple function sequence or LangChain LCEL?

3. Walk through the four nodes: what does each one do and what does it write to state?

4. What is the conditional edge? What is the routing logic?

5. What is the human-in-the-loop pattern? Why is needs_human_review the correct default for a system generating customer-facing responses?

6. How does this workflow reuse code from Sessions 4 and 5? What does that tell you about your architecture?

7. What are the trade-offs of this design? What would you change if this needed to handle 10,000 tickets per day?

8. What is the difference between an agent and a chain? Use your Session 6 build as the example.

Keep the explanation technically precise and interview-ready. Do not use vague language like "it uses AI to help."
```

---

## Prompt 6: Unit Test Generation Prompt

```text
Generate pytest unit tests for the LangGraph workflow in the AI Support Ticket Resolution Copilot.

Test file location: tests/test_agent.py

Write tests for the following:

1. test_classify_node_happy_path:
   - Mock classify_ticket() to return {"category": "billing", "confidence": 0.9}
   - Call classify_node({"ticket_id": 1, "ticket_text": "I was charged twice", ...}) with other fields set to None
   - Assert result == {"classification": "billing"}

2. test_classify_node_handles_exception:
   - Mock classify_ticket() to raise Exception("OpenAI timeout")
   - Call classify_node({"ticket_id": 1, "ticket_text": "..."})
   - Assert result == {"classification": "unknown"}

3. test_retrieve_node_returns_docs:
   - Mock retrieve_docs() to return ["doc1", "doc2"]
   - Call retrieve_node({"ticket_id": 1, "ticket_text": "password reset", ...})
   - Assert result == {"retrieved_docs": ["doc1", "doc2"]}

4. test_confidence_router_high_confidence:
   - Call confidence_router({"confidence_score": 0.85, ...})
   - Assert result == "suggest"

5. test_confidence_router_low_confidence:
   - Call confidence_router({"confidence_score": 0.45, ...})
   - Assert result == "human_review"

6. test_confidence_router_string_confidence:
   - Call confidence_router({"confidence_score": "0.30", ...})
   - Assert result == "human_review" (should cast to float without crashing)

7. test_full_graph_invoke_high_confidence:
   - Mock classify_ticket(), retrieve_docs(), generate_response(), and confidence score to produce score 0.9
   - Call ticket_graph.invoke(initial_state)
   - Assert final_state["needs_human_review"] == False
   - Assert final_state["classification"] is not None

8. test_post_tickets_resolve_returns_404_for_missing_ticket:
   - Use FastAPI TestClient
   - POST /tickets/9999/resolve with valid JWT
   - Assert response.status_code == 404

Use unittest.mock.patch for all external calls. Do not make real OpenAI or ChromaDB calls in tests.
```

---

## Prompt 7: Edge Case and Error State Prompt

```text
Add comprehensive error handling and edge case coverage to the LangGraph workflow in app/services/agent.py and the POST /tickets/{id}/resolve endpoint in app/routes/tickets.py.

Handle the following cases:

1. classify_node:
   - If classify_ticket() raises any exception, return {"classification": "unknown"} instead of propagating the error
   - If classify_ticket() returns a dict without a "category" key, default to "unknown"

2. retrieve_node:
   - If retrieve_docs() raises any exception, return {"retrieved_docs": []}
   - If retrieve_docs() returns None, return {"retrieved_docs": []}

3. generate_node:
   - If generate_response() raises any exception, return {"suggested_response": None, "confidence_score": 0.0}
   - If the LLM returns a confidence score outside [0.0, 1.0], clamp it: confidence_score = max(0.0, min(1.0, float(score)))
   - If retrieved_docs is empty, still call generate_response() but log a warning that no context docs were available

4. confidence_router:
   - If confidence_score is None, treat as 0.0 (route to human_review)
   - If confidence_score is a string, cast to float before comparison, catching ValueError and defaulting to 0.0

5. POST /tickets/{id}/resolve route handler:
   - Return 404 if ticket is not found before invoking the graph
   - Wrap graph.invoke() in try/except Exception and return 500 with detail if the graph raises an unhandled error
   - Validate that all required fields are present in the final state before constructing the response; if any are missing, set safe defaults (None for optional fields, False for needs_human_review)

After adding error handling, explain what the system's behavior is if the OpenAI API is completely unavailable. What does the endpoint return?
```

---

# What You Should Be Able to Explain After Session 6

By the end of the session, you should be able to answer these questions without looking at the code:

1. What is the difference between an agent, a chain, and a pipeline? Give a concrete example from this project.

2. Why does LangGraph use TypedDict for state instead of a Pydantic model? What is the merge semantics difference?

3. What is the function signature all LangGraph nodes must follow and why does the return type being a partial dict matter?

4. Trace the state through the graph for a billing ticket with high confidence. What does each node add to the state?

5. What does `confidence_router` return and how does LangGraph use that return value to select the next graph step?

6. What does `graph.compile()` do? What errors does it catch? When in the application lifecycle does it run?

7. Why is the ticket DB lookup done in the route handler and not inside a graph node? What problem would arise if you passed `db: Session` through the LangGraph state?

8. What is the human-in-the-loop pattern? When should `needs_human_review` be True in this system?

9. What happens to the endpoint response if the OpenAI API is unavailable during a `POST /tickets/{id}/resolve` call?

10. How does Session 6 prove the value of separating service functions from route handlers (the architecture decision made in Sessions 4 and 5)?

---

## Final Session 6 Explanation

```text
In Session 6, I added a LangGraph agentic workflow to the AI Support Ticket Resolution Copilot. I defined a TicketState TypedDict that flows through four nodes — classify, retrieve, generate, and a conditional router — where each node reads from state, calls the relevant service function, and writes only its output fields back to state. The conditional edge uses a confidence_score threshold of 0.7 to route tickets to either a suggested response or a human review queue. The workflow is exposed as POST /tickets/{id}/resolve and reuses the LLM classifier from Session 4 and the RAG functions from Session 5 without modification, demonstrating the value of keeping business logic in service modules.
```
