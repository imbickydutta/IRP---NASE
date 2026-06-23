# Session 8 Student Pre-Session File: Final System Design and Interview Demo

## What We Are Building

This is the final session of the AI Systems Interview Portfolio (Cohort C).

Across Sessions 1–7, you built seven standalone Python modules. Each one demonstrates a different skill area of AI engineering:

- Session 1: Structured output with Gemini
- Session 2: LLM logging and evaluation tracking
- Session 3: Serverless-style AI function
- Session 4: RAG pipeline with ChromaDB
- Session 5: RAG evaluation and improvement
- Session 6: Simple agent router
- Session 7: Vision/OCR with multimodal Gemini

Today you are not building a new module. You are wrapping all seven into a professional, interview-ready portfolio.

## Session 8 Goal

By the end of Session 8, you will have:

- A README.md that explains your full portfolio to anyone who opens your folder
- An architecture_diagram.md showing how all 7 modules connect
- A demo_script.md: a 2-minute spoken pitch you can deliver in an interview
- A viva_prep.md: 15 interview questions with model answers covering all modules
- A module_summary.md: one-page reference table for all 7 modules
- A limitations.md: honest, specific production failure analysis for each module

## Session 8 Deliverables

```
README.md
architecture_diagram.md
demo_script.md
viva_prep.md
module_summary.md
limitations.md
```

These files live alongside your existing Python scripts. They do not replace the scripts — they document them.

---

## Cross-Session Reference

**Previous session:** Session 7 — Vision/OCR Mini Module (all 7 portfolio modules built)

**Next session:** None — this is the final session

---

# Pre-Read

## Why Does This Module Exist in the Portfolio?

Most students who complete technical AI projects struggle to present them in interviews. They built something real, but they cannot answer: "Walk me through the architecture." or "What would break if this system had 10,000 users?"

Session 8 fixes this. It forces you to look at your own portfolio from the outside — as an interviewer would see it — and produce documentation that communicates your engineering thinking, not just your code.

A working script without documentation tells an interviewer: "I can code." A documented portfolio with an architecture diagram, limitations analysis, and demo script tells an interviewer: "I think like an engineer."

## Portfolio Module Map

The diagram below shows all 8 sessions and which ones are connected:

```
Session 1: Structured Output Prompt Engine
  structured_output_engine.py + output_examples.json
  (standalone — introduces Gemini structured output)
         |
         | (logging pattern reused)
         v
Session 2: LLM Logging and Evaluation Tracker
  llm_logger.py + llm_logs.csv + eval_summary.json
  (standalone — adds observability to any Gemini call)
         |
         | (handler pattern reused)
         v
Session 3: Serverless-Style AI Function
  ai_handler.py + .env.example + local test output
  (standalone — simulates cloud function design)
         |
         | (Gemini call pattern + .env pattern carried forward)
         v
Session 4: Basic RAG Pipeline  <-----------------+
  rag_pipeline.py + chroma_db/ (shared)          |
  (depends on: sentence-transformers, ChromaDB)  |
         |                                        |
         | (shares ChromaDB collection)           |
         v                                        |
Session 5: RAG Evaluation and Improvement        |
  rag_evaluator.py + rag_eval_report.csv         |
  (depends on: Session 4's ChromaDB collection)  |
         |                                        |
         | (evaluation pattern)                   |
         v                                        |
Session 6: Simple Agent Router                   |
  agent_router.py + test_queries output          |
  (standalone — uses Gemini intent classification)|
         |                                        |
         v                                        |
Session 7: Vision/OCR Mini Module                |
  vision_ocr_module.py + sample_image + ocr_output.json
  (standalone — uses Gemini multimodal input)
         |
         v
Session 8: Final System Design and Interview Demo  <-- YOU ARE HERE
  README.md + architecture_diagram.md + demo_script.md
  + viva_prep.md + module_summary.md + limitations.md
  (consolidation — no new Python feature)
```

Key architectural dependency: Session 4 and Session 5 share the same local ChromaDB collection. Session 4 must be run before Session 5. All other sessions are standalone.

## Key Concepts to Revise Before This Session

Revise these concepts before class. You will be asked about them in viva practice:

**1. RAG vs Fine-Tuning**
RAG retrieves relevant documents at inference time and injects them into the prompt. Fine-tuning changes the model's weights using a training dataset. RAG is better when knowledge changes frequently. Fine-tuning is better when you need consistent style or a specialized task.

