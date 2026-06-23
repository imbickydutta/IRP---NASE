# Session 6 Student Pre-Session File: Simple Agent Router

## What We Are Building

This is an 8-session AI Engineering Portfolio. Each session produces one standalone Python script or notebook. These scripts are not throwaway exercises — they are portfolio artifacts you will show in interviews.

Here is what the portfolio looks like so far:

```
portfolio/
  structured_output_engine.py       ← Session 1: Structured output with Gemini
  output_examples.json              ← Session 1: Sample structured outputs
  llm_logger.py                     ← Session 2: LLM call logging
  llm_logs.csv                      ← Session 2: Log file
  eval_summary.json                 ← Session 2: Evaluation summary
  ai_handler.py                     ← Session 3: Serverless-style AI function
  .env.example                      ← Session 3: Environment variable template
  rag_pipeline.py                   ← Session 4: RAG pipeline (ChromaDB + Gemini)
  chroma_db/                        ← Session 4: Local persistent vector store
  rag_evaluator.py                  ← Session 5: RAG evaluation script
  rag_eval_report.csv               ← Session 5: Evaluation results
  agent_router.py                   ← Session 6: Building today
```

## Session 6 Goal

Build agent_router.py — a simple AI agent that classifies user queries using Gemini 1.5 Flash and routes them to one of four Python tool functions.

## Session 6 Deliverable

agent_router.py + test_queries output showing intent → tool → result for each of the 4–5 hardcoded test queries.

---

# Pre-Read

## Why Does This Module Exist in the Portfolio?

Sessions 1 through 5 each built a pipeline — one script with one job. Session 6 is different. For the first time, the script makes a decision before it does anything. That decision-making step is what separates an agent from a pipeline.

In AI engineering roles, "agentic systems" are everywhere. LangChain, LangGraph, CrewAI, AutoGen — these are all frameworks for building agents. If you understand what an agent is at the function level (an intent classifier + a tool dispatcher), you can reason about any of these frameworks in an interview. That is why this module exists in the portfolio.

Session 6 also connects to the earlier sessions. The rag_pipeline.py you built in Session 4 becomes a tool that this agent can call. That is a real demonstration of composition — small AI components combined into a larger system.

## Portfolio Module Map

```
Session 1: Structured Output Prompt Engine
  structured_output_engine.py
  Introduces: Gemini structured output, JSON schema prompting, response_mime_type
  Used by: Session 2 (logging format), Session 6 (intent classifier uses structured output)
       |
       v
Session 2: LLM Logging and Evaluation Tracker
  llm_logger.py
  Introduces: CSV logging, evaluation metrics, cost/latency tracking
  Used by: Session 5 (evaluation pattern), Session 6 (logging inside tools)
       |
       v
Session 3: Serverless-Style AI Function
  ai_handler.py
  Introduces: .env pattern, function-as-handler pattern, local testing
  Used by: Session 6 (tool functions are handlers; same .env pattern)
       |
       v
Session 4: Basic RAG Pipeline ──────────────────────────────────┐
  rag_pipeline.py + chroma_db/                                   |
  Introduces: ChromaDB, sentence-transformers, RAG loop           |
  Used by: Session 5 (evaluated here), Session 6 (called as tool) |
       |                                                          |
       v                                                          |
Session 5: RAG Evaluation and Improvement                        |
  rag_evaluator.py                                               |
  Introduces: RAG metrics, before/after comparison               |
  Used by: Session 6 (rag_answer tool uses the improved pipeline) |
       |                                                          |
       v                                                          |
Session 6: Simple Agent Router  <──────────────────────────────┘
  agent_router.py    (TODAY)
  Introduces: intent classification, tool routing, agent loop, ReAct concept
  Used by: Session 7 (vision tool can be added as a fifth agent tool)
       |
       v
Session 7: Vision/OCR Mini Module
  vision_ocr_module.py
  Introduces: Gemini 1.5 Flash vision API, image-to-text, structured OCR output
       |
       v
Session 8: Final System Design and Interview Demo
```

## Key Concepts to Revise Before Session 6

Revise these concepts before class. You do not need to code them — just understand them at a conceptual level.

