# Session 8 Instructor File: Final System Design and Interview Demo

## Session Title

Final System Design and Interview Demo

## Duration

2 hours

## Portfolio Module

Module 8 — Portfolio Consolidation: System Design Documentation and Interview Readiness

## Session 8 Objective

By the end of Session 8, students will have a professionally documented AI Systems Interview Portfolio. They will be able to present each module in a structured interview setting, explain architectural decisions with production-aware vocabulary, articulate trade-offs and limitations, and deliver a confident 2-minute spoken demo. This session does not introduce any new AI feature. It consolidates, documents, and wraps the full portfolio built across Sessions 1–7.

## Session 8 Deliverables

Students will produce the following documentation artifacts:

1. README.md — Full portfolio overview with setup instructions, module list, and Gemini API setup guide
2. architecture_diagram.md — Text-based Mermaid diagram showing how all 7 modules connect
3. demo_script.md — A 2-minute spoken walkthrough script for presenting the portfolio live
4. viva_prep.md — 15 interview Q&A pairs covering all modules and production topics
5. module_summary.md — One-page summary table of all 7 modules with concept, tool, output, and limitation
6. limitations.md — Per-module breakdown of what breaks in production and how to address it

---

## Cross-Session Reference

**Previous session:** Session 7 — Vision/OCR Mini Module (all 7 portfolio modules built)

**Next session:** None — this is the final session

---

## Strict Scope Control

### Include

- README.md covering all 7 portfolio modules with clear setup and file structure
- Architecture diagram using Mermaid or clean ASCII text notation
- Demo script: spoken, interview-style, 2 minutes, structured narrative
- Viva prep: 15 Q&A pairs, technically specific, covering all modules
- Module summary: one-pager table format, all 7 modules
- Limitations document: production-aware, per-module failure analysis
- Cost and latency notes for Gemini 1.5 Flash at scale
- Safety notes: prompt injection, PII, hallucination risks per module
- Interview vocabulary practice: latency, throughput, cost per call, chunking strategy, embedding dimensions, hallucination rate

### Do Not Include

- Any new Python script or AI feature
- New ChromaDB collection or Gemini API call
- FastAPI, Flask, Streamlit, or any web framework
- New fine-tuning experiment or new RAG pipeline
- Cloud deployment steps (mention only as architecture commentary)
- Docker, Kubernetes, or CI/CD pipeline setup
- New LangChain or LangGraph integration
- A new evaluation framework or benchmarking experiment
- Redesigning or refactoring any existing module

---

# Instructor Framing

## Opening Message

Show students the complete folder structure across Sessions 1–7 before starting. Let them see all seven Python scripts side by side. Tell them: "You have now built seven functional AI engineering modules. Most engineering candidates who apply for AI roles cannot explain their own projects clearly in an interview. Today is the session where you fix that. We are going to document everything, draw the architecture, prepare 15 interview answers, and rehearse a 2-minute demo pitch. You will leave this session with a portfolio you can actually open in front of an interviewer."

## Key Philosophy

An AI engineer who cannot explain their system is less valuable than one who can. Production-readiness is as much about communication as it is about code. A portfolio without documentation is a folder of scripts. With documentation, it is an engineering artifact. Today we turn scripts into a portfolio.

## Repeated Instructor Line

"You built it. Now own it. That means documenting it, presenting it, and defending every design decision."

---

# Session Flow

## 0–10 min: Opening — Show the Portfolio, Recap All 7 Modules

Display the full project folder. Walk through each session's output file by name. Ask students to describe each module in one sentence before you explain. The goal is activation: students should feel ownership over what they built. Show the complete list on screen: structured_output_engine.py, llm_logger.py, ai_handler.py, rag_pipeline.py, rag_evaluator.py, agent_router.py, vision_ocr_module.py. Point out that today's task is not to build new code but to wrap these seven artifacts into an interview-ready portfolio. Tell students explicitly that this is the hardest session because explaining code is harder than writing it.

## 10–20 min: Concept Explanation — What Is AI System Design Communication?

Explain the difference between a working system and a communicable system. A senior AI engineer or hiring manager will ask: "Walk me through how you built this." They expect answers that include: what the components are, how data flows between them, why each technology was chosen, what the failure modes are, and how this would change at scale. Introduce the vocabulary students need: latency (time per LLM call), throughput (calls per second), cost per call (Gemini free tier vs paid tier), context window (Gemini 1.5 Flash: 1M tokens), embedding dimensions (all-MiniLM-L6-v2: 384 dimensions), vector similarity search, hallucination risk, retrieval precision vs recall. Explain that architecture diagrams are not just visuals — they are how engineers communicate system boundaries to other engineers. Spend 3 minutes on the concept of "production readiness": what makes a prototype different from a production system (monitoring, error handling, auth, cost control, rate limiting, logging, fallback strategies).

