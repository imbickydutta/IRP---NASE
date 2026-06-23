# Session 1 Instructor File: Structured Output Prompt Engine

## Session Title

Structured Output Prompt Engine

## Duration

2 hours

## Portfolio Module

Module 1 of 8 — AI Systems Interview Portfolio (Cohort C)

## Session 1 Objective

By the end of Session 1, students should have a working Python script that takes unstructured text inputs and converts them into clean, predictable JSON using Gemini 1.5 Flash. Students will understand why structured output matters in production AI systems and be able to explain the design choices in an interview.

This script becomes the first artifact in the AI Systems Interview Portfolio. Every future session adds one more standalone module. Session 1 establishes the core pattern that other modules will build on: call an LLM with a well-designed system prompt, get deterministic output, and save the results.

## Session 1 Deliverable

Students will build:

1. `structured_output_engine.py` — a Python script that processes 3–4 hardcoded unstructured text inputs and returns structured JSON using Gemini 1.5 Flash
2. `output_examples.json` — a file containing the parsed outputs from all sample inputs

The script must demonstrate:

- A system prompt that defines the exact JSON schema
- Gemini API call using `response_mime_type="application/json"` in `generation_config`
- Temperature set to 0 for deterministic output
- Side-by-side comparison of free-text vs. structured output
- Token count logging for each call
- Output saved to `output_examples.json`

## Strict Scope Control

### Include

- One Python script: `structured_output_engine.py`
- Gemini 1.5 Flash via `google-generativeai` library
- System prompt with JSON schema definition
- 3–4 hardcoded sample inputs (customer complaint, support ticket, feedback form, product review)
- `response_mime_type="application/json"` in generation config
- Temperature = 0
- Console output showing free-text comparison vs. structured JSON
- Token usage logging (prompt tokens, completion tokens)
- Saves final results to `output_examples.json`
- Clear inline code comments on every function
- Basic error handling for API failures and JSON parse errors

### Do Not Include

- FastAPI or any web framework
- Streamlit or any UI
- Database or ChromaDB (that is Session 4+)
- PDF parsing or file reading
- Batch file processing from disk
- LangChain or LangGraph
- OpenAI or any paid API
- sentence-transformers (not needed for this session — embeddings start in Session 3)
- Complex orchestration or agents
- argparse or CLI flags
- Unit tests (unless a student finishes very early)

Session 1 is only about demonstrating the structured output pattern cleanly.

---

# Instructor Framing

## Opening Message

Show this to students at the start:

```
AI Systems Interview Portfolio — Cohort C

Session 1:  Structured Output Prompt Engine         <- TODAY
Session 2:  LLM Logging and Evaluation Tracker
Session 3:  Serverless-Style AI Function
Session 4:  Basic RAG Pipeline
Session 5:  RAG Evaluation and Improvement
Session 6:  Simple Agent Router
Session 7:  Vision/OCR Mini Module
Session 8:  Final System Design and Interview Demo
```

Tell students: "We are not building one big app. We are building a portfolio of 8 standalone AI engineering modules. Each session produces one Python script or notebook that you can open in any interview and walk through line by line. Session 1 starts today."

## Key Philosophy

Students already studied LLM engineering and prompt engineering. This portfolio is not a lecture series — it is a build series. Every session:

- builds a real artifact
- practices the AI coding tool workflow (prompt → generate → understand → test → explain)
- prepares a specific interview story

The instructor's job is to keep the scope tight, make sure the code runs, and make sure the student can explain every line.

## Repeated Instructor Line

"AI generated the code. But you are responsible for running it, understanding it, and explaining it when an interviewer asks."

---

# Session Flow

## 0–10 min: Opening, Portfolio Recap, Show Existing Folder

### Instructor Goal

Establish context. Show students what the full portfolio looks like and make clear that today's module is the first artifact.

### Actions