1. Python functions as first-class objects — In Python, a function can be stored in a variable or a dictionary. This is how the agent dispatcher works: it maps intent names to function references and calls the right one. Example: tool_map = {"summarize": summarize_text}; tool_map["summarize"]("some text") calls the function.

2. JSON parsing with json.loads() — Gemini returns a string. When that string is JSON like {"intent": "rag_answer"}, you parse it with json.loads() to get a Python dict, then read intent_data["intent"]. Know what JSONDecodeError is and when it happens.

3. try/except in Python — The agent must not crash when Gemini returns unexpected output. Know how to write try/except Exception as e and what to do in the except block (log the error, return a fallback).

4. Environment variables and os.environ.get() — GEMINI_API_KEY is loaded with os.environ.get("GEMINI_API_KEY"). Know how to set an environment variable in your terminal: export GEMINI_API_KEY="your_key_here".

5. google-generativeai library basics — Know how to call genai.configure(api_key=...), create a model with genai.GenerativeModel("gemini-1.5-flash"), and call model.generate_content(prompt, generation_config=...).

6. response_mime_type="application/json" in GenerationConfig — This tells Gemini to return valid JSON only, with no markdown wrapping. This is essential for any structured output from Gemini.

7. The concept of a tool in AI agents — A tool is any callable function that an agent can invoke. It does not need to be wrapped in a framework. A plain def function() is already a tool.

8. The concept of intent classification — Given a piece of text, the classifier assigns it to one of a fixed set of categories (intents). This is a text classification problem, but instead of using a fine-tuned classifier model, we use a prompted LLM with explicit category names in the prompt.

## Technical Explanation of the Core Concept

A chatbot sends every query to the same LLM and returns the LLM's text response. The flow is always:

```
Query → LLM → Response
```

An agent adds a decision layer before the LLM (or as part of the first LLM call):

```
Query → Intent Classifier (LLM call 1) → Tool Selection → Tool Execution → Response
```

In agent_router.py, the intent classifier is Gemini 1.5 Flash. It is given the query and a list of four valid intent names and asked to return a JSON object with a single intent field. That intent field determines which Python function runs next.

The Python functions that run are called tools. They are just ordinary Python functions. In production, LangChain would wrap these functions in Tool objects with names and descriptions that are fed to the LLM. But the underlying concept is identical: the LLM decides which function to call, the agent runtime calls it, and the result is returned.

The ReAct pattern (Reason + Act) is the formal name for this loop. In a single-step ReAct agent like today's module: Reason (classify_intent) → Act (run tool) → return result. In a multi-step ReAct agent, the result is fed back to the LLM to decide if another action is needed.

---

# Setup Before Class

## Required pip Installs

Run these before the session. All packages should already be installed from Sessions 1–5, but verify them.

```
pip install google-generativeai
pip install sentence-transformers
pip install chromadb
pip install python-dotenv
```

Verify installations:

```
python -c "import google.generativeai; print('Gemini OK')"
python -c "from sentence_transformers import SentenceTransformer; print('ST OK')"
python -c "import chromadb; print('ChromaDB OK')"
```

## Gemini API Key Setup

Get your free API key from https://aistudio.google.com.

Set it as an environment variable. In terminal:

```
export GEMINI_API_KEY="your_api_key_here"
```

For persistence across terminal sessions, add this line to your ~/.zshrc or ~/.bashrc file.

Alternatively, create a .env file in your portfolio folder:

```
GEMINI_API_KEY=your_api_key_here
```

Then load it in Python with:

```python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
```

## Verify Setup: One-Line Test

Paste this into a Python file called test_gemini.py and run it:

```python
import google.generativeai as genai
import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say: setup verified")
print(response.text)
```

If you see "setup verified" or similar text, your Gemini setup is working.

## Confirm rag_pipeline.py is Available

agent_router.py will call rag_pipeline.py as the rag_answer tool. Confirm the file exists:

```
ls /path/to/your/portfolio/rag_pipeline.py
```

If it does not exist, the rag_answer() tool will use a stub response. That is acceptable for the session — the routing logic still works.

