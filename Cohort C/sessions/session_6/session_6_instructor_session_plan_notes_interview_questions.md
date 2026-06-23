# Session 6 Instructor File: Simple Agent Router

## Session Title

Simple Agent Router

## Duration

2 hours

## Portfolio Module

Module 6 of 8 — agent_router.py

## Session 6 Objective

By the end of Session 6, students will have a working Python script called agent_router.py that demonstrates how a simple AI agent works: it classifies a user query into one of four intents using Gemini 1.5 Flash, then routes the query to the corresponding Python tool function, runs that function, and prints the full reasoning trace — intent → tool → result.

This is the first true "agent" module in the portfolio. Students will understand why an agent is fundamentally different from a chatbot: it does not just generate a response, it decides which action to take.

## Deliverable

agent_router.py + test_queries output showing intent → tool → result for each of the 4–5 hardcoded test queries.

---

## Strict Scope Control

### Include

- agent_router.py as a single Python script
- Gemini 1.5 Flash for intent classification using google-generativeai
- response_mime_type="application/json" in generation_config for structured JSON output from Gemini
- Four tool functions as plain Python functions: rag_answer(query), summarize_text(text), safety_check(text), ask_clarification(query)
- route(query) as the main orchestrator function
- 4–5 hardcoded test queries covering each tool path
- Clear printed output in this format: Intent: <intent> | Tool: <tool_name> | Result: <result>
- A brief comment block at the top of agent_router.py describing what each component does
- Optional mention of LangGraph as the production upgrade (one paragraph in comments, no code)

### Do Not Include

- Full LangGraph implementation (mention only as a comment/note)
- CrewAI, AutoGen, or any multi-agent framework
- Autonomous loops where the agent keeps retrying or self-correcting without human input
- External API tools (no weather API, news API, search API)
- A memory system or conversation history
- Streaming output from Gemini
- A web UI or FastAPI endpoint
- ChromaDB integration inside this file — the rag_answer() tool function is a stub/simple call, or a minimal call to the existing rag_pipeline.py from Session 4; keep it clearly bounded

---

# Instructor Framing

## Opening Message

Show students the portfolio folder structure at the start of the session:

```
portfolio/
  structured_output_engine.py       ← Session 1
  llm_logger.py / llm_logs.csv      ← Session 2
  ai_handler.py                     ← Session 3
  rag_pipeline.py / chroma_db/      ← Session 4
  rag_evaluator.py / rag_eval_report.csv  ← Session 5
  agent_router.py                   ← Session 6 (building today)
```

Say this explicitly: "Every script you have built is a building block. Today we connect them. The agent we build today can call your RAG pipeline from Session 4 as one of its tools. That is what real AI systems do — they compose smaller components."

Then frame the shift: "So far, every script we wrote had one job. LLM in, answer out. Today the script makes a decision about what to do before it does anything. That is the agent pattern."

## Key Philosophy

Students are not expected to implement a production-grade agent framework. They are expected to understand the core loop: receive input → classify intent → select tool → execute tool → return result. This loop is the foundation of every agent system from simple LangChain agents to production AutoGen networks. Understanding it at this level means they can reason about any agent system in an interview.

AI generates the boilerplate. Students are responsible for explaining why each function exists, what the intent classifier is actually doing, and what breaks if Gemini returns a malformed JSON response.

## Repeated Instructor Line

The LLM is not the agent. The orchestrator that uses the LLM to make decisions and then calls tools — that is the agent.

---

# Session Flow

## 0–10 min: Opening, Portfolio Recap, Show Existing Scripts in Folder

Open the terminal and run `ls` on the portfolio folder. Show every script built so far. Name each one and say what it does in one sentence. Ask a student: "What does rag_pipeline.py do?" and "What does rag_evaluator.py do?" — these are the previous two sessions. Confirm that rag_pipeline.py is on disk because today's agent will call it as a tool. Then show the session plan: "Today we add agent_router.py. This script will use Gemini to classify incoming queries and decide which tool to run." Set the expectation: by end of class, running `python agent_router.py` should print 4–5 blocks each showing Intent, Tool, and Result.

## 10–20 min: Concept Explanation — Agent vs Chatbot Distinction

Draw or display this comparison on screen:

```
Chatbot:          User input → LLM → Response
Agent:            User input → LLM (classify intent) → Select tool → Run tool → Return result
```

