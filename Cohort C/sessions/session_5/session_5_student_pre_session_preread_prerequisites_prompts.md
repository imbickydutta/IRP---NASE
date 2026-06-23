# Session 5 Student Pre-Session File: RAG Evaluation and Improvement

## What We Are Building

This is the AI Systems Interview Portfolio — Cohort C.

Each session produces one standalone Python script or notebook that demonstrates a specific AI engineering skill. The sessions are not one continuous application. They are a portfolio of modules, each showcasing a different capability you would be expected to know in an AI engineering role.

By the end of all 8 sessions, your portfolio will contain:

- `structured_output_engine.py` — prompt-to-JSON structured output
- `llm_logger.py` — LLM call logging and cost tracking
- `ai_handler.py` — serverless-style AI function with `.env` config
- `rag_pipeline.py` — document ingestion, ChromaDB, Gemini-powered Q&A
- `rag_evaluator.py` — RAG evaluation with groundedness and relevance scoring ← today
- Session 6: Agent Router — LLM-driven tool selection
- Session 7: Vision/OCR Mini Module — multimodal Gemini image understanding
- Session 8: Final System Design and Interview Demo — portfolio documentation and interview prep

## Session 5 Goal

In Session 5, you will take the RAG pipeline you built in Session 4 and evaluate it. You will measure whether it actually works — not just whether it runs without errors, but whether the answers it generates are grounded in the retrieved context and whether the retriever is fetching relevant chunks.

You will build an evaluation harness that is simple, explainable, and interview-ready.

## Session 5 Deliverable

Expected deliverable: `rag_evaluator.py` + `rag_eval_report.csv` + before/after comparison output

- `rag_evaluator.py` — evaluation script that wraps around the Session 4 RAG Pipeline (rag_pipeline.py with ChromaDB + Gemini)
- `rag_eval_report.csv` — output file with one row per test question, containing scores and failure reasons
- Before/after comparison printed to the console showing the effect of changing one pipeline parameter

---

# Pre-Read

## Why Does This Module Exist in the Portfolio?

Building a RAG pipeline is table stakes for an AI engineering role in 2024–2025. Every team that uses RAG also needs to measure whether it works. Interviewers know this. They will ask: "How do you know your RAG pipeline is returning good answers?" If you say "I tested it manually," that is a weak answer. If you say "I built an evaluation harness that tracks groundedness, relevance, and failure reasons across a test set," that is a strong answer.

This module exists in the portfolio to show you can close the loop: build → evaluate → improve. It also teaches you the vocabulary of RAG evaluation — groundedness, faithfulness, retrieval failure, generation failure — that appears in every serious AI engineering interview.

## Portfolio Module Map

```
Session 1: Structured Output Prompt Engine
     structured_output_engine.py
     ↓ (LLM output concepts feed into)
Session 2: LLM Logging and Evaluation Tracker
     llm_logger.py + llm_logs.csv
     ↓ (logging and eval mindset feeds into)
Session 3: Serverless-Style AI Function
     ai_handler.py + .env.example
     ↓ (standalone function pattern feeds into)
Session 4 — Basic RAG Pipeline (rag_pipeline.py with ChromaDB + Gemini) ←──┐
     rag_pipeline.py + chroma_db/                                            │
     ↓ (pipeline output is evaluated by)                                     │
Session 5: RAG Evaluation and Improvement  ←─── builds on Session 4
     rag_evaluator.py + rag_eval_report.csv
     ↓ (eval mindset + tool-use pattern feeds into)
Session 6 — Simple Agent Router
     agent_router.py
     ↓ (routing logic feeds into)
Session 7: Vision/OCR Mini Module
     vision_ocr_module.py + ocr_output.json
     ↓ (multimodal pattern feeds into)
Session 8: Final System Design and Interview Demo
     README.md + architecture_diagram.md + demo_script.md
```

Sessions 4 and 5 are the only pair that are directly connected — Session 5 reads from the `chroma_db/` folder that Session 4 created.

## Key Concepts to Revise

Revise these concepts before Session 5:

