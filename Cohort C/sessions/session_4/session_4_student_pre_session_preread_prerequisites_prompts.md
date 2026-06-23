# Session 4 Student Pre-Session File: Basic RAG Pipeline

## What We Are Building

In this 8-session AI Systems Interview Portfolio, we are not building one big app. We are building a collection of standalone AI engineering modules — each one a clean, well-understood Python script that demonstrates a real technique used in production AI systems.

The complete portfolio will look like this when finished:

```
structured_output_engine.py    ← Session 1: Structured Output Prompt Engine
output_examples.json
llm_logger.py                  ← Session 2: LLM Logging and Evaluation Tracker
llm_logs.csv
eval_summary.json
ai_handler.py                  ← Session 3: Serverless-Style AI Function
.env.example
rag_pipeline.py                ← Session 4: Basic RAG Pipeline  (TODAY)
chroma_db/
rag_evaluator.py               ← Session 5: RAG Evaluation and Improvement
rag_eval_report.csv
agent_router.py                ← Session 6: Simple Agent Router
vision_ocr_module.py           ← Session 7: Vision/OCR Mini Module
ocr_output.json
README.md                      ← Session 8: Final System Design and Interview Demo
```

## Session 4 Goal

Build a complete Retrieval-Augmented Generation (RAG) pipeline in a single Python file called `rag_pipeline.py`. This script will embed support documents, store them in a local vector database, retrieve the most relevant chunks for any query, and generate a grounded answer using Gemini 1.5 Flash.

## Session 4 Deliverable

- `rag_pipeline.py` — the complete RAG pipeline script
- `chroma_db/` — a local persistent folder created automatically by ChromaDB when the script runs

---

# Pre-Read

## Why Does This Module Exist in the Portfolio?

RAG (Retrieval-Augmented Generation) is one of the most frequently asked topics in AI engineering interviews at every level from fresher to senior. Almost every company building an AI product that needs to answer questions about its own data — customer support bots, internal knowledge assistants, document Q&A systems — uses some form of RAG. Understanding RAG means understanding three foundational AI engineering concepts simultaneously: how meaning is represented as numbers (embeddings), how similarity search works at scale (vector databases), and how to give an LLM accurate, grounded context without retraining it.

This module also directly feeds into Session 5, where you will evaluate the quality of the pipeline you build today. That means by the end of Session 5, you will have both built and evaluated a RAG system — a combination that is almost never demonstrated at the fresher level.

## Portfolio Module Map

```
Session 1: Structured Output Prompt Engine
    structured_output_engine.py + output_examples.json
    Concept: prompt engineering, JSON schema, response parsing
            |
            v
Session 2: LLM Logging and Evaluation Tracker
    llm_logger.py + llm_logs.csv + eval_summary.json
    Concept: LLMOps, logging, metrics, evaluation design
            |
            v
Session 3 — Serverless-Style AI Function (local handler pattern established)
    ai_handler.py + .env.example
    Concept: function design, handler pattern, .env, error handling
            |
            v
Session 4: Basic RAG Pipeline  <-- TODAY
    rag_pipeline.py + chroma_db/
    Concept: embeddings, chunking, vector DB, retrieval, grounded generation
            |
            v
Session 5 — RAG Evaluation and Improvement
    rag_evaluator.py + rag_eval_report.csv
    Concept: retrieval metrics, faithfulness scoring, LLM-as-judge
    (USES rag_pipeline.py and chroma_db/ from Session 4)
            |
            v
Session 6: Simple Agent Router
    agent_router.py
    Concept: LLM-based intent classification, tool dispatch, agent loop
            |
            v
Session 7: Vision/OCR Mini Module
    vision_ocr_module.py + ocr_output.json
    Concept: multimodal Gemini input, structured JSON extraction from images
            |
            v
Session 8: Final System Design and Interview Demo
    README.md + architecture_diagram.md + demo_script.md
    Concept: portfolio documentation, system design communication, interview preparation
```

Sessions 4 and 5 are directly connected. The `rag_pipeline.py` and `chroma_db/` folder you create today are the inputs for Session 5.

