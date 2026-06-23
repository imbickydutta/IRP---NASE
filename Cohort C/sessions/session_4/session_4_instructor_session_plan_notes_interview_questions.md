# Session 4 Instructor File: Basic RAG Pipeline

## Session Title

Build a Complete RAG Pipeline: Embeddings, Vector Storage, and Grounded Generation

## Duration

2 hours

## Portfolio Module

Module 4 of 8 — rag_pipeline.py

## Objective

By the end of Session 4, students will have built a complete Retrieval-Augmented Generation pipeline from scratch in a single Python script. They will understand how embeddings work, why chunking matters, what ChromaDB stores, how top-k retrieval works, and why grounded generation produces more accurate answers than a vanilla LLM call.

## Deliverable

- `rag_pipeline.py` — standalone Python script with all pipeline logic and an `ask(query)` function
- `chroma_db/` — local persistent ChromaDB folder created automatically when the script runs

---

## Strict Scope Control

### Include

- `rag_pipeline.py` as the single deliverable script
- 6–8 support documents defined as Python string constants inside the script
- Paragraph-level chunking by splitting on double newline `\n\n`
- Embedding generation using `sentence-transformers` library with model `all-MiniLM-L6-v2` — fully local, no API key required
- ChromaDB local persistent collection stored in `chroma_db/` folder using `PersistentClient`
- Top-3 chunk retrieval using ChromaDB's `collection.query()` method with `n_results=3`
- Grounded answer generation using Gemini 1.5 Flash with retrieved context injected into the prompt
- `ask(query)` as the main callable function that accepts a query string and returns a dict with `answer` and `retrieved_chunks`
- Printing both the generated answer and the retrieved chunks to the terminal for transparency
- A brief comparison: same query run with RAG vs. a vanilla Gemini call to show the quality difference

### Do Not Include

- PDF upload, file parser, or document loader of any kind
- Hybrid search combining keyword and semantic search
- Re-ranking of retrieved results using a cross-encoder
- Multiple ChromaDB collections
- FastAPI, Flask, or any web server
- OpenAI embeddings API or any paid embedding API
- Complex chunking strategies such as sliding window, sentence-level splitting, or token-based chunking
- Any UI, frontend component, or Gradio/Streamlit interface
- Document metadata filtering
- Production-grade logging or external monitoring services

---

# Instructor Framing

## Opening Message

Show the portfolio folder at the start of the session. Students should see these files already present from previous sessions:

```
structured_output_engine.py      ← Session 1: Structured Output Prompt Engine
output_examples.json             ← Session 1
llm_logger.py                    ← Session 2: LLM Logging and Evaluation Tracker
llm_logs.csv                     ← Session 2
eval_summary.json                ← Session 2
ai_handler.py                    ← Session 3: Serverless-Style AI Function
.env.example                     ← Session 3
```

Tell students: Today we are building the most technically substantial module in the portfolio. RAG is asked in almost every AI engineering interview at every level. By the end of this session, you will not just have run a RAG pipeline — you will be able to explain every line of it, every step in the flow, and every trade-off it makes.

## Key Philosophy

Students do not need to memorize embedding math or transformer architecture theory.

They need to be able to explain:

- what an embedding is and why it captures semantic meaning better than keyword matching
- why a vector database stores embeddings alongside text rather than just the text itself
- why we retrieve relevant chunks before generating instead of asking the LLM directly
- what changes in the answer quality between a RAG call and a vanilla LLM call

The ability to explain this system clearly and accurately is worth more in an interview than having built a more complex system you cannot describe in detail.

## Repeated Instructor Line

"We are not building a product today. We are building understanding. The code is the vehicle — the explanation is the destination."

---

# Session Flow

## 0–10 min: Opening, Portfolio Recap, Show Existing Scripts in Folder

### Instructor Goal

Establish continuity with previous sessions and build motivation for today's module.

### Steps

Open the terminal and run `ls` in the project folder. Show students all files built in Sessions 1, 2, and 3. Name each file and state what it does in one sentence — do not spend more than 30 seconds per file. Point out that the portfolio is growing one artifact per session.

Ask students verbally: "What does `ai_handler.py` do?" and "What pattern did we use in Session 3?" This warms them up for the function-based pattern they will use again today. (Session 3 — Serverless-Style AI Function (local handler pattern established) — introduced the single-function handler design that `rag_pipeline.py` follows with its `ask()` function.)

Tell students that today's session adds two new artifacts to the portfolio: `rag_pipeline.py` and `chroma_db/`. Explain that `chroma_db/` is a folder, not a script — it is created automatically by the code.

Ask: "Has anyone heard of RAG in an interview, a job description, or a course?" Let 2–3 students answer. Use their framing to set up the session — if a student says "it helps LLMs use your own data," build on that.