1. **How RAG works end-to-end** — document ingestion → chunking → embedding → vector store → query embedding → cosine similarity retrieval → context injection → LLM generation. If you are fuzzy on any step, re-read your Session 4 notes.

2. **What ChromaDB's `.query()` method returns** — it returns a dictionary with keys `ids`, `documents`, `distances`, and `metadatas`. The `documents` key contains the retrieved chunk strings. The `distances` key contains cosine distances (lower = more similar). You will use `documents` in the evaluator.

3. **Keyword overlap as a similarity metric** — the simplest way to measure text similarity without a model is to tokenize two strings into sets of words and compute the Jaccard similarity: `|A ∩ B| / |A ∪ B|`. We use a simpler version: `|A ∩ B| / |A|` (overlap relative to answer length). Know why we filter out short words (stopwords add noise).

4. **What a CSV row looks like in Python** — the `csv.DictWriter` class writes dictionaries as rows. Each dictionary key becomes a column. You write the header once, then one `writerow()` call per result dictionary.

5. **Gemini API error types** — the most common errors are `google.api_core.exceptions.ResourceExhausted` (429 rate limit) and `google.api_core.exceptions.InvalidArgument` (bad request, often caused by an empty prompt). Know how to catch these with `try/except`.

6. **The concept of test QA pairs** — an evaluation dataset is a list of `(question, expected_answer)` pairs. The expected answer is your ground truth. You do not score the LLM answer as right or wrong — you measure how much it overlaps with the retrieved context (groundedness) and how much the retrieved context overlaps with the expected answer (relevance).

7. **What `sentence-transformers` does** — `SentenceTransformer("all-MiniLM-L6-v2").encode(text)` returns a 384-dimensional numpy array. You pass this array to ChromaDB's `.query()` as the `query_embeddings` argument. The model runs fully locally — no API key, no internet required after the first download.

8. **Iterative improvement mindset** — change one variable, measure the result, compare before and after. This is controlled experimentation. In RAG: changing `top_k` changes how many chunks are retrieved. Changing chunk size changes the granularity of retrieved information. Changing the prompt template changes how the LLM uses the retrieved context.

## Technical Explanation of the Core Concept

A RAG pipeline has two stages that can fail independently. The first stage is retrieval: given a user query, does the system fetch document chunks that actually contain the relevant information? The second stage is generation: given the retrieved chunks, does the LLM produce an answer that uses that information?

We measure retrieval quality with a **relevance score**: we compare the text of the retrieved chunks against the expected answer for a test question. If the chunks contain keywords from the expected answer, retrieval quality is good. If the chunks contain irrelevant text, retrieval has failed regardless of how good the LLM is.

We measure generation quality with a **groundedness score**: we compare the generated answer text against the retrieved chunks. If the LLM's answer contains keywords that appear in the retrieved chunks, the answer is grounded in the context. If the answer introduces facts that do not appear in any retrieved chunk, the LLM is hallucinating from its pretrained knowledge — this is a groundedness failure.

The combination of these two scores gives you four diagnostic quadrants:
- High relevance + high groundedness = pipeline working correctly
- Low relevance + high groundedness = retriever failing, LLM hallucinating based on good-sounding but wrong context
- High relevance + low groundedness = retriever working, LLM ignoring context (prompt engineering problem)
- Low relevance + low groundedness = complete pipeline failure

---

# Setup Before Class

## Required pip Installs

Run these before the session. Use the same virtual environment you used for Sessions 1–4.

```bash
pip install google-generativeai
pip install chromadb
pip install sentence-transformers
pip install tabulate
```

Notes:
- `google-generativeai` must be version 0.5.0 or higher for `generation_config` support
- `chromadb` must match the version used in Session 4 — check with `pip show chromadb`
- `sentence-transformers` is ~90MB on first install and will download the `all-MiniLM-L6-v2` model (~90MB) on first use
- `tabulate` is a small utility for printing formatted tables to the console

## Gemini API Key Setup

You need a Gemini API key. It is free.

1. Go to https://aistudio.google.com
2. Click "Get API key" → "Create API key in new project"
3. Copy the key (starts with `AIza...`)
4. Set it as an environment variable:

On Mac/Linux:
```bash
export GEMINI_API_KEY="AIza..."
```

On Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=AIza...
```

To make it permanent on Mac/Linux, add the export line to your `~/.zshrc` or `~/.bashrc`.

## Verify Setup

Run this one-liner to confirm Gemini works before class:

```python
import google.generativeai as genai
import os
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
print(model.generate_content("Say hello").text)
```

You should see a short greeting printed to the console. If you see `KeyError: 'GEMINI_API_KEY'`, the environment variable is not set. If you see a 403 error, the API key is invalid.

Also confirm your ChromaDB collection from Session 4 is accessible:

```python
import chromadb
client = chromadb.PersistentClient(path="chroma_db")
print(client.list_collections())
```

You should see at least one collection listed. If the list is empty, your `chroma_db/` folder is missing or in the wrong directory.

---

# Sample Data / Content to Prepare

## Test QA Pairs for Session 5

These 5 hardcoded test questions are calibrated to a general AI/ML concepts corpus. If you ingested a different document in Session 4, you will need to write 5 questions that match your corpus. Use these as your template:

```text
Test QA Pair 1:
Question: What is the purpose of chunking in a RAG pipeline?
Expected Answer: Chunking splits long documents into smaller pieces so that the most relevant sections can be retrieved independently rather than returning an entire document.

Test QA Pair 2:
Question: What embedding model is used to convert text chunks into vectors?
Expected Answer: A sentence-transformers model such as all-MiniLM-L6-v2 converts text into 384-dimensional vectors that represent semantic meaning.

Test QA Pair 3:
Question: What is ChromaDB used for in a RAG system?
Expected Answer: ChromaDB is a vector database that stores text chunk embeddings and retrieves the most semantically similar chunks for a given query using cosine similarity.

Test QA Pair 4:
Question: What is the role of Gemini in the RAG pipeline?
Expected Answer: Gemini receives the retrieved chunks as context and generates a natural language answer to the user's question based on that context.

Test QA Pair 5:
Question: What does top-k control in a RAG retriever?
Expected Answer: Top-k controls how many of the most similar chunks are retrieved from the vector database for each query. A higher top-k returns more context but may introduce less relevant information.
```

---

# Prompts for Session 5

Use these prompts in Claude Code or Cursor when instructed during the session.

---

## Prompt 1: Main Build Prompt

```text
I am building a portfolio of AI engineering modules in Python. I am working on Session 5: RAG Evaluation and Improvement.

Portfolio context:
- Session 1: structured_output_engine.py — structured JSON output using Gemini
- Session 2: llm_logger.py — LLM call logging and evaluation tracking
- Session 3: ai_handler.py — serverless-style AI function
- Session 4: rag_pipeline.py — RAG pipeline with ChromaDB (local persistent at ./chroma_db) and Gemini 1.5 Flash

Session 5 task:
Create a file called rag_evaluator.py that evaluates the Session 4 RAG pipeline.

Technical requirements:
- LLM: Gemini 1.5 Flash using the google-generativeai library (NOT openai). Model name: "gemini-1.5-flash". Configure with: genai.configure(api_key=os.environ["GEMINI_API_KEY"])
- Embeddings: sentence-transformers library, model "all-MiniLM-L6-v2" (local, no API key). Use SentenceTransformer("all-MiniLM-L6-v2").encode(query_text) to embed queries.
- Vector DB: ChromaDB local persistent client. Use chromadb.PersistentClient(path="chroma_db") and client.get_collection(name="rag_collection") to load the existing collection from Session 4.
- Output: rag_eval_report.csv using Python's built-in csv module (csv.DictWriter)

Implement these functions with these exact signatures:

1. run_rag_query(query: str, collection, embedding_model, gemini_model, top_k: int = 3) -> dict
   - Encodes the query using the sentence-transformers embedding model
   - Queries ChromaDB collection with the query embedding and top_k
   - Formats retrieved chunks into a prompt: "Answer based only on the context below.\nContext:\n{chunks}\nQuestion: {query}\nAnswer:"
   - Calls gemini_model.generate_content(prompt).text
   - Returns dict with keys: query, retrieved_chunks (list of strings), generated_answer (string)
   - Wrap Gemini call in try/except for google.api_core.exceptions.ResourceExhausted (429). On 429, sleep 10 seconds and retry once. If retry fails, return empty string for generated_answer.

