# Session 5 Instructor File: Add RAG Knowledge Base

## Session Title

Add RAG Knowledge Base: Embeddings, Vector Storage, and Grounded Response Suggestions

## Duration

2 hours

## Project

AI Support Ticket Resolution Copilot

## Session 5 Objective

By the end of Session 5, students will have extended the Support Ticket backend with a full Retrieval-Augmented Generation (RAG) pipeline. The pipeline ingests a static knowledge base of support documents, chunks and embeds them using the sentence-transformers all-MiniLM-L6-v2 model (local, no API key required), stores the vectors in a local persistent ChromaDB collection, and at request time retrieves the top-3 most relevant chunks to construct a grounded LLM response suggestion for any ticket.

Students will understand the difference between retrieval and generation, why grounding reduces hallucination, and how to expose the feature through a clean FastAPI endpoint.

## Session 5 Deliverable

A working `GET /tickets/{id}/suggested-response` endpoint that:

1. Loads the ticket from the database by ID
2. Queries ChromaDB for the top-3 relevant knowledge base chunks using cosine similarity on the ticket's subject and description
3. Injects those chunks as context into a Gemini chat completion prompt
4. Returns a structured JSON response containing `ticket_id`, `suggested_response`, and `sources` (the chunk IDs used)

The knowledge base is populated once at application startup from Python string constants. ChromaDB persists to disk across restarts.

---

## Strict Scope Control

### Include

- Static knowledge base as Python string constants in `app/knowledge_base/documents.py`
- Text chunking by paragraph (split on double newline `\n\n`) with a maximum chunk character length fallback
- sentence-transformers `all-MiniLM-L6-v2` for generating embeddings (384-dimensional vectors, local, no API key required)
- ChromaDB local persistent collection stored at `./chroma_db` directory
- `app/services/rag_service.py` module that owns all RAG logic: chunking, embedding (sentence-transformers), upserting, querying
- Top-3 cosine similarity retrieval from ChromaDB (ChromaDB handles cosine by default with `cosine` space)
- LLM call with retrieved context injected into the system or user prompt
- `GET /tickets/{id}/suggested-response` endpoint in `app/routes/tickets.py`
- Startup event in `main.py` that initialises the ChromaDB collection and populates it if empty
- Response model with `ticket_id`, `suggested_response`, and `sources` fields

### Do Not Include

- PDF or file upload pipeline for knowledge base ingestion
- Sentence-level or semantic chunking (spaCy, NLTK sentence tokenisers)
- Multiple ChromaDB collections (one collection named `support_kb` is sufficient)
- Re-ranking of retrieved chunks (cross-encoder, Cohere rerank)
- Hybrid search (BM25 + vector)
- Caching embeddings in PostgreSQL or Redis
- FAISS or any vector store other than ChromaDB
- Streaming LLM responses
- Asynchronous embedding generation (keep it synchronous at startup)
- LangChain or LangGraph wrappers (those come in Session 6)
- OpenAI embeddings API (use sentence-transformers locally instead)

Session 5 is specifically about understanding raw RAG mechanics. Abstraction layers come in Session 6.

---

# Instructor Framing

## Opening Message

Show the current codebase state before writing a single line of new code.

The project currently has:

- `app/main.py` — FastAPI app with lifespan/startup, CORS
- `app/models/ticket.py` — SQLModel `Ticket` table with `id`, `subject`, `description`, `status`, `priority`, `created_at`, `category` (added in Session 4)
- `app/models/user.py` — SQLModel `User` table with hashed password
- `app/routes/tickets.py` — CRUD endpoints: `POST /tickets`, `GET /tickets`, `GET /tickets/{id}`, `PUT /tickets/{id}`, `DELETE /tickets/{id}`
- `app/routes/auth.py` — `POST /auth/register`, `POST /auth/login` returning JWT
- `app/dependencies.py` — `get_current_user` dependency, `get_session` DB dependency
- `app/services/classifier.py` — LLM-based classifier that sets `category` on ticket creation
- `app/database.py` — SQLite engine + `create_db_and_tables()`
- `requirements.txt` — includes `fastapi`, `sqlmodel`, `google-generativeai`, `python-jose`, `passlib`

Tell students: today we are not touching auth, CRUD, or the classifier. We are adding one new capability on top: the ability to retrieve relevant knowledge and generate a grounded support response.

