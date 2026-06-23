# Session 1 After-Session Notes: Structured Output Prompt Engine

## What We Built Today

Today we built the first module of the AI Systems Interview Portfolio.

Deliverables:

1. `structured_output_engine.py` — a Python script that takes 4 unstructured text inputs and converts each into a structured JSON object using Gemini 1.5 Flash. The script demonstrates free-text vs. structured output comparison, logs token counts, and handles API errors.

2. `output_examples.json` — a JSON file containing all processed outputs, each with the original input text, the structured JSON extracted by Gemini, a timestamp, and the model name used.

The inputs processed:

- A customer complaint about a delayed order
- A bug report about an app crashing on PDF export
- A feedback form response with product suggestions
- A product review about a defective wireless mouse

Each output contains:
- `category` (complaint / bug_report / feedback / review)
- `priority` (low / medium / high / critical)
- `sentiment` (positive / neutral / negative)
- `summary` (one-sentence summary)
- `key_issue` (the single most important problem mentioned)
- `action_required` (boolean)
- `confidence_score` (float 0.0–1.0)

---

# Why This Module Matters for AI Engineering Interviews

Structured output is not a niche topic. It is asked about in almost every AI engineering interview because it is the boundary between a demo and a production system.

Any AI system that needs to do something with the LLM's output — route a ticket, trigger an alert, populate a database, feed a pipeline — must have predictable output. Free-text responses look intelligent but are operationally unreliable. The moment a model slightly rephrases an answer, any downstream code that was parsing that text breaks silently.

When you show this module in an interview, you are demonstrating that you understand the engineering constraints of LLM output, not just the capabilities. You can explain:

- Why `response_mime_type` matters (constraint at the API level)
- Why temperature 0 matters (determinism for testability)
- Why the system prompt is a schema contract (not optional documentation)
- Why saving outputs matters (auditability and evaluation)

This kind of thinking — treating LLMs as components in a system, not magic boxes — is exactly what hiring managers for AI engineering roles are looking for.

---

# Portfolio Module Map

```
Session 1: Structured Output Prompt Engine              <- COMPLETED
           structured_output_engine.py + output_examples.json
                |
                v
Session 2: LLM Logging and Evaluation Tracker           (next session)
           llm_logger.py + eval_log.json
                |
                v
Session 3: Serverless-Style AI Function
           ai_handler.py + .env.example
                |
                v
Session 4: Basic RAG Pipeline                 <---------+
           rag_pipeline.py + chroma_db/                  |
                |                                        |
                v                                        |
Session 5: RAG Evaluation and Improvement     <----------+
           rag_evaluator.py + rag_eval_report.csv   (4 and 5 are connected)
                |
                v
Session 6: Simple Agent Router
           agent_router.py
                |
                v
Session 7: Vision/OCR Mini Module
           vision_ocr_module.py
                |
                v
Session 8: Final System Design and Interview Demo
```

Session 1 is standalone but foundational. The structured output pattern — system prompt as schema, `response_mime_type`, temperature 0 — appears in Sessions 4, 6, and 8.

---

# Technical Deep-Dive: Prompt Engineering + Structured Output + Token Awareness + Deterministic Design

## How the Structured Output Pattern Works

When you call `model.generate_content()` with `generation_config={"response_mime_type": "application/json", "temperature": 0}`, two things happen at the API level. First, `response_mime_type` applies a structural constraint: Gemini's decoding logic is instructed to produce only tokens that form a valid JSON string. This is not enforced at the prompt level alone — it is an API-level instruction that works in conjunction with the model. Second, `temperature: 0` removes stochastic sampling — the model uses greedy decoding, always selecting the highest-probability token at each step. The result is a response that is both structurally valid JSON and consistent across repeated calls for the same input.

The system prompt then defines what that JSON must contain. A well-designed system prompt for structured output specifies every field by name, gives the expected type or enumeration of values, and provides a brief description of what to extract. It also instructs the model not to add extra fields not in the schema and not to include any text outside the JSON object. The system prompt is a schema contract: it is as important as any API specification in a production system. Engineers who treat the system prompt as an afterthought produce systems that work in demos and break in production.