2. compute_groundedness(answer: str, retrieved_chunks: list) -> float
   - Concatenates all retrieved_chunks into one string
   - Lowercases and tokenizes both answer and chunks by splitting on whitespace and removing punctuation
   - Filters tokens shorter than 4 characters
   - Returns the fraction of unique answer tokens that also appear in the chunk tokens
   - Returns 0.0 if answer is empty or no chunks provided

3. compute_relevance(retrieved_chunks: list, expected_answer: str) -> float
   - Same keyword overlap logic as compute_groundedness but compares chunk tokens against expected_answer tokens
   - Returns fraction of unique expected_answer tokens found in chunk tokens
   - Returns 0.0 if either input is empty

4. evaluate_all(test_cases: list, collection, embedding_model, gemini_model, top_k: int = 3) -> list
   - test_cases is a list of dicts with keys: question, expected_answer
   - For each test case: call run_rag_query, compute_groundedness, compute_relevance
   - Set failure_reason = "" by default
   - If groundedness < 0.3: set failure_reason = "low_groundedness"
   - If relevance < 0.3 and failure_reason == "": set failure_reason = "low_relevance"
   - If generated_answer == "": set failure_reason = "empty_generation", set both scores to 0.0
   - If retrieved_chunks is empty: set failure_reason = "no_chunks_retrieved", set both scores to 0.0
   - Print progress: "Evaluating question {i+1}/5: {question[:50]}..."
   - Sleep 2 seconds between Gemini calls to avoid rate limit
   - Returns list of result dicts with keys: query, retrieved_chunks (joined as single string), generated_answer, expected_answer, relevance_score, groundedness_score, failure_reason

5. save_report(results: list, filename: str = "rag_eval_report.csv") -> None
   - Writes results list to CSV using csv.DictWriter
   - Columns: query, retrieved_chunks, generated_answer, expected_answer, relevance_score, groundedness_score, failure_reason
   - Print: "Report saved to {filename}"

6. compare_runs(results_before: list, results_after: list, param_changed: str) -> None
   - Prints a before/after comparison table to console
   - For each question: print query (truncated to 40 chars), before groundedness, after groundedness, before relevance, after relevance, delta groundedness, delta relevance
   - Print average scores for before and after runs
   - Print: "Parameter changed: {param_changed}"

In the main block (if __name__ == "__main__":):
- Initialize ChromaDB client and load collection
- Initialize sentence-transformers embedding model
- Initialize Gemini model
- Define 5 hardcoded test_cases (use the AI/ML RAG concepts QA pairs below)
- Run evaluate_all with top_k=2 — this is the "before" run
- Save report to rag_eval_report.csv
- Run evaluate_all with top_k=5 — this is the "after" run
- Save report to rag_eval_report_improved.csv
- Call compare_runs(results_before, results_after, "top_k: 2 → 5")

Test QA pairs to hardcode:
1. Q: "What is the purpose of chunking in a RAG pipeline?" A: "Chunking splits long documents into smaller pieces so that the most relevant sections can be retrieved independently rather than returning an entire document."
2. Q: "What embedding model is used to convert text chunks into vectors?" A: "A sentence-transformers model such as all-MiniLM-L6-v2 converts text into 384-dimensional vectors that represent semantic meaning."
3. Q: "What is ChromaDB used for in a RAG system?" A: "ChromaDB is a vector database that stores text chunk embeddings and retrieves the most semantically similar chunks for a given query using cosine similarity."
4. Q: "What is the role of Gemini in the RAG pipeline?" A: "Gemini receives the retrieved chunks as context and generates a natural language answer to the user's question based on that context."
5. Q: "What does top-k control in a RAG retriever?" A: "Top-k controls how many of the most similar chunks are retrieved from the vector database for each query."

