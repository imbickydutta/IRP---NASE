# Cohort B QC Audit Report
## AI Support Ticket Resolution Copilot

**Total Sessions Audited:** 8
**Files per Session:** 3 (instructor, student pre-session, after-session)
**Total Files Audited:** 24

---

## Session 1: Build Core Backend — Ticket CRUD API
**Overall Status:** PASS WITH WARNINGS

**File Sizes:** Instructor: 605 lines | Student: 532 lines | After-Session: 314 lines

### Check Results
- ✅ **CHECK 1 — TIMING** (PASS): 10 blocks sum to exactly 120 minutes (0-10, 10-20, 20-35, 35-50, 50-65, 65-80, 80-95, 95-105, 105-115, 115-120), within the 110-120 minute target.
- ✅ **CHECK 2 — HANDS-ON** (PASS): AI-assisted build demo starts at minute 20 (block: '20-35 min: Build the Feature Using Claude Code or Cursor'), well before the 35-minute mark.
- ✅ **CHECK 3 — PROMPTS** (PASS): Student file has 9 text blocks total and 7 numbered prompts. Main Build Prompt (Prompt 1) is ~50 lines, highly specific with file structure, field definitions, endpoint specs, and negative constraints.
- ⚠️ **CHECK 4 — SCOPE COMPLIANCE** (WARN): Session 1 intentionally excludes SQLModel, Alembic, and PostgreSQL (those are Session 2); content is correctly scoped to in-memory FastAPI REST API. No forbidden topics (frontend, React, payment, email, file upload, Docker, CI/CD) appear in core content — Docker and CI/CD appear only in Session 8 forward-reference diagrams.
- ✅ **CHECK 5 — INTERVIEW QUESTIONS** (PASS): Exactly 15 questions (Q1-Q15) present in instructor file. Every answer is 5-7 technical sentences covering Pydantic internals, HTTP semantics, FastAPI request lifecycle, and concurrency trade-offs.
- ✅ **CHECK 6 — CROSS-SESSION** (PASS): Previous session correctly flagged as 'Session 1 — no previous codebase, starting from empty directory.' Session 2 preview is detailed in both the 115-120 min wrap-up block and a dedicated 'Session 2 Preview' section in the after-session notes.
- ⚠️ **CHECK 7 — DELIVERABLE** (WARN): The QC-specified deliverable ('Running FastAPI skeleton with SQLModel, Alembic, PostgreSQL, folder structure') does not match what Session 1 actually delivers — Session 1 is deliberately in-memory only. The actual deliverable (FastAPI + Pydantic + in-memory storage + Swagger) IS clearly and consistently stated in all 3 files. The deliverable wording in the QC spec appears to belong to Session 2.
- ✅ **CHECK 8 — SESSION NOT DAY** (PASS): No instances of 'Day X' found across all three files. All references use 'Session 1', 'Session 2', etc. consistently.
- ✅ **CHECK 9 — COMPLETION CHECKLIST** (PASS): Instructor file contains 13 artifact-based checklist items (lines 580-593), all verifiable by running the server and testing Swagger — exceeds the 10-item minimum.
- ✅ **CHECK 10 — TECHNICAL DEPTH** (PASS): Code snippets present throughout: request flow diagram, Pydantic Literal validator, 422 JSON error body example, uvicorn command, full POST lifecycle walkthrough (11 numbered steps). Concepts explained at line-by-line coding level appropriate for Cohort B.
- ✅ **CHECK 11 — FILE SIZE** (PASS): Instructor: 605 lines (threshold 300 — PASS). Student: 532 lines (threshold 250 — PASS). After-session: 314 lines (threshold 180 — PASS). All three files exceed their minimum thresholds.

### Minor Issues
- CHECK 4 WARN: The QC scope definition lists 'FastAPI app factory, SQLModel, Alembic migrations, PostgreSQL' as in-scope for Session 1, but Session 1 is intentionally in-memory only — SQLModel/Alembic/PostgreSQL are correctly deferred to Session 2. The scope spec for this audit appears to describe Session 2 content, not Session 1.
- CHECK 7 WARN: The QC-expected deliverable phrase 'Running FastAPI skeleton with SQLModel, Alembic, PostgreSQL, folder structure' does not match Session 1's actual deliverable (in-memory REST API). This is a mismatch in the QC checklist specification, not in the session files themselves. All 3 files are internally consistent about what Session 1 delivers.

### Recommended Fixes
- Confirm whether the QC audit scope definition ('FastAPI app factory, SQLModel, Alembic, PostgreSQL') was intended for Session 2, not Session 1 — if so, update the QC spec to reflect Session 1's correct scope (FastAPI + Pydantic + in-memory storage + Swagger).
- Update the QC deliverable string for Session 1 to read 'Running FastAPI application with 5 CRUD endpoints, Pydantic validation, in-memory storage, and Swagger at /docs' to match what all 3 files actually describe.
- No changes required to the three session files themselves — they are internally consistent, well-structured, and meet all measurable thresholds.

---

## Session 2: Add Database Layer + Data Modeling
**Overall Status:** WARN — 1 FAIL (deliverable mismatch vs QC rubric), 1 WARN (scope rubric mismatch), 9 PASS. Content quality is strong; the FAIL is a rubric-alignment issue between the QC prompt's expected deliverable (Session 3 auth scope) and Session 2's actual, correct deliverable (database layer).

**File Sizes:** Instructor: 634 lines | Student: 561 lines | After-Session: 235 lines

