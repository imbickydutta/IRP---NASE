from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ─── COLOR PALETTE ────────────────────────────────────────────────────────────
DARK_NAVY   = colors.HexColor('#0D1B2A')
ACCENT_BLUE = colors.HexColor('#1565C0')
LIGHT_BLUE  = colors.HexColor('#E3F0FF')
ACCENT_TEAL = colors.HexColor('#00838F')
LIGHT_TEAL  = colors.HexColor('#E0F7FA')
ACCENT_PURPLE = colors.HexColor('#6A1B9A')
LIGHT_PURPLE  = colors.HexColor('#F3E5F5')
MID_GREY    = colors.HexColor('#546E7A')
LIGHT_GREY  = colors.HexColor('#F5F7FA')
WHITE       = colors.white
TABLE_HDR   = colors.HexColor('#1A237E')
ROW_ALT     = colors.HexColor('#F0F4FF')


def make_styles(accent, light):
    styles = getSampleStyleSheet()
    return {
        'cover_title': ParagraphStyle('cover_title',
            fontSize=28, textColor=WHITE, fontName='Helvetica-Bold',
            leading=34, alignment=TA_CENTER, spaceAfter=6),
        'cover_sub': ParagraphStyle('cover_sub',
            fontSize=14, textColor=colors.HexColor('#CFD8DC'),
            fontName='Helvetica', leading=18, alignment=TA_CENTER, spaceAfter=4),
        'cover_tag': ParagraphStyle('cover_tag',
            fontSize=11, textColor=colors.HexColor('#B0BEC5'),
            fontName='Helvetica-Oblique', leading=14, alignment=TA_CENTER),
        'section_heading': ParagraphStyle('section_heading',
            fontSize=14, textColor=accent, fontName='Helvetica-Bold',
            leading=18, spaceBefore=14, spaceAfter=6,
            borderPad=4),
        'session_title': ParagraphStyle('session_title',
            fontSize=11, textColor=WHITE, fontName='Helvetica-Bold',
            leading=14, spaceBefore=2, spaceAfter=2),
        'session_label': ParagraphStyle('session_label',
            fontSize=9, textColor=colors.HexColor('#B0BEC5'),
            fontName='Helvetica', leading=12),
        'body': ParagraphStyle('body',
            fontSize=9.5, textColor=DARK_NAVY, fontName='Helvetica',
            leading=14, spaceAfter=4),
        'bullet': ParagraphStyle('bullet',
            fontSize=9, textColor=MID_GREY, fontName='Helvetica',
            leading=13, leftIndent=12, bulletIndent=0, spaceAfter=1),
        'deliverable': ParagraphStyle('deliverable',
            fontSize=9, textColor=accent, fontName='Helvetica-Bold',
            leading=13, spaceAfter=2),
        'goal_box': ParagraphStyle('goal_box',
            fontSize=10.5, textColor=DARK_NAVY, fontName='Helvetica',
            leading=16, spaceAfter=4),
        'table_hdr': ParagraphStyle('table_hdr',
            fontSize=8.5, textColor=WHITE, fontName='Helvetica-Bold',
            leading=11, alignment=TA_CENTER),
        'table_cell': ParagraphStyle('table_cell',
            fontSize=8, textColor=DARK_NAVY, fontName='Helvetica',
            leading=11),
        'table_cell_bold': ParagraphStyle('table_cell_bold',
            fontSize=8, textColor=DARK_NAVY, fontName='Helvetica-Bold',
            leading=11),
    }


def cover_block(story, title, subtitle, tag, accent, light):
    # Full-width banner via a 1-cell table
    banner_data = [[
        [
            Paragraph(title, make_styles(accent, light)['cover_title']),
            Spacer(1, 4),
            Paragraph(subtitle, make_styles(accent, light)['cover_sub']),
            Spacer(1, 2),
            Paragraph(tag, make_styles(accent, light)['cover_tag']),
        ]
    ]]
    banner = Table(banner_data, colWidths=[170*mm])
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), accent),
        ('ROUNDEDCORNERS', [8]),
        ('TOPPADDING',    (0,0), (-1,-1), 28),
        ('BOTTOMPADDING', (0,0), (-1,-1), 28),
        ('LEFTPADDING',   (0,0), (-1,-1), 18),
        ('RIGHTPADDING',  (0,0), (-1,-1), 18),
    ]))
    story.append(banner)
    story.append(Spacer(1, 10))


