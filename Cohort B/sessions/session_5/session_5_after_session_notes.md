# Session 5 After-Session Notes: Add RAG Knowledge Base

## What We Built Today

In Session 5 we extended the AI Support Ticket Resolution Copilot backend with a complete RAG (Retrieval-Augmented Generation) pipeline. The addition consists of three new components wired into the existing FastAPI application:

1. **`app/knowledge_base/documents.py`** — 8 to 10 Python string constants representing support policy documents (refund policy, payment failure guide, login troubleshooting, account deletion, subscription cancellation, password reset steps, billing dispute process, shipping policy). A `DOCUMENTS` dict maps short names to each constant for the ingestion loop.

2. **`app/services/rag_service.py`** — The core RAG module with four functions:
   - `chunk_document()` — splits a document by `\n\n` paragraph breaks with a 500-character fallback splitter; returns deterministic chunk IDs (`{doc_name}_chunk_{i}`)
   - `embed_texts()` — calls `SentenceTransformer("all-MiniLM-L6-v2").encode(texts).tolist()` locally; returns a list of 384-float vectors (no API key, no network call)
   - `init_knowledge_base()` — called once at startup; checks `collection.count()` and skips if already populated; otherwise embeds all chunks and upserts them into ChromaDB
   - `get_suggested_response()` — embeds the ticket subject and description using sentence-transformers, queries ChromaDB for top-3 chunks, constructs a grounded LLM prompt, calls Gemini 1.5 Flash `model.generate_content(prompt)`, and returns `{"suggested_response": str, "sources": list[str]}`

3. **New endpoint in `app/routes/tickets.py`** — `GET /tickets/{id}/suggested-response` loads the ticket from the database, calls `rag_service.get_suggested_response()`, and returns a `SuggestedResponseOut` Pydantic model with `ticket_id`, `suggested_response`, and `sources` fields.

ChromaDB persists to `./chroma_db` on disk. The collection is named `support_kb` with cosine similarity distance metric.

---

# Why This Feature Matters for Production Systems

Every production AI assistant that handles domain-specific questions uses some form of RAG. Here is why it is standard practice rather than a nice-to-have:

**LLMs have parametric memory, not live memory.** Gemini 1.5 Flash knows what it was trained on. It does not know your company's refund window, your specific escalation process, or whether your policy changed last quarter. If you ask it without context, it will either refuse or generate a plausible-sounding but potentially wrong answer — this is hallucination. RAG forces the LLM to answer from retrieved evidence, dramatically reducing this risk.

**Support knowledge bases change.** A new policy document, a product update, a procedure change — these happen constantly. In a RAG system, you update the knowledge base and re-embed. The LLM behaviour changes immediately without retraining. In a fine-tuned model, you would need to re-run training, which is expensive and slow.

**Auditability.** The `sources` field in the response lets a human reviewer check which knowledge base sections the LLM used. This is critical for regulated industries (financial services, healthcare) where an AI recommendation must be traceable to a source document.

---

# System Architecture Flow (Sessions 1 through 5)