## Key Concepts to Revise Before Session 4

Spend 10–15 minutes reviewing these before class. You do not need to be an expert — just have the vocabulary fresh.

**1. What is an embedding?**
An embedding is a numerical representation of text as a vector (a list of numbers). It captures the meaning of the text in a way that allows mathematical comparison. You likely encountered this when studying word2vec, transformers, or BERT.

**2. What is cosine similarity?**
A measure of how similar two vectors are by comparing the angle between them. Two embeddings with high cosine similarity represent texts with similar meanings. This is the core mechanism behind semantic search.

**3. What is a vector database?**
A database that stores embedding vectors and lets you query it by providing a vector — it returns the most similar stored vectors. ChromaDB, Pinecone, and Weaviate are examples. This session uses ChromaDB, which runs entirely on your local machine.

**4. What is RAG (Retrieval-Augmented Generation)?**
A pattern where you retrieve relevant documents from a knowledge base and inject them into the LLM prompt before generating an answer. This reduces hallucination by grounding the answer in actual retrieved text.

**5. What is document chunking?**
Splitting a long document into smaller pieces before embedding. You do this because embedding models have a token length limit and because retrieving a small, focused paragraph is more precise than retrieving a whole document.

**6. What is the sentence-transformers library?**
A Python library for generating high-quality text embeddings using pre-trained transformer encoder models. The `all-MiniLM-L6-v2` model is fast, lightweight, produces 384-dimensional embeddings, and runs entirely locally — no API key needed.

**7. What is ChromaDB?**
An open-source embedding database that runs locally. It stores embeddings with their associated text and metadata, and supports similarity search via a `.query()` method. With `PersistentClient`, data is saved to disk and survives between Python runs.

**8. What is grounded generation?**
Passing retrieved document text into the LLM prompt and instructing the model to base its answer on that text, not its general training data. This is the "G" in RAG — the generation step is grounded in retrieved context.

## Technical Explanation of the Core Concept

A RAG pipeline has two phases: **ingestion** (done once) and **querying** (done for each user question).

**Ingestion phase:**
```
Support document (string)
    → split into paragraphs (chunking)
    → each paragraph → SentenceTransformer → 384-dim embedding vector
    → store (chunk_text, embedding_vector, chunk_id) in ChromaDB
```

**Query phase:**
```
User question (string)
    → SentenceTransformer → 384-dim query vector
    → ChromaDB.query(query_vector, n_results=3)
    → returns top-3 most similar chunks
    → build prompt: "Based on this context: [chunk1][chunk2][chunk3] Answer: [question]"
    → Gemini 1.5 Flash generates grounded answer
    → return answer + retrieved chunks
```

The key insight: the model never directly accesses ChromaDB. The retrieved text is copied into the prompt as a string. The model reads it as part of its input context.

---

# Setup Before Class

Complete all of these steps before the live session. If any step fails, do not wait — message the instructor or attempt the fix using the debugging resources listed.

## Required pip Installs

Run these in your terminal (use your active Python environment):

```bash
pip install google-generativeai
pip install sentence-transformers
pip install chromadb
```

Important notes:
- `sentence-transformers` (hyphen in pip) imports as `sentence_transformers` (underscore in Python)
- `chromadb` latest stable version is recommended; if you see dependency conflicts, try `pip install chromadb==0.5.0`
- On first run, `SentenceTransformer("all-MiniLM-L6-v2")` will download a ~90MB model file. This is a one-time download. It will not download again on subsequent runs.

## Gemini API Key Setup

1. Go to: https://aistudio.google.com
2. Sign in with a Google account
3. Click "Get API Key" → "Create API key in new project"
4. Copy the key (it starts with `AIza...`)
5. Set it as an environment variable:

On Mac/Linux:
```bash
export GEMINI_API_KEY="AIzaSy..."
```

On Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=AIzaSy...
```

On Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="AIzaSy..."
```

To make it permanent on Mac/Linux, add the export line to your `~/.zshrc` or `~/.bashrc` file.

## Verify Your Setup

Run this one-time test script before class to confirm everything works:

