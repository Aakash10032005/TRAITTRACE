from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import os

os.makedirs('submission', exist_ok=True)

doc = SimpleDocTemplate('submission/TraitTrace_Pitch_Deck.pdf',
    pagesize=landscape(A4), leftMargin=18*mm, rightMargin=18*mm,
    topMargin=14*mm, bottomMargin=14*mm)

RED   = colors.HexColor('#b91c1c')
INK   = colors.HexColor('#1c1d1f')
CREAM = colors.HexColor('#faf7f0')
SLATE = colors.HexColor('#64748b')
BORD  = colors.HexColor('#d4c5ab')
WHITE = colors.white

styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, parent=styles['Normal'], **kw)

RM   = S('RM',  fontName='Courier-Bold', fontSize=9,  textColor=RED,   spaceAfter=2)
H1   = S('H1',  fontName='Courier-Bold', fontSize=26, textColor=INK,   spaceAfter=6, leading=30)
RH1  = S('RH1', fontName='Courier-Bold', fontSize=30, textColor=RED,   spaceAfter=8, leading=34)
H2   = S('H2',  fontName='Courier-Bold', fontSize=15, textColor=INK,   spaceAfter=4, leading=18)
H3   = S('H3',  fontName='Courier-Bold', fontSize=11, textColor=INK,   spaceAfter=3)
BD   = S('BD',  fontName='Helvetica',    fontSize=10, textColor=colors.HexColor('#3a3a3a'), spaceAfter=4, leading=14)
SM   = S('SM',  fontName='Courier',      fontSize=8,  textColor=SLATE, spaceAfter=2)

def tbl_style(header_bg=INK):
    return TableStyle([
        ('BACKGROUND',  (0,0), (-1,0), header_bg),
        ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
        ('FONTNAME',    (0,0), (-1,0), 'Courier-Bold'),
        ('FONTSIZE',    (0,0), (-1,0), 9),
        ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',    (0,1), (-1,-1), 9),
        ('GRID',        (0,0), (-1,-1), 0.5, BORD),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, WHITE]),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING',  (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ])

def hr(): return HRFlowable(width='100%', thickness=0.5, color=BORD, spaceAfter=14)
def rhr(): return HRFlowable(width='100%', thickness=2, color=RED, spaceAfter=8)

story = []

# ── SLIDE 1: TITLE ──────────────────────────────────────────────────────────
story += [
    Paragraph('EPSILON TEXPEDITION HACKATHON', RM),
    Spacer(1, 4*mm),
    Paragraph('TraitTrace', RH1),
    Paragraph('Privacy-First Cookie-less Personalization via Zero-Party Knowledge Graphs', H1),
    Spacer(1, 4*mm),
    rhr(),
    Paragraph('FastAPI  |  NetworkX  |  Groq Llama 3.1 8B  |  Next.js 14  |  Framer Motion  |  react-force-graph-2d', SM),
    Spacer(1, 3*mm),
    Paragraph('github.com/Aakash10032005/TRAITTRACE', SM),
    hr(), PageBreak(),
]

# ── SLIDE 2: THE PROBLEM ────────────────────────────────────────────────────
story += [
    Paragraph('01 // THE PROBLEM', RM),
    Paragraph('Cookies are dying. Marketers are blind.', H1),
    Spacer(1, 3*mm),
]
problems = [
    ['Challenge', 'Impact on Marketers'],
    ['GDPR / CCPA regulations', 'Third-party data collection legally restricted'],
    ["Apple App Tracking Transparency", 'Cross-app tracking blocked by default on iOS'],
    ["Google Privacy Sandbox", 'Third-party cookies deprecated in Chrome'],
    ['Browser tracker blockers', 'Safari ITP and Firefox ETP block most tracking pixels'],
]
t = Table(problems, colWidths=[120*mm, 140*mm])
t.setStyle(tbl_style())
story += [t, Spacer(1, 4*mm),
    Paragraph('Critical question: How do we serve personalized experiences WITHOUT invading user privacy?', H3),
    hr(), PageBreak(),
]

# ── SLIDE 3: SOLUTION ───────────────────────────────────────────────────────
story += [
    Paragraph('02 // OUR SOLUTION', RM),
    Paragraph('TraitTrace: Explicit Consent. Zero Cookies. Full Personalization.', H2),
    Spacer(1, 2*mm),
]
for label, desc in [
    ('01  INTAKE INDEX CARDS', 'Consumer interacts with a gamified physical-styled swipe card deck to explicitly declare visual, pricing, and lifestyle preferences. No guessing, no tracking.'),
    ('02  IN-MEMORY KNOWLEDGE GRAPH', 'Every swipe is mapped into a session-isolated NetworkX DiGraph on the backend. Builds a real-time behavioral graph path, ephemeral by design — zero persistence.'),
    ('03  GROQ LLAMA 3.1 INFERENCE', 'Graph-text compiler translates paths into a semantic prompt queried through llama-3.1-8b-instant. Returns hyper-personalized storefront copy in under 150ms.'),
    ('04  MARKETPLACE RE-ROUTING', 'Tailored smartwatch recommendations rendered from the synthesized profile with direct checkout links to Amazon.in, Flipkart, and Google Shop.'),
]:
    story += [Paragraph(f'<font color="#b91c1c"><b>{label}</b></font>', H3), Paragraph(desc, BD), Spacer(1, 2*mm)]