## 20–35 min: Build Using Claude Code or Cursor — README and Architecture Diagram

Students use Prompt 1 from the student file to generate README.md. They use Prompt 2 to generate architecture_diagram.md. Instructor monitors outputs. README.md must include: project title, one-line description of each module, technology stack table, Gemini API setup instructions, sentence-transformers install, ChromaDB install, folder structure, and how to run each script. Architecture diagram must show: all 7 modules as labeled nodes, Gemini 1.5 Flash as a shared external dependency, ChromaDB as a shared persistent store for Sessions 4 and 5, sentence-transformers as a shared embedding layer, arrows showing the dependency between Session 4 (RAG Pipeline) and Session 5 (RAG Evaluator), and a legend for API calls vs local operations. Remind students: the diagram does not need to be beautiful, it needs to be correct and explainable.

## 35–50 min: Walk Through Generated Files — Line by Line Explanation

Open README.md and walk through every section. Ask students: "If you sent this README to a hiring manager right now, what questions would they still have?" Common gaps: no mention of Gemini API rate limits, no explanation of why ChromaDB was chosen over Pinecone or FAISS, no mention of embedding model choice and its trade-offs, no cost estimate. Open architecture_diagram.md and trace the data flow for each module. Ask: "Where does the user's input enter the system? Where does Gemini get called? Where is the output stored?" Walk students through the Mermaid syntax if they are unfamiliar. Explain how to read a top-down or left-right Mermaid graph. Point out that Session 4 and Session 5 share the same ChromaDB collection — this is an important architectural dependency that must be explained.

## 50–65 min: Student Follow-Along Build

Students generate demo_script.md using Prompt 3 and viva_prep.md using Prompt 4. Instructor monitors both outputs. For demo_script.md: the spoken script must be 2 minutes (approximately 300 words), start with a one-sentence summary of the portfolio, cover all 7 modules with one sentence each, include one production-awareness comment ("In production, I would add rate limiting and a fallback response"), and end with a clear statement of what the student learned. For viva_prep.md: students should check that all 15 Q&A pairs are technically specific, mention actual library names, function names, and design decisions. If Gemini generates generic answers, students use Prompt 4b (debugging follow-up) to regenerate with more specificity.

## 65–80 min: Generate Module Summary and Limitations Files

Students use Prompt 5 to generate module_summary.md and Prompt 6 to generate limitations.md. module_summary.md must be a table with columns: Session, Module Name, Core Concept, Python File, Key Library, Output File, One-Line Limitation. limitations.md must address each of the 7 modules individually with: what the module does not handle, what would break at scale, what a production version would add. Instructor reviews sample outputs on screen. Common failure: Gemini generates limitations that are too vague ("could be improved for production"). Push students to get specific: "ChromaDB's local persistence does not support concurrent writes — for a multi-user system you would migrate to a managed vector store like Pinecone or Weaviate."

## 80–95 min: Edge Cases, Error Handling, and Failure Mode Analysis

This block is conceptual but grounded in the actual modules. Walk through each module and ask: "What happens if the Gemini API returns a 429 rate limit error in this module?" Answer for each: structured_output_engine.py — response parsing fails if rate limit is hit and no retry logic exists; llm_logger.py — the log entry is still written but the response field is empty, which can corrupt eval_summary.json averages; ai_handler.py — the serverless-style handler returns a 500-equivalent dict; rag_pipeline.py — the retrieve step succeeds but the generate step fails, producing a silent hallucination risk; rag_evaluator.py — evaluation scores are missing for failed calls; agent_router.py — the router returns the correct intent but the tool execution fails silently; vision_ocr_module.py — the image is sent but no structured output is returned. Discuss: how would you add retry logic? Answer: use a simple exponential backoff loop in Python (time.sleep with increasing delays). How would you add fallback? Answer: return a default response dict instead of raising an exception.

## 95–105 min: Concept Pause — System Design Vocabulary and Interview Storytelling

This is the most important conceptual block. Teach students the four interview storytelling frameworks they need:

Framework 1 — The 30-Second Module Explanation: "In Session X, I built [module name]. It does [one sentence of what it does]. I used [library] because [reason]. The output is [file or structure]. The limitation is [one honest limitation]."

Framework 2 — The Architecture Walk: "The portfolio is structured as seven standalone Python modules. Sessions 4 and 5 are connected — the RAG pipeline builds a ChromaDB collection that the RAG evaluator reads. All modules that call an LLM use Gemini 1.5 Flash via the google-generativeai library. Embeddings are generated locally using sentence-transformers all-MiniLM-L6-v2, which produces 384-dimensional vectors."