**2. Embedding Dimensions**
The sentence-transformers all-MiniLM-L6-v2 model produces 384-dimensional vectors. Each chunk of text is converted to a 384-element float array. Cosine similarity is computed between the query embedding and stored chunk embeddings to find the most relevant chunks.

**3. ChromaDB Persistence**
ChromaDB stores embedding collections in a local folder (chroma_db/). You create a client with chromadb.PersistentClient(path="./chroma_db") and add documents with collection.add(). Querying uses collection.query(query_embeddings=..., n_results=...).

**4. Gemini 1.5 Flash API Call Pattern**
```python
import google.generativeai as genai
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("your prompt here")
print(response.text)
```

**5. Structured Output with Gemini**
Pass response_mime_type="application/json" inside generation_config to get JSON output:
```python
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"response_mime_type": "application/json"}
)
```

**6. Serverless Function Pattern**
A serverless-style handler accepts an event dict and returns a response dict. No running server is needed. This pattern maps directly to AWS Lambda or Google Cloud Functions with minimal modification.

**7. LLMOps Observability**
Observability means logging what went into the LLM, what came out, how long it took, and whether the output was good. In Session 2, this was done with a CSV log and a JSON summary file. In production, tools like LangSmith, Helicone, or Weights & Biases provide this.

**8. Production vs Prototype Trade-offs**
A prototype runs locally with one user. A production system handles concurrent users, has authentication, rate limiting, retry logic, fallback responses, monitoring dashboards, and cost controls. You must be able to name the gap between what you built and what production would require.

## Technical Explanation of the Core Concept

Session 8 is about AI system design communication. This means being able to explain an AI system at three levels:

**Level 1 — Component level**: What does each piece do? (Module name, function, input, output, library used)

**Level 2 — Architecture level**: How do the pieces connect? (Data flow, shared dependencies, sequential vs parallel execution, API vs local computation)

**Level 3 — Production level**: What would break? How would you scale it? What would you add? What would it cost?

Most candidates in interviews can only answer at Level 1. A strong AI engineering candidate can move fluidly between all three levels. Session 8 prepares you for Level 2 and Level 3.

---

# Setup Before Class

## Required pip Installs

You should already have these installed from previous sessions. Verify each one:

```bash
pip install google-generativeai
pip install sentence-transformers
pip install chromadb
pip install python-dotenv
pip install pillow
```

There are no new package installs for Session 8. This session produces Markdown documents, not Python scripts.

## Gemini API Key Setup

If you do not have your Gemini API key set up:

1. Go to https://aistudio.google.com
2. Sign in with your Google account
3. Click "Get API Key" and create a new key
4. Copy the key
5. In your project folder, open or create a .env file and add:

```
GEMINI_API_KEY=your_key_here
```

6. In any Python script, load it with:

```python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.environ["GEMINI_API_KEY"]
```

## Verify Setup: One-Line Test

Run this in a Python file or notebook cell to confirm Gemini works:

```python
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Say: Gemini is working.")
print(response.text)
```

Expected output: a sentence confirming Gemini is working. If you see a 403 or 429 error, check that your API key is correct and that you have not exceeded the free-tier daily limit.

---

# Sample Data / Content to Prepare

Before class, collect the following information in a text file. You will use it to personalise your README.md and demo_script.md:

```
My name:

My Session 1 output file name:

My Session 2 log file location:

My Session 3 .env.example contents:

My Session 4 ChromaDB folder path:

My Session 5 eval report file name:

My Session 6 test queries (at least 3):

My Session 7 sample image file name:

One thing I found hardest to build (for the demo script):

One production improvement I would make (for the demo script):
```

This preparation will save time in class and make your documentation specific to your actual work rather than generic.

---

# Prompts for Session 8

Use these prompts during the session when the instructor directs you to. All prompts are copy-paste ready for Claude Code or Cursor.

---

## Prompt 1: Portfolio README Prompt