```python
# save as verify_setup.py and run: python verify_setup.py

import os

print("Checking google-generativeai...")
import google.generativeai as genai
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in environment")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Say: setup ok")
    print("Gemini:", response.text.strip())

print("Checking sentence-transformers...")
from sentence_transformers import SentenceTransformer
st_model = SentenceTransformer("all-MiniLM-L6-v2")
vec = st_model.encode("test sentence")
print("Embedding shape:", vec.shape)  # should print (384,)

print("Checking chromadb...")
import chromadb
client = chromadb.Client()
col = client.get_or_create_collection("test")
print("ChromaDB in-memory client: OK")

print("All checks passed.")
```

Expected output:
```
Checking google-generativeai...
Gemini: setup ok
Checking sentence-transformers...
Embedding shape: (384,)
Checking chromadb...
ChromaDB in-memory client: OK
All checks passed.
```

---

# Sample Data to Prepare Before Class

The knowledge base for this session consists of 6–8 customer support documents for a fictional SaaS product. These are defined as Python string constants inside the script — you do not need to create separate files.

Below is the content you can use or modify. Review it before class so you understand what the RAG system will be answering questions about.

```text
REFUND_POLICY:
Our refund policy allows customers to request a full refund within 30 days of purchase.

To request a refund:
Submit a refund request through the Help Center.
Provide your order ID and the reason for the refund.
Refunds are processed within 5–7 business days to the original payment method.

After 30 days, refunds are not available unless the product is defective.
Subscription refunds are prorated for the unused billing period.

LOGIN_TROUBLESHOOTING:
If you cannot log in to your account, try these steps in order.

First, confirm you are using the correct email address.
Second, use the Forgot Password link on the login page to reset your password.
Third, clear your browser cache and cookies and try again.
Fourth, try logging in from a different browser or device.

If none of these steps work, contact support with your account email and a screenshot of the error.
Two-factor authentication issues should be reported with your phone number.

PAYMENT_FAILURE:
Payment failures can occur for several reasons.

The most common reason is an expired or invalid credit card.
Update your payment method in Account Settings under Billing.

Other common causes include insufficient funds, bank blocks on online transactions, and incorrect billing address.
If your payment fails three times, your account will be temporarily locked for security reasons.

Contact your bank if the payment continues to fail after updating the card details.
We accept Visa, Mastercard, and American Express. We do not accept PayPal.

SUBSCRIPTION_CANCELLATION:
You can cancel your subscription at any time from Account Settings.

Navigate to Account Settings and click Manage Subscription.
Click Cancel Subscription and confirm your choice.

Your subscription will remain active until the end of the current billing period.
You will not be charged again after cancellation.
Your data will be retained for 90 days after cancellation in case you decide to reactivate.

To reactivate, log in and click Reactivate Subscription in Account Settings.

ACCOUNT_DELETION:
Account deletion is permanent and cannot be undone.

To delete your account:
Go to Account Settings and scroll to the bottom.
Click Delete Account.
Enter your password to confirm.
Your account and all data will be deleted within 48 hours.

Exported data will be sent to your registered email before deletion.
Active subscriptions must be cancelled before account deletion.
Refund eligibility is assessed separately from account deletion.

BILLING_FAQ:
Our billing cycle runs on a monthly or annual basis depending on your chosen plan.

Invoices are sent to your registered email on the billing date.
You can download past invoices from Account Settings under Billing History.

We support multi-seat billing for teams. Each seat is billed at the per-user rate.
Volume discounts apply for 10 or more seats — contact sales for pricing.

Tax is applied based on your billing address and local regulations.
VAT invoices are available for EU customers upon request.

PASSWORD_RESET:
If you have forgotten your password, use the Forgot Password link on the login page.

Enter your registered email address.
You will receive a password reset link within 5 minutes.
The link expires in 24 hours.

If you do not receive the email, check your spam folder.
Add support@company.com to your contacts to prevent future emails from going to spam.
If the email still does not arrive, contact support with your account email.

TWO_FACTOR_AUTH:
Two-factor authentication (2FA) adds a second layer of security to your account.

To enable 2FA, go to Account Settings and click Security.
You can use an authenticator app (such as Google Authenticator or Authy) or receive codes by SMS.

If you lose access to your 2FA device, use your backup codes saved during 2FA setup.
If you have lost your backup codes, contact support with a government-issued ID to verify your identity.
Support cannot disable 2FA without identity verification.
```

