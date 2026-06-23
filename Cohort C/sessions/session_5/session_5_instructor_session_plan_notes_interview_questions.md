# Session 5 Instructor File: RAG Evaluation and Improvement

## Session Title

RAG Evaluation and Improvement

## Duration

2 hours

## Portfolio Module

eval-module — standalone evaluation script that runs against the Session 4 RAG pipeline

## Session 5 Objective

By the end of Session 5, students will have a working evaluation harness that runs 5 hardcoded test questions against their RAG pipeline, scores each answer for groundedness and relevance, saves results to a CSV, then reruns the evaluation after changing one pipeline parameter (chunk size, top-k, or prompt template) and prints a before/after comparison to the console.

Students will understand what groundedness and faithfulness mean, why they matter, and how to articulate RAG failure modes in an interview without needing a full evaluation framework like RAGAS.

## Deliverable

- `rag_evaluator.py` — main evaluation script
- `rag_eval_report.csv` — output CSV with per-question scores and metadata
- Before/after comparison printed to console showing the effect of changing one pipeline parameter

---

## Strict Scope Control

### Include

- `rag_evaluator.py` with clearly commented functions
- 5 hardcoded test QA pairs (question + expected_answer) relevant to the corpus used in Session 4
- Per-question tracking: `query`, `retrieved_chunks`, `generated_answer`, `expected_answer`, `relevance_score`, `groundedness_score`, `failure_reason`
- Simple groundedness check using keyword overlap between `generated_answer` and `retrieved_chunks`
- Simple relevance score using keyword overlap between `retrieved_chunks` and `expected_answer` (or manual 1–5 labeling in the hardcoded list)
- `rag_eval_report.csv` output using Python's built-in `csv` module
- Improvement loop: change ONE parameter (e.g., top-k from 2 to 5, or chunk size from 200 to 500, or swap in a more explicit prompt template) and rerun the same 5 questions
- Before/after comparison table printed to console using `tabulate` or simple f-string formatting
- Reuse of the ChromaDB collection created in Session 4
- Gemini 1.5 Flash for answer generation via `google-generativeai`

### Do Not Include

- RAGAS framework or any automated LLM-as-judge scoring
- Re-ranking (cross-encoder or otherwise)
- Hybrid search (BM25 + vector)
- A production evaluation dashboard or Streamlit UI
- New document ingestion — Session 5 uses the same ChromaDB collection from Session 4
- OpenAI library or any paid embedding API
- Complex benchmark datasets (HotpotQA, NaturalQuestions, etc.)
- Asynchronous evaluation or batch API calls
- pytest or unit testing frameworks

---

# Instructor Framing

## Opening Message

Show students their portfolio folder. They now have four working scripts:

- `structured_output_engine.py` (Session 1)
- `llm_logger.py` (Session 2)
- `ai_handler.py` (Session 3)
- `rag_pipeline.py` + `chroma_db/` folder (Session 4 — Basic RAG Pipeline (rag_pipeline.py with ChromaDB + Gemini))

Say this to open:

"Last session you built a RAG pipeline that retrieves chunks and generates answers. Today you will do something that most junior engineers skip entirely — you will evaluate whether your RAG pipeline actually works. You will measure groundedness, relevance, and failure reasons. This is the skill that separates engineers who ship working AI systems from engineers who ship systems that look like they work."

## Key Philosophy

Building a RAG pipeline is a Session 4 task. Knowing whether it works, why it fails, and how to improve it — that is Session 5. In AI engineering, evaluation is not optional. Every production RAG system has an eval harness. Today students will build a minimal version of one, understand what each metric means conceptually, and practice the iterative improvement mindset that interviews specifically test.

## Repeated Instructor Line

"If you cannot measure it, you cannot improve it. The eval script is not a test suite — it is a feedback loop."

---

# Session Flow

## 0–10 min: Opening, Portfolio Recap, Show Existing Scripts in Folder

Open the terminal and run `ls` in the portfolio folder. Show students the four files they have built so far. Ask one student to describe what `rag_pipeline.py` does from memory — this reactivates Session 4 context. Briefly draw the RAG flow on the whiteboard: documents → chunks → embeddings → ChromaDB → query → retrieve top-k chunks → Gemini generates answer. Tell students: "Today we are adding one more layer — after the answer comes back, we measure it." Explain that the eval script does not replace the pipeline; it wraps around it. Set the goal: by end of session, every student has a CSV with 5 rows of evaluation results and a before/after comparison in their console.

## 10–20 min: Concept Explanation — What Is RAG Evaluation and Why Does It Matter

