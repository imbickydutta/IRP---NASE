# Session 5 Student Pre-Session File: Add RAG Knowledge Base

## What We Are Building

Over these sessions, we are building one continuous backend project:

# AI Support Ticket Resolution Copilot

This is a production-style FastAPI backend that handles customer support tickets using AI. By the end of all sessions, the backend will:

- Accept and manage support tickets via a REST API
- Store data in a SQLite database using SQLModel ORM
- Protect endpoints with JWT-based authentication and role-based access
- Automatically classify tickets using an LLM on creation
- Suggest grounded responses using a RAG pipeline (Session 5 — today)
- Run an agentic workflow using LangGraph to triage and resolve tickets (Session 6)
- Deploy to a cloud environment with environment-based configuration

## What Has Been Built So Far

- **Session 1** — Core Ticket CRUD API: `POST /tickets`, `GET /tickets`, `GET /tickets/{id}`, `PUT /tickets/{id}`, `DELETE /tickets/{id}`
- **Session 2** — Database Layer: SQLite via SQLModel, Alembic migrations, `Ticket` and `User` models
- **Session 3** — Auth Layer: JWT login, `POST /auth/register`, `POST /auth/login`, `get_current_user` dependency, role-based access
- **Session 4** — LLM Classifier: On `POST /tickets`, a Gemini 1.5 Flash chat completion classifies the ticket into one of 6 categories and stores it in the `category` column

## Session 5 Goal

Add a complete RAG (Retrieval-Augmented Generation) pipeline that:

1. Stores a static knowledge base of support policy documents as Python string constants
2. Chunks those documents by paragraph
3. Embeds the chunks using sentence-transformers `all-MiniLM-L6-v2` (local, no API key required)
4. Stores vectors in a local persistent ChromaDB collection
5. At request time, retrieves the top-3 relevant chunks for any ticket
6. Generates a grounded suggested response using Gemini 1.5 Flash with the retrieved context
7. Exposes this via `GET /tickets/{id}/suggested-response`

## Session 5 Output

By the end of Session 5, hitting `GET /tickets/{id}/suggested-response` in Swagger will return a JSON response like:

```json
{
  "ticket_id": 3,
  "suggested_response": "Thank you for reaching out. Based on our payment troubleshooting guide, the most common causes of a declined transaction are...",
  "sources": ["payment_failure_guide_chunk_0", "payment_failure_guide_chunk_2", "refund_policy_chunk_1"]
}
```

---

# Pre-Read

## Why Are We Adding This Feature Now?

Session 4 proved the LLM can understand ticket text (classification). But classification is labelling — the LLM has no access to your company's specific policies. If you ask Gemini "what is our refund window?" without giving it the actual policy, it will guess or hallucinate a plausible-sounding answer.

RAG solves this by separating two concerns:

- **Retrieval**: Find the most relevant sections of your actual knowledge base for this specific ticket
- **Generation**: Give those sections to the LLM as context, so it generates a response grounded in real information

This is the pattern used in virtually every production AI assistant: retrieval first, generation second. Nailing this session means you can explain — and implement — one of the most important patterns in applied AI engineering.

## System Architecture Flow (Sessions 1 through 5)

```
Client (Swagger / Frontend)
        ↓ HTTP Request
FastAPI Router (app/routes/tickets.py, app/routes/auth.py)
        ↓
Authentication Middleware (get_current_user → JWT decode → User lookup)
        ↓
Route Handler
        ├─→ [POST /tickets] → LLM Classifier (app/services/classifier.py)
        │                              ↓ Gemini 1.5 Flash generate_content()
        │                         category string → save to DB
        │
        ├─→ [GET /tickets/{id}/suggested-response] → RAG Service (app/services/rag_service.py)   ← NEW SESSION 5
        │       ↓                                            ↓
        │  Load Ticket from DB                   Embed ticket text (sentence-transformers local)
        │                                                    ↓
        │                                       Query ChromaDB (cosine similarity top-3)
        │                                                    ↓
        │                                       Retrieved chunks injected into LLM prompt
        │                                                    ↓
        │                                       Gemini 1.5 Flash generate_content()
        │                                                    ↓
        │                                       Return suggested_response + sources
        │
        └─→ [All CRUD endpoints] → SQLModel session → SQLite DB
```

**At startup (app/main.py lifespan):**

