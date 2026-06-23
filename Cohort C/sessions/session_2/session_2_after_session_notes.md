# Session 2 After-Session Notes: LLM Logging and Evaluation Tracker

## What We Built Today

Today we built the observability layer of our AI engineering portfolio. Starting from the Gemini API call we established in Session 1, we wrapped it in a logging function and tracked every call with precision.

The three deliverables created in this session:

- llm_logger.py — the main Python module containing log_llm_call(), generate_summary(), and print_report()
- llm_logs.csv — a running log file with one row per LLM call, created automatically when the script runs
- eval_summary.json — an aggregated summary file with total calls, pass count, fail count, average latency, and average quality score

We ran 7 hardcoded test cases through the logger, covering successful calls, failed calls, edge cases (empty prompt), and calls with varying expected quality. Each run appended a new row to the CSV. At the end, print_report() displayed a readable terminal summary showing how the system performed across all test cases.

---

# Why This Module Matters for AI Engineering Interviews

When a hiring manager or technical interviewer asks "how would you monitor an LLM in production?", most candidates answer vaguely. They say "I would add logging" without being able to describe what fields they would log, how they would estimate cost, how they would handle failures, or how they would surface quality metrics over time.

Session 2 gives you a concrete, working answer. You did not just talk about logging — you built a logger that tracks seven fields per call, handles exceptions without crashing, writes to two output formats, and computes aggregated statistics. This is production thinking, and it is rare among candidates who come primarily from a prompting or notebook background.

The module also demonstrates that you understand the difference between a working prototype and a deployable component. A prototype calls an LLM and prints the output. A component wraps the call, measures it, logs it, costs it, and reports on it. Session 2 is your first step from prototype to component.

---

# Portfolio Module Map

Use this to understand where Session 2 sits in the full portfolio and which sessions depend on it.

```
Session 1 — Structured Output Prompt Engine (structured_output_engine.py with Gemini call)  [DONE]
    structured_output_engine.py + output_examples.json
    |
    v
Session 2 — LLM Logging and Evaluation Tracker  [DONE - TODAY]
    llm_logger.py + llm_logs.csv + eval_summary.json
    |
    v
Session 3 — Serverless-Style AI Function
    ai_handler.py + .env.example
    (log_llm_call pattern reusable across sessions)
    |
    v
Session 4 — Basic RAG Pipeline -----------> Session 5 — RAG Evaluation and Improvement
    rag_pipeline.py + chroma_db/               rag_evaluator.py + rag_eval_report.csv
    (directly connected — Session 5 reads Session 4's ChromaDB)
    |
    v
Session 6 — Simple Agent Router
    agent_router.py
    |
    v
Session 7 — Vision/OCR Mini Module
    vision_ocr_module.py + ocr_output.json
    |
    v
Session 8 — Final System Design and Interview Demo
    README.md + architecture_diagram.md + demo_script.md
```

Sessions done: 1, 2. Next: Session 3.
The log_llm_call() pattern from Session 2 is reused in Sessions 3, 4, and 7.

---

# Technical Deep-Dive: LLMOps, Observability, Monitoring, Evaluation Mindset, and Production Readiness

LLMOps is the operational discipline that governs how LLM-powered systems are built, deployed, monitored, and improved over time. It is analogous to MLOps for traditional machine learning, but with additional concerns specific to LLMs: prompt versioning (because the prompt is part of the model behavior), output non-determinism (the same prompt can produce different outputs on different calls), and cost unpredictability (token-based billing means a single poorly-written prompt can cost orders of magnitude more than a well-engineered one). Session 2 introduces the most fundamental LLMOps practice: logging every call. Every production LLM system, from a simple chatbot to a multi-agent pipeline, must have a logging layer. Without it, failures are invisible, cost trends are untracked, and quality degradation goes undetected until a user complains.