Draw the following failure modes on the board:

1. Wrong chunk retrieved — the retriever fetches irrelevant passages, so the LLM has no useful context
2. Hallucination — the LLM ignores the retrieved context and generates from its pretrained knowledge
3. Incomplete answer — the retrieved chunk has partial information and the LLM does not flag it

Explain two core metrics students will implement:
- **Groundedness** (also called faithfulness): Does the generated answer actually use the retrieved context? If you remove the retrieved chunks, would the answer change? We check this by testing keyword overlap between the answer and the chunks.
- **Relevance**: Did the retrieval system fetch the right chunks for the question? We check this by comparing retrieved chunk text against the expected answer keywords.

Ask students: "If you ask a question and the LLM gives a correct-sounding answer, but none of the retrieved chunks contain that information — what is happening?" Lead them to say: the model is hallucinating from pretraining. This is a groundedness failure, not an accuracy pass.

## 20–35 min: Build the Module Using Claude Code or Cursor

Instruct students to open Claude Code or Cursor in their portfolio folder. Tell them to use Prompt 1 from the student file verbatim. Walk them through what the prompt specifies:
- Exact filename `rag_evaluator.py`
- 5 hardcoded QA pairs
- Functions: `run_rag_query()`, `compute_groundedness()`, `compute_relevance()`, `evaluate_all()`, `save_report()`, `compare_runs()`
- Output: `rag_eval_report.csv`
- Before/after comparison using a changed parameter

While the AI generates the code, monitor for: Does it use `google-generativeai`? Does it reference `chroma_db/` directory? Does it define all 5 functions? Does it use `sentence-transformers` for embeddings? If the AI generates OpenAI imports or uses `response.choices[0]`, stop and redirect immediately.

## 35–50 min: Walk Through Generated Code — Explain Every Function

Open `rag_evaluator.py` and walk through it function by function. For each function, ask a student to explain what it does before you explain it. Cover:

- `run_rag_query(query, chroma_collection, embedding_model, gemini_model, top_k)` — embeds the query, queries ChromaDB, formats retrieved chunks into a prompt, calls Gemini, returns answer + chunk list
- `compute_groundedness(answer, retrieved_chunks)` — tokenizes answer and chunks, counts overlapping unique words above a minimum length, returns a 0–1 score or 1–5 scale
- `compute_relevance(retrieved_chunks, expected_answer)` — same keyword overlap logic but between chunks and expected answer; represents retrieval quality
- `evaluate_all(test_cases, top_k, chunk_config)` — loops through all 5 QA pairs, calls run_rag_query, computes both scores, records failure_reason if scores are below threshold
- `save_report(results, filename)` — writes results list to CSV using Python's `csv.DictWriter`
- `compare_runs(results_before, results_after, param_changed)` — prints a side-by-side table showing per-question score changes

Emphasize: no LLM is judging the answers here. All scoring is deterministic keyword overlap. That makes it fast, free, and explainable.

## 50–65 min: Student Follow-Along Build

Students run Prompt 1, generate `rag_evaluator.py`, and execute it. Instructor circulates and monitors for the most common errors (listed in Common Student Mistakes below). Key checks:
- Does ChromaDB collection load without error? Students must use the same `persist_directory` and `collection_name` from Session 4.
- Do the 5 test questions match the corpus? If a student ingested a different document in Session 4, their test QA pairs need to match that corpus.
- Does `rag_eval_report.csv` appear in the folder after running?
- Is the groundedness score non-zero for at least some questions?

If a student's Session 4 ChromaDB is broken or missing, they should use the instructor's shared `chroma_db/` folder. Do not let a broken ChromaDB block the eval session — the evaluation concepts are more important than re-ingesting documents.

## 65–80 min: Test with Sample Inputs, Inspect Output Files

Open `rag_eval_report.csv` in a spreadsheet view (or print it via pandas). Walk through the 5 rows:
- Which questions had high groundedness? Why?
- Which questions had low relevance? What does that mean about the retriever?
- Are there any `failure_reason` entries? What are they?

Ask students to pick the worst-scoring question and identify whether the failure is retrieval failure (wrong chunks) or generation failure (chunks correct but answer ignores them). This distinction is the core of the session's conceptual learning. Run the before/after comparison and show how changing top-k from 2 to 5 affects coverage. Ask: "More chunks always better?" Lead them to see: more chunks can introduce noise, reduce precision, and cause the LLM to lose focus.

## 80–95 min: Edge Cases, Error Handling, Failure Modes