- Open the terminal. Show the empty `Cohort C/sessions/` folder.
- Explain: "By Session 8, each folder will have a Python script or notebook that demonstrates a real AI engineering concept."
- Show the portfolio module map. Read through all 8 session names.
- Ask: "Who has used response_mime_type with Gemini before?" — gauge prior exposure.
- Introduce today's module: "Session 1 is about structured output. This is not just a Gemini feature — it is one of the most important patterns in production AI engineering. If your LLM cannot return predictable JSON, you cannot build reliable pipelines."
- Tell students to open their `google-generativeai` docs tab now.
- Confirm everyone has their `GEMINI_API_KEY` environment variable set. This should have been done as pre-session setup.

---

## 10–20 min: Concept Explanation — Prompt Engineering and Structured Output

### Instructor Goal

Give students the mental model before they see the code.

### Key Concepts to Explain

1. What is prompt engineering in production?

   Prompt engineering is not just "write a better prompt." In production AI systems, it means designing prompts that produce consistent, testable, machine-readable output every time. The system prompt is part of your code — it is not optional documentation.

2. What is structured output?

   Structured output means the LLM returns data in a fixed, predictable schema (usually JSON) instead of free text. Free-text responses look great to humans but are nearly impossible to parse reliably in a pipeline.

3. Why does this matter for engineering?

   If an LLM returns free text, every downstream function that reads it will eventually break. If it returns a validated JSON schema, the rest of your pipeline becomes reliable. Structured output is the difference between a demo and a production system.

4. How does Gemini 1.5 Flash support this?

   By passing `response_mime_type="application/json"` in the `generation_config`, Gemini is constrained to return only valid JSON. The system prompt then defines the exact keys, types, and structure expected.

5. What is temperature and why does it matter here?

   Temperature controls randomness. For structured output tasks, temperature should be 0 — we want the same output every time for the same input. This makes the system testable and auditable.

### Draw on the board (or share screen)

```
Unstructured Input (messy text)
        |
        v
System Prompt (defines JSON schema)
        |
        v
Gemini 1.5 Flash (response_mime_type="application/json", temperature=0)
        |
        v
Structured JSON Output (parseable, consistent, pipeline-ready)
        |
        v
output_examples.json (saved for audit, evaluation, review)
```

---

## 20–35 min: Build the Module Using Claude Code or Cursor

### Instructor Goal

Demonstrate the AI-assisted build workflow. The instructor builds first on screen. Students watch and take notes.

### Build Steps

1. Open Claude Code or Cursor in the `session_1/` folder.
2. Paste Prompt 1 from the student pre-session file (the main build prompt).
3. Watch the output together. Do not approve it immediately — scan it first.
4. Check these things before running:
   - Is `google-generativeai` imported?
   - Is `GEMINI_API_KEY` read from environment (not hardcoded)?
   - Is `response_mime_type="application/json"` present in `generation_config`?
   - Is temperature set to 0?
   - Are there at least 3 sample inputs?
   - Does it save output to `output_examples.json`?
5. Run the script. Show the console output.
6. Open `output_examples.json` in the editor. Confirm the JSON is valid.

### What to Watch For During Generation

- AI may try to use `json.loads()` on a response that is already a dict — watch for this
- AI may hardcode the API key — tell students this is a security issue and show the env var pattern
- AI may set temperature higher than 0 — correct it
- AI may import `openai` — this cohort uses Gemini, not OpenAI

---

## 35–50 min: Walk Through Generated Code — Explain Every Function

### Instructor Goal

Students need to understand what was generated. Walk through the script line by line.

### Walk Through These Areas

1. **Imports and API setup**

   ```python
   import google.generativeai as genai
   import os
   import json

   genai.configure(api_key=os.environ["GEMINI_API_KEY"])
   ```

   Explain: `configure()` must be called before any model is used. The API key must come from the environment, not from the code.

2. **The system prompt / schema definition**

   Explain: The system prompt is where you define the JSON schema. It should be clear, specific, and include field names, types, and a description of each field. A vague system prompt gives a vague schema even with `response_mime_type`.

3. **The `generation_config` block**

   Explain: `response_mime_type="application/json"` tells Gemini to return only valid JSON. Temperature 0 removes randomness. Without these two settings, you do not have structured output — you have structured-looking output that will occasionally break.

