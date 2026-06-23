# Session 2 Instructor File: LLM Logging and Evaluation Tracker

## Session Title

LLM Logging and Evaluation Tracker

## Duration

2 hours

## Portfolio Module

Module 2 of 8 — Wrapper Module

## Objective

By the end of Session 2, students will have built a logging and evaluation layer that wraps any Gemini LLM call. This module captures prompt text, response text, latency in milliseconds, estimated token count, estimated cost in USD, a manual quality score from 1 to 5, and a failure reason field. Students will run 5–8 hardcoded test cases through the structured output engine from Session 1, log all results to a CSV file and a JSON summary, and implement a print_report() function that shows pass/fail statistics at a glance.

## Deliverable

- llm_logger.py
- llm_logs.csv
- eval_summary.json

---

## Strict Scope Control

### Include

- llm_logger.py with a log_llm_call() wrapper function
- CSV logging using Python's built-in csv module (no pandas)
- JSON summary written with Python's built-in json module
- Latency measured using time.time() before and after the Gemini call
- Token estimate calculated as len(prompt.split()) * 1.3
- Cost estimate derived from token count using Gemini 1.5 Flash pricing approximation
- 5 to 8 hardcoded test cases covering success, partial success, and failure scenarios
- print_report() function that prints total calls, pass count, fail count, average latency, and average quality score
- Comments in the code explaining each logical section
- Brief mention of Langfuse and LangSmith as professional alternatives (verbal mention only, not implemented)

### Do Not Include

- Any dashboard, UI, or web interface
- Langfuse or LangSmith integration (mention only, never implement)
- CI/CD pipelines or deployment scripts
- Production monitoring infrastructure or alerting systems
- External evaluation frameworks like RAGAS or DeepEval
- Database storage — CSV and JSON flat files only
- Pandas, NumPy, or any data science libraries
- OpenAI library or any non-Gemini LLM calls
- FastAPI or Flask endpoints
- Complex statistical evaluation — keep metrics simple and printable

---

# Instructor Framing

## Opening Message

Show students the portfolio folder on screen. Point to structured_output_engine.py from Session 1. Say:

"Last session we built an engine that calls Gemini and gets structured JSON output. Today we are going to wrap that call with a logging layer. In production, every LLM call costs money, takes time, and can fail. If you cannot observe what happened, you cannot improve the system. Today's module gives you that observation layer."

Display the full portfolio module list on screen and highlight Module 1 as done and Module 2 as today's build. Show students that Module 3 will build on today's logger.

## Key Philosophy

Students in this cohort understand prompting and LLM outputs. What they often miss is the engineering layer that sits around the LLM call. Logging, cost tracking, latency measurement, and quality scoring are what separate a notebook experiment from a production-ready component. Session 2 teaches that engineering mindset.

Students should understand that they are not just building a script. They are building the observability infrastructure of a real AI system — one call at a time.

## Repeated Instructor Line

"You cannot improve what you cannot measure. Every LLM call in production must be logged, costed, and scored."

---

# Session Flow

## 0–10 min: Opening, Portfolio Recap, Show Existing Scripts

Open the student's portfolio folder in the terminal or file explorer. Show Session 1 deliverable: structured_output_engine.py and output_examples.json. Ask one student to describe what structured_output_engine.py does in two sentences. Reinforce the portfolio model — each session produces one new Python file or notebook that builds on what came before. Show the full module map on screen. Say: "By the end of Session 8, you will have 8 working Python modules. Each one solves a real AI engineering problem. Today we build the logging layer." Tell students: "Without today's module, you have no idea how fast your LLM calls are, how much they cost, or which prompts are failing."

## 10–20 min: Concept Explanation — What is LLMOps and Why Does It Matter

Ask the class: "If you deployed a chatbot and it started returning wrong answers, how would you know?" Take 2–3 answers. Introduce LLMOps as the practice of managing LLM-powered systems in production — including logging, monitoring, evaluation, cost control, and version tracking. Explain the four pillars relevant to this session: observability (can you see what happened?), cost tracking (how much did each call cost?), latency measurement (how fast is each call?), and quality scoring (is the output good?). Explain why these matter in real companies: engineers are accountable for model quality and infrastructure cost. Draw a simple diagram on the whiteboard: LLM Call → Wrapper → Log Entry → CSV File → Report. Mention that tools like Langfuse and LangSmith automate this at scale, but building it manually first teaches you what those tools are actually doing under the hood.

## 20–35 min: Build the Module Using Claude Code or Cursor