## Key Philosophy

RAG is one of the most important practical patterns in production AI systems. Every student in this cohort will encounter it in interviews and on the job. Today we are not using a framework — we are building the raw pipeline by hand so that when students later use LangChain or LlamaIndex they understand exactly what those libraries are hiding from them.

The mental model to reinforce:

- Retrieval is a search problem.
- Generation is an LLM problem.
- They are separate steps. Mixing them up in interviews is a red flag.

## Repeated Instructor Line

"Retrieval finds the right context. Generation uses that context. They are not the same step — do not confuse them."

---

# Session Flow

## 0–10 min: Opening and Recap of Session 4

### Instructor Goal

Ground students in what exists before adding anything new.

### Specific Actions

1. Open the project in the terminal. Run `uvicorn app.main:app --reload` and open Swagger at `http://127.0.0.1:8000/docs`.
2. Walk through the existing endpoints: hit `POST /tickets` live and show the response JSON — note that `category` is now auto-populated by the Session 4 classifier.
3. Show `app/services/classifier.py` briefly — remind students this calls Gemini with the ticket text and returns a category string that gets written to the DB.
4. State the gap: "We can classify a ticket. But we cannot suggest what the support agent should say. That requires knowledge. Today we add that knowledge layer."
5. Ask the class: "If a user says their payment failed, where does the support agent get their answer from?" Accept answers. Lead to: a knowledge base of standard operating procedures and policy documents.
6. Write on the board or share screen: "Session 5 adds: Knowledge Base → Embeddings → Vector DB → Retrieval → Grounded Generation."
7. Confirm every student has the project running locally and can hit the existing endpoints before proceeding.

---

## 10–20 min: Architecture Breakdown

### Instructor Goal

Ensure students understand the full RAG data flow before touching code.

### Specific Actions

1. Draw or display this pipeline on the whiteboard:

```
[Knowledge Base Documents]
        ↓ chunk by paragraph
[Text Chunks]
        ↓ sentence-transformers (local) all-MiniLM-L6-v2
[384-dim float vectors]
        ↓ upsert with metadata
[ChromaDB local persistent collection: support_kb]

--- at request time ---

[Ticket subject + description]
        ↓ embed with same model
[Query vector]
        ↓ cosine similarity top-3
[Retrieved chunks]
        ↓ inject as context into LLM prompt
[Gemini 1.5 Flash chat completion]
        ↓
[Suggested response + source chunk IDs]
        ↓ return via GET /tickets/{id}/suggested-response
```

2. Ask: "What is an embedding?" — accept answers. Correct answer: a dense numerical vector that encodes the semantic meaning of text, such that semantically similar texts have vectors close together in the vector space.
3. Ask: "What is cosine similarity?" — accept answers. Explain: it measures the angle between two vectors. Vectors pointing in the same direction (angle near 0) have cosine similarity near 1. It ignores magnitude and captures directional similarity, which is what we want for semantic search.
4. Explain the two-phase nature of RAG: ingestion (offline, or at startup) vs. retrieval+generation (online, per request).
5. Show the file structure we will create today:
   - `app/knowledge_base/documents.py`
   - `app/services/rag_service.py`
   - new imports and endpoint in `app/routes/tickets.py`
   - startup call in `app/main.py`
6. Emphasise: ChromaDB stores vectors on disk in `./chroma_db`. Between restarts, the collection persists. The startup code checks if the collection already has documents before re-embedding.

---

## 20–35 min: Build the Feature Using Antigravity

### Instructor Goal

Demonstrate how to use an AI coding tool to scaffold the RAG feature with a precise, scoped prompt.

### Specific Actions

1. Open Antigravity in the project directory.
2. Use Prompt 1 from the student pre-session file verbatim. Read it aloud before pasting so students understand the structure of a good engineering prompt.
3. Watch the generated output together. Before accepting, review:
   - Does `documents.py` contain 8–10 string constants, not a file loader?
   - Does `rag_service.py` import `chromadb`, `sentence_transformers`, `google.generativeai`, and chunk by `\n\n`?
   - Is the ChromaDB client created with `PersistentClient(path="./chroma_db")`?
   - Does the `get_or_create_collection` call specify `metadata={"hf:space": "cosine"}`?
   - Is the embedding call using `SentenceTransformer("all-MiniLM-L6-v2").encode()`?
   - Is the endpoint `GET /tickets/{id}/suggested-response` and does it return `ticket_id`, `suggested_response`, `sources`?