Observability is a property of a system that lets you understand its internal state from its external outputs. In the context of LLM systems, observability means that for any call that happened — today, last week, or three months ago — you can answer: what prompt was sent, what response was returned, how long it took, how much it cost, and whether the output was good. Session 2's logger provides all five dimensions of observability. The distinction between monitoring and evaluation is important: monitoring is real-time or near-real-time tracking of operational health metrics (latency, error rate, cost per day), while evaluation is the offline or batch measurement of output quality (are the responses correct, complete, relevant, and safe). Session 2 provides the foundation for both: the latency and failure_reason fields feed monitoring, while the quality_score field initiates the evaluation mindset.

Production readiness is not a binary state — it is a spectrum. A notebook that calls Gemini and prints output is zero percent production-ready. A script that wraps the call with error handling, logs every invocation with cost and latency data, writes to a structured output file, and produces an aggregated report is meaningfully closer to production-ready. Session 2 moves your Gemini integration along that spectrum. The remaining gaps — concurrent write safety, PII redaction, async logging, database persistence, automated quality evaluation — are real gaps, but identifying them is itself a demonstration of engineering maturity. In an interview, the ability to say "here is what my module does and here is exactly what it does not do yet" is more valuable than claiming a fully production-ready system.

---

# What Students Should Understand

1. The log_llm_call() function is a wrapper — it does not change what the Gemini API call does, it adds observability around it. The return value is still the response text.

2. The token estimation formula len(prompt.split()) * 1.3 is an approximation. It overcounts for code-heavy prompts and undercounts for prompts with many technical symbols. It is accurate enough for cost awareness but not for billing.

3. The CSV is written in append mode using open(filename, 'a', newline=''). The header row is written only once — when the file does not yet exist. This is checked with os.path.exists() before every write.

4. The failure_reason field is the key to debugging. If it is empty, the call succeeded. If it is not empty, the string it contains tells you exactly what went wrong: "rate_limit_exceeded", "timeout", "empty_prompt", "empty_response", or the raw exception message.

5. quality_score is a manual metric. Today it was hardcoded because we are running test cases we already know the answers to. In production, it would be assigned by a human reviewer, a secondary LLM judge, or an automated scoring function comparing the response to a reference answer.

6. print_report() reads the CSV — it does not keep any state in memory. This means it always reflects the current state of the log file, even if you run it multiple times between script executions.

7. eval_summary.json is a snapshot. It reflects the state of the CSV at the moment generate_summary() was called. If you add more logs and do not call generate_summary() again, the JSON will be stale.

8. Langfuse and LangSmith are professional tools that implement this same logging pattern at scale, with dashboards, tracing, and automated evaluation. Building it manually first means you understand what those tools are doing under the hood, which makes you a better user of them.

9. The Gemini 1.5 Flash model is specified as a string constant at the top of the module, not hardcoded inside the function. This makes it easy to change the model in one place and have the change propagate everywhere.

10. Exception handling must be specific. Catching bare Exception catches everything but tells you nothing. Catching google.api_core.exceptions.ResourceExhausted tells you specifically that the rate limit was hit, which is actionable information that can trigger a retry with backoff.

---

# Interview-Ready Explanation

Read this, internalize it, and practice saying it out loud. Aim for a smooth delivery under 90 seconds.

```text
In Session 2 of my AI engineering portfolio, I built llm_logger.py — a Python wrapper module that adds an observability layer around Gemini 1.5 Flash API calls. Every time the LLM is called through this wrapper, it records seven fields: the prompt text, the response text, latency in milliseconds measured with time.time(), an estimated token count calculated as word count times 1.3, an estimated cost in USD based on Gemini's per-token pricing, a manual quality score from 1 to 5, and a failure reason if the call failed. All records are written to a CSV log file using Python's built-in csv module, and an aggregated summary is written to a JSON file. I ran seven test cases covering successful calls, edge cases like empty prompts, and calls expected to produce low-quality responses. The print_report() function reads the CSV back and prints total calls, pass/fail counts, average latency, and average quality score. This module teaches that production AI systems need observability — logging every call, costing every call, and scoring every output — because you cannot improve what you cannot measure.
```