## Why Token Awareness Matters

LLMs are billed by tokens, not by characters, words, or API calls. A token is roughly 4 characters or 0.75 words in English. Every call to the Gemini API consists of two token counts: prompt tokens (the combined length of the system prompt plus the user input) and completion tokens (the length of the model's response). The total cost of a call is the sum of these two multiplied by the model's per-token rate.

In this module, the system prompt is approximately 200–300 tokens for every single call. That means if you process 10,000 tickets per day, the system prompt alone contributes 2–3 million tokens of input cost per day. This is why engineers write lean, precise system prompts. It is also why token logging is not optional — without it, you cannot forecast costs, detect prompt injection attacks that inflate token counts, or identify optimization opportunities. Gemini's `response.usage_metadata.prompt_token_count` and `response.usage_metadata.candidates_token_count` give you these numbers directly from every API response.

## Deterministic Output and Its Trade-offs

Setting temperature to 0 produces deterministic output: the same input will always produce the same output (assuming the same model version and system prompt). This is critical for structured extraction tasks because it makes the system testable and auditable. You can write a test that sends a known complaint and verifies the returned JSON exactly. You can reproduce any output by replaying the input.

The trade-off is that temperature 0 gives the model no flexibility when the input is ambiguous. If a customer complaint could reasonably be classified as either "complaint" or "feedback," the model will always pick the same one — but it will not express uncertainty unless your schema includes a `confidence_score` field. This is why the schema in Session 1 includes `confidence_score` as a float. It gives the model a mechanism to signal uncertainty within the structured output constraints, which a downstream system can use to route ambiguous cases to human review. This design choice — building uncertainty signaling into the schema — is an interview-worthy design decision.

---

# What Students Should Understand

1. `response_mime_type="application/json"` belongs inside the `generation_config` dictionary, not as a parameter on the model object. Putting it in the wrong place silently does nothing.

2. Temperature 0 is the correct setting for any structured extraction task. Higher temperatures introduce output variation that breaks pipeline assumptions and is impossible to debug reliably.

3. The system prompt is the schema definition. It is part of the codebase, not documentation. If you change the system prompt, you change the output schema — which may break downstream systems.

4. `json.loads(response.text)` converts the response string to a Python dict. `response.text["category"]` will fail with `TypeError: string indices must be integers` because `response.text` is a string, not a dict.

5. Always save LLM outputs to a persistent store. In Session 1, this is `output_examples.json`. In production, it would be a database with timestamps, model version, and latency. Saved outputs enable evaluation, debugging, and auditing.

6. Token logging is a professional habit. `response.usage_metadata.prompt_token_count` and `response.usage_metadata.candidates_token_count` are available on every Gemini API response. Always log them.

7. The free-text vs. structured output comparison in `compare_free_text_vs_structured()` is the most important demonstration in this module. It makes visible the engineering problem that structured output solves — and it is a compelling thing to show in an interview.

8. Retry logic for 429 errors is not optional in production. The free tier rate limit will be hit. The correct response is: catch the `ResourceExhausted` exception, wait with exponential backoff, and retry. Do not crash the whole pipeline because one call rate-limited.

9. Schema completeness matters. If the model returns valid JSON but omits a field, downstream code that accesses that field will raise a `KeyError`. Always validate that all expected keys are present and use `.get()` with safe defaults when accessing fields.

10. This pattern generalizes. The exact same structure — system prompt as schema, `response_mime_type`, temperature 0, token logging, output file — applies in Sessions 4, 6, and 8. Mastering Session 1 means the pattern recognition in later sessions is instant.

---

# Interview-Ready Explanation

```text
Session 1 of my AI Systems Interview Portfolio is a Structured Output Prompt Engine built with Python and Gemini 1.5 Flash. It takes unstructured customer text — complaints, support tickets, feedback forms, and product reviews — and converts each input into a clean, predictable JSON object with fields for category, priority, sentiment, summary, and action_required. I used response_mime_type="application/json" in the Gemini generation config to enforce valid JSON at the API level, and set temperature to 0 for deterministic, testable output. This demonstrates the foundational pattern for production AI pipelines: any downstream system that needs to process LLM output reliably must constrain the model to a fixed schema, and this is how you do it.
```

---

# What Happens When `process_input()` Is Called

```text
Input text is passed to process_input(text, model)
        |
        v
Input is checked: if empty or under 10 characters, return error dict immediately (no API call)
        |
        v
System prompt (JSON schema definition) is combined with the user input text
        |
        v
model.generate_content() is called with:
  - The combined prompt
  - generation_config: response_mime_type="application/json", temperature=0
        |
        v
Gemini 1.5 Flash processes the input and returns a response object
        |
        v
response.usage_metadata is read:
  - prompt_token_count is logged
  - candidates_token_count is logged
        |
        v
response.text (a JSON string) is passed to json.loads()
        |
   +----+----+
   |         |
Success    JSONDecodeError
   |         |
   v         v
Python    Error dict is returned:
dict is   {"error": "parse_failed", "raw": response.text}
returned
        |
        v
Caller receives the parsed dict (or error dict)
        |
        v
Result is added to the results list with "input_text" and "structured_output" keys
        |
        v
After all inputs are processed, results list is written to output_examples.json
```

---

# What AI Was Used For + What Engineers Must Still Do

## What AI (Claude Code / Cursor) Was Used For

- Generating the complete `structured_output_engine.py` script from the main build prompt
- Generating the system prompt with JSON schema definition
- Generating the 4 sample inputs
- Adding retry logic for 429 errors
- Adding error handling for missing keys and empty inputs
- Generating the `compare_free_text_vs_structured()` function
- Suggesting token logging patterns

## What Engineers Must Still Do

- Verify the script runs end to end without errors
- Confirm `response_mime_type` is placed in `generation_config`, not on the model object
- Confirm the API key is read from the environment, not hardcoded
- Confirm `output_examples.json` is valid JSON using `python -m json.tool output_examples.json`
- Confirm all 4 inputs appear in the output file, not just the last one
- Understand every function and be able to explain it without reading the code
- Test edge cases: empty input, missing API key, rate limit behavior
- Be able to explain the engineering trade-offs to an interviewer

AI generates. Engineers understand, verify, and own.

---

# Common Issues and Fixes

## Issue 1: `response_mime_type` Not Working — Model Returns Free Text Anyway

Symptom: `json.loads(response.text)` raises `json.JSONDecodeError` because `response.text` contains a sentence like "Here is the extracted information: ..."

Root cause: `response_mime_type` was placed on the model constructor instead of inside `generation_config`.

Wrong:
```python
model = genai.GenerativeModel("gemini-1.5-flash", response_mime_type="application/json")
```

Correct:
```python
generation_config = {"response_mime_type": "application/json", "temperature": 0}
model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)
```

What to ask AI:

```text
My structured_output_engine.py is returning free text instead of JSON even though I set response_mime_type.
Here is my model initialization code: [paste your code here]
The error is: json.JSONDecodeError when calling json.loads(response.text)
Please find the bug. The response_mime_type parameter must be inside generation_config as a dictionary,
not passed directly to GenerativeModel. Fix it and explain what was wrong.
```

## Issue 2: Only the Last Input Is Saved to `output_examples.json`

Symptom: `output_examples.json` contains only one entry instead of four.

Root cause: The `json.dump()` call is inside the loop and opens the file in `"w"` mode on every iteration, overwriting the previous result each time.

Wrong pattern:
```python
for text in SAMPLE_INPUTS:
    result = process_input(text, model)
    with open("output_examples.json", "w") as f:
        json.dump(result, f, indent=2)
```

Correct pattern:
```python
results = []
for text in SAMPLE_INPUTS:
    result = process_input(text, model)
    results.append(result)

with open("output_examples.json", "w") as f:
    json.dump(results, f, indent=2)
```

What to ask AI:

```text
My output_examples.json only contains the last processed input instead of all four.
Here is the relevant section of my script: [paste the loop and file-write code]
The issue is that json.dump is being called inside the loop in write mode.
Fix this so all results are collected in a list first and the file is written once after the loop.
```

## Issue 3: `KeyError: 'GEMINI_API_KEY'` When Running the Script

Symptom:
```
KeyError: 'GEMINI_API_KEY'
```

Root cause: The environment variable is not set in the current terminal session, or it was set in a different terminal tab.

Fix: Run the following in the same terminal tab where you will run the script:
```bash
export GEMINI_API_KEY="your_key_here"
echo $GEMINI_API_KEY
```

If you want it to persist across terminal sessions, add the export line to `~/.zshrc` (Mac/zsh) or `~/.bashrc` (Linux/bash) and then run `source ~/.zshrc`.

What to ask AI:

```text
My structured_output_engine.py raises KeyError: 'GEMINI_API_KEY' even though I set the variable.
Please add a check at the top of the script that:
1. Checks if GEMINI_API_KEY exists in os.environ before calling genai.configure()
2. If it is missing, prints a clear error message with instructions on how to get and set the key
3. Calls sys.exit(1) so the script exits cleanly instead of raising an unhandled KeyError
```

---

# Limitations of This Module

1. **Hardcoded inputs**: The 4 sample inputs are hardcoded in the script. In production, inputs would come from a message queue, database, or API endpoint. The script does not demonstrate how to handle streaming or batch processing.

2. **Single schema for all input types**: The same JSON schema is applied to all 4 input types. In production, a complaint schema might differ from a feedback schema. A more robust design would select the schema based on a first-pass classification call.

3. **No schema versioning**: The system prompt is a string literal in the code. When the schema changes (adding a field, changing an enum value), there is no version history and no way to know which schema produced a given output in `output_examples.json`.

4. **No downstream routing**: The script extracts structured data but does not do anything with it. In a real system, a `critical` priority complaint with `action_required: true` would trigger an alert, a ticket in a CRM, or a Slack notification.

5. **Confidence score is self-reported**: The `confidence_score` field is generated by the model itself — it is not an objective measure. Models are known to be miscalibrated in self-reported confidence. In production, you would supplement this with an external evaluation step.

6. **Rate limit handling is basic**: The retry logic uses fixed sleep intervals. Production systems use exponential backoff with jitter to avoid thundering herd problems when many workers retry simultaneously.

---

# Key Takeaways

1. **Structured output is an engineering discipline, not just a prompt trick.** The combination of `response_mime_type="application/json"`, temperature 0, and a precise system prompt is a three-layer contract with the model. Each layer is necessary — remove any one of them and reliability degrades.

2. **The system prompt is code.** It defines the output schema just as clearly as a function signature defines an API. Engineers should version it, review it, and test changes to it like any other code change. A vague system prompt produces a vague schema, which breaks the pipeline in ways that are hard to trace.

3. **Token logging is a first-class engineering concern.** Every API call has a cost in tokens, latency, and money. Logging `prompt_token_count` and `candidates_token_count` on every call is not debugging overhead — it is operational data that informs cost forecasting, performance tuning, and abuse detection. Build this habit from the first module.

4. **Production AI systems fail at the edges, not the center.** The happy path (valid input, API succeeds, JSON parses, all fields present) works fine. What distinguishes production-ready code is handling the edges: empty input, missing API key, 429 rate limit, partial JSON, missing fields. Session 1 covers these edge cases explicitly because they are exactly what interviewers ask about.

---

# Session 2 Preview

In Session 2, we will build the LLM Logging and Evaluation Tracker.

Module: `llm_logger.py` + `eval_log.json`

What it does: Logs every LLM API call — the prompt sent, the response received, the token counts, the latency in milliseconds, and a quality score — to a structured JSON log file. The logger can be imported and used by any other module in the portfolio.

How it connects to Session 1: We will run `structured_output_engine.py` through the logger. Every Gemini call made by the structured output engine will be captured: input text, system prompt, JSON response, prompt tokens, completion tokens, and latency. By the end of Session 2, you will have an audit trail for every LLM call your portfolio makes.

What concepts it introduces: LLMOps observability, call logging patterns, latency measurement with `time.perf_counter()`, evaluation metrics (response quality scoring), and the difference between logging for debugging vs. logging for evaluation.

Prepare for Session 2: Make sure `structured_output_engine.py` runs end to end. If it breaks, use the debugging prompt from this session's pre-session file to fix it before Session 2 starts.
