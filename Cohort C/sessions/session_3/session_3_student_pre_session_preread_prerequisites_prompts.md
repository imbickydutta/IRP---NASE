# Session 3 Student Pre-Session File: Serverless-Style AI Function

## What We Are Building

In this portfolio, you are building 8 standalone AI engineering modules in Python. Each module demonstrates a different pattern used in real AI systems. You are not building one big app — you are building a portfolio of scripts and notebooks that show you understand how AI systems work in production.

At the end of all 8 sessions, your portfolio will contain scripts covering structured output, logging and evaluation, serverless handlers, RAG pipelines, RAG evaluation, fine-tuning, agentic workflows, and LLMOps.

## Session 3 Goal

In Session 3, you will build a local implementation of the serverless function handler pattern — the foundational design used by AWS Lambda, Google Cloud Functions, and Azure Functions.

You will write a Python script that:
- follows the `handler(event, context)` signature used by every serverless platform
- accepts a JSON event dict as input
- validates the event before doing any AI processing
- calls Gemini 1.5 Flash to classify and summarize the text
- returns a structured JSON response with fixed fields
- tests itself with 3 different event payloads
- manages the API key safely using environment variables

## Session 3 Deliverable

- `ai_handler.py` — main Python script
- `.env.example` — template file for environment variables (committed to git)
- Local test output in terminal — 3 structured JSON responses printed when you run `python ai_handler.py`

---

# Pre-Read

## Why Does This Module Exist in the Portfolio?

Session 1 taught you how to produce structured output from an LLM. Session 2 taught you how to log and evaluate LLM calls. But neither of those sessions addressed a key production question: how do you make an AI function callable from anywhere — a web app, a mobile app, a scheduled job, or another service?

The answer in modern AI systems is serverless functions. AWS Lambda, Google Cloud Functions, and Azure Functions all let you deploy a Python function that runs on demand, scales automatically, and costs nothing when idle. Every one of these platforms uses the same handler pattern: `handler(event, context)`.

Building this pattern locally, before deploying to a cloud, is the right engineering approach. You understand the function first, then you deploy it. The cloud deployment is a 10-minute operation once the function works correctly.

This module also introduces two concepts that come up in nearly every AI engineering interview: environment variable management (how to keep API keys out of code) and cold start (why the first invocation of a serverless function is slower than subsequent ones).

## Portfolio Module Map

```
Session 1: Structured Output Prompt Engine
           structured_output_engine.py + output_examples.json
           Pattern: prompt design + structured JSON from LLM
           |
           v
Session 2: LLM Logging and Evaluation Tracker
           llm_logger.py + llm_logs.csv + eval_summary.json
           Pattern: wrapping LLM calls with observability
           |
           v
Session 3: Serverless-Style AI Function  <-- YOU ARE HERE
           ai_handler.py + .env.example
           Pattern: handler(event, context) + input/output contracts
           |
           v
Session 4: Basic RAG Pipeline
           rag_pipeline.py + chroma_db/ (local vector store)
           Pattern: embed + store + retrieve + generate
           |
           v
Session 5: RAG Evaluation
           rag_evaluator.py + rag_eval_report.csv
           Pattern: automated quality scoring of RAG output
           (CONNECTS TO SESSION 4 — uses the same ChromaDB)
           |
           v
Session 6: Simple Agent Router
           agent_router.py
           Pattern: LLM-based intent classification + tool dispatch
           |
           v
Session 7: Vision/OCR Mini Module
           vision_ocr_module.py
           Pattern: multimodal Gemini input, structured JSON extraction
           |
           v
Session 8: Final System Design and Interview Demo
           Pattern: portfolio documentation, architecture diagram, interview preparation
```

Sessions 4 and 5 are directly connected. The ChromaDB vector store built in Session 4 is evaluated in Session 5. Do not delete your Session 4 files after that session.

## Key Concepts to Revise Before This Session

Before attending Session 3, make sure you can explain these concepts in your own words:

1. **Environment variables** — What is `os.environ`? Why do applications read configuration from environment variables instead of hardcoding values in code? What happens if you hardcode an API key?

2. **JSON as a data contract** — What is the difference between a Python dict and a JSON string? When would you use `json.dumps()` versus `json.loads()`? Why does a function that returns a fixed-schema dict create a reliable contract for its callers?

3. **try/except in Python** — What is the difference between a caught exception and an unhandled exception? What should a function do when it cannot complete its task — raise the exception, return None, or return an error dict? In a serverless context, which is most useful?

