# Session 4 After-Session Notes: Basic RAG Pipeline

## What We Built Today

Today we built `rag_pipeline.py` — a complete, standalone Retrieval-Augmented Generation pipeline in a single Python file. We also created `chroma_db/`, a persistent local vector database folder that was generated automatically when the script ran.

The pipeline handles:
- 6–8 customer support documents defined as Python string constants
- Paragraph-level chunking by splitting on double newlines
- Local embedding generation using `SentenceTransformer("all-MiniLM-L6-v2")` — no API call needed
- Persistent vector storage in ChromaDB using `PersistentClient(path="chroma_db")`
- Top-3 chunk retrieval using `collection.query()` with cosine similarity
- Grounded answer generation using Gemini 1.5 Flash via `google-generativeai`
- An `ask(query)` function that returns both the answer and the retrieved chunks

The portfolio now looks like this:

```
structured_output_engine.py    ← Session 1
output_examples.json
llm_logger.py                  ← Session 2
llm_logs.csv
eval_summary.json
ai_handler.py                  ← Session 3
.env.example
rag_pipeline.py                ← Session 4  (built today)
chroma_db/                     ← Session 4  (created today)
```

---

# Why This Module Matters for AI Engineering Interviews

RAG is one of the top 5 topics asked in AI engineering interviews at every level. Interviewers ask about it because it touches multiple foundational AI engineering concepts at once: how language meaning is represented numerically (embeddings), how similarity search works at scale (vector databases), how to give an LLM grounded knowledge without retraining it (retrieval-augmented prompting), and how to reduce hallucination in production systems.

What makes this module particularly valuable in an interview is that you built the full pipeline from scratch using raw library calls — no LangChain abstractions, no managed RAG service. This means you can explain what happens at every step rather than describing a black box. Most candidates who say "I built a RAG system" used a framework that hid the implementation. You can explain the embedding dimensions, the ChromaDB query structure, and why the retrieved text is injected as a string into the prompt.

Session 5 makes this even stronger: you will evaluate the pipeline you built today, which means you can speak about both building and measuring a RAG system — a combination that is rarely demonstrated at the fresher level.

---

# Portfolio Module Map

```
Session 1: Structured Output Prompt Engine
    structured_output_engine.py + output_examples.json
    DONE
            |
            v
Session 2: LLM Logging and Evaluation Tracker
    llm_logger.py + llm_logs.csv + eval_summary.json
    DONE
            |
            v
Session 3 — Serverless-Style AI Function (local handler pattern established)
    ai_handler.py + .env.example
    DONE
            |
            v
Session 4: Basic RAG Pipeline  <<< COMPLETED TODAY
    rag_pipeline.py + chroma_db/
    DONE
            |
            v
Session 5 — RAG Evaluation and Improvement
    rag_evaluator.py + rag_eval_report.csv
    USES rag_pipeline.py and chroma_db/ from today
    NEXT SESSION
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
    README.md + architecture_diagram.md + demo_script.md
```

Sessions 4 and 5 are directly connected. Do not modify or delete `rag_pipeline.py` or `chroma_db/` before Session 5 — the evaluation script will import from `rag_pipeline.py` and query the same ChromaDB collection you created today.

---

# Technical Deep-Dive: Embeddings, Vector Database, Chunking, Top-k Retrieval, Grounded Generation, and RAG vs. Vanilla LLM

**How the embedding and retrieval layer works:**
An embedding is a dense numerical vector produced by passing text through a transformer encoder model. The `all-MiniLM-L6-v2` model produces a 384-dimensional vector for any input string — a single list of 384 floating-point numbers that encodes the semantic meaning of that text. The key property of these vectors is that texts with similar meanings end up with vectors that point in similar directions in 384-dimensional space. Cosine similarity measures how closely two vectors point in the same direction: a score close to 1.0 means the texts are semantically similar, while a score close to 0.0 means they are unrelated. When ChromaDB receives a query vector, it computes cosine similarity between the query and every stored embedding, then returns the IDs and text of the top-k most similar chunks. This is fundamentally different from keyword search, which requires word overlap — semantic search finds relevant chunks even when the exact words do not match.

