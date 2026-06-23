# Session 5 After-Session Notes: RAG Evaluation and Improvement

## What We Built Today

In Session 5, we built `rag_evaluator.py` — a standalone evaluation harness that wraps around the Session 4 RAG pipeline and measures whether it produces grounded, relevant answers.

Deliverables produced this session: `rag_evaluator.py` + `rag_eval_report.csv` + before/after comparison output

- `rag_evaluator.py` — evaluation script with 6 functions: `run_rag_query`, `compute_groundedness`, `compute_relevance`, `evaluate_all`, `save_report`, `compare_runs`
- `rag_eval_report.csv` — per-question scores with columns: `query`, `retrieved_chunks`, `generated_answer`, `expected_answer`, `relevance_score`, `groundedness_score`, `failure_reason`
- `rag_eval_report_improved.csv` — same evaluation re-run after changing `top_k` from 2 to 5
- Console output showing the before/after comparison table with score deltas per question

---

# Why This Module Matters for AI Engineering Interviews

Building a RAG pipeline is expected. Knowing whether your RAG pipeline works — and being able to prove it — is what differentiates a junior candidate from a strong mid-level one.

Interviewers at AI-forward companies ask questions like:
- "How do you validate that your RAG system isn't hallucinating?"
- "How would you detect retrieval failures versus generation failures?"
- "What metrics do you track for a RAG pipeline in production?"

If you built only Session 4, you can answer the first question. If you also built Session 5, you can answer all three with specific implementation details. You can name the metrics (groundedness, relevance), describe how they are computed (keyword overlap), show the output format (CSV with failure_reason column), and describe an improvement workflow (before/after comparison with a controlled parameter change).

This module also demonstrates engineering discipline: you did not just ship a pipeline, you closed the loop with measurement.

---

# Portfolio Module Map

```
Session 1: Structured Output Prompt Engine          [DONE]
  structured_output_engine.py + output_examples.json
  ↓
Session 2: LLM Logging and Evaluation Tracker       [DONE]
  llm_logger.py + llm_logs.csv + eval_summary.json
  ↓
Session 3: Serverless-Style AI Function             [DONE]
  ai_handler.py + .env.example
  ↓
Session 4 — Basic RAG Pipeline (rag_pipeline.py with ChromaDB + Gemini) [DONE]  ←──┐
  rag_pipeline.py + chroma_db/                                                       │
  ↓                                                                                  │ (directly connected)
Session 5: RAG Evaluation and Improvement                              [DONE]  ──────┘
  rag_evaluator.py + rag_eval_report.csv
  ↓
Session 6 — Simple Agent Router                                        [NEXT]
  agent_router.py
  ↓
Session 7: Vision/OCR Mini Module
  vision_ocr_module.py + ocr_output.json
  ↓
Session 8: Final System Design and Interview Demo
  README.md + architecture_diagram.md + demo_script.md
```

Sessions 4 and 5 are the only pair in the portfolio with a hard dependency. Session 5 reads the `chroma_db/` folder that Session 4 wrote. All other sessions are fully standalone.

---

# Technical Deep-Dive: RAG Evaluation, Groundedness, Faithfulness, Retrieval Failure Analysis, and Iterative Improvement

## How the Evaluation Works

The `rag_evaluator.py` script runs a fixed set of 5 test question-answer pairs through the existing RAG pipeline and scores each output on two dimensions. For each question, it calls `run_rag_query()`, which encodes the query using `sentence-transformers` (`all-MiniLM-L6-v2`), queries ChromaDB with the encoded vector to retrieve the top-k most similar document chunks, assembles those chunks into a context-injection prompt, and sends the prompt to Gemini 1.5 Flash for generation.

The scoring functions use token-level keyword overlap — not semantic similarity, not an LLM judge. `compute_groundedness()` tokenizes the generated answer and the concatenated retrieved chunks, filters out short tokens (below 4 characters) to reduce stopword noise, and returns the fraction of unique answer tokens that also appear in the chunk tokens. A score close to 1.0 means the LLM's answer is built almost entirely from words that appeared in the context. A score near 0.0 means the answer is composed of words that were not in the retrieved context, which is the fingerprint of hallucination. `compute_relevance()` applies the same logic in the other direction: it compares the retrieved chunk tokens against the expected answer tokens, measuring how much of the expected answer's vocabulary was present in what the retriever returned.

## Why Keyword Overlap Instead of an LLM Judge