def goal_block(story, text, accent, light):
    s = make_styles(accent, light)
    data = [[Paragraph('<b>End Goal</b>', s['section_heading']),
             Paragraph(text, s['goal_box'])]]
    t = Table([[
        Paragraph(text, s['goal_box'])
    ]], colWidths=[170*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING',    (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))


def overview_block(story, items, accent, light):
    """Key program stats as pill chips in a row."""
    s = make_styles(accent, light)
    cells = []
    for label, val in items:
        cells.append(Paragraph(f'<b>{val}</b><br/><font size=7 color="#546E7A">{label}</font>',
                                ParagraphStyle('chip', fontSize=10, fontName='Helvetica-Bold',
                                               textColor=accent, leading=13, alignment=TA_CENTER)))
    chip_table = Table([cells], colWidths=[170*mm/len(cells)]*len(items))
    chip_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEAFTER', (0,0), (-2,-1), 0.5, colors.HexColor('#BBDEFB')),
    ]))
    story.append(chip_table)
    story.append(Spacer(1, 12))


def session_card(story, number, title, topics, deliverable, accent, light):
    s = make_styles(accent, light)
    # Header row
    hdr = Table([[
        Paragraph(f'Session {number}', s['session_label']),
        Paragraph(title, s['session_title']),
    ]], colWidths=[22*mm, 140*mm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), accent),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    # Body: topics + deliverable
    topic_paras = [Paragraph(f'• {t}', s['bullet']) for t in topics]
    del_para = Paragraph(f'<b>Deliverable:</b> {deliverable}', s['deliverable'])
    body_content = topic_paras + [Spacer(1, 4), del_para]

    body = Table([[body_content]], colWidths=[170*mm])
    body.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 12),
        ('RIGHTPADDING',  (0,0), (-1,-1), 12),
    ]))

    story.append(KeepTogether([hdr, body, Spacer(1, 6)]))