story += [hr(), PageBreak()]

# ── SLIDE 4: ARCHITECTURE ───────────────────────────────────────────────────
story += [
    Paragraph('03 // TECHNICAL ARCHITECTURE', RM),
    Paragraph('End-to-End Ephemeral Data Flow', H2),
    Spacer(1, 3*mm),
]
arch = [
    ['Layer', 'Technology', 'Role'],
    ['Frontend UI',       'Next.js 14 App Router + TypeScript',  'Gamified swipe cards, split-screen dual interface'],
    ['Animations',        'Framer Motion',                       'Drag gestures, card transitions, indicator overlays'],
    ['API Transport',     'FastAPI POST /api/interact',          'Receives session UUID + trait value per swipe'],
    ['Graph Engine',      'NetworkX DiGraph (in-memory)',        'Session-isolated trait graph, zero persistence'],
    ['LLM Inference',     'Groq llama-3.1-8b-instant',          'Graph paths to structured JSON persona, <150ms'],
    ['Graph Visualizer',  'react-force-graph-2d',                'Live 2D force-directed graph, marketer dashboard'],
    ['Validation',        'Pydantic v2 + FastAPI models',        'Schema enforcement on all I/O payloads'],
]
t2 = Table(arch, colWidths=[48*mm, 72*mm, 140*mm])
t2.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0), INK),
    ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
    ('FONTNAME',    (0,0), (-1,0), 'Courier-Bold'),
    ('FONTSIZE',    (0,0), (-1,0), 9),
    ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE',    (0,1), (-1,-1), 9),
    ('GRID',        (0,0), (-1,-1), 0.5, BORD),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, WHITE]),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING',  (0,0), (-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ('TEXTCOLOR',   (0,1), (0,-1), RED),
    ('FONTNAME',    (0,1), (0,-1), 'Courier-Bold'),
]))
story += [t2, hr(), PageBreak()]

# ── SLIDE 5: PRIVACY ────────────────────────────────────────────────────────
story += [
    Paragraph('04 // PRIVACY ARCHITECTURE', RM),
    Paragraph('Zero-Party by Design. No Compromises.', H2),
    Spacer(1, 3*mm),
]
privacy = [
    ['Privacy Principle',   'Implementation Detail',                     'Verifiable Outcome'],
    ['No Cookies',          'Session ID travels in JSON body only',       'Browser writes zero tracking cookies'],
    ['Ephemeral State',     'NetworkX graph lives in RAM only',           'Process restart = complete data wipe'],
    ['Zero-Party Data',     'User explicitly declares all preferences',   'GDPR Article 6 legitimate interest basis'],
    ['No Persistent DB',    'No SQL, no Redis, no cloud object store',    'Nothing to subpoena, nothing to breach'],
    ['Session Isolation',   'UUID per page load, never persisted',        'Zero cross-session user linkage possible'],
    ['Open Weights LLM',    'Groq Llama 3.1 (open-source model)',         'No OpenAI black-box data retention risk'],
]
tp = Table(privacy, colWidths=[52*mm, 94*mm, 110*mm])
tp.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0), RED),
    ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
    ('FONTNAME',    (0,0), (-1,0), 'Courier-Bold'),
    ('FONTSIZE',    (0,0), (-1,0), 9),
    ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE',    (0,1), (-1,-1), 9),
    ('GRID',        (0,0), (-1,-1), 0.5, BORD),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, WHITE]),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING',  (0,0), (-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ('TEXTCOLOR',   (0,1), (0,-1), RED),
    ('FONTNAME',    (0,1), (0,-1), 'Courier-Bold'),
]))
story += [tp, hr(), PageBreak()]