Keyword overlap is a weak proxy for semantic similarity — two paraphrased sentences may have very low keyword overlap while conveying identical meaning. However, it is free, instantaneous, deterministic, and fully explainable. RAGAS and similar frameworks use an LLM to score each answer, which adds API latency and cost to every evaluation run and introduces a black box: if the judge gives a score of 3/5, it is not always clear why. In a portfolio context and in early-stage production systems, the ability to explain every step of your evaluation is more valuable than marginally better scoring accuracy. The goal of this module is to teach the concept and the habit — the specific scoring mechanism can be upgraded later.

## The Iterative Improvement Mindset

The before/after comparison is not just a feature — it is a philosophy. We change exactly one variable (`top_k` from 2 to 5) and re-run the identical 5 test questions. The `compare_runs()` output shows the score delta per question. This is a controlled experiment. In production RAG systems, teams iterate the same way: freeze the test set, change one parameter, measure the delta. Common parameters to tune are chunk size (affects the granularity and coherence of retrieved passages), `top_k` (affects context coverage versus noise), overlap between chunks during ingestion (affects whether a sentence that spans a chunk boundary is ever retrieved fully), and the prompt template (affects whether the LLM uses the context or ignores it). Changing multiple variables simultaneously makes it impossible to attribute score changes to specific causes.

---

# What Students Should Understand

Students who complete Session 5 should be able to explain and defend each of the following points:

1. **Groundedness is not the same as accuracy.** A grounded answer means the answer is anchored in the retrieved context. It may still be wrong if the retrieved context contained incorrect information. Groundedness measures source-anchoring, not factual correctness.

2. **Relevance is a retrieval metric, not a generation metric.** A high relevance score means the retriever fetched useful chunks. It says nothing about what the LLM did with those chunks. This separation is what makes it possible to identify whether failures are retrieval failures or generation failures.

3. **The `failure_reason` column is a triage tool.** In production, you would scan this column to count how many failures are `low_relevance` (retrieval problems) versus `low_groundedness` (prompt/generation problems) versus `api_rate_limit` (infrastructure problems). Each category points to a different team and a different fix.

4. **The embedding model used for query encoding must match the one used during ingestion.** If you used `all-MiniLM-L6-v2` to encode chunks into ChromaDB in Session 4, you must use the same model to encode queries in Session 5. A different model produces vectors in a geometrically incompatible space, causing cosine similarity to return meaningless results without any error.

5. **Changing `top_k` involves a precision-recall trade-off.** More chunks increase the chance that relevant information is included (higher recall, higher relevance score), but also increase the chance that the LLM has too much context to process and either loses focus or gets distracted by irrelevant passages (potentially lower groundedness).

6. **Keyword overlap scoring has known weaknesses.** It will undercount groundedness when the LLM paraphrases the context using synonyms. It will overcount groundedness if the LLM happens to use many common words that also appear in the chunks for unrelated reasons. These weaknesses are acceptable for a portfolio project but would motivate a move to embedding-similarity scoring in production.

7. **The eval script is designed to be run repeatedly.** The backup logic for existing CSV files and the `run_timestamp` column mean you can run the evaluator multiple times and compare runs over time. This is the foundation of regression testing for RAG systems.

8. **`time.sleep(2)` between Gemini calls is not a workaround — it is correct rate-limit hygiene.** The Gemini free tier has request-per-minute limits. In a production system, you would use exponential backoff with jitter, but a fixed sleep is appropriate for a sequential 5-question eval loop.

9. **An eval harness without a fixed test set is useless.** The 5 hardcoded QA pairs are what make the before/after comparison meaningful. If the test questions changed between runs, score differences would be uninterpretable. Test set stability is as important as the scoring logic.

10. **This eval harness is a foundation, not a final product.** Students should be able to articulate what they would add next: more test cases loaded from a JSON file, embedding-similarity scoring, human-review columns, a CI/CD hook that runs the eval before any pipeline change is deployed.

---

# Interview-Ready Explanation

```text
I built rag_evaluator.py as the evaluation layer for my RAG pipeline. The script runs 5 hardcoded test questions through the pipeline and scores each answer on two metrics: relevance, which measures whether the retrieved chunks contain keywords from the expected answer, and groundedness, which measures whether the generated answer is anchored in the retrieved context. Both scores are computed using keyword overlap in pure Python — no LLM judge, no external framework. Results are saved to a CSV with a failure_reason column that categorizes low-scoring answers. I then changed the top_k retrieval parameter from 2 to 5 and re-ran the same questions, printing a before/after comparison to quantify the effect of that change on both metrics.
```

