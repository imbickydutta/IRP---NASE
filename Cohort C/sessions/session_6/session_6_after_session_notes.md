# Session 6 After-Session Notes: Simple Agent Router

## What We Built Today

Today we built agent_router.py — a standalone Python script that implements a simple AI agent.

The agent does the following:

- Receives a user query as a string
- Calls Gemini 1.5 Flash to classify the query's intent into one of four categories
- Uses a Python dictionary to dispatch to the corresponding tool function
- Runs the tool function and prints the full trace: Intent, Tool, Result

The four tool functions are:

- rag_answer(query): Calls the RAG pipeline from Session 4 to answer a factual question
- summarize_text(text): Asks Gemini to produce a 2–3 sentence summary of the input
- safety_check(text): Asks Gemini to classify the content as SAFE or UNSAFE with a reason
- ask_clarification(query): Asks Gemini to generate a clarifying follow-up question

The main route(query) function orchestrates all of this: intent classifier → tool dispatch → tool execution → printed result.

---

# Why This Module Matters for AI Engineering Interviews

Interviewers at AI-focused companies ask about agents constantly. Terms like LangChain agents, LangGraph, AutoGen, tool use, and function calling appear in nearly every job description for AI engineering roles in 2024 and 2025. What they are actually testing is whether you understand the underlying concept: an agent is a system that uses an LLM to make decisions about which action to take, rather than always taking the same action.

agent_router.py strips that concept down to its minimum working implementation. There is no framework, no abstraction layer, no magic. You can point to every line of the script and explain exactly what it does. That ability — to explain a concept at the implementation level — is what separates strong candidates from candidates who have only used high-level libraries.

This module also demonstrates system composition. The rag_pipeline.py you built in Session 4 is now a callable tool inside a larger system. That is how real AI products are built: not as one monolithic script, but as composed, independently testable components.

---

# Portfolio Module Map

```
Session 1: Structured Output Prompt Engine
  structured_output_engine.py + output_examples.json
  Status: DONE
  Concepts: Gemini structured output, response_mime_type, JSON schema prompting
       |
       v
Session 2: LLM Logging and Evaluation Tracker
  llm_logger.py + llm_logs.csv + eval_summary.json
  Status: DONE
  Concepts: CSV logging, latency tracking, evaluation metrics
       |
       v
Session 3: Serverless-Style AI Function
  ai_handler.py + .env.example
  Status: DONE
  Concepts: Function-as-handler, .env pattern, local testing without a server
       |
       v
Session 4: Basic RAG Pipeline
  rag_pipeline.py + chroma_db/
  Status: DONE
  Concepts: ChromaDB, sentence-transformers, retrieval-augmented generation
       |
       v
Session 5: RAG Evaluation and Improvement
  rag_evaluator.py + rag_eval_report.csv
  Status: DONE
  Concepts: RAG metrics, faithfulness, relevance, before/after comparison
       |
       v
Session 6: Simple Agent Router  ← YOU ARE HERE
  agent_router.py
  Status: DONE
  Concepts: Intent classification, tool routing, ReAct pattern, safety fallback
  Connects to: Sessions 1 (structured output), 4 (RAG as a tool)
       |
       v
Session 7: Vision/OCR Mini Module
  vision_ocr_module.py
  Status: NEXT
  Concepts: Gemini vision API, image-to-text, structured OCR output
       |
       v
Session 8: Final System Design and Interview Demo
  (capstone or wrap-up module)
  Status: UPCOMING
```

---

# Technical Deep-Dive: Core Concepts Covered in Session 6

## Agent vs Chatbot, and the Role of the Intent Classifier

A chatbot sends every query to the same LLM and returns the response. The execution path is static. An agent inserts a decision layer before the LLM response: the agent first asks "what should I do with this query?" and then does it. In agent_router.py, this decision layer is the classify_intent() function. It calls Gemini 1.5 Flash with a prompt that lists four valid intent labels and asks the model to assign the query to one of them. The response is a JSON object: {"intent": "rag_answer"}. The agent then uses this classification to select and execute a tool. The key insight is that the LLM is not the whole agent — the LLM is one component (the classifier) that the agent uses to make a routing decision.

