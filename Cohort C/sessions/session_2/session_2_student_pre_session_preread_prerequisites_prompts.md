# Session 2 Student Pre-Session File: LLM Logging and Evaluation Tracker

## What We Are Building

In this 8-session portfolio program, we are not building one big project. We are building a portfolio of 8 standalone AI engineering modules. Each module is a real Python script or notebook that solves a specific AI engineering problem.

Here is the full portfolio:

1. Session 1 — Structured Output Prompt Engine → structured_output_engine.py + output_examples.json
2. Session 2 — LLM Logging and Evaluation Tracker → llm_logger.py + llm_logs.csv + eval_summary.json (TODAY)
3. Session 3 — Serverless-Style AI Function → ai_handler.py + .env.example
4. Session 4 — Basic RAG Pipeline → rag_pipeline.py + chroma_db/
5. Session 5 — RAG Evaluation and Improvement → rag_evaluator.py + rag_eval_report.csv
6. Session 6 — Simple Agent Router → agent_router.py
7. Session 7 — Vision/OCR Mini Module → vision_ocr_module.py + ocr_output.json
8. Session 8 — Final System Design and Interview Demo

Sessions 4 and 5 are directly connected: Session 4 builds the RAG pipeline and Session 5 evaluates it. Session 2's logger is used as a reusable component in Session 3 onwards.

## Session 2 Goal

Build a logging and evaluation wrapper for Gemini LLM calls. Every call to the Gemini API should be tracked so you can measure performance, cost, and quality over time.

## Session 2 Deliverable

- llm_logger.py — the main Python script
- llm_logs.csv — a log file created when the script runs
- eval_summary.json — an aggregated summary created when the script runs

---

# Pre-Read

## Why Does This Module Exist in the Portfolio?

Session 1 taught you how to make a structured Gemini call and get JSON output. That is a capability. Session 2 teaches you how to operate that capability responsibly. In a real company, every LLM call runs in production and costs money. If something goes wrong — wrong output, slow response, unexpected cost spike, silent failure — you need to know about it immediately. That requires logging.

This module exists because most students who learn prompt engineering and LLM APIs skip the engineering layer that surrounds the API call. The logging wrapper is that layer. Without it, your AI system is a black box in production. With it, you have full observability over every call.

## Portfolio Module Map

The diagram below shows how all 8 modules connect. Modules that feed into other modules are marked with arrows.

```
Session 1: Structured Output Prompt Engine
    structured_output_engine.py + output_examples.json
    |
    v
Session 2: LLM Logging and Evaluation Tracker  <-- TODAY
    llm_logger.py + llm_logs.csv + eval_summary.json
    |
    v
Session 3: Serverless-Style AI Function
    ai_handler.py + .env.example
    |
    v
Session 4: Basic RAG Pipeline ------------> Session 5: RAG Evaluation and Improvement
    rag_pipeline.py + chroma_db/               rag_evaluator.py + rag_eval_report.csv
    |
    v
Session 6: Simple Agent Router
    agent_router.py
    |
    v
Session 7: Vision/OCR Mini Module
    vision_ocr_module.py + ocr_output.json
    |
    v
Session 8: Final System Design and Interview Demo
```

## Key Concepts to Revise Before This Session

Read or review these concepts before coming to Session 2. You do not need to be an expert — just refresh your understanding.

1. Python try/except blocks — how to catch specific exception types and handle errors without crashing the script. Know the difference between catching Exception, catching a specific error like ValueError, and using finally.

2. Python's csv module — specifically csv.DictWriter and csv.DictReader. Understand how DictWriter writes rows using dictionary keys as column names, and how DictReader reads a CSV back as a list of dictionaries.

3. Python's json module — specifically json.dump() and json.load(). Know how to write a Python dictionary to a JSON file with proper indentation using indent=2.

4. Python's time module — specifically time.time(). Understand that time.time() returns the current time in seconds as a float, and that subtracting two time.time() values and multiplying by 1000 gives milliseconds.

5. Environment variables in Python — how to read an environment variable using os.environ.get('VARIABLE_NAME'). Know why API keys must never be hardcoded in Python scripts.

6. Gemini 1.5 Flash API basics — from Session 1, you already know how to call google.generativeai.GenerativeModel and use generate_content(). Review how the response object is structured and how to access response.text.

7. What is a token in the context of LLMs — the basic idea that LLMs process text as subword units called tokens, that English words are typically 1 to 2 tokens each, and that API pricing is charged per million tokens.

8. What is LLMOps — the practice of managing LLM systems in production. Read a one-paragraph summary online if this term is new to you. Key ideas: logging, monitoring, cost control, quality evaluation, prompt versioning.

## Technical Explanation of the Core Concept