Make the point: Session 4 is the module interviewers ask about most. It covers embeddings, vector databases, retrieval, and grounded generation all in one pipeline.

---

## 10–20 min: Concept Explanation — What Are Embeddings and Why Do They Matter

### Instructor Goal

Give students a solid conceptual foundation before touching any code. Do not open any editor during this block.

### Explain: What Is an Embedding?

An embedding is a list of numbers — called a vector — that represents the meaning of a piece of text. It is produced by a transformer encoder model. The `all-MiniLM-L6-v2` model produces a 384-dimensional vector for any input string.

The key property: texts with similar meanings produce vectors that are close together in 384-dimensional space. Closeness is measured using cosine similarity — the higher the cosine similarity score, the more semantically similar the two texts are.

Give this example to make it concrete:

```
"I want a refund"  →  embedding vector A
"How do I get my money back?"  →  embedding vector B
cosine_similarity(A, B)  ≈  0.92  (very similar)

"I want a refund"  →  embedding vector A
"Two-factor authentication setup"  →  embedding vector C
cosine_similarity(A, C)  ≈  0.08  (very different)
```

Keyword search would fail to connect "refund" and "money back" because there is no word overlap. Embedding search succeeds because it captures meaning, not words.

### Explain: The Three-Step RAG Pipeline

Write or draw this on the board:

```
Step 1 — Ingestion (done once):
    Documents → chunk by paragraph → embed each chunk → store in ChromaDB

Step 2 — Retrieval (per query):
    User query → embed query → find top-3 similar chunks in ChromaDB

Step 3 — Generation (per query):
    Top-3 chunks + user query → build prompt → send to Gemini → return grounded answer
```

Ask 2–3 students to repeat the three-step flow in their own words before moving on.

---

## 20–35 min: Build the Module Using Claude Code or Cursor

### Instructor Goal

Use an AI coding tool to generate `rag_pipeline.py` from Prompt 1 in the student file.

### Steps

Open Claude Code or Cursor. Paste Prompt 1 from the student pre-session file (the main build prompt). Watch the AI generate `rag_pipeline.py`. Do not interrupt the generation.

After the file appears, do a quick visual scan before running anything. Check for these five elements:

1. Document string constants defined at the top of the file
2. `from sentence_transformers import SentenceTransformer` present in imports
3. `chromadb.PersistentClient(path="chroma_db")` used (not the in-memory client)
4. `collection.query(query_embeddings=[...], n_results=3)` called for retrieval
5. Retrieved chunks injected into the Gemini prompt as a context string

If any of these are missing, use Prompt 2 (the improvement prompt) before the walkthrough. Do not walk through or demo broken or incomplete code.

Run the script once in the terminal: `python rag_pipeline.py`. Confirm it completes without error and that `chroma_db/` folder is created. Show students the folder using `ls chroma_db/`.

### What to Watch For

- The sentence-transformers model will download (~90MB) on first run if not already cached. Tell students this is expected — it is a one-time download.
- If the Gemini API key is missing, the script will fail at the generation step. Fix in the terminal before the walkthrough.
- The `chroma_db/` folder should contain a `chroma.sqlite3` file after the first run.

---

## 35–50 min: Walk Through Generated Code — Explain Every Function

### Instructor Goal

Build student understanding of the generated code section by section. Students should be able to explain every part by the end of this block.

### Walkthrough Structure

Go through `rag_pipeline.py` top to bottom. For each section, explain what it does and why it is written that way:

**Document constants:**
Why string constants instead of loading files? Simplicity and portability — the script runs anywhere without needing external data files. Mention that in production, you would load from a database or file system.

**Paragraph chunking with `split("\n\n")`:**
What is a chunk? It is one small piece of the document. Why split on `\n\n`? Because that is the paragraph separator in plain text. Why not embed the whole document? Because we want to retrieve the specific paragraph that answers the query, not the whole document.

**`SentenceTransformer("all-MiniLM-L6-v2")`:**
What does this line do? It loads a pre-trained encoder model from the sentence-transformers library. What does it produce? A 384-dimensional embedding vector for any input string. Why is it local? No API call — the model weights are on the student's machine after first download.

**`chromadb.PersistentClient(path="chroma_db")`:**
What does persistent mean? The data is saved to disk at the given path. What is stored? The embedding vectors, the chunk text, and the chunk IDs. What happens if you use `Client()` instead? Data disappears when the Python process ends.

**`collection.add(ids=..., embeddings=..., documents=...)`:**
What are IDs? Unique string identifiers for each chunk — like `"doc_0_chunk_2"`. What happens if you try to add the same ID twice? ChromaDB raises a `UniqueConstraintError`.

**`collection.query(query_embeddings=[query_vec], n_results=3)`:**
What does this do? It computes cosine similarity between the query vector and every stored embedding, then returns the top 3 most similar chunks. What does the return value look like? A dictionary with nested lists: `result["documents"][0]` is the list of chunk strings.