### Check Results
- ✅ **CHECK 1 — TIMING** (PASS): 10 blocks total exactly 120 minutes: 0-10, 10-20, 20-35, 35-50, 50-65, 65-80, 80-95, 95-105, 105-115, 115-120 = 120 min, within the 110-120 window.
- ✅ **CHECK 2 — HANDS-ON** (PASS): Build activity ('Build the Feature Using Claude Code or Cursor') starts at minute 20, well before the 35-minute mark.
- ✅ **CHECK 3 — PROMPTS** (PASS): 7 prompts in ```text blocks (Prompts 1-7). Main build prompt (Prompt 1) is 57 lines and highly specific with exact file paths, field names, and ORM operation requirements.
- ⚠️ **CHECK 4 — SCOPE COMPLIANCE** (WARN): Session 2's own scope (SQLite + SQLModel database layer) is clean and well-controlled. However, the QC rubric scope (JWT, bcrypt, User model, /register /login /me, auth middleware) belongs to Session 3, not Session 2 — these files are correctly scoped to the database layer build.
- ✅ **CHECK 5 — INTERVIEW QUESTIONS** (PASS): Exactly 15 interview questions (Q1-Q15) with expected answers. All answers are 4-8 sentences, technically precise at mid-level backend engineer depth.
- ✅ **CHECK 6 — CROSS-SESSION** (PASS): Instructor file correctly references Session 1 (in-memory list state) and previews Session 3 (JWT auth, User table, login endpoint) in both the wrap-up block and after-session notes.
- ❌ **CHECK 7 — DELIVERABLE** (FAIL): Deliverable across all 3 files is 'SQLite database layer, SQLModel Ticket table, updated CRUD endpoints, data persistence' — NOT 'JWT auth, register/login endpoints, protected routes, auth middleware.' That is Session 3's deliverable. Session 2's deliverable is correctly the database layer, but it does not match the QC rubric's expected deliverable string.
- ✅ **CHECK 8 — SESSION NOT DAY** (PASS): No instances of 'Day X' found in any of the 3 files. All references use 'Session X' consistently throughout.
- ✅ **CHECK 9 — COMPLETION CHECKLIST** (PASS): Instructor file has a 12-item completion checklist (lines 609-622), all artifact-based and verifiable (pip install, table=True, engine config, get_session, all 5 endpoints, swagger tests, server restart persistence check).
- ✅ **CHECK 10 — TECHNICAL DEPTH** (PASS): Multiple inline code snippets across all 3 files covering Ticket model, database.py, endpoint patterns, select() queries, and error handling. Explanations target mid-level Python backend engineer and use correct SQLAlchemy/Pydantic terminology throughout.
- ✅ **CHECK 11 — FILE SIZE** (PASS): Instructor: 634 lines (threshold 300, PASS). Student: 561 lines (threshold 250, PASS). After-session: 235 lines (threshold 180, PASS).

### Critical Issues
- CHECK 7 FAIL: The QC rubric specifies the deliverable as 'JWT auth, register/login endpoints, protected routes, auth middleware' — but all 3 Session 2 files correctly define the deliverable as the SQLite/SQLModel database layer. Either the QC rubric was written for Session 3 and applied to Session 2 by mistake, or the session numbering is off by one. Confirm whether this QC audit was intended for Session 3 (JWT auth) or Session 2 (database layer). If the intent was Session 3, these files need to be reviewed against the correct session.

### Minor Issues
- CHECK 4 WARN: The QC scope rubric (JWT, bcrypt, python-jose, /register /login /me, auth middleware, OAuth exclusions, refresh tokens, 2FA) is entirely Session 3 content. Session 2's own scope control is well-executed and tightly enforced. The rubric should be updated to reference Session 2's actual scope for accurate QC.
- After-session file (235 lines) passes the 180-line threshold but is the thinnest of the three files — the section on 'What Students Should Understand' is a list of 10 points without the depth of the instructor file. Consider expanding the technical deep-dive section.
- The after-session file previews Session 3 as including 'role-based guard: only admins can delete tickets' and 'OAuth2PasswordBearer' — but the QC rubric for Session 3 scope lists OAuth as excluded. Verify the Session 3 scope definition is consistent across the after-session preview and the Session 3 files.

### Recommended Fixes
- Confirm whether this QC audit rubric (JWT auth deliverable) was meant for Session 3. If yes, re-run the audit against the Session 3 files. If Session 2 is correct as the database layer, update the QC rubric's deliverable string for Session 2 to read: 'SQLModel Ticket table, SQLite engine, get_session dependency, all 5 CRUD endpoints persisting to tickets.db, verified data persistence across server restarts.'
- Add 'OAuth2PasswordBearer' scope consistency check to Session 3 QC audit — the after-session file preview mentions it, but the QC rubric for Session 3 lists OAuth as excluded. These may conflict.
- Consider adding ~20-30 lines to the after-session file's technical deep-dive to bring it further above the 180-line floor with more margin.

---

## Session 3: Add Auth + Role-Based Access
**Overall Status:** WARN — 2 FAIL checks on scope/deliverable mismatch against audit spec; all structural and content-quality checks pass

**File Sizes:** Instructor: 565 lines | Student: 511 lines | After-Session: 292 lines

### Check Results
- ✅ **CHECK 1 — TIMING** (PASS): 10 blocks total exactly 120 min: 0-10, 10-20, 20-35, 35-50, 50-65, 65-80, 80-95, 95-105, 105-115, 115-120. Squarely within 110-120 min window.
- ✅ **CHECK 2 — HANDS-ON** (PASS): Build activity (AI code generation via main prompt) starts at the 20-minute mark — 15 minutes before the 35-min deadline.
- ✅ **CHECK 3 — PROMPTS** (PASS): 7 prompts in text blocks (Prompts 1-7). Main build prompt (Prompt 1) is 73 lines, highly specific with exact file structure, constraints, and library pinning.
- ❌ **CHECK 4 — SCOPE COMPLIANCE** (FAIL): Session 3 content is JWT auth and RBAC — correct for a progression build. However, the audit spec scope (Ticket status enum, full CRUD, pagination, Pydantic validation) is Session 2 content, not Session 3. These files contain the wrong scope relative to the QC spec, OR the QC spec is using the wrong session number for this content.
- ✅ **CHECK 5 — INTERVIEW QUESTIONS** (PASS): Exactly 15 questions (Q1-Q15) with full expected answers. Answers are 4-7 sentences each and technically precise: JWT structure, bcrypt mechanics, 401 vs 403, Depends() chain, scale trade-offs.
- ✅ **CHECK 6 — CROSS-SESSION** (PASS): Instructor file correctly references Session 2 (SQLModel/SQLite state) in opening recap and 'Codebase State After Session 2' block; previews Session 4 (LLM Ticket Classifier) in the 115-120 min wrap-up and after-session notes.
- ❌ **CHECK 7 — DELIVERABLE** (FAIL): Deliverable across all 3 files is 'JWT auth layer, User SQLModel table, bcrypt password hashing, get_current_user dependency, RBAC' — NOT 'Full Ticket CRUD, SQLModel models, ticket status enum, pagination' as required by the audit spec. This is a session numbering/scope mismatch issue.
- ✅ **CHECK 8 — SESSION NOT DAY** (PASS): No instances of 'Day X' found in any of the three files. All references correctly use 'Session X' throughout.
- ✅ **CHECK 9 — COMPLETION CHECKLIST** (PASS): Instructor file has 12-item completion checklist (lines 541-552), all artifact-based: specific HTTP status codes, Swagger test outcomes, and one verbal explanation item.
- ✅ **CHECK 10 — TECHNICAL DEPTH** (PASS): All 3 files contain code snippets (file trees, Python function signatures, SQLModel select().where() patterns, JWT flow diagrams, pytest stubs with dependency_overrides). Concepts explained at implementation level with exact exception types and method calls.
- ✅ **CHECK 11 — FILE SIZE** (PASS): Instructor: 565 lines (threshold 300). Student: 511 lines (threshold 250). After-session: 292 lines (threshold 180). All three exceed their minimums comfortably.

### Critical Issues
- SCOPE MISMATCH (Check 4 + Check 7): The QC audit spec defines Session 3 scope as 'Ticket model with status enum, full CRUD endpoints, pagination with offset/limit, input validation with Pydantic' and expects the deliverable to be 'Full Ticket CRUD, SQLModel models, ticket status enum, pagination.' The actual Session 3 files cover JWT authentication and role-based access control — which is coherent internal content but does NOT match the scope defined in this audit task. Either (a) the audit spec is using Session 2 scope requirements against Session 3 files by mistake, or (b) the session files are mislabeled and Session 3 should be the CRUD/pagination session while the auth content belongs to a different session number. This must be resolved before cohort delivery.
- DELIVERABLE STATEMENT MISMATCH: None of the 3 files state 'Full Ticket CRUD, SQLModel models, ticket status enum, pagination' as the deliverable — all 3 files are internally consistent on auth as the deliverable, which conflicts with the audit spec requirement for Check 7.

### Minor Issues
- After-session notes do not include a standalone completion checklist — they have a 'What Students Should Understand' section with 10 conceptual items but no artifact-based checklist matching the instructor file format. Recommend adding a mirror checklist for student self-assessment.
- Student file has 7 prompts (Prompts 1-7) but the session flow only explicitly directs students to use 'Prompt 1' and 'Prompt 2' during class. Prompts 3-7 have no explicit call-out in the instructor flow indicating when to use them. Recommend adding timing references for Prompts 3-7 in the instructor notes.
- Completion checklist item 12 ('Student can explain the difference between 401 and 403 responses without looking at notes') is a verbal/behavioral item, not an artifact. All 11 preceding items are measurable artifacts. This is a minor inconsistency.
- The after-session notes use PATCH notation in places (e.g., 'PATCH /tickets/{id} requires Depends(require_admin)') — verify PATCH is the correct HTTP verb for status updates across the whole series for consistency.

### Recommended Fixes
- CRITICAL: Clarify whether the QC audit spec scope definition (CRUD/pagination/status enum) belongs to Session 2 and was accidentally applied to Session 3 in this audit task. If so, rerun the audit with the correct scope for Session 3 (JWT auth, RBAC). If the content in these files is misassigned, renumber or restructure the session sequence.
- Add a student-facing completion checklist to the after-session notes that mirrors the 12-item instructor checklist — students need a self-assessment tool after class.
- In the instructor session flow, add inline references to when Prompts 3-7 (debugging, explanation, interview prep, test generation, edge case) should be used — either during the 65-80 min Swagger testing block or as take-home assignments.
- Consider adding an explicit 'Assessment Gate' note in the instructor file between the 65-80 min block and the 80-95 min block — instructors should confirm all students have a working JWT flow before moving to error hardening.

---

## Session 4: Add LLM Ticket Classifier
**Overall Status:** PASS with one criteria mismatch and one scope-labeling issue to note

**File Sizes:** Instructor: 672 lines | Student: 652 lines | After-Session: 288 lines

### Check Results
- ✅ **CHECK 1 — TIMING** (PASS): 10 blocks total to 120 min: 0-10, 10-20, 20-35, 35-50, 50-65, 65-80, 80-95, 95-105, 105-115, 115-120. Total = 120 min, within the 110-120 min window.
- ✅ **CHECK 2 — HANDS-ON** (PASS): Build activity starts at the 20-minute mark ('20–35 min: Build the Feature Using Claude Code or Cursor AI'), which is well before the 35-minute deadline.
- ✅ **CHECK 3 — PROMPTS** (PASS): 7 numbered prompts in ```text blocks (Prompts 1-7) plus 2 additional text blocks; Prompt 1 (main build) is 73 lines and highly specific — well above the 15-line minimum.
- ⚠️ **CHECK 4 — SCOPE COMPLIANCE** (WARN): The check criteria describes Session 5 scope (ChromaDB, sentence-transformers, /search endpoint). Session 4 correctly covers its own scope (LLM classification, JSON mode, TicketClassification table) with no RAG/ChromaDB bleed-in. The mismatch is in the check criteria, not the content.
- ✅ **CHECK 5 — INTERVIEW QUESTIONS** (PASS): Exactly 15 questions (Q1-Q5 Basic, Q6-Q10 Technical Deep-Dive, Q11-Q15 System Design). All answers are 3-5+ sentences with technical depth including code examples (e.g., Q9 has a full pytest mock snippet).
- ✅ **CHECK 6 — CROSS-SESSION** (PASS): Instructor file explicitly recaps Session 3 (JWT auth, RBAC, codebase state) and previews Session 5 (RAG Knowledge Base, ChromaDB, embeddings, cosine similarity) with actionable prep steps.
- ❌ **CHECK 7 — DELIVERABLE** (FAIL): The check asks for 'ChromaDB collection, ingestion script, semantic search /search endpoint' — that is the Session 5 deliverable, not Session 4. Session 4's actual deliverable (TicketClassification table, llm_classifier.py, updated POST /tickets with classification) is clearly stated in all 3 files. The check criteria targets the wrong session.
- ✅ **CHECK 8 — SESSION NOT DAY** (PASS): No instances of 'Day X' found in any of the three files. All temporal references use 'Session X' consistently throughout.
- ✅ **CHECK 9 — COMPLETION CHECKLIST** (PASS): Instructor file contains a 12-item 'Session 4 Completion Checklist' (lines 648-661) with all artifact-based items: file existence, API parameter verification, Swagger tests, DB row verification, pytest pass, and explanation readiness.
- ✅ **CHECK 10 — TECHNICAL DEPTH** (PASS): Multiple code snippets at coding level: OpenAI client instantiation, chat.completions.create call signature, SQLModel FK definition, try/except with specific openai exception types, full pytest mock example, sql query. Concepts explained with exact parameter names and library methods.
- ✅ **CHECK 11 — FILE SIZE** (PASS): Instructor: 672 lines (threshold ≥300 — PASS). Student: 652 lines (threshold ≥250 — PASS). After-session: 288 lines (threshold ≥180 — PASS). All three files comfortably exceed their minimums.