The core pattern in Session 2 is the wrapper function. A wrapper function calls another function (in this case, the Gemini API call), adds logic around that call (logging, timing, error handling), and returns the result without changing what the caller receives.

Here is the pattern in plain terms:

Before calling Gemini: record the start time using time.time(). Store the prompt text.

Call Gemini: use google.generativeai to send the prompt and receive a response.

After receiving the response: record the end time. Compute latency as (end_time - start_time) * 1000. Extract response.text. Estimate tokens as len(prompt.split()) * 1.3. Estimate cost from the token count.

On failure: catch the exception. Set response text to empty string. Set failure_reason to the exception type. Set quality_score to 0.

Write to CSV: append one row to llm_logs.csv with all seven fields.

Write to JSON: compute summary statistics across all rows and write to eval_summary.json.

This pattern is the foundation of every production LLM observability layer. Tools like Langfuse and LangSmith implement this same pattern with more features, but they are doing exactly what you are building manually today.

---

# Setup Before Class

## Required pip Installs

Run these commands in your terminal before the session. Make sure you are in the same virtual environment you used for Session 1.

```
pip install google-generativeai
```

The following packages are part of Python's standard library and do not need to be installed:

```
csv, json, time, os
```

Do not install pandas, langfuse, langsmith, openai, or any other library for this session.

## Gemini API Key Setup

If you completed Session 1, your GEMINI_API_KEY should already be set. Confirm it is working.

Get a free API key from: https://aistudio.google.com

Set the environment variable before running your script. On Mac or Linux:

```
export GEMINI_API_KEY="your_key_here"
```

On Windows Command Prompt:

```
set GEMINI_API_KEY=your_key_here
```

On Windows PowerShell:

```
$env:GEMINI_API_KEY="your_key_here"
```

Never paste your API key directly into your Python script.

## Verify Your Setup

Run this one-time test to confirm that google-generativeai is installed and your key works before the session:

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say hello in one word.")
print(response.text)
```

If this prints a single word, your setup is working. If you see an authentication error, double-check that GEMINI_API_KEY is set in your current terminal session.

---

# Sample Data / Content to Prepare

Prepare the following test prompts before class. These are the inputs you will run through the logger. Have them saved in a text file so you can reference them during the session.

Test case 1 — well-formed prompt expected to succeed:
"Extract the key skills from this job description: We are hiring a Python developer with experience in REST APIs, SQL databases, and cloud deployment."

Test case 2 — well-formed prompt expected to succeed:
"Summarize this text in one sentence: Artificial intelligence is transforming healthcare by enabling faster diagnosis, personalized treatment plans, and predictive patient monitoring."

Test case 3 — ambiguous prompt expected to return a low-quality response:
"Tell me about things."

Test case 4 — structured output prompt expected to succeed:
"Return a JSON object with fields: topic, difficulty, and recommended_reading for the concept of gradient descent."

Test case 5 — edge case: empty prompt (your script should catch this before calling Gemini):
""

Test case 6 — long prompt to observe token count increase:
"You are an expert in machine learning. Explain the following concepts in detail: overfitting, underfitting, regularization, cross-validation, bias-variance tradeoff, dropout, batch normalization, learning rate scheduling, early stopping, and ensemble methods."

Test case 7 — prompt that may trigger a quality score debate:
"What is the capital of France? Also explain quantum entanglement in detail."

---

# Prompts for Session 2

Use these prompts during the session when instructed by the instructor. Copy and paste each prompt exactly as written into Claude Code or Cursor.

## Prompt 1: Main Build Prompt

```text
I am building an AI engineering portfolio. I have already built Session 1: a structured output engine in structured_output_engine.py that calls Gemini 1.5 Flash using google-generativeai and returns JSON responses.

Now build Session 2: LLM Logging and Evaluation Tracker.

Create a Python file called llm_logger.py. This file must:

1. Import only these libraries: google.generativeai, os, csv, json, time. Do NOT use pandas, openai, langfuse, langsmith, Flask, or FastAPI.

2. Load the Gemini API key using: api_key = os.environ.get("GEMINI_API_KEY")

3. Configure google.generativeai using genai.configure(api_key=api_key)

4. Define a constant LOG_FILE = "llm_logs.csv"

5. Define a constant SUMMARY_FILE = "eval_summary.json"

6. Define a constant FIELDNAMES as a list: ["prompt", "response", "latency_ms", "estimated_tokens", "estimated_cost_usd", "quality_score", "failure_reason"]