**Prompt construction:**
How are retrieved chunks inserted into the Gemini prompt? They are formatted as a string and appended before the user's question. Why instruct the model to answer only from context? Without this instruction, the model may blend retrieved content with training data.

**Gemini generation call:**
Which model? `gemini-1.5-flash`. How is the API configured? `genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))`. Point to Session 2 and Session 3 — students have used this same setup before.

**The `ask(query)` function:**
This wraps the entire retrieval-and-generation pipeline. It is the public API of the module. Ask a student to describe what it accepts (a string) and what it returns (a dict with `answer` and `retrieved_chunks`).

### Ask Students During Walkthrough

Ask two students to each explain one section in their own words.

---

## 50–65 min: Student Follow-Along Build

### Instructor Goal

Every student builds their own working `rag_pipeline.py`.

### Student Task

Students open their own Claude Code or Cursor, paste Prompt 1 from the student pre-session file, and generate their own `rag_pipeline.py`.

### Instructor Support Areas

Watch for and assist with:

- `pip install sentence-transformers` not run before the session — direct students to install it and re-run
- ChromaDB collection already exists error from a previous test — add a `collection.count()` check or delete the `chroma_db/` folder
- Gemini API key not exported in the current shell — help students run `export GEMINI_API_KEY=...` in the terminal
- AI-generated code that uses `chromadb.Client()` (in-memory) instead of `PersistentClient` — have them prompt for the fix

### Confirm Success

Once a student's script runs, ask them to confirm:

1. Output prints retrieved chunks and a generated answer
2. `chroma_db/` folder was created
3. `ls chroma_db/` shows `chroma.sqlite3`

### If a Student Finishes Early

Direct them to Prompt 6 (test case generation) in the student file — run 3 additional custom queries and observe how the retrieved chunks change for different question types.

### Do Not Allow at This Stage

Do not let students add PDF parsing, metadata, re-ranking, or new functions during the follow-along block. The goal is a working baseline pipeline. Improvements come later.

---

## 65–80 min: Test with Sample Inputs, Inspect Output Files

### Instructor Goal

Demonstrate what a working RAG pipeline looks like across multiple query types, and show students how to read the output.

### Recommended Test Queries

Run all of these live and show the output for each:

1. "How do I request a refund?"
2. "My login is not working"
3. "What happens when my payment fails?"
4. "How do I cancel my subscription?"
5. "Can I delete my account permanently?"

For each query, point out:

- Which document each retrieved chunk came from
- Whether the retrieved chunks are actually relevant to the query (they should be)
- Whether the generated answer accurately reflects the retrieved content

### The Most Important Demonstration in the Session

Run the same query — for example, "How do I get a refund?" — in two ways:

1. Using `ask("How do I get a refund?")` — show the RAG answer with retrieved context
2. Using a direct Gemini call with no context — `model.generate_content("How do I get a refund?")`

Compare the two answers side by side. The RAG answer will reference the specific 30-day policy from the knowledge base. The vanilla LLM answer will be generic or slightly different. This is the visual proof of why RAG matters.

### Student Exercise

Have students run at least 3 different queries on their own machines and show you the terminal output before the session moves on.

---

## 80–95 min: Edge Cases, Error Handling, Failure Modes

### Instructor Goal

Build robustness awareness. Students should know what can go wrong and how to handle it.

### Use Prompt 7

Use the edge case prompt from the student file to guide this block. Discuss and add handling for:

- Empty query string — return early without calling ChromaDB or Gemini
- Gemini API rate limit 429 — wrap `generate_content()` in `try/except google.api_core.exceptions.ResourceExhausted`, return retrieved chunks with a message
- ChromaDB collection already populated — check `collection.count()` before `collection.add()` to skip re-ingestion
- sentence-transformers model download failing on first run — catch `OSError` and instruct the user to check their pip install

### Run the Experiment

Send a query about a topic not covered in any of the 8 documents. For example: "What programming languages does the product support?" or "How do I upgrade my plan?"

Ask students: what should happen? The retrieval step will return the closest chunks even if they are not very relevant (ChromaDB always returns n_results chunks regardless of relevance score). The generation step may produce a vague or off-topic answer, or may correctly note that the provided context does not cover the question.

Discuss: how would you detect and handle this in production? Introduce the concept of a similarity score threshold — if all retrieved chunks score below a minimum threshold, do not generate. Instead, return a "I don't have information about that" fallback.

### Ask Students

What would happen if `collection.query()` returned zero results? Walk through the code path: `result["documents"][0]` would be `[]`, joining it would produce an empty string, the prompt would say "Context: " with nothing after it, and the model would generate from its training data. This is a silent failure mode.

---

## 95–105 min: Concept Pause — Explain the Full RAG System

### Instructor Goal

