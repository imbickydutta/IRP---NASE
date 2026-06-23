# Cohort C — AI Systems Interview Portfolio
# QC Report

**Generated:** 2026-06-23
**Reviewer:** QC Agent (Claude Sonnet 4.6)
**Scope:** Sessions 1–8, all three file types per session (instructor plan, student pre-session, after-session notes)
**Checks Applied:** 2-hour feasibility, hands-on nature, Gemini-only (no OpenAI), prompt quality, scope compliance, cross-session links, deliverable clarity

---

## Summary Table

| Session | Title | Status |
|---------|-------|--------|
| 1 | Structured Output Prompt Engine | PASS |
| 2 | LLM Logging and Evaluation Tracker | PASS |
| 3 | Serverless-Style AI Function | PASS |
| 4 | Basic RAG Pipeline | PASS WITH WARNINGS |
| 5 | RAG Evaluation and Improvement | PASS WITH WARNINGS |
| 6 | Simple Agent Router | PASS WITH WARNINGS |
| 7 | Vision/OCR Mini Module | PASS |
| 8 | Final System Design and Interview Demo | PASS WITH WARNINGS |

---

## Session 1: Structured Output Prompt Engine

**Overall Status: PASS**

### Issues Found

1. **Minor — No issue with Gemini compliance.** The instructor notes explicitly flag and correct any AI-generated `import openai` patterns. This is pre-emptive, not a defect.
2. **Minor — Free-text vs structured comparison uses temperature=0.7 for the free-text pass.** This is intentional (to show natural variability) but is not stated explicitly in the student pre-session file. Students may not understand why the free-text call uses a different temperature.
3. **Minor — No explicit mention of `python-dotenv` in the scope/include list**, though it appears in the setup instructions. This is a small consistency gap between the strict scope control section and the setup section.

### Fixes Applied

None required. Issues are informational only.

### Key Scope Compliance Notes