```
Start server
        ↓
create_db_and_tables()   (existing from Session 2)
        ↓
rag_service.init_knowledge_base()   (NEW Session 5)
        ↓
ChromaDB PersistentClient → get_or_create_collection("support_kb")
        ↓
If collection is empty: chunk all documents → embed → upsert
If collection already has items: skip (idempotent)
```

## Key Concepts to Revise Before This Session

### 1. sentence-transformers (Local Embeddings)

Instead of a cloud API, we use the `sentence-transformers` library which runs an embedding model entirely on your machine — no API key, no cost, no network call. Install it with `pip install sentence-transformers`. Review the usage:

```python
from sentence_transformers import SentenceTransformer
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = embedding_model.encode(["hello world", "another text"])  # NumPy array
vector_list = vectors.tolist()  # convert to plain Python list for ChromaDB
# each vector is a list of 384 floats
```

The model is downloaded once (~90MB) on first use and cached locally. You can embed a list of strings in a single call (batch embedding).

### 2. Cosine Similarity

You do not need to implement cosine similarity yourself — ChromaDB computes it internally. But you need to understand it conceptually: given two vectors A and B, cosine similarity = (A · B) / (|A| × |B|). It measures how aligned two vectors are directionally. For semantic embeddings, texts with similar meaning produce vectors pointing in similar directions, giving cosine similarity close to 1. Orthogonal vectors (cosine similarity = 0) indicate no semantic relationship.

### 3. ChromaDB Basics

ChromaDB is a Python-native vector database. Key concepts:

- `chromadb.PersistentClient(path="./chroma_db")` — creates or opens a collection on disk
- `client.get_or_create_collection(name="...", metadata={"hf:space": "cosine"})` — creates the collection with cosine distance metric
- `collection.upsert(ids, embeddings, documents, metadatas)` — insert-or-update records
- `collection.query(query_embeddings=[vector], n_results=3)` — returns top-3 nearest neighbours

ChromaDB returns a dict: `{"ids": [[...]], "documents": [[...]], "distances": [[...]]}`. Note the double nesting — it supports batch queries, so results are lists of lists.

### 4. Text Chunking

Chunking is splitting a long document into smaller, retrievable pieces. The goal: each chunk should be semantically self-contained and small enough that its embedding captures one specific topic. Common strategies:

- Paragraph splitting (`"\n\n"`) — simple, respects natural document structure
- Fixed character/token size — predictable chunk sizes, may split mid-sentence
- Sentence-level — precise but requires NLP tooling

We use paragraph splitting with a character limit fallback.

### 5. RAG Pipeline Pattern

```
Ingestion (run once at startup):
  documents → chunk → embed → store in vector DB

Retrieval + Generation (run per request):
  query text → embed → nearest-neighbour search → retrieve chunks
  → inject chunks into LLM prompt → generate response
```

### 6. Pydantic Response Models in FastAPI

The new endpoint returns a new response schema. You will define:

```python
class SuggestedResponseOut(BaseModel):
    ticket_id: int
    suggested_response: str
    sources: list[str]
```

This is the same pattern used for `TicketOut` in previous sessions.

### 7. FastAPI Lifespan / Startup Events

The knowledge base needs to be initialised once when the server starts, not on every request. In FastAPI, use the `lifespan` context manager (or `@app.on_event("startup")` for older versions):

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    rag_service.init_knowledge_base()
    yield