The quality of the entire routing system depends on the quality of the classify_intent() prompt. If the prompt lists vague intent descriptions, Gemini will misclassify ambiguous queries. If the prompt does not list the exact intent strings, Gemini will use its own naming and the dispatcher will fail to match. This is why prompt engineering for intent classification is a real, production-relevant skill: poorly written classifier prompts cause routing failures that are hard to debug because the script runs without throwing errors — it just routes every query to the wrong tool silently.

## Tools as Plain Python Functions and the Function Calling Concept

Each of the four tools in agent_router.py is an ordinary Python function. There is no Tool class, no schema registration, no framework wrapping. This is intentional. The concept of a "tool" in an agent system is nothing more than a callable that the agent can invoke. OpenAI's function calling API automates tool selection by having the LLM choose from a list of registered tool schemas — but the underlying tool implementations are still just Python functions. agent_router.py demonstrates the manual version of this: the intent classifier returns a string, the dispatcher maps that string to a function reference, and the function is called. Understanding this manual version makes it much easier to understand what LangChain or LangGraph are doing when they abstract this process, because you know what the abstraction is hiding.

## ReAct Pattern, Safety Fallback, and Production Scalability

The ReAct (Reason + Act) pattern is the formal description of the agent loop. In agent_router.py, the Reason step is classify_intent() — the agent uses the LLM to reason about what to do. The Act step is the tool function call. A single-step ReAct loop is what agent_router.py implements: one Reason, one Act, one result. A full ReAct agent (like a LangGraph graph) feeds the Act result back into the Reason step and loops until the task is complete. The safety fallback design in this module deserves specific attention: when classify_intent() fails (JSONDecodeError, missing key, unknown intent), the agent routes to ask_clarification() rather than returning an error or crashing. This is a production-relevant pattern — agents in production must degrade gracefully, and asking for clarification is almost always safer than guessing or failing loudly. The trade-off is that the fallback can mask real classification failures if debug logging is not in place.

---

# What Students Should Understand After Session 6

1. An agent is not a chatbot with more features. The fundamental difference is dynamic routing: the agent decides which code path to execute based on the input, rather than always following the same path.

2. Intent classification is the critical component that determines routing quality. A poorly written classify_intent() prompt will silently route queries to the wrong tools without throwing any errors.

3. response_mime_type="application/json" in the Gemini GenerationConfig is not optional for intent classification. Without it, Gemini wraps JSON in markdown code blocks, and json.loads() throws a JSONDecodeError.

4. Python functions are tools. There is no magic in "tool use." A tool is any callable Python function that the agent dispatcher can invoke. Frameworks like LangChain add metadata (names, descriptions) on top of this, but the function itself is unchanged.

5. The dictionary dispatch pattern (tool_map = {"intent_name": function_reference}) is cleaner and more extensible than a long if/elif chain. Adding a new tool requires only a new function definition and one new dictionary entry.

6. The fallback to ask_clarification() is a safety pattern, not just a convenience. In production, failing gracefully with a clarification request is always preferable to crashing or routing to a wrong tool with high confidence.

7. Session 4's rag_pipeline.py being callable from Session 6's agent demonstrates component composition — the same pattern used in every production AI system, where smaller modules are composed into larger systems.

8. The ReAct pattern (Reason + Act) is implemented in one iteration here. Understanding single-step ReAct is the prerequisite for understanding multi-step LangGraph graphs.

9. Gemini rate limits (429 ResourceExhausted errors) are a real operational concern on the free tier. Any script that calls Gemini in a loop needs either time.sleep() between calls or retry logic with exponential backoff.

10. Monitoring an agent requires logging intent decisions, not just errors. If every query routes to ask_clarification, the system is "working" (no errors) but producing useless output. Classification quality monitoring requires logging and periodic review.

---

# Interview-Ready Explanation

```text
In my portfolio I built agent_router.py, a simple AI agent in Python that demonstrates the core agent pattern: intent classification followed by tool routing. The agent uses Gemini 1.5 Flash to classify incoming queries into one of four intents — RAG-based answering, summarization, safety checking, or clarification — using structured JSON output via response_mime_type="application/json". Based on the classified intent, a Python dictionary dispatcher calls the corresponding tool function, which is just a plain Python function that either calls Gemini again or calls the RAG pipeline built in Session 4. This one-step ReAct loop — Reason by classifying intent, Act by running the tool — is the same fundamental pattern used in LangChain and LangGraph agents, just without the framework abstraction.
```

