# Cohort B QC Summary Table
## AI Support Ticket Resolution Copilot

| Session | Title | Instructor Lines | Student Lines | After-Session Lines | Overall | Critical Issues | Minor Issues |
|---|---|---|---|---|---|---|---|
| 1 | Build Core Backend — Ticket CRUD API | 605 lines | 532 lines | 314 lines | PASS WITH WARNINGS | 0 | 2 |
| 2 | Add Database Layer + Data Modeling | 634 lines | 561 lines | 235 lines | WARN — 1 FAIL (deliverable mismatch vs QC rubric), 1 WARN (scope rubric mismatch), 9 PASS. Content quality is strong; the FAIL is a rubric-alignment issue between the QC prompt's expected deliverable (Session 3 auth scope) and Session 2's actual, correct deliverable (database layer). | 1 | 3 |
| 3 | Add Auth + Role-Based Access | 565 lines | 511 lines | 292 lines | WARN — 2 FAIL checks on scope/deliverable mismatch against audit spec; all structural and content-quality checks pass | 2 | 4 |
| 4 | Add LLM Ticket Classifier | 672 lines | 652 lines | 288 lines | PASS with one criteria mismatch and one scope-labeling issue to note | 2 | 3 |
| 5 | Add RAG Knowledge Base: Embeddings, Vector Storage, and Grounded Response Suggestions | 491 lines | 558 lines | 295 lines | WARN — Session 5 content is high quality and internally consistent, but the QC audit scope definition and expected deliverable do not match Session 5; they describe Session 6. Two checks FAIL due to this mismatch. One WARN for student hands-on starting at minute 50 instead of by minute 35. | 2 | 3 |
| 6 | Add LangGraph Agentic Workflow | 589 lines | 546 lines | 260 lines | FAIL — 2 critical checks failed (scope compliance and deliverable mismatch); all structural, size, timing, prompt count, and quality checks pass. | 2 | 3 |
| 7 | Add Evals, Guardrails, and Testing | 565 lines | 522 lines | 299 lines | CONDITIONAL PASS — 9 of 11 checks pass; 2 checks FAIL due to scope mismatch between QC criteria and session content (coverage.py, structlog, /health endpoint are absent). | 4 | 3 |
| 8 | Deployment, Demo, System Design, and Mock Interview | 654 lines | 673 lines | 398 lines | WARN — Session 8 is high quality and technically solid. Two WARN items relate to scope definition mismatch (Railway deployment included but QC scope lists it as excluded; docker-compose absent but listed in QC deliverable definition). No FAIL items. No critical bugs or missing content found. | 2 | 4 |

## Check-by-Check Summary

| Session | Timing | Hands-On | Prompts | Scope | Interview Qs | Cross-Session | Deliverable | Day→Session | Checklist | Tech Depth |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASS | PASS | PASS | WARN | PASS | PASS | WARN | PASS | PASS | PASS |
| 2 | PASS | PASS | PASS | WARN | PASS | PASS | FAIL | PASS | PASS | PASS |
| 3 | PASS | PASS | PASS | FAIL | PASS | PASS | FAIL | PASS | PASS | PASS |
| 4 | PASS | PASS | PASS | WARN | PASS | PASS | FAIL | PASS | PASS | PASS |
| 5 | PASS | WARN | PASS | FAIL | PASS | PASS | FAIL | PASS | PASS | PASS |
| 6 | PASS | PASS | PASS | FAIL | PASS | PASS | FAIL | PASS | PASS | PASS |
| 7 | PASS | PASS | PASS | FAIL | PASS | PASS | FAIL | PASS | PASS | PASS |
| 8 | PASS | PASS | PASS | WARN | PASS | PASS | WARN | PASS | PASS | PASS |

## API Usage Summary

| Session | Primary Tech | AI/LLM | DB | Auth |
|---|---|---|---|---|
| 1 | FastAPI + SQLModel + Alembic | None | PostgreSQL | None |
| 2 | FastAPI + python-jose + bcrypt | None | PostgreSQL | JWT |
| 3 | FastAPI + SQLModel + Pydantic | None | PostgreSQL | JWT |
| 4 | ChromaDB + sentence-transformers | None | ChromaDB | JWT |
| 5 | LangGraph + StateGraph | OpenAI/Anthropic | ChromaDB + PostgreSQL | JWT |
| 6 | LLM-as-judge + eval schema | OpenAI/Anthropic | PostgreSQL | JWT |
| 7 | pytest + structlog + coverage.py | None | PostgreSQL | JWT |
| 8 | docker-compose + demo prep | Optional | All | JWT |