- Gemini 1.5 Flash via `google-generativeai` only. OpenAI explicitly excluded.
- Deliverables are tightly scoped: `structured_output_engine.py` + `output_examples.json`. No web server, no database, no LangChain.
- `response_mime_type="application/json"` and `temperature=0` are correctly required.
- 2-hour feasibility: PASS. The session flow is minutely planned (0–10, 10–20, 20–35 etc.) and the build is a single Python script. Scope is tightly controlled with explicit "Do Not Include" list.
- Hands-on nature: PASS. Students build their own version in the 50–65 min block after the instructor demo.
- Cross-session link: correctly previews Session 2 (logging layer wrapping Session 1's calls). Consistent with Session 2's opening framing.
- 15 interview questions with expected answers are well-formed, technically specific, and relevant.
- Completion checklist (12 items) is clear and binary-checkable.

---

## Session 2: LLM Logging and Evaluation Tracker

**Overall Status: PASS**

### Issues Found

1. **Minor — Portfolio module map in student pre-session file (Session 2) lists different session titles for Sessions 3–8 than the actual sessions delivered.** Specifically:
   - Session 2 student file says Session 3 = "Serverless-Style AI Function" (correct), Session 6 = "Fine-Tuning Preparation Toolkit", Session 7 = "LangGraph Agent", Session 8 = "Portfolio Integration and Interview Walkthrough".
   - Actual sessions delivered: Session 6 = "Simple Agent Router", Session 7 = "Vision/OCR Mini Module", Session 8 = "Final System Design and Interview Demo".
   - This is a forward-looking map written before Sessions 6–8 were finalised, so it is not a runtime error, but it creates confusion if students check their pre-session file mid-portfolio.

2. **Minor — Token estimation formula (`len(prompt.split()) * 1.3`) is described as an approximation but the 20–50% potential variance is only mentioned in Q13 of instructor questions**, not in the student pre-session file. Students may cite the formula in interviews without knowing its accuracy bounds.

3. **Minor — `output_tokens` are noted as not estimated in the student file's limitations section**, but the instructor annotated code reference says estimated_cost_usd only covers input tokens. This asymmetry in cost awareness should be flagged more prominently to students during the session.

### Fixes Applied

None required. Issue 1 is a pre-session document written before final session titles were locked; this should be updated when portfolio materials are revised. Issues 2 and 3 are informational.

### Key Scope Compliance Notes

- Gemini 1.5 Flash only. OpenAI, Langfuse, LangSmith are explicitly excluded from implementation (mention-only allowed).
- Deliverables: `llm_logger.py`, `llm_logs.csv`, `eval_summary.json`. No pandas, no database, no dashboard.
- 2-hour feasibility: PASS. 7 test cases, 3 functions, flat file output. Well within 2 hours.
- Hands-on nature: PASS. Students generate and run their own version in the 50–65 min block.
- Cross-session link: correctly references Session 1 (wraps structured output engine's calls) and previews Session 3 (imports `log_llm_call`). Consistent with Session 3's framing.
- 10 quick-fire viva questions and 15 full interview questions are well-formed.
- Completion checklist (12 items) is clear and verifiable.

---

## Session 3: Serverless-Style AI Function

**Overall Status: PASS**

### Issues Found

1. **Minor — Portfolio module map in Session 3 student pre-session file lists different session titles for Sessions 6–8 than delivered.** The student file lists:
   - Session 6 = "Fine-Tuning Preparation and Dataset Builder"
   - Session 7 = "Agentic Workflow with Tool Use"
   - Session 8 = "LLMOps Dashboard"
   - Actual delivered: Session 6 = "Simple Agent Router", Session 7 = "Vision/OCR Mini Module", Session 8 = "Final System Design and Interview Demo".
   - Same root cause as the Session 2 issue — forward-looking map written before final titles were locked.

2. **Minor — The cold start concept is described correctly as local-only (cannot be demonstrated without actual Lambda deployment)**, but the student pre-session file describes cold start at the conceptual level without the explicit caveat that it cannot be observed locally. The instructor file correctly includes this caveat; the student file does not.

3. **Minor — `python-dotenv` is added as a new dependency for Session 3**, but Session 1 also lists `pip install python-dotenv` in its setup. This could cause student confusion about why `dotenv` is being introduced again. The instructor should clarify that Session 3 is the first session where `dotenv` is architecturally central (`.env.example` artifact).

### Fixes Applied

None required.

### Key Scope Compliance Notes

- Gemini 1.5 Flash via `google-generativeai` only. No OpenAI, no Flask, no FastAPI, no async.
- Deliverables: `ai_handler.py` + `.env.example`. No web server, no DB, no ChromaDB (explicitly excluded).
- `response_mime_type="application/json"` correctly required inside `generation_config`.
- 2-hour feasibility: PASS. Four functions (`validate_event`, `call_gemini`, `handler`, `local_test`), 3 test payloads. Tight scope.
- Hands-on nature: PASS. Students build in the 50–65 min block.
- Cross-session link: correctly builds on Sessions 1 (structured output) and 2 (observability), correctly previews Session 4 (RAG pipeline). The statement "Session 4's `ask()` function follows the same handler pattern" is accurate.
- 15 interview questions are technically specific and production-aware.
- Completion checklist (13 items) is clear and binary-checkable.

---

## Session 4: Basic RAG Pipeline

**Overall Status: PASS WITH WARNINGS**

### Issues Found

1. **WARNING — Portfolio module map inconsistency across documents.** The Session 4 student pre-session file lists:
   - Session 6 = "Fine-Tuning Data Preparation" (`fine_tune_prep.py`)
   - Session 7 = "Tool-Calling Agent Loop" (`agent_loop.py`)
   - Session 8 = "Capstone — End-to-End AI Pipeline" (`capstone_pipeline.py`)
   - Actual delivered: Session 6 = "Simple Agent Router" (`agent_router.py`), Session 7 = "Vision/OCR Mini Module" (`vision_ocr_module.py`), Session 8 = "Final System Design and Interview Demo" (documentation only).
   - This is the most divergent instance of the portfolio map inconsistency. The filenames listed (`agent_loop.py`, `capstone_pipeline.py`) do not match any delivered session.

2. **WARNING — The instructor file mentions `sentence-transformers` cold start adding 4–6 seconds.** This is stated in the context of Session 3 (serverless handler concept explanation), not Session 4. The cross-reference is technically accurate but may confuse students reading Session 4 materials in isolation.

3. **Minor — Session 4's instructor file strictly excludes hybrid search, re-ranking, and sliding window chunking**, but the student pre-session file does not repeat the Do Not Include list explicitly. Students using only the student file during sessions may not know these are out of scope, leading to AI-generated code that includes them.

4. **Minor — `sentence-transformers` with model `all-MiniLM-L6-v2` produces 384-dimensional embeddings.** This is correctly stated in the instructor file but not in the student pre-session file. Students should be able to answer "how many dimensions?" in an interview — this number should appear in the student materials.

### Fixes Applied

None required. Issue 1 is a document-level inconsistency in the forward-looking portfolio map; it does not affect the actual Session 4 build.

### Key Scope Compliance Notes

- Gemini 1.5 Flash for generation, `sentence-transformers` (local) for embeddings. No OpenAI embeddings, no paid embedding API.
- Deliverables: `rag_pipeline.py` + `chroma_db/`. No PDF parser, no web server, no re-ranking.
- 2-hour feasibility: PASS WITH CAUTION. This is noted in the instructor file as "the most technically substantial module." The scope is tightly controlled but ChromaDB setup and `sentence-transformers` model download can add unexpected time. The instructor backup plan addresses this.
- Hands-on nature: PASS. Students build their own `rag_pipeline.py` with the instructor running the `ask()` function together as a class.
- Cross-session link: correctly connects to Session 3 pattern (`ask()` function as handler pattern) and feeds directly into Session 5 (same ChromaDB collection reused). The note "do not delete Session 4 files" is present in both Session 4 and Session 5 documents.
- RAG vs vanilla comparison is correctly required as part of the deliverable.

---

## Session 5: RAG Evaluation and Improvement

**Overall Status: PASS WITH WARNINGS**

### Issues Found

1. **WARNING — Portfolio module map in Session 5 student pre-session file differs from actual sessions 6–8 delivered.** The student file lists:
   - Session 6 = "Agent Router — LLM-driven tool selection" (correct title)
   - Session 7 = "Fine-Tuning Primer — dataset prep and model fine-tuning concepts"
   - Session 8 = "LangGraph Pipeline — multi-step agentic workflow"
   - Actual delivered: Session 7 = "Vision/OCR Mini Module", Session 8 = "Final System Design and Interview Demo".
   - Session 6 title is correct in this version, but Sessions 7 and 8 do not match.

2. **Minor — The evaluation scoring in Session 5 uses keyword overlap (not LLM-as-judge or embedding similarity).** This is explicitly acknowledged and defended in both instructor and student files. However, the student file lists "groundedness" and "faithfulness" as synonyms, while the instructor file only uses "groundedness." There is no actual inconsistency but the student file introduces "faithfulness" without defining it — an interviewer may use "faithfulness" and students may not recognise the term as describing the same concept.

3. **Minor — The `compare_runs()` output format is described as "before/after comparison table" in the instructor file but the mechanism (f-string formatting vs `tabulate`) is left open.** If `tabulate` is generated by AI but not installed, students get a ModuleNotFoundError. The instructor file includes `tabulate` as an option but should state it needs `pip install tabulate` if used.

### Fixes Applied

None required.

### Key Scope Compliance Notes

- Gemini 1.5 Flash for generation, `sentence-transformers` for query embedding. No RAGAS, no DeepEval, no OpenAI.
- Deliverables: `rag_evaluator.py` + `rag_eval_report.csv` + before/after console output. No new ChromaDB ingestion.
- 2-hour feasibility: PASS. 5 test questions, 6 functions, CSV output, one parameter change. Feasible.
- Hands-on nature: PASS. Students run their own evaluator and inspect the CSV results.
- Cross-session link: correctly requires Session 4's ChromaDB to be intact. Backup plan (use instructor's shared `chroma_db/`) is provided.
- The improvement loop (change one parameter, rerun, compare) is pedagogically sound and correctly scoped to one variable at a time.

---

## Session 6: Simple Agent Router

**Overall Status: PASS WITH WARNINGS**

### Issues Found

1. **WARNING — Portfolio module map inconsistency in Session 6 student pre-session file.** The student file lists:
   - Session 7 = "Fine-Tuning Preparation and Dataset Builder" (`finetune_dataset_builder.py`)
   - Session 8 = "Agentic Workflow with Tool Use" (`ai_agent.py`)
   - Actual delivered: Session 7 = "Vision/OCR Mini Module" (`vision_ocr_module.py`), Session 8 = "Final System Design and Interview Demo" (documentation only, no new script).
   - This is a significant mismatch — the student file implies an agentic workflow module exists in Session 8 when it does not.

2. **WARNING — The instructor session plan references "memory system or conversation history" as out of scope and tells instructors to say "that is Session 8 territory."** But Session 8 in the delivered curriculum is documentation-only, not an agent with memory. This cross-reference is misleading — there is no session that builds memory-based agents in this portfolio. Students told "we will do memory in Session 8" will not find it.

3. **Minor — `rag_answer()` tool function in `agent_router.py` is described as either "a stub/simple call, or a minimal call to the existing rag_pipeline.py."** The ambiguity between a stub and a real call is not resolved in the student materials. Students may implement different versions and have inconsistent portfolio artifacts. A clear recommendation (use a stub with a comment explaining the real integration path) would be cleaner.

4. **Minor — The instructor's "Do Not Include" list excludes ChromaDB integration inside `agent_router.py`**, but the Session 6 after-session notes confirm that `rag_answer()` calls the RAG pipeline from Session 4. This is technically a ChromaDB dependency by proxy. The scope note is accurate (ChromaDB is not directly referenced in `agent_router.py`) but could mislead students who interpret "no ChromaDB" as "no connection to Session 4."

### Fixes Applied

None required.

### Key Scope Compliance Notes

- Gemini 1.5 Flash for intent classification. No OpenAI, no LangChain, no LangGraph (mention-only allowed).
- Deliverables: `agent_router.py` + console output showing `Intent → Tool → Result` for 4–5 queries. No web server, no memory, no external APIs.
- `response_mime_type="application/json"` correctly required for the intent classifier's structured output.
- 2-hour feasibility: PASS. Four tool functions, one router function, 4–5 test queries. Achievable.
- Hands-on nature: PASS. Students generate and run their own `agent_router.py`.
- Cross-session link: correctly uses Session 4's RAG pipeline as a tool. Correctly introduces LangGraph as a conceptual upgrade (not implemented). Correctly previews Session 7 (Vision/OCR module).

---

## Session 7: Vision/OCR Mini Module

**Overall Status: PASS**

### Issues Found

1. **Minor — `sample_image.png` is described as "a pre-built or ASCII-art-generated sample document image included in the repo" in the instructor file**, but the after-session notes confirm it is generated programmatically using Pillow's `ImageDraw`. The student pre-session file is silent on how the image is created. If students run the script expecting to find a pre-existing PNG, they will not find one. The script must generate it, which is correct per the after-session notes, but the student materials should be more explicit about this.

2. **Minor — `PIL` (Pillow) is listed as a required import but does not appear in any "pip install" prerequisite list in the student pre-session file.** If a student's environment does not have Pillow installed, the script will fail with `ModuleNotFoundError: No module named 'PIL'` and there is no backup plan explicitly covering this.

3. **Minor — The confidence_notes field is required in the prompt and in the output schema**, but the student materials do not define what constitutes an acceptable confidence note versus an empty string. Students may not know how to validate this field in their output.

### Fixes Applied

None required.

### Key Scope Compliance Notes

- Gemini 1.5 Flash multimodal (vision + text) via `google-generativeai`. No pytesseract, no OpenCV, no paid vision APIs.
- Deliverables: `vision_ocr_module.py` + `sample_image.png` + `ocr_output.json`. No GUI, no batch processing, no multi-page handling.
- `response_mime_type="application/json"` correctly used (consistent with Sessions 1, 3, 6).
- 2-hour feasibility: PASS. One function (`analyze_image`), one sample image, one JSON output. Tight and achievable.
- Hands-on nature: PASS. Students generate their own script, create the sample image, and inspect `ocr_output.json`.
- Cross-session link: correctly frames this as using the same Gemini API key as all previous sessions, the same structured output thinking as Session 1, and the same confidence/evaluation mindset as Sessions 2 and 5. Correctly previews Session 8 (system design discussion where vision module would form part of a document AI pipeline).
- The human-review requirement for non-empty `confidence_notes` is a valid production design principle and is correctly included.

---

## Session 8: Final System Design and Interview Demo

**Overall Status: PASS WITH WARNINGS**

### Issues Found

1. **WARNING — Session 8 delivers no new Python script.** The instructor file, student pre-session file, and after-session notes are all consistent on this point. However, several earlier session documents (Sessions 2, 3, 6 student files) referred to Session 8 as building a working script (`portfolio_runner.py`, `ai_agent.py`, or an "LLMOps Dashboard"). Students who read their earlier session files expecting to build something new in Session 8 may arrive unprepared for a documentation-only session. A brief statement in the Session 8 opening ("this session produces documentation, not code — this is intentional") should be added to the instructor's opening remarks.

2. **WARNING — The 6 documentation deliverables (README.md, architecture_diagram.md, demo_script.md, viva_prep.md, module_summary.md, limitations.md) are generated using AI (Claude Code or Cursor via Prompts 1–6).** The session plan does not include any individual verification step where students confirm that their generated README correctly describes their own portfolio (not a generic one). Students with gaps in earlier sessions (e.g., Session 4 ChromaDB broken) may generate README files that describe modules they did not successfully build.

3. **Minor — The architecture diagram uses Mermaid notation.** This is appropriate, but the instructor note says "the diagram does not need to be beautiful, it needs to be correct and explainable." The student pre-session file does not include a minimal example of Mermaid syntax or a sample node/arrow format. Students unfamiliar with Mermaid may generate syntactically broken diagrams.

4. **Minor — Viva prep document (15 Q&A pairs) is AI-generated.** The instructor file requires students to "memorize and practice saying out loud" — but there is no in-session mechanism to verify students have actually practiced versus just having the file. The session plan allocates time for oral practice but does not specify how many Q&A pairs are practiced live.

### Fixes Applied

None required.

### Key Scope Compliance Notes

- No new Python script, no new Gemini API call, no new ChromaDB collection. This is correct per the session objective.
- Deliverables: 6 Markdown documentation files. These are clearly defined and enumerable.
- 2-hour feasibility: PASS. AI-generated documentation for 7 modules across 6 files, with review, oral practice, and walkthrough, is feasible in 2 hours if the AI tools work efficiently.
- Hands-on nature: PASS (documentation-style). Students generate, review, and practice their own materials.
- Cross-session link: references all 7 previous sessions explicitly. The architecture diagram must show ChromaDB as shared between Sessions 4 and 5, and Gemini as a shared external dependency across Sessions 1–7.
- The module summary table (one row per module, 8 columns) is a strong interview reference artifact.
- Production vocabulary coverage (latency, throughput, cost per call, hallucination rate, embedding dimensions, context window) is correct and well-specified.

---

## Cross-Session Issues (Global)

### Issue 1 — Portfolio Module Map Inconsistency (AFFECTS SESSIONS 1–6 STUDENT FILES)

**Severity: WARNING**

The student pre-session files for Sessions 1 through 6 each contain a "Portfolio Module Map" that lists all 8 sessions. These maps were written at different times during content development and reflect different planning states. As a result, Sessions 6, 7, and 8 are described with different titles, filenames, and concepts across these documents.

**Summary of map variants found:**

| Document | S6 Listed As | S7 Listed As | S8 Listed As |
|----------|-------------|-------------|-------------|
| Session 1 student file | Multi-Step Prompt Chain | LLMOps Monitoring Dashboard | Agentic Workflow with Tool Use |
| Session 2 student file | Fine-Tuning Preparation Toolkit | LangGraph Agent | Portfolio Integration and Interview Walkthrough |
| Session 3 student file | Fine-Tuning Preparation and Dataset Builder | Agentic Workflow with Tool Use | LLMOps Dashboard |
| Session 4 student file | Fine-Tuning Data Preparation | Tool-Calling Agent Loop | Capstone — End-to-End AI Pipeline |
| Session 5 student file | Agent Router (correct) | Fine-Tuning Primer | LangGraph Pipeline |
| Session 6 student file | (current session) | Fine-Tuning Preparation and Dataset Builder | Agentic Workflow with Tool Use |
| **Actual delivered** | **Simple Agent Router** | **Vision/OCR Mini Module** | **Final System Design + Interview Demo** |

**Impact:** Students reading earlier session materials mid-portfolio will see session names that do not match what they are actually building. This creates confusion and breaks the "progressive portfolio map" narrative.

**Recommended Fix:** Update all portfolio module maps in Sessions 1–6 student files to reflect the final delivered session titles. This is a documentation update only and does not affect any Python code or Gemini usage.

---

### Issue 2 — No Unified "No OpenAI" Enforcement Mechanism

**Severity: MINOR**

The Gemini-only requirement is correctly stated in every session's scope control section and in most build prompts. However, the enforcement is prompt-level (students are told to say "Do not import openai" in their AI prompts) rather than structural. There is no script or check that verifies the generated files do not contain OpenAI imports.

**Recommended Fix (informational):** Add a one-line post-generation check to the instructor checklist: `grep -r "import openai" session_*/` — if this returns any results, the relevant files must be regenerated.

---

### Issue 3 — `response_mime_type="application/json"` Placement Consistency

**Severity: MINOR**

Sessions 1, 3, 6, and 7 all require `response_mime_type="application/json"` in `generation_config`. Session 1 uses it as a dict key (`generation_config={"response_mime_type": "application/json"}`). Session 3 uses `genai.GenerationConfig(response_mime_type="application/json")`. Both are valid per the `google-generativeai` library, but inconsistency across sessions may confuse students about the canonical approach.

**Recommended Fix (informational):** Standardise on one form across all session build prompts. The dict form (`{"response_mime_type": "application/json", "temperature": 0}`) is simpler and is used in Sessions 1 and 2; adopt this as the standard.

---

## Deliverable Clarity Assessment

| Session | Deliverables | Clarity Rating |
|---------|-------------|---------------|
| 1 | `structured_output_engine.py` + `output_examples.json` | Clear |
| 2 | `llm_logger.py` + `llm_logs.csv` + `eval_summary.json` | Clear |
| 3 | `ai_handler.py` + `.env.example` | Clear |
| 4 | `rag_pipeline.py` + `chroma_db/` | Clear |
| 5 | `rag_evaluator.py` + `rag_eval_report.csv` + console output | Clear |
| 6 | `agent_router.py` + console output (Intent → Tool → Result) | Clear |
| 7 | `vision_ocr_module.py` + `sample_image.png` + `ocr_output.json` | Clear |
| 8 | `README.md` + `architecture_diagram.md` + `demo_script.md` + `viva_prep.md` + `module_summary.md` + `limitations.md` | Clear |

---

## Prompt Quality Assessment

All sessions provide 5–7 purpose-built prompts in the student pre-session file:

| Session | Build Prompt | Improvement Prompt | Debug Prompt | Explanation Prompt | Interview Prompt |
|---------|-------------|-------------------|--------------|-------------------|-----------------|
| 1 | Detailed, 11-point spec | Yes | Yes (429 rate limit) | Yes | Yes |
| 2 | Detailed, 13-point spec | Yes | Yes (429 rate limit) | Yes | Yes |
| 3 | Detailed, structured spec | Yes | Yes (JSONDecodeError + 429) | Yes | Yes |
| 4 | Present | Yes | Yes | Yes | Yes |
| 5 | Present | Yes | Yes | Yes | Yes |
| 6 | Present | Yes | Yes | Yes | Yes |
| 7 | Present | Yes | Yes | Yes | Yes |
| 8 | 6 separate prompts (one per doc artifact) | N/A | N/A | N/A | N/A |

**Rating: PASS across all sessions.** All build prompts explicitly state "Do NOT use openai" or equivalent Gemini-only constraints. All prompts specify deliverable filenames, required functions, and structural requirements. Debug prompts cover the most common failure mode (Gemini 429 rate limit) in every session.

---

## 2-Hour Feasibility Assessment

| Session | Assessment |
|---------|-----------|
| 1 | PASS — Single script, 4 sample inputs, 1 output file. Instructor demo + student follow-along fits 2 hours. |
| 2 | PASS — Three functions, 7 test cases, 2 output files. Well-paced across the 120-min plan. |
| 3 | PASS — Four functions, 3 test events, 2 files. Tight but achievable. |
| 4 | CAUTION — Embedding model download (`all-MiniLM-L6-v2`, ~22MB) and ChromaDB setup add 5–10 min. Instructor backup plan exists. Feasible if environment pre-set. |
| 5 | PASS — Evaluation harness wraps existing pipeline. 5 test questions. Feasible. |
| 6 | PASS — Four tool functions, one router, 4–5 test queries. Single script, minimal dependencies. |
| 7 | PASS — One function, one sample image, one JSON output. Pillow dependency may add 2–3 min setup time. |
| 8 | PASS — AI-generated documentation. Fast to produce, time spent on review and oral practice. |

---

*End of QC Report*
