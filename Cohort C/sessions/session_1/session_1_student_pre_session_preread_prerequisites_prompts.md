# Session 1 Student Pre-Session File: Structured Output Prompt Engine

## What We Are Building

In this 8-session AI Systems Interview Portfolio, we are not building one app. We are building 8 standalone Python scripts and notebooks — one per session. Each is a self-contained AI engineering module that you own, can run independently, and can explain in an interview.

By the end of all 8 sessions, your portfolio will cover: structured output, LLM observability, semantic search, RAG pipelines, RAG evaluation, prompt chaining, LLMOps monitoring, and agentic workflows.

## Session 1 Goal

In Session 1, we will build the Structured Output Prompt Engine.

This script takes messy, unstructured text — customer complaints, support tickets, feedback forms, product reviews — and converts them into clean, predictable JSON using Gemini 1.5 Flash.

This is not a toy demo. Structured output extraction is one of the most common patterns in real production AI systems: customer support routing, CRM enrichment, compliance monitoring, ticket triage, and content moderation all rely on it.

## Session 1 Deliverable: `structured_output_engine.py` + `output_examples.json`

By the end of Session 1, you will have:

1. `structured_output_engine.py` — a Python script that processes 3–4 unstructured text inputs and converts each into a structured JSON object using Gemini 1.5 Flash
2. `output_examples.json` — a file containing the structured outputs from all processed inputs

The script will demonstrate:

- A system prompt that defines the JSON schema
- Gemini API configured with `response_mime_type="application/json"` and temperature 0
- Console output showing the free-text LLM response vs. the structured JSON
- Token count logging for every API call
- Results saved to `output_examples.json`

---

# Pre-Read

## Why Does This Module Exist in the Portfolio?

Every module in this portfolio solves a real problem that AI engineers face in production systems.

The problem Session 1 solves: LLMs return free text. Free text is unpredictable. Unpredictable output breaks pipelines.

If you ask an LLM "what is the priority of this complaint?" it might say:
- "The priority is high."
- "I would classify this as a high-priority issue."
- "High priority — the customer is very frustrated."

All three answers mean the same thing, but no code can reliably extract the word "high" from all three without fragile string parsing. The moment the model changes its phrasing style, your parser breaks.

Structured output solves this by constraining the model to return a fixed JSON schema every time. This is the foundation of reliable AI pipelines.

## Portfolio Module Map

```
Session 1: Structured Output Prompt Engine              <- YOU ARE HERE
           (structured_output_engine.py + output_examples.json)
                |
                v
Session 2: LLM Logging and Evaluation Tracker
           (llm_logger.py + eval_log.json)
                |
                v
Session 3: Serverless-Style AI Function
           (ai_handler.py + .env.example)
                |
                v
Session 4: Basic RAG Pipeline              <---------+
           (rag_pipeline.py + chroma_db/)             |
                |                                     |
                v                                     |
Session 5: RAG Evaluation and Improvement  <----------+
           (rag_evaluator.py + rag_eval_report.csv)   (Sessions 4 & 5 are connected)
                |
                v
Session 6: Simple Agent Router
           (agent_router.py)
                |
                v
Session 7: Vision/OCR Mini Module
           (vision_ocr_module.py)
                |
                v
Session 8: Final System Design and Interview Demo
```

Sessions 4 and 5 are directly connected: Session 4 builds the RAG pipeline, Session 5 evaluates it. All other sessions are standalone, but the concepts build on each other.

## Key Concepts to Revise Before Session 1

1. **System prompt vs. user prompt**

   A system prompt sets the model's role, rules, and output format. A user prompt is the actual input. In production systems, the system prompt is engineered carefully — it is your contract with the model. The user prompt changes per request; the system prompt usually stays fixed.

2. **JSON structure**

   JSON (JavaScript Object Notation) is a key-value data format used universally in APIs and pipelines. Know what a JSON object, array, string, number, boolean, and null look like. Know how to access a value by key in Python: `data["category"]`.