Stop coding entirely. Convert implementation into interview-level understanding.

### Ask Students to Close Laptops

Do a verbal concept review. Ask one student to define each concept before you explain it:

**Embeddings:**
Vectors that represent semantic meaning, produced by a transformer encoder model such as all-MiniLM-L6-v2. Two semantically similar texts produce embedding vectors with high cosine similarity even if they share no words.

**Vector Database:**
A database that stores embedding vectors alongside text and IDs, and enables similarity search by comparing a query vector against all stored vectors. ChromaDB is a local example. Pinecone and Weaviate are cloud examples.

**Chunking:**
Splitting a document into smaller pieces before embedding. Paragraph-level splitting on `\n\n` is the approach used here. The trade-off: chunks that are too small lose context; chunks that are too large reduce retrieval precision.

**Top-k Retrieval:**
Retrieving the k most similar stored chunks for a given query. `n_results=3` means retrieve 3 chunks. Higher k increases recall but dilutes the prompt. Lower k is more focused but risks missing relevant content.

**Grounded Generation:**
Injecting retrieved chunk text into the LLM prompt and instructing the model to base its answer on that context rather than its training data. This is how RAG reduces hallucination.

**RAG vs. Vanilla LLM:**
A vanilla LLM call answers from training data alone — generic and potentially hallucinated for specific questions. RAG grounds the answer in retrieved documents — more accurate for domain-specific questions and updateable without retraining.

### Student Writing Task

Ask every student to write one sentence about each of the six concepts from memory. Give them 3 minutes.

---

## 105–115 min: Interview Discussion and Viva Practice

### Instructor Goal

Prepare students to speak fluently about this module in an interview setting.

### How to Run This Block

Pick 3 questions from the Basic set below, 2 from the Technical Deep-Dive set, and 1 from the Production set.

Do not read the expected answers aloud before asking the question. Let students attempt each answer first. After a student answers, fill in any technical detail they missed.

Focus especially on these questions, as they are most frequently asked at the fresher-to-junior level:

- Q3 (chunking), Q5 (ask() function), Q7 (top-k trade-off), Q9 (ChromaDB.query() internals), Q12 (production failure modes)

### Verbal Exercise

Ask each student to deliver the 3-sentence final explanation from the student pre-session file without looking at their notes. The explanation should cover: what they built, how the pipeline works, and why RAG reduces hallucination.

---

## 115–120 min: Wrap-Up, Show rag_pipeline.py and chroma_db/, Preview Session 5

### Instructor Closing

Open the terminal. Run `ls` in the project folder and confirm `rag_pipeline.py` is present. Run `ls chroma_db/` and show `chroma.sqlite3` inside. Run `python -c "import chromadb; c = chromadb.PersistentClient(path='chroma_db'); col = c.get_collection('support_docs'); print(col.count(), 'chunks stored')"` to show students the number of chunks in the collection.

The portfolio now has 4 modules. Tell students the key fact for Session 5: do not delete `rag_pipeline.py` or `chroma_db/` — Session 5 will import the `ask()` function directly from this file and reuse the same ChromaDB collection.

Session 5 — RAG Evaluation and Improvement — is next. Students will measure how good the pipeline they built today actually is — retrieval precision, faithfulness scoring, and LLM-as-judge evaluation. The evaluation script they write in Session 5 will call `ask()` from today's `rag_pipeline.py`.

---

# Instructor Notes

## What to Emphasize

Session 4 is the most technically dense session in the portfolio. The instructor's job is not to cover every possible RAG feature — it is to ensure students can explain the minimal working pipeline completely.

Emphasize three things above all others:

First, the difference between embedding search and keyword search. If students only retain one concept from this session, it should be that cosine similarity on embedding vectors can match semantically similar texts even when they share no words. Keyword search cannot do this.

Second, why chunking exists. The entire RAG architecture depends on the idea that we retrieve relevant pieces of a document, not whole documents. Without chunking, retrieval would return an entire policy document when the user only needs one paragraph.

Third, why the retrieved chunks go into the prompt as a string. Students sometimes imagine the LLM is "connected to" ChromaDB. It is not. The retrieved text is copied into the prompt string, and the model reads it as part of its input context. This distinction matters for understanding why prompt construction is a critical engineering step.

## Common Student Mistakes

1. **`ModuleNotFoundError: No module named 'sentence_transformers'`**

   Students forget to install before running. Fix: `pip install sentence-transformers`. Note carefully: the PyPI package name is `sentence-transformers` (hyphen) but the Python import uses `sentence_transformers` (underscore). These are the same package. Students sometimes try `pip install sentence_transformers` with an underscore and get confused when it does not resolve.

2. **`chromadb.errors.UniqueConstraintError: IDs ['doc_0_chunk_0'] already exist in the collection`**

   Students run the ingestion code twice — once successfully, then again when they restart the script. ChromaDB enforces unique IDs per collection. Fix: add a guard: `if collection.count() > 0: print("Already ingested, skipping"); else: collection.add(...)`. Alternatively, delete the `chroma_db/` folder to start fresh.