Use Prompt 7 from the student file to add edge case handling. Walk through these scenarios:
- Empty retrieved chunks (ChromaDB returns no results for a query) — the script must not crash; it should record `failure_reason = "no_chunks_retrieved"` and skip Gemini call
- Gemini returns an empty string — record `failure_reason = "empty_generation"` and set both scores to 0
- Gemini throws a 429 rate limit error — wrap the Gemini call in a `try/except` with a 10-second sleep and one retry; if it fails again, record `failure_reason = "api_rate_limit"` and continue to next question
- All retrieved chunks are identical (duplicate embedding issue from Session 4) — groundedness will be artificially high; add a deduplication step
- CSV file already exists from a previous run — overwrite it cleanly or append with a run timestamp column

Discuss why `failure_reason` is important: in production, you want to know not just that a score was low, but WHY it was low. This is triage information.

## 95–105 min: Concept Pause — RAG Evaluation, Groundedness, Faithfulness, Retrieval Failure Analysis, Iterative Improvement

Stop coding. Ask students to close their laptops halfway. Explain:

**Groundedness vs. Faithfulness**: These terms are often used interchangeably. Strictly, faithfulness measures whether each claim in the generated answer is supported by the retrieved context. Groundedness is whether the answer is anchored to the context at all. Our keyword overlap is a proxy for both — it is not perfect but it is fast and requires no LLM judge.

**Retrieval failure vs. generation failure**: If relevance score is low, the retriever fetched wrong chunks — this is a retrieval failure. If relevance is high but groundedness is low, the LLM ignored good context — this is a generation failure or hallucination. These require different fixes: retrieval failures need better chunking or embedding; generation failures need a stricter prompt.

**Iterative improvement mindset**: Change ONE variable at a time. We changed top-k (or chunk size or prompt) and re-ran the same 5 questions. The before/after comparison tells us whether the change helped. This is how production teams improve RAG — not by rebuilding from scratch but by measuring, changing one thing, and measuring again.

Ask every student to write a 2-sentence answer: "What is groundedness and how did you measure it today?" Collect answers verbally.

## 105–115 min: Interview Discussion and Viva Practice

Use the interview questions in the section below. Run 10 minutes of rapid-fire viva. Call on students by name. For weaker students, use Q1–Q5. For stronger students, use Q6–Q15. Correct any student who says "groundedness means the answer is correct" — it means the answer is anchored in the retrieved context. An answer can be grounded but wrong if the retrieved context itself was wrong.

## 115–120 min: Wrap-Up, Show Deliverables, Preview Next Session

Show the three deliverables in the portfolio folder:
- `rag_evaluator.py`
- `rag_eval_report.csv`
- Console output with before/after comparison

Tell students: "You now have 5 portfolio modules. Your RAG pipeline not only works — you can measure whether it works and show evidence of improvement. That is what a senior engineer would call an eval-driven workflow."

Preview Session 6 — Simple Agent Router: "Next session we build an Agent Router. Instead of one fixed pipeline, we will give the LLM a set of tools to choose from and let it decide which tool to call based on the user's query. That is the foundation of agentic AI systems."

---

# Instructor Notes

## What to Emphasize

Session 5 is the conceptual peak of the RAG arc (Sessions 4–5). The code is relatively simple — keyword overlap, CSV writing, a loop. The hard part is helping students understand what the scores mean and why they matter. Spend at least 15 minutes on the conceptual distinction between retrieval failure and generation failure. Students who understand this distinction can answer senior-level RAG questions in interviews.

Emphasize that we are NOT using a LLM to judge the answers. This is a deliberate scope choice. RAGAS and similar frameworks use LLM-as-judge scoring, which is powerful but expensive and opaque. Our approach is transparent and free — students can explain every line of the scoring logic, which is exactly what interviewers want to hear.

Emphasize the iterative improvement mindset: one change at a time, measure before and after, look at the delta. This is how real RAG systems are improved in production.

## Common Student Mistakes

1. **Using `import openai` in `rag_evaluator.py`** — The AI coding tool may default to OpenAI. If you see `openai.ChatCompletion.create()` or `response.choices[0].message.content`, stop immediately. The correct import is `import google.generativeai as genai` and the correct call is `model.generate_content(prompt).text`.

2. **Wrong ChromaDB collection name** — Students may use a different `collection_name` than what they used in Session 4. This causes `chroma_collection.query()` to return empty results. Fix: check Session 4 code for the exact collection name and match it in Session 5.

3. **Wrong `persist_directory` path** — If `chroma_db/` was created inside a subfolder in Session 4 but the evaluator script runs from the root portfolio folder, the path won't resolve. Use `os.path.abspath("chroma_db")` and confirm the folder exists before running.