---

# What Happens When `evaluate_all()` Is Called

```text
evaluate_all(test_cases, collection, embedding_model, gemini_model, top_k=3) is called with 5 QA dicts

For each test case:
  ↓
  run_rag_query(query, collection, embedding_model, gemini_model, top_k) is called
    ↓
    query string → embedding_model.encode(query) → 384-dim numpy vector
    ↓
    collection.query(query_embeddings=[vector], n_results=top_k)
    → returns dict with "documents" key containing list of chunk strings
    ↓
    chunks are joined and injected into prompt:
    "Answer based only on the context below.\nContext:\n{chunks}\nQuestion: {query}\nAnswer:"
    ↓
    gemini_model.generate_content(prompt).text
    → returns generated_answer string (or "" if 429 error after retry)
    ↓
    returns {query, retrieved_chunks: [list], generated_answer: str}
  ↓
  compute_groundedness(generated_answer, retrieved_chunks)
    → tokenize answer and chunks, lowercase, filter short tokens
    → compute intersection of unique token sets
    → return fraction = |answer_tokens ∩ chunk_tokens| / |answer_tokens|
  ↓
  compute_relevance(retrieved_chunks, expected_answer)
    → same overlap logic but comparing chunk tokens against expected_answer tokens
    → return fraction = |chunk_tokens ∩ expected_tokens| / |expected_tokens|
  ↓
  check scores against threshold (0.3)
  → set failure_reason if either score is below threshold
  ↓
  append result dict to results list
  sleep 2 seconds before next question
  print progress line to console

After all 5 questions:
  return results list with 5 dicts

save_report(results, "rag_eval_report.csv") writes CSV
compare_runs(before_results, after_results, "top_k: 2 → 5") prints table to console
```

---

# What AI Was Used For + What Engineers Must Still Do

## What AI (Claude Code / Cursor) Generated

- The full function structure of `rag_evaluator.py`
- The tokenization logic in `compute_groundedness()` and `compute_relevance()`
- The `try/except` block for Gemini 429 error handling with retry
- The `csv.DictWriter` usage in `save_report()`
- The `tabulate` formatting in `compare_runs()`
- The before/after comparison loop in the main block

## What Engineers Must Still Do

- Verify that the ChromaDB `collection_name` and `persist_directory` path match Session 4 exactly
- Confirm that the 5 hardcoded test QA pairs are actually answerable from the ingested corpus
- Run the script and check that `rag_eval_report.csv` has 5 non-empty rows
- Inspect the scores and identify which questions have low groundedness or low relevance
- Interpret the failure_reason column — AI generated the column, but understanding what it means for your specific pipeline is a human judgment
- Explain every function in an interview without reading the code
- Decide whether the before/after comparison result is meaningful or an artifact of the small test set

---

# Common Issues and Fixes

## Issue 1: `ValueError: Collection rag_collection does not exist`

Full error message: `ValueError: Collection rag_collection does not exist.`

Cause: The collection name in `rag_evaluator.py` does not match the name used in `rag_pipeline.py`. This is the most common error in Session 5.

Fix: Open `rag_pipeline.py` from Session 4 and find the line where the collection was created — it looks like `client.get_or_create_collection(name="...")`. Copy the exact name string and use it in `rag_evaluator.py`. You can also run `client.list_collections()` to print all existing collections.

What to ask AI:

```text
My rag_evaluator.py throws: ValueError: Collection rag_collection does not exist.
I have a chroma_db folder from Session 4 but I may have used a different collection name.
Add code to list all existing ChromaDB collections at startup so I can see what name to use.
Then update the get_collection call to use the correct name.
```

## Issue 2: All groundedness scores are 0.0

Cause: The `compute_groundedness()` function is comparing text without lowercasing, so `"Chunking"` and `"chunking"` are treated as different tokens and no overlap is found. Alternatively, the tokenization splits on characters rather than whitespace, or the filter for short tokens is too aggressive.

Fix: Ensure `answer.lower()` and `"".join(chunks).lower()` are called before tokenizing. Check that the token filter length is 3 or 4 characters, not higher. Print a few tokens from both the answer and the chunks to verify what is being compared.

What to ask AI:

```text
In rag_evaluator.py, all my groundedness scores are 0.0 even though the generated answers look correct.
The issue is in compute_groundedness(). Please debug it by:
1. Adding a print statement that shows the first 10 tokens from both the answer and the chunks after tokenization
2. Checking that both are lowercased before tokenization
3. Checking that the short-token filter length is not too aggressive
Fix the function and explain what was wrong.
```