Framework 3 — The Trade-Off Statement: "I chose ChromaDB because it runs locally with no infrastructure setup, which is appropriate for a portfolio project. In production, I would switch to a managed vector store to support concurrent reads, horizontal scaling, and persistent backups."

Framework 4 — The Limitation and Improvement Pair: "The current RAG pipeline uses fixed chunk sizes of 500 characters. In production, I would experiment with semantic chunking or sliding window chunking to improve retrieval precision, and I would add a re-ranking step using a cross-encoder."

Have students practice each framework for two modules of their choice out loud.

## 105–115 min: Interview Discussion and Viva Practice

Use the 15 interview questions from the Questions section below. Do not rush. Pick 5–7 and run them as a mock viva. Students give answers verbally. Instructor provides one improvement comment per answer. Focus on: specificity (did they name the library, the function, the parameter?), honesty (did they admit the limitation?), architecture awareness (did they explain the data flow, not just the feature?). If students struggle, return to their viva_prep.md and ask them to read their own model answer first, then restate it in their own words.

## 115–120 min: Wrap-Up — Show Final Deliverables, Portfolio Summary

Display all 6 documentation files on screen. Congratulate students on completing all 8 sessions. Tell them: "You now have seven working Python modules and a fully documented portfolio. You can share this on GitHub. You can open it in an interview. You can walk through the architecture diagram and explain every arrow." Remind students about the cost/latency notes in limitations.md — this is often what separates average candidates from strong ones in AI engineering interviews. Preview: there is no Session 9. This is the final session. Encourage students to record themselves delivering the demo_script.md out loud and watch it back once before their next interview.

---

# Instructor Notes

## What to Emphasize

Session 8 is a metacognitive session. Students are not learning a new technical concept — they are learning how to articulate seven technical concepts they already built. The instructor's job is to push students toward specificity. Vague answers like "it uses AI to process text" are not acceptable. Force the technical vocabulary: embedding dimensions, cosine similarity, context window, structured output, intent classification, retrieval precision, hallucination risk. Emphasize that README.md is not optional — it is the first thing a hiring manager or technical screener reads. A missing README signals that the candidate does not think about maintainability or collaboration. Emphasize that the architecture diagram must be explainable without looking at the code. If a student cannot trace the data flow through the diagram, the diagram is incomplete. Emphasize that the demo script must be deliverable in 2 minutes without notes — not read from a screen.

## Common Student Mistakes

1. Writing a README.md that lists files but does not explain what each module does. Instructor fix: ask "If someone cloned this repo and had never heard of your project, would they know what to run first and why?"

2. Generating a Mermaid diagram that Claude Code produces but the student cannot explain. Students paste the diagram without reading it. Instructor fix: ask the student to trace one data flow through the diagram out loud, arrow by arrow.

3. Viva answers that cite the wrong library. For example, a student says "I used OpenAI embeddings" because they are more familiar with that library. This portfolio uses sentence-transformers exclusively for embeddings. Instructor fix: stop immediately and correct: "This portfolio uses sentence-transformers all-MiniLM-L6-v2, not OpenAI. Saying the wrong library in a viva is a red flag."

4. Demo script that is too long (over 3 minutes) because students try to explain every function. Instructor fix: enforce the 2-minute rule. Timer them. Tell them: "An interviewer who has to wait 4 minutes for your intro has already decided you cannot communicate concisely."

5. Limitations.md that is generic. Phrases like "could be more efficient" or "would need more testing" are not acceptable. Instructor fix: push for specific failure modes, for example: "rag_pipeline.py does not handle documents larger than the ChromaDB default chunk limit, and cosine similarity can return irrelevant results if the query embedding is semantically distant from any stored chunk."

6. Students who try to add new features in Session 8. Common request: "Can I add a Streamlit UI today?" Instructor response: "No. Session 8 is documentation and interview prep only. A Streamlit UI that breaks during your interview demo is worse than no UI."

7. Students who receive a `google.api_core.exceptions.ResourceExhausted: 429` error when generating long documents like README.md with Gemini. Instructor fix: split the prompt into smaller sections and generate README in two passes — first the module descriptions, then the setup instructions.

8. Students who generate viva_prep.md but do not read their own answers. They generate the file and move on without internalizing the content. Instructor fix: make every student read one of their own model answers out loud before the viva practice block.

9. Students who write module_summary.md in paragraph form instead of a table. The one-pager must be a scannable reference table, not an essay. Instructor fix: re-prompt with explicit instruction to use markdown table format with specific columns.

10. Students who cannot answer "What is the difference between RAG and fine-tuning?" This is a guaranteed interview question for AI engineering roles. If students skip Session 8 prep, they often cannot answer this clearly. Instructor fix: use this as a warm-up question at minute 10.