def summary_table(story, sessions, accent, light):
    s = make_styles(accent, light)
    hdr_row = [
        Paragraph('#', s['table_hdr']),
        Paragraph('Session Title', s['table_hdr']),
        Paragraph('Key Topics', s['table_hdr']),
        Paragraph('Deliverable', s['table_hdr']),
    ]
    rows = [hdr_row]
    for i, (title, topics, deliverable) in enumerate(sessions):
        bg = ROW_ALT if i % 2 == 0 else WHITE
        topic_str = ' · '.join(topics[:3]) + ('…' if len(topics) > 3 else '')
        rows.append([
            Paragraph(str(i+1), ParagraphStyle('cn', fontSize=8, fontName='Helvetica-Bold',
                                                textColor=accent, alignment=TA_CENTER, leading=11)),
            Paragraph(title, s['table_cell_bold']),
            Paragraph(topic_str, s['table_cell']),
            Paragraph(deliverable, s['table_cell']),
        ])

    col_w = [10*mm, 48*mm, 68*mm, 44*mm]
    t = Table(rows, colWidths=col_w, repeatRows=1)
    style = TableStyle([
        ('BACKGROUND',   (0, 0), (-1, 0), TABLE_HDR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [ROW_ALT, WHITE]),
        ('GRID',         (0, 0), (-1, -1), 0.4, colors.HexColor('#CFD8DC')),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        ('LEFTPADDING',  (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
    ])
    t.setStyle(style)
    story.append(t)
    story.append(Spacer(1, 8))


# ─── COHORT DATA ──────────────────────────────────────────────────────────────

COHORT_A = {
    'title': 'AI Interview Prep Copilot',
    'subtitle': 'Cohort A · Interview Preparation Phase (IRP)',
    'tag': 'New Age Software Engineering Program · 8 Sessions · 2 Hours Each',
    'goal': (
        'By the end of 8 sessions, students will have built a fully functional, portfolio-ready '
        'AI Interview Prep Copilot — a React web app with no backend — that they can live-demo '
        'in interviews and explain every AI decision they made, from prompt design to error handling. '
        'The app helps students prepare for job interviews using AI-powered features built feature-by-feature across all 8 sessions.'
    ),
    'overview': [
        ('Sessions', '8'),
        ('Duration per Session', '2 Hours'),
        ('Format', 'Hands-On Build'),
        ('Stack', 'React + Gemini API'),
        ('Storage', 'localStorage'),
        ('Deliverable', 'Portfolio App'),
    ],
    'audience': (
        'Students who completed the 6–7 month NASE program covering Python, AI/GenAI, prompt engineering, '
        'RAG, agents, and LangChain. They use AI coding tools (Antigravity) to build features. '
        'No strong web dev background required — all frontend is generated with AI assistance.'
    ),
    'sessions': [
        (
            'Launch HQ: Build Your AI Interview War Room',
            ['localStorage persistence', 'Form-based data entry', 'Profile form with 6 fields', 'Input validation', 'Future navigation layout'],
            'Working web app with profile form, save/load from localStorage, and layout for all 7 upcoming AI features'
        ),
        (
            'Decode Any JD: Make AI Read Jobs for You',
            ['Structured prompt engineering', 'JSON output parsing', 'App state management', 'Result card UI', 'Loading + error states'],
            'JD Analyzer section: text area → Analyze button → structured result cards (Required Skills, Responsibilities, Difficulty, Top Interview Topics)'
        ),
        (
            'Know Your Gap: AI-Powered Profile vs. JD Battle Report',
            ['Multi-context prompting', 'Reading from localStorage + app state', 'Explainable AI output', 'Match bands (Strong / Moderate / Weak)', 'Risk area identification'],
            'Match Report section: matched skills, missing skills, improvement suggestions, and interview risk areas'
        ),
        (
            'Arm Yourself: Generate 12 Targeted Interview Questions',
            ['Prompt chaining', 'Multi-source context building', 'Categorised question generation (Technical, HR, Project, Scenario)', 'Copy-per-category controls', 'Output stored for Session 5'],
            '12 interview questions across 4 collapsible categories with copy and regenerate controls'
        ),
        (
            'Practice Under Fire: Get Your Answers Scored by AI',
            ['Rubric-based AI evaluation', 'Dropdown from Session 4 output', 'Score out of 10', 'Strengths and missing points', 'Improved sample answer + follow-up question'],
            'Evaluator feature: question dropdown, answer text area, AI feedback card with score, strengths, gaps, improved answer'
        ),
        (
            'Never Get Stuck: Build a RAG-Powered Doubt Crusher',
            ['Retrieval-Augmented Generation concept', 'In-app knowledge base as JS array', 'Keyword-based retrieval', 'Grounded AI prompting', 'Source attribution display'],
            'Doubt Solver section: question input → AI answer grounded in retrieved knowledge note → source note title displayed'
        ),
        (
            'Own Your Prep: Deploy Your Personal 7-Day AI Coach',
            ['AI agent vs. chatbot distinction', 'Goal + constraint-based planning', 'Pre-filling from localStorage profile', '7-day plan with daily tasks and questions', 'Revision checklist generation'],
            '7-day prep plan with collapsible day cards (topic, 3–5 questions, 1 mock task per day) + revision checklist'
        ),
        (
            'Ship It: Polish, Test, and Nail the Demo',
            ['Loading spinners on all AI calls', 'Error messages for failed calls', 'Input validation across all forms', 'Project README with AI', 'Manual test checklist + 2-min demo script'],
            'Fully polished, error-handled, portfolio-ready AI Interview Prep Copilot with README, test checklist, and rehearsed demo'
        ),
    ],
}

COHORT_B = {
    'title': 'AI Support Ticket Resolution Copilot',
    'subtitle': 'Cohort B · Interview Preparation Phase (IRP)',
    'tag': 'New Age Software Engineering Program · 8 Sessions · 2 Hours Each',
    'goal': (
        'By the end of 8 sessions, students will have built a production-grade AI-powered backend — '
        'a FastAPI service that automatically classifies support tickets, retrieves grounded knowledge '
        'using RAG (ChromaDB + embeddings), resolves tickets through a LangGraph multi-node agent '
        'workflow, and includes auth, evals, guardrails, and deployment. Students will be able to '
        'explain every architectural decision, trade-off, and AI component in a technical interview.'
    ),
    'overview': [
        ('Sessions', '8'),
        ('Duration per Session', '2 Hours'),
        ('Format', 'Backend Build'),
        ('Stack', 'FastAPI + LangGraph'),
        ('Database', 'SQLite / PostgreSQL'),
        ('Deliverable', 'Deployed API'),
    ],
    'audience': (
        'Students who completed the 6–7 month NASE program covering Python, FastAPI, SQL, JWT auth, '
        'RAG, LangGraph, and agentic workflows. They have hands-on coding experience and use AI coding '
        'tools (Antigravity) to build features. Strong Python background; web dev experience optional.'
    ),
    'sessions': [
        (
            'Lay the Foundation: Build a Production FastAPI Backend',
            ['FastAPI + APIRouter', 'Pydantic models for request validation', 'HTTP status codes (201, 200, 204, 404)', 'In-memory storage', 'Swagger UI at /docs'],
            'FastAPI app with 5 REST endpoints: POST/GET/PATCH/DELETE /tickets, all testable via Swagger UI'
        ),
        (
            'Make Data Stick: Add a Real Database Layer',
            ['SQLModel ORM (SQLAlchemy + Pydantic)', 'SQLite file-based persistence', 'FastAPI dependency injection (get_session)', 'CRUD DB operations', 'Alembic first migration (stretch)'],
            'All 5 endpoints persisting to tickets.db; data survives server restarts'
        ),
        (
            'Lock It Down: JWT Auth + Role-Based Access Control',
            ['JWT auth with python-jose', 'bcrypt password hashing', '/auth/signup and /auth/login endpoints', 'get_current_user dependency', 'Role-scoped data access (user vs. admin)', '401 and 403 response patterns'],
            'Working auth system with JWT-protected routes, role-based guards, and unit tests for auth flows'
        ),
        (
            'Teach the Machine: Add an LLM Ticket Classifier',
            ['Gemini 1.5 Flash via google-generativeai', 'JSON mode (response_mime_type="application/json")', 'Low-temperature deterministic LLM calls', 'Graceful fallback if LLM fails', 'pytest mocking with unittest.mock.patch', 'Ollama as local alternative'],
            'llm_classifier.py service + TicketClassification DB table; POST /tickets response includes category, priority, sentiment, urgency_score, summary, suggested_team'
        ),
        (
            'Ground the AI: Build a RAG Knowledge Base',
            ['RAG: retrieval vs. generation', 'Text chunking by paragraph', 'sentence-transformers all-MiniLM-L6-v2 (384-d, local)', 'ChromaDB local persistent collection', 'Top-3 cosine similarity retrieval', 'Context injection into LLM prompt'],
            'GET /tickets/{id}/suggested-response endpoint returning suggested_response and sources; rag_service.py + ChromaDB persisted to disk'
        ),
        (
            'Build the Brain: Add a LangGraph Agent Workflow',
            ['LangGraph StateGraph with TypedDict state', '4 nodes: classify → retrieve → generate → confidence_router', 'Conditional edges on confidence_score < 0.7', 'Human-in-the-loop flag (needs_human_review)', 'Reuse of Sessions 4 and 5 functions'],
            'POST /tickets/{id}/resolve endpoint returning suggested_response, confidence_score, needs_human_review, classification; workflow in app/graph/nodes.py'
        ),
        (
            'Bulletproof It: Evals, Guardrails, and Tests',
            ['pytest with FastAPI TestClient and fixtures', 'In-memory SQLite test DB', 'Custom groundedness evaluator (string overlap or cosine)', 'System prompt guardrails (block PII leakage, off-topic)', 'Fallback response pattern', 'confidence_score from ChromaDB similarity'],
            'tests/test_tickets.py (5–8 CRUD tests), tests/test_classifier.py, app/evals/groundedness.py, guardrail logic in generate_node'
        ),
        (
            'Ship and Shine: Deploy, Demo, Ace the Interview',
            ['requirements.txt pinning via pip freeze', '.env.example documentation', 'README.md with Mermaid architecture diagram', 'Railway / Render free-tier deployment', 'Swagger UI verification on live URL', '3-minute demo script + system design Q&A'],
            'Live deployed backend on Railway/Render with Swagger UI; complete README; rehearsed 3-minute demo and system design explanation'
        ),
    ],
}

COHORT_C = {
    'title': 'AI Systems Interview Portfolio',
    'subtitle': 'Cohort C · Interview Preparation Phase (IRP)',
    'tag': 'New Age Software Engineering Program · 8 Sessions · 2 Hours Each · Gemini Free Tier',
    'goal': (
        'By the end of 8 sessions, students will have built a portfolio of 8 standalone AI engineering '
        'modules — covering structured output, LLMOps, serverless patterns, RAG, RAG evaluation, agent '
        'routing, vision/OCR, and system design — all using Gemini 1.5 Flash (free tier) and local '
        'tools (sentence-transformers, ChromaDB). Students will be able to explain every module, its '
        'trade-offs, production limitations, and design decisions confidently in AI engineering interviews. '
        'Zero cost: only a free Google AI Studio API key is required.'
    ),
    'overview': [
        ('Sessions', '8'),
        ('Duration per Session', '2 Hours'),
        ('Format', 'Portfolio Modules'),
        ('LLM', 'Gemini 1.5 Flash'),
        ('Cost', 'Free Tier'),
        ('Deliverable', '8 Python Modules'),
    ],
    'audience': (
        'Students who completed the 6–7 month NASE program covering Python, GenAI, prompt engineering, '
        'RAG, LLMOps, agents, and LangGraph. They use AI coding tools (Antigravity). '
        'No web dev background required — all deliverables are Python scripts or notebooks. '
        'Only requirement: free Gemini API key from aistudio.google.com.'
    ),
    'sessions': [
        (
            'Tame the Chaos: Build a Structured Output Engine',
            ['System prompts with JSON schema definitions', 'response_mime_type="application/json"', 'Temperature = 0 for deterministic output', 'Free-text vs. structured output comparison', 'Token count logging'],
            'structured_output_engine.py + output_examples.json'
        ),
        (
            'Watch Every Call: Build Your LLM Observatory',
            ['log_llm_call() wrapper pattern', 'Latency measurement with time.time()', 'Token + cost estimation', 'Manual quality scoring (1–5)', 'CSV + JSON flat file output', 'print_report() pass/fail stats'],
            'llm_logger.py + llm_logs.csv + eval_summary.json'
        ),
        (
            'Think Serverless: Wrap AI in a Cloud-Ready Function',
            ['handler(event, context) pattern', 'Input validation + structured JSON response', 'Cold start concept', 'Cost-per-invocation thinking', 'Environment variable management with python-dotenv'],
            'ai_handler.py + .env.example'
        ),
        (
            'Build the Memory: Engineer a RAG Pipeline from Scratch',
            ['Embeddings with sentence-transformers (all-MiniLM-L6-v2, local)', 'Paragraph-level chunking', 'ChromaDB persistent local collection', 'Top-3 chunk retrieval', 'Grounded generation vs. vanilla LLM comparison'],
            'rag_pipeline.py + chroma_db/ (local persistent)'
        ),
        (
            'Grade the Brain: Evaluate and Improve Your RAG System',
            ['Groundedness and faithfulness concepts', 'Keyword-overlap relevance scoring', 'Per-question tracking (query, retrieved chunks, answer, expected, scores)', 'Before/after comparison with one changed parameter', 'RAG failure mode articulation'],
            'rag_evaluator.py + rag_eval_report.csv'
        ),
        (
            'Route with Intent: Build an Agent That Picks Its Tools',
            ['Agent vs. chatbot distinction', 'Intent classification with Gemini (structured JSON)', '4 tool functions: rag_answer(), summarize_text(), safety_check(), ask_clarification()', 'route(query) orchestrator', 'Reasoning trace: Intent → Tool → Result'],
            'agent_router.py'
        ),
        (
            'See and Understand: Give Your AI Eyes with Vision/OCR',
            ['Vision-language model vs. traditional OCR', 'Multimodal prompting with PIL.Image', 'Structured JSON extraction: extracted_text, document_type, key_fields, confidence_notes', 'Human verification importance', 'Same API key, same model, no extra cost'],
            'vision_ocr_module.py + sample_image.png + ocr_output.json'
        ),
        (
            'Tell the Story: System Design, Demo, and Interview Ready',
            ['Portfolio README and Mermaid architecture diagrams', 'Interview vocabulary: latency, throughput, cost, hallucination rate', 'Production trade-off articulation per module', 'Safety topics: prompt injection, PII, hallucination', '2-minute spoken demo structuring'],
            'README.md + architecture_diagram.md + demo_script.md + viva_prep.md + module_summary.md'
        ),
    ],
}


# ─── PDF GENERATOR ────────────────────────────────────────────────────────────

def build_pdf(cohort_data, output_path, accent, light):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=18*mm, bottomMargin=18*mm,
        leftMargin=20*mm, rightMargin=20*mm,
    )
    s = make_styles(accent, light)
    story = []

    # ── Cover banner
    cover_block(story, cohort_data['title'], cohort_data['subtitle'], cohort_data['tag'], accent, light)
    story.append(Spacer(1, 6))

    # ── Overview chips
    overview_block(story, cohort_data['overview'], accent, light)

    # ── Audience
    story.append(Paragraph('Target Audience', s['section_heading']))
    story.append(HRFlowable(width='100%', thickness=1, color=accent, spaceAfter=6))
    story.append(Paragraph(cohort_data['audience'], s['body']))
    story.append(Spacer(1, 6))

    # ── End Goal
    story.append(Paragraph('Program End Goal', s['section_heading']))
    story.append(HRFlowable(width='100%', thickness=1, color=accent, spaceAfter=6))
    goal_block(story, cohort_data['goal'], accent, light)

    # ── Session Details
    story.append(Paragraph('Session-by-Session Breakdown', s['section_heading']))
    story.append(HRFlowable(width='100%', thickness=1, color=accent, spaceAfter=8))

    for i, (title, topics, deliverable) in enumerate(cohort_data['sessions']):
        session_card(story, i+1, title, topics, deliverable, accent, light)

    # ── Summary Table
    story.append(PageBreak())
    story.append(Paragraph('Quick-Reference Summary Table', s['section_heading']))
    story.append(HRFlowable(width='100%', thickness=1, color=accent, spaceAfter=8))
    summary_table(story, cohort_data['sessions'], accent, light)

    # ── Footer note
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        '<i>New Age Software Engineering Program · Interview Preparation Phase (IRP-NASE) · '
        '8 Sessions × 2 Hours · All content generated for instructional use.</i>',
        ParagraphStyle('footer', fontSize=7.5, textColor=MID_GREY, fontName='Helvetica-Oblique',
                       leading=11, alignment=TA_CENTER)
    ))

    doc.build(story)
    print(f'Generated: {output_path}')


# ─── RUN ──────────────────────────────────────────────────────────────────────

BASE = '/Users/bickydutta/IRP - NASE'

build_pdf(COHORT_A, f'{BASE}/Cohort_A_Syllabus.pdf', ACCENT_BLUE, LIGHT_BLUE)
build_pdf(COHORT_B, f'{BASE}/Cohort_B_Syllabus.pdf', ACCENT_TEAL, LIGHT_TEAL)
build_pdf(COHORT_C, f'{BASE}/Cohort_C_Syllabus.pdf', ACCENT_PURPLE, LIGHT_PURPLE)

print('\nAll 3 syllabi generated successfully.')