```text
Generate a complete README.md file for my AI Systems Interview Portfolio.

The portfolio contains 7 standalone Python modules built across 8 sessions. All LLM calls use Gemini 1.5 Flash via the google-generativeai library. Embeddings use sentence-transformers all-MiniLM-L6-v2 (local, 384-dimensional vectors). Vector storage uses ChromaDB local persistent mode.

The README.md must include the following sections:

1. Title: AI Systems Interview Portfolio
2. One-paragraph overview of the portfolio and its purpose for AI engineering interview preparation
3. Technology Stack table with columns: Component | Library | Version/Model | Notes
   Include rows for: LLM (Gemini 1.5 Flash, google-generativeai), Embeddings (all-MiniLM-L6-v2, sentence-transformers), Vector DB (ChromaDB, local persistent), Environment (python-dotenv), Image Processing (Pillow)
4. Portfolio Modules section listing all 7 modules in a table with columns:
   Session | Module Name | Python File | Output File(s) | Core Concept
   Session 1: Structured Output Prompt Engine | structured_output_engine.py | output_examples.json | Gemini structured JSON output
   Session 2: LLM Logging and Evaluation Tracker | llm_logger.py | llm_logs.csv, eval_summary.json | LLMOps observability
   Session 3: Serverless-Style AI Function | ai_handler.py | .env.example | Serverless function pattern
   Session 4: Basic RAG Pipeline | rag_pipeline.py | chroma_db/ | Retrieval-Augmented Generation
   Session 5: RAG Evaluation and Improvement | rag_evaluator.py | rag_eval_report.csv | RAG quality evaluation
   Session 6: Simple Agent Router | agent_router.py | test_queries output | LLM-based intent routing
   Session 7: Vision/OCR Mini Module | vision_ocr_module.py | ocr_output.json | Multimodal LLM input
5. Folder Structure section showing the expected directory layout with all scripts and output files
6. Gemini API Setup section with step-by-step instructions: get key from aistudio.google.com, set GEMINI_API_KEY in .env file, install google-generativeai, verify with a one-line test
7. Installation section with pip install commands for all required libraries
8. How to Run Each Module section with one-line run instructions per script
9. Important Notes section mentioning: Sessions 4 and 5 share the same ChromaDB collection and must be run in order; all modules are standalone Python scripts, no server required; the free-tier Gemini API has a rate limit of 60 requests per minute
10. Portfolio Architecture section with a brief paragraph describing how the modules relate to each other

Output only the raw Markdown content for README.md. Do not add any explanation outside the file content.
```

---

## Prompt 2: Architecture Diagram Prompt

```text
Generate a complete architecture_diagram.md file for my AI Systems Interview Portfolio.

The portfolio has 7 modules. Create a Mermaid diagram that shows how they connect.

Requirements for the diagram:
- Use Mermaid graph TD (top-down) syntax
- Label each of the 7 modules as a node with its session number and Python filename
- Show Gemini 1.5 Flash as a shared external API node that all 6 LLM-calling modules connect to (Sessions 1, 2, 3, 4, 5, 6, 7 all call Gemini)
- Show sentence-transformers all-MiniLM-L6-v2 as a local embedding node connected to Sessions 4 and 5
- Show ChromaDB as a shared local persistent store connected to Sessions 4 and 5
- Show a dependency arrow from Session 4 to Session 5 labeled "shares chroma_db/ collection"
- Use different arrow styles for API calls (-->>) versus local operations (-->)
- Add a legend section explaining the arrow types

After the Mermaid diagram, include a written section called "Data Flow Walkthrough" that traces the data flow for each of the 7 modules in one paragraph each:
- What is the input?
- What processing happens (local vs API)?
- What is the output file or structure?

Also include a section called "Module Dependencies" that explicitly states:
- Session 4 must be run before Session 5
- All other sessions are independent
- All sessions require GEMINI_API_KEY in the .env file
- Sessions 4 and 5 additionally require sentence-transformers and chromadb installed

Output only the raw Markdown content for architecture_diagram.md.
```

---

## Prompt 3: Demo Script Prompt

```text
Write a complete demo_script.md for my AI Systems Interview Portfolio.

This is a spoken 2-minute script (approximately 280-320 words) that I will deliver verbally in an interview when asked to walk through my portfolio.

The script must follow this structure:

Opening (20 seconds): One sentence introducing the portfolio by name and purpose. One sentence on the technology stack used (Gemini 1.5 Flash, sentence-transformers, ChromaDB, Python).

Module Walk (90 seconds): One sentence per module covering all 7:
- Session 1: Structured Output Prompt Engine — what it does and the output format
- Session 2: LLM Logging and Evaluation Tracker — what it logs and why it matters for LLMOps
- Session 3: Serverless-Style AI Function — what the function pattern is and how it maps to cloud
- Session 4: Basic RAG Pipeline — what RAG does and what ChromaDB stores
- Session 5: RAG Evaluation — how it measures quality and what rag_eval_report.csv contains
- Session 6: Agent Router — how it classifies intent and dispatches to tools
- Session 7: Vision/OCR — how Gemini handles the image and what ocr_output.json contains

Production Awareness (20 seconds): One sentence naming a production limitation of the portfolio (e.g., ChromaDB local persistence, lack of retry logic, free-tier rate limits). One sentence on what you would add for production (e.g., managed vector store, request logging, fallback responses).

Closing (10 seconds): One sentence on what this portfolio demonstrates about your ability to build and explain AI systems.

Format the script as a markdown file with:
- A title: "2-Minute Portfolio Demo Script"
- Labeled time sections (Opening, Module Walk, Production Awareness, Closing)
- The spoken text in plain paragraphs (not bullet points)
- A word count at the bottom
- A "Delivery Tips" section at the end with 4 practical tips for delivering this live

Output only the raw Markdown content for demo_script.md.
```