---

# What Happens When log_llm_call() is Called

Trace this execution path in your head. This is what happens under the hood for a normal successful call.

```text
Caller invokes: log_llm_call("Extract skills from: Python, SQL, cloud", quality_score=4)

Step 1: Guard clause — checks if prompt.strip() == ""
        → prompt is not empty, continue

Step 2: start_time = time.time()
        → records current timestamp in seconds (e.g., 1749123456.891)

Step 3: model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        → sends HTTP request to Gemini API
        → waits for response (typically 800ms to 2000ms)
        → response object contains response.text

Step 4: end_time = time.time()
        → records timestamp after response received (e.g., 1749123458.234)

Step 5: latency_ms = round((end_time - start_time) * 1000, 2)
        → (1749123458.234 - 1749123456.891) * 1000 = 1343.0 ms

Step 6: estimated_tokens = round(len("Extract skills from: Python, SQL, cloud".split()) * 1.3)
        → len = 7 words → 7 * 1.3 = 9.1 → round to 9 tokens

Step 7: estimated_cost_usd = round(9 * 0.000000075, 8)
        → 9 * 0.000000075 = 0.000000675 → stored as 6.75e-07

Step 8: Build the log row dictionary:
        {
          "prompt": "Extract skills from: Python, SQL, cloud",
          "response": "The key skills mentioned are Python, SQL, and cloud deployment.",
          "latency_ms": 1343.0,
          "estimated_tokens": 9,
          "estimated_cost_usd": 6.75e-07,
          "quality_score": 4,
          "failure_reason": ""
        }

Step 9: Check if llm_logs.csv exists
        → If not: open in write mode, write header row, close
        → If yes: open in append mode

Step 10: csv.DictWriter appends one row to llm_logs.csv

Step 11: Return response.text to caller
         → "The key skills mentioned are Python, SQL, and cloud deployment."
```

---

# What AI Was Used For + What Engineers Must Still Do

## What AI Was Used For

In Session 2, AI (Claude Code or Cursor) was used to generate the initial llm_logger.py code based on the detailed Prompt 1. The AI wrote the function signatures, the CSV writer logic, the token estimation formula, the exception handling structure, and the test cases. AI also helped explain the generated code when students ran Prompt 4, and helped add edge case handling when students ran Prompt 7. The AI accelerated the build from 2 hours of solo coding to approximately 15 minutes of guided generation and review.

## What Engineers Must Still Do

You must verify that the latency is measured correctly — that time.time() brackets only the API call and not the entire function. You must verify that the CSV header row is written exactly once, not on every call. You must confirm that the failure test case (empty prompt) actually produces a row in the CSV with failure_reason populated. You must inspect llm_logs.csv in a text editor to verify that the columns align correctly and that no rows are malformed. You must understand the token estimation formula well enough to explain its limitations in an interview. You must decide what quality_score to assign to each test case and justify that decision. AI generated the scaffolding — you are responsible for correctness, testing, and explanation.

---

# Common Issues and Fixes

## Issue 1: ModuleNotFoundError for google-generativeai

Error message seen in terminal:
```
ModuleNotFoundError: No module named 'google.generativeai'
```
This means google-generativeai is not installed in your current Python environment. Make sure you are in the same virtual environment you used for Session 1.

What to ask AI:
```text
I am getting ModuleNotFoundError: No module named 'google.generativeai' when running my script. I am using Python 3.11 in a virtual environment. Show me the exact commands to activate my environment, install google-generativeai, and verify the installation. Also confirm what the correct import statement is.
```

## Issue 2: CSV file has duplicate header rows or blank rows between entries

Error symptom: when you open llm_logs.csv, you see the header row repeated multiple times, or blank lines appear between data rows.

The duplicate header is caused by using open(filename, 'w') instead of checking os.path.exists() first — write mode truncates the file and rewrites the header on every call. The blank lines on Windows are caused by not passing newline='' to the open() call.