```
Session 1 — Core CRUD
Client → FastAPI Router → Ticket CRUD Operations → SQLite DB (SQLModel)

Session 2 — Database Layer added
Client → FastAPI Router → Route Handlers → SQLModel ORM → SQLite DB
                                               ↑
                                     (Alembic migrations, typed models)

Session 3 — Auth Layer added
Client → FastAPI Router
               ↓
        [JWT Auth Middleware]         POST /auth/login → password verify → JWT issued
        get_current_user()            POST /auth/register → bcrypt hash → User saved
               ↓
        Route Handlers → SQLModel → SQLite DB

Session 4 — LLM Classifier added
Client → POST /tickets (with JWT)
               ↓
        get_current_user() → verified
               ↓
        Ticket data saved to DB
               ↓
        classifier.py → Gemini 1.5 Flash model.generate_content()
               ↓
        category string returned → saved to ticket.category in DB
               ↓
        TicketOut returned with category populated

Session 5 — RAG Pipeline added (today)
At startup:
  app/main.py lifespan
        ↓
  create_db_and_tables()
        ↓
  rag_service.init_knowledge_base()
        ↓
  documents.py DOCUMENTS dict → chunk_document() → embed_texts() [sentence-transformers, local]
        ↓
  ChromaDB PersistentClient("./chroma_db") → collection.upsert()
        ↓
  support_kb collection populated (skipped if already has items)

At request time:
  Client → GET /tickets/{id}/suggested-response (with JWT)
        ↓
  get_current_user() → verified
        ↓
  session.get(Ticket, id) → 404 if not found
        ↓
  rag_service.get_suggested_response(ticket.subject, ticket.description)
        ↓
  SentenceTransformer("all-MiniLM-L6-v2").encode([query]) → 384-dim query vector (local)
        ↓
  collection.query(query_embeddings=[vector], n_results=3) → top-3 chunks
        ↓
  LLM prompt constructed (instructions + ticket text + 3 context chunks)
        ↓
  Gemini 1.5 Flash model.generate_content(prompt, temperature=0.3)
        ↓
  SuggestedResponseOut { ticket_id, suggested_response, sources }

Session 6 Preview — LangGraph Agentic Workflow
  The RAG service becomes a Retrieve node inside a LangGraph StateGraph.
  Additional nodes: Classify → Retrieve → Generate → Review (self-critique loop)
  Conditional edges allow re-retrieval if the Review node rates the output insufficient.
```

---

# Technical Deep-Dive: Embeddings + Vector Database + RAG Pipeline + Retrieval vs Generation Separation

## Embeddings: What They Are and What They Encode

An embedding is a fixed-length dense vector produced by a neural encoder model trained to map text to a continuous vector space where semantic similarity corresponds to geometric proximity. The sentence-transformers `all-MiniLM-L6-v2` model uses a transformer architecture (similar to BERT) that encodes the full contextual meaning of an input string into 384 floating-point numbers. These 384 dimensions are not human-interpretable individually — the representation is distributed. But the model is trained so that "credit card declined" and "payment transaction failed" produce vectors with high cosine similarity, while "refund policy" and "login troubleshooting" produce vectors pointing in very different directions. The model runs entirely locally — no network call, no API key, no cost — and is downloaded once on first use (~90MB).

The practical consequence: you can compare any two pieces of text by computing the angle between their vectors. If the angle is small (cosine similarity near 1), the texts are semantically related regardless of exact wording. This is what makes semantic search work. Keyword search would fail on "payment declined" vs "transaction failed" because there is no token overlap. Embedding-based search succeeds because the vectors are close.

## ChromaDB as a Vector Store: What It Does Under the Hood

ChromaDB is a purpose-built database for storing and querying embedding vectors. When you call `collection.upsert()`, ChromaDB stores three things for each record: the vector, the original text (`documents` field), and metadata. When you call `collection.query(query_embeddings=[v], n_results=3)`, ChromaDB computes the cosine similarity between the query vector `v` and every stored vector, then returns the 3 records with the highest cosine similarity. With `PersistentClient`, all of this data is written to SQLite files inside `./chroma_db` — the collection survives process restarts.

In production, a local ChromaDB instance becomes a bottleneck at scale (millions of vectors, concurrent reads). Production replacements — Pinecone, Weaviate, pgvector — provide distributed storage, ANN (approximate nearest neighbour) indexing algorithms like HNSW, and horizontal scalability. The core API concepts transfer directly: upsert + query with the same semantics.

## Retrieval vs Generation: The Separation That Matters

The most common conceptual error when explaining RAG in interviews is conflating retrieval and generation into a single step. They are architecturally distinct:

**Retrieval** is deterministic search. Given the same query vector and the same ChromaDB collection, it will always return the same top-3 chunks. It is a fast nearest-neighbour operation with O(n) complexity (linear scan for small collections, HNSW for large). It does not understand language — it only computes geometric distances. Retrieval can fail by returning irrelevant chunks if the embeddings are poor, the query is ambiguous, or the chunking strategy loses important context.

**Generation** is probabilistic language modelling. The LLM receives a prompt containing the retrieved chunks and generates a response by sampling tokens based on a probability distribution over the vocabulary. With `temperature=0.3`, we bias the sampling toward higher-probability tokens, making the output more deterministic and fact-adherent. Generation can fail by ignoring the retrieved context (the model may fall back on parametric memory even when context is provided), by hallucinating details not in the chunks, or by producing a grammatically fluent but factually wrong synthesis.