3. **Temperature in LLMs**

   Temperature is a parameter that controls how random the model's output is. Temperature 0 means fully deterministic — the model always picks the highest-probability next token. Temperature 1 means more random and creative. For structured extraction tasks, always use temperature 0.

4. **Tokens and cost awareness**

   LLMs do not process words — they process tokens. A token is roughly 4 characters or 0.75 words in English. Every API call has a token count: prompt tokens (input) + completion tokens (output). In production, you pay per token. Even on the free tier, logging tokens builds the habit of cost awareness.

5. **Environment variables for API keys**

   Never hardcode an API key in a Python script. Always store it in an environment variable and read it with `os.environ["GEMINI_API_KEY"]`. This prevents accidental key leakage when you share or commit your code.

6. **The google-generativeai Python library**

   This is the official Python SDK for Google's Gemini models. It is not the same as the OpenAI library. The key class is `genai.GenerativeModel`. The key method is `model.generate_content()`. Configuration is passed via a `generation_config` dictionary.

7. **JSON parsing in Python**

   `json.loads()` converts a JSON string into a Python dictionary. `json.dumps()` converts a Python dictionary into a JSON string. `json.dump()` writes a Python object to a JSON file. Know the difference between these three.

8. **Try/except for external API calls**

   Any call to an external API can fail — network issues, rate limits, server errors. Wrap API calls in try/except blocks. Catch specific exceptions when possible (for example, `google.api_core.exceptions.ResourceExhausted` for a 429 rate limit error).

## Technical Explanation of the Core Concept

When you call Gemini with `response_mime_type="application/json"` in the `generation_config`, you are telling the API to apply a structural constraint on the model's output. The model will not return explanatory text, markdown formatting, or code fences — it returns a raw JSON string that Python can parse directly with `json.loads()`.

The system prompt then defines what that JSON must look like: which keys to include, what values to expect, and how to extract them from the input text. Together, these two mechanisms — the structural constraint from the API and the schema definition from the system prompt — produce output that is both valid JSON and semantically correct.

The reason this matters in production: imagine a customer support pipeline that processes 5,000 tickets per hour. Each ticket must be classified by category, assigned a priority, and have a one-line summary extracted. If even 1% of tickets return malformed output, that is 50 tickets per hour that break the pipeline. With structured output properly configured, that error rate drops to near zero — and when an error does occur, it is caused by an API failure, not by model phrasing variability, which is a different and solvable problem.

---

# Setup Before Class

## Required Installations

Run these before the session. Do not do this during the live session.

```bash
pip install google-generativeai
pip install python-dotenv
```

Verify the installation:

```bash
python -c "import google.generativeai as genai; print('google-generativeai installed successfully')"
```

## Gemini API Key Setup

1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (it starts with `AIzaSy...`)

Set it as an environment variable in your terminal:

```bash
export GEMINI_API_KEY="your_key_here"
```

For permanent setup (so you do not have to set it every session), add that line to your `~/.zshrc` or `~/.bashrc` file.

Verify the key is set:

```bash
echo $GEMINI_API_KEY
```

You should see your key printed in the terminal. If you see nothing, the variable is not set.

## Verify Setup: One-Line Test

Run this in your terminal to confirm Gemini is working:

```python
python -c "
import google.generativeai as genai
import os
genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content('Say hello in one word')
print(response.text)
"
```

If this prints a single word (like "Hello" or "Hi"), your setup is working. If you see an error, fix it before the session.

## Folder Setup

Create this folder before the session:

```bash
mkdir -p "Cohort C/sessions/session_1"
cd "Cohort C/sessions/session_1"
```

---

# Sample Data / Content to Prepare

Prepare these 4 input texts before class. You will use them as hardcoded samples in your script. Save them in a text file so you can paste them quickly.