## How to Control the Session

This session has no live coding, which means students can drift into passive listening. Use the following control techniques: after every generated file, ask 2 students to read one section out loud and explain it; use the 30-second module explanation framework as a recurring check — ask any student at any point to give a 30-second explanation of any module; enforce the viva practice block strictly — do not skip it even if documentation generation runs long; keep the timer visible for the demo script practice.

---

# Questions to Discuss: Interview Perspective

## Basic Module Questions

### Q1. What is the AI Systems Interview Portfolio you built, and what does it demonstrate?

Expected answer:

The portfolio is a collection of seven standalone Python modules, each demonstrating a different AI engineering skill. The modules cover structured LLM output, LLM logging and evaluation, serverless-style AI function design, RAG pipeline construction using ChromaDB and sentence-transformers, RAG evaluation using automated scoring, agent-based intent routing, and vision/OCR with multimodal LLM input. Together they demonstrate practical fluency with the Google Gemini 1.5 Flash API via the google-generativeai library, local embedding generation with sentence-transformers all-MiniLM-L6-v2, persistent vector storage with ChromaDB, and Python-based LLMOps patterns. The portfolio is designed to be explainable in an interview without requiring a running server or cloud deployment.

### Q2. Why did you use Gemini 1.5 Flash instead of GPT-4o or Claude for this portfolio?

Expected answer:

Gemini 1.5 Flash was chosen primarily because its free tier on Google AI Studio provides sufficient API access for a portfolio-scale project without requiring a paid subscription. Its context window of 1 million tokens is significantly larger than GPT-3.5-turbo's 16K window, which matters for the RAG pipeline module where retrieved chunks are appended to the prompt. The google-generativeai Python library has a straightforward interface: model instantiation with genai.GenerativeModel, and generation via model.generate_content(). Structured output is handled by passing response_mime_type="application/json" in generation_config, which avoids the need for manual JSON parsing heuristics. In production, the choice of LLM would depend on task-specific benchmarks, cost per token, latency SLAs, and data residency requirements.

### Q3. How does the RAG pipeline in Session 4 connect to the RAG evaluator in Session 5?

Expected answer:

Session 4 builds a RAG pipeline in rag_pipeline.py that chunks input documents, generates 384-dimensional embeddings using sentence-transformers all-MiniLM-L6-v2, and stores them in a local ChromaDB collection. Session 5 builds rag_evaluator.py, which reads from the same ChromaDB collection created in Session 4. The evaluator runs a set of test queries through the retrieval and generation pipeline, then scores each response on faithfulness (does the answer align with the retrieved chunks?), relevance (does the answer address the query?), and completeness. The scores are written to rag_eval_report.csv and a before/after comparison is produced showing the effect of prompt modifications on response quality. This architectural dependency means Session 4 must be run before Session 5, and the ChromaDB collection path must be consistent between both scripts.

### Q4. What is the purpose of the LLM logger in Session 2, and what does it store?

Expected answer:

The LLM logger in llm_logger.py provides an observability layer for Gemini API calls. Every call to Gemini 1.5 Flash is wrapped in a logging function that records: the timestamp, the input prompt, the response text, the latency in milliseconds, a relevance score, and a quality flag. This data is appended to llm_logs.csv as a running log. After a set of calls, eval_summary.json is generated containing aggregate statistics: average latency, average relevance score, pass rate, and total calls logged. In an LLMOps context, this pattern mirrors production monitoring tools like LangSmith, PromptLayer, or Weights & Biases prompts tracking. The key limitation in this portfolio implementation is that scoring is heuristic-based rather than grounded in human annotation or a reference answer set.

### Q5. What does the agent router in Session 6 do, and how does it decide which tool to call?

Expected answer:

The agent router in agent_router.py takes a natural language query as input and classifies it into one of several intent categories such as summarization, question answering, calculation, or data extraction. This classification is done by sending the query to Gemini 1.5 Flash with a structured prompt that specifies the list of available intents and asks for a JSON response containing the matched intent and confidence score. Based on the returned intent, the router dispatches the query to the appropriate handler function. The output for each test query is printed in the format: query → intent → tool → result. This pattern demonstrates single-agent routing with LLM-based intent detection, which is a common architectural component in production AI systems that need to handle diverse user requests without hardcoded rule matching.

## Technical Deep-Dive Questions

### Q6. What chunking strategy does the RAG pipeline use, and what are its trade-offs?

Expected answer:

The RAG pipeline in rag_pipeline.py uses fixed-size character chunking with a configurable chunk_size parameter, typically set to 500 characters with a 50-character overlap. This approach is simple to implement and predictable in its behavior — every chunk is approximately the same length, which makes embedding dimensions and retrieval behavior consistent. The trade-off is that fixed-size chunking can split sentences or paragraphs mid-thought, which degrades the semantic coherence of each chunk and therefore reduces retrieval precision. A production improvement would be to use sentence-boundary-aware chunking using spaCy or NLTK sentence tokenizers, or to use semantic chunking where chunk boundaries are determined by embedding similarity drops rather than character counts. The overlap parameter helps mitigate boundary issues by ensuring that context from the end of one chunk is included at the start of the next.

### Q7. What is response_mime_type="application/json" in Gemini's generation_config, and why is it used?

Expected answer:

In the google-generativeai library, the generation_config parameter of model.generate_content() accepts a dictionary that controls output format. Setting response_mime_type="application/json" instructs Gemini 1.5 Flash to return its response as a JSON-formatted string rather than plain prose. This is used in Session 1's structured_output_engine.py and Session 6's agent_router.py to ensure that the LLM output can be directly parsed with json.loads() without needing regex or string manipulation heuristics. The practical benefit is that downstream code can reliably access fields like response["intent"] or response["confidence"] without defensive parsing. The risk is that even with this setting, Gemini can occasionally return malformed JSON if the prompt is ambiguous or the schema is not clearly specified, so the code should still wrap json.loads() in a try/except block and handle parsing failures gracefully.

### Q8. Why was sentence-transformers all-MiniLM-L6-v2 chosen for embeddings, and what are its limitations?

Expected answer:

all-MiniLM-L6-v2 was chosen for three practical reasons: it runs entirely locally with no API key or network dependency, it produces compact 384-dimensional vectors that are fast to compute and store, and it performs well on semantic similarity tasks for English text, making it suitable for document retrieval. The SentenceTransformer("all-MiniLM-L6-v2") constructor downloads the model on first run and caches it locally. The encode() method returns numpy arrays that ChromaDB accepts directly as embeddings. Limitations include: it was trained on general English text and may underperform on highly technical or domain-specific corpora (e.g., medical, legal, code); at 384 dimensions, it has lower representational capacity than larger models like all-mpnet-base-v2 (768 dimensions) or OpenAI text-embedding-3-large (3072 dimensions); and it does not support multilingual text without switching to a multilingual model variant.

### Q9. How does the vision/OCR module in Session 7 pass image data to Gemini 1.5 Flash?

Expected answer:

In vision_ocr_module.py, the image is loaded from disk using the PIL library (Pillow), and then passed directly to Gemini 1.5 Flash as part of a multimodal content list. The google-generativeai library supports multimodal inputs by accepting a list as the contents argument to model.generate_content(), where each element can be either a string (text) or a PIL Image object. The prompt includes an instruction to extract text from the image and return it as structured JSON. Gemini 1.5 Flash is a natively multimodal model, meaning it processes the image and text prompt jointly in a single forward pass without requiring a separate OCR pre-processing step. The output is written to ocr_output.json with fields for extracted text, confidence commentary, and any detected structure such as tables or headings. A limitation is that the accuracy of text extraction depends on image quality and resolution, and Gemini may silently misread low-contrast or stylized fonts.

### Q10. How does the serverless-style AI function in Session 3 simulate a serverless execution model in plain Python?

Expected answer:

Session 3's ai_handler.py simulates a serverless function pattern by structuring the code as a single handler function that accepts an event dictionary (analogous to an AWS Lambda event payload), processes the AI request, and returns a response dictionary (analogous to an HTTP response). The function loads its Gemini API key from a .env file using python-dotenv, calls Gemini 1.5 Flash, and returns a structured dict with fields for status, response_text, and latency_ms. This mirrors the interface contract of a real serverless function without requiring actual cloud infrastructure. The .env.example file documents required environment variables. In a real deployment, this handler could be wrapped with a cloud provider's function framework (AWS Lambda handler, Google Cloud Functions entry point) with minimal changes. The module demonstrates environment variable management, structured response contracts, and stateless function design — all critical patterns for production AI microservices.

## Production and System Design Questions

### Q11. If you were to deploy the RAG pipeline to serve 1000 users per day, what would you change?

Expected answer:

The current rag_pipeline.py uses ChromaDB in local persistent mode, which does not support concurrent writes from multiple processes and has no built-in authentication or access control. For 1000 users per day, the first change would be to migrate the vector store to a managed service such as Pinecone, Weaviate, or ChromaDB's hosted offering, which provides horizontal scaling, concurrent read/write support, and persistent backups. The embedding generation step using sentence-transformers would be moved to a dedicated service or batch-processed offline, since running encode() synchronously in a request path adds 50–200ms of latency per query. The Gemini API calls would need rate limiting and retry logic to handle the free tier's 60 requests-per-minute limit or manage costs on the paid tier. Logging would be added to capture query patterns, failed retrievals, and response latencies for ongoing quality monitoring. A re-ranking step using a cross-encoder model would improve precision without requiring vector store changes.