Ask students to open Claude Code or Cursor. Direct them to paste Prompt 1 from the student pre-session file. The prompt will generate llm_logger.py. While the AI generates the code, narrate what you expect to see: a log_llm_call() function, a token estimation formula, a cost calculation, a CSV writer, and a JSON summary writer. Once the code is generated, do a quick first-pass scan. Check that the file structure matches the deliverable: llm_logs.csv and eval_summary.json should be created on first run. Make sure time.time() is present for latency. Check that there are at least 5 test cases. If the AI generated pandas instead of csv module, direct students to use Prompt 2 immediately to fix the scope. Do not spend more than 15 minutes on generation — move to walkthrough.

## 35–50 min: Walk Through Generated Code — Explain Every Function

Open llm_logger.py in the editor. Walk through the code section by section. Start with imports: explain why time, csv, json, os are being imported and why google.generativeai is used (not openai). Explain the token estimation formula — len(prompt.split()) * 1.3 — and why 1.3 is a rough approximation for subword tokenization. Show the cost estimation: explain that Gemini 1.5 Flash charges per million tokens and the per-call cost is computed from the estimate. Walk through log_llm_call(): show how it wraps a Gemini call, measures time before and after, catches exceptions, and writes a row to the CSV. Walk through the test cases: explain why they cover both success and failure paths. Walk through print_report(): show how it reads the CSV back and computes aggregated statistics. Ask students: "What would happen if the CSV file does not exist yet when print_report() is called?" Take answers and show how to handle the FileNotFoundError.

## 50–65 min: Student Follow-Along Build

Students now run the main prompt themselves and generate their own llm_logger.py. Circulate and check four things on each screen: (1) the Gemini API key is set as GEMINI_API_KEY environment variable, (2) time.time() is present around the API call, (3) the CSV file is created after running the script, (4) eval_summary.json exists and contains valid JSON. Common issues at this stage: ModuleNotFoundError for google-generativeai (fix: pip install google-generativeai), KeyError when the GEMINI_API_KEY is not set (fix: instruct students to set the env var), and a blank CSV file because the test cases were not run (fix: ensure the if __name__ == "__main__" block calls all test cases). If a student's Gemini key hits rate limit, redirect them to Prompt 3 from the student file which handles the 429 retry logic.

## 65–80 min: Test with Sample Inputs, Inspect Output Files

Run the script live. Show the terminal output from print_report(). Open llm_logs.csv in a text editor or the terminal and show every column: prompt, response, latency_ms, estimated_tokens, estimated_cost_usd, quality_score, failure_reason. Walk through a specific row and verify the numbers make sense. Open eval_summary.json and validate the structure. Ask students: "What does a quality_score of 1 mean? What does 5 mean?" Explain that manual quality scoring is an interim step — in production, you replace it with an LLM-as-judge pattern or embedding similarity. Have students inspect their own output files and verify at least one row shows a failure_reason that is not empty. This confirms failure tracking is working.

## 80–95 min: Edge Cases, Error Handling, Failure Modes

Ask: "What could go wrong with this logger in production?" Take answers. Cover these five scenarios: (1) Gemini returns a 429 rate limit error — show the ResourceExhausted exception from google.generativeai and how to catch it, log it as a failure, and not crash the script. (2) The response is valid JSON syntactically but semantically wrong — show why quality_score must be filled manually when automated checks are ambiguous. (3) The CSV file is corrupted or has wrong number of columns — show how csv.DictWriter with fieldnames prevents this issue. (4) Network timeout — show how to set a timeout and catch the DeadlineExceeded exception. (5) prompt is an empty string — show how to add an early guard clause that logs a failure_reason of "empty_prompt" and skips the API call entirely. Direct students to run Prompt 7 from the student pre-session file to add edge case handling to their scripts.

## 95–105 min: Concept Pause — LLMOps, Observability, Monitoring, Evaluation Mindset, Production Readiness

Stop coding. Ask students to close their laptops halfway. Explain the five concepts in sequence. LLMOps: the practice of operating LLM systems reliably at scale — includes model versioning, prompt versioning, A/B testing, cost control, and quality regression detection. Observability: the ability to understand the internal state of a system from its external outputs — in LLM terms, this means logging every call so you can reconstruct what happened. Monitoring: real-time or near-real-time tracking of system health metrics — latency spikes, error rates, cost overruns, quality score drops. Evaluation mindset: treating LLM output quality as a measurable metric that must be tracked over time, not just inspected once at build time. Production readiness: the difference between a notebook experiment and a deployable module — today's logger is one concrete step toward production readiness. Ask one student to explain the difference between monitoring and evaluation without notes. Correct and reinforce the distinction.