4. If the AI generates LangChain imports — stop and redirect. Explain this is a scope issue and re-prompt with an explicit "Do not use LangChain or LangGraph" constraint.
5. If the AI generates `openai.embeddings.create` — redirect to sentence-transformers.
6. Accept the generated code and immediately run the server. Show the startup log where ChromaDB is initialised.

---

## 35–50 min: Instructor Code Walkthrough

### Instructor Goal

Every student must understand what the AI generated before they are allowed to proceed to their own build.

### Walkthrough Sequence

1. **`app/knowledge_base/documents.py`** — Show 2–3 of the document constants. Point out they are plain Python strings, not files. Ask: "Why strings instead of files?" Answer: simplicity — no file I/O, no path dependencies, version-controlled with the codebase.

2. **Chunking logic in `rag_service.py`** — Walk through the chunk function. Explain: `doc.split("\n\n")` splits on blank lines (paragraph breaks). Point out the character-length fallback: if a chunk is longer than `MAX_CHUNK_SIZE` characters, split it further. Ask: "What is the risk of very large chunks?" (Diluted relevance, fewer chunks retrieved.)

3. **Embedding call** — Show the `SentenceTransformer("all-MiniLM-L6-v2").encode(texts)` call. Explain that this runs locally — no API key, no network call, no cost. It returns a NumPy array of 384-float vectors; call `.tolist()` to convert to plain Python lists for ChromaDB. Mention the model is 90MB and is downloaded once on first use.

4. **ChromaDB upsert** — Show `collection.upsert(ids=chunk_ids, embeddings=vectors, documents=texts, metadatas=meta)`. Explain `upsert` means insert-or-update by ID — safe to call on startup multiple times.

5. **Query logic** — Show `collection.query(query_embeddings=[query_vector], n_results=3)`. Explain ChromaDB returns `documents`, `ids`, `distances`, and `metadatas`. Point out we use `distances` only for optional debugging.

6. **LLM generation call** — Show the prompt construction. The system message explains the agent role. The user message contains the ticket text followed by numbered context chunks. Ask: "What would the LLM answer without context?" (Generic, possibly wrong.) "What does context add?" (Grounding in actual policy.)

7. **Endpoint** — Show `GET /tickets/{id}/suggested-response`. Confirm it uses `get_current_user` dependency (auth-protected), loads the ticket from DB, calls `rag_service.get_suggested_response(ticket)`, and returns the structured response.

---

## 50–65 min: Student Follow-Along Build

### Instructor Goal

Students replicate the build in their own environment.

### Specific Actions

1. Direct all students to run Prompt 1 from the pre-session file in their Antigravity.
2. Tell students to run `pip install chromadb sentence-transformers` if not already installed. Also confirm `google-generativeai` is present from Session 4 and `GEMINI_API_KEY` is set in `.env`.
3. Give students 12 minutes to paste the prompt, review the generated output, and run the server.
4. Circulate (or watch student screens if remote) for these specific failure modes:
   - `ModuleNotFoundError: No module named 'chromadb'` — fix with `pip install chromadb`.
   - `ModuleNotFoundError: No module named 'sentence_transformers'` — fix with `pip install sentence-transformers`.
   - `google.auth.exceptions.DefaultCredentialsError` or similar — confirm `GEMINI_API_KEY` is set in the environment or `.env`.
   - `AttributeError: 'Collection' has no attribute 'upsert'` — student has old ChromaDB. Fix: `pip install --upgrade chromadb`.
   - ChromaDB `InvalidArgumentError` about distance metric — ensure `metadata={"hf:space": "cosine"}` not `{"distance": "cosine"}`. The correct key for ChromaDB is `hf:space`.
5. When a student's server starts cleanly and they can see the startup log showing "Knowledge base initialised with N chunks", mark them as unblocked.

---

## 65–80 min: Test and Improve

### Instructor Goal

Use Swagger and targeted LLM prompts to verify correctness and improve output quality.

### Specific Actions