### Q12. What are the hallucination risks in this portfolio, and how would you mitigate them in production?

Expected answer:

The primary hallucination risk is in the RAG pipeline (Session 4) when retrieved chunks are not relevant to the query. In this case, Gemini may generate a plausible-sounding answer that is not grounded in the retrieved context. The RAG evaluator (Session 5) partially addresses this by measuring faithfulness — whether the generated answer is supported by the retrieved chunks — but this evaluation is automated and imperfect. In production, mitigation strategies include: adding a relevance threshold check before the generation step so that Gemini is only called if the top retrieved chunk exceeds a minimum cosine similarity score; using citation generation so the LLM is forced to quote the source chunk in its answer; adding a guard prompt that instructs Gemini to say "I don't have enough information" if the retrieved context is insufficient; and implementing a human-in-the-loop review process for high-stakes outputs. The vision/OCR module (Session 7) has a separate hallucination risk where Gemini may invent characters in low-quality images — a confidence score threshold and a fallback to a dedicated OCR library like Tesseract would reduce this risk.

### Q13. How would you monitor the production performance of the LLM logger module built in Session 2?

Expected answer:

In production, llm_logger.py's CSV-based logging would be replaced with a structured logging pipeline. Each Gemini call would emit a structured JSON log event containing: request ID, user ID (anonymized), prompt hash, response latency, token count (input and output), relevance score, and error code if applicable. These logs would be streamed to a centralized logging service such as Google Cloud Logging, Datadog, or the ELK stack. Dashboards would track: p50/p95/p99 latency distribution, error rate by error type (429 rate limit, parsing failure, timeout), average relevance score over time, and token consumption rate for cost forecasting. Alerting thresholds would be set on: error rate above 5%, p99 latency above 10 seconds, and relevance score dropping below a defined quality floor. The eval_summary.json aggregation pattern from Session 2 would be replaced by a time-series aggregation query in the monitoring platform. The key production addition is per-user rate limiting and anomaly detection for unusual prompt patterns that might indicate prompt injection attempts.

### Q14. What is the difference between RAG and fine-tuning, and when would you use each approach?

Expected answer:

RAG (Retrieval-Augmented Generation) dynamically retrieves relevant documents at inference time and appends them to the LLM's context window before generating a response. It does not modify the LLM's weights. Fine-tuning modifies the LLM's weights by training on a task-specific dataset, embedding knowledge or behavioral patterns directly into the model parameters. RAG is appropriate when the knowledge base is large, frequently updated, or proprietary — because you can update the vector store without retraining. It is also preferable when you need source attribution (the model can cite the retrieved chunk). Fine-tuning is appropriate when you need the model to consistently follow a specific output format, adopt a particular style or tone, or perform a specialized task where few-shot prompting is insufficient. Fine-tuning has higher upfront cost (compute for training, curated dataset preparation) but lower inference cost since no retrieval step is needed. In this portfolio, Session 4 and 5 implement RAG rather than fine-tuning because the use case — question answering over a document — is well-served by retrieval, and fine-tuning Gemini 1.5 Flash would require access to the model's training API and a labeled dataset.

### Q15. If you had to add a safety layer to the agent router (Session 6), how would you implement it?

Expected answer:

A safety layer for agent_router.py would address two risk categories: prompt injection (a user crafting a query that overrides the router's intent classification) and unsafe tool dispatch (the router calling a destructive or sensitive tool without verification). For prompt injection, the safety layer would include a pre-processing step that scans the incoming query for patterns that attempt to override system instructions, such as "ignore the above" or "act as a different assistant." A secondary LLM call with a guard prompt could be used to classify the input as safe or potentially adversarial before routing. For unsafe tool dispatch, the router would implement a confirmation gate for any tool classified as write, delete, or external — requiring an explicit approval flag in the event payload. All routed calls would be logged with the original query, the classified intent, the dispatched tool, and the outcome. Rate limiting per user would prevent automated abuse of the routing system. In production, this safety layer would be implemented as a middleware wrapper around the handler function in ai_handler.py's serverless pattern, keeping the core routing logic clean and testable.

---

# Session 8 Completion Checklist

Students should verify all of the following by end of session:

- [ ] README.md exists and covers all 7 modules with a one-line description each
- [ ] README.md includes technology stack table (Gemini 1.5 Flash, sentence-transformers, ChromaDB)
- [ ] README.md includes Gemini API key setup instructions referencing aistudio.google.com
- [ ] README.md includes folder structure showing all 7 Python scripts and output files
- [ ] architecture_diagram.md contains a valid Mermaid diagram with all 7 modules as nodes
- [ ] architecture_diagram.md shows the Session 4 → Session 5 dependency on ChromaDB
- [ ] architecture_diagram.md distinguishes between Gemini API calls and local operations
- [ ] demo_script.md is approximately 300 words (2 minutes spoken at normal pace)
- [ ] demo_script.md mentions at least one production-awareness statement
- [ ] viva_prep.md contains exactly 15 Q&A pairs with technically specific answers
- [ ] module_summary.md is in table format with at least 6 columns
- [ ] limitations.md addresses all 7 modules individually with specific production failure modes
- [ ] Student can deliver demo_script.md verbally without reading from screen

---

# Instructor Backup Plan

## If Gemini Rate Limit Hits During README Generation

The README.md generation prompt is long and may trigger the free-tier rate limit (60 RPM or 1 million tokens per day). If this happens: split the prompt into two passes — first generate the module descriptions (Sessions 1–4), then generate Sessions 5–7 plus the setup section in a second call. Alternatively, have students write the README manually using a template the instructor shares on screen. The content of README.md is known information — students have already built all 7 modules and can fill a template from memory. Do not let a rate limit error consume more than 5 minutes.

## If a Student's Setup Is Incomplete

Some students may not have completed all 7 sessions. This is acceptable for Session 8. Their documentation files will reflect the modules they completed. For modules they did not complete, instruct them to document the intended design based on the session specifications. This is also good interview preparation — being able to describe a module you planned but did not finish is a realistic scenario ("I designed the RAG evaluator but ran out of time to complete the cross-encoder re-ranking step").

## If Viva Practice Runs Long

If the interview discussion section runs over time, prioritize the following five questions as the minimum viva set: Q3 (RAG Session 4–5 connection), Q6 (chunking trade-offs), Q8 (embedding model choice), Q14 (RAG vs fine-tuning), Q15 (safety layer design). These five cover the highest-frequency interview topics for AI engineering roles and represent the most impactful subset for student preparation.

## If Students Cannot Recall Module Details

Some students will struggle to answer viva questions about modules they built several sessions ago. Do not skip the viva because of this. Instead, give students 3 minutes to open their Python scripts from Sessions 1–7 and re-read the first 20 lines of each file (the imports, constants, and first function signature). After 3 minutes, close the files and run the viva. This is a realistic interview condition — candidates are expected to recall from memory, with brief review allowed during preparation time.

---

# Interview Vocabulary Reference

Use this section to ensure students are using the correct technical terms during viva practice. If a student uses an imprecise term, correct it with the precise equivalent.

## LLM and API Terms

| Student Says | Correct Term to Use |
|---|---|
| "the AI model" | Gemini 1.5 Flash or google-generativeai |
| "I called the API" | model.generate_content() with a prompt string |
| "it returns JSON" | response_mime_type="application/json" in generation_config |
| "it checks the context" | the context window (Gemini 1.5 Flash: 1 million tokens) |
| "it was slow" | latency; typical Gemini API call: 1–4 seconds |
| "it hit a limit" | 429 ResourceExhausted — free-tier rate limit: 60 RPM |
| "I parsed the output" | json.loads(response.text) |

## RAG and Embedding Terms

| Student Says | Correct Term to Use |
|---|---|
| "I split the document" | fixed-size character chunking with chunk_size=500 and overlap=50 |
| "I converted text to numbers" | generated embeddings using SentenceTransformer("all-MiniLM-L6-v2").encode() |
| "I stored the data" | ingested documents and embeddings into a ChromaDB collection using collection.add() |
| "I searched for relevant parts" | retrieved top-k chunks using collection.query(query_embeddings=..., n_results=3) |
| "the similarity score" | cosine similarity between query embedding and stored chunk embeddings |
| "the vector size" | 384-dimensional float vector (all-MiniLM-L6-v2 output dimension) |
| "the database folder" | local ChromaDB persistent store at ./chroma_db/ |

## Production and System Design Terms

| Student Says | Correct Term to Use |
|---|---|
| "if lots of people use it" | concurrent users; horizontal scaling |
| "it might give wrong answers" | hallucination risk; faithfulness score |
| "I would add error handling" | try/except with exponential backoff for 429 errors |
| "I would add monitoring" | structured logging with latency, token count, and error code per call |
| "I would use a better database" | migrate from local ChromaDB to a managed vector store (Pinecone, Weaviate) |
| "it costs money" | cost per call: ~$0.075 per 1M input tokens, ~$0.30 per 1M output tokens |
| "it could be attacked" | prompt injection risk; input sanitisation and guard prompt |

---

# Concept Map: How All 7 Modules Teach AI Engineering

This map helps instructors explain why each session exists and what professional skill it builds:

## Session 1: Structured Output Prompt Engine
**Professional skill built**: Prompt engineering for reliable downstream parsing. Any production AI system that passes LLM output to another system (database write, API call, UI render) needs structured output. This module teaches students to use generation_config parameters to enforce output format rather than hoping the LLM formats its response correctly.

## Session 2: LLM Logging and Evaluation Tracker
**Professional skill built**: LLMOps observability. No production AI system runs without logging. This module builds the habit of wrapping every Gemini call in a function that records what went in, what came out, how long it took, and whether the output was good. The CSV + JSON pattern is a simplified version of what tools like LangSmith and Helicone do.

## Session 3: Serverless-Style AI Function
**Professional skill built**: Stateless function design and environment variable management. Every cloud-deployed AI microservice follows the event-in / response-out pattern. This module teaches students to think about AI functions as deployable units, not just interactive scripts. The .env.example file teaches the professional practice of never hardcoding API keys.

## Session 4: Basic RAG Pipeline
**Professional skill built**: Vector search and augmented generation. RAG is the dominant architecture for knowledge-grounded AI applications. This module teaches the full pipeline: chunk, embed, store, retrieve, augment, generate. Students learn when ChromaDB's collection.add() is called (at ingestion) versus when collection.query() is called (at runtime), and why the order matters.

## Session 5: RAG Evaluation and Improvement
**Professional skill built**: Systematic quality measurement for AI outputs. Building a pipeline is not enough — you must measure whether it works. This module teaches students to quantify LLM output quality using faithfulness and relevance scores, to compare before/after changes, and to report results in a structured CSV. This is the LLMOps evaluation skill that most junior AI engineers lack.

## Session 6: Simple Agent Router
**Professional skill built**: LLM-based decision making and tool dispatch. The agent pattern — where an LLM decides which function to call based on a natural language input — is the foundation of agentic AI systems. This module demonstrates that you do not need a framework like LangGraph to build a working router; a structured Gemini call returning a JSON intent dict is sufficient for simple routing.

## Session 7: Vision/OCR Mini Module
**Professional skill built**: Multimodal input handling. As AI models become increasingly multimodal, engineers need to understand how to pass non-text inputs (images, PDFs, audio) to LLMs. This module teaches the PIL → Gemini multimodal content list pattern and demonstrates that image understanding and text extraction are now a single API call, not a multi-step OCR + NLP pipeline.

## Session 8: Final System Design and Interview Demo
**Professional skill built**: Technical communication and portfolio presentation. This is the hardest skill to teach because it is metacognitive — students must think about their own work from the outside. The documentation artifacts produced in this session are evidence that a student can do what senior engineers do: explain a system to someone who did not build it, admit its limitations, and propose production improvements.

---

# Quick-Reference: Expected Output Files After Session 8

By the end of Session 8, each student's portfolio folder should contain the following files. Use this as a visual checklist on screen during the final wrap-up:

```
ai-systems-portfolio/
├── structured_output_engine.py
├── output_examples.json
├── llm_logger.py
├── llm_logs.csv
├── eval_summary.json
├── ai_handler.py
├── .env.example
├── rag_pipeline.py
├── chroma_db/
│   └── (ChromaDB collection files)
├── rag_evaluator.py
├── rag_eval_report.csv
├── agent_router.py
├── vision_ocr_module.py
├── sample_image.png
├── ocr_output.json
├── README.md                    ← Session 8
├── architecture_diagram.md      ← Session 8
├── demo_script.md               ← Session 8
├── viva_prep.md                 ← Session 8
├── module_summary.md            ← Session 8
└── limitations.md               ← Session 8
```

Students who have this complete folder, can run every Python script without errors, and can deliver the demo_script.md verbally have completed the AI Systems Interview Portfolio.

---

# Instructor Self-Assessment: Session 8 Goals

Before ending the session, verify the following for the cohort as a group:

- At least 80% of students have all 6 documentation files generated and present in their folder
- At least one student delivered the demo script verbally in front of the group
- The viva practice block covered at least 5 of the 15 Q&A pairs
- The concept of RAG vs fine-tuning was explicitly discussed and at least one student articulated the distinction correctly
- The architecture diagram was traced out loud by at least one student showing all dependencies
- The 30-second module explanation framework was practised by at least 3 students on different modules
- Students left with a clear understanding that this portfolio is presentable to a hiring manager today

If any of these were not achieved, note them for follow-up. The most common gap is viva practice being skipped due to time pressure. If this happens, send the 15 Q&A pairs as a homework assignment and ask students to record a 2-minute video of themselves delivering the demo script before their next interview.
