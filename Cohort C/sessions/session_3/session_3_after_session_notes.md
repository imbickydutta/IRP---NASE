# Session 3 After-Session Notes: Serverless-Style AI Function

## What We Built Today

Today we built `ai_handler.py` — a local implementation of the serverless function handler pattern used by AWS Lambda, Google Cloud Functions, and Azure Functions.

The script contains:
- `validate_event(event)` — validates the input event dict before any API call
- `call_gemini(text)` — calls Gemini 1.5 Flash with `response_mime_type="application/json"` to get structured classification
- `handler(event, context)` — the main orchestrator following the universal serverless signature
- `local_test()` — simulates 3 different event payloads and prints structured JSON output

We also created:
- `.env.example` — committed template file showing required environment variables
- `.env` — local-only file with the real `GEMINI_API_KEY` (never committed to git)

When you run `python ai_handler.py`, the `local_test()` function fires 3 events through the handler and prints structured JSON responses to the terminal.

---

# Why This Module Matters for AI Engineering Interviews

Almost every production AI system runs AI logic inside a function handler. The handler receives an event, calls an LLM or ML model, and returns a structured response. Whether the system is AWS Lambda, Google Cloud Functions, Azure Functions, or a Kafka consumer, the pattern is the same.

Interviewers test this in two ways. First, they ask conceptual questions: "How would you deploy an AI function to Lambda?" or "What is a cold start and how do you minimize it?" Second, they give you a code review task: they show you a handler function with no validation, hardcoded API keys, and no error handling, and ask you to identify the problems.

After today, you can answer both kinds of questions. You have written a handler, you know why validation comes before the API call, you know why `genai.configure()` lives at module level, and you know exactly what `processing_time_ms` measures.

This module also demonstrates professional habits that matter in interviews: environment variable management, structured error responses, and the separation between the AI logic (`call_gemini()`) and the orchestration logic (`handler()`).

---

# Portfolio Module Map

```
Session 1: Structured Output Prompt Engine         [DONE]
           structured_output_engine.py + output_examples.json
           Skill: prompt design, structured JSON from LLM, GenerationConfig

Session 2: LLM Logging and Evaluation Tracker      [DONE]
           llm_logger.py + llm_logs.csv + eval_summary.json
           Skill: wrapping LLM calls with observability, CSV logging, eval metrics

Session 3: Serverless-Style AI Function            [DONE — TODAY]
           ai_handler.py + .env.example
           Skill: handler(event, context) pattern, input/output contracts,
                  environment variables, cold start, structured error handling
           |
           v
Session 4: Basic RAG Pipeline                      [NEXT SESSION]
           rag_pipeline.py + chroma_db/ (local ChromaDB)
           Skill: chunking, sentence-transformers embeddings, ChromaDB, RAG query

Session 5: RAG Evaluation and Improvement          [CONNECTS TO SESSION 4]
           rag_evaluator.py + rag_eval_report.csv
           Skill: automated scoring of RAG output, uses Session 4's ChromaDB

Session 6: Simple Agent Router
           agent_router.py
           Skill: LLM-based intent classification, tool dispatch, agent loop

Session 7: Vision/OCR Mini Module
           vision_ocr_module.py + ocr_output.json
           Skill: Gemini 1.5 Flash multimodal input, structured JSON extraction from images

Session 8: Final System Design and Interview Demo
           README.md + architecture_diagram.md + demo_script.md
           Skill: portfolio documentation, system design communication, interview preparation
```

Sessions 4 and 5 share a ChromaDB vector store. Do not delete your Session 4 output files.

---

# Technical Deep-Dive: Core Concepts Explained

## The Handler Pattern and Input/Output Contracts

The `handler(event, context)` signature exists because serverless platforms need a single, predictable entry point into your code. When AWS Lambda receives an HTTP request, it deserializes the request body to a Python dict and passes it to your function as `event`. Your function returns a dict, which Lambda serializes back to JSON as the HTTP response. The platform handles all network I/O, scaling, and resource management. You handle only the transformation: event in, response out.

An input contract is the formal specification of what the event dict must contain. In `ai_handler.py`, the contract is: event must be a dict, it must have a `text` key, and the value must be a non-empty string of at least 10 characters and no more than 10,000 characters. An output contract specifies what the returned dict will always contain: `status` (always present), `summary`, `category`, `risk_level`, `processing_time_ms`, and `request_id` (always present in success responses). Downstream systems that call your handler depend on these contracts being consistently honored. A function that returns different keys depending on internal state is unreliable and hard to integrate.