## 105–115 min: Interview Discussion and Viva Practice

Use the interview questions section below. Start with Q1 and Q3 from the basic section. Then go to Q7 and Q9 for technical depth. End with Q13 for production thinking. Ask students to answer out loud — do not accept one-word answers. Require at least two complete sentences per answer. If a student says "I logged the calls," push back: "How exactly? What fields? Why those fields?" If a student says "I estimated tokens," push back: "What formula? Why 1.3? What does subword tokenization mean?" The goal is to make students fluent in technical explanation, not just able to run the code.

## 115–120 min: Wrap-Up, Show Deliverables, Preview Session 3

Show the three deliverables on screen: llm_logger.py, llm_logs.csv, eval_summary.json. Add them to the mental portfolio map. Say: "You now have two modules: a structured output engine and a logging wrapper. Session 3 will build a serverless-style AI function that uses both of these as its internal components." Ask students to save and commit their files before closing. Remind them that the after-session notes file has the full interview-ready explanation they should memorize before the next session.

---

# Instructor Notes

## What to Emphasize

Session 2 is the first time students encounter operational thinking rather than capability thinking. Most students understand how to make an LLM call. Very few understand why every call needs to be wrapped, logged, and measured. Emphasize that production AI systems fail silently without observability. Emphasize that cost tracking matters at scale — 10,000 calls per day at $0.0001 per call is $1 per day, which sounds small, but bad prompts or infinite loops can multiply that by 1000. Emphasize that the quality_score field, even if filled manually today, establishes the pattern for automated evaluation in later sessions. Emphasize that the CSV format is intentionally simple — it is readable by humans, inspectable in a text editor, and importable into any spreadsheet or analytics tool.

## Common Student Mistakes

1. Student imports pandas instead of the built-in csv module. This adds an unnecessary dependency and defeats the purpose of building a lightweight logging layer. Error example: ModuleNotFoundError: No module named 'pandas' on a machine where pandas is not installed. Fix: use import csv and csv.DictWriter exclusively.

2. Student measures latency incorrectly by placing time.time() outside the try block but inside a function that does other processing. This inflates the latency reading. Fix: both start_time = time.time() and end_time = time.time() must immediately bracket only the genai.GenerativeModel(...).generate_content(...) call.

3. Student uses response.text directly without checking whether the response is None or whether a safety filter blocked the response. Error example: AttributeError: 'NoneType' object has no attribute 'text'. Fix: wrap in try/except and check if response is not None before accessing .text.

4. Student sets quality_score as a hardcoded value of 5 for all rows because they do not understand manual scoring. Instructor must stop and explain that quality_score is meant to be assigned case-by-case based on whether the output is correct, complete, and well-formatted.

5. Student writes to the CSV using open(filename, 'w') on every call, which overwrites previous logs. Error: only the last row appears in the CSV. Fix: use open(filename, 'a', newline='') in append mode, and only write the header row if the file does not exist yet (check with os.path.exists()).

6. Student's Gemini API key is hardcoded as a string in the script. Instructor must intervene immediately: "Never hardcode API keys. Always use os.environ.get('GEMINI_API_KEY')." This is a security and professionalism issue.

7. Student catches all exceptions with a bare except: clause, which hides the actual error type. Fix: catch specific exceptions — google.api_core.exceptions.ResourceExhausted for rate limits, google.api_core.exceptions.DeadlineExceeded for timeouts, and a generic Exception as e fallback that logs str(e) as the failure_reason.

8. Student's print_report() function crashes with FileNotFoundError if llm_logs.csv does not exist yet. This happens when a student runs print_report() before running any test cases. Fix: add a guard — if not os.path.exists(LOG_FILE): print("No logs found."); return.

9. Student generates eval_summary.json with Python's json.dump() but forgets to set indent=2, producing a single-line JSON blob that is hard to inspect. Fix: always use json.dump(summary, f, indent=2).

10. Student confuses estimated_tokens with actual tokens billed. Emphasize that len(prompt.split()) * 1.3 is an approximation. The Gemini API does not return token counts on the free tier response object in all SDK versions. This estimate is for cost awareness, not billing accuracy.

## How to Control the Session

Use the strict scope rule: if a student asks to add a dashboard, a database, or Langfuse integration, the answer is "That is Session 7 territory. Today we do CSV and JSON only." If a student finishes early, direct them to Prompt 6 from the student file to generate 3–5 additional test cases. If the class is running behind at the 80-minute mark, skip the edge cases exercise and go directly to the concept pause. The interview preparation block (105–115 min) is non-negotiable — never skip it.

---

# Questions to Discuss: Interview Perspective