4. **Function signatures as contracts** — What is the difference between a function that accepts `**kwargs` and one with a fixed signature like `handler(event, context)`? Why do cloud platforms enforce a specific function signature?

5. **`time.time()` for performance measurement** — How do you calculate elapsed time in Python? Why would an AI function track its own execution time in the response?

6. **`python-dotenv`** — What does `load_dotenv()` do? Where does it look for the `.env` file? What is the difference between `.env` (private, gitignored) and `.env.example` (committed, has placeholder values)?

7. **Gemini `generation_config`** — In the `google-generativeai` library, what is `GenerationConfig`? What does `response_mime_type="application/json"` do to the Gemini response?

8. **Input validation before external calls** — What is the "fail fast" principle? Why should you validate inputs before making an API call rather than after?

## Technical Explanation of the Core Concept

The serverless function handler is the most important deployment pattern in modern AI systems. Here is the mental model:

Imagine a function that lives in the cloud. It is not running continuously. It is asleep. When an event arrives — an HTTP request, a message from a queue, a file upload notification, a scheduled timer — the cloud platform wakes up your function, passes the event to it as a Python dict, and waits for a dict response. Your function does its work (validates input, calls the LLM, formats the output), returns the dict, and goes back to sleep. The platform takes the returned dict, serializes it to JSON, and delivers it as the response.

From your perspective as the function author, the entire interface is: `def handler(event, context)`. You never write HTTP server code. You never manage connections. You never handle concurrent requests. The platform handles all of that.

The `event` dict is the serialized JSON input. For an HTTP trigger, it might look like: `{"text": "Quarterly revenue fell 12% due to supply chain disruptions.", "source": "financial_report"}`. For a queue message trigger, it might look like: `{"body": "...", "messageId": "abc123", "timestamp": 1704067200}`. The shape of the event depends on the trigger, but your handler always receives it as a Python dict.

The `context` object carries platform metadata: which function this is, how much time is left before timeout, a unique request ID for tracing. In local testing, you pass `None` for context. In production, the platform injects it automatically.

The return value is always a dict. The platform serializes it to JSON. Your handler never calls `json.dumps()` — it just returns the dict.

This pattern is simple, powerful, and universal. Once you understand it, you can read any Lambda function, any Cloud Function, or any Azure Function and immediately understand its structure.

---

# Setup Before Class

## Required pip Installs

Run these commands in your terminal before the session. Do this in the same Python environment (virtualenv or conda env) where you have been working for Sessions 1 and 2.

```
pip install google-generativeai
pip install python-dotenv
```

If you need to verify existing installations:

```
pip show google-generativeai
pip show python-dotenv
```

Expected output for `pip show google-generativeai` should show version 0.7.0 or higher.

## Gemini API Key Setup

If you do not have a Gemini API key yet:

1. Go to https://aistudio.google.com
2. Sign in with a Google account
3. Click "Get API Key" in the left sidebar
4. Create a new API key
5. Copy the key — it starts with "AIza..."

Create a file named `.env` in your portfolio folder (the same folder where `structured_output_engine.py` and `llm_logger.py` live):

```
GEMINI_API_KEY=AIzaSy...your_actual_key_here...
```

Also create `.env.example` in the same folder:

```
GEMINI_API_KEY=your_key_here
```

Add `.env` to your `.gitignore` file immediately. The `.env.example` file is safe to commit — it has no real key.

## Verify Your Setup

Run this one-time test before the session to confirm Gemini works:

```python
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say: setup verified")
print(response.text)
```

Expected output: `setup verified` or similar confirmation text. If you see an authentication error, double-check that your `.env` file is in the correct folder and the key is spelled correctly.

---

# Sample Data to Prepare Before Class

Prepare 3 short text snippets that you can use as event payloads during the session. Each should be 2–4 sentences long. Choose different types so the category classification is interesting.

Here are examples — you can use these or write your own:

```text
Snippet 1 (Financial):
The company reported a 23% decline in quarterly earnings, citing increased raw material costs
and reduced consumer demand in the Asia-Pacific region. The board has approved a restructuring
plan that includes workforce reductions in non-core divisions.

Snippet 2 (Technical/IT):
A critical SQL injection vulnerability was discovered in the user authentication module.
The vulnerability allows unauthenticated users to bypass login by submitting a specially
crafted payload in the username field. A patch has been developed and is pending QA review.

Snippet 3 (General/Neutral):
The annual team offsite will be held at the Riverside Conference Center on March 14th and 15th.
All team members are requested to confirm attendance by February 28th. Travel reimbursements
will be processed within 10 business days after the event.
```