3. **`ValueError: GEMINI_API_KEY not found` or silent None**

   Students set the key in a `.env` file but never load it into the environment. The script reads `os.environ.get("GEMINI_API_KEY")` which only works if the variable is actually exported in the shell session. Fix: run `export GEMINI_API_KEY="..."` in the terminal before running the script. Alternatively, use `python-dotenv` and call `load_dotenv()` at the top of the script.

4. **Empty retrieval results: `{'documents': [[]], 'ids': [[]]}`**

   Students run `ask()` before the ingestion block has executed. This happens when the script is structured so that ingestion is only run in the `__main__` block, but the student calls `ask()` from a different context. Fix: ensure that ingestion is triggered at module load time or at the start of `ask()` with a count check.

5. **`google.api_core.exceptions.ResourceExhausted: 429 RESOURCE_EXHAUSTED`**

   The Gemini free tier allows 15 requests per minute for `gemini-1.5-flash`. Running 3–5 test queries quickly in a loop hits this. Fix: add `import time` and `time.sleep(4)` between calls in the main block. Wrap `model.generate_content()` in `try/except google.api_core.exceptions.ResourceExhausted` with a graceful fallback.

6. **Sentence-transformers model download appears to hang**

   On first run, `SentenceTransformer("all-MiniLM-L6-v2")` downloads approximately 90MB of model weights from Hugging Face. Students may think the script is frozen. Fix: tell them to wait for the progress bar to complete. It will not download again on subsequent runs. Pre-download before class if bandwidth is unreliable by running: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"`.

7. **ChromaDB dimension mismatch error**

   If a student previously created a `chroma_db/` collection using a different embedding model (different number of dimensions), querying with 384-dimensional all-MiniLM vectors will fail with an embedding dimension error. Fix: delete the `chroma_db/` folder entirely and re-run the script from scratch: `rm -rf chroma_db/`.

8. **`result['documents'][0]` returns a list, not a string**

   Students expect `result['documents']` to be a list of strings directly. But ChromaDB returns a nested structure: `result['documents']` is a list of lists (one list per query). For a single query, the chunks are at `result['documents'][0]`. Students who do `for chunk in result['documents']:` will iterate over the outer list and get a list of strings per iteration, not a single string. Fix: always access `result['documents'][0]` to get the flat list of chunk strings for the single query.

9. **Gemini prompt produces an answer that ignores the context**

   This happens when the prompt instruction does not clearly tell the model to use only the provided context. If the prompt says "Answer the question: [context] [question]" without clear framing, the model may blend context with training data. Fix: rewrite the prompt to start with an explicit instruction: "You are a support assistant. Answer the following question using ONLY the context provided below. Do not use information outside the provided context."

10. **`ask()` function only returns a string, not a dict**

    AI-generated code sometimes returns only `response.text` from the `ask()` function rather than the required `{"answer": ..., "retrieved_chunks": [...]}` dictionary. Students then cannot display the retrieved chunks in the output, which breaks the transparency requirement of the module. Fix: check the `ask()` return statement and ensure it always returns a dictionary with both keys.

## How to Control the Session

The biggest risk in Session 4 is scope creep. Students will want to add:

- PDF upload and parsing
- A Gradio or Streamlit UI
- Multiple ChromaDB collections (one per document type)
- Metadata filtering on retrieval
- Re-ranking with a cross-encoder
- LangChain or LlamaIndex integration

Redirect every such request with: "That is a great idea for a production system. Write it down as a potential improvement. Today we are building the minimal working pipeline that you can fully explain in an interview. A simple system you understand completely is worth more than a complex system you cannot describe."

Do not let the code grow beyond what students can explain line by line. The interview value of this module comes from explainability, not complexity.

---

# Questions to Discuss: Interview Perspective

## Basic Module Questions

### Q1. What is a RAG pipeline and why is it useful?

Expected answer: RAG stands for Retrieval-Augmented Generation. It is a technique where, instead of relying only on an LLM's training data, you retrieve relevant documents from a knowledge base and inject them into the prompt before generating an answer. This is useful because it reduces hallucination — the model grounds its answer in actual retrieved text rather than generating from memory. It also makes the system updatable: you can change the knowledge base without retraining the model. In this module, the knowledge base is a set of 6–8 customer support documents stored as chunks in a ChromaDB local persistent collection.

### Q2. What is an embedding and what does cosine similarity measure?