**Why chunking exists and what the trade-offs are:**
Embedding models have a maximum token input length — for `all-MiniLM-L6-v2`, this is 256 tokens (approximately 180–200 words). But the deeper reason for chunking is retrieval precision: if you embed an entire 500-word policy document as one vector, the embedding averages out all the topics covered in the document. A query about refunds might match a document that discusses both refunds and cancellations, even if the refund section is only two sentences long. By splitting on paragraph breaks (`\n\n`), you create smaller, more focused chunks — a query about refunds will retrieve a chunk that is specifically about refunds, not a chunk that happens to mention refunds somewhere in the middle. The trade-off runs in both directions: chunks that are too small lose context (a single sentence may not have enough meaning to match well), while chunks that are too large reduce retrieval precision. Paragraph-level chunking is a practical starting point that works well for structured support documents.

**How grounded generation differs from a vanilla LLM call and why it reduces hallucination:**
A vanilla Gemini call — just passing the user's question with no context — relies entirely on the model's training data. For general questions, the model may give a plausible-sounding answer that is actually generic or slightly wrong for this specific company's policies. For company-specific questions like "what is the exact refund window," the model has no training data and will either make something up (hallucinate) or refuse to answer. The RAG approach fixes this by copying the retrieved document chunks into the prompt string before the question. The prompt explicitly instructs the model to base its answer only on the provided context, not on general knowledge. Because the model is reading the actual policy text as part of its input, it can quote it, summarize it accurately, and say "this is not covered in the provided documents" when the context does not contain the answer. The key technical point: the model does not access ChromaDB directly — the retrieved text is literally a string appended to the prompt, and the model treats it as part of its input context.

---

# What Students Should Understand

1. An embedding is a list of 384 numbers that represents the meaning of a text. Two semantically similar texts will have embedding vectors with high cosine similarity, regardless of whether they share any words.

2. Chunking exists because we want to retrieve focused, relevant pieces of text, not whole documents. Splitting on `\n\n` gives paragraph-level chunks, which are a good balance between specificity and context.

3. `SentenceTransformer("all-MiniLM-L6-v2")` runs entirely locally — it downloads once and then works offline. It requires no API key, no cost, and produces high-quality embeddings for semantic similarity tasks.

4. ChromaDB's `PersistentClient(path="chroma_db")` saves the embedding vectors and their associated text to a SQLite file on disk. The collection survives between Python runs, so you do not need to re-embed all documents every time you use the pipeline.

5. `collection.query(query_embeddings=[query_vec], n_results=3)` returns the 3 stored chunks whose embedding vectors are most similar to the query vector. The returned object is a dictionary with nested lists: `result["documents"][0]` is a list of 3 chunk strings.

6. The retrieved chunks are injected into the Gemini prompt as plain text. The model never directly accesses ChromaDB — retrieval and generation are two separate steps with a string as the bridge.

7. A vanilla LLM call and a RAG-augmented call can produce very different answers for company-specific questions. The RAG answer is grounded in actual retrieved documents; the vanilla answer is based on general training data and may hallucinate specific details.

8. The `ask(query)` function returns a dictionary with both `"answer"` and `"retrieved_chunks"`. Returning the chunks is important for transparency, debugging, and for the evaluation work in Session 5.

9. The most common errors in this pipeline are: duplicate ChromaDB IDs on re-run (fix: check `collection.count()` before ingesting), Gemini 429 rate limit (fix: try/except with fallback), and `sentence-transformers` not installed (fix: `pip install sentence-transformers`).

10. In production, this pipeline would need: a document update mechanism to replace stale embeddings, retrieval quality monitoring to detect when returned chunks are irrelevant, and similarity score thresholds to handle queries that have no good match in the knowledge base.

---

# Interview-Ready Explanation

```text
I built a complete RAG pipeline in Python that answers customer support queries using a local knowledge base of 8 support documents. The pipeline chunks the documents by paragraph, generates embeddings using sentence-transformers all-MiniLM-L6-v2 — a fully local model that requires no API key — and stores the embeddings in a ChromaDB persistent collection. When a query arrives, it is embedded with the same model, the top-3 most similar chunks are retrieved from ChromaDB using cosine similarity, and those chunks are injected into a Gemini 1.5 Flash prompt that instructs the model to answer only from the provided context. This approach reduces hallucination because the model is grounding its answer in retrieved document text rather than generating from training data alone, and the pipeline is updatable by simply changing the documents and re-running ingestion without touching the model.
```

---

# What Happens When `ask("How do I request a refund?")` Is Called