---

# Sample Data / Content to Prepare

Prepare these 5 test queries in a text file before class. You will use them to test agent_router.py once it is built.

```text
Test Query 1 (should route to rag_answer):
"What is retrieval-augmented generation and how does it work?"

Test Query 2 (should route to summarize_text):
"Summarize this: Large language models are trained on vast amounts of text data and can generate coherent, contextually relevant responses across a wide range of topics. They use transformer architectures with attention mechanisms to understand and generate language."

Test Query 3 (should route to safety_check):
"Check if this is appropriate: I want to hack into the school server and change my grades."

Test Query 4 (should route to ask_clarification):
"Tell me something interesting."

Test Query 5 (edge case — should route to safety_check or ask_clarification):
"Kill all background processes."
```

---

# Prompts for Session 6

All prompts below are ready to copy and paste into Claude Code or Cursor. Use them in order during the session.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Engineering Portfolio. I need you to create a Python script called agent_router.py in my portfolio folder.

Portfolio context (scripts already built):
- structured_output_engine.py: Gemini structured output engine (Session 1)
- llm_logger.py: LLM call logger to CSV (Session 2)
- ai_handler.py: Serverless-style AI function (Session 3)
- rag_pipeline.py: RAG pipeline using ChromaDB and sentence-transformers (Session 4)
- rag_evaluator.py: RAG evaluation script (Session 5)

Today's script: agent_router.py
This script builds a simple AI agent that classifies user query intent using Gemini 1.5 Flash and routes the query to one of four Python tool functions.

EXACT REQUIREMENTS:

1. LLM: Use google-generativeai library. Model name must be "gemini-1.5-flash". Load API key from environment variable GEMINI_API_KEY using os.environ.get(). Call genai.configure() at module level.

2. Function: classify_intent(query: str) -> str
   - Sends the query to Gemini 1.5 Flash with a structured prompt
   - The prompt must explicitly list the four valid intents: rag_answer, summarize_text, safety_check, ask_clarification
   - The prompt must instruct Gemini to return ONLY a JSON object with a single key: "intent"
   - Use generation_config=genai.types.GenerationConfig(response_mime_type="application/json") to force JSON output
   - Parse the response with json.loads(response.text)
   - Extract and return the "intent" field as a string
   - Wrap json.loads() in a try/except json.JSONDecodeError and return "ask_clarification" as fallback

3. Four tool functions (plain Python functions, no external APIs):

   def rag_answer(query: str) -> str:
   - Try to import and call the answer() function from rag_pipeline.py
   - If import fails, return a stub: f"[RAG stub] Searching knowledge base for: {query}"
   - Wrap in try/except and return a graceful error message if RAG fails

   def summarize_text(text: str) -> str:
   - Call Gemini 1.5 Flash with a summarization prompt
   - Return the summarized text
   - Keep the summary to 2-3 sentences

   def safety_check(text: str) -> str:
   - Call Gemini 1.5 Flash with a safety classification prompt
   - The prompt must ask Gemini to return a JSON object with fields: "verdict" (SAFE or UNSAFE) and "reason" (one sentence)
   - Use response_mime_type="application/json"
   - Return a formatted string: f"Verdict: {verdict} | Reason: {reason}"

   def ask_clarification(query: str) -> str:
   - Call Gemini 1.5 Flash to generate a clarifying question based on the query
   - Return the clarifying question as a string

4. Function: route(query: str) -> str
   - Call classify_intent(query) to get the intent
   - Use a dictionary dispatch to call the correct tool function:
     tool_map = {
       "rag_answer": rag_answer,
       "summarize_text": summarize_text,
       "safety_check": safety_check,
       "ask_clarification": ask_clarification,
     }
   - Default to ask_clarification if intent is not in tool_map
   - Print this trace before returning:
     print(f"Intent: {intent}")
     print(f"Tool: {tool_name}")
     print(f"Result: {result}")
   - Return the result string

5. At the bottom of the script, in an if __name__ == "__main__": block, define a list of 5 test queries and call route() on each one. Print a separator line ("---") between each query.

6. Add a comment block at the very top of the file explaining what each component does (classify_intent, tool functions, route).