```text
Sample Input 1 — Customer Complaint:
"I ordered a laptop bag on the 5th and it still hasn't arrived. It's been 12 days!
I've sent two emails and nobody has responded. This is completely unacceptable.
I need either my item delivered immediately or a full refund. Order #89234."

Sample Input 2 — Support Ticket:
"App crashes every time I try to export a report as PDF. I'm on version 3.2.1,
MacOS Ventura 13.4. This has been happening since the last update. It works fine
if I export as CSV. Happens 100% of the time, not intermittent."

Sample Input 3 — Feedback Form Response:
"The onboarding experience was decent but the tutorial videos are too fast.
I couldn't follow along. The UI is clean and the search works well but I wish
there was a dark mode. Overall I'd give it a 6 out of 10. Would recommend
to someone with technical background but not to a beginner."

Sample Input 4 — Product Review:
"Bought this wireless mouse 3 weeks ago. The scroll wheel started squeaking
after week one and the Bluetooth drops out every few minutes. Build quality
feels cheap for the price. Customer service replaced it quickly which was good
but the replacement has the same issue. Very disappointed."
```

---

# Prompts for Session 1

Use these prompts during the session in Claude Code or Cursor. Copy each prompt exactly as written.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Systems Interview Portfolio in Python. This is a portfolio of standalone scripts — not a web app.

Context:
- Portfolio name: AI Systems Interview Portfolio (Cohort C)
- Session 1 module: Structured Output Prompt Engine
- LLM: Gemini 1.5 Flash via google-generativeai library
- No OpenAI. No LangChain. No FastAPI. No Streamlit. No database.
- Python script only.

Modules already built: None — this is the first session.

Create a Python file called structured_output_engine.py that does the following:

1. Import google.generativeai as genai, os, json, and time.
2. Read the Gemini API key from os.environ["GEMINI_API_KEY"] — do not hardcode it.
3. Configure the Gemini client with genai.configure(api_key=...).
4. Define a system prompt that instructs Gemini to extract structured information from unstructured customer text and return a JSON object with exactly these fields:
   - "category": string, one of ["complaint", "bug_report", "feedback", "review"]
   - "priority": string, one of ["low", "medium", "high", "critical"]
   - "sentiment": string, one of ["positive", "neutral", "negative"]
   - "summary": string, one-sentence summary of the main issue or message
   - "key_issue": string, the single most important problem or topic mentioned
   - "action_required": boolean, true if this requires a human response
   - "confidence_score": float between 0.0 and 1.0 indicating model confidence

5. Create a GenerativeModel using "gemini-1.5-flash" with generation_config that includes:
   - response_mime_type set to "application/json"
   - temperature set to 0

6. Create a function called process_input(text: str, model) that:
   - Takes the unstructured text and sends it to Gemini with the system prompt
   - Returns the parsed JSON as a Python dictionary
   - Logs prompt token count and completion token count from response.usage_metadata
   - Handles json.JSONDecodeError and returns an error dict if parsing fails
   - Handles google.api_core.exceptions.ResourceExhausted (429) with a time.sleep(5) retry once

7. Create a list called SAMPLE_INPUTS with exactly these 4 hardcoded inputs:
   - A customer complaint about a delayed order (order not arrived, 12 days, no email response)
   - A bug report about an app crashing on PDF export (version 3.2.1, MacOS, 100% reproducible)
   - A feedback form response (onboarding too fast, clean UI, wants dark mode, 6/10 rating)
   - A product review about a wireless mouse (scroll wheel squeaking, Bluetooth drops, poor build quality)

8. Create a function called compare_free_text_vs_structured(text: str, model) that:
   - First calls Gemini WITHOUT response_mime_type (temperature=0.7) and prints the free text response
   - Then calls Gemini WITH response_mime_type="application/json" and temperature=0 and prints the structured JSON
   - Shows a clear separator between the two outputs
   - Only run this comparison for the first sample input, not all four

9. In the main() function:
   - Run compare_free_text_vs_structured on SAMPLE_INPUTS[0]
   - Process all 4 inputs with process_input()
   - Collect results in a list: each result should be a dict with "input_text" and "structured_output" keys
   - Print each result to console with clear formatting
   - Save the full list to output_examples.json using json.dump with indent=2

10. Add a comment block at the top of the file explaining:
    - What this module does
    - Why structured output matters
    - Which Gemini parameters are critical and why