4. **Sentence-transformers model not downloaded yet** — The first time `SentenceTransformer("all-MiniLM-L6-v2")` runs, it downloads ~90MB. On slow connections, this looks like a hang. Tell students to wait; it is not frozen.

5. **Gemini 429 rate limit on the fifth consecutive question** — Gemini free tier allows approximately 60 requests per minute. Running 5 eval questions + the re-run equals 10 Gemini calls in quick succession. Add a `time.sleep(2)` between calls. Error message looks like: `google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted (e.g. check quota).`

6. **Groundedness score is 0 for all questions** — Usually caused by comparing raw strings without lowercasing and stripping punctuation. The tokenization in `compute_groundedness()` must lowercase both the answer and chunk text before computing overlap. Run `answer.lower()` and `chunk.lower()` before splitting.

7. **CSV has only one row** — `csv.DictWriter` will overwrite if opened in `"w"` mode inside a loop. The `save_report()` function must collect all results first, then write once — not write inside the evaluation loop.

8. **Before/after comparison shows identical scores** — The student changed the parameter in the function call but forgot to clear and reinitialize the ChromaDB client between runs if chunk size was changed. Chunk size changes require re-ingesting documents. If only top-k or prompt template is changed, no re-ingestion is needed.

9. **`failure_reason` column is always empty** — The threshold check for recording failure reasons was not implemented. Remind students: if `groundedness_score < 0.3` or `relevance_score < 0.3`, set `failure_reason` to a descriptive string. An empty `failure_reason` column on all rows makes the report less useful.

10. **Test questions do not match the ingested corpus** — If a student asks questions about a document they did not ingest in Session 4, all retrieved chunks will be irrelevant. The 5 hardcoded QA pairs in the student file are calibrated to a generic AI/ML concepts corpus. Students who ingested a different document must write their own QA pairs accordingly.

## How to Control the Session

Use the "one variable at a time" rule strictly. If students want to change chunk size AND top-k AND the prompt template simultaneously, stop them. The before/after comparison only makes sense if exactly one variable changes. This is a real engineering discipline — controlled experiments.

If students get excited and want to add RAGAS or an LLM judge, acknowledge it is a great idea for a portfolio extension but out of scope for today. "You can add that after the session. Today's goal is to understand the fundamentals without hiding them behind a library."

If the session is running behind schedule, the before/after improvement comparison can be simplified to a console print of average scores across all 5 questions rather than a per-question table.

---

# Questions to Discuss: Interview Perspective

## Basic Module Questions

### Q1. What is RAG evaluation and why does it matter?

Expected answer:
RAG evaluation is the process of measuring whether a Retrieval-Augmented Generation pipeline produces answers that are accurate, grounded in the retrieved context, and relevant to the user's query. It matters because a RAG pipeline can appear to work — it generates fluent, confident-sounding answers — while actually hallucinating information that was never in the retrieved documents. Without evaluation, you cannot tell whether your pipeline is trustworthy. In a production system, you would run an eval harness regularly, especially after changing any pipeline parameter, to detect regressions. Even a simple keyword-overlap evaluation is better than no evaluation at all.

### Q2. What does groundedness mean in the context of RAG?

Expected answer:
Groundedness measures whether the generated answer is anchored in the retrieved context. A grounded answer uses information that actually appears in the chunks returned by the retriever. An ungrounded answer sounds plausible but introduces facts that were not present in the retrieved documents — this is hallucination from the LLM's pretrained weights. In our implementation, we measure groundedness by computing the keyword overlap between the generated answer text and the concatenated retrieved chunk text. If the answer contains many words that also appear in the chunks, the groundedness score is high. If the answer contains words that do not appear in any retrieved chunk, the score is low, which is a signal that the LLM may have ignored the context.

### Q3. What is the difference between relevance and groundedness in your evaluation script?

Expected answer:
Relevance and groundedness measure different parts of the RAG pipeline. Relevance measures retrieval quality — did the retriever fetch the right chunks for the question? We compute this by comparing the retrieved chunk text against the expected answer using keyword overlap. A low relevance score means the retriever returned chunks that do not contain the information needed to answer the question correctly. Groundedness measures generation quality — did the LLM actually use the retrieved context when formulating its answer? A high relevance but low groundedness score means the retriever did its job but the LLM ignored the context and hallucinated. This distinction is critical for debugging: retrieval failures require fixing chunking or embeddings, while generation failures require fixing the prompt template.

### Q4. What is a `failure_reason` field in your evaluation report, and what values can it take?