You will use these as the text values in your 3 event payloads inside `local_test()`.

---

# Prompts for Session 3

Use these prompts during the session when the instructor directs you. Paste them into Claude Code or Cursor.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI engineering portfolio. I have already built:
- Session 1: structured_output_engine.py — a structured output prompt engine using Gemini 1.5 Flash
- Session 2: llm_logger.py — an LLM logging and evaluation tracker wrapping Gemini calls

For Session 3, I need to build a standalone Python script called ai_handler.py that implements
a local serverless-style AI function handler.

Create a file named ai_handler.py with the following exact structure and requirements:

IMPORTS AND SETUP:
- Import: os, json, time
- Import: google.generativeai as genai
- Import: from dotenv import load_dotenv
- Call load_dotenv() at module level (outside all functions)
- Call genai.configure(api_key=os.environ.get("GEMINI_API_KEY")) at module level
- Initialize the Gemini model at module level: model = genai.GenerativeModel("gemini-1.5-flash")

FUNCTION 1 — validate_event(event):
- Accepts one argument: event (expected to be a dict)
- Returns a tuple: (is_valid: bool, error_message: str or None)
- Checks: event is a dict, event has a "text" key, event["text"] is a non-empty string after strip()
- Returns (True, None) if valid
- Returns (False, "specific error description") if invalid

FUNCTION 2 — call_gemini(text):
- Accepts one argument: text (string)
- Builds a prompt asking Gemini to analyze the text and return a JSON object with exactly these keys:
  - "summary": a 1-2 sentence summary of the text
  - "category": one of ["financial", "legal", "medical", "technical", "hr", "general"]
  - "risk_level": one of ["low", "medium", "high"]
- Uses generation_config with response_mime_type="application/json" to enforce JSON output
- Parses the response with json.loads(response.text)
- Returns the parsed dict
- Wraps the entire operation in try/except and returns {"status": "error", "message": str(e)} on failure

FUNCTION 3 — handler(event, context):
- Accepts two arguments: event (dict) and context (can be None for local testing)
- Records start time using time.time()
- Calls validate_event(event) — if invalid, returns immediately with:
  {"status": "error", "message": <validation error>, "processing_time_ms": <elapsed ms>}
- Calls call_gemini(event["text"]) if validation passes
- If call_gemini returns a dict with "status": "error", propagates the error with processing_time_ms added
- On success, returns:
  {
    "status": "success",
    "summary": <from gemini>,
    "category": <from gemini>,
    "risk_level": <from gemini>,
    "processing_time_ms": <int, milliseconds elapsed>
  }
- Wraps the entire handler body in try/except returning error JSON on unexpected failures

FUNCTION 4 — local_test():
- Defines 3 different event dicts with a "text" key:
  Event 1: a financial/business text (2-3 sentences about earnings, revenue, or market conditions)
  Event 2: a technical/security text (2-3 sentences about a software vulnerability or system issue)
  Event 3: an empty text to test error handling: {"text": ""}
- Calls handler(event, context=None) for each event
- Prints "--- Event N ---" before each result
- Prints the result using json.dumps(result, indent=2)
- Adds a blank line between results

MAIN BLOCK:
- if __name__ == "__main__": call local_test()

ADDITIONAL REQUIREMENTS:
- Add a comment above each function explaining what it does in one line
- Add inline comments inside handler() explaining each step
- Do NOT use Flask, FastAPI, or any web server
- Do NOT make any HTTP server or port listening
- Do NOT use the openai library — only google-generativeai
- Do NOT use sentence-transformers in this script (no embeddings needed)
- processing_time_ms must be an int, not a float

The script should run successfully with: python ai_handler.py
```

---

## Prompt 2: Improvement Prompt

```text
Improve the ai_handler.py script I just generated. Apply these improvements:

1. Error handling improvements:
   - In call_gemini(), add a specific except clause for google.api_core.exceptions.ResourceExhausted
     that returns {"status": "error", "message": "Gemini API rate limit exceeded. Retry after a delay."}
   - In call_gemini(), add a specific except clause for json.JSONDecodeError that returns
     {"status": "error", "message": "Gemini returned non-JSON response. Check the prompt format."}
   - In handler(), if context is not None, extract and log context.aws_request_id if it exists
     (use getattr(context, "aws_request_id", "local") to avoid AttributeError)