app = FastAPI(lifespan=lifespan)
```

### 8. Idempotency in Data Ingestion

Idempotency means running an operation multiple times has the same result as running it once. In the RAG pipeline: if the server restarts, we do not want to re-embed and duplicate all chunks. Two mechanisms ensure idempotency:

- Deterministic chunk IDs (e.g., `refund_policy_chunk_0`) — same ID = upsert overwrites, not duplicates
- Count check before ingestion: `if collection.count() > 0: return` — skip if already populated

---

# Prerequisites: Setup Before This Session

## Python Packages to Install

Run this before the session:

```bash
pip install chromadb
pip install sentence-transformers
pip install --upgrade google-generativeai
```

Verify installation:

```bash
python -c "import chromadb; print(chromadb.__version__)"
python -c "from sentence_transformers import SentenceTransformer; print('sentence-transformers OK')"
python -c "import google.generativeai; print('google-generativeai OK')"
```

ChromaDB requires Python 3.8+. If you are on Python 3.12, use `chromadb>=0.4.0`.

Also ensure `chromadb` and `sentence-transformers` are added to your `requirements.txt`.

## Environment Setup

Confirm your `.env` file has a valid Gemini API key:

```
GEMINI_API_KEY=your_key_here
```

Get a free key at aistudio.google.com (no credit card required). The Session 5 code uses sentence-transformers for embeddings (no API key needed — runs locally) and calls the Gemini API only for chat completion. If the Gemini key is missing, the server will start and the knowledge base will initialise successfully (embeddings are local), but the generation step will fail when you hit the endpoint.

## Code State from Session 4

Your project directory should look like this before Session 5:

```
your_project/
├── app/
│   ├── main.py                    (FastAPI app, startup, CORS)
│   ├── database.py                (SQLite engine, create_db_and_tables)
│   ├── dependencies.py            (get_session, get_current_user)
│   ├── models/
│   │   ├── ticket.py              (Ticket SQLModel table, TicketCreate, TicketOut)
│   │   └── user.py                (User SQLModel table)
│   ├── routes/
│   │   ├── tickets.py             (CRUD + classifier call on POST)
│   │   └── auth.py                (register, login)
│   └── services/
│       └── classifier.py          (LLM-based category classifier)
├── .env                           (GEMINI_API_KEY)
├── requirements.txt
└── support_tickets.db             (SQLite DB file from previous sessions)
```

After Session 5, you will add:

```
├── app/
│   ├── knowledge_base/
│   │   └── documents.py           (NEW — 8-10 string constants)
│   └── services/
│       ├── classifier.py          (unchanged)
│       └── rag_service.py         (NEW — chunking, embedding, retrieval, generation)
└── chroma_db/                     (NEW — created automatically by ChromaDB on first run)
```

## Confirm Your Session 4 Codebase Works

Before Session 5, run the server and confirm:

1. `POST /auth/register` creates a user
2. `POST /auth/login` returns a JWT token
3. `POST /tickets` with auth header creates a ticket and returns a `category` field
4. `GET /tickets/{id}` returns the ticket with its category

If any of these fail, fix them before Session 5 — the RAG endpoint depends on a working ticket in the database.

---

# Content to Prepare Before Class

Copy this into a scratch file. You will use it when testing the new endpoint during class.

```text
Test ticket 1 (payment issue):
Subject: My payment keeps failing at checkout
Description: I have tried three times to complete my order but every time I enter my card
details and click Pay, I get an error saying "transaction declined". I have checked with
my bank and they say there is no block on my card. This has been happening for the past
two days.

Test ticket 2 (account deletion):
Subject: I want to permanently delete my account
Description: I no longer need my account and would like to delete all my personal data
including purchase history, saved addresses, and payment methods. Please let me know
the process and how long it takes.