## Environment Variable Management

API keys must never appear in source code. The professional Python pattern is three files working together: `.env` (local private file, listed in `.gitignore`, contains real key value), `.env.example` (committed to git, contains placeholder `GEMINI_API_KEY=your_key_here`, documents what variables are needed), and `python-dotenv` library (calls `load_dotenv()` which reads `.env` and loads its contents into `os.environ`). Code then reads the key with `os.environ.get("GEMINI_API_KEY")`. In production serverless deployments, the `.env` file does not exist — the environment variables are set directly in the Lambda or Cloud Function configuration console, and `os.environ` is populated by the platform before your code runs. `python-dotenv` is a local development convenience that mirrors this production behavior.

## Cold Start, Module-Level Initialization, and Cost Thinking

Cold start is what happens the first time a serverless function is invoked after being idle: the platform allocates a new container, loads the Python runtime, imports all your dependencies, and executes all module-level code before calling `handler()`. For a function using `google-generativeai`, cold start adds 2–4 seconds of overhead. The mitigation is to put all initialization — `load_dotenv()`, `genai.configure()`, `genai.GenerativeModel(...)` — at module level so it runs once during cold start and is reused by all subsequent warm invocations. If these calls were inside `handler()`, they would run on every single call, adding latency to warm invocations unnecessarily. Cost-per-invocation thinking changes how you write AI functions: every millisecond of execution time in Lambda costs money (billed per 100ms), every Gemini call costs tokens, and failed validations that prevent unnecessary Gemini calls are direct cost savings.

---

# What Students Should Understand

1. The `handler(event, context)` signature is not a Python convention — it is a cloud platform contract. Every serverless platform on every cloud uses this exact or equivalent signature. Understanding it means you can read any Lambda function in the world.

2. Input validation before the Gemini call is a cost and correctness decision. Calling Gemini with an empty string is a waste of money and time. The `validate_event()` function adds approximately 0 cost and 0.1ms of latency to prevent a 1–2 second Gemini call that would return a useless result.

3. `response_mime_type="application/json"` in `generation_config` is the correct way to get structured output from Gemini 1.5 Flash using the `google-generativeai` library. Without it, Gemini returns prose and `json.loads()` fails. Students should know this parameter by name.

4. Module-level initialization of the Gemini client simulates the cold start optimization used in production Lambda. The pattern is: heavy initialization once (cold), reuse forever (warm).

5. An error response that returns a structured dict with `{"status": "error", "message": "..."}` is far more useful in production than an unhandled exception. Callers can parse the error, retry, or route to a dead-letter queue. An unhandled exception gives callers nothing to work with.

6. `processing_time_ms` measures only handler execution time — from the first line of `handler()` to the return statement. It does not measure cold start time (module imports and initialization) or the caller's network latency to reach the function.

7. The `.env` + `.env.example` + `.gitignore` pattern is a professional workflow. Many junior developers skip `.env.example` (making it unclear what variables are needed) or forget `.gitignore` (exposing their API key). Both mistakes are visible in a code review.

8. `context=None` in `local_test()` is intentional and correct. In production, the platform injects a real context object. The handler uses `getattr(context, "aws_request_id", "local")` to safely read from context without crashing when it is None.

9. The `category` field uses a fixed vocabulary: `["financial", "legal", "medical", "technical", "hr", "general"]`. Constrained output values make downstream logic reliable. A system that needs to route messages by category cannot work if the category can be any arbitrary string.

10. This module is directly deployable. If you zipped `ai_handler.py` with its dependencies and uploaded it to AWS Lambda, set `GEMINI_API_KEY` as a Lambda environment variable, and pointed the handler to `ai_handler.handler`, it would work. No rewriting needed. That is the point of the pattern.

---

# Interview-Ready Explanation

```text
In Session 3 of my AI systems portfolio, I built a serverless-style AI function handler in
Python following the handler(event, context) pattern used by AWS Lambda and Google Cloud
Functions. The handler validates input, calls Gemini 1.5 Flash using the google-generativeai
library with response_mime_type set to application/json to enforce structured output, and
returns a response dict with summary, category, risk_level, and processing_time_ms fields.
The Gemini client is initialized at module level to simulate the cold start optimization, and
the API key is managed with python-dotenv so it never appears in source code. The same
function could be deployed to AWS Lambda with no code changes — only the environment variable
configuration method would change from a .env file to the Lambda console.
```

---

# What Happens When handler(event, context) Is Called