What to ask AI:
```text
My llm_logs.csv has duplicate header rows appearing every time I run the script. Also, on Windows, blank lines appear between each data row. Show me the correct way to open a CSV file for appending in Python that writes the header only once (checking os.path.exists first) and prevents blank lines on Windows using newline='' in the open() call.
```

## Issue 3: AttributeError when Gemini response is None

Error message seen in terminal:
```
AttributeError: 'NoneType' object has no attribute 'text'
```
This happens when the Gemini API returns None instead of a response object — typically when a safety filter blocks the content or the model cannot generate a response for the given input.

What to ask AI:
```text
My llm_logger.py is crashing with: AttributeError: 'NoneType' object has no attribute 'text'. This happens because response is None when Gemini's safety filter blocks the output. Fix the log_llm_call function to check if response is None before accessing response.text. If response is None, log failure_reason as "safety_filter_blocked" and quality_score as 0. Show only the changed section of the function.
```

---

# Limitations of This Module

Being able to articulate these limitations is a sign of engineering maturity. Know them before interviews.

1. Flat file CSV does not support concurrent writes. If two processes call log_llm_call() at the same time on the same CSV file, the file can become corrupted. This module is single-process only.

2. Token estimation is inaccurate for non-English text, code-heavy prompts, and prompts with mathematical notation. The 1.3 multiplier is calibrated for standard English prose.

3. Output tokens are not estimated or logged. Gemini bills for both input and output tokens. This module only estimates input cost, so the true cost per call is higher than the logged figure.

4. Quality score is manual. At scale, manually scoring every LLM response is impossible. This module does not implement automated evaluation.

5. The JSON summary is a point-in-time snapshot. It reflects the state of the CSV when generate_summary() was last called. It can be stale if new logs have been written since then.

6. No log rotation. The CSV file grows indefinitely. After thousands of calls, the file becomes large and print_report() becomes slow because it reads the entire file on every call.

7. No PII handling. If prompts contain personally identifiable information — names, email addresses, phone numbers — they are stored in plain text in the CSV file. This violates data privacy requirements in most production environments.

8. The except Exception as e fallback catches every possible error, including programming errors like NameError. In production, errors should be categorized precisely and routed to different handlers.

---

# Key Takeaways

1. Every LLM call in production must be logged. Latency, cost, quality, and failure reason are the minimum four dimensions to track. Without these, you have no visibility into whether your system is working, degrading, or costing too much.

2. The wrapper function pattern is the foundation of LLM observability. A wrapper adds measurement and logging around an API call without changing what the call does. This pattern scales from a simple Python script to enterprise observability platforms like Langfuse and LangSmith.

3. Flat files are a valid starting point, not a permanent solution. CSV and JSON files are readable, portable, and require no setup — they are correct for a portfolio module and for early-stage experimentation. At scale, they must be replaced with a database, but understanding the flat file layer makes the transition to a database-backed system easier.

4. Production readiness is a spectrum, and naming your gaps is as important as your solutions. Saying "this module does not handle concurrent writes or PII redaction, and those would need to be added before production deployment" demonstrates exactly the engineering judgment that differentiates a strong candidate from one who cannot think beyond their own code.

---

# Session 3 Preview

In Session 3, we build a Serverless-Style AI Function.

The idea: take the Gemini call and the logging wrapper from Sessions 1 and 2 and package them into a function-style interface — similar to how AWS Lambda or Google Cloud Functions work. The function accepts a structured input payload, calls Gemini internally, logs the call using log_llm_call(), and returns a structured output payload.

Deliverable: ai_handler.py + .env.example

Main concept: function-as-a-service thinking applied to AI — how to design a clean input/output interface for an AI capability so it can be called from any context, tested in isolation, and integrated into larger systems.

You will reuse log_llm_call() from today's llm_logger.py directly. Keep your Session 2 files in the portfolio folder — Session 3 imports from them.

Before Session 3, make sure:
- llm_logger.py runs without errors
- llm_logs.csv is generated correctly
- You can explain what log_llm_call() does in under 60 seconds