1. In Swagger, authenticate using `POST /auth/login` to get a JWT token and click "Authorize".
2. Create a test ticket using `POST /tickets` with subject "My payment keeps failing" and a realistic description.
3. Hit `GET /tickets/{id}/suggested-response` with the new ticket ID.
4. Examine the response JSON together: `suggested_response` should reference refund policy or payment failure steps. `sources` should list 3 chunk IDs.
5. Ask: "Does the response mention our actual policy text, or is it generic?" If generic, the retrieval is working but the LLM is not using context — check that the context chunks are injected into the prompt correctly.
6. Use Improvement Prompt 2 from the pre-session file to add source attribution inline in the response text (e.g., "According to our payment troubleshooting guide: ...").
7. Test a second ticket: "I want to delete my account". Verify the retrieved chunks are about account deletion, not payment.

---

## 80–95 min: Error Handling and Edge Cases

### Instructor Goal

Teach production-grade defensive coding for the RAG pipeline.

### Specific Actions

1. Test `GET /tickets/9999/suggested-response` — confirm it returns HTTP 404, not a 500. If it returns 500, show the fix: add `if not ticket: raise HTTPException(status_code=404, detail="Ticket not found")`.
2. Simulate ChromaDB returning zero results (e.g., query with a nonsense string). Show what happens downstream — the LLM prompt has no context. Add a guard: if `len(retrieved_chunks) == 0`, return a response that says no relevant knowledge was found rather than calling the LLM with empty context.
3. Show what happens if `GEMINI_API_KEY` is missing at generation time — a `google.api_core.exceptions.PermissionDenied` or similar error bubbles up as a 500. Add a startup check that logs a clear warning if the key is absent. Note: sentence-transformers embeddings do not require any API key, so embedding always works locally.
4. Discuss idempotency: what happens if the server restarts and the startup event runs again? The `upsert` call handles this — no duplicate chunks if chunk IDs are deterministic (e.g., `doc_name_chunk_0`, `doc_name_chunk_1`).
5. Briefly show how to write a test for the endpoint using `pytest` and `httpx.AsyncClient` with a mocked ChromaDB query — preview for the unit test prompt.

---

## 95–105 min: Concept Pause

### Instructor Goal

Translate implementation into durable technical understanding students can articulate in interviews.

### Explain These Concepts Precisely

**What is an embedding?**

An embedding is a fixed-length numerical vector produced by a neural encoder model. The model is trained so that inputs with similar meaning produce vectors that are geometrically close in the high-dimensional vector space. The sentence-transformers `all-MiniLM-L6-v2` model produces 384-dimensional vectors and runs entirely locally — no API key, no network call. Every float in that vector encodes some aspect of the semantic content of the input text. The model has no explicit feature list — the representation is distributed across all 384 dimensions.

**What is cosine similarity, really?**

Given two vectors A and B, cosine similarity = (A · B) / (|A| × |B|). It measures the cosine of the angle between them. Values range from -1 (opposite) to 1 (identical direction). For embeddings, two semantically similar texts like "my payment was declined" and "card transaction failed" will produce vectors pointing in nearly the same direction, giving cosine similarity close to 1. ChromaDB uses this to rank chunks.

**Why does RAG reduce hallucination?**

In a vanilla LLM call, the model answers from parametric memory — knowledge baked into its weights at training time. That knowledge may be outdated, incomplete, or wrong for your specific domain. RAG injects retrieved ground-truth text into the context window. The LLM is now answering from retrieved evidence, not from memory. Hallucination is not eliminated, but it is substantially reduced because the LLM has a reference document to cite.

**Retrieval vs. Generation — the separation that matters**

Retrieval is deterministic search: given a query vector, find the nearest stored vectors. It always returns the same chunks for the same query. Generation is probabilistic: given a prompt, the LLM samples tokens based on a probability distribution. These are separate components with separate failure modes. Retrieval can fail by returning irrelevant chunks (bad embeddings, poor chunking). Generation can fail by ignoring the retrieved context or hallucinating on top of it. Separating them means you can improve each independently.

**Draw on the board:**

```
Retrieval (deterministic) → correct chunks → LLM (probabilistic) → grounded response
```

Ask students to write a 2–3 sentence answer to: "How does RAG work in your project?"

---

## 105–115 min: Interview Discussion and Technical Viva Practice

### Instructor Goal

Drill the questions from the interview questions section below. Use cold-calling.

### Method