DO NOT include:
- LangGraph, LangChain, CrewAI, or any agent framework imports
- External API calls (no weather, search, or news APIs)
- Memory or conversation history
- Streaming output
- FastAPI or any web framework
- User input() — use only the hardcoded test queries in the main block

Add code comments throughout explaining why each design decision was made (e.g., why response_mime_type is set, why the fallback returns ask_clarification, why tools are plain functions).
```

---

## Prompt 2: Improvement Prompt

```text
Improve agent_router.py with better error handling, cleaner output, and edge case coverage.

Apply these improvements:

1. In classify_intent():
   - Add a second fallback: if the parsed JSON does not contain the "intent" key, return "ask_clarification" instead of raising a KeyError
   - Print a debug line when the fallback is triggered: print("[DEBUG] classify_intent fallback triggered")

2. In route():
   - Wrap the tool function call in a try/except Exception to catch tool-level failures
   - If a tool raises an exception, print the error and return: "Tool execution failed. Please try a different query."

3. Improve the print output format:
   - Add a blank line before each test query block
   - Print the query on its own line: print(f"Query: {query}")
   - Then print Intent, Tool, Result on separate lines with consistent labels
   - Print a separator "=" * 60 between each query block

4. Add a rate limit handler:
   - In classify_intent() and in each Gemini-calling tool function, catch google.api_core.exceptions.ResourceExhausted
   - When caught, print "Rate limit reached. Waiting 5 seconds..." and use time.sleep(5) before returning the fallback

5. Add a check at the start of the script:
   - If GEMINI_API_KEY is not set (os.environ.get returns None), print a clear error message and exit with sys.exit(1)

6. Keep all existing functionality intact — do not remove any of the original four tools or the route() function.
```

---

## Prompt 3: Debugging Prompt — JSONDecodeError and Gemini Structured Output

```text
My agent_router.py is throwing a JSONDecodeError when classify_intent() tries to parse Gemini's response.

Here is the error I see:
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

Or sometimes:
json.decoder.JSONDecodeError: Extra data: line 3 column 1 (char 45)

The issue is that Gemini is not returning clean JSON — it is wrapping the JSON in markdown like:
```json
{"intent": "rag_answer"}
```

Please fix classify_intent() to handle this correctly.

Requirements:
1. Use generation_config=genai.types.GenerationConfig(response_mime_type="application/json") — this should prevent markdown wrapping from Gemini, but add a defensive strip as well
2. After getting response.text, strip any leading/trailing whitespace with .strip()
3. If the text starts with ```json or ```, strip those markers before calling json.loads()
4. Wrap json.loads() in try/except json.JSONDecodeError
5. In the except block, print the raw response.text for debugging: print(f"[DEBUG] Raw Gemini response: {response.text}")
6. Return "ask_clarification" as the fallback intent
7. Also check: if the parsed dict does not have the "intent" key, return "ask_clarification" — do not let a KeyError crash the script

Show me the corrected classify_intent() function only. Explain what was wrong and why each fix works.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the generated agent_router.py technically, as if I need to present it in a job interview.

Cover each component:

1. What does classify_intent() do? Why is it a separate function from route()? What is response_mime_type="application/json" doing and why is it important?

2. What are the four tool functions? Why are they plain Python functions instead of LangChain Tool objects? What would need to change to make them work in a LangChain pipeline?

3. What does route() do? Walk through the exact execution order. What is the dictionary dispatch pattern and why is it better than a long if/elif chain?

4. What is the ReAct pattern? Does agent_router.py implement it? Where is the Reason step? Where is the Act step? What would a full ReAct loop look like?

5. What is the safety fallback? Why does ask_clarification serve as the default fallback instead of returning an error?

6. What are the limitations of this agent? What would need to change before it could be used in production?

Explain at a level appropriate for a senior AI engineer interviewing me. Be specific about the Python patterns and Gemini API parameters used.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Help me prepare a clear, technical explanation of agent_router.py for a job interview.

Structure the explanation using this format:

1. What it does (2 sentences — high level)
2. Why it matters for AI engineering (connect to production agent systems — LangChain, LangGraph, AutoGen)
3. How it works technically (walk through: intent classifier → dispatcher → tool function → result)
4. Key design decisions with trade-offs:
   - Why Gemini for intent classification instead of keyword matching
   - Why tools are plain Python functions
   - Why ask_clarification is the fallback instead of an error
   - Why response_mime_type="application/json" is used instead of parsing free-form text
5. What I would change in production (3 specific improvements)
6. How this connects to the rest of my portfolio (Sessions 1–5 build into this)

Keep the answer to under 3 minutes of speaking time. Use technical vocabulary appropriate for a software engineer with 1-2 years of AI/ML experience.
```

---

## Prompt 6: Test Case Generation Prompt

```text
Generate 5 additional test queries for agent_router.py that test edge cases and route to different tools.

Requirements:
- At least one query that is ambiguous (should route to ask_clarification)
- At least one query that has clearly unsafe content (should route to safety_check)
- At least one query that is a clear summarization request with a passage included
- At least one query that should route to rag_answer based on a factual AI/ML question
- At least one query that tests the boundary between rag_answer and ask_clarification (e.g., a very vague question about AI)

For each query, predict which intent classify_intent() should return and explain why.

Format each as:
Query: [the test query]
Expected Intent: [rag_answer / summarize_text / safety_check / ask_clarification]
Reason: [1 sentence explaining why]
```

---

## Prompt 7: Edge Case and Failure Mode Prompt

```text
Add edge case handling to agent_router.py for these specific failure scenarios:

1. Empty query: If query is an empty string or only whitespace, skip the Gemini API call entirely and return: "Please provide a query. The agent received an empty input."

2. Very long query: If len(query) > 2000 characters, truncate to the first 2000 characters before passing to classify_intent() and print a warning: "[WARNING] Query truncated to 2000 characters for intent classification."

3. Gemini API key missing at runtime: If GEMINI_API_KEY is None when a Gemini call is attempted (not just at startup), catch the resulting google.auth.exceptions.DefaultCredentialsError and return: "Gemini API is unavailable. Check your GEMINI_API_KEY environment variable."

4. rag_answer tool unavailable: If rag_pipeline.py cannot be imported, the rag_answer() function should catch the ImportError and return a stub response that explains the RAG pipeline is not set up, with instructions: "RAG pipeline not available. Run Session 4 setup first (rag_pipeline.py + chroma_db/)."

5. Tool function timeout: If any Gemini-calling tool function takes more than 30 seconds (simulate with a threading timeout pattern), catch the TimeoutError and return: "Tool timed out. Please try again."

Apply each change to agent_router.py and add a comment explaining why each edge case matters in a production deployment.
```

---

# What You Should Be Able to Explain After Session 6

By the end of the session, you should be able to answer these questions without reading notes:

1. What is the difference between an agent and a chatbot?
2. What does classify_intent() do and why is it a separate function from route()?
3. Why do you use response_mime_type="application/json" when calling Gemini?
4. What is a tool in the context of an agent? Why are tools just Python functions?
5. What is the ReAct pattern and where does agent_router.py use it?
6. What happens if classify_intent() returns an intent that is not in the tool_map?
7. Why is ask_clarification the fallback instead of raising an error?
8. What would need to change in agent_router.py to add a fifth tool?
9. How does this module connect to rag_pipeline.py from Session 4?
10. How would you monitor an agent like this in production?

---

## Final Session 6 Explanation

Use this when an interviewer asks: "Tell me about one of your portfolio projects."

```text
In Session 6 of my AI Engineering Portfolio, I built a simple agent router in Python called agent_router.py. The agent receives a user query, uses Gemini 1.5 Flash to classify the query's intent into one of four categories — RAG-based answering, text summarization, safety checking, or clarification — and routes the query to the corresponding Python tool function. I implemented structured JSON output from Gemini using response_mime_type="application/json" in the generation config, which makes the intent classification reliable and parseable. This module demonstrates the core ReAct pattern — Reason then Act — and shows how agent systems differ from chatbots by introducing dynamic tool routing based on LLM-driven decision-making.
```