```text
Step 1: handler() records start_time = time.time() and generates a unique request_id with uuid4

Step 2: handler() calls validate_event(event)
  -> validate_event checks: is event a dict? does it have "text"? is "text" a non-empty string?
  -> If invalid: handler() returns immediately with
     {"status": "error", "message": "<reason>", "processing_time_ms": <elapsed>, "request_id": <id>}
  -> No Gemini call is made

Step 3: If valid, handler() calls call_gemini(event["text"])
  -> call_gemini() builds a prompt asking Gemini to return JSON with summary, category, risk_level
  -> call_gemini() calls model.generate_content(prompt, generation_config=config)
     where config has response_mime_type="application/json"
  -> Gemini 1.5 Flash processes the prompt (network call: ~500ms–2000ms)
  -> call_gemini() calls json.loads(response.text) to parse the JSON string into a dict
  -> call_gemini() returns the parsed dict: {"summary": "...", "category": "...", "risk_level": "..."}

Step 4: handler() checks if call_gemini() returned an error dict
  -> If status is "error": propagates with processing_time_ms added
  -> If success: continues to Step 5

Step 5: handler() calculates processing_time_ms = int((time.time() - start_time) * 1000)

Step 6: handler() assembles and returns the final response:
  {
    "status": "success",
    "summary": <from Gemini>,
    "category": <from Gemini>,
    "risk_level": <from Gemini>,
    "processing_time_ms": <int>,
    "request_id": <uuid string>
  }

Step 7: local_test() receives the dict and prints it with json.dumps(result, indent=2)
```

---

# What AI Was Used For + What Engineers Must Still Do

## What AI Generated

- The overall structure of `ai_handler.py` including all function signatures
- The Gemini prompt inside `call_gemini()` that asks for structured classification
- The `try/except` blocks and error dict formats
- The `generation_config` with `response_mime_type`
- The `local_test()` function with sample events
- The module-level docstring and inline comments

## What You Must Still Do

- Verify that `validate_event()` actually catches all the cases you need (empty string, wrong type, missing key)
- Confirm that `response_mime_type="application/json"` is present and that the Gemini response actually parses with `json.loads()`
- Check that all 3 test cases in `local_test()` produce sensible output — the category and risk_level should match the text
- Ensure `.env` is in `.gitignore` before making any git commit
- Understand and be able to explain why `genai.configure()` is at module level — AI generated it there but you must know why
- Test the error path manually by changing one event to `{"text": ""}` and confirming the error JSON is returned
- Be able to explain the cold start concept without looking at the code — this is a pure conceptual interview question

---

# Common Issues and Fixes

## Issue 1: json.JSONDecodeError when parsing Gemini response

Error message:
```
json.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```
or:
```
json.JSONDecodeError: Extra data: line 3 column 1 (char 45)
```

This happens when `response_mime_type="application/json"` is missing from `generation_config`, causing Gemini to return prose text or markdown-wrapped JSON instead of a raw JSON string.

What to ask AI:

```text
My ai_handler.py is throwing json.JSONDecodeError when parsing the Gemini response.
The response.text value is coming back as prose or markdown, not pure JSON.

Please check my call_gemini() function:
1. Is generation_config = genai.GenerationConfig(response_mime_type="application/json") present?
2. Is generation_config passed to model.generate_content() as the second argument?
3. Is the prompt explicitly asking for a JSON object (not a code block or explanation)?

Show me the corrected call_gemini() function with all three fixes confirmed.
```

## Issue 2: Gemini API returns 429 ResourceExhausted

Error message:
```
google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted
(e.g. check quota). [links....]
```

This is the Gemini free tier rate limit (approximately 15 requests per minute on the free plan). It is expected when running multiple test calls quickly.

What to ask AI:

```text
My ai_handler.py is hitting Gemini's free tier rate limit during local_test().
I need two changes:

1. Add a specific except clause for google.api_core.exceptions.ResourceExhausted in call_gemini()
   that returns {"status": "error", "message": "Gemini API rate limit exceeded. Wait 60 seconds and retry."}

2. Add import google.api_core.exceptions at the top of the file if not present.

3. In local_test(), add time.sleep(4) between each handler() call to stay under the rate limit.

Show me the exact updated code for the imports, call_gemini(), and local_test().
```

## Issue 3: GEMINI_API_KEY is None — authentication error

Error message:
```
google.api_core.exceptions.Unauthenticated: 401 Request had invalid authentication credentials.
```
or the key is `None`:
```
TypeError: api_key must be a string, got NoneType
```