Expected answer: An embedding is a dense vector — a list of floating-point numbers — that represents the semantic meaning of a text. It is produced by passing text through a transformer encoder model. For `all-MiniLM-L6-v2`, each embedding is a 384-dimensional vector. Cosine similarity measures the angle between two vectors in this 384-dimensional space: a score near 1.0 means the vectors point in nearly the same direction and the texts are semantically similar, while a score near 0.0 means they are semantically unrelated. This captures meaning rather than word overlap — "I want a refund" and "how do I get my money back" have high cosine similarity because they express the same intent, even though they share no keywords.

### Q3. What is chunking and why do we chunk documents?

Expected answer: Chunking is the process of splitting a document into smaller pieces before embedding and storing them in the vector database. We chunk for two reasons: embedding models have a maximum token input length, and retrieving a focused paragraph is more precise than retrieving an entire document. If an entire 500-word policy document were embedded as one vector, that vector would average out all the topics in the document, making retrieval less precise. In this module, we split on double newline `\n\n`, which separates natural paragraph breaks — a simple but effective strategy for structured support documents. The trade-off is that chunks that are too small lose context, while chunks that are too large reduce retrieval precision.

### Q4. What does ChromaDB store and what is a persistent collection?

Expected answer: ChromaDB stores embedding vectors alongside their corresponding text (the chunk content) and a unique string ID for each chunk. When you initialize ChromaDB with `PersistentClient(path="chroma_db")`, it creates a SQLite-backed store on disk at the specified path. This means the collection persists between Python script runs — you do not need to re-embed and re-insert all documents every time the script is executed. The `chroma_db/` folder contains a `chroma.sqlite3` file that holds all the stored embeddings and their associated text. This is in contrast to the in-memory `Client()`, which loses all data when the Python process ends.

### Q5. What does the `ask(query)` function do step by step?

Expected answer: The `ask(query)` function takes a natural language query string as input and performs three steps in sequence. First, it embeds the query using the same `SentenceTransformer("all-MiniLM-L6-v2")` model used to embed the documents, producing a 384-dimensional query vector. Second, it calls `collection.query(query_embeddings=[query_vector], n_results=3)` to find the 3 stored chunks whose embeddings are most similar to the query vector — this comparison is done internally by ChromaDB using cosine similarity. Third, it constructs a prompt string that includes the retrieved chunks as context, adds the user's question, and calls Gemini 1.5 Flash via `google-generativeai` to generate a grounded answer. The function returns a dictionary with keys `"answer"` and `"retrieved_chunks"` so the caller can inspect both the generated text and the evidence it was based on.

---

## Technical Deep-Dive Questions

### Q6. Why use `sentence-transformers` instead of the OpenAI embeddings API?

Expected answer: `sentence-transformers` runs entirely locally — there is no API call, no network latency, no cost per request, and no API key required for the embedding step. The `all-MiniLM-L6-v2` model is a highly efficient transformer encoder that produces strong 384-dimensional embeddings for semantic similarity tasks. It is well-benchmarked on the MTEB (Massive Text Embedding Benchmark) and works well for retrieval tasks involving short to medium-length text. Using a local embedding model also means the ingestion and retrieval steps can run fully offline, which matters for data privacy or cost-sensitive use cases. The trade-off is dimensionality and capacity: all-MiniLM-L6-v2 produces 384 dimensions, while OpenAI's `text-embedding-3-small` produces 1536 dimensions and may capture more nuanced semantic distinctions — but for a support document retrieval task with clear, focused text, the practical difference is small.

### Q7. What is the trade-off between retrieving 1 chunk vs. 10 chunks (top-k)?

Expected answer: Retrieving more chunks (higher k) increases recall — you are less likely to miss a relevant piece of information if the knowledge base has multiple documents partially relevant to the query. But it also increases the amount of text injected into the prompt, which raises token cost, may dilute the most relevant content with less relevant material, and can confuse the model with contradictory context. Retrieving fewer chunks keeps the prompt focused and reduces cost but risks missing relevant context when the best answer is in the 4th or 5th ranked chunk. In this module, `n_results=3` is a practical middle ground for a small knowledge base of 6–8 documents. In production RAG systems, k is treated as a tunable hyperparameter evaluated with retrieval metrics like recall@k and NDCG (Normalized Discounted Cumulative Gain).

### Q8. What would happen if you ran the same query with a vanilla Gemini call instead of the RAG pipeline?

Expected answer: A vanilla Gemini call — passing only the user's question with no retrieved context — forces the model to answer from its training data alone. For a general question like "how do I cancel a subscription," the model may give a plausible generic answer that does not match this company's specific policy details. For a company-specific question like "what is the exact refund window in this company's policy," the model has no training data and will either hallucinate a specific number or admit it does not know. The RAG pipeline fixes this by providing the exact policy text as context. The model reads the retrieved chunks as part of its input and generates an answer that directly cites the content. This is why RAG is described as reducing hallucination — the model is grounding its output in real retrieved documents rather than generating from memory.

### Q9. How does ChromaDB's `.query()` method find the most similar chunks?