11. Add inline comments on every function explaining what it does and why.

Do not add:
- Streamlit or any UI
- FastAPI or any web server
- ChromaDB or any vector database
- LangChain or LangGraph
- argparse or CLI argument parsing
- Unit tests
- sentence-transformers (not needed this session)

This must be a single Python file that runs with: python structured_output_engine.py
```

---

## Prompt 2: Improvement Prompt

```text
Improve the structured_output_engine.py script with the following enhancements:

1. Better error handling:
   - If os.environ["GEMINI_API_KEY"] is not set, print a clear error message with instructions and exit gracefully instead of raising a KeyError.
   - If response.text is empty or None after the API call, return a structured error dict instead of crashing.
   - Add a check that the returned JSON contains all 7 expected keys. If any key is missing, add it with a default value and log a warning.

2. Cleaner output formatting:
   - Print a separator line (e.g., 60 dashes) between each processed input in the console output.
   - Print a summary at the end showing: total inputs processed, total prompt tokens used, total completion tokens used, and estimated total tokens.

3. Token and cost awareness:
   - After processing all inputs, print a token summary table to console.
   - Add a comment in the code explaining how to estimate cost using Gemini's pricing page.

4. JSON output quality:
   - Before saving to output_examples.json, validate that json.dumps(results) does not raise an error.
   - Add a "processed_at" timestamp field (ISO format) to each result dict using datetime.now().isoformat().
   - Add a "model_used" field set to "gemini-1.5-flash" to each result dict.

Do not add any UI, database, or external dependencies beyond google-generativeai and Python standard library.
Preserve the existing function structure — only add to it, do not rewrite it.
```

---

## Prompt 3: Debugging Prompt — Gemini 429 Rate Limit

```text
My structured_output_engine.py script is failing with this error:

google.api_core.exceptions.ResourceExhausted: 429 RESOURCE_EXHAUSTED.
Quota exceeded for quota metric 'generate_content_free_tier_requests' and limit
'GenerateContentPerMinute_FreeTier' of service 'generativelanguage.googleapis.com'.

Please fix the script to handle this error gracefully.

Expected behavior after fix:
1. When a 429 error is encountered, wait 10 seconds and retry the same request once.
2. If the retry also fails with 429, wait 30 seconds and retry a second time.
3. If the second retry also fails, log the error and return a dict with "error": "rate_limit_exceeded" and "input_text": the original input text.
4. The script should continue processing remaining inputs even if one fails.
5. At the end of the script, print how many inputs succeeded and how many failed.

Also add a 2-second delay between each API call to reduce the chance of hitting the rate limit in the first place.

Do not change the structure of the main function or the output format of output_examples.json.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the structured_output_engine.py script technically, as if I am preparing to describe it in a job interview.

Cover all of these points:

1. What does the script do at a high level? What problem does it solve?
2. What is the role of the system prompt and how does it define the JSON schema?
3. What does response_mime_type="application/json" do and where exactly is it placed in the code?
4. Why is temperature set to 0 and what would happen if it were higher?
5. What does process_input() do step by step?
6. What does compare_free_text_vs_structured() demonstrate and why is it important?
7. How are token counts accessed from the response object?
8. Why are results saved to output_examples.json instead of just printed?
9. What are the failure modes handled in the script and how are they handled?
10. How would I explain this script to an interviewer in 3 sentences?

Do not rewrite the code. Only explain it clearly and technically.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Explain the Structured Output Prompt Engine module as if I am presenting it in a technical interview.

Use this exact structure:

1. What is this module? (1-2 sentences)
2. What problem does it solve? (2-3 sentences — explain why free-text output is a problem in production)
3. How did I build it? (mention: Gemini 1.5 Flash, google-generativeai, response_mime_type, temperature=0, system prompt with schema)
4. What design decisions did I make and why? (mention: temperature 0 for determinism, mime type for constraint, system prompt as schema contract)
5. What are the limitations of this approach? (mention: schema rigidity, schema versioning, model hallucinating wrong values within valid JSON)
6. How would I improve this in production? (mention: schema validation, retry logic, monitoring, database storage)
7. How does this module connect to the rest of my portfolio?