Keeping them separate is not just architectural cleanliness — it means you can debug and improve each independently. If responses are wrong, you first check retrieval quality (are the right chunks being returned?). If retrieval looks correct but responses are still wrong, you improve the generation prompt. Mixing both into one function makes it impossible to isolate the failure.

---

# What Students Should Understand

1. An embedding is not a keyword or a tag — it is a geometric representation of meaning. Two semantically equivalent sentences have similar embeddings even with no shared words.

2. The embedding model used at ingestion and the model used at query time must be identical. Different models produce incompatible vector spaces.

3. Chunk size is a trade-off: smaller chunks are more topically precise but lose surrounding context; larger chunks retain context but produce diluted embeddings that are harder to distinguish semantically.

4. ChromaDB's `upsert` is preferred over `add` at startup because it is idempotent. Calling `add` twice with the same IDs raises an error; `upsert` overwrites — safe for repeated startup calls.

5. The `sources` field in the response is not cosmetic — it is the mechanism for human verification of the LLM's grounding. In production it enables audit trails and compliance checking.

6. `all-MiniLM-L6-v2` (sentence-transformers) produces 384-dimensional vectors at zero cost — it runs locally. The model is called twice per RAG flow: once at ingestion per chunk, and once at query time per request. Both calls are local with no per-call cost. Understanding the trade-off between local models (free, lower capability, requires local compute) and cloud APIs (paid, higher capability, no local resources) matters for production architecture decisions.

7. The retrieval step is not the LLM — the LLM has no access to ChromaDB. The application code does the retrieval, then hands the results to the LLM as part of the prompt. This distinction is a common interview test.

8. Paragraph splitting (`"\n\n"`) works well for well-structured policy documents with natural paragraph breaks. It is not suitable for unstructured text, code documentation, or tables — those require different chunking strategies.

9. Without RAG, the LLM answers from parametric memory — knowledge baked in at training time. With RAG, the LLM answers from retrieved evidence. Hallucination is not eliminated but is substantially reduced because the model has a reference document.

10. The startup initialisation is a one-time ingestion job. In production, this would be a separate batch process triggered by document updates, not something that runs on every server start.

---

# Interview-Ready Explanation

```text
In Session 5, I built a RAG pipeline for the Support Ticket Copilot. At server startup, the pipeline chunks a static knowledge base of support policy documents by paragraph, embeds each chunk using the sentence-transformers all-MiniLM-L6-v2 model (local, no API key, 384-dimensional vectors), and stores the vectors in a local persistent ChromaDB collection. When a support agent hits the GET /tickets/{id}/suggested-response endpoint, the system embeds the ticket text using the same local model, retrieves the top-3 semantically similar chunks via cosine similarity, injects them as numbered context into a Gemini 1.5 Flash prompt, and returns a structured response with the suggested text and the source chunk IDs. This grounding step prevents the LLM from hallucinating company-specific policies because it is forced to answer from retrieved evidence rather than parametric memory.
```

---

# What Happens When GET /tickets/{id}/suggested-response Is Called

```text
1. FastAPI routes the request to the get_suggested_response handler in app/routes/tickets.py.

2. The get_current_user dependency decodes the Authorization header JWT using python-jose, extracts the user email claim, and queries the User table to confirm the user exists. If the token is missing or expired, FastAPI returns 401 before the handler runs.

3. The handler calls session.get(Ticket, id) — a SQLModel call that executes SELECT * FROM ticket WHERE id = ? with the path parameter. If no row is returned, the handler raises HTTPException(status_code=404, detail="Ticket not found").

4. The handler calls rag_service.get_suggested_response(ticket.subject, ticket.description).

5. Inside get_suggested_response(), the ticket subject and description are concatenated into a single query string. This string is passed to the local SentenceTransformer model: embedding_model.encode([query_string]).tolist()[0] — a list of 384 floats. This is the query vector. No network call is made; the encoder runs in-process.

6. The query vector is passed to collection.query(query_embeddings=[query_vector], n_results=3). ChromaDB computes cosine similarity between the 384-dim query vector and every stored 384-dim vector in the support_kb collection, and returns the 3 nearest neighbours as a dict: {"ids": [["chunk_id_0", "chunk_id_1", "chunk_id_2"]], "documents": [["chunk_text_0", "chunk_text_1", "chunk_text_2"]], "distances": [[0.12, 0.18, 0.25]]}.

7. The three chunk texts are extracted from result["documents"][0] and formatted into a numbered context string. The three chunk IDs are extracted from result["ids"][0] for the sources field.

8. A Gemini generation call is made: model.generate_content(prompt) where the prompt combines the system instructions, the ticket text, and the 3 numbered context chunks into a single string. The model is configured with GenerationConfig(temperature=0.3) to make the output more deterministic and grounded.

9. The LLM response text is extracted from response.text.

10. The handler returns SuggestedResponseOut(ticket_id=id, suggested_response=llm_text, sources=chunk_ids) which FastAPI serialises to JSON and returns with HTTP 200.
```