---

# Prompts for Session 4

Use these prompts during the session when instructed. All prompts are copy-paste ready for Claude Code or Cursor.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI engineering portfolio. I have already built:
- structured_output_engine.py (Session 1: structured output with Gemini)
- llm_logger.py (Session 2: LLM logging and evaluation tracking)
- ai_handler.py (Session 3: serverless-style AI handler function)

Now build Session 4: a complete RAG pipeline.

Create a Python file called rag_pipeline.py with the following specifications:

KNOWLEDGE BASE:
Define 6-8 customer support documents as Python string constants at the top of the file.
Topics: refund policy, login troubleshooting, payment failure, subscription cancellation, account deletion, billing FAQ, password reset, two-factor authentication.
Each document should be 3-6 paragraphs with natural paragraph breaks (double newlines between paragraphs).

EMBEDDINGS:
Use the sentence-transformers library with model "all-MiniLM-L6-v2".
Import as: from sentence_transformers import SentenceTransformer
This model is fully local and requires no API key.

VECTOR DATABASE:
Use ChromaDB with persistent storage.
Import as: import chromadb
Use: chromadb.PersistentClient(path="chroma_db")
Collection name: "support_docs"
Use get_or_create_collection so repeated runs do not throw duplicate errors.
Check if collection already has documents before re-ingesting.

CHUNKING:
Split each document into chunks by splitting on double newline "\n\n".
Filter out empty strings after splitting.
Each chunk gets a unique string ID like "doc_0_chunk_2".

INGESTION:
Generate embeddings for all chunks using model.encode(list_of_chunks).
Use collection.add(ids=..., embeddings=..., documents=...) to store chunks.

RETRIEVAL:
For a given query, generate its embedding using model.encode([query]).
Call collection.query(query_embeddings=[query_embedding], n_results=3).
Extract the top-3 chunks from result["documents"][0].

GENERATION:
Use Gemini 1.5 Flash via the google-generativeai library.
Configure with: genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
Model: genai.GenerativeModel("gemini-1.5-flash")
Build a prompt that includes: a system instruction to answer only from context, the 3 retrieved chunks labeled as Context, and the user's question.
Call model.generate_content(prompt) to get the answer.
Wrap the Gemini call in try/except to handle rate limit errors (google.api_core.exceptions.ResourceExhausted).

MAIN FUNCTION:
def ask(query: str) -> dict:
    Returns: {"answer": str, "retrieved_chunks": list[str]}
    This function should: embed query, retrieve top-3 chunks, build prompt, call Gemini, return dict.

OUTPUT:
When the script is run directly (if __name__ == "__main__":), run 3 sample queries:
1. "How do I request a refund?"
2. "My login is not working"
3. "How do I cancel my subscription?"
For each query, print the query, the 3 retrieved chunks, and the generated answer.

CONSTRAINTS:
Do not use OpenAI or any paid embedding API.
Do not add PDF parsing, file upload, web scraping, or HTTP servers.
Do not use LangChain or any framework — raw library calls only.
Do not add re-ranking, hybrid search, or multiple collections.
Add clear inline comments explaining each major step.
The script must run with: python rag_pipeline.py
```

---

## Prompt 2: Improvement Prompt

```text
Improve rag_pipeline.py with the following changes. Do not change the core pipeline logic or the ask() function signature.

1. Add a reset_collection() function that deletes and recreates the "support_docs" collection.
   This is useful when the knowledge base content changes and stale embeddings need to be cleared.

2. Improve the ingestion guard: before running collection.add(), check collection.count().
   If count > 0, skip ingestion and print "Collection already populated. Skipping ingestion."
   If count == 0, run ingestion and print "Ingesting X chunks into ChromaDB."