Expected answer:
The `failure_reason` field in `rag_eval_report.csv` is a diagnostic column that records the likely cause of a low-scoring evaluation case. We populate it when a score falls below a defined threshold — for example, when `groundedness_score < 0.3` or `relevance_score < 0.3`. Possible values include `"no_chunks_retrieved"` when ChromaDB returns an empty result set, `"low_groundedness"` when the answer text has very little overlap with the retrieved chunks, `"low_relevance"` when the chunks do not contain keywords from the expected answer, `"empty_generation"` when Gemini returns an empty string, and `"api_rate_limit"` when a Gemini 429 error is caught. This field turns the CSV from a score table into a triage document — engineers can scan it to understand what kind of failures are most common and prioritize fixes accordingly.

### Q5. Why did you choose keyword overlap instead of using an LLM to score the answers?

Expected answer:
We chose keyword overlap because it is free, fast, deterministic, and fully explainable. An LLM-based judge — as used in frameworks like RAGAS — requires additional API calls for every evaluated answer, which adds latency and cost. More importantly, it introduces a black box: if the judge says an answer scores 3 out of 5, it is not always clear why. Keyword overlap, by contrast, is completely transparent: you can inspect exactly which words matched and which did not. For a portfolio project and for interview discussions, explainability matters more than precision. The trade-off is that keyword overlap is a weak proxy — two semantically similar sentences may share few keywords, and keyword overlap can be gamed. In production, you would eventually move toward embedding-similarity scoring or LLM-as-judge, but keyword overlap is an appropriate starting point.

## Technical Deep-Dive Questions

### Q6. Walk me through the `compute_groundedness()` function. What are its inputs, logic, and output?

Expected answer:
`compute_groundedness(answer, retrieved_chunks)` takes two inputs: `answer`, which is a string containing the LLM-generated response, and `retrieved_chunks`, which is a list of strings representing the document chunks returned by ChromaDB. The function first concatenates all chunks into a single string. It then lowercases and tokenizes both the answer and the chunk string by splitting on whitespace and stripping punctuation. It filters out very short tokens (typically fewer than 4 characters) to avoid noise from stopwords. It then computes the intersection of the unique token sets from the answer and the chunk string and divides by the number of unique tokens in the answer. The result is a float between 0 and 1, where 1 means every content word in the answer also appeared in the retrieved chunks and 0 means there is no overlap at all. The function returns this float, which we optionally scale to a 1–5 integer for the CSV report.

### Q7. How does your script load the ChromaDB collection from Session 4, and what could go wrong?

Expected answer:
The script uses `chromadb.PersistentClient(path="chroma_db")` to connect to the local ChromaDB instance created during Session 4. It then calls `client.get_collection(name="collection_name")` using the exact same collection name used during ingestion. The collection object exposes a `.query()` method that accepts an embedding vector and a `n_results` parameter. Three common failure modes exist here: first, if the `path` argument points to the wrong directory, ChromaDB will create a new empty database and queries will return no results; second, if the `collection_name` string does not match what was used in Session 4, `get_collection()` will raise a `ValueError`; third, if the ChromaDB version installed differs between Session 4 and Session 5 (e.g., due to an upgrade), the on-disk format may be incompatible and the client will throw a migration error. The fix for the third case is to re-ingest the documents using the new ChromaDB version.

### Q8. What embedding model do you use to encode queries in the evaluator, and why must it match the embedding model used during ingestion?

Expected answer:
We use `sentence-transformers` with the `all-MiniLM-L6-v2` model, which produces 384-dimensional float vectors. This must exactly match the embedding model used in `rag_pipeline.py` during Session 4. The reason is that ChromaDB stores vectors and performs approximate nearest-neighbor search in the embedding space defined by the model that generated those vectors. If you encode the query with a different model — say, a 768-dimensional model or even a different 384-dimensional model — the query vector will live in a different geometric space than the stored chunk vectors. The cosine similarity computation will return meaningless results because the dimensions are not aligned conceptually. In practice, this means the retriever will return wrong chunks even though the ChromaDB query succeeds without errors. Embedding model consistency is one of the most subtle bugs in production RAG systems.

### Q9. How does the before/after comparison work in your script, and what parameter did you change?