---

# What AI Was Used For + What Engineers Must Still Do

## What the AI Coding Tool Generated

- The complete `app/knowledge_base/documents.py` with realistic support policy text and the `DOCUMENTS` dict
- The `rag_service.py` module with all four functions including chunking logic, sentence-transformers local embedding call, ChromaDB upsert, query, and Gemini LLM prompt construction
- The `SuggestedResponseOut` Pydantic model and the new endpoint in `tickets.py`
- The startup call in `main.py`

## What Engineers Must Still Do

These are the responsibilities an engineer cannot delegate to AI:

1. **Verify the ChromaDB collection is actually being written to disk.** Run `ls -la ./chroma_db` after server start. If the directory is missing, the PersistentClient path may be wrong relative to where `uvicorn` is launched from.

2. **Validate retrieval quality manually.** Hit the endpoint with 3 different ticket topics. Check that the `sources` field returns chunk IDs from the correct document. A payment ticket should retrieve payment-related chunks, not login-related chunks. If retrieval is wrong, the chunking or embedding may be the issue.

3. **Read and understand the generated prompt.** The quality of the LLM output depends entirely on the prompt. Verify the system message and user message structure. Change temperature if output is too variable or too repetitive.

4. **Add `chromadb` and `sentence-transformers` to `requirements.txt`** — AI tools sometimes generate working code but forget to update the requirements file, causing deployment failures.

5. **Test the 404 and 401 cases explicitly in Swagger** — not just the happy path.

6. **Understand the performance implications.** The sentence-transformers model is downloaded (~90MB) on first use. In production, pre-download the model as part of the Docker image build or CI pipeline. The only external API call per request is the Gemini generation call — there is no longer a cloud embedding call. For high-volume use, embedding caching (store query vectors in Redis with a TTL) can still reduce CPU usage from repeated local encoding of identical queries.

7. **Check idempotency.** Restart the server twice and confirm the startup log says "skipping ingestion" on the second start, not re-embedding all documents.

---

# Common Issues and Fixes

## Issue 1: `ModuleNotFoundError: No module named 'chromadb'` at server startup

Root cause: `chromadb` was not installed, or it was installed in a different virtual environment than the one running the server.

Fix: Activate the correct virtual environment and run `pip install chromadb`. Verify with `python -c "import chromadb"`. Add `chromadb` to `requirements.txt`.

What to ask AI:

```text
I am getting ModuleNotFoundError: No module named 'chromadb' when starting my FastAPI server.
My app uses chromadb.PersistentClient in app/services/rag_service.py.
I have a virtual environment at ./venv. How do I install chromadb correctly and confirm it is available to my server process?
Also check if there is anything wrong with my import statement in rag_service.py.
```

---

## Issue 2: `suggested_response` is generic and does not reference any policy — for example, it says "Please contact our support team" when there is a detailed refund policy in the knowledge base

Root cause: The retrieved chunks are not being injected into the Gemini prompt. The context variable is constructed but not included in the prompt string, or the chunks are being concatenated with incorrect formatting.

Fix: Print the full prompt string before the model.generate_content() call to verify the chunks appear in it. Confirm the prompt format is: system instructions + newline + ticket text + newline + "Context 1: {chunk}" + "Context 2: ..." + "Context 3: ...". Also verify `collection.count()` returns a non-zero value — the collection may have failed to initialise.