2. Validation improvements:
   - Add a check for maximum text length: if len(event["text"]) > 10000, return an error
     saying "text exceeds maximum length of 10000 characters"
   - Add a check that event["text"] contains at least 10 characters after strip()

3. Output improvements:
   - Add a "request_id" field to all responses (success and error) using a uuid4 string
     generated at the start of handler() — import uuid at the top
   - Ensure processing_time_ms is always present in every response dict, including all error paths

4. Code quality:
   - Add a module-level docstring at the top explaining: what the script does, the handler
     signature, the input contract (event must have "text" key), and the output contract
     (fields: status, summary, category, risk_level, processing_time_ms, request_id)

Do not change the function signatures or the overall structure. Only add the improvements listed above.
```

---

## Prompt 3: Debugging Prompt — Gemini Returns Non-JSON or Rate Limit Error

```text
My ai_handler.py is running into one of these two errors. Please help me debug both.

ERROR 1 — json.JSONDecodeError when parsing Gemini response:
The error appears as:
  json.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
or:
  json.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

This happens because Gemini is returning a prose response or markdown-wrapped JSON instead of
pure JSON. Please check:
1. Is response_mime_type="application/json" set in generation_config?
2. Is the GenerationConfig object being passed to generate_content() correctly?
3. Is the prompt explicitly asking for a JSON object with the exact keys?
Show me the corrected call_gemini() function with these fixes applied.

ERROR 2 — google.api_core.exceptions.ResourceExhausted (HTTP 429 rate limit):
The error appears as:
  google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted
  (e.g. check quota).

This is Gemini's free tier rate limit. Please:
1. Add a specific except clause for google.api_core.exceptions.ResourceExhausted in call_gemini()
2. Return a structured error dict: {"status": "error", "message": "Rate limit exceeded. Wait 60 seconds."}
3. Add import google.api_core.exceptions at the top of the file if not already present
4. In local_test(), add a time.sleep(2) between each handler() call to reduce rate limit hits

Show me the exact corrected code for the imports, call_gemini() function, and local_test() function.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the ai_handler.py script I just built as if you are teaching an AI engineering student
who understands Python but is new to serverless concepts.

Explain each of the following:

1. Why is load_dotenv() called at module level instead of inside handler()?
   What is the difference in behavior between the two placements?

2. Why is genai.configure() called at module level instead of inside handler()?
   What is the serverless cold start concept and how does module-level initialization relate to it?

3. What is the purpose of validate_event()? Why is it called before call_gemini()?
   What is the "fail fast" principle?

4. In call_gemini(), what does response_mime_type="application/json" do?
   What would happen to the output if this parameter were removed?

5. In handler(), how is processing_time_ms calculated?
   What exactly does it measure — what is included and what is excluded from the measurement?

6. What is the input contract of handler()? What must the event dict contain?

7. What is the output contract of handler()? What fields will always be present in the returned dict?

8. Why does local_test() pass context=None? What would context contain in a real Lambda function?

9. What is the difference between returning json.dumps(result) versus returning result from handler()?
   Why is returning the dict the correct approach for a serverless handler?

10. If this script were deployed to AWS Lambda unchanged, what single configuration change would
    be needed to handle the GEMINI_API_KEY instead of the .env file approach?

Do not rewrite the code. Only explain the concepts and design decisions.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Help me prepare to explain the ai_handler.py module to a technical interviewer.

Structure the explanation as follows:

1. What did you build? (2 sentences — what the script does at a high level)

2. What problem does it solve? (1-2 sentences — why this pattern exists in AI engineering)

3. What is the handler(event, context) pattern? (2-3 sentences — explain it as if to someone
   who has seen AWS Lambda but never looked inside a handler function)

4. What is the input contract? (list the exact shape of the event dict)

5. What is the output contract? (list all fields in the success response and error response)

6. Why do you validate input before calling Gemini? (1-2 sentences — cost and correctness reasoning)

7. How do you manage the API key? (2 sentences — the .env + python-dotenv + .gitignore pattern)

8. What is a cold start and how does your implementation minimize its impact? (2-3 sentences)

9. What are two things you would change to make this production-ready on AWS Lambda?
   (2 specific, technical changes — not "add better logging" in vague terms)

10. How does this module fit into your portfolio? (1 sentence connecting it to Session 1 and 2)