Expected answer:
The `compare_runs(results_before, results_after, param_changed)` function takes two lists of evaluation dictionaries — one from the initial run and one from the improved run — along with a string describing what changed. It loops through both lists simultaneously, matching questions by index, and prints a row for each question showing the query text, the before scores, the after scores, and the delta. The delta is computed as `after_score - before_score` for both groundedness and relevance. A positive delta means the change improved that metric. At the bottom, it prints the average groundedness and relevance for both runs. In our script, we changed `top_k` from 2 to 5 as the default improvement. With `top_k=2`, the retriever returns only the two most similar chunks; with `top_k=5`, it returns five. This typically improves relevance because more chunks cover more of the expected answer, but it can reduce groundedness precision because the LLM has more context to potentially ignore or get distracted by. Observing this trade-off in the before/after table is the key learning outcome.

### Q10. How does your script handle a Gemini 429 rate limit error, and what is recorded in the report?

Expected answer:
The `run_rag_query()` function wraps the Gemini `model.generate_content(prompt)` call in a `try/except` block catching `google.api_core.exceptions.ResourceExhausted`. When this exception is caught, the function sleeps for 10 seconds using `time.sleep(10)` and retries once. If the retry also fails, the function returns an empty string as the answer and signals to the caller to record `failure_reason = "api_rate_limit"`. The `evaluate_all()` function detects the empty answer string and sets both `groundedness_score` and `relevance_score` to 0 for that question before appending it to the results list. The script then continues to the next question without crashing. This graceful degradation is important because a crash midway through the evaluation run would lose all previously computed scores. The `rag_eval_report.csv` will still contain rows for all 5 questions, with the rate-limited question clearly flagged.

## Production and System Design Questions

### Q11. How would you scale this evaluation script to 500 test questions instead of 5?

Expected answer:
Scaling to 500 questions requires three changes. First, the Gemini calls must be rate-limited more carefully — the free tier allows approximately 60 requests per minute, so 500 questions would take at minimum 9 minutes with 1-second delays. You could use `time.sleep(1)` between calls and wrap the loop with a progress bar using `tqdm`. Second, the test QA pairs should not be hardcoded in the script but loaded from a CSV or JSON file using `pandas` or the `json` module, making the harness data-driven. Third, the `compare_runs()` function should output to a file rather than the console, because 500-row comparisons are not readable in a terminal. In production at scale, you would move to an async evaluation architecture where Gemini calls are batched or run in parallel using `asyncio`, and results are stored in a proper database rather than a flat CSV. You would also add statistical significance testing to determine whether a score improvement is meaningful or just noise.

### Q12. What is the difference between offline and online RAG evaluation, and which does your script implement?

Expected answer:
Offline evaluation runs against a fixed, labeled dataset of question-answer pairs before deployment. It measures how well the pipeline performs on known ground truth. Our script implements offline evaluation: we have 5 hardcoded questions with expected answers, and we score the pipeline against those. Online evaluation measures real user queries in production, where there is no ground truth — you must use proxy signals like user feedback, thumbs up/down, session length, or follow-up questions to infer answer quality. Online evaluation is harder to implement but more representative of real usage. In a production system, you would combine both: offline evaluation for regression testing before deployments, and online evaluation for monitoring in production. Our script is the foundation for the offline component. Adding a feedback column to the CSV (e.g., a column for human reviewers to mark answers as good or bad) would be the first step toward a more complete offline eval system.

### Q13. What breaks in your evaluation script when the RAG corpus changes — for example, when new documents are added to ChromaDB?

Expected answer:
When new documents are added to ChromaDB, the evaluation script may need to be updated in two ways. First, the 5 hardcoded QA pairs may no longer be representative — if new documents introduce new topics, the old test questions may consistently receive high relevance scores because there is now more relevant content, artificially inflating scores. This is called distribution shift in the eval dataset. Second, if chunk overlap between old and new documents creates near-duplicate embeddings, the retriever may return slightly different chunks for the same queries, causing score variance across runs even without changing any pipeline parameter. In production, eval datasets should be version-controlled alongside the corpus and updated whenever the corpus changes. Each eval run should record the ChromaDB document count and a corpus hash so you can detect when the underlying data changed between runs.

### Q14. How would you monitor a deployed RAG pipeline using ideas from what you built today?

Expected answer:
The core idea from our eval script — track each query with its retrieved chunks, generated answer, and quality scores — translates directly to a production monitoring approach called request logging with quality scoring. In production, you would log every user query along with the retrieved chunks and generated answer to a database table. You would then run the same keyword-overlap groundedness check on every logged query asynchronously, flagging low-scoring responses for human review. You could set up a dashboard that shows average groundedness and relevance scores over time, broken down by query type or user segment. Anomalies — a sudden drop in average groundedness — would trigger alerts indicating that the corpus may have changed, the embedding model may be stale, or the LLM behavior may have shifted. Our `failure_reason` categorization from the eval report directly maps to the alert categories in such a monitoring system: `no_chunks_retrieved` alerts would go to the retrieval team, `low_groundedness` alerts would go to the prompt engineering team.

