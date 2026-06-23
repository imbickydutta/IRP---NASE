# Session 3 Instructor File: Serverless-Style AI Function

## Session Title

Serverless-Style AI Function

## Duration

2 hours

## Portfolio Module

Module 3 of 8 — AI Systems Interview Portfolio (Cohort C)

## Objective

By the end of Session 3, students should understand the function-as-a-service mental model and be able to build a local serverless-style AI handler in Python that accepts a structured JSON event, validates input, calls Gemini 1.5 Flash to classify and summarize text, and returns a structured JSON response — all following the universal `handler(event, context)` pattern used in AWS Lambda, Google Cloud Functions, and Azure Functions.

## Deliverable

- `ai_handler.py` — main Python script with `handler(event, context)`, `validate_event()`, `call_gemini()`, and `local_test()` functions
- `.env.example` — template showing required environment variables
- Local test output printed to terminal showing 3 structured JSON responses

---

## Strict Scope Control

### Include

- `ai_handler.py` with `handler(event, context)` function signature
- Input validation using a `validate_event()` helper
- Gemini 1.5 Flash call via `google-generativeai` library using `response_mime_type="application/json"` in `generation_config`
- Structured JSON output with `summary`, `category`, `risk_level`, and `processing_time_ms`
- `local_test()` function simulating 3 different event payloads
- `.env.example` file showing `GEMINI_API_KEY=your_key_here`
- `python-dotenv` for environment variable loading
- `try/except` error handling returning error JSON with `status: "error"` and `message` fields
- `time.time()` for measuring `processing_time_ms`
- Conceptual explanation of cold start
- Conceptual explanation of cost-per-invocation thinking

### Do Not Include

- Actual AWS Lambda deployment or any cloud deployment
- Google Cloud Functions deployment
- API Gateway configuration
- Docker or containerization
- Flask, FastAPI, or any web framework
- Async processing or `asyncio`
- Database writes or persistence
- File uploads or binary event payloads
- Any HTTP server running locally
- Authentication or JWT tokens
- OpenAI library or any non-Gemini LLM

---

# Instructor Framing

## Opening Message

Show students their portfolio folder before starting. At this point they should have two Python files from previous sessions: `structured_output_engine.py` from Session 1, and `llm_logger.py` from Session 2. Today we are not building a new feature on top of those. We are building a standalone third module that introduces a completely different pattern: the serverless function handler.

Tell students: Every major cloud platform — AWS Lambda, Google Cloud Functions, Azure Functions — uses the same `handler(event, context)` pattern to run AI logic on demand. Today we are building that pattern locally in a Python script. The cloud version is just a deployment wrapper around exactly what we are building today. If you understand the handler pattern, you understand serverless AI.

## Key Philosophy

Students in this cohort will be hired as AI engineers, not cloud infrastructure engineers. Their value is in writing the AI logic inside the handler cleanly — clean input contracts, clean output contracts, safe API key management, and graceful error handling. A cloud engineer can wrap that logic in Lambda or Cloud Functions in 10 minutes. The AI logic is what matters.

## Repeated Instructor Line

The handler does not care how it is called. It only cares about the shape of the event coming in and the shape of the response going out. That is the entire contract.

---

# Session Flow

## 0–10 min: Opening, Portfolio Recap, Show Existing Scripts

Open the student's project folder in the terminal. Show the existing files: `structured_output_engine.py` and `llm_logger.py`. Ask one student to describe what each file does in one sentence. This primes the brain to see the portfolio as a growing set of patterns — not isolated exercises.

Then introduce today's module: "We are adding `ai_handler.py`. This module teaches a completely different pattern — the function handler — which is how AI is actually deployed in production serverless environments."

Draw on the whiteboard or screen: three boxes labeled `Event In → AI Handler → JSON Out`. Explain that this is the atomic unit of serverless AI. Everything else — API Gateway, Lambda, Cloud Functions, autoscaling — is infrastructure wrapping this one box.

Ask students: "Where have you seen this pattern before?" Expected answers: AWS Lambda tutorials, Google Cloud Function docs, Zapier webhooks, Slack event handlers. Affirm all of these. The pattern is everywhere.

Tell students: by the end of this session, they will have a function they could drop into AWS Lambda with two lines of change.

## 10–20 min: Concept Explanation — What Is Serverless Architecture Thinking and Why Does It Matter

Explain serverless in AI engineering terms, not infrastructure terms. The key idea is: instead of running a server that waits for requests, you write a function that runs exactly once per event, does one job, returns a result, and then disappears.