Expected answer: When you call `collection.query(query_embeddings=[query_vector], n_results=3)`, ChromaDB computes similarity between the query vector and every stored embedding vector in the collection, then returns the top 3 with the highest similarity scores. By default, ChromaDB uses cosine similarity (specifically, it computes L2 distance on normalized vectors, which is mathematically equivalent to cosine similarity for unit-norm vectors). For small collections like the one in this module, this is an exact nearest-neighbor search — every stored vector is compared. For large collections with millions of vectors, ChromaDB can use approximate nearest-neighbor (ANN) indexing via HNSW for faster search at a small accuracy cost. The returned object is a dictionary with nested lists: `result['documents'][0]` gives the list of chunk text strings, and `result['ids'][0]` gives their corresponding IDs.

### Q10. How is the retrieved context injected into the Gemini prompt?

Expected answer: The retrieved chunks are formatted as a plain text string and concatenated into the prompt template before the user's question. A typical pattern looks like this: the prompt begins with an instruction such as "You are a support assistant. Answer the question using only the context provided below. Do not use information outside the context." Then the chunks are listed under a "Context:" heading, and the user's question follows under a "Question:" heading. This prompt engineering step is critical — without the explicit instruction to use only the provided context, the model may blend retrieved content with its training data in ways that are difficult to detect. In the `google-generativeai` library, the assembled prompt string is passed directly to `model.generate_content(prompt_string)`. There is no system prompt parameter in the basic API — the instruction is embedded as part of the single prompt string.

---

## Production and System Design Questions

### Q11. How would you scale this pipeline to handle 10,000 documents instead of 8?

Expected answer: With 10,000 documents, the pipeline would need several changes. The ingestion process must become a separate one-time setup job, not inline with the query function — re-embedding 10,000 documents on every script run would take minutes. ChromaDB's default exact search would slow down as the collection grows; enabling HNSW approximate nearest-neighbor indexing would restore fast query times. The sentence-transformers model still works locally for this scale but encoding should be batched: `model.encode(list_of_chunks, batch_size=64)` is much faster than encoding one chunk at a time. Each chunk should also store metadata — the document name, section title, and last-updated timestamp — so you can filter by metadata before running vector search (for example, only search chunks from documents updated in the last 90 days). Finally, ingestion would need incremental update logic: detect which documents changed, delete the stale embeddings from ChromaDB by ID, and add the new ones.

### Q12. What breaks in production RAG that does not break in this module?

Expected answer: Several failure modes are invisible at the small scale of this module but become critical in production. Knowledge base staleness is the first: these documents are static Python string constants, but real support policies change quarterly. A production system needs a change-detection process that identifies updated documents, removes stale embeddings from ChromaDB, and inserts fresh ones. Retrieval failures are the second: if the user's query is very different in phrasing from anything in the knowledge base, the top-3 results may all be irrelevant — ChromaDB will return chunks regardless of how low the similarity scores are. A production system checks the returned similarity scores and triggers a "I don't have information about that" fallback when all scores are below a threshold (for example, 0.3). Context window management is the third: very large chunks or a high k value can make the assembled prompt exceed the model's useful context window, degrading generation quality.

### Q13. How would you monitor this RAG pipeline in production?

Expected answer: Monitoring a RAG pipeline requires tracking two separate quality dimensions: retrieval quality and generation quality. For retrieval quality, you would log each query, the IDs and similarity scores of the retrieved chunks, and a human relevance label (correct or incorrect). From these logs you compute precision@3 (what fraction of the top-3 retrieved chunks were actually relevant to the query) and recall@3 (what fraction of all relevant chunks appeared in the top-3). For generation quality, you use an LLM-as-judge approach: for each query-answer pair, pass the question, the retrieved context, and the generated answer to a second LLM call that scores whether the answer is faithful to the context (faithfulness score) and whether it correctly answers the question (answer correctness score). Both sets of metrics are written to a log file or dashboard. This exact evaluation approach is what we build in Session 5 using `rag_evaluator.py`.

### Q14. What would you change about the chunking strategy for a production support system?

Expected answer: Paragraph splitting on `\n\n` is a practical starting point but has two main weaknesses for a production system. First, paragraph length is highly variable — one paragraph might be 2 sentences and another 20, leading to unequal embedding quality. A fixed-size token chunking strategy with overlap (for example, 256 tokens per chunk with 50 tokens of overlap between adjacent chunks) gives more uniform representation and reduces the risk of splitting a relevant sentence across two chunks. Second, later chunks in a document lose the contextual header — a chunk about "refund timing" may be retrieved without the reader knowing it came from the "30-Day Refund Policy" document. Parent-child chunking solves this: store small chunks for retrieval but attach the parent section header as metadata, and send the full parent section as context to the LLM. For a real support knowledge base, each chunk should also carry metadata fields (document title, policy version, last updated date) to enable pre-filtering before vector search.