3. Improve the output format: when printing results in the __main__ block,
   print a separator line between each query result.
   Print retrieved chunks with their index: "Chunk 1:", "Chunk 2:", "Chunk 3:".
   Print the answer with a clear label.

4. Add a compare_rag_vs_vanilla(query) function that:
   - runs ask(query) to get the RAG answer
   - also calls Gemini directly with only the question and no context (vanilla call)
   - prints both answers side by side with labels "RAG Answer:" and "Vanilla LLM Answer:"
   This demonstrates the value of RAG vs a plain LLM call.

5. Add input validation in ask(): if query is empty or only whitespace, return
   {"answer": "Query cannot be empty.", "retrieved_chunks": []} immediately.

Keep all existing code intact. Only add to it.
```

---

## Prompt 3: Debugging Prompt — ChromaDB and Sentence-Transformers Issues

```text
I am getting errors when running rag_pipeline.py. Help me debug each of these:

Error 1 (ChromaDB duplicate IDs):
chromadb.errors.UniqueConstraintError: IDs ['doc_0_chunk_0'] already exist in the collection.

This happens when I run the script a second time. The ingestion code tries to add the same chunk IDs again.

Fix: Modify the ingestion section to check collection.count() before calling collection.add().
If count > 0, skip ingestion entirely. Show me the corrected ingestion block.

Error 2 (Sentence-transformers import error):
ModuleNotFoundError: No module named 'sentence_transformers'

I installed it with: pip install sentence-transformers
But the import still fails.

Fix: Explain why the package name (sentence-transformers with hyphen) differs from the import name (sentence_transformers with underscore). Show me the correct pip install command and the correct import statement.

Error 3 (Gemini API rate limit):
google.api_core.exceptions.ResourceExhausted: 429 RESOURCE_EXHAUSTED

This happens when I run multiple queries quickly on the free tier.

Fix: Wrap the model.generate_content() call in a try/except block.
On ResourceExhausted, return the retrieved chunks with a message that generation is temporarily unavailable.
Also add import time and time.sleep(2) between queries in the __main__ block.

Show me the corrected code for all three fixes.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the rag_pipeline.py code to me as if I need to explain it in a technical interview.

Cover each of these sections:

1. Document constants at the top — why are they defined as string constants instead of loading files?

2. The chunking logic — what does split("\n\n") do? Why not split on single newlines or by sentence?
   What is the trade-off between chunk size and retrieval precision?

3. SentenceTransformer("all-MiniLM-L6-v2") — what does this model do?
   What does "384 dimensions" mean? Why is this model a good choice over the OpenAI embeddings API?

4. chromadb.PersistentClient(path="chroma_db") — what does persistent mean here?
   What is stored inside the chroma_db/ folder? What is the difference from Client() (in-memory)?

5. collection.add(ids=..., embeddings=..., documents=...) — what is stored for each chunk?
   Why do IDs need to be unique strings?

6. collection.query(query_embeddings=[...], n_results=3) — how does ChromaDB find the top 3?
   What does the returned dictionary look like? Why does result["documents"] return a nested list?

7. The prompt construction in ask() — how is retrieved context injected into the prompt?
   Why does it matter that we instruct the model to answer only from the provided context?

8. model.generate_content(prompt) — what Gemini model is used? How is the API configured?
   What would happen if we sent an empty context?

9. The ask() return value — why return a dict with both "answer" and "retrieved_chunks"?
   Why is showing the retrieved chunks important for debugging and transparency?

Do not rewrite the code. Explain each section clearly using technical language I can use in an interview.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Help me explain rag_pipeline.py in a job interview setting.

Give me responses for each of these interview questions:

1. "What is RAG and why did you build this?"
   Explain what RAG is, what problem it solves, and why it matters for AI engineering.

2. "Walk me through the pipeline."
   Describe every step: document ingestion, chunking, embedding, storage, query embedding, retrieval, prompt construction, and generation.

3. "Why use sentence-transformers instead of OpenAI embeddings?"
   Cover: local vs. API-based, cost, latency, privacy, and quality trade-offs.