What to ask AI:

```text
The suggested-response endpoint returns a generic response that does not reference my knowledge base documents. The sources field returns chunk IDs correctly, so retrieval is working. But the LLM response ignores the context. Please review the prompt construction in get_suggested_response() in app/services/rag_service.py and fix how the retrieved chunks are injected into the Gemini prompt string. Show me the corrected prompt construction code.
```

---

## Issue 3: `chromadb.errors.InvalidCollectionException: Collection support_kb does not exist` when hitting the endpoint

Root cause: The `init_knowledge_base()` call in `main.py` raised an exception during startup (e.g., missing API key, network error during embedding) and the exception was silently swallowed, leaving the collection uncreated. Or the server was started from a different directory and `./chroma_db` does not exist at the expected relative path.

Fix: Wrap the `init_knowledge_base()` call in `main.py` with try/except and log any exception explicitly. Since sentence-transformers runs locally, the embedding step should always succeed — if init fails, the issue is more likely a ChromaDB path problem. Add a guard at the start of `get_suggested_response()` that checks `collection.count()` and raises `HTTPException(status_code=503)` if the collection is empty or missing. Use an absolute path for the ChromaDB client: `chromadb.PersistentClient(path=os.path.join(os.path.dirname(__file__), "../../chroma_db"))`.

What to ask AI:

```text
I am getting chromadb.errors.InvalidCollectionException: Collection support_kb does not exist when hitting GET /tickets/{id}/suggested-response, even though the server started without visible errors.
Please:
1. Add explicit error logging to the init_knowledge_base() startup call in app/main.py so startup failures are visible
2. Add a guard in get_suggested_response() in app/services/rag_service.py that returns HTTP 503 if the collection does not exist or is empty
3. Change the ChromaDB PersistentClient path to use an absolute path relative to the rag_service.py file location so it works regardless of where uvicorn is launched from
```

---

# Key Takeaways

1. **Retrieval and generation are separate systems with separate failure modes.** Retrieval fails when embeddings are poor or chunking loses context. Generation fails when the LLM ignores context or adds information not in the retrieved chunks. Debug them independently.

2. **Chunk design is an engineering decision, not an afterthought.** Chunks that are too large produce embeddings that average across multiple topics and retrieve imprecisely. Chunks that are too small lose surrounding context. Paragraph splitting is a reasonable starting point for structured policy documents. The right chunk size for your domain requires experimentation.

3. **The static knowledge base is a deliberate scope choice.** In production you would use a document store with versioning, and a separate ingestion pipeline that runs on document updates. The static Python constants pattern is not a shortcut — it is the correct complexity level for learning the RAG mechanics without file I/O, parsers, or async batch jobs obscuring the core concepts.

4. **RAG does not eliminate hallucination — it constrains it.** If the retrieved chunks do not contain the answer, the LLM may still generate plausible-sounding text. Adding an explicit system message instruction ("If the context does not contain the answer, say so explicitly") and low temperature reduces this risk. Source attribution allows human reviewers to catch it when it does occur.

---

# Session 6 Preview

In Session 6, we will wrap the Session 5 RAG pipeline inside a LangGraph agentic workflow. Instead of one direct function call chain, the system will be modelled as a directed graph of nodes:

- **ClassifyNode** — determines the ticket category (using the Session 4 classifier logic)
- **RetrieveNode** — performs the ChromaDB query from Session 5
- **GenerateNode** — constructs the LLM prompt and generates the response from Session 5
- **ReviewNode** — a new node that self-critiques the generated response and decides whether to loop back to RetrieveNode with a refined query or accept the output

The graph will have conditional edges: if ReviewNode rates the response quality as insufficient (below a threshold), it sends the state back to RetrieveNode with an expanded or rephrased query. This is the LangGraph pattern called a reflection loop or self-critique loop.

Students will implement `StateGraph`, `TypedDict` state, node functions, `add_edge`, `add_conditional_edges`, and `compile`. The key concept is that graph state flows through nodes — each node receives the full state dict and returns an updated dict.

The `rag_service.py` module from Session 5 will be imported directly as a utility — Session 6 orchestrates it, not replaces it.