Test ticket 3 (login problem):
Subject: Cannot log into my account after password reset
Description: I clicked Forgot Password and received the reset email but after setting
a new password I still cannot log in. The error says invalid credentials. I have tried
in three different browsers.
```

---

# Prompts for Session 5

Use these prompts during the session when instructed by your instructor.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Support Ticket Resolution Copilot using FastAPI, SQLModel, Gemini (google-generativeai), and sentence-transformers.
The project is a Python backend. Here is the current state of the codebase:

Existing files and what they contain:
- app/main.py — FastAPI app with lifespan startup that calls create_db_and_tables()
- app/database.py — SQLite engine using SQLModel, create_db_and_tables() function
- app/dependencies.py — get_session() DB dependency, get_current_user() JWT dependency
- app/models/ticket.py — Ticket SQLModel table with fields: id, subject, description, status, priority, created_at, category. Also TicketCreate and TicketOut Pydantic models.
- app/models/user.py — User SQLModel table with id, email, hashed_password, role
- app/routes/tickets.py — CRUD endpoints: POST /tickets (calls classifier), GET /tickets, GET /tickets/{id}, PUT /tickets/{id}, DELETE /tickets/{id}
- app/routes/auth.py — POST /auth/register, POST /auth/login returning JWT
- app/services/classifier.py — calls Gemini 1.5 Flash generate_content() to classify ticket into a category string

Add a complete RAG pipeline with the following exact files and structure:

FILE 1: app/knowledge_base/documents.py
- Define 8 to 10 Python string constants (not a file loader, not a dict — plain uppercase constant names like REFUND_POLICY, LOGIN_TROUBLESHOOTING_GUIDE, etc.)
- Each document should be 150 to 400 words covering a distinct support topic
- Required topics: refund policy, payment failure troubleshooting, login issues guide, account deletion process, subscription cancellation guide, password reset steps, billing dispute process, shipping and delivery policy
- Add 2 optional topics if needed: contact support escalation, two-factor authentication setup
- Each document should have clear paragraph breaks (blank lines between paragraphs) since we chunk by paragraph
- Add a constant DOCUMENTS: dict[str, str] at the bottom that maps a short document name to each constant (e.g., {"refund_policy": REFUND_POLICY, "login_troubleshooting": LOGIN_TROUBLESHOOTING_GUIDE, ...})

FILE 2: app/services/rag_service.py
- Import: chromadb, os, google.generativeai as genai, SentenceTransformer from sentence_transformers
- Use chromadb.PersistentClient(path="./chroma_db")
- Collection name: "support_kb" with metadata={"hf:space": "cosine"}
- Embedding model: SentenceTransformer("all-MiniLM-L6-v2") — local, no API key, 384-dim vectors (do NOT use openai.embeddings.create)
- Gemini setup: genai.configure(api_key=os.environ["GEMINI_API_KEY"]); model = genai.GenerativeModel("gemini-1.5-flash")
- Chunking: split each document string by "\n\n" (paragraph breaks), then apply a MAX_CHUNK_SIZE = 500 character limit (split further if a paragraph exceeds this). Filter out empty strings.
- Chunk IDs must be deterministic: format "{doc_name}_chunk_{i}" (e.g., "refund_policy_chunk_0")
- Function signatures required:
    def chunk_document(text: str, doc_name: str, max_chunk_size: int = 500) -> tuple[list[str], list[str]]: (returns chunk_texts, chunk_ids)
    def embed_texts(texts: list[str]) -> list[list[float]]: (calls SentenceTransformer("all-MiniLM-L6-v2").encode(texts).tolist(), returns list of 384-dim vectors)
    def init_knowledge_base() -> None: (called at startup — checks collection.count() > 0 to skip if already populated, otherwise embeds and upserts all documents)
    def get_suggested_response(ticket_subject: str, ticket_description: str) -> dict: (embeds query, calls collection.query with n_results=3, constructs LLM prompt, calls Gemini model.generate_content(prompt) with temperature=0.3, returns dict with keys "suggested_response" and "sources")
- In the LLM prompt: combine system instructions and ticket text + numbered context chunks into a single prompt string for Gemini
- The "sources" value in the returned dict must be the list of retrieved chunk IDs (not document names)

FILE 3: app/routes/tickets.py — add to existing file
- Add this Pydantic model: class SuggestedResponseOut(BaseModel): ticket_id: int, suggested_response: str, sources: list[str]
- Add this endpoint:
    @router.get("/{id}/suggested-response", response_model=SuggestedResponseOut)
    async def get_suggested_response(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
- The endpoint must: load ticket from DB, raise HTTPException 404 if not found, call rag_service.get_suggested_response(ticket.subject, ticket.description), return SuggestedResponseOut
- Do NOT modify any existing endpoints

FILE 4: app/main.py — update startup
- Import rag_service from app.services
- Add rag_service.init_knowledge_base() call inside the lifespan startup block, after create_db_and_tables()
- Add a print or logging statement: "Knowledge base initialisation complete."

Constraints and scope — do NOT generate the following:
- LangChain or LangGraph imports of any kind
- openai library or openai.embeddings.create (use sentence-transformers instead)
- PDF file loader or any file I/O for the knowledge base
- multiple ChromaDB collections
- re-ranking logic
- hybrid search (BM25 + vector)
- FAISS
- streaming responses
- async embedding calls
- refresh token logic

Add clear inline comments in rag_service.py explaining each step of the pipeline.
Use the existing Gemini client pattern from app/services/classifier.py (read that file first to match the genai.configure and GenerativeModel instantiation style).
```

---

## Prompt 2: Improvement Prompt

```text
Improve the RAG pipeline in app/services/rag_service.py and the suggested-response endpoint with the following changes:

1. Source attribution in the response text: modify the LLM prompt to instruct the model to cite its sources inline using the format "According to [source]:" at the start of each paragraph that draws from a specific chunk. The source name should be derived from the chunk ID (e.g., "refund_policy_chunk_0" → "our Refund Policy").

2. Improved prompt engineering: the system message should also instruct the LLM to:
   - Respond in a professional, empathetic support agent tone
   - Limit the response to 3 to 5 sentences
   - If the context does not contain relevant information, say "I do not have enough information to answer this specific question. Please contact our support team directly."
   - Never make up policies or procedures not mentioned in the provided context

3. Graceful fallback: in get_suggested_response(), if collection.query returns zero documents (empty results or distances above 0.8 threshold), return {"suggested_response": "No relevant knowledge base articles found for this ticket. Please handle manually.", "sources": []} without calling the LLM.

4. Add a helper function: def format_source_name(chunk_id: str) -> str that converts "refund_policy_chunk_0" to "Refund Policy" for display in the response.

Do not change the function signatures. Do not add new dependencies.
```