4. **The `process_input()` function**

   Explain: This function sends one text input to Gemini and returns the parsed JSON. It should handle the case where `response.text` is already valid JSON (not double-encoded). It should also handle the case where Gemini returns an error or empty text.

5. **The sample inputs list**

   Explain: These are hardcoded for this session. In production, these would come from a database, queue, or file. Show students all 3–4 input types: customer complaint, support ticket, feedback form, product review.

6. **The free-text vs. structured comparison block**

   Explain: Before running with `response_mime_type`, show what Gemini returns with free text for the same input. This side-by-side is the most important learning moment of Session 1.

7. **Token usage logging**

   Explain: `response.usage_metadata.prompt_token_count` and `response.usage_metadata.candidates_token_count` give token counts. Students should log these so they can estimate costs. On Gemini 1.5 Flash free tier, this is $0 for now, but in production every token has a cost.

8. **Saving to `output_examples.json`**

   Explain: Always save LLM outputs to a file. In production you would save to a database. For this portfolio, a JSON file is enough. This file becomes an artifact you can show in interviews.

### Ask During Walkthrough

- What happens if `os.environ["GEMINI_API_KEY"]` is not set?
- What does `response_mime_type="application/json"` actually guarantee?
- Why do we call `json.loads()` on `response.text` instead of using `response.text` directly?
- What would break if temperature were set to 0.9 instead of 0?
- How would you add a new sample input type without changing the schema?

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students open their own terminal and Claude Code / Cursor session in their `session_1/` folder. They paste Prompt 1 and build their own version of `structured_output_engine.py`.

### Instructor Support Areas

Watch for and help students with:

- `GEMINI_API_KEY` not set — show: `export GEMINI_API_KEY="your_key_here"` in terminal
- `ModuleNotFoundError: No module named 'google.generativeai'` — run: `pip install google-generativeai`
- Student AI tool generates `import openai` — remind them Cohort C uses Gemini only
- `response.text` returning an empty string — usually means the prompt triggered a safety filter, show how to inspect `response.prompt_feedback`
- Generated code does not include the free-text comparison — tell students to ask the AI tool to add it
- `output_examples.json` not being created — check that the save function is actually called at script end

### If a Student's Setup Fails

Do not block the class. The student should:

1. Follow the instructor screen
2. Pair with a neighbour who has a working setup
3. Use the shared completed code after session to catch up
4. Run the script at home and bring questions to the next session

---

## 65–80 min: Test With Sample Inputs, Inspect Output Files

### Instructor Goal

Verify the output is correct and discuss what the JSON means for a production pipeline.

### Test Steps

1. Run `python structured_output_engine.py` together as a class.
2. Read the console output. Ask: "Is the JSON valid? Is the schema consistent across all 4 inputs?"
3. Open `output_examples.json`. Validate it at jsonlint.com or with `python -m json.tool output_examples.json`.
4. Ask: "If this were an actual production system, what would the next step be after producing this JSON?" Expected: downstream system reads the JSON, routes the ticket, triggers a workflow, stores in a database.
5. Show students how to add a 5th test input themselves without changing the schema.
6. Run again and verify the 5th input appears in `output_examples.json`.

### Discussion

Ask: "What would happen to a downstream pipeline if the LLM returned 'I'm sorry, I could not parse that' in plain text instead of JSON?"

This question gets students thinking about reliability, error contracts, and why structured output matters beyond aesthetics.

---

## 80–95 min: Edge Cases, Error Handling, Failure Modes

### Instructor Goal

Teach students to think about what breaks. This is what separates a demo from a production module.

### Edge Cases to Cover

1. **Empty input string**

   What happens if someone calls `process_input("")`? The LLM will either hallucinate a response or return an error. Show students how to add an input validation check before calling the API.

2. **Gemini rate limit (429 error)**

   On the free tier, Gemini has rate limits. Show students the error message:
   ```
   google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded
   ```
   Show how to wrap the API call in a try/except and add a simple retry with `time.sleep(5)`.