### Q15. An interviewer asks: "Your RAG pipeline has low groundedness scores. What do you do?" Walk through your debugging process.

Expected answer:
I would start by checking whether it is a retrieval failure or a generation failure by examining the `relevance_score` alongside the `groundedness_score`. If relevance is also low, the retriever is fetching wrong chunks — the problem is in the embedding model, chunk size, or corpus quality, not in the prompt. I would inspect the actual retrieved chunks for a few low-scoring questions to see what the retriever is returning, then try increasing `top_k` to see if the correct information appears in a larger retrieved set. If relevance is high but groundedness is low, the retriever is doing its job but the LLM is ignoring the context. This is a prompt engineering problem: I would rewrite the prompt to be more explicit about using only the provided context — for example, adding an instruction like "Answer strictly based on the following context. If the answer is not in the context, say 'I don't know'." I would then re-run the evaluation with the new prompt and check whether groundedness improved. If both scores are high but the answer still seems wrong to a human reviewer, the issue may be with the quality of the ground truth in the eval dataset itself, which requires updating the QA pairs.

---

# Session 5 Completion Checklist

- [ ] `rag_evaluator.py` exists in the portfolio folder and runs without errors
- [ ] Script connects to the ChromaDB collection from Session 4 without `ValueError` or path errors
- [ ] All 5 test questions are processed and generate non-empty answers from Gemini
- [ ] `rag_eval_report.csv` is created with correct columns: `query`, `retrieved_chunks`, `generated_answer`, `expected_answer`, `relevance_score`, `groundedness_score`, `failure_reason`
- [ ] `rag_eval_report.csv` has exactly 5 data rows (one per test question)
- [ ] Groundedness scores are computed and non-zero for at least 3 of the 5 questions
- [ ] Relevance scores are computed and non-zero for at least 3 of the 5 questions
- [ ] `failure_reason` column is populated for any question with a score below 0.3 (not left empty for all rows)
- [ ] Gemini 429 rate limit is handled with a `try/except` block and one retry
- [ ] Before/after comparison prints to console after changing one pipeline parameter (top-k, chunk size, or prompt template)
- [ ] Student can explain the difference between groundedness and relevance without reading notes
- [ ] Student can identify at least one low-scoring question in their report and explain why it failed
- [ ] Expected deliverable complete: `rag_evaluator.py` + `rag_eval_report.csv` + before/after comparison output

---

# Instructor Backup Plan

## If Gemini Rate Limit Hits During Class

The most common issue during this session is hitting the Gemini free tier rate limit when multiple students run their evaluations simultaneously. Mitigation steps:

1. Add `time.sleep(2)` between each of the 5 evaluation calls in `evaluate_all()` before students start running
2. Stagger student runs — ask students to start in groups of 3, 2 minutes apart
3. If 429 errors persist, have students run only 3 of the 5 test questions during class and complete the rest after session
4. The `failure_reason = "api_rate_limit"` handling in the script means the eval report will still be written even if 1–2 questions fail; students can explain this as correct error handling behavior in an interview

## If a Student's Session 4 ChromaDB Setup Is Missing or Broken

1. Share a pre-built `chroma_db/` folder (instructor machine export) via Google Drive or USB that students can drop into their portfolio folder
2. The shared collection should contain at least 20 chunks from a generic AI/ML concepts document (recommended: a 500-word article about transformers or RAG systems)
3. Instruct the student to copy the folder and run `rag_evaluator.py` — they do not need to re-run `rag_pipeline.py`
4. Do not spend more than 5 minutes debugging a broken Session 4 setup during live class; get the student unstuck with the shared folder and let them revisit Session 4 after class

## If Claude Code or Cursor Generates Incorrect Code

1. Check for OpenAI imports — replace with `google.generativeai`
2. Check that `ChromaDB.PersistentClient` is used, not the deprecated `chromadb.Client()`
3. Check that `SentenceTransformer("all-MiniLM-L6-v2")` is used for query encoding, not any API-based embedding
4. Use Prompt 3 (Debugging Prompt) from the student file to fix specific errors
5. As a last resort, have students type the key functions manually from the whiteboard — the functions are short enough that this is feasible in 10 minutes

## If the Before/After Comparison Shows No Difference