## Basic Module Questions

### Q1. What did you build in Session 2?

Expected answer: In Session 2, I built llm_logger.py — a Python module that wraps Gemini 1.5 Flash API calls with an observability layer. Every time the LLM is called, the wrapper records the prompt text, response text, latency in milliseconds, estimated token count, estimated cost in USD, a manual quality score from 1 to 5, and a failure reason if the call failed. All logs are written to llm_logs.csv using Python's built-in csv module, and an aggregated summary is written to eval_summary.json. A print_report() function reads the CSV and prints pass/fail statistics.

### Q2. What is LLMOps and why does it matter?

Expected answer: LLMOps stands for Large Language Model Operations. It is the practice of deploying, monitoring, evaluating, and maintaining LLM-powered systems in production. It matters because LLM calls are probabilistic — the same prompt can produce different outputs on different runs — and because they have real costs in time and money. Without LLMOps practices like logging, cost tracking, and quality evaluation, engineers have no visibility into whether their system is working correctly, degrading over time, or costing more than expected. LLMOps also covers prompt versioning and model upgrade management.

### Q3. Why do you log every LLM call?

Expected answer: Logging every LLM call gives you the raw data you need to debug failures, measure performance, track costs, and evaluate quality over time. If a user reports a bad answer, the log lets you replay exactly what prompt was sent and what response was received. If costs spike unexpectedly, the log lets you identify which prompts are generating large token counts. If quality scores drop, the log lets you correlate that drop with a prompt change or a model update. In production, logging is not optional — it is the minimum viable observability layer for any AI system.

### Q4. What fields does your logger track and why did you choose each one?

Expected answer: The logger tracks seven fields. Prompt text is stored so you can replay and debug any call. Response text is stored so you can evaluate output quality after the fact. Latency in milliseconds is measured with time.time() to track performance and identify slow calls. Estimated tokens is computed as len(prompt.split()) * 1.3 to give a cost-awareness signal without relying on API billing data. Estimated cost in USD is derived from the token estimate using Gemini 1.5 Flash per-token pricing. Quality score from 1 to 5 is a manual signal that captures human judgment about whether the response was correct and useful. Failure reason is a string field that records the exception type or error message when a call fails, enabling failure mode analysis.

### Q5. What is the difference between a quality score and a pass/fail flag?

Expected answer: A pass/fail flag is binary — the call either succeeded technically or it did not. A quality score from 1 to 5 captures degrees of correctness and usefulness that a binary flag cannot express. For example, a call might succeed technically — Gemini returns a 200 response — but the output might be incomplete, hallucinated, or off-topic. In that case, the pass/fail flag shows success but the quality score of 2 reveals that the output was poor. Quality scoring introduces the evaluation mindset that is central to LLMOps: measuring output quality as a first-class metric, not just tracking API errors.

## Technical Deep-Dive Questions

### Q6. How do you estimate token count and cost without the API meter?

Expected answer: Token count is estimated using the formula len(prompt.split()) * 1.3. The word count from split() gives the number of whitespace-separated tokens, and multiplying by 1.3 approximates the inflation caused by subword tokenization — where words like "tokenization" are split into multiple byte-pair encoding units. This is a rough estimate, typically accurate to within 20 to 30 percent for English text. Cost is then estimated by multiplying the token estimate by the per-token price of Gemini 1.5 Flash, which as of mid-2025 is approximately $0.075 per million input tokens. The result is a per-call cost estimate that is useful for budget awareness even though it is not billing-accurate.

### Q7. How does the CSV logging work technically? Walk me through the code.

Expected answer: The logging uses Python's built-in csv.DictWriter class. A list of fieldnames is defined at the top of the module matching the seven log fields. When log_llm_call() is called, it first checks whether llm_logs.csv exists using os.path.exists(). If the file does not exist, it opens the file in write mode, creates a DictWriter, and writes the header row. If the file already exists, it opens the file in append mode with newline='' to avoid blank line insertion on Windows, and writes only the data row without the header. This pattern ensures the CSV has exactly one header row regardless of how many times the script is run. Each row is a Python dictionary with keys matching the fieldnames, which DictWriter serializes to a comma-separated line.

### Q8. What happens when a Gemini API call fails inside your wrapper?

Expected answer: The log_llm_call() function uses a try/except block that catches specific exception types from the google.api_core.exceptions module. If a ResourceExhausted exception is raised — which is the 429 rate limit error — the failure_reason field is set to "rate_limit_exceeded" and response_text is set to an empty string. If a DeadlineExceeded exception is raised — a network timeout — the failure_reason is set to "timeout". For all other exceptions, the generic Exception as e handler catches the error and logs str(e) as the failure_reason. In all failure cases, latency_ms is still recorded — it captures how long the call ran before failing — and quality_score is set to 0 to indicate an unusable response. The function returns None for the response and logs the failure row to the CSV.