3. **JSON parse failure**

   Even with `response_mime_type="application/json"`, the returned string may occasionally not be parseable if there is a network error or unexpected response. Show:
   ```python
   try:
       result = json.loads(response.text)
   except json.JSONDecodeError as e:
       print(f"JSON parse error: {e}")
       result = {"error": "parse_failed", "raw": response.text}
   ```

4. **Missing keys in returned JSON**

   The LLM may return a valid JSON object but omit a field. Show students how to use `.get()` with a default instead of direct key access.

5. **API key not set**

   Show the error:
   ```
   KeyError: 'GEMINI_API_KEY'
   ```
   And the fix: check for the key at script start and give a clear error message.

6. **Model name typo**

   Show what happens with `genai.GenerativeModel("gemini-1.5-flaash")` — the API returns a model not found error. Correct model name is `gemini-1.5-flash`.

Use Prompt 2 (Improvement Prompt) from the student pre-session file to let students ask their AI tool to add this error handling automatically.

---

## 95–105 min: Concept Pause

### Instructor Goal

Step back from the code and build interview-level understanding of the concepts.

### Concepts to Cover

**1. Prompt Engineering in Production**

Prompt engineering at the production level is not about clever phrasing. It is about designing prompts that behave like function contracts: given this input, always return this output shape. The system prompt is a specification. Temperature 0 is an enforcement mechanism. `response_mime_type` is a constraint layer. Together, these three elements make LLM output reliable enough to be used in a pipeline.

**2. Structured Output and Why It Matters**

Free text is for humans. JSON is for systems. The moment you need an LLM to feed output into another function, a database, a workflow, or a dashboard, you need structured output. Developers who do not enforce structured output spend enormous time writing fragile parsers. Structured output moves that contract to the model layer, where it belongs.

**3. Token and Cost Awareness**

Every LLM call has a cost — in tokens, latency, and money. Even on the free tier, practicing token logging builds the habit. In production at scale, a 500-token prompt called 100,000 times per day costs real money. Students should always log prompt tokens and completion tokens. Show: the system prompt itself has a fixed token cost on every call — that is why lean, precise system prompts matter.

**4. Deterministic Output Design**

Non-deterministic AI output creates non-deterministic bugs. A bug that only appears sometimes because temperature was 0.7 is the hardest kind of bug to reproduce. For structured output tasks — parsing, classification, extraction — always use temperature 0. Reserve higher temperatures for creative tasks where variation is acceptable and does not flow into a pipeline.

### Student Writing Task

Ask every student to write 2–3 lines:

"Why would you set temperature to 0 for a structured output task?"

Expected response: Because we want the same output format every time for the same input. Temperature 0 removes randomness, which makes the output testable and auditable. For tasks that feed a pipeline, non-determinism is a defect.

---

## 105–115 min: Interview Discussion and Viva Practice

### Instructor Goal

Prepare students to speak about this module confidently in an interview setting.

Use the interview questions from the Questions to Discuss section below. Do not cover all 15 — pick 5–6 that fit the time. Prioritize Q1, Q3, Q6, Q9, Q12, Q14.

### Practice Format

Ask the question aloud. Give students 60 seconds to prepare. Call on one student to answer. Ask one follow-up question. Let others add to the answer. Repeat for 2–3 questions.

---

## 115–120 min: Wrap-Up, Show Deliverables, Preview Next Session

### Instructor Closing

"Today you built Module 1 of your AI Systems Interview Portfolio. You have two artifacts: `structured_output_engine.py` and `output_examples.json`. Open them now. These are yours. You can run them, explain them, modify them."

"In Session 2, we will build the LLM Logging and Evaluation Tracker. That module will log every LLM call — the prompt, the response, the token count, the latency, and a quality score. Session 2 builds directly on Session 1: we will log the calls that structured_output_engine.py makes as one of the inputs to the logging system."

"Before Session 2: make sure your script runs end to end. If it breaks, use the debugging prompt from your pre-session file to fix it. Bring any unresolved errors to Session 2."

---

# Instructor Notes

## What to Emphasize