```text
Input: ask("How do I request a refund?")

Step 1 — Query Embedding:
    The query string "How do I request a refund?" is passed to
    SentenceTransformer("all-MiniLM-L6-v2").encode(["How do I request a refund?"])
    Output: a 384-dimensional numpy array (a list of 384 floats)

Step 2 — Vector Retrieval:
    collection.query(query_embeddings=[query_vector], n_results=3) is called
    ChromaDB computes cosine similarity between the query vector and all stored chunk vectors
    Returns the 3 chunks with the highest similarity scores
    Example returned chunks:
        Chunk 1: "Our refund policy allows customers to request a full refund within 30 days..."
        Chunk 2: "To request a refund: Submit a refund request through the Help Center..."
        Chunk 3: "Subscription refunds are prorated for the unused billing period..."

Step 3 — Prompt Construction:
    The 3 chunks are joined into a context string
    The prompt is assembled:
        "Answer the question using only the context provided below.
         Context:
         [Chunk 1 text]
         [Chunk 2 text]
         [Chunk 3 text]
         Question: How do I request a refund?"

Step 4 — Gemini Generation:
    model.generate_content(prompt) is called on gemini-1.5-flash
    The model reads the assembled prompt and generates a response grounded in the context
    Example output: "To request a refund, submit a request through the Help Center with
    your order ID and reason. Refunds are processed within 5-7 business days. Full
    refunds are available within 30 days of purchase."

Step 5 — Return:
    The function returns:
    {
        "answer": "To request a refund, submit a request through the Help Center...",
        "retrieved_chunks": [
            "Our refund policy allows customers...",
            "To request a refund: Submit a refund request...",
            "Subscription refunds are prorated..."
        ]
    }
```

---

# What AI Was Used For + What Engineers Must Still Do

**What AI was used for:**
- Generating the initial `rag_pipeline.py` structure from Prompt 1
- Writing the document ingestion loop and the `collection.add()` call
- Constructing the prompt template with retrieved context
- Adding the `try/except` blocks for error handling
- Generating the sample document constants

**What engineers must still do:**
- Verify that the ChromaDB collection is actually being populated (check `collection.count()` after ingestion)
- Test that retrieval is returning relevant chunks, not random ones
- Confirm that the Gemini prompt is formatted correctly so the model actually uses the context
- Check that `chroma_db/` persists between runs and does not re-ingest on every call
- Run multiple test queries and inspect the retrieved chunks to evaluate retrieval quality
- Handle the edge cases that AI may have missed (empty query, API key missing, collection empty)
- Be able to explain the entire pipeline in an interview — AI generated the code but cannot explain your design decisions

---

# Common Issues and Fixes

## Issue 1: ChromaDB Duplicate ID Error on Re-Run

**Error message:**
```
chromadb.errors.UniqueConstraintError: IDs ['doc_0_chunk_0'] already exist in the collection.
```

**Why it happens:** The ingestion code runs every time the script starts, trying to add the same chunk IDs to the collection even though they were already added in a previous run. ChromaDB enforces unique IDs per collection.

**Fix:** Add a count check before ingesting. Only ingest if the collection is empty.

**What to ask AI:**

```text
My rag_pipeline.py throws a UniqueConstraintError when I run it a second time because the ingestion code tries to add duplicate IDs to ChromaDB. Fix the ingestion section to check collection.count() before calling collection.add(). If count > 0, skip ingestion and print a message. If count == 0, run ingestion normally.
```

---

## Issue 2: Retrieved Chunks Are Irrelevant or Empty

**Error message (no crash, but wrong behavior):**
```
Retrieved chunks: ['', '', '']
```
or chunks from completely unrelated documents.

**Why it happens:** One of two causes. Either the collection was not populated before querying (ingestion was skipped or failed silently), or the chunking produced empty strings (if the document had no `\n\n` separators, the whole document became one chunk and related paragraphs were not split).

**Fix:** Check `collection.count()` after ingestion and print the count. Print a sample chunk after ingestion to verify content. Add a filter to remove empty strings from chunks: `chunks = [c.strip() for c in doc.split("\n\n") if c.strip()]`.

**What to ask AI:**

```text
The retrieved chunks in rag_pipeline.py are empty or irrelevant. Help me debug this. Add a debug print after ingestion that shows collection.count() and the first 3 stored chunk IDs. Also add a filter to remove empty strings during chunking: chunks should only include non-empty strings after stripping whitespace.
```

---

## Issue 3: Gemini 429 Rate Limit During Multiple Queries

**Error message:**
```
google.api_core.exceptions.ResourceExhausted: 429 RESOURCE_EXHAUSTED
Quota exceeded for quota metric 'generate_content_free_tier_requests' and limit 'generate_content_free_tier_requests_per_minute_per_project_per_base_model'
```