### Q9. How does print_report() work?

Expected answer: print_report() opens llm_logs.csv using csv.DictReader, which reads each row as a Python dictionary keyed by the header fieldnames. It iterates through all rows and accumulates: total call count, count of rows where failure_reason is empty (passes), count of rows where failure_reason is not empty (failures), total latency summed from the latency_ms column, and total quality score summed from the quality_score column. After iteration, it computes average latency and average quality score by dividing by total call count. It then prints a formatted report to stdout. The function also handles the edge case of an empty or missing CSV file by checking os.path.exists() before attempting to open the file and printing a "No logs found" message if the file does not exist.

### Q10. Why use flat files (CSV and JSON) instead of a database?

Expected answer: For a portfolio module and for early-stage LLM experimentation, flat files are the right choice for three reasons. First, they require no setup — no database server, no connection string, no schema migration. The script can be run on any machine with Python installed. Second, they are human-readable and inspectable with any text editor, which makes debugging faster. Third, they are portable — CSV files can be opened in Excel or Google Sheets for quick manual analysis, and JSON files can be parsed by any downstream script. The trade-off is that flat files do not scale — they cannot handle concurrent writes from multiple processes, they have no query capability, and they grow without bound. In a production system, you would replace flat files with a database like PostgreSQL or a dedicated observability backend like Langfuse, but understanding the flat file layer first makes those tools easier to adopt.

## Production and System Design Questions

### Q11. How would this logging system change if you needed to handle 10,000 LLM calls per day?

Expected answer: At 10,000 calls per day, three things would break in the current design. First, the flat file CSV would become large and slow to append to — you would replace it with a database such as PostgreSQL and use connection pooling for concurrent writes. Second, the synchronous logging approach — where every API call blocks until the log is written — would add latency to each call. You would move to asynchronous logging using a queue, where the LLM call completes immediately and a background worker writes the log entry. Third, the manual quality scoring approach becomes impractical — you cannot manually score 10,000 responses per day, so you would replace it with automated evaluation: an LLM-as-judge pattern or embedding similarity scoring against reference answers. The eval_summary.json file would also move to a real-time dashboard like Grafana or Langfuse.

### Q12. What would you monitor in production for a system using this logger?

Expected answer: I would monitor four categories of metrics in production. Latency: track p50, p95, and p99 response times — a spike in p95 latency indicates that some calls are degrading even if the median is stable. Error rate: track the percentage of calls where failure_reason is not empty, broken down by error type — rate limit errors suggest you need request throttling or a paid tier upgrade; timeout errors suggest network issues or model overload. Cost: track daily and monthly estimated cost using the per-call cost field — set alerts when daily cost exceeds a budget threshold. Quality score: track average quality score over rolling time windows — a declining average score may indicate prompt regression after a model update or a domain shift in incoming queries. All four metrics together give a complete operational picture of the system.

### Q13. What are the limitations of using len(prompt.split()) * 1.3 for token estimation?

Expected answer: This formula has three significant limitations. First, the 1.3 multiplier is calibrated for English text and overestimates tokens for short prompts while underestimating for prompts with many technical symbols, code snippets, or non-ASCII characters. Code prompts can have much higher tokenization ratios because operators, brackets, and indentation are often individual tokens. Second, the formula only estimates input tokens and ignores output tokens, which are billed separately. A complete cost estimate requires estimating both input and output tokens, but output token count is not known until after the call completes. Third, Gemini 1.5 Flash uses a specific tokenizer that does not exactly match the word-split-times-1.3 approximation — the actual token count for a given prompt could vary by 20 to 50 percent. For production billing accuracy, you should use the usage_metadata field returned in the Gemini response object if available, or use the count_tokens() method from the google.generativeai library.

### Q14. How would you integrate this logger with the RAG pipeline built in Session 4?

Expected answer: The RAG pipeline in Session 4 involves a retrieval step and a generation step. Each of these should be logged separately. For the retrieval step, you would log the query text, the number of documents retrieved, and the retrieval latency. For the generation step, you would use the existing log_llm_call() wrapper — passing the augmented prompt that includes retrieved context — and log the full prompt, response, latency, token estimate, cost estimate, and quality score. The combined log gives you end-to-end observability over the RAG pipeline: you can see whether retrieval is returning relevant documents (quality score), how much the context expansion inflates the prompt token count (estimated cost), and whether the generation step is the bottleneck (latency). In Session 5, when you build the RAG evaluator, the llm_logs.csv from Session 2 becomes the data source for evaluation metrics.