4. "What is a vector database and why did you use ChromaDB?"
   Explain what ChromaDB stores, how similarity search works, and why ChromaDB is a good choice for a local/portfolio use case.

5. "What are the limitations of this pipeline?"
   Cover: static knowledge base, no re-ranking, no metadata filtering, small collection size, and what would break in production.

6. "How is this different from just asking Gemini the same question?"
   Explain the difference between a vanilla LLM call and a RAG-augmented call.

Keep each answer to 3-5 sentences. Use technical vocabulary correctly. Avoid marketing language.
```

---

## Prompt 6: Test Case Generation Prompt

```text
Generate 6 additional test queries to run against rag_pipeline.py.

Requirements for the test queries:
1. Two queries should be clearly answerable from the knowledge base (e.g., asking about refunds or login).
2. Two queries should be partially answerable — they ask about something mentioned in the documents but from an unexpected angle.
3. One query should be about a topic NOT in the knowledge base (to test what the model does when context is insufficient).
4. One query should be very short and ambiguous (e.g., "billing?") to test edge case behavior.

For each query, write:
- The query text
- Which document(s) you expect to be retrieved
- What the expected behavior of the RAG system should be (correct answer, partial answer, or graceful fallback)

Also write code to run all 6 queries in a loop using ask() and print the results, formatted cleanly.
```

---

## Prompt 7: Edge Case and Failure Mode Prompt

```text
Add robust edge case handling to rag_pipeline.py. Do not change the core pipeline logic.

Add handling for the following failure scenarios:

1. Empty query: if query is empty string or only whitespace, return immediately with a helpful message.

2. Query too short: if query is fewer than 3 characters, return a message asking for a more specific question.

3. Gemini API key missing: if os.environ.get("GEMINI_API_KEY") returns None, raise a clear ValueError with a message explaining how to set the key.

4. ChromaDB collection empty: after collection.query(), check if result["documents"][0] is an empty list. If so, return a message saying the knowledge base has no matching documents.

5. Gemini rate limit (429): wrap model.generate_content() in try/except for google.api_core.exceptions.ResourceExhausted. On this error, return the retrieved chunks with answer: "Generation temporarily unavailable due to rate limit. Retrieved context shown above."

6. Sentence-transformers model not downloaded: wrap SentenceTransformer() initialization in try/except for OSError. On this error, print a clear message: "Model download failed. Run: pip install sentence-transformers and ensure you have internet access for first-time model download."

Show me the updated ask() function and the updated model initialization block with all these checks added.
```

---

# What You Should Be Able to Explain After Session 4

By the end of the session, you should be able to answer all of these without looking at your notes:

1. What is RAG and what problem does it solve compared to a vanilla LLM call?
2. What is an embedding and what does it mean for two embeddings to be "similar"?
3. What does cosine similarity measure, and why does it work for semantic search?
4. Why do we chunk documents before embedding instead of embedding the whole document at once?
5. What does `SentenceTransformer("all-MiniLM-L6-v2")` do, and why is it a good local alternative to the OpenAI embeddings API?
6. What does ChromaDB store for each chunk, and what does "persistent" mean in `PersistentClient`?
7. When `collection.query()` is called with `n_results=3`, how does ChromaDB find the top 3 chunks?
8. How exactly does retrieved context get passed to Gemini? What does the prompt look like?
9. What is the difference between the answer quality when using RAG vs. calling Gemini directly with no context?
10. What are three things that would break in this pipeline if you moved it to production?

---

## Final Session 4 Explanation

Memorize this 3-4 sentence explanation. You should be able to say this in an interview without reading it:

```text
I built a complete RAG pipeline in Python that answers customer support queries using a local knowledge base. The pipeline chunks and embeds 8 support documents using sentence-transformers all-MiniLM-L6-v2 — a fully local embedding model — and stores the embeddings in ChromaDB with persistent local storage. When a query comes in, it is embedded using the same model, and the top-3 most semantically similar chunks are retrieved from ChromaDB using cosine similarity. Those chunks are injected into a Gemini 1.5 Flash prompt as context, and the model generates a grounded answer that is verifiably based on the retrieved documents rather than the model's general training data.
```