1. Pick Q1 cold — ask a student to answer without notes. Give 30 seconds.
2. Read the expected answer aloud. Ask: "What did they get right? What did they miss?"
3. Move through Q6, Q9, Q11, Q14 — these are the highest-value questions for this feature.
4. For Q11 (chunking strategy trade-offs), expect incomplete answers — use it to teach.
5. Ask students to pair up and explain the full RAG flow to each other in 60 seconds. Instructor listens and corrects.

---

## 115–120 min: Wrap-Up and Session 6 Preview

### Instructor Closing

Today we added a full RAG pipeline from scratch: static knowledge base, chunking, sentence-transformers local embeddings, ChromaDB vector storage, cosine similarity retrieval, and grounded generation via Gemini 1.5 Flash.

In Session 6, we will wrap this pipeline inside a LangGraph agentic workflow. Instead of a single direct call, the system will use a graph of nodes — a Classify node, a Retrieve node, a Generate node, and a Review node — that can loop or branch based on the quality of the output. We will add a self-critique step that re-runs retrieval if the initial response is rated as insufficient.

The RAG service you built today becomes one node inside that graph.

---

# Instructor Notes

## What to Emphasize

1. The ingestion pipeline (embed + store) and the query pipeline (embed + retrieve + generate) are architecturally separate. In production they run at different times. Startup vs. per-request.
2. Chunk IDs must be deterministic — using `{doc_name}_chunk_{i}` ensures upsert is idempotent across restarts.
3. ChromaDB's `PersistentClient` writes to disk. `EphemeralClient` does not. Students must use `PersistentClient` or the collection resets on every restart.
4. The `all-MiniLM-L6-v2` model dimension is 384. Do not mix embedding models — if you embed documents with model A and query with model B, retrieval results are meaningless.
5. Cosine similarity is the correct distance metric for text embeddings. Euclidean distance on high-dimensional vectors suffers from the curse of dimensionality. ChromaDB uses cosine when you set `metadata={"hf:space": "cosine"}`.
6. The LLM does not retrieve — it generates. Students often conflate the two. Reinforce: "The LLM has no access to ChromaDB. We do the retrieval, then hand the results to the LLM."
7. Source attribution (`sources` field in the response) is important for production trust. It allows a human reviewer to verify the LLM's answer against the original document.
8. For embeddings, sentence-transformers runs locally — no API call, no cost, no latency from the network. The only external API call per request is the Gemini generation call. Students should understand that local embeddings eliminate one network round-trip compared to using a cloud embedding API.

## Common Student Mistakes

1. **`ModuleNotFoundError: No module named 'chromadb'`** — Student did not install chromadb. Fix: `pip install chromadb`. Check that it is also added to `requirements.txt`.

2. **`sentence_transformers encode() returns unexpected shape`** — Usually caused by passing a single string instead of a list. Fix: always pass a `list[str]` to `embedding_model.encode(texts)`, then call `.tolist()` on the result.

3. **`AttributeError: 'NoneType' has no attribute 'text'`** — The Gemini response returned unexpectedly. Usually caused by a quota/rate-limit hit on the free tier. Fix: add `time.sleep(2)` between calls in classroom demos. Verify `GEMINI_API_KEY` is set.

4. **ChromaDB `ValueError: Collection already exists`** — Student is calling `create_collection` instead of `get_or_create_collection`. Fix: use `client.get_or_create_collection(name="support_kb", metadata={"hf:space": "cosine"})`.

5. **`422 Unprocessable Entity` on `GET /tickets/{id}/suggested-response`** — Path parameter `id` is being sent as a string but the route expects an integer. Check the route definition: `async def get_suggested_response(id: int, ...)`.

6. **Retrieval returns completely wrong chunks** — Student is embedding documents with one model and querying with a different one. Fix: confirm both ingestion and query calls use the same `SentenceTransformer("all-MiniLM-L6-v2")` instance (or identical model name).

7. **`suggested_response` is generic and ignores the context chunks** — The retrieved chunks are not being injected into the LLM prompt. Fix: verify the prompt construction concatenates chunk texts into the user message before the LLM call.

8. **Server starts but `GET /tickets/{id}/suggested-response` returns 500 with "collection has no items"** — Startup initialisation failed silently. Add a try/except around the startup embedding block and log errors explicitly.