---

# What Happens When route("What is RAG?") Is Called

```text
Execution trace for route("What is RAG?"):

1. route("What is RAG?") is called.

2. route() calls classify_intent("What is RAG?").

3. classify_intent() builds a prompt:
   "Classify the following query into one of these intents:
    rag_answer, summarize_text, safety_check, ask_clarification.
    Return ONLY a JSON object with the key 'intent'.
    Query: What is RAG?"

4. classify_intent() calls Gemini 1.5 Flash with:
   generation_config = GenerationConfig(response_mime_type="application/json")

5. Gemini returns response.text = '{"intent": "rag_answer"}'

6. classify_intent() calls json.loads('{"intent": "rag_answer"}')
   → returns {"intent": "rag_answer"}
   → extracts and returns the string "rag_answer"

7. Back in route():
   intent = "rag_answer"
   tool_map["rag_answer"] → points to the rag_answer function
   tool_name = "rag_answer"

8. route() calls rag_answer("What is RAG?")

9. rag_answer() tries to import rag_pipeline.py and call its answer() function.
   If rag_pipeline.py is available: returns the retrieved-and-generated answer.
   If not available: returns "[RAG stub] Searching knowledge base for: What is RAG?"

10. route() receives the result string.

11. route() prints:
    Query: What is RAG?
    Intent: rag_answer
    Tool: rag_answer
    Result: [answer from RAG or stub]
    ============================================================

12. route() returns the result string.
```

---

# What AI Was Used For + What Engineers Must Still Do

## What AI Was Used For

- Generating the full agent_router.py script structure from the main build prompt
- Writing the classify_intent() prompt that instructs Gemini on the four valid intents
- Writing the summarize_text() and safety_check() Gemini prompts
- Writing the error handling blocks and fallback logic
- Suggesting the dictionary dispatch pattern over if/elif
- Generating test queries that exercise each tool path

## What Engineers Must Still Do

- Verify that classify_intent() actually routes each test query to the expected tool (run the script, read the output)
- Confirm that response_mime_type="application/json" is set correctly and that json.loads() works without errors
- Test the fallback by passing an empty string and a gibberish query
- Confirm that rag_answer() gracefully handles the case where rag_pipeline.py is not present
- Understand the route() function well enough to add a fifth tool without asking AI for help
- Be able to explain every function in an interview without reading the code

---

# Common Issues and Fixes

## Issue 1: JSONDecodeError when parsing Gemini's intent response

Error message:
```
json.decoder.JSONDecodeError: Extra data: line 3 column 1 (char 45)
```
or
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