Draw the contrast: a traditional Python Flask API runs continuously on a server, consuming memory and CPU even when idle. A serverless function costs nothing when not running. For AI workloads — which are bursty, high-cost-per-call, and event-driven — serverless is often the right architecture.

Introduce the `handler(event, context)` signature. Every serverless platform uses this exact signature. `event` is the input payload (always a dict/JSON). `context` carries platform metadata (request ID, timeout remaining, function name). The function must return a dict that can be serialized to JSON.

Explain cold start conceptually: the first invocation of a Lambda function takes longer because the Python runtime, dependencies, and your code are loaded fresh. For AI functions that import `google-generativeai`, cold starts can be 2–3 seconds. Functions that additionally load `sentence-transformers` (as Session 4's RAG pipeline will) can see cold starts of 4–6 seconds due to the model weight loading. Warm starts (subsequent calls) are much faster. Students should know this concept for interviews.

Introduce cost-per-invocation thinking: in serverless, you pay per call and per millisecond of execution. This changes how you write AI functions — you want to minimize unnecessary API calls, cache results where possible, and fail fast on invalid inputs before calling the expensive LLM.

## 20–35 min: Build the Module Using Claude Code or Cursor

Instruct students to open Claude Code or Cursor in their portfolio folder. Direct them to use Prompt 1 from the student pre-session file. Paste the prompt and generate `ai_handler.py`.

While the code generates, narrate what you are watching for:
- Does the file have a `handler(event, context)` function at the top?
- Is there a `validate_event()` function called before the Gemini API call?
- Does the Gemini call use `response_mime_type="application/json"` in `generation_config`?
- Does the output dict contain `summary`, `category`, `risk_level`, `processing_time_ms`?
- Is `python-dotenv` imported and `load_dotenv()` called?
- Is there a `local_test()` function with 3 event payloads?
- Are `try/except` blocks present returning error JSON?

If the AI-generated code is missing any of these, prompt students to use the improvement prompt immediately before explaining the code. It is better to have a complete file before the walkthrough.

Also instruct students to create `.env.example` with a single line: `GEMINI_API_KEY=your_key_here`. This is separate from their actual `.env` file which is never committed.

## 35–50 min: Walk Through Generated Code — Explain Every Function

Walk through `ai_handler.py` function by function. Do not skim. Every function teaches a different concept.

**`load_dotenv()` at module level:** Explain that this runs once when the module is imported — analogous to the initialization phase of a Lambda function before the handler is called. In production Lambda, this would be replaced by environment variables set in the Lambda console.

**`validate_event(event)`:** Explain input contracts. The function checks that `event` is a dict, that it has a `text` key, and that the value is a non-empty string. If validation fails, it returns a validation error immediately — before any Gemini call. This is "fail fast" design: never call an expensive external API with invalid input.

**`call_gemini(text)`:** Walk through the Gemini call. Show the `generation_config` with `response_mime_type="application/json"`. Explain that this tells Gemini to return valid JSON, not markdown or prose. Show the prompt structure that asks Gemini to return `summary`, `category`, and `risk_level`.

**`handler(event, context)`:** Show the orchestration logic: start timer → validate → call Gemini → add `processing_time_ms` → return response dict. Explain that the handler is a pure orchestrator — it delegates to helper functions and assembles the final response.

**`local_test()`:** Show the 3 event payloads. Explain that in production, these events would come from API Gateway, a Pub/Sub topic, or a cron trigger. Locally, we simulate them with a dictionary.

## 50–65 min: Student Follow-Along Build

Students run Prompt 1 from the student file in their own Claude Code or Cursor session. The instructor circulates and checks:
- Is `load_dotenv()` present at the top?
- Is the `.env` file created (not `.env.example`, but the actual `.env` with the real key)?
- Does `python ai_handler.py` run without import errors?

Common failure points at this stage: missing `pip install python-dotenv google-generativeai`, missing `.env` file, Gemini API key not set, `response_mime_type` missing from `generation_config`.

If any student is blocked on installation, have them run: `pip install google-generativeai python-dotenv` in the terminal. Do not let setup issues consume more than 5 minutes of group time.

Instructor rule: if a student's Gemini call returns a rate limit error (HTTP 429), direct them to the Instructor Backup Plan section of this file. Do not stop the class.

## 65–80 min: Test With Sample Inputs, Inspect Output

Have students run `python ai_handler.py` and observe the terminal output. The `local_test()` function should print 3 JSON response blocks.

Ask students to inspect the output carefully:
- Is `processing_time_ms` a number greater than 0?
- Does `category` match the type of text in the event?
- Is `risk_level` one of the expected values (low/medium/high)?
- Is the `summary` coherent and shorter than the input text?

Then ask students to manually modify one event payload — change the text to an empty string — and observe what happens. The handler should return an error JSON, not crash.

Introduce structured inspection: show students how to parse the output with `json.loads()` in a Python interactive shell or quick notebook cell. Confirm that every field is present and the types are correct.

Point out `processing_time_ms`. Ask: "What would happen to this number in a cold start versus a warm start?" Expected answer: cold start would show a much higher time because the Gemini client and model configuration must be initialized from scratch. Warm start reuses already-initialized objects. Note for the instructor: Session 3's handler does not load `sentence-transformers` — that is a Session 4 concept. Do not imply it is part of this handler.

## 80–95 min: Edge Cases, Error Handling, Failure Modes

Walk through the failure modes students should know for interviews:

**Case 1 — Empty text:** `event = {"text": ""}`. The validator should catch this and return `{"status": "error", "message": "text field is empty"}` without calling Gemini.

**Case 2 — Missing key:** `event = {"content": "some text"}` (wrong key name). The validator should catch `KeyError` and return a validation error.

**Case 3 — Gemini rate limit (HTTP 429):** The `try/except` in `call_gemini()` should catch this and return `{"status": "error", "message": "Gemini API rate limit exceeded"}`. Show students the exact error type: `google.api_core.exceptions.ResourceExhausted`.

**Case 4 — Gemini returns non-JSON despite `response_mime_type`:** Rare but possible. The handler should catch `json.JSONDecodeError` and return an error JSON rather than crashing with an unhandled exception.

**Case 5 — `context` is None:** In `local_test()`, context is passed as `None`. The handler should not crash if `context` is None — it should simply not read from it.

Ask students: "In production Lambda, what is the right behavior when your handler crashes?" Expected answer: return an error JSON with a 500-equivalent status, log the full traceback to CloudWatch/logging, and never expose internal error details to the caller.

Have students use Prompt 7 (Edge Case prompt) from the student file to improve their script to handle all 5 cases.

## 95–105 min: Concept Pause — Core Concepts Explained

This is the most important teaching block. Slow down and ensure every student can explain these concepts in interview language.

**Serverless Architecture Thinking:** Serverless does not mean "no server." It means the developer does not manage the server. The platform (AWS, GCP, Azure) handles provisioning, scaling, and teardown. For AI engineers, the benefit is automatic scaling — if 1,000 users invoke your AI function simultaneously, Lambda runs 1,000 parallel instances. You only pay for what runs.

**Function Handler Pattern:** `handler(event, context)` is the universal contract. `event` is always a dict (deserialized from JSON). `context` carries runtime metadata. The function returns a dict (serialized back to JSON). This pattern exists in every serverless platform because it is the minimal interface needed to run stateless compute. Your AI logic lives entirely inside this function.

**Input/Output Contracts:** An input contract defines exactly what shape the `event` dict must have. An output contract defines exactly what shape the returned dict will have. Both contracts must be documented and enforced. Input contracts prevent wasted API calls. Output contracts allow the calling system to reliably parse your response. This is why we have `validate_event()` and a fixed set of output keys.

**Environment Variable Management:** API keys must never be hardcoded in source code. They must never be committed to git. The pattern is: `.env` file (local development, gitignored) → `python-dotenv` loads it into `os.environ` → code reads from `os.environ`. In production, environment variables are set in the Lambda/Cloud Function configuration UI, not in files.

**Cold Start Concept:** The first invocation of a serverless function loads the entire Python runtime, installs packages, and executes module-level code. For functions using large libraries like `google-generativeai`, cold starts can add 2–5 seconds of latency. Strategies to minimize cold start: keep dependencies minimal, initialize clients at module level (not inside the handler), use provisioned concurrency in Lambda.

Write these 5 concepts on the board. Ask one student to explain each one back in their own words. Correct any misunderstandings.

## 105–115 min: Interview Discussion and Viva Practice

Use the questions from the "Questions to Discuss: Interview Perspective" section below. Run this as a rapid-fire oral quiz, not a monologue. Call on specific students.

Start with Basic Module Questions (Q1–Q5). Move to Technical Deep-Dive (Q6–Q10) only if time permits. Save Production and System Design (Q11–Q15) for strong students or if the group finishes early.

The instructor should not answer the questions — ask them, wait for student answers, then add the "Expected answer" nuance if needed.

After the quiz, ask every student to write one sentence answering: "What is the purpose of the `handler(event, context)` pattern?" Collect verbal answers. Expected: it provides a standard, platform-agnostic contract for running stateless AI logic on-demand in response to events.

## 115–120 min: Wrap-Up, Show Deliverables, Preview Next Session

Show the portfolio folder. Students should now have:
- `structured_output_engine.py` (Session 1)
- `output_examples.json` (Session 1)
- `llm_logger.py` (Session 2)
- `llm_logs.csv` (Session 2)
- `eval_summary.json` (Session 2)
- `ai_handler.py` (Session 3) — NEW
- `.env.example` (Session 3) — NEW

Read through the Session 3 Completion Checklist with the class.

Preview Session 4: "Next session we build a RAG pipeline. We will take a folder of documents, chunk them, embed them using sentence-transformers, store them in ChromaDB, and query them with Gemini. Sessions 4 and 5 are connected — Session 5 will evaluate the RAG pipeline we build in Session 4. So the work you do in Session 4 carries forward."

---

# Instructor Notes

## What to Emphasize

1. The `handler(event, context)` signature is not arbitrary — it is the universal serverless contract, and students will see this exact signature when they look at any Lambda tutorial, GCP Cloud Function example, or Azure Function.

2. Input validation before the Gemini call is not optional. Every production AI function must fail fast on bad input. A Gemini call that fails after 2 seconds wastes time and costs money. A validation check that fails in 1 millisecond costs nothing.

3. `response_mime_type="application/json"` in `generation_config` is the correct way to get structured JSON from Gemini 1.5 Flash. Students often try to parse JSON out of prose responses using string manipulation — that is brittle and wrong.

4. Environment variables are not a security feature on their own — they are a separation of concerns feature. The actual security comes from secrets managers (AWS Secrets Manager, GCP Secret Manager). But for portfolio projects, `.env` + `python-dotenv` + `.gitignore` is the correct pattern.

5. `processing_time_ms` is not just a nice-to-have. In serverless, every millisecond costs money. Students should be able to explain what contributes to execution time: import time, client initialization, network latency to Gemini, JSON parsing.

6. Cold start is conceptual in this session. Do not try to demonstrate it locally — local Python does not have cold starts. Explain it purely as a concept for interview readiness.

7. The `context` parameter is passed as `None` in `local_test()`. This is intentional and correct for local testing. In production Lambda, context carries `context.function_name`, `context.aws_request_id`, `context.get_remaining_time_in_millis()`, etc. Students should know this exists without needing to implement it today.

8. The portfolio module map matters. Students should be able to explain how `ai_handler.py` connects to the larger portfolio. The key connection is: Session 1 built structured output, Session 2 — LLM Logging and Evaluation Tracker (`llm_logger.py` wrapping Gemini calls) — built observability, Session 3 wraps both patterns in a deployable function. Session 4 — Basic RAG Pipeline — will build retrieval-augmented generation.

## Common Student Mistakes

1. **Hardcoding the API key in the script:** Students type `api_key = "AIzaSy..."` directly in `ai_handler.py`. This is a critical mistake. If they push to GitHub, the key is exposed and Google will revoke it. Fix: use `os.environ.get("GEMINI_API_KEY")` and load from `.env` via `python-dotenv`.

2. **Missing `load_dotenv()` call:** Students create the `.env` file but forget to call `load_dotenv()` at the top of the script. The error appears as `None` being passed as the API key, which triggers: `google.api_core.exceptions.Unauthenticated: 401 API key not valid`. Fix: add `from dotenv import load_dotenv` and `load_dotenv()` before the `genai.configure()` call.

3. **Not using `response_mime_type="application/json"`:** The Gemini response comes back as a prose string like "Here is the JSON: ```json {...}```". Then `json.loads()` fails with `json.JSONDecodeError: Expecting value: line 1 column 1`. Fix: add `response_mime_type="application/json"` to the `GenerationConfig`.

4. **Returning a string instead of a dict from the handler:** Students write `return json.dumps(result)` instead of `return result`. In production Lambda, the platform handles serialization. Locally, the calling code expects a dict. Fix: return the dict directly and let `json.dumps()` happen only in the print statement in `local_test()`.

5. **`validate_event()` not called before Gemini:** Students write the Gemini call at the top of the handler and add validation afterward. If validation fails, the Gemini call has already been made and charged. Fix: validate first, call Gemini only after validation passes.

6. **`time.time()` used incorrectly for `processing_time_ms`:** Students calculate `end - start` but forget to multiply by 1000 to get milliseconds. The output shows `processing_time_ms: 0.002` (seconds, not ms). Fix: `processing_time_ms = int((time.time() - start_time) * 1000)`.

7. **`try/except Exception as e` swallows all errors silently:** Students write a bare `except` block with `pass` or just `return {}`. The function appears to succeed but returns an empty dict. Fix: always return a structured error dict with at minimum `{"status": "error", "message": str(e)}`.

8. **Prompt does not specify structured output fields:** The AI generates a Gemini prompt that asks for "a summary and classification" in prose form. Gemini returns natural language, not the required fields. Fix: the prompt sent to Gemini must explicitly list `summary`, `category`, and `risk_level` as the exact JSON keys to return, with allowed values for `risk_level` (low/medium/high).

9. **`genai.configure()` called inside the handler:** This reconfigures the Gemini client on every invocation. In production Lambda, this wastes time on every warm call. Fix: call `genai.configure()` at module level, outside the handler function, so it runs once during cold start initialization.

10. **`.env` file committed to git:** Students run `git add .` and commit the `.env` file with their real API key. Fix: add `.env` to `.gitignore` immediately. Only `.env.example` should ever be committed.

## How to Control the Session

Use a strict time budget. If the code generation in the 20–35 min block produces a working file quickly, use the saved time to go deeper on the concept pause (95–105 min) or add more interview questions.

If students start asking about Docker, Lambda deployment, API Gateway, or Cloud Functions: acknowledge the question, confirm it is the right next step in production, and defer it. Say: "That is a deployment concern. We are focused today on the AI logic inside the handler. The deployment wrapper is one hour of work once you have this function working correctly."

Do not let students spend time on output formatting (pretty-printing JSON, adding colors to terminal output). The output content matters, not the presentation.

If any student completes the module early, direct them to Prompt 6 (Test Case Generation) from the student file. They should generate 5 additional event payloads and test edge cases.

---

# Questions to Discuss: Interview Perspective

## Basic Module Questions

### Q1. What is a serverless function and how did you implement one locally in this module?

Expected answer:
A serverless function is a unit of compute that runs in response to an event, executes a single task, and returns a result — without the developer managing the underlying server. In this module, I implemented the `handler(event, context)` pattern locally in Python. The `handler` function accepts a JSON event dict containing a `text` field, validates the input, calls Gemini 1.5 Flash to classify and summarize the text, and returns a structured JSON dict with `summary`, `category`, `risk_level`, and `processing_time_ms`. While this runs locally as a regular Python function, the exact same code could be deployed to AWS Lambda or Google Cloud Functions with minimal changes — the platform would call `handler(event, context)` automatically when triggered.

### Q2. What is the purpose of the `handler(event, context)` function signature and what does each parameter contain?

Expected answer:
The `handler(event, context)` signature is the universal contract for serverless functions across all major cloud platforms — AWS Lambda, Google Cloud Functions, and Azure Functions all use this exact or equivalent pattern. The `event` parameter is a Python dict deserialized from the JSON payload that triggered the function — it carries the actual input data, such as the text to be processed, a user ID, or request metadata. The `context` parameter is injected by the platform and carries runtime metadata specific to that invocation — in AWS Lambda this includes `context.aws_request_id`, `context.function_name`, and `context.get_remaining_time_in_millis()`. Locally in testing, `context` is passed as `None` since we are not running on a real platform. The function must return a dict that the platform can serialize back to JSON as the response.

### Q3. Why do you validate the event input before calling the Gemini API? What does your `validate_event()` function check?

Expected answer:
Validation before the API call is a "fail fast" principle. Calling Gemini costs money per invocation and takes network latency — typically 500ms to 2 seconds. If the event is missing the `text` key or the text is an empty string, there is nothing useful to process. The `validate_event()` function checks three conditions: that the event is a dict (not None or a list), that the `text` key exists in the event, and that the value of `text` is a non-empty string after stripping whitespace. If any check fails, the function returns a validation error dict immediately without making any API call. In production, this pattern also protects against malformed events from misconfigured upstream triggers, which is a common source of unexpected Lambda costs.

### Q4. How do you manage the Gemini API key in this module and why is that approach important?

Expected answer:
The API key is stored in a `.env` file at the project root, loaded into `os.environ` using `python-dotenv`'s `load_dotenv()` function, and read with `os.environ.get("GEMINI_API_KEY")` before being passed to `genai.configure()`. The `.env` file is listed in `.gitignore` so it is never committed to source control. A `.env.example` file with a placeholder value is committed instead, so other developers know which variables are required. This approach matters because API keys committed to public GitHub repositories are automatically scanned and revoked by Google within minutes. In production serverless deployments, environment variables are set directly in the cloud console (Lambda environment variables, GCP Secret Manager) rather than files — `python-dotenv` is a local development convenience that mirrors that production pattern.

### Q5. What structured fields does your `handler()` return and why were those specific fields chosen?

Expected answer:
The handler returns a dict with five fields: `status` (either "success" or "error"), `summary` (a one-to-two sentence condensed version of the input text), `category` (a classification of the text type, such as "financial", "legal", "medical", "technical", or "general"), `risk_level` (one of "low", "medium", or "high" indicating potential content risk), and `processing_time_ms` (the total handler execution time in milliseconds including the Gemini call). These fields were chosen because they represent a realistic AI enrichment contract — the kind of output a downstream system (a database write, a routing decision, a human review queue) would need. The fixed set of allowed values for `category` and `risk_level` is important: if Gemini were allowed to return arbitrary strings, downstream systems would break unpredictably. Constraining the output vocabulary is part of a good output contract.

## Technical Deep-Dive Questions

### Q6. How do you ensure Gemini returns valid JSON instead of prose text? What parameter is responsible for this?

Expected answer:
The key is setting `response_mime_type="application/json"` inside the `GenerationConfig` object passed to `genai.GenerativeModel.generate_content()`. This instructs Gemini 1.5 Flash to treat the output as a JSON payload and format it accordingly, rather than returning natural language prose that might contain the JSON embedded in markdown code fences. In code, this looks like: `generation_config = genai.GenerationConfig(response_mime_type="application/json")` followed by `model.generate_content(prompt, generation_config=generation_config)`. The response text can then be parsed directly with `json.loads(response.text)` without any string manipulation. Without this parameter, students often receive responses like "Here is the classification: ```json {...}```" which cause `json.JSONDecodeError` when passed to `json.loads()`. This `response_mime_type` approach is specific to the `google-generativeai` library and is the recommended way to get structured output from Gemini models.

### Q7. Where does `genai.configure()` appear in your code and why does its placement matter?

Expected answer:
`genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))` is called at module level — outside any function, near the top of the file after `load_dotenv()`. This matters because of how serverless platforms handle cold starts versus warm starts. When a Lambda function is first invoked, Python loads the entire module including all module-level code. If `genai.configure()` is placed at module level, it runs once during cold start and the configured client is reused for all subsequent warm invocations. If `genai.configure()` were placed inside the `handler()` function, it would run on every single invocation — adding unnecessary latency and re-initializing the client connection even when it is already ready. For a Gemini client, this might add 50–200ms per warm call unnecessarily. Module-level initialization is a standard Lambda optimization pattern applicable to any client — database connections, ML model loading, and LLM client configuration all benefit from this placement.

### Q8. How does `processing_time_ms` work in your implementation and what does it actually measure?

Expected answer:
`processing_time_ms` is calculated using Python's `time.time()` called at two points: immediately before the validation check at the start of the `handler()` function, and immediately after the Gemini response is received and parsed. The difference is converted from seconds to milliseconds by multiplying by 1000 and converting to an integer. The measurement captures: input validation time (microseconds), the network round-trip to Gemini's API (typically 500ms–2000ms depending on input length and load), JSON parsing of the response, and the final dict assembly. It does not capture module import time or `genai.configure()` time because those run at module level before the handler is called. In production Lambda, `processing_time_ms` is useful for identifying when the Gemini API is slow (timeout risk), for cost analysis (billing is per 100ms rounded up), and for setting appropriate function timeouts in the Lambda configuration.

### Q9. What is the difference between what `local_test()` does and how the handler would actually be invoked in production?

Expected answer:
In `local_test()`, the three event dicts are Python dictionaries constructed directly in code and passed to `handler(event, context)` with `context=None`. This simulates what would happen in production where the platform deserializes an incoming JSON payload into a Python dict before passing it to the handler. The key differences are: in production, the event arrives as serialized JSON from an upstream source (API Gateway, Pub/Sub, S3 event notification, or a scheduled cron trigger) which the platform automatically deserializes before passing to the handler; the `context` parameter would carry real platform metadata instead of `None`; and the return dict is automatically serialized back to JSON by the platform and returned as an HTTP response or written to an output topic. Locally, we handle the print/serialization ourselves in `local_test()`. The handler function itself is identical — it does not need to know whether it is being called locally or by a real cloud platform, which is exactly the benefit of the pattern.

### Q10. How does your error handling work and what would a caller receive if the Gemini API returned a 429 rate limit error?

Expected answer:
The Gemini API call in `call_gemini()` is wrapped in a `try/except` block. The `except` clause catches the `google.api_core.exceptions.ResourceExhausted` exception (which is the Python exception type for HTTP 429 from Google APIs) as well as a general `Exception` fallback for other unexpected errors. When a 429 occurs, the function returns a dict: `{"status": "error", "message": "Gemini API rate limit exceeded. Retry after a delay.", "processing_time_ms": <elapsed_ms>}`. The caller — whether a test script or a real upstream system — receives a valid, parseable JSON dict with `status: "error"` rather than an unhandled exception crash. This is important because in production serverless environments, an unhandled exception propagates as a platform error (Lambda returns a 500), which is harder to handle gracefully downstream than a well-structured error JSON. For the free tier Gemini API, students will commonly see 429 errors after approximately 15 requests per minute. The fix in production is exponential backoff retry logic or a request queue.

## Production and System Design Questions

### Q11. How would you deploy this `handler()` function to AWS Lambda and what would you need to change?

Expected answer:
The Python code in `handler(event, context)` would need almost no changes. The deployment steps would be: create a Lambda function in the AWS console, set `GEMINI_API_KEY` as a Lambda environment variable (replacing the `.env` file approach — `python-dotenv` is not needed in Lambda), package the dependencies in a Lambda layer or a ZIP file including `google-generativeai`, and set the handler to `ai_handler.handler` (Python file name dot function name). The one behavioral change is that `load_dotenv()` would have no effect in Lambda (there is no `.env` file) but it also would not break anything — `os.environ` would already have the key from the Lambda configuration. For Google Cloud Functions, the entry point would be the same function with the same signature. The local `local_test()` function would be removed or kept as dead code. The core insight for students is that the 200 lines of AI logic they wrote locally are directly deployable — the cloud platform is just a trigger and runtime wrapper.

### Q12. What would break about this module if it received 1,000 simultaneous requests in production?

Expected answer:
Several things would break or degrade. First, the Gemini free tier has a rate limit of approximately 15 requests per minute — 1,000 simultaneous requests would trigger HTTP 429 errors immediately for all but the first few requests. In production, this would require either upgrading to a paid Gemini tier with higher quota, implementing a request queue (like AWS SQS or GCP Pub/Sub) to batch and rate-limit requests, or using exponential backoff retry logic. Second, the current implementation does not log failures to any persistent store — if 900 out of 1,000 requests fail, there is no audit trail. Third, `processing_time_ms` would spike because all 1,000 Lambda instances would be cold-starting simultaneously, each making a Gemini API call. Fourth, there is no idempotency key in the event schema — if a request is retried, there is no way to detect that it was already processed, potentially charging the Gemini API twice for the same input.

### Q13. How would you monitor this function in production and what metrics would you track?

Expected answer:
For a production serverless AI function, I would track five categories of metrics. First, invocation metrics: total invocations per minute, error rate (percentage of responses with `status: "error"`), and timeout rate. Second, latency metrics: p50, p95, and p99 of `processing_time_ms` to detect Gemini API slowdowns. Third, AI-specific metrics: distribution of `category` values and `risk_level` values over time — a sudden spike in `risk_level: "high"` might indicate a prompt injection attempt or a change in the input source. Fourth, cost metrics: since Gemini charges per token, tracking input and output token counts per invocation gives a cost-per-call estimate. Fifth, cold start frequency: the difference between first-invocation latency and subsequent invocation latency, which informs decisions about Lambda provisioned concurrency. In AWS, these metrics would be sent to CloudWatch. The `processing_time_ms` field already in the response makes local benchmarking easy without any additional instrumentation.

### Q14. What is a cold start and how would you reduce its impact for this specific function?

Expected answer:
A cold start occurs when a serverless platform needs to provision a new execution environment for a function that has not been called recently or is scaling to handle more concurrent requests. For a Python Lambda function using `google-generativeai`, cold start includes: downloading and initializing the Python runtime, importing all packages (`google-generativeai` and its transitive dependencies are approximately 50MB), executing module-level code including `genai.configure()`. Cold start latency for this function would likely be 2–4 seconds. Strategies to reduce cold start impact in order of effectiveness: keep dependencies minimal and remove unused imports; initialize the Gemini client at module level rather than inside the handler (already done in our implementation); use Lambda provisioned concurrency to keep N instances pre-warmed at all times (costs money even when idle); or migrate to a language with faster cold starts for latency-critical paths (Go or Node.js). For a portfolio project, understanding and explaining cold start conceptually is sufficient — demonstrating it in production requires actual Lambda deployment.

### Q15. How would you change the input/output contract if multiple text documents needed to be processed in a single invocation?

Expected answer:
The current contract accepts a single `text` field. To support batch processing, I would change the event schema to accept a `documents` key containing a list of dicts, each with a `text` field and optionally an `id` field. The output contract would change to include a `results` list where each element corresponds to one input document and contains `id`, `summary`, `category`, and `risk_level`. The `handler` would loop through the documents list, calling `call_gemini()` for each item, and aggregate results. The key design tradeoff is latency versus throughput: processing 10 documents serially takes 10x the time of processing one, but the overall cost-per-document decreases because Lambda billing is per invocation plus per millisecond. An alternative approach is to use Gemini's batch processing capability or to make parallel Gemini calls using `concurrent.futures.ThreadPoolExecutor` within the handler — though this requires careful management of the Gemini rate limit across concurrent threads. The output contract must also handle partial failures: if 2 out of 10 documents fail Gemini processing, the response should contain 8 success dicts and 2 error dicts in the `results` list, not a top-level error that discards all 10 results.

---

# Session 3 Completion Checklist

Students should be able to confirm each item by the end of the session:

- [ ] `ai_handler.py` runs without import errors using `python ai_handler.py`
- [ ] `.env.example` file exists with `GEMINI_API_KEY=your_key_here` placeholder
- [ ] `.env` file exists locally with real API key and is listed in `.gitignore`
- [ ] `handler(event, context)` function is present with correct signature
- [ ] `validate_event()` is called before the Gemini API call inside `handler()`
- [ ] Gemini call uses `response_mime_type="application/json"` in `generation_config`
- [ ] Output JSON contains all four fields: `summary`, `category`, `risk_level`, `processing_time_ms`
- [ ] `local_test()` runs 3 different event payloads and prints results to terminal
- [ ] Local test output (3 structured JSON blocks) is visible in terminal when running `python ai_handler.py`
- [ ] Empty string event input returns an error JSON (not a crash)
- [ ] Missing `text` key in event returns an error JSON (not a KeyError exception)
- [ ] `genai.configure()` is called at module level, not inside `handler()`
- [ ] Student can explain the `handler(event, context)` pattern verbally in 60 seconds

---

# Instructor Backup Plan

## If Gemini Rate Limit Hits During Class

Gemini free tier allows approximately 15 requests per minute. If the class hits rate limits during the session:

1. Ask students to space out their `local_test()` runs — do not run all at the same time.
2. Add a `time.sleep(2)` between calls inside `local_test()` as a temporary fix.
3. Direct students to the rate limit error handling section (Q10 in interview questions) — this is a teaching moment, not a failure.
4. If the entire group is blocked, run `local_test()` only on the instructor screen and have students follow along.
5. Students can run their individual tests later when the rate limit window resets (1 minute).
6. Do not skip the concept pause (95–105 min) to compensate for lost time — the interview concepts matter more than running the code a second time.

## If a Student's Python Environment Fails

1. Confirm the student has Python 3.9 or higher: `python --version`.
2. Confirm packages are installed: `pip show google-generativeai python-dotenv`.
3. If pip install fails due to permissions, try `pip install --user google-generativeai python-dotenv`.
4. If the student is on Windows and `python` is not recognized, try `python3` or check PATH.
5. If no local fix works in 5 minutes: have the student pair with the student next to them and observe. Share the completed `ai_handler.py` after class. Do not delay the group.
6. The student can run the code in Google Colab as a fallback — the same Python code works in Colab, and the `.env` approach can be replaced with `import os; os.environ["GEMINI_API_KEY"] = "..."` at the top of the notebook for that session only.

## If AI Tool (Claude Code or Cursor) Does Not Generate a Complete File

1. Use Prompt 2 (Improvement Prompt) from the student file immediately after the first generation.
2. If the handler is missing key functions, generate them one at a time using smaller, targeted prompts.
3. As a last resort, the instructor can write the skeleton of `ai_handler.py` live on screen and students copy it, then use AI to fill in the Gemini call and validation logic.
4. A reference `ai_handler.py` should be available in the instructor's own portfolio folder to share if needed.