### Q15. What would you change about this logger before deploying it to a real company project?

Expected answer: I would make five changes before production deployment. First, replace the flat CSV file with a structured database — PostgreSQL for relational queries or a time-series database for metric aggregation. Second, add request ID and session ID fields to every log row so that logs can be joined across a multi-turn conversation or a multi-step pipeline. Third, replace manual quality_score with an automated evaluation function — an LLM-as-judge call that scores each response against a rubric, or embedding cosine similarity against a reference answer. Fourth, add PII redaction before logging prompt text — prompts may contain user names, email addresses, or other sensitive data that should not be stored in plain text. Fifth, move the logging call to an asynchronous background task so that the logging overhead does not block the main application response path. These five changes would transform the Session 2 module from a learning tool into a production-grade observability component.

---

# Session 2 Completion Checklist

Students should be able to confirm all of the following by the end of the session:

- [ ] llm_logger.py runs without error from the command line using python llm_logger.py
- [ ] llm_logs.csv is created in the same directory as the script after the first run
- [ ] llm_logs.csv contains a header row with correct column names: prompt, response, latency_ms, estimated_tokens, estimated_cost_usd, quality_score, failure_reason
- [ ] llm_logs.csv contains at least 5 data rows from the hardcoded test cases
- [ ] At least one row in llm_logs.csv has a non-empty failure_reason, demonstrating that failure logging works
- [ ] eval_summary.json is created and contains valid, parseable JSON with total_calls, pass_count, fail_count, avg_latency_ms, and avg_quality_score fields
- [ ] print_report() outputs a readable summary to the terminal matching the values in eval_summary.json
- [ ] Latency is measured using time.time() directly bracketing the Gemini API call (not the whole function)
- [ ] Token estimation uses the formula len(prompt.split()) * 1.3 and is visible in the code
- [ ] The Gemini API key is loaded from environment variable GEMINI_API_KEY using os.environ.get(), not hardcoded
- [ ] Gemini 429 rate limit error is caught and logged as a failure row rather than crashing the script
- [ ] Student can verbally explain what each field in llm_logs.csv represents and why it is there

---

# Instructor Backup Plan

## If Gemini Rate Limit is Hit During Class

The free tier of Gemini 1.5 Flash allows 15 requests per minute. If the class runs multiple test cases in rapid succession and hits the 429 ResourceExhausted error, do the following. First, use this as a teaching moment — show students what the ResourceExhausted exception looks like and explain that this is exactly why rate limit handling must be in the logger. Second, add a time.sleep(5) between each test case call in the main block. Third, stagger the class so not all students run their scripts at the same time — ask half the class to run first, then the other half. Fourth, if a student's personal API key is exhausted, ask them to work with the instructor's live screen and run their version after class.

## If a Student's Environment Setup Fails

If a student cannot get google-generativeai installed or cannot set the GEMINI_API_KEY environment variable, do not stop the class. Direct them to follow the instructor's screen for the walkthrough and concept sections. Have them copy the generated llm_logger.py to their machine after class. Provide the sample llm_logs.csv and eval_summary.json output files so they can study the expected output format even if their script did not run. Ensure they participate fully in the interview question discussion — the concepts apply regardless of whether their code ran.

## If AI Code Generation Produces an Out-of-Scope Output

If Claude Code or Cursor generates a script that uses pandas, Flask, or any out-of-scope library, have students run Prompt 2 (the improvement prompt) immediately to constrain the output. If the generated code uses OpenAI instead of google-generativeai, have students run a targeted correction prompt: "Rewrite this using google-generativeai library and gemini-1.5-flash model. Remove all references to openai." Do not try to manually patch a fundamentally wrong output — regenerate.

---

# Instructor Concept Reference: Five Core Concepts for Session 2

Use this section to prepare your explanations. Do not read from this verbatim — internalize the ideas and teach them in your own words.

## Concept 1: LLMOps

LLMOps (Large Language Model Operations) is the engineering discipline that manages LLM-powered systems from development through production. It is a specialization of MLOps adapted for the unique challenges of language models. The key practices include:

Prompt versioning: tracking changes to prompts the way you track changes to code. A prompt is part of your system's behavior, and changing it changes the output. Version control for prompts prevents regressions.

Model versioning: knowing exactly which version of Gemini or any other model is running in production, and having a process to test and approve model upgrades before they affect users.