### Q15. What is the difference between this RAG approach and fine-tuning Gemini on the same support documents?

Expected answer: Fine-tuning trains the model's weights on domain-specific examples, so the knowledge becomes baked into the model parameters. RAG retrieves knowledge at inference time from an external store without changing the model weights at all. Fine-tuning is better when you need the model to adopt a specific tone or format, learn unusual task structures, or internalize a very large corpus where retrieval would be impractical. RAG is better when the knowledge base changes frequently — fine-tuning would require a full retraining run every time a support policy changes, while RAG only requires updating the ChromaDB collection. RAG is also better when you need to cite sources: you can show the user exactly which chunks the answer was based on, which is not possible with a fine-tuned model. For a customer support use case where policies are updated quarterly, RAG is almost always the right architectural choice over fine-tuning because it decouples knowledge from model training.

---

# Session 4 Completion Checklist

Students should be able to confirm all of the following by end of session:

- [ ] `rag_pipeline.py` exists in the portfolio folder and runs without errors using `python rag_pipeline.py`
- [ ] `chroma_db/` folder is created automatically when the script runs and contains a `chroma.sqlite3` file
- [ ] All 6–8 support documents are defined as Python string constants inside the script — no external files required
- [ ] Paragraph chunking splits documents on `\n\n` and produces at least 15 total chunks across all documents
- [ ] Embeddings are generated using `SentenceTransformer("all-MiniLM-L6-v2")` from the `sentence-transformers` library — no OpenAI API call is made
- [ ] ChromaDB is initialized with `PersistentClient(path="chroma_db")` and not the in-memory `Client()`
- [ ] `collection.query(query_embeddings=[...], n_results=3)` is used for retrieval and returns exactly 3 chunks per query
- [ ] The `ask(query)` function constructs a prompt that includes retrieved context and calls `gemini-1.5-flash` via `google-generativeai`
- [ ] The `ask(query)` function returns a dictionary with both `"answer"` (string) and `"retrieved_chunks"` (list of strings)
- [ ] Running `ask("How do I request a refund?")` prints the 3 retrieved chunks and a grounded answer in the terminal
- [ ] Gemini 429 rate limit error is handled with a `try/except` block so the script does not crash on quota exhaustion
- [ ] Student can explain the three-step RAG pipeline — embed, retrieve, generate — verbally without looking at notes

---

# Instructor Backup Plan

## If Gemini Rate Limit Hits During the Demo

The free tier of Gemini 1.5 Flash has a rate limit of 15 requests per minute and 1 million tokens per day. If you hit a 429 error during the live demo, take these steps:

1. Switch to showing the retrieved chunks output only. ChromaDB retrieval does not call any external API and will always work regardless of Gemini quota.

2. Tell students: "This is the retrieval step working perfectly. The generation step is temporarily rate-limited. Notice that retrieval and generation are completely separate steps — one can fail independently of the other. In a production system, you would return the retrieved chunks with a fallback message if generation fails."

3. Add `import time` and `time.sleep(5)` between demo queries and continue when quota resets.

4. If the limit is fully exhausted for the session, run the concept pause block (Session Flow block 7) early and return to the generation demo at the end of class.

5. Never skip the interview discussion section even if the code demo is cut short — the conceptual explanation is the primary deliverable of Session 4.

## If a Student's Setup Fails

1. Do not stop class. Tell the student to follow the instructor screen and take notes.

2. Pair the student with a neighbor who has a working setup — they observe and share the keyboard during the follow-along block.

3. Quick diagnoses for common failures:
   - Wrong Python environment: run `python3 -c "import chromadb; import sentence_transformers; print('OK')"` to confirm the right environment
   - `sentence-transformers` installed in wrong env: run `which python3` and confirm pip is installing to the same Python binary
   - GEMINI_API_KEY not in environment: run `echo $GEMINI_API_KEY` in the terminal — if empty, run the export command

4. After class, share the completed `rag_pipeline.py` file so the student can run it independently.

5. The student must still complete the verbal interview explanation exercise before the session ends. Setup failure does not excuse conceptual understanding.

## If ChromaDB Throws Errors Across All Students

This sometimes happens with version conflicts between `chromadb` and its internal dependencies (`hnswlib`, `grpc`) on certain Python versions. Take these steps:

1. Quick fix: instruct all students to run `pip install chromadb==0.5.0 --force-reinstall` and re-run the script.

2. If that does not resolve the issue, switch to `chromadb.Client()` (in-memory) for the session by removing `path="chroma_db"` from the client initialization.

3. Explain to students: "The in-memory client works identically to the persistent client for everything we are doing today. The only difference is that data does not survive after the Python process ends. The architecture, the query logic, and the pipeline are identical."

4. Students can reproduce the persistent version independently after class once the version conflict is resolved.