9. **`JSONDecodeError` when parsing LLM output** — The LLM returned extra prose around the JSON. Fix: do not ask the LLM to return JSON in the RAG endpoint — return plain text for `suggested_response` and handle `sources` separately in Python code, not from the LLM output.

10. **`OperationalError: no such table: ticket`** — Student added the new endpoint but the DB tables were not created. Confirm `create_db_and_tables()` is still called in `main.py` startup and the `Ticket` model is imported.

## How to Control the Session

Use this rule: if a student's question is about a feature not in the scope list (re-ranking, streaming, PDF upload), write it on a "backlog" section of the board and explicitly say "that is a real production feature — let's add it to the backlog." Do not attempt to build it live.

## Setup Rule

If a student's ChromaDB installation fails during the session, they should comment out the RAG startup call and follow along conceptually. They rebuild after the session using the provided prompts. Do not block the interview discussion section to fix one student's environment.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What did you add in Session 5?

Expected answer:
I added a RAG pipeline to the Support Ticket Copilot. This consists of a static knowledge base of support policy documents stored as Python string constants, a chunking step that splits documents by paragraph, an embedding step using the sentence-transformers `all-MiniLM-L6-v2` model (local, no API key) to convert each chunk into a 384-dimensional vector, and a ChromaDB local persistent collection that stores those vectors. At request time, the `GET /tickets/{id}/suggested-response` endpoint embeds the ticket text using the same local model, queries ChromaDB for the top-3 semantically similar chunks, injects them as context into a Gemini 1.5 Flash chat completion call, and returns a structured JSON response with the suggested text and the source chunk IDs.

### Q2. What is the role of ChromaDB in your project?

Expected answer:
ChromaDB is the vector database. It stores the embedding vectors for each knowledge base chunk along with the original chunk text and metadata. At query time, I pass a query vector and ChromaDB performs approximate nearest-neighbour search using cosine similarity to return the most relevant chunks. I use `PersistentClient` so the collection is written to disk and survives server restarts. I use a single collection named `support_kb` with `metadata={"hf:space": "cosine"}` to specify the distance metric.

### Q3. What is the knowledge base made of and why did you choose that structure?

Expected answer:
The knowledge base is 8 to 10 support policy documents defined as Python string constants in `app/knowledge_base/documents.py`. Documents cover topics like refund policy, login troubleshooting, payment failure resolution, account deletion, and subscription cancellation. I chose Python string constants rather than files for simplicity — no file I/O, no path dependencies, and the documents are version-controlled alongside the code. In production, this would be replaced by a document loader from S3 or a CMS, but for this scope, constants are correct.

### Q4. How does the `GET /tickets/{id}/suggested-response` endpoint work end to end?

Expected answer:
The endpoint receives a ticket ID as a path parameter. It first checks the database for the ticket using `session.get(Ticket, id)` and raises a 404 if not found. It then calls `rag_service.get_suggested_response(ticket)`, which embeds the ticket's subject and description concatenation using the local sentence-transformers model, queries ChromaDB for the top-3 chunks, constructs a Gemini 1.5 Flash chat completion prompt with those chunks as context, and returns a `SuggestedResponseOut` Pydantic model containing `ticket_id`, `suggested_response` (the LLM text), and `sources` (the list of retrieved chunk IDs).

### Q5. Why did you add this feature after the LLM classifier and not before?

Expected answer:
Session 4 added the LLM classifier which introduced the Gemini client and the pattern of calling the LLM during request processing. Session 5 builds on that foundation by introducing a second AI subsystem — the RAG pipeline — that adds local embeddings via sentence-transformers and a retrieval step before generation. The sequencing matters because students first needed to understand direct LLM calls before introducing the more complex retrieval-augmented pattern. Also, classification depends only on the ticket text, while RAG depends on a separate data store — the vector DB — which is a new infrastructure component to introduce after the LLM basics are established.

---

## Technical Deep-Dive Questions

### Q6. How does your chunking function work and what are its parameters?

Expected answer:
The chunking function takes a document string and a `max_chunk_size` integer (defaulting to 500 characters). It first splits the document on `"\n\n"` to produce paragraph-level chunks. It then iterates through each paragraph: if the paragraph is shorter than `max_chunk_size`, it is kept as-is. If it is longer, it is further split into sub-chunks by slicing at `max_chunk_size` character intervals. Empty strings are filtered out. The function returns a list of chunk strings. Chunk IDs are generated as `{doc_name}_chunk_{index}` to ensure determinism across restarts.