# ── SLIDE 6: UI DESIGN ──────────────────────────────────────────────────────
story += [
    Paragraph('05 // INTERFACE DESIGN CONCEPT', RM),
    Paragraph('A Dual-Concept Split Screen', H2),
    Spacer(1, 3*mm),
]
ui = [
    ['THE MANILA FOLDER (Left Panel)', 'THE CONTROL ROOM (Right Panel)'],
    ['Warm kraft card-stock aesthetic. The consumer\'s readable case file. Explicit zero-party consent UI.',
     'Inverted near-black marketer dashboard. Live 2D force-directed knowledge graph + API log feed.'],
    ['Framer Motion swipe gesture cards\n4 trait-profiling index cards (Aesthetic, Value, Budget, Habit)\nDynamic Groq-generated hero copy\nSmart product recommendation card\nMarketplace checkout links',
     'react-force-graph-2d live visualization\nReal-time node/edge counter\nTypewriter-style console log feed\nCategory color legend\nEphemeral session state badge'],
]
tc = Table(ui, colWidths=[130*mm, 130*mm])
tc.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (0,0), colors.HexColor('#faf7f0')),
    ('BACKGROUND',  (1,0), (1,0), colors.HexColor('#17181a')),
    ('TEXTCOLOR',   (1,0), (1,2), WHITE),
    ('FONTNAME',    (0,0), (-1,0), 'Courier-Bold'),
    ('FONTSIZE',    (0,0), (-1,0), 10),
    ('FONTNAME',    (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE',    (0,1), (-1,-1), 9),
    ('VALIGN',      (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING',(0,0), (-1,-1), 10),
    ('TOPPADDING',  (0,0), (-1,-1), 8),
    ('BOTTOMPADDING',(0,0),(-1,-1), 8),
    ('LINEAFTER',   (0,0), (0,-1), 1, BORD),
    ('GRID',        (0,0), (-1,-1), 0.5, BORD),
]))
story += [tc, hr(), PageBreak()]

# ── SLIDE 7: TESTS ──────────────────────────────────────────────────────────
story += [
    Paragraph('06 // TESTING & RELIABILITY', RM),
    Paragraph('4/4 Tests Passing. 100% Critical Path Coverage.', H2),
    Spacer(1, 3*mm),
]
tests = [
    ['Test Name',                                    'Validates',                              'Result'],
    ['test_graph_manager_path_creation',             'Node/edge creation, path string output', 'PASS'],
    ['test_interact_endpoint_success',               'Groq mock returns correct persona JSON', 'PASS'],
    ['test_interact_endpoint_groq_failure_fallback', 'API error gracefully falls to default',  'PASS'],
    ['test_interact_endpoint_invalid_json_fallback', 'Malformed LLM output handled cleanly',   'PASS'],
]
tt = Table(tests, colWidths=[100*mm, 120*mm, 40*mm])
tt.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0), INK),
    ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
    ('FONTNAME',    (0,0), (-1,0), 'Courier-Bold'),
    ('FONTSIZE',    (0,0), (-1,0), 9),
    ('FONTNAME',    (0,1), (-1,-1), 'Courier'),
    ('FONTSIZE',    (0,1), (-1,-1), 9),
    ('GRID',        (0,0), (-1,-1), 0.5, BORD),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, WHITE]),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING',  (0,0), (-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ('TEXTCOLOR',   (0,1), (-1,-1), colors.HexColor('#166534')),
    ('FONTNAME',    (-1,1), (-1,-1), 'Courier-Bold'),
    ('BACKGROUND',  (-1,1), (-1,-1), colors.HexColor('#f0fdf4')),
]))
story += [tt, Spacer(1, 4*mm),
    Paragraph('Run from project root with venv active:  python -m pytest', BD),
    hr(), PageBreak(),
]

# ── SLIDE 8: HOW TO RUN ─────────────────────────────────────────────────────
story += [
    Paragraph('07 // INSTRUCTIONS TO RUN', RM),
    Paragraph('Up and Running in 4 Steps', H2),
    Spacer(1, 3*mm),
]
run_steps = [
    ['Step', 'Command / Action', 'Notes'],
    ['1. API Key',   'Create .env in project root: GROQ_API_KEY=gsk_...',  'Free key at console.groq.com'],
    ['2. Backend',   'cd backend  then  uvicorn main:app --reload --port 8000', 'Verify: localhost:8000/health'],
    ['3. Frontend',  'cd frontend  then  npm install  then  npm run dev',        'Open: localhost:3000'],
    ['4. Tests',     'python -m pytest  (from project root, venv active)',        '4/4 pass expected'],
]
ts2 = Table(run_steps, colWidths=[28*mm, 140*mm, 92*mm])
ts2.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0), INK),
    ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
    ('FONTNAME',    (0,0), (-1,0), 'Courier-Bold'),
    ('FONTSIZE',    (0,0), (-1,0), 9),
    ('FONTNAME',    (0,1), (-1,-1), 'Courier'),
    ('FONTSIZE',    (0,1), (-1,-1), 9),
    ('GRID',        (0,0), (-1,-1), 0.5, BORD),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, WHITE]),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING',  (0,0), (-1,-1), 6),
    ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ('TEXTCOLOR',   (0,1), (0,-1), RED),
    ('FONTNAME',    (0,1), (0,-1), 'Courier-Bold'),
]))
story += [ts2, hr(), PageBreak()]

# ── SLIDE 9: CLOSING ────────────────────────────────────────────────────────
story += [
    Spacer(1, 10*mm),
    Paragraph('TraitTrace', RH1),
    Paragraph('The future of personalization is explicit, ephemeral, and earned.', H1),
    Spacer(1, 6*mm),
    rhr(),
    Spacer(1, 4*mm),
    Paragraph('Repository:   github.com/Aakash10032005/TRAITTRACE', SM),
    Paragraph('Stack:        FastAPI + NetworkX + Groq Llama 3.1 + Next.js 14', SM),
    Paragraph('Hackathon:    Epsilon TeXpedition 2024', SM),
]

doc.build(story)
print("PDF saved: submission/TraitTrace_Pitch_Deck.pdf")