### Critical Issues
- CHECK 7 criteria mismatch: The deliverable check asks for 'ChromaDB collection, ingestion script, semantic search /search endpoint' which is the Session 5 deliverable. Session 4's deliverable (TicketClassification table, llm_classifier.py service, updated POST /tickets endpoint with classification) is correctly and clearly stated in all 3 files. This is an error in the QC check criteria, not in the session content.
- CHECK 4 scope criteria mismatch: The in-scope/excluded items listed in the check (ChromaDB, sentence-transformers, /search endpoint, hybrid search, re-ranking, PDF parsing, multiple collections) describe Session 5 RAG scope, not Session 4 LLM classifier scope. Session 4 content is correctly scoped to its own topic and does not bleed into Session 5 territory.

### Minor Issues
- The after-session notes file (288 lines) is the thinnest of the three files — it passes the 180-line minimum but has less instructor reflection content compared to the depth of the instructor and student files. Consider adding a 'What worked well / What to adjust next time' section.
- The student file's 'Content to Prepare Before Class' section (lines 340-361) uses a ```text block to describe a preparation task rather than an actual prompt for an AI coding tool. This is functionally fine but is inconsistent with the prompt labeling convention used for Prompts 1-7.
- Prompt 3 (Debugging Prompt) presents three separate symptoms in one block. If a student pastes the full prompt, the AI coding tool receives all three symptoms simultaneously. Consider splitting into three targeted debugging prompts or clearly instructing students to delete inapplicable symptoms before pasting.