This happens when Gemini wraps the JSON in a markdown code block like ```json { "intent": "rag_answer" } ```, or returns extra text before or after the JSON. The fix is to set response_mime_type="application/json" in the GenerationConfig — this forces Gemini to return only raw JSON with no markdown wrapping. As a defensive backup, strip any leading/trailing whitespace and ```json markers from response.text before calling json.loads().

```text
What to ask AI:
"My classify_intent() function is throwing a JSONDecodeError when parsing Gemini's response. The error is: json.decoder.JSONDecodeError: Extra data: line 3 column 1. Gemini appears to be wrapping the JSON in a markdown code block. Please fix classify_intent() to: (1) use response_mime_type="application/json" in the GenerationConfig, (2) strip whitespace and markdown markers from response.text before parsing, and (3) wrap json.loads() in try/except json.JSONDecodeError with a fallback to returning 'ask_clarification'."
```

## Issue 2: ModuleNotFoundError for rag_pipeline when calling rag_answer()

Error message:
```
ModuleNotFoundError: No module named 'rag_pipeline'
```

This happens when agent_router.py tries to import rag_pipeline inside rag_answer(), but rag_pipeline.py is not in the same directory or is not on the Python path. Fix: wrap the import in a try/except ImportError block inside rag_answer(). If the import fails, return a stub message that explains the RAG pipeline is unavailable. The agent continues routing other queries correctly — only the rag_answer tool degrades.

```text
What to ask AI:
"My rag_answer() function is throwing ModuleNotFoundError: No module named 'rag_pipeline'. Please update the rag_answer() function to wrap the import inside a try/except ImportError block. If the import fails, the function should return: 'RAG pipeline not available. Ensure rag_pipeline.py and chroma_db/ are in the same directory.' The rest of agent_router.py should continue working normally."
```

## Issue 3: All test queries routing to ask_clarification (silent misclassification)

There is no error message — the script runs, but every query shows:
```
Intent: ask_clarification
Tool: ask_clarification
```

This happens when the classify_intent() prompt does not list the exact intent strings, and Gemini returns a different label (e.g., "rag_based_answer" instead of "rag_answer"). The dispatcher's tool_map does not find a match and falls back to ask_clarification for every query. Fix: check the raw Gemini response by printing response.text in classify_intent() before parsing. The exact intent strings in the prompt must match the keys in tool_map exactly: rag_answer, summarize_text, safety_check, ask_clarification.

```text
What to ask AI:
"My agent_router.py is routing every query to ask_clarification even though the queries should go to different tools. I printed the raw Gemini response and it's returning 'rag_based_answer' instead of 'rag_answer'. Please update the classify_intent() prompt to explicitly state that the four valid intent values are exactly: rag_answer, summarize_text, safety_check, ask_clarification — no other values. The prompt should emphasize that these exact strings must be used with no variation."
```

---

# Limitations of This Module

agent_router.py is a portfolio-level implementation. It demonstrates the concept correctly but is not production-ready for the following reasons:

Single-step only — The agent runs the Reason + Act loop once and stops. It cannot handle tasks that require multiple tool calls. For example, if a query requires both a safety check and a RAG answer, the agent picks one and ignores the other. A production agent needs a loop and a completion condition.

No memory or context window — Each call to route() is independent. The agent does not remember previous queries or maintain conversation state. This means multi-turn conversations are not supported.

No tool parallelism — Tools are called sequentially. A production agent might call multiple tools in parallel for efficiency (e.g., safety check and RAG retrieval simultaneously).

Prompt brittleness — If the user's query language shifts significantly (e.g., queries in a different language, highly technical jargon, or very short queries), the intent classifier may misroute without any error signal.

Flat tool structure — All four tools are at the same level. There is no hierarchy (e.g., always run safety_check before rag_answer). In production, safety filtering is typically a pre-routing gate, not a parallel tool option.

No logging of classification decisions — There is no persistent log of which intent was assigned to each query. Without this log, classification quality cannot be monitored or improved over time.

---

# Key Takeaways

1. The agent pattern is: Reason (use LLM to decide what to do) + Act (call a Python function). Everything in LangChain, LangGraph, CrewAI, and AutoGen builds on this same loop with additional infrastructure for multi-step execution, memory, and parallelism.

2. response_mime_type="application/json" is the correct way to get reliable structured output from Gemini. Always use it when you need the LLM to return JSON. Never rely on parsing free-form text to extract JSON.

3. Tools being plain Python functions is the most important conceptual insight from this session. No framework is required to build a working agent. Adding LangChain or LangGraph adds structure, tooling, and scalability — but the underlying concept is identical to what agent_router.py does.

4. In production, the classify_intent() prompt is the system's most critical component. Poor prompt engineering at the classification layer produces silent failures — the script runs without errors, but routes everything to the wrong tool. Testing intent classification with diverse query sets before deploying an agent is non-negotiable.

---

# Session 7 Preview

In Session 7, we build the Vision and OCR Mini Module.

The deliverable is vision_ocr_module.py — a Python script that uses the Gemini vision API to process images, extract text (OCR), and return structured output describing what it sees.

Key concepts in Session 7:

- Gemini's multimodal capability: the same Gemini 1.5 Flash model can accept both text and image inputs
- How to pass an image to Gemini using the google-generativeai library (PIL Image or base64 encoding)
- Structured output from vision: asking Gemini to return extracted text, document type, and key fields as JSON
- Why vision + structured output is valuable in document processing pipelines

The connection to Session 6: in a future extension, vision_ocr_module.py becomes a fifth tool in agent_router.py. A query like "What does this image say?" would be classified as a vision_extract intent and routed to the vision tool. This is exactly how production agents with multimodal capability work.

Portfolio status after Session 7: 7 of 8 modules complete.