Explain the key difference: a chatbot always goes to the same LLM and returns text. An agent first decides what to do. The decision-making step — intent classification — is what makes it an agent. Use a concrete analogy: a customer service chatbot answers every question with text; a customer service agent decides whether to look up your order (tool: database query), escalate the issue (tool: human handoff), or give a standard answer (tool: knowledge base). Then explain the four tools in today's module:
- rag_answer: retrieval-based answer (uses Session 4 pipeline)
- summarize_text: condensed rewrite
- safety_check: content moderation
- ask_clarification: returns a follow-up question when the query is ambiguous

Show that each tool is just a Python function. There is no magic. The agent's intelligence is in the intent classifier.

## 20–35 min: Build the Module Using Claude Code or Cursor

Instructor uses the Main Build Prompt from the student pre-session file. Paste the prompt into Claude Code or Cursor, targeting an empty agent_router.py in the portfolio folder. Watch for the generated output and verify:
- Does it import google.generativeai correctly?
- Is generation_config using response_mime_type="application/json"?
- Are all four tool functions present and clearly defined?
- Is the route() function calling the intent classifier first and then dispatching to a tool?
- Are the 4–5 test queries at the bottom in a main block?
- Does the print output include all three fields: Intent, Tool, Result?

If the model omits any of these, use a targeted follow-up prompt before moving on. Do not patch by hand during the live session — use prompts to fix.

## 35–50 min: Walk Through Generated Code — Explain Every Function

Open agent_router.py and walk through it section by section. Cover these five areas:

1. The imports block — why google.generativeai, why os for the API key, why json for parsing
2. The classify_intent(query) function — explain the prompt structure inside it, explain why response_mime_type="application/json" forces structured output, explain how the returned JSON is parsed with json.loads()
3. Each of the four tool functions — explain what each does and why it is a plain Python function (not a class, not a LangChain tool, not anything exotic)
4. The route(query) function — the orchestrator. Show that it calls classify_intent() first, reads the intent field, then uses a dictionary dispatch or if/elif chain to call the right tool. This is the agent loop.
5. The test block — explain why hardcoded test queries are used instead of user input for a portfolio deliverable. Point out that each query is designed to hit a different tool.

Ask students: "What happens if Gemini returns an intent that is not in our four tools?" — let them reason about the safety fallback. Then show the fallback in code (it should route to ask_clarification by default).

## 50–65 min: Student Follow-Along Build

Students paste the Main Build Prompt into their own Claude Code or Cursor session. The instructor circulates or monitors in a group session. Common issues at this stage:

- GEMINI_API_KEY not set — students see an AuthenticationError or a credentials error
- json.loads() throws JSONDecodeError — Gemini returned extra text around the JSON
- rag_answer() throws an ImportError because rag_pipeline.py is not in the same folder
- The intent classification returns a different field name than expected (e.g., "action" instead of "intent")

Have students run `python agent_router.py` and confirm they see output for all 4–5 test queries before moving on.

## 65–80 min: Test with Sample Inputs, Inspect Output

Run agent_router.py and show the terminal output. The expected output format for each query is:

```
Query: What is retrieval-augmented generation?
Intent: rag_answer
Tool: rag_answer
Result: [answer from RAG pipeline or stub]

Query: Summarize this paragraph: [text]
Intent: summarize_text
Tool: summarize_text
Result: [summarized text]

Query: Is this text appropriate: [text]
Intent: safety_check
Tool: safety_check
Result: SAFE / UNSAFE + reason

Query: What is neural network?
Intent: ask_clarification
Tool: ask_clarification
Result: Could you clarify whether you want a conceptual explanation, a code example, or interview tips?

Query: Kill all processes on my server
Intent: safety_check
Tool: safety_check
Result: UNSAFE — content flagged as potentially harmful
```

Walk through each output block. Ask: "Why did the RAG query go to rag_answer and not summarize_text?" — the answer is in the classify_intent() prompt and the specific wording of each query.

## 80–95 min: Edge Cases, Error Handling, Failure Modes

Cover these four failure modes explicitly:

1. Gemini returns malformed JSON — json.loads() throws JSONDecodeError. Show the try/except block. The fallback should route to ask_clarification rather than crashing.
2. Gemini rate limit (429 error) — google.api_core.exceptions.ResourceExhausted. Show the except block and the wait message. For portfolio purposes, a simple print("Rate limit hit, retrying in 5s") + time.sleep(5) is sufficient.
3. rag_answer() fails because chroma_db/ folder is missing — rag_pipeline.py raises a ChromaDB collection error. The agent should catch this and return a graceful message instead of a stack trace.
4. Empty or nonsensical query — the classifier should still return a valid intent. Show what happens when query="" is passed and confirm the fallback fires correctly.

Use the Edge Case and Failure Mode Prompt from the student file to improve the script after demonstrating each issue.

## 95–105 min: Concept Pause

Stop coding. This is the conceptual anchor block. Cover these five concepts in plain language:

Agent vs Chatbot: A chatbot receives a query and generates a text response. An agent receives a query, decides what action to take (intent classification), runs a tool, and returns the tool's output. The LLM is one component of the agent, not the whole agent.

Intent Classification as the Gateway: The quality of the entire routing system depends on the quality of the classify_intent() prompt. A poorly written classifier routes queries to the wrong tools. This is why prompt engineering for intent classification is a real, testable skill.

Tools as Plain Python Functions: In production LangChain or LangGraph agents, tools are wrapped in a Tool object with a name, description, and function. But under the hood they are still just Python functions. Today's implementation strips away that wrapping to show the essential concept.

ReAct Pattern: ReAct stands for Reason + Act. In a full ReAct loop, the agent reasons about what to do, acts by calling a tool, observes the result, and may reason again. Today's implementation is one iteration of that loop — Reason (classify intent) → Act (run tool) → Observe (print result). This is the foundation for multi-step agents.

Safety Fallback Design: Any agent system that touches user input needs a safety fallback. The safety_check() tool is a simple example. In production, you would chain this before routing — check safety first, route second. This is a common interview discussion topic.

Function Calling Concept: The OpenAI function calling API automates tool selection by binding tool schemas to the LLM. Today's implementation does tool selection manually via a JSON intent field. Students should be able to explain both approaches and articulate why JSON-based intent classification achieves the same result without vendor lock-in to OpenAI's function calling format.

## 105–115 min: Interview Discussion and Viva Practice

Use the interview questions from the section below. Run these as a class discussion or as a rapid-fire solo exercise where each student must answer one question aloud before the next student goes. Focus especially on Q5 (what makes this an agent and not a chatbot), Q8 (what happens if classify_intent returns an unknown intent), and Q13 (how would you monitor this in production).

## 115–120 min: Wrap-Up

Show agent_router.py in the terminal. Run it one final time. Point to the output and map each line back to the code: "This line is from classify_intent(), this line is from the tool function, this line is from the route() print statement." Then show the portfolio folder — 6 scripts, each doing one AI engineering job, each building toward more complex architectures. Preview Session 7: Vision and OCR Mini Module. The agent will eventually be able to call a vision tool that reads images and extracts text. That is next session.

---

# Instructor Notes

## What to Emphasize

Session 6 marks a conceptual step change in the portfolio. Emphasize this shift: up to Session 5, every module was a pipeline — input goes in, output comes out, same path every time. Session 6 introduces dynamic routing. The script now chooses its own execution path based on the input. This is the foundation of every agent architecture.

Emphasize that the tools being plain Python functions is intentional and pedagogically important. Students coming from LangChain tutorials often think tools require a specific framework. They do not. Any Python function can be a tool. The framework (LangChain, LangGraph) just provides a structured way to register and call them.

Emphasize the role of the prompt inside classify_intent(). The quality of the routing depends entirely on how well this prompt is written. If the prompt is vague, Gemini will classify ambiguous queries incorrectly. This is a direct demonstration of why prompt engineering matters in production.

Emphasize the safety_check tool as an architectural pattern, not just a function. In production, safety checking is often done as a pre-routing gate (before any tool runs), not as a parallel tool option. Students should be able to discuss both approaches.

## Common Student Mistakes

1. Missing GEMINI_API_KEY environment variable — students get a google.auth.exceptions.DefaultCredentialsError or a google.api_core.exceptions.PermissionDenied error. Fix: confirm the key is set with `print(os.environ.get("GEMINI_API_KEY"))` before initializing the Gemini client.