### Q7. What does the `upsert` call look like in your code and why upsert rather than add?

Expected answer:
The call is `collection.upsert(ids=chunk_ids, embeddings=vectors, documents=chunk_texts, metadatas=metadatas)` where `chunk_ids` is a list of strings like `["refund_policy_chunk_0", "refund_policy_chunk_1"]`, `embeddings` is a list of 384-element float lists (produced by the local sentence-transformers model), `documents` is the original text of each chunk, and `metadatas` is a list of dicts containing `{"source": doc_name}`. I use `upsert` rather than `add` because `upsert` is idempotent — if a chunk with that ID already exists in the collection it updates it, if not it inserts it. This means the startup initialisation code can run safely on every server restart without creating duplicate entries.

### Q8. How do you construct the LLM prompt in the generation step?

Expected answer:
I construct the prompt in two parts. The system message tells the LLM it is a support agent assistant that must base its answer only on the provided context. The user message contains two sections: first the ticket text formatted as "Ticket subject: {subject}\nDescription: {description}", and then the retrieved context formatted as a numbered list: "Context 1: {chunk_text}\nContext 2: ...\nContext 3: ...". I call `model.generate_content(prompt)` with a Gemini 1.5 Flash model configured with `temperature=0.3` to reduce variance in the output. The lower temperature makes the response more deterministic and grounded.

### Q9. What does `collection.query` return and which fields do you use?

Expected answer:
`collection.query(query_embeddings=[query_vector], n_results=3)` returns a dict with keys `ids`, `documents`, `distances`, `metadatas`, and `embeddings` (optional). Each value is a list of lists because ChromaDB supports batch queries. For a single query, `result["documents"][0]` is a list of 3 chunk texts, and `result["ids"][0]` is a list of 3 chunk IDs. I use `documents[0]` to build the context for the LLM prompt and `ids[0]` to populate the `sources` field in the response. I do not use `distances` in the response but I log them during development to verify retrieval quality.

### Q10. How does the RAG endpoint differ from the classifier endpoint in Session 4?

Expected answer:
The Session 4 classifier endpoint calls Gemini once — it sends the ticket text in a chat completion with a classification prompt and parses the returned category string. The Session 5 RAG endpoint generates an embedding locally using sentence-transformers (no API call) and then calls Gemini once to generate the suggested response. The classifier writes its output to the database (updating `ticket.category`). The RAG endpoint is read-only — it does not persist anything, it only computes and returns a response. The RAG endpoint also has a dependency on ChromaDB and sentence-transformers which the classifier does not.

---

## System Design and Trade-off Questions

### Q11. What are the trade-offs of your chunking strategy?

Expected answer:
Paragraph-level chunking (`split("\n\n")`) is simple and semantically reasonable — paragraphs tend to be about one topic. The trade-off is that paragraph lengths vary widely: some may be one sentence, others may be 10. Very short chunks lose context; very long chunks dilute relevance because the embedding captures the average semantics of the whole chunk. The max character limit fallback addresses the long-chunk problem but introduces arbitrary splits mid-sentence. Alternative strategies include sentence-level chunking using NLTK or spaCy (more precise but adds a dependency), fixed-token chunking (more predictable for embedding models), or semantic chunking that detects topic shifts. For a support knowledge base with well-structured documents, paragraph chunking is an acceptable and practical starting point.

### Q12. Why does mixing embedding models break retrieval?

Expected answer:
Embedding models learn a specific mapping from text to vector space during training. The geometry of that space — which directions encode which semantic concepts — is model-specific. If you embed documents with model A and later query with model B, the two vectors inhabit different geometric spaces. The cosine similarity between a document vector from model A and a query vector from model B is essentially meaningless — you are measuring the angle between apples and oranges. This is why the ingestion and retrieval steps must always use the exact same model and version. This also means you cannot simply upgrade your embedding model without re-embedding the entire knowledge base.

### Q13. How would you scale this RAG pipeline for a production system with 100,000 support documents?