---

## Prompt 3: Debugging Prompt

```text
I am getting a 500 Internal Server Error when hitting GET /tickets/{id}/suggested-response.

The error in the terminal is:

google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded (Gemini free tier 15 RPM limit)

OR

AttributeError: 'numpy.ndarray' object has no attribute 'tolist' (or wrong shape from encode())

OR

chromadb.errors.InvalidCollectionException: Collection support_kb does not exist.

Please diagnose and fix all three possible root causes:

1. For the Gemini rate limit error: add time.sleep(2) before the model.generate_content() call in get_suggested_response(). This respects the 15 RPM free tier limit during classroom demos.

2. For the NumPy array error: ensure embed_texts() calls embedding_model.encode(texts).tolist() — the .tolist() call is required to convert the NumPy array to a plain Python list of lists before passing to ChromaDB. Also filter out empty or whitespace-only strings before calling encode().

3. For the collection not found error: the collection is created at startup but the endpoint is being called before startup completes, OR the PersistentClient path is wrong. Add a module-level check at the start of get_suggested_response() that calls init_knowledge_base() if collection.count() == 0, as a safety fallback.

Show the corrected rag_service.py code with all three fixes applied. Explain what caused each issue.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the code in app/services/rag_service.py to me in technical language suitable for a backend engineering interview.

For each function, explain:
1. What it does and why it exists as a separate function
2. The exact API call being made (endpoint, parameters, response structure)
3. Any design decisions (why paragraph chunking, why upsert not add, why temperature=0.3)
4. What could go wrong and how the current code handles it

Then explain the end-to-end flow:
- What happens at server startup (init_knowledge_base)
- What happens when GET /tickets/{id}/suggested-response is called

Finally, explain the data flowing through the system:
- A document string goes in — what comes out of chunk_document?
- A list of strings goes into embed_texts — what comes back?
- A query vector goes into collection.query — what does the response dict look like?
- The retrieved chunks go into the LLM prompt — how are they formatted?

Do not simplify for beginners. Use correct terminology: vector, cosine similarity, embedding dimension, upsert, collection, token limit, NumPy array, encode().
```

---

## Prompt 5: Interview Explanation Prompt

```text
Help me prepare to explain the RAG pipeline I built in Session 5 during a technical interview.

Structure your response as:

1. One-sentence description of what RAG is
2. Why I added it to the Support Ticket Copilot (the business problem it solves)
3. The exact technical steps in my implementation (ingestion pipeline + retrieval pipeline)
4. Trade-offs I made:
   - Why paragraph chunking over sentence chunking
   - Why ChromaDB over FAISS or Pinecone
   - Why all-MiniLM-L6-v2 (sentence-transformers, local) over a cloud embedding API
   - Why a static knowledge base over a dynamic document store
5. What would change if this went to production with 100,000 documents
6. A 3-sentence answer I can say out loud if asked "describe your RAG pipeline" with no time to think

Keep the explanation technically precise — I know Python and FastAPI, so do not simplify.
```

---

## Prompt 6: Unit Test Generation Prompt

```text
Generate pytest tests for the RAG pipeline in app/services/rag_service.py and the suggested-response endpoint in app/routes/tickets.py.

Project context:
- Tests live in tests/test_rag.py
- The project uses FastAPI TestClient (or httpx AsyncClient)
- Database uses SQLite in-memory for tests
- Gemini API and ChromaDB calls should be mocked — do not make real API calls in tests; sentence-transformers encode() should also be mocked to avoid downloading the model during test runs
- Auth is required on the endpoint — generate a test JWT or mock get_current_user

Tests to generate:

1. test_chunk_document_basic — verify that a multi-paragraph string is split into correct number of chunks with correct IDs (e.g., "test_doc_chunk_0", "test_doc_chunk_1")
2. test_chunk_document_long_paragraph — verify that a single paragraph exceeding MAX_CHUNK_SIZE is split into multiple sub-chunks
3. test_chunk_document_empty_string — verify that empty strings are filtered out of chunk output
4. test_embed_texts_returns_correct_shape — mock SentenceTransformer.encode to return a fake NumPy array of shape (2, 384) and verify embed_texts returns a list of 2 vectors each with 384 elements
5. test_init_knowledge_base_skips_if_populated — mock collection.count() to return 10 and verify embed_texts is NOT called (idempotency check)
6. test_get_suggested_response_returns_correct_shape — mock collection.query to return 3 fake chunks, mock Gemini model.generate_content to return a fake response with a .text attribute, call get_suggested_response and assert the returned dict has keys "suggested_response" and "sources" with correct types
7. test_suggested_response_endpoint_200 — use TestClient to hit GET /tickets/{id}/suggested-response with a valid ticket ID and mocked RAG service, assert HTTP 200 and response body shape
8. test_suggested_response_endpoint_404 — hit GET /tickets/9999/suggested-response and assert HTTP 404
9. test_suggested_response_endpoint_401 — hit GET /tickets/{id}/suggested-response without Authorization header and assert HTTP 401

Use unittest.mock.patch for all external calls. Add clear docstrings to each test explaining what it verifies.
```