1. The system prompt is not optional text — it is a contract that defines the output schema. If the system prompt is vague, the JSON structure will be inconsistent.

2. `response_mime_type="application/json"` is a Gemini-specific parameter in `generation_config`, not a parameter on the model object. Students often put it in the wrong place.

3. Temperature 0 does not mean the model is stupid — it means the model is consistent. For structured parsing tasks, consistency matters more than creativity.

4. Token logging is a professional habit. Students who never log tokens do not understand the cost model of production AI systems.

5. The free-text vs. structured comparison is the most important demo of Session 1. Do not skip it. Without seeing what free-text output looks like, students do not appreciate why structured output is a design decision and not just a feature.

6. `output_examples.json` is an artifact, not just a debug file. In a real system this would be stored in a database. In this portfolio it is a file. Either way, saving LLM outputs is a non-negotiable engineering practice — it enables evaluation, auditing, and debugging.

7. Students should be able to say: "I used `response_mime_type='application/json'` in the generation_config to constrain Gemini to return only valid JSON, and I set temperature to 0 to ensure deterministic output." This one sentence answers 3 interview questions.

8. The `google-generativeai` library is different from the OpenAI library. The API object is `genai.GenerativeModel`, not `openai.ChatCompletion`. Make sure students are not copying OpenAI patterns.

## Common Student Mistakes

1. **Hardcoding the API key in the script**

   Error pattern: `genai.configure(api_key="AIzaSy...")`

   Fix: Use `os.environ["GEMINI_API_KEY"]`. Show how to set it in terminal with `export GEMINI_API_KEY="..."`.

2. **Putting `response_mime_type` on the model object instead of in generation_config**

   Error: `genai.GenerativeModel("gemini-1.5-flash", response_mime_type="application/json")` — this does not work.

   Fix: Put it inside `generation_config={"response_mime_type": "application/json", "temperature": 0}`.

3. **Calling `json.loads()` on a response that is already a Python dict**

   Error: `TypeError: the JSON object must be str, bytes or bytearray, not dict`

   This happens when the AI-generated code returns `response.candidates[0].content.parts[0].text` as a dict instead of a string. Check the actual type before parsing.

4. **Model name typo**

   Error: `google.api_core.exceptions.NotFound: 404 models/gemini-1.5-flaash is not found`

   Fix: Correct model name is `"gemini-1.5-flash"` (one 's').

5. **Not setting temperature to 0**

   The script runs but the JSON structure varies between runs — different field names appear sometimes. This is a temperature issue. Show how the same input gives different output with temperature=0.7 vs. temperature=0.

6. **Empty system prompt**

   Student deletes the system prompt to "simplify" the code. The model then returns free text or inconsistent JSON. Emphasize: the system prompt is the schema definition — it must be specific and must not be removed.

7. **`GEMINI_API_KEY` environment variable not exported before running**

   Error: `KeyError: 'GEMINI_API_KEY'`

   This happens when students set the variable in a new terminal tab but run the script in a different tab. Show: `echo $GEMINI_API_KEY` to verify it is set in the current shell.

8. **Forgetting to call `json.loads()` on `response.text`**

   The student prints `response.text` and sees what looks like JSON, but it is a string. Downstream code that tries to access `response.text["category"]` will fail with `TypeError: string indices must be integers`.

9. **Saving to `output_examples.json` with `w` mode inside a loop**

   Error: only the last input gets saved because each iteration overwrites the file. Fix: collect all results in a list first, then write the entire list at the end.

10. **Gemini 429 rate limit mid-session**

    Error: `google.api_core.exceptions.ResourceExhausted: 429 RESOURCE_EXHAUSTED`

    This is common on the free tier during class when many students hit the API at the same time. Fix: add `time.sleep(5)` between calls and wrap in try/except with retry logic. See the Instructor Backup Plan section.

## How to Control the Session

Use this rule: if a student is adding something that is not in the Include list, stop them.

The most common out-of-scope additions:

- Building a Streamlit UI around the script
- Adding a database to store outputs
- Adding a loop that reads from a CSV file
- Switching from Gemini to GPT-4 "because it is better"
- Adding LangChain "just to try it"