---

## Prompt 4: Viva Prep Prompt

```text
Generate a complete viva_prep.md file containing 15 interview Q&A pairs for my AI Systems Interview Portfolio.

Portfolio details:
- 7 modules built in Python
- LLM: Gemini 1.5 Flash via google-generativeai library
- Embeddings: sentence-transformers all-MiniLM-L6-v2, 384-dimensional vectors
- Vector DB: ChromaDB local persistent mode, chromadb.PersistentClient
- Sessions 4 and 5 share a ChromaDB collection
- Structured output uses response_mime_type="application/json" in generation_config
- LLM logger writes to llm_logs.csv and produces eval_summary.json
- Agent router uses LLM-based intent classification returning a JSON dict
- Vision module passes PIL Image objects to model.generate_content()
- No OpenAI, no LangChain, no FastAPI, no frontend

The 15 questions must cover:
Questions 1-3: Portfolio overview and purpose
Questions 4-6: RAG pipeline specifics (chunking, embeddings, ChromaDB queries)
Questions 7-9: Structured output and Gemini API usage
Questions 10-11: LLM logging and evaluation approach
Questions 12-13: Agent routing and intent classification design
Question 14: RAG vs fine-tuning — when to use each
Question 15: Production readiness — what would you change for a real deployment

For each question, provide:
- The question text
- A model answer that is 3-5 sentences, technically specific, names actual library names and function names where relevant, and includes at least one honest limitation or trade-off

Format as a numbered list with clearly labeled "Question:" and "Model Answer:" for each item.

Output only the raw Markdown content for viva_prep.md.
```

---

## Prompt 5: Module Summary Prompt

```text
Generate a complete module_summary.md file for my AI Systems Interview Portfolio.

This is a one-page reference document that I can use during interview prep.

Create a single Markdown table with the following 8 columns:
Session | Module Name | Core Concept | Python File | Key Library | Output File | Key Function | One-Line Limitation

Fill in all 7 rows with accurate information:

Session 1 | Structured Output Prompt Engine | Gemini structured JSON output | structured_output_engine.py | google-generativeai | output_examples.json | generate_structured_output() | No schema validation on Gemini's JSON response
Session 2 | LLM Logging and Evaluation Tracker | LLMOps observability | llm_logger.py | csv, json | llm_logs.csv, eval_summary.json | log_llm_call(), generate_eval_summary() | Scoring is heuristic, not human-annotated
Session 3 | Serverless-Style AI Function | Stateless handler pattern | ai_handler.py | python-dotenv, google-generativeai | local test output | handle_event() | No real cloud deployment, no auth
Session 4 | Basic RAG Pipeline | Retrieval-Augmented Generation | rag_pipeline.py | sentence-transformers, chromadb | chroma_db/ folder | ingest_documents(), retrieve_and_generate() | Fixed-size chunking splits semantic units
Session 5 | RAG Evaluation and Improvement | Retrieval quality scoring | rag_evaluator.py | sentence-transformers, chromadb | rag_eval_report.csv | evaluate_rag_response() | Automated scoring does not replace human judgment
Session 6 | Simple Agent Router | LLM-based intent classification | agent_router.py | google-generativeai | test_queries output | classify_intent(), route_to_tool() | Single-hop routing only, no memory
Session 7 | Vision/OCR Mini Module | Multimodal LLM input | vision_ocr_module.py | Pillow, google-generativeai | ocr_output.json | extract_text_from_image() | Quality depends on image resolution

Below the table, include a section called "Architecture Notes" with 5 bullet points covering the most important cross-module observations:
- Which modules share dependencies
- What the common Gemini call pattern is
- Where ChromaDB is used and by which sessions
- The embedding model used and its vector dimensions
- The one production gap common to all modules

Output only the raw Markdown content for module_summary.md.
```

---

## Prompt 6: Limitations and Production Notes Prompt