## Issue 3: `google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted`

Full error message: `google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted (e.g. check quota).`

Cause: Multiple Gemini API calls in quick succession have exceeded the free tier rate limit (approximately 60 requests per minute, or 2 requests per minute for some newer models). With 5 test questions and a before/after re-run, that is 10 Gemini calls. If students are also running simultaneously, the class-wide request count is higher.

Fix: Add `time.sleep(2)` between each question in `evaluate_all()`. Wrap the Gemini call in `try/except google.api_core.exceptions.ResourceExhausted` with `time.sleep(10)` and one retry. If the retry also hits 429, record `failure_reason = "api_rate_limit"` and continue.

What to ask AI:

```text
My rag_evaluator.py hits a 429 rate limit error from Gemini after the 2nd or 3rd question.
Full error: google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted.
Please update evaluate_all() to:
1. Add time.sleep(2) between each question evaluation
2. Wrap the Gemini call in run_rag_query() in try/except for ResourceExhausted
3. On 429, sleep 10 seconds and retry once
4. If retry also fails, return empty string and set failure_reason = "api_rate_limit"
Show the updated code for both functions.
```

---

# Limitations of This Module

**Keyword overlap is a weak proxy for semantic similarity.** A LLM-generated answer that paraphrases the retrieved context using synonyms will receive a low groundedness score even though it is perfectly grounded. Conversely, an answer that happens to use common domain vocabulary (words like "model", "data", "system") may score artificially high even if those words match the chunks coincidentally. This limitation is acknowledged and accepted for a portfolio module but would motivate a move to embedding-similarity scoring in production.

**Five test questions are not statistically significant.** Score differences between the before and after runs may be noise rather than signal. A meaningful evaluation would require at least 50–100 questions, statistical significance testing, and multiple re-runs to confirm consistency.

**Hardcoded test questions do not cover edge cases.** The 5 QA pairs cover common factual questions about RAG concepts. They do not include adversarial questions (designed to cause retrieval failure), out-of-scope questions (to test rejection behavior), or multi-hop questions (requiring synthesis from multiple chunks). A production eval set would include all of these.

**The script only evaluates, it does not fix.** When `failure_reason = "low_groundedness"` appears, the script records it but takes no automated action. In production, a low groundedness score might trigger an automatic prompt retry with a stricter instruction, or flag the answer for human review before serving it to the user.

**ChromaDB version compatibility is fragile.** If ChromaDB is upgraded between Session 4 and Session 5, the on-disk format may be incompatible, requiring re-ingestion of all documents. This is not a problem in a 1-session context but would be significant in a long-running production system.

---

# Key Takeaways

1. **Evaluation is not optional.** Every RAG system that is used in production has an eval harness — or it should. Building one is not extra work; it is part of building responsibly. The habit of measuring before and after every change is what separates engineering from guessing.

2. **Groundedness and relevance diagnose different failure modes.** Low relevance means fix the retriever (chunking, embedding model, top-k). Low groundedness means fix the generator (prompt template, context injection format). These require different interventions, and conflating them wastes debugging time.

3. **The before/after mindset is a career skill.** Changing one variable, running the same test set, and comparing results is the scientific method applied to AI engineering. This pattern applies to every parameter change in any AI system — not just top-k in RAG.

4. **Simple tools, clearly explained, beat complex tools you cannot explain.** Keyword overlap is less sophisticated than RAGAS or an LLM judge. But in an interview, you can explain every line of the keyword overlap logic. You can describe exactly why a score went up or down. That explainability is worth more to an interviewer than a black-box framework score.

---

# Session 6 Preview

In Session 6, we build a Simple Agent Router.

Instead of a fixed pipeline that always retrieves from ChromaDB and generates with Gemini, we will give the LLM a set of named tools and let it decide which tool to call based on the user's query. A query like "What is RAG?" will route to a knowledge retrieval tool. A query like "Summarize this document" will route to a summarization tool. A query like "Translate this text" will route to a translation tool.

The LLM acts as a router — it reads the query, decides which tool is appropriate, and calls it with the right arguments.

File to build: `agent_router.py`

Main concept: function calling and tool-use with Gemini 1.5 Flash. We will use `response_mime_type="application/json"` in the generation config to get structured routing decisions from Gemini, then execute the selected tool.

This session builds directly on the eval mindset from Session 5: we will also log which tool was selected for each query and whether the routing decision was correct, connecting back to the tracking discipline from Sessions 2 and 5.