### Recommended Fixes
- Fix the QC audit criteria for CHECK 7 to match Session 4's actual deliverable: 'TicketClassification SQLModel table, llm_classifier.py service module, updated POST /tickets endpoint returning classification fields'.
- Fix the QC audit criteria for CHECK 4 to reflect Session 4's actual scope boundaries: include OpenAI Chat Completions API, JSON mode, temperature settings, TicketClassification table, graceful degradation; exclude LangChain, RAG/ChromaDB, async LLM calls, streaming, multiple providers.
- Add a 'Reflection' section to the after-session notes covering what typically goes well and what to adjust — this makes the document more useful for re-running the session.
- Add a note to Prompt 3 instructing students to delete the non-applicable SYMPTOM blocks before pasting to avoid confusing the AI coding tool with multiple simultaneous problem descriptions.

---

## Session 5: Add RAG Knowledge Base: Embeddings, Vector Storage, and Grounded Response Suggestions
**Overall Status:** WARN — Session 5 content is high quality and internally consistent, but the QC audit scope definition and expected deliverable do not match Session 5; they describe Session 6. Two checks FAIL due to this mismatch. One WARN for student hands-on starting at minute 50 instead of by minute 35.

**File Sizes:** Instructor: 491 lines | Student: 558 lines | After-Session: 295 lines