If this happens: "That is a great idea. Write it down. We are not building it today because it is not in Session 1 scope. If you add it now, you will spend the whole session on it and miss the concept."

Session 1 is one script, one API, one output file. Nothing more.

---

# Questions to Discuss: Interview Perspective

## Basic Module Questions

### Q1. What did you build in Session 1?

Expected answer:

I built a Python script called `structured_output_engine.py` that takes unstructured text inputs — a customer complaint, a support ticket, a feedback form, and a product review — and converts them into clean, predictable JSON using Gemini 1.5 Flash. The script uses `response_mime_type="application/json"` in the generation config to constrain the model to return only valid JSON, and sets temperature to 0 to make the output deterministic. All results are saved to `output_examples.json`. This module demonstrates the structured output pattern, which is foundational to building reliable AI pipelines.

### Q2. What problem does structured output solve?

Expected answer:

Structured output solves the problem of unreliable LLM responses in production systems. When an LLM returns free text, any downstream function that tries to extract specific fields from that text will eventually break — the model might phrase things differently, add extra explanation, or change its formatting. By enforcing a JSON schema through `response_mime_type` and a precise system prompt, the output becomes consistent and machine-readable. This means the rest of the pipeline can treat the LLM as a reliable function that always returns the same shape of data, which is what production engineering requires.

### Q3. Why did you use Gemini 1.5 Flash instead of a larger model?

Expected answer:

Gemini 1.5 Flash is a fast, efficient model available on the free tier via Google AI Studio, which makes it practical for a portfolio project. More importantly, for structured output tasks like extraction and classification, a smaller model with a well-designed system prompt and `response_mime_type` constraint produces reliable results without needing the capacity of a larger model. In production, engineers often choose smaller, faster models for structured extraction tasks to reduce cost and latency, reserving larger models for complex reasoning tasks.

### Q4. What is `response_mime_type="application/json"` and what does it do?

Expected answer:

`response_mime_type="application/json"` is a parameter in the `generation_config` dictionary passed to Gemini's `generate_content()` method. It instructs the model to return its response as a valid JSON string rather than free text. This is different from simply asking the model to "respond in JSON" in the prompt — the mime type is a structural constraint applied at the API level, which makes the output significantly more reliable. When this parameter is set, the model will not include any preamble, explanation, or markdown — it returns only the JSON object.

### Q5. What is stored in `output_examples.json` and why does it matter?

Expected answer:

`output_examples.json` contains a JSON array where each element includes the original unstructured input text and the structured JSON output that Gemini returned. Saving LLM outputs is an important engineering practice because it enables evaluation, auditing, and debugging. In production, you would store these in a database with timestamps, model version, token counts, and latency. For this portfolio, the JSON file is an artifact that demonstrates the complete input-to-output transformation and can be shown in an interview to prove the module works end to end.

## Technical Deep-Dive Questions

### Q6. Why is temperature set to 0 and what happens if you change it?

Expected answer:

Temperature controls the randomness of the model's output. At temperature 0, the model always selects the highest-probability token at each step, which produces consistent, deterministic output. For structured extraction tasks, determinism is critical — if you send the same customer complaint twice, you want the same JSON back both times. If temperature were set to 0.7 or higher, the model might occasionally return different field values, different key names, or add extra fields not in the schema. This makes the output non-deterministic and breaks downstream pipeline components that depend on a fixed schema. Temperature 0 is the correct setting for any task that feeds structured output into a pipeline.

### Q7. How do you define the JSON schema in the system prompt?

Expected answer:

The system prompt defines the schema by specifying the exact JSON structure the model must return, including all field names, their expected data types, and a brief description of what each field should contain. A well-designed system prompt for structured output will include an example of the expected output, list all mandatory fields explicitly, and instruct the model not to add fields not in the schema and not to include any text outside the JSON object. The system prompt acts as a contract between the engineer and the model. The more specific the system prompt, the more consistent the output.

### Q8. What is the difference between passing the schema in the system prompt versus using Gemini's native structured output with response_schema?