Keep the language technical but clear. Avoid using words like "amazing" or "powerful".
Use precise terms: function handler, input contract, output contract, cold start, environment variable,
rate limit, structured JSON output, generation_config.
```

---

## Prompt 6: Test Case Generation Prompt

```text
Generate 5 additional event payloads I can use to test my ai_handler.py script.

Requirements for the test payloads:
1. Each payload must be a Python dict with a "text" key
2. The text values should represent different content categories:
   - one legal/compliance text
   - one medical/health text
   - one HR/people management text
   - one text that is borderline high risk (something that would likely get risk_level: "high")
   - one very short text (exactly 15-20 characters) that passes validation but is minimal

For each payload, provide:
- The Python dict
- A prediction of what category Gemini will assign
- A prediction of what risk_level Gemini will assign
- Your reasoning for those predictions

Format each test case as a ready-to-paste Python dict that can be passed directly to:
result = handler(event, context=None)
print(json.dumps(result, indent=2))
```

---

## Prompt 7: Edge Case and Failure Mode Prompt

```text
Review my ai_handler.py and add handling for these additional edge cases and failure modes.
Implement each fix:

EDGE CASE 1 — context is not None but lacks expected attributes:
In handler(), when context is not None, the code tries to access context.aws_request_id.
But in local testing, someone might pass a custom object or a dict instead of None.
Add safe attribute access using getattr() with a fallback value of "unknown".

EDGE CASE 2 — Gemini returns a JSON object missing expected keys:
call_gemini() parses the JSON successfully, but the returned dict is missing "category"
or "risk_level". The handler then returns a success response with those fields as None.
Add a check after json.loads(): verify that all three required keys are present.
If any key is missing, return: {"status": "error", "message": "Gemini response missing required fields: <list of missing keys>"}

EDGE CASE 3 — event["text"] contains only whitespace:
Currently validate_event() calls .strip() but only checks the length of the stripped string.
However the check should happen on the stripped version, not the original.
Confirm this is handled correctly, or fix it if not.

EDGE CASE 4 — Gemini returns a valid JSON array instead of a JSON object:
If json.loads() returns a list instead of a dict, the subsequent dict access will fail.
Add a type check: if the parsed result is not a dict, return an error.

EDGE CASE 5 — Very long processing time (Gemini timeout):
The google-generativeai library will raise a google.api_core.exceptions.DeadlineExceeded
exception if the request times out. Add a specific except clause for this in call_gemini()
returning: {"status": "error", "message": "Gemini API request timed out."}

Show the updated validate_event() and call_gemini() functions with these fixes applied.
Also update the local_test() function to add one additional test case demonstrating
the missing-key edge case (pass a text that is valid but simulate the check).
```

---

# What You Should Be Able to Explain After Session 3

By the end of this session, you should be able to answer these questions without reading your code:

1. What is the `handler(event, context)` function signature and why is it the same across AWS Lambda, Google Cloud Functions, and Azure Functions?

2. What does the `event` parameter contain and what does the `context` parameter contain?

3. Why do you validate the event before calling the Gemini API? What is the "fail fast" principle?

4. What does `response_mime_type="application/json"` do in `generation_config` and what breaks if you remove it?

5. Why is `genai.configure()` placed at module level and not inside `handler()`? How does this relate to cold start?

6. What is the input contract of your `handler()` function? What is the output contract?

7. How do you keep your Gemini API key out of your source code? What three files are involved?

8. What is a cold start in serverless computing and what causes it to be slow for Python AI functions?

9. What does your error handling return when the Gemini API returns a 429 rate limit error?

10. If you deployed this script to AWS Lambda today, what would the platform call and what would it need from you?

---

## Final Session 3 Explanation

Use this when an interviewer asks you to describe this module:

```text
In Session 3 of my portfolio, I built a serverless-style AI function handler in Python. The
script implements the handler(event, context) pattern — the same function signature used by
AWS Lambda and Google Cloud Functions — that accepts a JSON event dict, validates the input,
calls Gemini 1.5 Flash using the google-generativeai library to classify and summarize the
text, and returns a structured JSON response with summary, category, risk_level, and
processing_time_ms fields. The API key is managed using python-dotenv so it never appears
in source code. The Gemini client is initialized at module level to simulate the cold start
optimization used in production serverless deployments. The same handler function could be
deployed to AWS Lambda or Google Cloud Functions with minimal changes — the local test
harness simulates exactly what the cloud platform would do when triggering the function.
```