### Check Results
- ✅ **CHECK 1 — TIMING** (PASS): 10 blocks total: 0–10, 10–20, 20–35, 35–50, 50–65, 65–80, 80–95, 95–105, 105–115, 115–120 = exactly 120 minutes, within the 110–120 min window.
- ⚠️ **CHECK 2 — HANDS-ON** (WARN): The 20–35 min block is an instructor-led AI demo, not student hands-on. Student Follow-Along Build starts at 50 min, which is 15 minutes past the 35-minute threshold.
- ✅ **CHECK 3 — PROMPTS** (PASS): 7 prompts in text blocks (Prompt 1 through Prompt 7). Prompt 1 is 67 lines, highly specific with exact file names, function signatures, constraints, and scope — well above the 15-line minimum.
- ❌ **CHECK 4 — SCOPE COMPLIANCE** (FAIL): The QC audit scope definition (LangGraph StateGraph, 4 nodes, conditional routing, /resolve endpoint) is Session 6 content. Session 5 covers RAG/ChromaDB/OpenAI embeddings only, and explicitly excludes LangGraph ('those come in Session 6'). The /resolve endpoint does not appear anywhere; the endpoint is /tickets/{id}/suggested-response.
- ✅ **CHECK 5 — INTERVIEW QUESTIONS** (PASS): Exactly 15 questions (Q1–Q15). All answers are 4–6 sentences and technically precise, covering API call details, parameter names, trade-offs, and production considerations.
- ✅ **CHECK 6 — CROSS-SESSION** (PASS): Instructor file opens with explicit Session 4 codebase recap (0–10 min block lists all files from previous sessions). Session 6 preview is a dedicated 115–120 min block naming LangGraph, StateGraph, Classify/Retrieve/Generate/Review nodes, and conditional edges. After-session file also includes a full Session 6 Preview section.
- ❌ **CHECK 7 — DELIVERABLE** (FAIL): The QC-expected deliverable 'LangGraph resolution workflow: classify → retrieve → respond → escalate nodes' is Session 6 content and does not appear in any file. All 3 files consistently state Session 5's actual deliverable: GET /tickets/{id}/suggested-response returning ticket_id, suggested_response, and sources. The deliverable IS consistent across files but does not match the QC specification.
- ✅ **CHECK 8 — SESSION NOT DAY** (PASS): No instances of 'Day X' found in any of the three files. All temporal references use 'Session X' consistently.
- ✅ **CHECK 9 — COMPLETION CHECKLIST** (PASS): Instructor file has a 'Session 5 Completion Checklist' with 12 artifact-based items covering: file creation, ChromaDB setup, startup log, disk persistence, HTTP 200/404/401 responses, retrieval quality, sources field, regression tests, and verbal explanation.
- ✅ **CHECK 10 — TECHNICAL DEPTH** (PASS): Code snippets and API patterns throughout all 3 files: OpenAI embeddings.create with response.data[0].embedding, ChromaDB PersistentClient, collection.upsert/query parameter names, FastAPI lifespan pattern, Pydantic SuggestedResponseOut model, pytest mocking patterns. Concepts explained with correct terminology (cosine similarity formula, 1536-dimensional vectors, upsert idempotency, parametric vs retrieved memory).
- ✅ **CHECK 11 — FILE SIZE** (PASS): Instructor: 491 lines (required ≥300). Student: 558 lines (required ≥250). After-session: 295 lines (required ≥180). All three files exceed their minimums.

### Critical Issues
- CHECK 4 SCOPE MISMATCH: The QC audit scope definition references LangGraph StateGraph, 4 nodes as Python functions, conditional routing, session state, and a /resolve endpoint — all of which are Session 6 content. Session 5 is scoped to raw RAG mechanics (embeddings, ChromaDB, OpenAI text-embedding-3-small) and correctly excludes LangGraph. Either the QC audit scope was copied from Session 6 by mistake, or this session needs to be re-labeled.
- CHECK 7 DELIVERABLE MISMATCH: The expected deliverable 'LangGraph resolution workflow: classify → retrieve → respond → escalate nodes' does not exist in any Session 5 file. All three files state the correct Session 5 deliverable (GET /tickets/{id}/suggested-response). If Session 5 is supposed to cover LangGraph, the files need a complete rewrite; if Session 6 covers LangGraph, the QC spec for this check is wrong.

### Minor Issues
- CHECK 2 HANDS-ON TIMING: Student hands-on build begins at minute 50, not by minute 35 as required. The 20–35 min block is an instructor-only AI demo. Consider converting part of the 20–35 min demo into a student parallel activity, or restructuring so the student build prompt is used by both instructor and students simultaneously starting at minute 20.
- After-session file (295 lines) clears the 180-line minimum but is noticeably shorter than the other two files; it could be expanded with a self-assessment quiz or a richer 'what went wrong and why' section.
- The instructor file's Completion Checklist item 12 is a verbal/oral check ('Student can verbally explain...') rather than an artifact — technically breaks the artifact-based requirement, though 11 of 12 are artifact-based so overall the checklist passes.

### Recommended Fixes
- Clarify whether Session 5 or Session 6 is supposed to cover LangGraph. If Session 6 = LangGraph, update the QC audit template for Session 5 to use the correct scope (RAG/ChromaDB/embeddings) and correct deliverable (GET /tickets/{id}/suggested-response). If Session 5 is supposed to cover LangGraph, the three files need to be fully rewritten.
- Move the student hands-on build earlier: restructure the 20–35 min block so students paste Prompt 1 simultaneously with the instructor demo (parallel activity), making minute 20 the effective start of student hands-on rather than minute 50.
- Add a student self-assessment or reflection table to the after-session file to increase its depth and bring it further above the 180-line minimum.
- Replace or supplement Completion Checklist item 12 with an artifact-based equivalent (e.g., 'Student has written a 2–3 sentence explanation of RAG in their notes document') to make it fully artifact-verifiable.

---

## Session 6: Add LangGraph Agentic Workflow
**Overall Status:** FAIL — 2 critical checks failed (scope compliance and deliverable mismatch); all structural, size, timing, prompt count, and quality checks pass.

**File Sizes:** Instructor: 589 lines | Student: 546 lines | After-Session: 260 lines