Add a comment above every function explaining what it does and why.
Add inline comments explaining every non-obvious line.
Do NOT use: openai library, RAGAS, LangChain, HuggingFace Inference API, Streamlit, FastAPI, pytest, or any paid API.
Do NOT add a web interface.
Keep the script to a single file.
```

---

## Prompt 2: Improvement Prompt

```text
Improve rag_evaluator.py with the following changes:

1. Better tokenization in compute_groundedness and compute_relevance:
   - Use Python's re module to remove all non-alphanumeric characters before splitting
   - Also filter out common English stopwords: ["the", "is", "in", "and", "of", "to", "a", "that", "for", "with", "are", "was", "it"]
   - This will give cleaner keyword overlap scores

2. Better progress output in evaluate_all:
   - Print groundedness and relevance scores immediately after each question is evaluated
   - Format: "  → Groundedness: {score:.2f} | Relevance: {score:.2f} | Failure: {failure_reason or 'none'}"

3. Add a run_timestamp to each result row:
   - Import datetime and add a "run_timestamp" key to each result dict
   - Format: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   - Update save_report to include this column

4. Add a summary print at the end of evaluate_all:
   - Print average groundedness and average relevance across all 5 questions
   - Print count of questions with failure_reason != ""

5. In compare_runs, use the tabulate library for formatted output:
   - from tabulate import tabulate
   - Format the comparison as a table with headers: Query, Before G, After G, Delta G, Before R, After R, Delta R
   - Use tabulate(rows, headers=headers, tablefmt="grid")

Do not change the function signatures or the main block logic.
```

---

## Prompt 3: Debugging Prompt — Specific Failures for This Module

```text
My rag_evaluator.py is failing. Here is the error:

[PASTE YOUR ACTUAL ERROR HERE]

Common errors and what to check:

Error 1: ValueError: Collection rag_collection does not exist.
Fix needed: The collection name in rag_evaluator.py must match exactly what was used in rag_pipeline.py. Check Session 4 code for the collection name. Use client.list_collections() to see what collections exist.

Error 2: google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted
Fix needed: Add time.sleep(10) before retrying. Also add time.sleep(2) between each of the 5 question evaluations. The Gemini free tier allows approximately 60 requests per minute.

Error 3: All groundedness scores are 0.0
Fix needed: The compute_groundedness function is likely comparing strings without lowercasing. Make sure both answer and chunk text are lowercased before tokenizing. Check: answer.lower() and "".join(chunks).lower()

Error 4: rag_eval_report.csv has only 1 row of data
Fix needed: save_report is probably being called inside the evaluation loop instead of after it. Move the save_report call outside the loop, after all 5 results are collected.

Error 5: sentence_transformers not found or SentenceTransformer model download hangs
Fix needed: Run "pip install sentence-transformers" in the correct virtual environment. The first run downloads ~90MB — wait at least 2 minutes before assuming it is frozen.

Please diagnose my specific error above and fix the code. Explain what was wrong and what you changed.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain rag_evaluator.py to me as if I am preparing for a technical interview.

For each function, explain:
1. What are its inputs and outputs?
2. What does it do step by step?
3. Why was it implemented this way instead of an alternative approach?
4. What could go wrong and how is it handled?

Also explain:
- Why we use sentence-transformers for query encoding instead of the Gemini embedding API
- Why keyword overlap is used instead of an LLM judge for scoring
- What the difference between groundedness_score and relevance_score tells you about the pipeline
- What the failure_reason column is used for in a production context
- Why we change top_k from 2 to 5 in the before/after comparison and what the expected effect is

Do not rewrite the code. Only explain it.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Help me explain the rag_evaluator.py module to an interviewer in a technical discussion.

Structure the explanation as follows:

1. What problem does this module solve? (1-2 sentences)
2. What are the two core metrics it measures and what do they mean?
3. How is groundedness computed? (be specific about the implementation)
4. How is relevance computed? (be specific about the implementation)
5. What does the failure_reason field tell you?
6. What is the before/after comparison showing?
7. What are the limitations of this approach? (at least 3 honest trade-offs)
8. How would you improve this in a production system?
9. Why did you not use RAGAS or an LLM judge?