```text
Generate a complete limitations.md file for my AI Systems Interview Portfolio.

For each of the 7 modules, write a detailed limitations section covering:
1. What the module currently does NOT handle
2. What would break if 100+ users used this system concurrently
3. What a production version of this module would add or change
4. Estimated latency for one call (local operations vs Gemini API call)
5. Safety consideration: what could go wrong with untrusted input

Modules to cover:
- Session 1: structured_output_engine.py
- Session 2: llm_logger.py
- Session 3: ai_handler.py
- Session 4: rag_pipeline.py
- Session 5: rag_evaluator.py
- Session 6: agent_router.py
- Session 7: vision_ocr_module.py

After all 7 modules, include a section called "Cross-Module Production Considerations" covering:
- Rate limiting: Gemini free tier is 60 RPM; how to handle 429 errors with exponential backoff
- Cost estimation: Gemini 1.5 Flash pricing is approximately $0.075 per 1M input tokens and $0.30 per 1M output tokens (as of the model's availability period); estimate per-call cost for each module
- Monitoring: what metrics to track across all modules
- Security: prompt injection risk in all modules that accept user text input; PII risk in logging modules
- Scalability path: local ChromaDB to managed vector store migration path

Format each module section with a clear H2 heading. Use bullet points for each of the 5 sub-items. Be specific — name actual ChromaDB methods, actual Gemini parameters, actual error types.

Output only the raw Markdown content for limitations.md.
```

---

## Prompt 7: Cost and Latency Analysis Prompt

```text
Generate a cost and latency analysis section that can be appended to limitations.md.

Analyze each of the 7 portfolio modules for:

1. Approximate latency breakdown:
   - Local compute time (embedding generation with sentence-transformers, image loading with Pillow, CSV write)
   - Gemini 1.5 Flash API call time (typical range: 1-4 seconds for short prompts)
   - Total estimated latency per user request

2. Approximate token count per call:
   - Input tokens: prompt length + any retrieved chunks or image description
   - Output tokens: typical response length for each module's task
   - Use Gemini 1.5 Flash pricing: ~$0.075 per 1M input tokens, ~$0.30 per 1M output tokens

3. Cost at scale:
   - Cost per 1,000 calls
   - Cost per 100,000 calls per month
   - Compare free tier limits vs paid tier

4. Optimization opportunities:
   - Where caching would help (e.g., repeated query embeddings, same document chunks)
   - Where batching would reduce latency (e.g., evaluating multiple RAG queries together)
   - Where a smaller model could replace Gemini (e.g., local model for intent classification)

Format as a markdown table per module with columns: Module | Avg Latency | Input Tokens | Output Tokens | Cost per 1K calls | Top Optimization.

Be specific about what contributes to latency in each module. For Session 4, note that sentence-transformers encode() adds approximately 50-200ms depending on text length and hardware.

Output only the raw Markdown content to be appended to limitations.md.
```

---

# What You Should Be Able to Explain After Session 8

By the end of the session, you should be able to answer these questions without looking at notes:

1. What are the 7 modules in your portfolio and what does each one do in one sentence?
2. Which two sessions share a ChromaDB collection, and why must they run in order?
3. What is the name of the Gemini model used across this portfolio, and how is it instantiated in Python?
4. What embedding model is used, how many dimensions does it produce, and what library provides it?
5. What is the difference between RAG and fine-tuning, and when would you choose each?
6. What is one specific production failure mode for the RAG pipeline, and how would you fix it?
7. What does response_mime_type="application/json" do in a Gemini generation_config, and why is it used?
8. How would you add retry logic to handle a 429 rate limit error from the Gemini API?
9. What is the difference between a prototype architecture and a production architecture for an AI system?
10. If an interviewer asks "what would break if 1000 users used this simultaneously?", what is your answer for the RAG pipeline specifically?

---

## Final Session 8 Explanation

Memorise and practise this explanation before your next interview:

```text
I built a 7-module AI Systems Interview Portfolio in Python. The modules cover structured LLM output, LLM observability logging, serverless AI function design, RAG pipeline construction, RAG quality evaluation, LLM-based agent routing, and multimodal vision input. All LLM calls use Gemini 1.5 Flash via the google-generativeai library. Embeddings are generated locally with sentence-transformers all-MiniLM-L6-v2, which produces 384-dimensional vectors stored in a local ChromaDB collection. Each module is a standalone Python script with documented inputs, outputs, and limitations. I can walk through the full architecture, explain every design decision, and discuss what a production version would require in terms of scaling, monitoring, cost control, and safety.
```