### Check Results
- ✅ **CHECK 1 — TIMING** (PASS): 10 blocks total 120 minutes exactly: 0-10 recap, 10-20 architecture, 20-35 build, 35-50 walkthrough, 50-65 student build, 65-80 test/improve, 80-95 error handling, 95-105 concept pause, 105-115 interview viva, 115-120 wrap-up.
- ✅ **CHECK 2 — HANDS-ON** (PASS): Build activity (Prompt 1 run live with Claude Code/Cursor AI) starts at the 20-minute mark, well within the 35-minute requirement.
- ✅ **CHECK 3 — PROMPTS** (PASS): 7 named prompts in ```text blocks (Prompts 1-7) plus a final explanation block; main build Prompt 1 is ~80 lines and fully specific with constraints, node specs, and file targets.
- ❌ **CHECK 4 — SCOPE COMPLIANCE** (FAIL): This session covers LangGraph StateGraph/agentic workflow — correct for Session 6 of the build series — but the QC audit scope specifies eval JSON schema, Gemini/OpenAI-as-judge, 5 test tickets, quality score, and /eval/run endpoint, which are Session 7 topics. The session contains zero content on those items. Either the audit scope definition is mismatched to this session number, or this file covers the wrong topic.
- ✅ **CHECK 5 — INTERVIEW QUESTIONS** (PASS): Exactly 15 interview questions (Q1-Q15) with expected answers averaging 5-7 technically precise sentences each, covering basic, deep-dive, and system-design/trade-off tiers.
- ✅ **CHECK 6 — CROSS-SESSION** (PASS): Instructor file correctly references Session 4 (classify_ticket), Session 5 (retrieve_docs, generate_response, POST /tickets/{id}/suggest) and previews Session 7 (evals, guardrails, pytest, LLM-as-judge) in the wrap-up and after-session notes.
- ❌ **CHECK 7 — DELIVERABLE** (FAIL): Deliverable across all 3 files is 'LangGraph StateGraph with POST /tickets/{id}/resolve' — the QC audit requires 'LLM-as-judge eval, resolution quality scoring, eval dashboard /eval endpoint', which is absent. Deliverable is consistent across all 3 files internally but does not match the prescribed QC deliverable definition.
- ✅ **CHECK 8 — SESSION NOT DAY** (PASS): No instances of 'Day X' found in any of the three files; all temporal references use 'Session X' consistently throughout.
- ✅ **CHECK 9 — COMPLETION CHECKLIST** (PASS): Instructor file has a 13-item artifact-based completion checklist covering langgraph install, TicketState definition, all four nodes, graph assembly, endpoint existence, Swagger 200/404 tests, and state-tracing ability.
- ✅ **CHECK 10 — TECHNICAL DEPTH** (PASS): Extensive code-level content: LangGraph API patterns (StateGraph, add_node, add_edge, add_conditional_edges, compile), TypedDict definitions, node function signatures, JSON response samples, pytest mocking patterns, 8 common error messages with root-cause analysis and fixes — all appropriate for Cohort B coding level.
- ✅ **CHECK 11 — FILE SIZE** (PASS): Instructor: 589 lines (threshold >=300, PASS). Student: 546 lines (threshold >=250, PASS). After-session: 260 lines (threshold >=180, PASS).

### Critical Issues
- SCOPE MISMATCH: The QC audit scope specifies 'Evaluation JSON schema, Gemini/OpenAI as judge, 5 test tickets, quality score, /eval/run endpoint' — this is Session 7 content. Session 6 files cover LangGraph StateGraph agentic workflow (correct for Session 6 of the build series but a mismatch against the audit scope definition provided). Either the audit scope block was written for Session 7 and mistakenly used for Session 6, or the session number in these files is incorrect.
- DELIVERABLE MISMATCH: The QC deliverable definition states 'LLM-as-judge eval, resolution quality scoring, eval dashboard /eval endpoint'. The actual deliverable in all 3 files is 'LangGraph StateGraph with TicketState TypedDict, 4 nodes, POST /tickets/{id}/resolve'. There is zero content on LLM-as-judge eval or /eval/run in these Session 6 files.

### Minor Issues
- The session title in the QC prompt placeholder reads '+ title +' (unfilled template variable) — not an issue in the files themselves, but the orchestration script may have a templating bug.
- Prompt 7 is referenced in the 80-95 min block as 'Add Prompt 7' but it is the edge-case hardening prompt — minor label inconsistency since Prompts 1-6 are numbered sequentially in the student file and the instructor references it out of that sequential context.
- The after-session notes file (260 lines) clears the 180-line threshold but is the leanest of the three; a few more lines on session retrospective or common student misconceptions observed during delivery would strengthen it.

### Recommended Fixes
- Clarify whether the QC audit scope definition (eval JSON schema, /eval/run, 5 test tickets, LLM-as-judge) was intended for Session 7, not Session 6. If so, rerun this QC audit against the Session 7 files with the correct scope block.
- If Session 6 is intentionally about LangGraph (as the files indicate), update the QC scope block for Session 6 to: 'Include: TicketState TypedDict, StateGraph, 4 nodes (classify/retrieve/generate/confidence_router), conditional edge, POST /tickets/{id}/resolve. Excluded: async graph execution, LangSmith tracing, multi-agent subgraphs, auto-sending responses to customers.'
- If the session numbering is wrong (i.e., these files should be Session 7 and the eval content should be Session 6), renumber the files and cross-session references accordingly.
- Fix the unfilled template variable '+ title +' in the QC orchestration script that spawned this audit.

---

## Session 7: Add Evals, Guardrails, and Testing
**Overall Status:** CONDITIONAL PASS — 9 of 11 checks pass; 2 checks FAIL due to scope mismatch between QC criteria and session content (coverage.py, structlog, /health endpoint are absent).

**File Sizes:** Instructor: 565 lines | Student: 522 lines | After-Session: 299 lines

### Check Results
- ✅ **CHECK 1 — TIMING** (PASS): 10 blocks total to 120 min: 0–10, 10–20, 20–35, 35–50, 50–65, 65–80, 80–95, 95–105, 105–115, 115–120 = 120 minutes, within the 110–120 range.
- ✅ **CHECK 2 — HANDS-ON** (PASS): Build activity (Prompt 1 run live with Claude Code/Cursor) starts at the 20-minute mark, well before the 35-minute threshold.
- ✅ **CHECK 3 — PROMPTS** (PASS): 9 text blocks total (1 sample block + 7 numbered prompts + 1 final explanation block); Prompt 1 is ~76 lines with exact file names, function signatures, and field-level instructions — far exceeds 15-line minimum.
- ❌ **CHECK 4 — SCOPE COMPLIANCE** (FAIL): Session 7 covers pytest/TestClient, groundedness eval, guardrails, and confidence_score — coverage.py, structlog structured logging, and a /health endpoint are entirely absent from all three files; these are listed as in-scope items in the QC criteria but are not addressed anywhere in the session.
- ✅ **CHECK 5 — INTERVIEW QUESTIONS** (PASS): Exactly 15 questions (Q1–Q5 Basic, Q6–Q10 Technical Deep-Dive, Q11–Q15 System Design); all answers are 4–6 sentences with specific code patterns, trade-off reasoning, and production context.
- ✅ **CHECK 6 — CROSS-SESSION** (PASS): Session 6 is explicitly recapped (4-node LangGraph graph, confidence routing, ChromaDB) in the Opening and Recap block; Session 8 is previewed (Docker, cloud deployment, mock interview) in the 115–120 min wrap-up block.
- ❌ **CHECK 7 — DELIVERABLE** (FAIL): The deliverable stated across all 3 files is pytest suite + groundedness eval + guardrails + confidence_score; coverage report, structured logging (structlog), and health check endpoint are absent from all three files, which do not match the QC reference deliverable definition.
- ✅ **CHECK 8 — SESSION NOT DAY** (PASS): No instances of 'Day X' found in any of the three files; all cross-session references correctly use 'Session 6', 'Session 7', and 'Session 8'.
- ✅ **CHECK 9 — COMPLETION CHECKLIST** (PASS): Instructor file contains 12 artifact-based checklist items covering conftest.py, test_tickets.py, test_classifier.py, pytest run, evals/__init__.py, groundedness.py, edge case handling, generate_node guardrail, post-check, confidence_score, Swagger verification, and verbal explanation — exceeds the 10-item minimum.
- ✅ **CHECK 10 — TECHNICAL DEPTH** (PASS): Code-level detail throughout: exact bash commands, dependency_overrides pattern, ChromaDB distance-to-similarity conversion formula, unittest.mock.patch pattern with MagicMock structure, fixture scope explanation, sqlalchemy error causes — appropriate depth for Cohort B.
- ✅ **CHECK 11 — FILE SIZE** (PASS): Instructor: 565 lines (min 300, PASS); Student: 522 lines (min 250, PASS); After-session: 299 lines (min 180, PASS).

### Critical Issues
- CHECK 4 FAIL: coverage.py is listed as in-scope in the QC criteria but is not mentioned anywhere in the instructor file, student file, or after-session notes. No 'pytest --cov' command, no coverage report, no .coveragerc configuration.
- CHECK 4 FAIL: structlog structured logging is listed as in-scope in the QC criteria but is completely absent from all three files. The session uses Python's built-in logging module only (referenced once in Prompt 7), not structlog.
- CHECK 4 FAIL: A /health endpoint is listed as in-scope in the QC criteria but is not mentioned or built in any of the three files.
- CHECK 7 FAIL: The QC reference deliverable ('pytest suite, coverage report, structured logging, health check, error handling') does not match the actual deliverable stated consistently across all 3 files ('pytest suite, groundedness eval, guardrails, confidence_score'). Either the QC reference definition is wrong for this session, or the session is missing three deliverable components.

### Minor Issues
- The student file has 9 prompts (7 numbered + 1 sample block + 1 final explanation block) but only Prompts 1–7 are labelled as prompts to use during the session; the 'Content to Prepare Before Class' block and 'Final Session 7 Explanation' block are text blocks but not build prompts — the count of usable build/debug prompts is 7, not 9.
- The after-session notes reference 'text-embedding-ada-002' at line 160 as a specific model but this model is deprecated as of the knowledge cutoff; no impact on session quality but worth flagging for accuracy.
- The instructor's 'Concept Pause' block (95–105 min) includes a 'System Flow Diagram' in a code block — this is good, but it duplicates the student file diagram nearly verbatim; a brief note to instructors that this is intentional reinforcement would be helpful.

### Recommended Fixes
- Clarify whether the QC scope definition for Session 7 is correct: if coverage.py, structlog, and /health endpoint are truly required, add them to all 3 files (install coverage.py, add 'pytest --cov=app tests/', add a /health route in main.py, replace logging with structlog in nodes.py). If the session's actual scope (groundedness eval + guardrails + confidence_score) is the intended design, update the QC reference deliverable definition to match.
- If coverage.py is added: update the instructor completion checklist to include 'pytest --cov=app tests/ runs and shows >= 80% coverage on routes/tickets.py', update Prompt 1 in the student file to generate a .coveragerc, and add a coverage report section to the after-session notes.
- If structlog is added: update instructor notes to explain structlog vs standard logging, add 'pip install structlog' to the student prerequisites block, and add a walkthrough section for structlog configuration in generate_node and the resolve endpoint.
- If /health endpoint is added: add it to the instructor's 'Do Not Include' override (it is simple and should be scoped clearly), add a test_health_endpoint test to test_tickets.py, and show it in the Swagger walkthrough.
- Consider adding 'pytest --cov' to the 65–80 min 'Run Commands' block even as an optional extension, since coverage is a natural follow-on after getting all tests to pass and many interviewers ask about it.

---

## Session 8: Deployment, Demo, System Design, and Mock Interview
**Overall Status:** WARN — Session 8 is high quality and technically solid. Two WARN items relate to scope definition mismatch (Railway deployment included but QC scope lists it as excluded; docker-compose absent but listed in QC deliverable definition). No FAIL items. No critical bugs or missing content found.

**File Sizes:** Instructor: 654 lines | Student: 673 lines | After-Session: 398 lines

### Check Results
- ✅ **CHECK 1 — TIMING** (PASS): 10 blocks total exactly 120 min: 0-10, 10-20, 20-35, 35-50, 50-65, 65-80, 80-95, 95-105, 105-115, 115-120 = 120 min, within the 110-120 min window.
- ✅ **CHECK 2 — HANDS-ON START** (PASS): Build activity (requirements.txt, .env.example, README) starts at the 20-minute mark — well before the 35-minute threshold.
- ✅ **CHECK 3 — PROMPTS** (PASS): 7 prompts in ```text blocks (Prompts 1-7). Main build prompt (Prompt 1: README Generation) is ~67 lines, highly specific with file structure, endpoints, AI features, and 8 numbered output requirements.
- ⚠️ **CHECK 4 — SCOPE COMPLIANCE** (WARN): Actual cloud deployment to Railway is included (65-80 min block) but the QC scope lists 'actual cloud deployment' as excluded. docker-compose.yml is absent from all deliverables — explicitly blocked ('Do not build a Dockerfile'). Session scope fits the project's final-session intent but diverges from the QC scope definition.
- ✅ **CHECK 5 — INTERVIEW QUESTIONS** (PASS): Exactly 15 questions (Q1-Q15) with expected answers. All answers are 3-6 sentences with specific technical vocabulary: model names, error types, code patterns, HTTP status codes.
- ✅ **CHECK 6 — CROSS-SESSION** (PASS): Instructor file correctly recaps Session 7 state in detail (lines 98-112). No next-session preview needed — this is the final session; the closing block explicitly lists all Sessions 1-8.
- ⚠️ **CHECK 7 — DELIVERABLE STATEMENT** (WARN): Deliverable is clearly stated in all 3 files. However, docker-compose.yml is absent (explicitly excluded by this session's scope), and 'deployment config' is Railway-based rather than Docker-based. The deliverable language differs from the QC-defined expected set of 'Polished app, docker-compose, deployment config, demo script, viva Q&A'.
- ✅ **CHECK 8 — SESSION NOT DAY** (PASS): No instances of 'Day X' found in any of the three files. All references consistently use 'Session X' throughout.
- ✅ **CHECK 9 — COMPLETION CHECKLIST** (PASS): Instructor file has 12 artifact-based checklist items (lines 630-642): requirements.txt, .env.example, .gitignore, README sections, architecture diagram, Railway deployment, Swagger UI, POST /tickets live test, GET /suggest live test, demo run, RAG verbal explanation, limitation verbal answer.
- ✅ **CHECK 10 — TECHNICAL DEPTH** (PASS): Code-level depth throughout: bash pip freeze command, uvicorn start command with $PORT, jwt.decode() call, collection.query() pattern, check_same_thread=False, StateGraph node wiring, 1536-dimension embedding. All concepts tied directly to project files and line-level behavior.
- ✅ **CHECK 11 — FILE SIZE** (PASS): Instructor: 654 lines (threshold 300). Student: 673 lines (threshold 250). After-session: 398 lines (threshold 180). All three comfortably exceed minimums.

### Critical Issues
- Scope mismatch: The QC scope definition states 'Excluded: actual cloud deployment' but Session 8 devotes a full 15-minute block (65-80 min) to Railway deployment and lists it as a primary deliverable. This is a deliberate design choice for this final session but contradicts the stated QC scope boundary.
- docker-compose.yml is explicitly absent: The QC-defined deliverable set includes 'docker-compose' but the session explicitly blocks Docker ('Do not build a Dockerfile — mention as a future improvement only'). The session uses Railway deployment config instead. Either the QC scope definition needs updating to reflect Railway-based deployment, or the session needs a docker-compose.yml activity added.

### Minor Issues
- The deliverable statement in all 3 files does not use the exact phrasing 'Polished app, docker-compose, deployment config, demo script, viva Q&A' — it is present in substance but not as a consolidated single-line summary matching the QC template language.
- After-session file demo checklist (lines 386-398) has 12 items but uses square bracket checkboxes without numbering — minor formatting inconsistency vs instructor checklist.
- Prompt 6 (Mock Viva Prompt) asks the AI to generate 15 viva Q&A pairs as a prompt task, but the instructor file already contains the 15 Q&A pairs. Students may run duplicate work — a cross-reference note would prevent this.
- The instructor's 'Questions to Discuss' section prioritizes Q6, 8, 10, 12, 14 for the 105-115 min block but the session flow shows only 10 minutes for this block — 6-8 questions in 10 minutes is tight; 5 questions would be more realistic.

### Recommended Fixes
- Resolve scope conflict: Either update the QC scope definition to read 'Includes: Railway/Render deployment (no Docker)' or add a brief docker-compose.yml generation activity (5 min) to the build block and list it as a deliverable, replacing or supplementing the Railway deployment step.
- Add a one-line deliverable summary to all 3 files that exactly matches the QC template: 'Deliverable: Polished app, Railway deployment config, .env.example, demo script, 15 viva Q&A pairs' — this makes QC audits unambiguous.
- Add a cross-reference note near Prompt 6 in the student file: 'Note: The instructor file already contains 15 Q&A pairs with model answers. Use this prompt only if you want to generate additional practice questions.'
- Reduce the viva block guidance from '6-8 questions' to '4-5 questions' in the 105-115 min instructor notes to match the 10-minute time allocation realistically.

---

## Overall QC Summary
- PASS: 1
- PASS WITH WARNINGS: 1
- FAIL: 6