2. Calling genai.configure() multiple times — if the script is run in a notebook and the cell is re-run, students see unexpected behavior. Fix: wrap the configure call in an if-block or use a module-level initialization guard.

3. Not using response_mime_type="application/json" in generation_config — Gemini returns a markdown code block around the JSON instead of raw JSON. json.loads() then throws a JSONDecodeError because the string starts with ```json. Fix: always set response_mime_type="application/json" when expecting JSON output from Gemini.

4. Parsing the intent field with the wrong key — if the classify_intent prompt asks Gemini to return {"intent": "..."} but the student's code reads response_dict["action"] or response_dict["tool"], they get a KeyError. Fix: always print the raw Gemini response during development to confirm the exact JSON structure.

5. Importing rag_pipeline inside rag_answer() without confirming the file exists in the same folder — students get a ModuleNotFoundError: No module named 'rag_pipeline'. Fix: use a try/except ImportError inside rag_answer() and return a fallback message if the import fails.

6. Writing the classify_intent prompt without listing the four valid intent names explicitly — Gemini may return "question_answering" instead of "rag_answer" or "safety" instead of "safety_check". The intent dispatcher then hits the fallback for every query. Fix: the classify_intent prompt must explicitly state the four exact intent strings: rag_answer, summarize_text, safety_check, ask_clarification.

7. Using an if/elif chain without a final else fallback — if classify_intent returns an unrecognized intent, the route() function returns None silently. Fix: always include an else that calls ask_clarification() as the default.

8. Forgetting to call json.loads() on the Gemini response text — students try to access response.text["intent"] directly, which fails because response.text is a string, not a dict. Fix: parse with intent_data = json.loads(response.text) first.

9. Confusing the rag_answer tool with the full rag_pipeline.py — students try to replicate the entire RAG pipeline inside rag_answer() instead of calling the existing rag_pipeline.py function. Fix: rag_answer() should import and call a function from rag_pipeline.py, or be a clearly labelled stub if rag_pipeline.py is not available. Keep the tool function short and focused.

10. Writing test queries that are too similar to each other — if all five test queries look like factual questions, the classifier may route all of them to rag_answer. Fix: write one clearly ambiguous query, one clearly unsafe query, one explicit summarization query, and one clear RAG factual query. The variety tests the classifier.

## How to Control the Session

Use the scope rule strictly: if a student asks "can we add LangGraph?", the answer is "yes, as a comment at the bottom of the file showing what that would look like — but we are not implementing it today." If a student asks "can we add memory so the agent remembers previous queries?", the answer is "that is Session 8 territory — add a comment and move on." The most common session-killer is students chasing tool integrations (weather API, search API) instead of understanding the routing logic. Keep returning to the core loop: intent classifier → tool dispatcher → tool function → print result.

---

# Questions to Discuss: Interview Perspective

## Basic Module Questions

### Q1. What does agent_router.py do?

Expected answer: agent_router.py is a Python script that implements a simple AI agent. It receives a user query, passes the query to Gemini 1.5 Flash with a structured prompt asking Gemini to classify the query's intent, parses the returned JSON to extract the intent field, and uses that intent to dispatch to one of four Python tool functions — rag_answer, summarize_text, safety_check, or ask_clarification. The route() function orchestrates this sequence and prints a trace showing which intent was detected, which tool was called, and what the result was.

### Q2. What is the difference between an agent and a chatbot?

Expected answer: A chatbot receives a query and generates a text response using the LLM directly. The execution path is always the same: input goes to the LLM, LLM returns text. An agent receives a query, uses the LLM to decide what action to take (intent classification), then calls the appropriate tool or function to generate the actual response. The agent's intelligence is in its decision-making layer, not just in generating text. This means agents can call APIs, databases, computation functions, or other LLMs as tools, while a chatbot can only produce natural language.

### Q3. Why is intent classification done by the LLM instead of keyword matching?

Expected answer: Keyword matching works for very narrow query sets but breaks on paraphrase, synonyms, or mixed-intent queries. For example, "Can you give me a quick overview of this article?" could match keywords for both summarize and explain, but the LLM correctly identifies it as a summarization request based on semantic understanding. Using Gemini for intent classification allows the system to handle natural language variability without maintaining an exhaustive keyword list. The trade-off is latency (an extra LLM call per query) and potential classification errors if the prompt is poorly written.

### Q4. Why do you use response_mime_type="application/json" when calling Gemini for intent classification?

Expected answer: By default, Gemini returns free-form text. When we need structured output like {"intent": "summarize_text"}, free-form text is unreliable because Gemini may wrap the JSON in a markdown code block, add extra explanation sentences, or vary the field names. Setting response_mime_type="application/json" in the GenerationConfig tells Gemini to return only valid JSON with no surrounding text, making json.loads() reliable. Without this setting, you would need fragile string parsing to extract the JSON from the response, which breaks frequently in production.

### Q5. What are the four tools in this agent and why were these specific ones chosen?

Expected answer: The four tools are rag_answer (retrieves answers using the Session 4 RAG pipeline), summarize_text (condenses a longer piece of text), safety_check (evaluates whether text content is appropriate or harmful), and ask_clarification (returns a follow-up question when the query is ambiguous). These four were chosen to cover four distinct patterns common in production AI systems: retrieval, transformation, safety moderation, and clarification-seeking. Each tool maps to a real production need. rag_answer connects the agent to the existing portfolio. safety_check demonstrates the safety fallback pattern. ask_clarification shows how agents handle ambiguity rather than guessing.

## Technical Deep-Dive Questions

### Q6. Walk me through what happens when route("What is RAG?") is called.

Expected answer: First, route() passes the query string "What is RAG?" to classify_intent(). Inside classify_intent(), a Gemini 1.5 Flash API call is made with a prompt that lists the four valid intents and asks Gemini to classify the query as one of them, returning a JSON object with a single "intent" key. Gemini returns {"intent": "rag_answer"}. The function parses this with json.loads() and returns the string "rag_answer". Back in route(), the dispatcher sees "rag_answer" and calls rag_answer("What is RAG?"). The rag_answer() function either calls the rag_pipeline.py retrieve-and-generate function or returns a stub response. The result is printed as Intent: rag_answer | Tool: rag_answer | Result: [answer text].

### Q7. What happens if Gemini returns a JSONDecodeError during intent classification?

Expected answer: If Gemini returns malformed JSON — for example, if it adds an explanation sentence before or after the JSON object — json.loads() will throw a JSONDecodeError. The classify_intent() function should wrap the json.loads() call in a try/except JSONDecodeError block. In the except block, the function should log the raw response for debugging and return a default intent of "ask_clarification". This way the agent degrades gracefully by asking for clarification instead of crashing. The caller route() never sees the exception; it just receives the fallback intent and routes accordingly.

### Q8. How does the route() function dispatch to the correct tool?

Expected answer: After classify_intent() returns an intent string, route() uses either an if/elif/else chain or a dictionary mapping intent names to function objects to call the correct tool. The dictionary approach looks like: tool_map = {"rag_answer": rag_answer, "summarize_text": summarize_text, "safety_check": safety_check, "ask_clarification": ask_clarification}. Then tool_fn = tool_map.get(intent, ask_clarification) fetches the correct function, using ask_clarification as the default fallback for any unrecognized intent. The tool function is then called with the original query as the argument. This approach is cleaner than a long if/elif chain and makes it easy to add new tools by extending the dictionary.

### Q9. What is the ReAct pattern and how does this module demonstrate it?

Expected answer: ReAct stands for Reason + Act. In a full ReAct agent, the loop is: Reason about what to do → Act by calling a tool → Observe the tool's output → Reason about whether the task is complete or another action is needed → Repeat. agent_router.py implements one iteration of this loop: Reason (classify_intent calls Gemini to decide what to do) → Act (route() calls the selected tool) → Observe (the result is printed). It does not loop back to reason about the result because the tasks in this module are single-step. A full ReAct implementation would feed the tool result back into the LLM and ask whether another action is needed. LangGraph provides infrastructure for managing this multi-step loop in production.

### Q10. How would you add a fifth tool to this agent?

Expected answer: Adding a fifth tool requires three steps. First, define the new Python function — for example def translate_text(text): ... — with its implementation. Second, add the new intent name (e.g., "translate_text") to the classify_intent() prompt so Gemini knows it is a valid option. Third, add the new intent-to-function mapping in the dispatcher — either extend the if/elif chain with elif intent == "translate_text": return translate_text(query) or add an entry to the tool_map dictionary. No other changes are needed. This extensibility is one of the strengths of this architecture: tools are loosely coupled to the routing logic.

## Production and System Design Questions

### Q11. How would you deploy this agent in a production environment?

Expected answer: In production, agent_router.py would be wrapped in a web framework endpoint. The route() function would become the handler for a POST endpoint accepting a JSON body with the query field. Gemini API calls would be rate-limited and retried with exponential backoff using a library like tenacity. The classify_intent() prompt would be versioned and stored in a config file rather than hardcoded. Tool functions would be separated into individual modules. The entire agent would be containerized and deployed on a serverless platform (Cloud Run, AWS Lambda) to handle concurrent requests. Logging would capture every intent classification decision for monitoring and retraining.

### Q12. What are the failure modes of this agent in production and how would you handle them?

Expected answer: There are four main failure modes. First, Gemini rate limits (429) cause the intent classifier to fail; handle with exponential backoff and a circuit breaker. Second, Gemini returning malformed JSON causes JSONDecodeError; handle with a try/except that falls back to ask_clarification. Third, a tool function throwing an exception (e.g., rag_answer() failing because chroma_db is unavailable) causes an unhandled error; wrap all tool calls in try/except and return a structured error message. Fourth, classification drift — over time, as user query patterns change, Gemini may misclassify more queries because the classifier prompt no longer covers the query distribution; handle by logging all intent decisions and reviewing misclassification rate weekly. All four require monitoring, not just error handling.

### Q13. How would you monitor this agent in production?

Expected answer: Three layers of monitoring are needed. First, system metrics: API latency per call, rate limit hit frequency, and error rates by tool — these go into a metrics system like Prometheus or Cloud Monitoring. Second, classification quality metrics: log every query, its classified intent, the tool called, and whether the user found the result useful (via a thumbs-up/down signal); compute a weekly misclassification rate by sampling 100 random queries and manually reviewing the intent assignments. Third, safety metrics: log every query routed to safety_check, every UNSAFE classification, and every false-positive safety flag. Alerts should fire if UNSAFE rate exceeds a threshold or if the error rate on any single tool exceeds 5%.

### Q14. How does this agent architecture compare to LangChain agents?

Expected answer: LangChain agents use the same core pattern — intent classification plus tool dispatch — but wrap it in a framework with standardized Tool objects (each with a name, description, and callable function), a ToolExecutor, and agent executors that manage the ReAct loop. The key difference is that LangChain abstracts the prompt engineering for tool selection: you provide tool descriptions and LangChain builds the routing prompt automatically. agent_router.py does this manually — the classify_intent prompt is hand-written and explicitly lists the valid tool names. The manual approach gives more control and is easier to debug, but does not scale to 20+ tools. LangChain scales better for large tool libraries. For portfolios and interviews, understanding the manual version is essential because it shows you understand what the framework is doing under the hood.

### Q15. How would you make the classify_intent() function more reliable?

Expected answer: Three improvements make intent classification more reliable in production. First, add few-shot examples to the classify_intent prompt — include 2–3 example queries and their correct intents to guide Gemini's classification. Few-shot examples significantly reduce misclassification on edge cases. Second, add a confidence score to the returned JSON — ask Gemini to return {"intent": "rag_answer", "confidence": 0.92} and treat any classification below 0.7 confidence as "ask_clarification". Third, add a second-pass validation: if the classified intent and the query have low semantic similarity (measured by embedding cosine similarity), reject the classification and default to ask_clarification. This is a simple form of self-consistency checking that prevents confidently wrong classifications.

---

# Session 6 Completion Checklist

- [ ] agent_router.py file exists in the portfolio folder
- [ ] Script runs without error when `python agent_router.py` is executed
- [ ] classify_intent() uses Gemini 1.5 Flash via google-generativeai library
- [ ] generation_config sets response_mime_type="application/json"
- [ ] Gemini response is parsed with json.loads() and the "intent" field is extracted
- [ ] All four tool functions are present: rag_answer, summarize_text, safety_check, ask_clarification
- [ ] route() function correctly dispatches to the right tool based on classified intent
- [ ] Output for each test query shows Intent, Tool, and Result on separate or labelled lines
- [ ] At least 4 test queries are present covering at least 3 different tool paths
- [ ] A fallback/default case exists in the dispatcher for unrecognized intents
- [ ] try/except block handles JSONDecodeError from Gemini response parsing
- [ ] Student can verbally explain the difference between an agent and a chatbot without reading notes

---

# Instructor Backup Plan

## If Gemini Rate Limit Hits During Live Build

The free tier of Gemini 1.5 Flash allows 15 requests per minute. During a class build, multiple students hitting the API simultaneously can trigger 429 ResourceExhausted errors. Backup actions:
1. Add time.sleep(4) between classify_intent() calls in the test query loop — this spaces requests to stay under the rate limit.
2. Have one or two students use a mock classify_intent() that returns hardcoded intents while the API cools down — define mock_classify_intent(query) that uses simple keyword matching as a fallback. This keeps the routing logic demonstrable without the API.
3. Students who hit the rate limit can continue coding the tool functions and dispatcher while waiting for the API quota to reset.

## If a Student's Python Environment Fails

If a student cannot get google-generativeai installed or cannot set GEMINI_API_KEY:
1. The student should follow the instructor screen without running code.
2. Pair the student with another student who has a working environment for the follow-along build section.
3. After class, the student runs the Main Build Prompt from the pre-session file in their own Claude Code session — the script will be generated correctly even outside the live session.
4. Provide the session's completed agent_router.py as a reference file — the student reviews, annotates, and runs it locally as a catch-up task.
5. Do not skip the interview discussion section for students with setup failures — that is the highest-value part of the session and does not require a working environment.

## If rag_pipeline.py Is Not Available on Student Machines

If students did not complete Session 4 or their chroma_db/ folder is missing, the rag_answer() tool will fail at import time. This is expected and acceptable. The fix:
1. Instruct students to use a stub version of rag_answer() that does not import rag_pipeline.py — it simply returns a hardcoded or Gemini-generated answer with a [RAG stub] prefix.
2. The routing logic, intent classification, and all other tools remain fully functional. The rag_answer tool just returns a stub response instead of actual retrieved content.
3. This is a good teaching moment: explain that in production, tool functions fail independently. One broken tool does not take down the entire agent. The dispatcher and classifier still work correctly.

## If the Session Runs Short (Unlikely)

If the build completes faster than expected and there is remaining time:
1. Ask the class to write a sixth test query that should route to safety_check and one that tests the fallback.
2. Discuss the LangGraph optional extension: show a text-only description of what agent_router.py would look like as a LangGraph StateGraph — three nodes: classify_intent node, tool_dispatch node, return_result node.
3. Run a rapid-fire interview round: each student must answer one question from the Q6–Q15 section without preparation.

---

# Appendix: Sample Expected Terminal Output

When a student runs `python agent_router.py` with the five test queries, the expected terminal output format is:

```
============================================================
Query: What is retrieval-augmented generation and how does it work?
Intent: rag_answer
Tool: rag_answer
Result: Retrieval-augmented generation (RAG) is a technique that combines document retrieval with LLM generation. A query is embedded and used to find relevant chunks from a vector database. Those chunks are passed as context to the LLM, which generates an answer grounded in the retrieved content rather than relying solely on its training data.
============================================================
Query: Summarize this: Large language models are trained on vast amounts of text data and can generate coherent, contextually relevant responses across a wide range of topics. They use transformer architectures with attention mechanisms to understand and generate language.
Intent: summarize_text
Tool: summarize_text
Result: Large language models use transformer architectures trained on massive text datasets to generate coherent responses. Their attention mechanisms allow them to understand and produce contextually relevant language across diverse topics.
============================================================
Query: Check if this is appropriate: I want to hack into the school server and change my grades.
Intent: safety_check
Tool: safety_check
Result: Verdict: UNSAFE | Reason: The content describes unauthorized access to computer systems, which is illegal and harmful.
============================================================
Query: Tell me something interesting.
Intent: ask_clarification
Tool: ask_clarification
Result: Could you tell me more about what kind of topic interests you — are you looking for something about science, AI, history, or a specific field you are studying?
============================================================
Query: Kill all background processes.
Intent: safety_check
Tool: safety_check
Result: Verdict: UNSAFE | Reason: This phrasing could be interpreted as a request for system-level commands that cause data loss or service disruption.
============================================================
```

Instructors should show this expected output at the start of the session (block 0–10 min) so students know what they are building toward. It sets a concrete target that makes the session more focused.