Cost management: tracking token usage and billing per call, per user, or per feature. LLMs are billed on consumption, so engineering decisions about prompt length and call frequency have direct financial consequences.

Quality regression detection: automatically or manually detecting when output quality drops after a model upgrade, a prompt change, or a shift in the distribution of incoming queries.

Failure mode tracking: categorizing and counting different types of failures (rate limits, timeouts, safety filters, empty responses) to understand system reliability and prioritize fixes.

Session 2 introduces students to the logging foundation on which all of these practices depend. You cannot do any LLMOps without first logging the calls.

## Concept 2: Observability

Observability is a systems engineering concept borrowed from control theory. A system is observable if you can infer its internal state from its external outputs. For LLM systems, full observability means: given any call that ever happened, you can reconstruct what prompt was sent, what response was returned, how long it took, how much it cost, whether it succeeded, and whether the output was any good.

The three pillars of observability in software engineering are logs, metrics, and traces. Session 2 implements logs (llm_logs.csv) and metrics (eval_summary.json). Traces — which track a request across multiple system components — are introduced later when students build multi-step pipelines.

Observability is different from monitoring. Observability is the property of a system that makes monitoring possible. You must build observability into a system (by adding logging, instrumentation, and tracing) before you can monitor it.

## Concept 3: Monitoring

Monitoring is the practice of continuously watching a live system and alerting when something is wrong. For LLM systems, the key metrics to monitor are:

Availability: what percentage of calls succeed. A drop in availability means users are experiencing errors.

Latency: how long calls take at p50, p90, and p99. p99 latency tells you what the worst 1 percent of users are experiencing.

Error rate: what percentage of calls fail, and what type of error they fail with. Rate limit errors require different interventions than timeout errors.

Cost rate: how much money the system is spending per hour or per day. A sudden cost spike usually means a runaway loop or a malformed prompt that is generating very long responses.

Quality score trend: if you have automated quality evaluation, track average quality score over rolling time windows. A declining trend may indicate prompt regression or model drift.

Session 2's print_report() function is the simplest possible monitoring report. It gives a point-in-time snapshot of all five dimensions. Real production monitoring would run this report continuously on a rolling window and surface alerts.

## Concept 4: Evaluation Mindset

The evaluation mindset is the practice of treating LLM output quality as a measurable, trackable metric — not a one-time visual check. Most beginners evaluate an LLM by running a few test prompts, reading the output, and deciding it looks good. The evaluation mindset says: define what good means, measure it consistently across every output, track it over time, and use it to make engineering decisions.

In Session 2, the quality_score field is the first implementation of the evaluation mindset. Even though the scores are assigned manually by the instructor in the test cases, the structure is in place. Later sessions will replace manual scoring with automated evaluation using embedding similarity, LLM-as-judge, and RAGAS-style metrics.

Key questions that drive the evaluation mindset:
- What does a score of 5 mean for this specific use case?
- What threshold of average quality score is acceptable for production?
- How quickly does quality degrade when the underlying model changes?
- How do I compare two prompt variants objectively?

Session 5 (RAG Evaluation) is where the evaluation mindset becomes fully quantitative.

## Concept 5: Production Readiness

Production readiness means that a component can be deployed in a live system and will behave reliably under real conditions. For a Python script that wraps an LLM call, production readiness requires:

Error handling: every exception that can occur in the call must be caught, logged, and handled gracefully. The script must never crash in production.

Observability: every call must be logged with enough information to diagnose any failure after the fact.

Security: no secrets, API keys, or credentials are stored in the code. All sensitive configuration is loaded from environment variables or secret management systems.

Idempotency: running the script multiple times should not corrupt the output. The CSV append pattern in Session 2 is idempotent at the call level.

Graceful degradation: if the LLM API is unavailable, the caller receives a clear failure signal rather than an unhandled exception that propagates up the stack.

Session 2's llm_logger.py achieves three of these five properties: error handling, observability, and security (via os.environ.get). It does not yet achieve full idempotency (no deduplication of calls) or graceful degradation in all edge cases. Naming these gaps is a sign of engineering maturity.

---

# Annotated Code Reference: What Each Function Must Contain

Use this section to verify student-generated code is correct. Check each function against this reference.

## log_llm_call() — Required Elements

The function signature must be:
def log_llm_call(prompt: str, quality_score: int = 3, model_name: str = "gemini-1.5-flash") -> str

Inside the function, these elements must be present in this order:

Guard clause for empty prompt: check if prompt.strip() == "" before making any API call. If true, set failure_reason = "empty_prompt", write the log row with latency_ms=0, return empty string.

Start time capture: start_time = time.time() must appear immediately before the API call, not earlier in the function body.