Expected answer:
Several components would need to change at production scale. The static Python string constants would be replaced by a document ingestion pipeline reading from S3 or a database, likely run as a batch job or triggered by document updates. ChromaDB local persistent storage would be replaced by a managed vector database like Pinecone, Weaviate, or pgvector in PostgreSQL — which support distributed storage, replication, and horizontal scaling. The startup initialisation would become a separate background service. Since sentence-transformers runs locally, embedding batches can be processed without API rate limits — but you would switch to a more capable model (e.g., a larger sentence-transformers variant) and possibly GPU-accelerate the encoder. You would also add caching: store the query embedding and top-k results in Redis with a short TTL for common ticket types.

### Q14. Why is source attribution important and how did you implement it?

Expected answer:
Source attribution is important because it allows a human reviewer (the support agent) to verify the suggested response against the original policy document. Without attribution, the LLM response is a black box — the agent cannot tell if it is based on the actual refund policy or if the LLM hallucinated a plausible-sounding policy. I implemented it by returning the `sources` field in the response — a list of chunk IDs like `["refund_policy_chunk_0", "payment_failure_guide_chunk_2"]`. These IDs encode both the source document and the chunk index. In a production UI, these IDs would be used to hyperlink directly to the relevant section of the source document.

### Q15. What is the difference between semantic search and keyword search, and why does this matter for a support system?

Expected answer:
Keyword search (BM25, SQL `LIKE`, Elasticsearch default) retrieves documents that contain the exact query terms or close variants. It fails when the user uses different vocabulary — a user who types "my card was rejected" will not match a document that says "transaction declined" if there is no token overlap. Semantic search using embeddings retrieves documents based on meaning regardless of exact wording, because the embedding model has learned that "card rejected" and "transaction declined" are semantically equivalent. In a support system, users phrase the same problem in many different ways, so semantic search has a substantial recall advantage. The trade-off is that semantic search is more expensive (requires an embedding model and vector index) and can sometimes retrieve plausible-sounding but topically wrong documents if the embedding space is noisy.

---

# Session 5 Completion Checklist

- [ ] `app/knowledge_base/documents.py` exists and contains at minimum 8 document string constants covering distinct support topics
- [ ] `app/services/rag_service.py` exists with chunking, embedding (sentence-transformers), upsert, query, and generation functions separated into distinct functions (not one monolithic function)
- [ ] ChromaDB collection `support_kb` is created with `metadata={"hf:space": "cosine"}` using `PersistentClient(path="./chroma_db")`
- [ ] Server startup initialises ChromaDB and logs the number of chunks inserted (or skips if already populated)
- [ ] `./chroma_db` directory exists on disk after server start (confirm with `ls -la`)
- [ ] `GET /tickets/{id}/suggested-response` returns HTTP 200 with `ticket_id`, `suggested_response`, and `sources` fields
- [ ] Swagger returns HTTP 404 when hitting `GET /tickets/9999/suggested-response` for a non-existent ticket ID
- [ ] Swagger returns HTTP 401 when hitting `GET /tickets/{id}/suggested-response` without a JWT token (auth is enforced)
- [ ] `suggested_response` text references content relevant to the ticket topic (not generic boilerplate), confirmed by testing with a payment-related ticket and an account-deletion ticket
- [ ] `sources` field is a non-empty list containing at least 1 chunk ID string
- [ ] Running `pytest` on existing tests from Sessions 1–4 does not break (no regressions introduced)
- [ ] Student can verbally explain the difference between retrieval and generation and state which component is deterministic

---

# Instructor Backup Plan

If ChromaDB or sentence-transformers installation fails for multiple students, or the Gemini API is unavailable:

1. Instructor continues the live build on screen using their own working environment.
2. Students follow the architecture explanation and code walkthrough conceptually without running the code.
3. The concept pause section (95–105 min) and interview questions section remain fully executable — these require no running code.
4. Share the complete Session 5 code after the session. Students self-build using the prompts in their own time.
5. Do not shorten the interview discussion section. The conceptual understanding of RAG is the most interview-relevant output of this session regardless of whether the code ran locally.
6. Since sentence-transformers runs locally, the embedding step should always be available regardless of network/API issues. If only the Gemini API is unavailable but ChromaDB and sentence-transformers are installed, demonstrate the full ingestion and retrieval flow — show that chunks are retrieved correctly — then mock the generation step with a hardcoded string to complete the endpoint demo.