Expected answer:

Gemini also supports `response_schema` in `generation_config`, which allows you to pass a Python dataclass or a Pydantic model as a schema and have Gemini validate against it at the API level. For this module, the schema is defined in the system prompt as a JSON example, and `response_mime_type="application/json"` is used to enforce JSON output. The system prompt approach is more portable — it works across different model providers and versions — while `response_schema` is more rigid but gives stricter validation. In production, `response_schema` provides better guarantees but creates tighter coupling to the Gemini API. For a portfolio module demonstrating the core pattern, the system prompt approach is the better teaching choice because it makes the schema visible and explicit.

### Q9. How do you handle the case where Gemini returns malformed JSON despite `response_mime_type`?

Expected answer:

Although `response_mime_type="application/json"` significantly reduces the likelihood of malformed output, edge cases can still occur — for example, network interruptions, safety filter triggers, or unexpected model behavior. The correct approach is to wrap `json.loads(response.text)` in a try/except block that catches `json.JSONDecodeError`. On failure, you should log the raw response, store an error record in the output, and continue processing the remaining inputs rather than crashing. In production, you would also add retry logic with exponential backoff and send alerts if the parse failure rate exceeds a threshold.

### Q10. How does token counting work in the google-generativeai library and why should you log it?

Expected answer:

After calling `generate_content()`, the response object includes a `usage_metadata` attribute with `prompt_token_count` and `candidates_token_count` fields. `prompt_token_count` is the number of tokens in the combined system prompt plus user input. `candidates_token_count` is the number of tokens in the model's response. Total tokens billed equals the sum of these two. Logging these values is important for cost forecasting, identifying expensive prompts, and detecting prompt injection attacks that inflate token counts. Even on the free tier, building the habit of token logging means you are production-ready: when you move to a paid deployment, you already have visibility into costs.

## Production and System Design Questions

### Q11. How would you scale this structured output pattern to process 10,000 inputs per day?

Expected answer:

To scale to 10,000 inputs per day, I would move from a script with hardcoded inputs to a pipeline with a queue. Inputs would arrive via a message queue (such as Google Pub/Sub or AWS SQS), and a pool of workers would read from the queue and call the Gemini API concurrently. The Gemini free tier has rate limits, so in production I would use the paid tier or implement retry logic with exponential backoff and jitter to handle 429 errors gracefully. Results would be written to a database (such as BigQuery or Postgres) instead of a JSON file. I would add a monitoring layer to track error rates, average latency, token costs, and schema validation failures. The system prompt and schema would be versioned in a config file, not hardcoded in the script.

### Q12. What breaks in production that does not break in this module?

Expected answer:

Several things that work fine in a local script break in production. First, the system prompt is hardcoded — in production it must be versioned and configurable so you can update the schema without redeploying code. Second, there is no retry logic — a single 429 or network error crashes the script. Third, outputs are saved to a local file — in production, concurrent writers would corrupt the file. Fourth, there is no schema validation after parsing — the module trusts that Gemini returns exactly the right fields, but production code should validate every field exists and has the expected type before routing the data downstream. Fifth, there is no latency tracking — without measuring how long each API call takes, it is impossible to detect model degradation or SLA violations.

### Q13. How would you monitor this system in production?

Expected answer:

I would instrument three layers. At the API call level, I would log every call with a timestamp, the input text hash, the prompt token count, the completion token count, the latency in milliseconds, and whether the response was valid JSON. At the output level, I would run a schema validator on every result and emit a metric each time a field is missing, the wrong type, or out of expected range. At the system level, I would set up alerts for error rate above 1%, average latency above 2 seconds, and daily token cost above a budget threshold. These metrics would flow into a dashboard (Grafana, Datadog, or even a Streamlit app built in a later session) so that degradation is visible before it affects downstream systems.

### Q14. How would you evaluate whether the structured output is correct?

Expected answer:

For evaluation, I would create a labeled test set: take 50 inputs and manually write the expected JSON output for each. Then I would run the system on those 50 inputs and compare the model's output with the ground truth using field-level accuracy — not exact string match, because some fields may have acceptable variation. I would calculate precision and recall for categorical fields like `category` and `priority`, and use semantic similarity (with sentence-transformers) for free-text fields like `summary`. If the model fails on a subset of inputs, I would refine the system prompt for those cases. This is called prompt-level evaluation and it is what Session 5 covers in the RAG evaluation module.

### Q15. How does this structured output module connect to the rest of the portfolio?

Expected answer:

The structured output pattern built in Session 1 is foundational to the entire portfolio. Session 2 (LLM Logging and Evaluation Tracker) will log every call that Session 1 makes, adding observability to the structured output engine. Session 4 (Basic RAG Pipeline) will use Gemini 1.5 Flash with a similar generation config to generate structured answers from retrieved documents. Session 5 (RAG Evaluation and Improvement) will evaluate the quality of those structured answers. Session 6 (Simple Agent Router) will use structured JSON output from Gemini 1.5 Flash for intent classification where the JSON result drives tool dispatch. Session 7 (Vision/OCR Mini Module) applies the same structured output principles to multimodal input. Session 8 (Final System Design and Interview Demo) will synthesize the portfolio. The skill of designing reliable system prompts, setting temperature to 0, and parsing JSON responses correctly appears in every module that follows.

---

# Session 1 Completion Checklist

Students should confirm each item before the session ends:

- [ ] `structured_output_engine.py` exists in the `session_1/` folder
- [ ] Script runs end to end with `python structured_output_engine.py` without errors
- [ ] Gemini API key is read from `os.environ["GEMINI_API_KEY"]`, not hardcoded
- [ ] `response_mime_type="application/json"` is present in `generation_config`
- [ ] Temperature is set to 0 in `generation_config`
- [ ] Model name is `"gemini-1.5-flash"` (correct spelling)
- [ ] Script processes at least 3 different input types (complaint, ticket, feedback)
- [ ] Console output shows both free-text response and structured JSON response for at least one input
- [ ] Token counts (prompt and completion) are printed to console for each call
- [ ] `output_examples.json` is created and contains valid, parseable JSON
- [ ] `output_examples.json` contains all inputs processed, not just the last one
- [ ] Student can explain what `response_mime_type` does without reading the script

---

# Instructor Backup Plan

## If Gemini Rate Limit (429) Hits During Class

This is the most common live disruption. When multiple students hit the free-tier API simultaneously, 429 errors will appear.

Actions:
1. Pause the class and acknowledge the error. Explain: "This is a real production issue. Free tier has rate limits. Paid tier has higher limits but still has them."
2. Show students how to add `time.sleep(5)` between API calls to spread the load.
3. If the class is large, stagger when students run their scripts — run in groups of 3–4 students at a time.
4. If rate limits persist: switch to showing the instructor screen only. Students follow along conceptually. They run their scripts after class.
5. Pre-generate and save a sample `output_examples.json` in the shared folder before class so students can inspect a real output even if their API calls fail.

## If a Student's Python Environment Fails

Actions:
1. First check: Is `google-generativeai` installed? Run `pip install google-generativeai` and retry.
2. Second check: Is the API key set? Run `echo $GEMINI_API_KEY` in the terminal.
3. Third check: Is the Python version correct? Gemini library requires Python 3.9+. Run `python --version`.
4. If the environment cannot be fixed in 5 minutes: the student pairs with a working student.
5. After session: share the instructor's completed `structured_output_engine.py` in the course folder so the student can run it in their own environment.

## If AI Code Generation Produces Unusable Output

Actions:
1. Share Prompt 1 directly from the student pre-session file on screen. Have the student copy it exactly — do not let them paraphrase it.
2. If Claude Code or Cursor generates code using `import openai`, add this line to the prompt: "Do not import openai. Use only google-generativeai."
3. If the generated code is too complex (adds LangChain, FastAPI, etc.), add: "This is a standalone Python script with no web framework, no LangChain, and no database."
4. If all else fails, the instructor live-codes the minimum viable version of the script on screen while explaining each line. Students take notes and build their version after class.