7. Define a function called log_llm_call(prompt: str, quality_score: int = 3, model_name: str = "gemini-1.5-flash") that:
   - Records start_time = time.time() before the API call
   - Calls genai.GenerativeModel(model_name).generate_content(prompt)
   - Records end_time = time.time() after the API call
   - Computes latency_ms = round((end_time - start_time) * 1000, 2)
   - Computes estimated_tokens = round(len(prompt.split()) * 1.3)
   - Computes estimated_cost_usd = round(estimated_tokens * 0.000000075, 8) based on Gemini 1.5 Flash pricing of $0.075 per million tokens
   - Extracts response_text from response.text
   - On any exception, sets response_text = "", failure_reason = str(e), quality_score = 0
   - Appends one row to LOG_FILE as a CSV using csv.DictWriter
   - If LOG_FILE does not exist, writes the header row first
   - Returns the response_text string

8. Define a function called generate_summary() that:
   - Reads all rows from LOG_FILE using csv.DictReader
   - Computes: total_calls, pass_count (failure_reason is empty), fail_count, avg_latency_ms, avg_quality_score
   - Writes these five fields to SUMMARY_FILE as a JSON object with indent=2
   - Prints "Summary written to eval_summary.json"

9. Define a function called print_report() that:
   - Reads LOG_FILE using csv.DictReader
   - Prints total calls, pass count, fail count, average latency in ms, and average quality score
   - If LOG_FILE does not exist, prints "No logs found. Run test cases first."

10. In the if __name__ == "__main__" block, run exactly these 7 test cases through log_llm_call(). Use the quality_score values specified below. Add a comment before each test case explaining what it tests:
    - Test 1: "Extract key skills from: Python developer, REST APIs, SQL, cloud deployment." quality_score=4
    - Test 2: "Summarize in one sentence: AI is transforming healthcare with faster diagnosis and predictive monitoring." quality_score=5
    - Test 3: "Tell me about things." quality_score=1
    - Test 4: "Return JSON with fields topic, difficulty, recommended_reading for: gradient descent." quality_score=4
    - Test 5: "" (empty string — add a guard clause at the start of log_llm_call to skip the API call and log failure_reason="empty_prompt" if prompt is empty or whitespace)
    - Test 6: "Explain overfitting, underfitting, regularization, cross-validation, bias-variance tradeoff." quality_score=5
    - Test 7: "What is the capital of France? Also explain quantum entanglement." quality_score=3

11. After all test cases, call generate_summary() and then print_report()

12. Add a comment block at the top of the file explaining: what this module does, what files it creates, and how it connects to Session 1

13. Add inline comments throughout explaining each logical section

Do not add any web framework, database, dashboard, or external evaluation library. Keep this as a standalone Python script.
```

## Prompt 2: Improvement Prompt

```text
Improve the llm_logger.py script with the following changes. Do not change the core structure or add new dependencies.

1. Add better error handling: catch google.api_core.exceptions.ResourceExhausted separately and log failure_reason as "rate_limit_exceeded". Catch google.api_core.exceptions.DeadlineExceeded separately and log failure_reason as "timeout". Keep a generic Exception catch as a fallback.

2. In the log_llm_call function, add validation: if the response is not None but response.text is empty, set failure_reason to "empty_response" and quality_score to 1.

3. In print_report(), add the following to the output: the test case with the highest latency_ms and the test case with the lowest quality_score (non-zero). Print the prompt text truncated to 60 characters.

4. In generate_summary(), add two more fields to the JSON output: total_estimated_cost_usd (sum of all estimated_cost_usd values) and highest_latency_ms (max value from the latency column).

5. Add a function called get_failed_calls() that reads LOG_FILE and prints all rows where failure_reason is not empty, showing the prompt, failure_reason, and latency_ms.

Keep all other functionality the same. Do not add pandas, databases, or dashboards.
```

## Prompt 3: Debugging Prompt — Gemini Rate Limit 429 Error

```text
My llm_logger.py script is crashing with this error when running multiple test cases quickly:

google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted (e.g. check quota).

The script crashes and stops logging. I need it to:
1. Catch the ResourceExhausted exception without crashing
2. Log the failed call to llm_logs.csv with failure_reason = "rate_limit_exceeded" and quality_score = 0
3. Wait 5 seconds using time.sleep(5) and then continue to the next test case
4. Print a warning message showing which test case triggered the rate limit

Please fix only the log_llm_call function and the if __name__ == "__main__" block. Do not change any other part of the script.

Also confirm: where in the code should I import google.api_core.exceptions to catch ResourceExhausted? Show me the exact import statement.
```

## Prompt 4: Code Explanation Prompt

```text
Explain the llm_logger.py script technically, as if explaining it to a fellow AI engineer. Focus on:

1. What does the log_llm_call() function do step by step? Describe each line's purpose.
2. Why is time.time() used instead of datetime.datetime.now() for latency measurement?
3. What does len(prompt.split()) * 1.3 calculate and why 1.3 specifically?
4. How does csv.DictWriter work? What is the purpose of the fieldnames parameter?
5. Why does the CSV writer check os.path.exists(LOG_FILE) before deciding whether to write the header row?
6. What is the difference between what generate_summary() does and what print_report() does?
7. Why is the API key loaded from os.environ.get() instead of being hardcoded?
8. What would break if two processes tried to write to llm_logs.csv at the same time?

Do not rewrite the code. Only explain the design decisions and the technical reasoning behind each choice.
```

## Prompt 5: Interview Explanation Prompt

```text
Help me explain llm_logger.py to an interviewer at an AI engineering role. Structure the explanation as follows:

1. What problem does this module solve? (one sentence)
2. What does it do technically? (2-3 sentences describing the wrapper pattern, logging, and output files)
3. What design decisions did I make and why? (cover: csv module over pandas, flat files over database, time.time() for latency, estimated tokens formula)
4. What are the production trade-offs of this approach? (cover: what breaks at scale, what would need to change)
5. How does this module connect to the rest of the portfolio? (cover: used by Session 3, provides evaluation data for Session 5)
6. What tools do professional companies use for this? (mention Langfuse and LangSmith without claiming I built those)

Keep the explanation clear, technically honest, and under 2 minutes of speaking time. Do not make the module sound more complex than it is.
```

## Prompt 6: Test Case Generation Prompt

```text
Generate 5 additional test cases to run through log_llm_call() in llm_logger.py.

Requirements for each test case:
1. Provide the prompt text as a Python string
2. Provide a suggested quality_score from 1 to 5 based on how clear and answerable the prompt is
3. Explain in one sentence what this test case is testing (e.g., long prompt, multilingual input, structured output request, ambiguous prompt)

Cover these scenarios across the 5 test cases:
- A prompt that requests structured JSON output
- A very long prompt (over 100 words)
- A prompt in a non-English language
- A prompt with contradictory instructions
- A prompt that is technically valid but likely to produce a vague response

Format each test case as Python code ready to paste into the if __name__ == "__main__" block.
```

## Prompt 7: Edge Case and Failure Mode Prompt

```text
Add the following edge case handling to llm_logger.py. Show only the changes needed — do not rewrite the entire file.

Edge case 1: Empty or whitespace-only prompt
Add a guard clause at the start of log_llm_call() that checks if prompt.strip() == "". If true, log a row with response="", latency_ms=0, estimated_tokens=0, estimated_cost_usd=0, quality_score=0, failure_reason="empty_prompt". Return an empty string without calling the Gemini API.

Edge case 2: Response contains no text
After receiving the Gemini response, check if response is None or if response.text is None or if response.text.strip() == "". If any of these are true, set failure_reason = "empty_response" and quality_score = 1.

Edge case 3: CSV file is deleted between calls
Wrap the csv.DictWriter append logic in a try/except FileNotFoundError. If the file is missing, recreate it with the header row before appending.

Edge case 4: generate_summary() called when CSV is empty
After reading LOG_FILE with csv.DictReader, check if the rows list is empty. If it is, print "No data to summarize." and return without writing the JSON file.

Edge case 5: Non-integer quality_score passed by caller
At the start of log_llm_call(), validate that quality_score is an integer between 0 and 5. If not, set it to 3 (default) and print a warning.

Show each fix as a short code snippet with a comment explaining what it handles.
```

---

# What You Should Be Able to Explain After Session 2

By the end of this session, you should be able to answer these questions without looking at notes. Practice answering them out loud before the next session.

1. What is LLMOps and why does it matter for production AI systems?
2. What is observability in the context of LLM systems, and how does your logger provide it?
3. What are the seven fields logged per LLM call, and what is the purpose of each one?
4. How does the token estimation formula work and what are its limitations?
5. How does cost estimation work in the logger and how accurate is it?
6. What is the difference between monitoring and evaluation in the context of AI systems?
7. What happens inside log_llm_call() step by step when a call succeeds?
8. What happens inside log_llm_call() step by step when a call fails?
9. Why are flat files (CSV and JSON) used instead of a database in this module?
10. How would this logging system need to change to handle 10,000 calls per day in production?

---

## Final Session 2 Explanation

Memorize this and practice saying it out loud. This is your interview-ready answer for Session 2.

```text
In Session 2 of my AI engineering portfolio, I built llm_logger.py — a logging and evaluation wrapper for Gemini 1.5 Flash API calls. Every time the LLM is called, the wrapper records the prompt, response, latency in milliseconds, estimated token count, estimated cost in USD, a manual quality score, and a failure reason if the call failed. Results are saved to a CSV log file and an aggregated JSON summary. The module teaches the observability layer that every production LLM system needs — you cannot improve what you cannot measure.
```