---

## Prompt 7: Edge Case and Error State Prompt

```text
Add comprehensive error handling and edge case coverage to the RAG pipeline in app/services/rag_service.py and the endpoint in app/routes/tickets.py.

Handle these specific cases:

1. Gemini API key missing: sentence-transformers runs locally so the knowledge base will always initialise successfully. However, wrap the model.generate_content() call in a try/except and check for missing GEMINI_API_KEY at module load time. Log a clear message ("GEMINI_API_KEY is missing or invalid — generation will fail") and allow the server to start. The suggested-response endpoint should return HTTP 503 with detail "Generation service is not available" if the Gemini key is absent.

2. Empty ticket description: if ticket.description is an empty string or None, construct the query using only ticket.subject. Do not send an empty string to the embeddings API.

3. ChromaDB collection not found: if the collection does not exist when get_suggested_response is called (e.g., the chroma_db directory was deleted), catch chromadb.errors.InvalidCollectionException and raise HTTPException(status_code=503, detail="Knowledge base unavailable. Contact system administrator.").

4. Gemini rate limit during generation: the free tier allows 15 RPM. Wrap the model.generate_content() call in a retry with exponential backoff — attempt 3 times with waits of 1s, 2s, 4s before raising. Use time.sleep for simplicity (no extra libraries). Note: sentence-transformers embedding has no rate limit since it runs locally.

5. LLM returns an empty response: if response.text is None or an empty string after model.generate_content(), return a default fallback: "Unable to generate a suggested response at this time. Please handle this ticket manually."

6. Ticket with no subject: the classifier should have prevented this, but add a guard in get_suggested_response: if both subject and description are empty, raise ValueError("Cannot generate a suggested response for a ticket with no content").

Show the updated code with all error handling in place. Add type hints to all function signatures.
```

---

# What You Should Be Able to Explain After Session 5

After this session, you should be able to answer these questions without notes. These are real interview questions:

1. What is an embedding and what information does it encode?
2. What is cosine similarity and why is it preferred over Euclidean distance for semantic search?
3. What is the difference between the retrieval step and the generation step in a RAG pipeline?
4. Why does RAG reduce hallucination compared to a vanilla LLM call?
5. What is the purpose of chunking and how does chunk size affect retrieval quality?
6. Why must the ingestion and query steps use the same embedding model?
7. What is the purpose of `upsert` in ChromaDB and why is idempotency important at startup?
8. What does `collection.query` return and which fields do you use from that response?
9. How does your `GET /tickets/{id}/suggested-response` endpoint differ technically from `GET /tickets/{id}`?
10. What would change in this pipeline if you had 100,000 documents instead of 10?

---

## Final Session 5 Explanation

Use this in interviews when asked to describe what you built:

```text
In Session 5, I added a RAG pipeline to the Support Ticket Copilot backend. The pipeline embeds a static knowledge base of support policy documents using the sentence-transformers all-MiniLM-L6-v2 model (local, 384-dimensional vectors, no API key) and stores the vectors in a local persistent ChromaDB collection. When a support agent requests a suggested response for any ticket, the system embeds the ticket text using the same local model, retrieves the top-3 semantically similar knowledge base chunks using cosine similarity, and injects those chunks as context into a Gemini 1.5 Flash chat completion call. The result is a grounded suggested response that cites actual company policy rather than relying on the LLM's parametric memory. This is exposed via a GET /tickets/{id}/suggested-response endpoint protected by JWT auth.
```