Keep the explanation precise and technically confident. No vague phrases like "it uses AI to do things."
```

---

## Prompt 6: Test Case Generation Prompt

```text
Generate 5 additional test inputs I can add to the SAMPLE_INPUTS list in structured_output_engine.py to further test the Structured Output Prompt Engine.

Requirements for the new test inputs:
1. Each input should be realistic unstructured text (1-4 sentences, not perfectly written)
2. Each should clearly belong to one of these categories: complaint, bug_report, feedback, review
3. Include at least one edge case:
   - A very short input (under 15 words) where the model might struggle to extract all fields
   - An ambiguous input that could be classified as complaint or feedback
   - An input that mentions a specific technical detail (version number, error code, or device name)
4. Each input should clearly have a different expected priority (include at least one critical and one low priority)
5. Format each input as a Python string I can add directly to the SAMPLE_INPUTS list

For each input, also show the expected JSON output so I can verify the model's response is correct.
```

---

## Prompt 7: Edge Case and Failure Mode Prompt

```text
Add the following edge case handling to structured_output_engine.py:

1. Empty input handling:
   - If process_input() receives an empty string or a string under 10 characters, do not call the API.
   - Return a dict with "error": "input_too_short", "input_text": the original text, and all other fields set to null.

2. API key missing at startup:
   - At the top of the main() function (before any API calls), check if GEMINI_API_KEY is in os.environ.
   - If not, print a helpful message: "Error: GEMINI_API_KEY environment variable not set. Get your free key at https://aistudio.google.com/app/apikey and run: export GEMINI_API_KEY=your_key"
   - Then call sys.exit(1).

3. Partial JSON response:
   - If json.loads(response.text) succeeds but the returned dict is missing one or more of the 7 expected keys, fill in the missing keys with safe defaults:
     - category: "unknown"
     - priority: "medium"
     - sentiment: "neutral"
     - summary: "No summary extracted"
     - key_issue: "No key issue extracted"
     - action_required: false
     - confidence_score: 0.0
   - Log a warning message listing which keys were missing.

4. Output file write failure:
   - Wrap the json.dump() call in a try/except for OSError and PermissionError.
   - If saving to output_examples.json fails, print the full results as a JSON string to console instead so no data is lost.

Do not change the overall structure of the script. Only add these checks inside the existing functions.
```

---

# What You Should Be Able to Explain After Session 1

By the end of the session, you should be able to answer these questions without reading the script:

1. What is structured output and why does it matter more than free-text output in production systems?
2. What does `response_mime_type="application/json"` do and where in the code does it go?
3. Why is temperature set to 0 for this module and what would change if it were 0.7?
4. What is the role of the system prompt in defining the JSON schema?
5. What is a token, and how do you access the prompt token count and completion token count from a Gemini API response?
6. What happens when `json.loads()` fails and how does the script handle it?
7. What is the difference between `json.loads()`, `json.dumps()`, and `json.dump()`?
8. What would break if you called `response.text["category"]` instead of `json.loads(response.text)["category"]`?
9. How would you add a new field to the JSON schema without breaking the existing pipeline?
10. How does this module connect to Session 2 (LLM Logging and Evaluation Tracker)?

---

## Final Session 1 Explanation

Use this when an interviewer asks: "Tell me about one of the modules in your AI portfolio."

```text
Session 1 of my AI Systems Interview Portfolio is a Structured Output Prompt Engine built with Python and Gemini 1.5 Flash. It takes unstructured customer text — complaints, support tickets, feedback forms, and product reviews — and extracts clean, predictable JSON with fields like category, priority, sentiment, summary, and action_required. I used response_mime_type="application/json" in the Gemini generation config to constrain the model to valid JSON, and set temperature to 0 to make the output deterministic and testable. This pattern is foundational to production AI pipelines where LLM output must be reliable enough to feed into downstream systems without manual parsing.
```