Keep the explanation technical but clear. Avoid vague statements like "it evaluates the RAG pipeline." Instead, explain the specific mechanism.
```

---

## Prompt 6: Test Case Generation Prompt

```text
Generate 5 additional test QA pairs for rag_evaluator.py.

The test QA pairs should be about the same AI/ML RAG concepts corpus (chunking, embeddings, vector databases, retrieval, generation).

For each test case, provide:
- question: a realistic question a user might ask
- expected_answer: a 1-2 sentence ground truth answer that uses keywords specific to the topic

Requirements:
- The questions should vary in type: some factual, some comparative, some "how" questions
- The expected answers should be specific enough that keyword overlap scoring will be meaningful
- Avoid yes/no questions
- Do not repeat the 5 questions already in the script

Format each as a Python dict:
{"question": "...", "expected_answer": "..."}
```

---

## Prompt 7: Edge Case and Failure Mode Prompt

```text
Add edge case handling to rag_evaluator.py for the following failure scenarios:

1. ChromaDB returns an empty documents list for a query:
   - In run_rag_query: if collection.query() returns empty documents, return retrieved_chunks=[] and generated_answer=""
   - In evaluate_all: detect this and set failure_reason = "no_chunks_retrieved", set both scores to 0.0, skip the Gemini call entirely

2. Gemini returns an empty string or None:
   - In run_rag_query: if model.generate_content(prompt).text is None or stripped to empty, return ""
   - In evaluate_all: detect empty generated_answer and set failure_reason = "empty_generation"

3. The chroma_db folder does not exist:
   - Before initializing the ChromaDB client, check if the path exists using os.path.exists("chroma_db")
   - If it does not exist, print a helpful error: "Error: chroma_db folder not found. Please run rag_pipeline.py from Session 4 first to create the ChromaDB collection."
   - Exit with sys.exit(1)

4. GEMINI_API_KEY environment variable is not set:
   - Check os.environ.get("GEMINI_API_KEY") at the top of the main block
   - If None, print: "Error: GEMINI_API_KEY environment variable not set. Set it with: export GEMINI_API_KEY=your_key"
   - Exit with sys.exit(1)

5. rag_eval_report.csv already exists from a previous run:
   - Before writing, check if the file exists using os.path.exists(filename)
   - If it exists, rename it to rag_eval_report_backup_{timestamp}.csv using os.rename()
   - Print: "Previous report backed up to {backup_filename}"

Add all these checks without changing the function signatures.
```

---

# What You Should Be Able to Explain After Session 5

By the end of the session, you should be able to answer these questions without reading your notes:

1. What is groundedness and how did you measure it in your script?
2. What is relevance in the context of RAG evaluation and how is it different from groundedness?
3. If relevance is high but groundedness is low, what does that tell you about your RAG pipeline?
4. What does the `failure_reason` column tell you in `rag_eval_report.csv`?
5. Why did you use keyword overlap instead of an LLM judge to score the answers?
6. What did you change in the before/after comparison and what effect did it have on the scores?
7. What are the limitations of keyword overlap as an evaluation metric?
8. How would you explain the `compute_groundedness()` function to a technical interviewer?
9. Why must the embedding model in `rag_evaluator.py` match the model used in `rag_pipeline.py`?
10. What is the difference between a retrieval failure and a generation failure in a RAG pipeline?

---

## Final Session 5 Explanation

Use this explanation when asked to describe this module in an interview:

```text
In Session 5, I built an evaluation harness for the RAG pipeline I created in Session 4. The evaluator runs 5 test questions through the pipeline and measures two metrics: relevance, which checks whether the retrieved chunks contain keywords from the expected answer, and groundedness, which checks whether the generated answer contains keywords from the retrieved chunks. Both metrics use keyword overlap computed with pure Python — no LLM judge needed. The results are saved to a CSV with a failure_reason column that categorizes low-scoring answers as retrieval failures, generation failures, or API errors. I then changed the top-k parameter from 2 to 5 and reran the evaluation, printing a before/after comparison to show the trade-off between context coverage and precision.
```