This can happen when:
- The corpus is too small (fewer than 10 chunks) — with a tiny ChromaDB collection, changing top_k from 2 to 5 may return the same 2 chunks because only 2 exist
- The test questions are answered fully by a single chunk — in this case, top_k makes no difference
- The keyword overlap scoring is insensitive to the change — if the LLM generates identical answers regardless of how many chunks are provided

Recovery steps:
1. Check how many chunks are in the ChromaDB collection: `print(collection.count())`
2. If fewer than 10 chunks exist, ask the student to re-run their Session 4 `rag_pipeline.py` with a longer document to create more chunks
3. Alternatively, switch the "after" improvement to a prompt template change instead of a top_k change — this is more likely to produce visible groundedness differences
4. Explain to students that a flat before/after result is itself informative: it means the parameter you changed is not the bottleneck for these specific test cases

---

# Instructor Reference: Key Vocabulary for This Session

Use these definitions consistently. Students will quote them in interviews.

**Groundedness**: The degree to which a generated answer is anchored in the retrieved context. Measured by the overlap between answer tokens and retrieved chunk tokens. Also called faithfulness in some evaluation frameworks.

**Relevance** (retrieval relevance): The degree to which the retrieved chunks contain information needed to answer the question correctly. Measured by the overlap between retrieved chunk tokens and expected answer tokens.

**Faithfulness**: In strict RAGAS terminology, faithfulness measures whether each individual claim in the generated answer is supported by the retrieved context. We approximate this with overall keyword overlap.

**Retrieval failure**: A failure mode where the vector retriever returns chunks that do not contain the information needed to answer the question. Identified by a low relevance score.

**Generation failure / Hallucination**: A failure mode where the LLM produces an answer that introduces facts not present in the retrieved chunks. Identified by a high relevance score but low groundedness score.

**Eval-driven development**: The engineering practice of maintaining a fixed evaluation dataset and running it against the system before and after every change. The before/after comparison in this session is a minimal implementation of this practice.

**Top-k**: The number of most similar document chunks returned by the vector retriever for a given query. Increasing top-k increases context coverage (recall) but may reduce precision and increase prompt length.

---

# Session 5 Sample Console Output

This is what a correctly working run should produce in the console:

```
Evaluating question 1/5: What is the purpose of chunking in a R...
  → Groundedness: 0.62 | Relevance: 0.58 | Failure: none
Evaluating question 2/5: What embedding model is used to convert...
  → Groundedness: 0.71 | Relevance: 0.64 | Failure: none
Evaluating question 3/5: What is ChromaDB used for in a RAG syst...
  → Groundedness: 0.55 | Relevance: 0.49 | Failure: none
Evaluating question 4/5: What is the role of Gemini in the RAG p...
  → Groundedness: 0.43 | Relevance: 0.38 | Failure: none
Evaluating question 5/5: What does top-k control in a RAG retrie...
  → Groundedness: 0.28 | Relevance: 0.22 | Failure: low_relevance

Average Groundedness: 0.52 | Average Relevance: 0.46
Questions with failures: 1

Report saved to rag_eval_report.csv

--- BEFORE/AFTER COMPARISON ---
Parameter changed: top_k: 2 → 5

+------------------------------------------+----------+---------+-------+----------+---------+-------+
| Query                                    | Before G | After G | ΔG    | Before R | After R | ΔR    |
+==========================================+==========+=========+=======+==========+=========+=======+
| What is the purpose of chunking in a...  | 0.62     | 0.65    | +0.03 | 0.58     | 0.71    | +0.13 |
| What embedding model is used to conv...  | 0.71     | 0.68    | -0.03 | 0.64     | 0.72    | +0.08 |
| What is ChromaDB used for in a RAG s...  | 0.55     | 0.61    | +0.06 | 0.49     | 0.68    | +0.19 |
| What is the role of Gemini in the RA...  | 0.43     | 0.47    | +0.04 | 0.38     | 0.55    | +0.17 |
| What does top-k control in a RAG ret...  | 0.28     | 0.41    | +0.13 | 0.22     | 0.47    | +0.25 |
+------------------------------------------+----------+---------+-------+----------+---------+-------+
| AVERAGE                                  | 0.52     | 0.56    | +0.04 | 0.46     | 0.63    | +0.17 |
+------------------------------------------+----------+---------+-------+----------+---------+-------+

Report saved to rag_eval_report_improved.csv
```

Point out to students:
- Relevance consistently improved with higher top_k — more chunks covered more of the expected answers
- Groundedness improved for most questions but slightly decreased for Q2 — this illustrates the precision-recall trade-off
- Q5 (top-k question) showed the biggest improvement because the answer was spread across multiple chunks that only appeared when top_k increased