Gemini call: model = genai.GenerativeModel(model_name) followed by response = model.generate_content(prompt). The model name must come from the parameter, not be hardcoded.

End time capture: end_time = time.time() must appear immediately after the API call returns successfully.

Latency computation: latency_ms = round((end_time - start_time) * 1000, 2)

Token estimation: estimated_tokens = round(len(prompt.split()) * 1.3)

Cost estimation: estimated_cost_usd = round(estimated_tokens * 0.000000075, 8). The cost constant 0.000000075 represents $0.075 per million tokens ($0.075 / 1,000,000 = 7.5e-8).

Response extraction: response_text = response.text after confirming response is not None.

Exception handling: wrap the API call section in try/except. Catch google.api_core.exceptions.ResourceExhausted first, then google.api_core.exceptions.DeadlineExceeded, then Exception as e as fallback. In each except block, set appropriate failure_reason, set quality_score = 0, set response_text = "".

CSV write: check os.path.exists(LOG_FILE) to decide whether to write the header. Use open(LOG_FILE, 'a', newline='') for appending. Use csv.DictWriter with fieldnames=FIELDNAMES and write a dict row.

Return value: return response_text.

## generate_summary() — Required Elements

Read the entire CSV using csv.DictReader inside a with open(LOG_FILE, 'r') block. Initialize counters to 0. Iterate rows and accumulate: total_calls, pass_count (failure_reason == ""), fail_count (failure_reason != ""), sum_latency, sum_quality. After the loop, compute averages. Handle the edge case of total_calls == 0 to avoid ZeroDivisionError. Build a summary dictionary. Write to SUMMARY_FILE using json.dump(summary, f, indent=2). Print confirmation.

## print_report() — Required Elements

Check os.path.exists(LOG_FILE) before attempting to open. If the file does not exist, print "No logs found. Run test cases first." and return. Otherwise, read the CSV and compute the same metrics as generate_summary(). Print a formatted report with clear labels. Minimum output must include: total calls, passes, failures, average latency in ms, average quality score.

---

# Portfolio Connection Reference

Use this to explain to students how Session 2 connects to the rest of the portfolio.

Session 1 → Session 2: Session 1 established the Gemini call pattern using google-generativeai. Session 2 wraps that call with observability. The structured_output_engine.py call is the internal mechanism that log_llm_call() monitors.

Session 2 → Session 3: Session 3 builds a serverless-style AI function. That function will import log_llm_call from llm_logger.py and call it internally. Session 2's module becomes a reusable component dependency.

Session 2 → Session 4: The RAG pipeline in Session 4 generates multiple LLM calls per user query. Each generation call should be logged through the Session 2 wrapper to enable cost and latency tracking on the full pipeline.

Session 2 → Session 5: Session 5 builds an evaluation layer for the RAG pipeline. The evaluation patterns introduced in Session 2 (quality_score, pass/fail, aggregated metrics) are the conceptual foundation for the more sophisticated evaluation methods in Session 5.

Session 2 → Session 7: The LangGraph agent in Session 7 involves multi-step LLM calls. The logging pattern from Session 2 can be applied at the node level to give per-step observability into the agent's behavior.

Session 2 → Session 8: The portfolio integration in Session 8 will use eval_summary.json from Session 2 as one of the output artifacts that portfolio_runner.py aggregates and displays.

---

# Viva Quick-Fire Round

Use these 10 quick-fire questions at the 110-minute mark. Ask each question and expect a one-sentence answer. If the student cannot answer in one sentence, they need to study more.

1. What Python module is used for CSV writing in llm_logger.py? (Expected: csv.DictWriter from the built-in csv module)

2. What does time.time() return? (Expected: the current time as a float in seconds since the Unix epoch)

3. Why multiply by 1.3 in the token estimate? (Expected: to approximate subword tokenization inflation where one word can become more than one token)

4. What does failure_reason contain when a call succeeds? (Expected: an empty string)

5. What is the Gemini 1.5 Flash model name string as used in the code? (Expected: "gemini-1.5-flash")

6. What does print_report() do if llm_logs.csv does not exist? (Expected: prints a message saying no logs found and returns without crashing)

7. Name one professional tool that does what llm_logger.py does at production scale. (Expected: Langfuse or LangSmith)

8. What quality_score value indicates a failed call in the logger? (Expected: 0)

9. What is the difference between generate_summary() and print_report()? (Expected: generate_summary writes to a JSON file, print_report prints to the terminal)

10. What exception class represents a Gemini 429 rate limit error? (Expected: google.api_core.exceptions.ResourceExhausted)