This happens when `load_dotenv()` is not called before `genai.configure()`, or the `.env` file is not in the correct directory, or the variable name in `.env` does not exactly match `GEMINI_API_KEY`.

What to ask AI:

```text
My ai_handler.py is failing with an authentication error. The Gemini API key appears to be None.
Here is my setup:
- I have a .env file in the same folder as ai_handler.py
- The .env file contains: GEMINI_API_KEY=AIzaSy...

Please check my ai_handler.py for these issues:
1. Is load_dotenv() called before genai.configure()?
2. Is genai.configure(api_key=os.environ.get("GEMINI_API_KEY")) using the exact variable name?
3. Is there a print statement I can temporarily add to confirm os.environ.get("GEMINI_API_KEY") is not None?

Add a startup check that prints "API key loaded: YES" or "API key loaded: NO" at the bottom
of the module-level setup code so I can verify the key loads correctly.
```

---

# Limitations of This Module

**No real cloud deployment.** The module demonstrates the handler pattern locally but does not deploy to any cloud. AWS Lambda, Google Cloud Functions, and Azure Functions each have their own packaging requirements (ZIP files, requirements.txt, function entry point configuration) that are not covered here.

**No retry logic.** The current implementation fails immediately on a 429 rate limit. Production AI functions should implement exponential backoff retry — wait 1 second, retry; wait 2 seconds, retry; wait 4 seconds, retry — before returning an error. The `tenacity` library in Python is the standard way to add this.

**No request queuing.** At high concurrency (100+ simultaneous calls), the Gemini API will reject most requests. A production system would use a message queue (AWS SQS, GCP Pub/Sub) to buffer requests and process them at a controlled rate, never exceeding the API quota.

**No persistent logging.** The script prints results to the terminal but does not write to a log file or structured logging system. In production, every handler invocation should emit structured logs (request ID, processing time, category result, error messages) to CloudWatch, GCP Cloud Logging, or a similar system.

**`processing_time_ms` does not include cold start.** The measurement starts when `handler()` is called, not when the Python process starts. Module import time and `genai.configure()` time are not included. In a real Lambda cold start measurement, you would need platform-level metrics, not code-level `time.time()`.

**Fixed category vocabulary may not match all use cases.** The prompt constrains Gemini to return one of six categories: financial, legal, medical, technical, hr, general. Real-world content may not fit cleanly into these categories, and Gemini may occasionally return a value outside this set if the prompt is not strict enough. Production systems would add post-processing validation to ensure the returned category is in the allowed set.

---

# Key Takeaways

1. **The handler pattern is universal.** `handler(event, context)` is the same in AWS Lambda, Google Cloud Functions, and Azure Functions. Learning this pattern once means you can build serverless AI functions for any cloud platform. The AI logic inside the handler — the Gemini call, the structured output, the error handling — is what you bring to the table as an AI engineer.

2. **Validate first, call LLM second.** Never call an external AI API with unvalidated input. Validation costs microseconds and prevents wasted API calls that cost money and time. In high-volume production systems, the savings from validation are significant. The "fail fast" principle is a cost management decision, not just a correctness decision.

3. **Environment variables are a separation of concerns.** The `.env` + `python-dotenv` + `.gitignore` pattern separates configuration (which changes per environment) from code (which should be the same everywhere). This is the same pattern used in all professional Python projects. Never hardcode API keys. Never commit `.env` files.

4. **Module-level initialization is not just style — it is a performance optimization.** Placing `genai.configure()` and `genai.GenerativeModel()` at module level means they run once per cold start and are reused for all warm invocations. This is the correct pattern for any expensive initialization (LLM clients, database connections, ML model loading) in a serverless function. Students who understand this can explain cold start mitigation strategies in interviews.

---

# Session 4 Preview

In Session 4, we will build a RAG (Retrieval-Augmented Generation) pipeline.

RAG is one of the most commonly asked-about topics in AI engineering interviews. The pipeline you build in Session 4 will:
- Take a folder of text documents
- Chunk the documents into smaller passages
- Generate embeddings for each chunk using `sentence-transformers` (`all-MiniLM-L6-v2` model, local, no API needed)
- Store the embeddings in ChromaDB (a local persistent vector database)
- Accept a query, embed it, retrieve the most similar chunks from ChromaDB, and pass them to Gemini as context

Session 5 will evaluate the RAG pipeline built in Session 4 — so the ChromaDB you set up in Session 4 carries directly into Session 5.

Before Session 4, install: `pip install chromadb sentence-transformers`

The ChromaDB folder created in Session 4 will be stored locally and reused in Session 5. Do not delete it.