**Why it happens:** The Gemini free tier allows 15 requests per minute for `gemini-1.5-flash`. Running 3+ queries in quick succession in the `__main__` block hits this limit.

**Fix:** Add `import time` and `time.sleep(4)` between queries in the main block. Wrap the `model.generate_content()` call in `try/except google.api_core.exceptions.ResourceExhausted` and return a graceful fallback.

**What to ask AI:**

```text
I am getting a 429 RESOURCE_EXHAUSTED error from Gemini when running multiple queries in rag_pipeline.py. Add two fixes:
1. In the __main__ block, add time.sleep(4) between each query to respect the free tier rate limit.
2. In the ask() function, wrap model.generate_content() in a try/except for google.api_core.exceptions.ResourceExhausted. On this exception, return {"answer": "Generation temporarily unavailable due to rate limit. Here are the retrieved chunks.", "retrieved_chunks": chunks}.
```

---

# Limitations of This Module

This pipeline is designed for learning and portfolio demonstration. In a production environment, the following would need to be addressed:

- **Static knowledge base:** Documents are hardcoded as Python string constants. Any policy change requires editing the source code and re-running ingestion. A production system would load documents from a file system, database, or CMS and detect when content changes.

- **No similarity score threshold:** ChromaDB always returns `n_results` chunks even if the query has no good match in the knowledge base. If all similarity scores are low (e.g., the user asked about something completely outside the support domain), the pipeline will still retrieve 3 chunks and generate an answer based on irrelevant context. A production system would check the similarity scores and trigger a fallback response when no chunk exceeds a minimum threshold (e.g., cosine similarity < 0.3).

- **No re-ranking:** The top-3 chunks are used in the order ChromaDB returns them. A cross-encoder re-ranker (such as a `cross-encoder/ms-marco-MiniLM-L-6-v2` model) would re-score the candidates and reorder them for better relevance before sending to the LLM.

- **Single-turn only:** The `ask()` function has no memory of previous queries. Multi-turn conversation would require a conversation history to be passed alongside the retrieved context.

- **No evaluation in the pipeline itself:** This module generates answers but does not measure whether they are correct. Session 5 adds this evaluation layer.

---

# Key Takeaways

1. **RAG is three steps, not one.** Embed → retrieve → generate. The retrieval step is what makes the answer grounded. If retrieval fails (wrong chunks), generation will produce a plausible-sounding wrong answer. Most RAG problems in production are retrieval problems, not generation problems.

2. **Local embeddings are a legitimate production choice.** `all-MiniLM-L6-v2` is used in real production RAG systems where data privacy, cost, or latency requirements make an API-based embedding service impractical. Knowing how to use it is a practical skill, not just an academic one.

3. **ChromaDB persistent storage separates ingestion from querying.** The ability to run ingestion once and query many times is fundamental to how RAG systems work at scale. The pattern of "ingest once, query many" is the same regardless of whether you use ChromaDB, Pinecone, Weaviate, or pgvector.

4. **What you can explain is more valuable than what you can run.** This module is intentionally kept simple — 8 documents, 3 retrieved chunks, one collection — so that every part of the pipeline is visible and explainable. A production RAG system would be more complex, but the core mechanism is identical to what you built today. The interview value comes from being able to describe exactly what happens between `ask("How do I get a refund?")` and the printed answer.

---

# Session 5 Preview

In Session 5, we will build `rag_evaluator.py` — an evaluation script that measures the quality of the RAG pipeline we built today.

**What we will build:**
- A set of test queries with known ground-truth answers
- A retrieval evaluation function that checks whether the correct chunk was retrieved in the top-3 results
- A faithfulness evaluation function that uses Gemini 1.5 Flash as a judge to score whether the generated answer is faithful to the retrieved context
- An evaluation loop that runs all test queries, collects scores, and writes results to `rag_eval_report.csv`

**What Session 5 requires from today:**
- `rag_pipeline.py` must exist and the `ask(query)` function must work correctly
- `chroma_db/` must exist with the support documents already ingested — Session 5 will import the `ask` function directly and reuse the same collection

**What you will be able to say after Session 5:**
"I built a RAG pipeline and then evaluated it — I measured retrieval precision at k=3 and used an LLM-as-judge approach to score faithfulness. I know the pipeline retrieves the correct chunk X% of the time and generates faithful answers Y% of the time."

That combination — built + evaluated — is the highest-value thing a fresher AI engineer can demonstrate in an interview.
