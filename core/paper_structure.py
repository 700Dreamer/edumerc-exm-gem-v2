"""
UNEB / National Exam Paper Structure Registry
Maps each Subject + Level combination to the actual paper structure
used in Uganda's national examinations (PLE, UCE, UACE).

Sources: UNEB official specimen papers and past papers.
"""

from typing import Optional

# ─── PAPER STRUCTURE DEFINITION ────────────────────────────────────────────
# Each entry:
#   "sec_a_count": int   — number of objective/short-answer questions
#   "sec_a_marks": int   — marks for section A
#   "sec_b_count": int   — number of structured/essay questions
#   "sec_b_marks": int   — marks for section B
#   "total_marks": int
#   "duration":    str   — e.g. "2 HRS 30 MIN"
#   "description": str   — official paper name

PAPER_STRUCTURES = {

    # ─── PRIMARY LEAVING EXAMINATION (PLE) ───────────────────────────────
    ("Mathematics", "Primary 7"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Mathematics Paper 1 (PLE)",
        "sec_b_note": "Answer all 5 questions in Section B (structured)"
    },
    ("Science", "Primary 7"): {
        "sec_a_count": 40, "sec_a_marks": 40,
        "sec_b_count": 10, "sec_b_marks": 60,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Science Paper (PLE)",
        "sec_b_note": "Answer 10 questions in Section B"
    },
    ("English", "Primary 7"): {
        "sec_a_count": 50, "sec_a_marks": 50,
        "sec_b_count": 5,  "sec_b_marks": 50,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "English Language Paper (PLE)",
        "sec_b_note": "Section B: Composition, Letter Writing, Comprehension"
    },
    ("Social Studies", "Primary 7"): {
        "sec_a_count": 40, "sec_a_marks": 40,
        "sec_b_count": 15, "sec_b_marks": 60,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Social Studies / Religious Education (PLE)",
        "sec_b_note": "Answer 15 questions in Section B"
    },
    ("Religious Education", "Primary 7"): {
        "sec_a_count": 40, "sec_a_marks": 40,
        "sec_b_count": 15, "sec_b_marks": 60,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Social Studies / Religious Education (PLE)",
        "sec_b_note": "Answer 15 questions in Section B"
    },

    # ─── LOWER PRIMARY (Internal / Promotional) ───────────────────────────
    ("Mathematics", "Primary 1"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 30,
        "total_marks": 50,  "duration": "1 HR 30 MIN",
        "description": "Mathematics Promotional Examination",
    },
    ("Mathematics", "Primary 2"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 30,
        "total_marks": 50,  "duration": "1 HR 30 MIN",
        "description": "Mathematics Promotional Examination",
    },
    ("Mathematics", "Primary 3"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 30,
        "total_marks": 50,  "duration": "1 HR 30 MIN",
        "description": "Mathematics Promotional Examination",
    },
    ("Mathematics", "Primary 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 40,
        "total_marks": 60,  "duration": "2 HRS",
        "description": "Mathematics Promotional Examination",
    },
    ("Mathematics", "Primary 5"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 40,
        "total_marks": 60,  "duration": "2 HRS",
        "description": "Mathematics Promotional Examination",
    },
    ("Mathematics", "Primary 6"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 40,
        "total_marks": 60,  "duration": "2 HRS",
        "description": "Mathematics Promotional Examination",
    },
    ("Social Studies", "Primary 6"): {
        "sec_a_count": 40, "sec_a_marks": 40,
        "sec_b_count": 10, "sec_b_marks": 40,
        "total_marks": 80,  "duration": "2 HRS",
        "description": "Social Studies Promotional Examination",
    },
    ("Social Studies", "Primary 5"): {
        "sec_a_count": 30, "sec_a_marks": 30,
        "sec_b_count": 10, "sec_b_marks": 40,
        "total_marks": 70,  "duration": "2 HRS",
        "description": "Social Studies Promotional Examination",
    },
    ("Social Studies", "Primary 4"): {
        "sec_a_count": 30, "sec_a_marks": 30,
        "sec_b_count": 10, "sec_b_marks": 40,
        "total_marks": 70,  "duration": "1 HR 30 MIN",
        "description": "Social Studies Promotional Examination",
    },
    ("Science", "Primary 6"): {
        "sec_a_count": 40, "sec_a_marks": 40,
        "sec_b_count": 10, "sec_b_marks": 40,
        "total_marks": 80,  "duration": "2 HRS",
        "description": "Science Promotional Examination",
    },
    ("English", "Primary 6"): {
        "sec_a_count": 30, "sec_a_marks": 30,
        "sec_b_count": 5,  "sec_b_marks": 40,
        "total_marks": 70,  "duration": "2 HRS",
        "description": "English Language Promotional Examination",
    },

    # ─── UGANDA CERTIFICATE OF EDUCATION (UCE / O-Level New Curriculum) ────
    ("Mathematics", "Senior 4"): {
        "sec_a_count": 0, "sec_a_marks": 0,
        "sec_b_count": 3, "sec_b_marks": 50,
        "total_marks": 50, "duration": "1 ½ HR",
        "description": "Mathematics UCE Competency Assessment",
        "sec_b_note": "Respond to only two items."
    },
    ("Physics", "Senior 4"): {
        "sec_a_count": 0, "sec_a_marks": 0,
        "sec_b_count": 3, "sec_b_marks": 50,
        "total_marks": 50, "duration": "1 ½ HR",
        "description": "Physics UCE Competency Assessment",
        "sec_b_note": "Respond to only two items."
    },
    ("Chemistry", "Senior 4"): {
        "sec_a_count": 0, "sec_a_marks": 0,
        "sec_b_count": 3, "sec_b_marks": 50,
        "total_marks": 50, "duration": "1 ½ HR",
        "description": "Chemistry UCE Competency Assessment",
        "sec_b_note": "Respond to only two items."
    },
    ("Biology", "Senior 4"): {
        "sec_a_count": 0, "sec_a_marks": 0,
        "sec_b_count": 3, "sec_b_marks": 50,
        "total_marks": 50, "duration": "1 ½ HR",
        "description": "Biology UCE Competency Assessment",
        "sec_b_note": "Respond to only two items."
    },
    ("English", "Senior 4"): {
        "sec_a_count": 0, "sec_a_marks": 0,
        "sec_b_count": 3, "sec_b_marks": 50,
        "total_marks": 50, "duration": "1 ½ HR",
        "description": "English Language UCE Competency Assessment",
        "sec_b_note": "Attempt all items."
    },

    # ─── UACE (A-Level) ───────────────────────────────────────────────────
    ("Mathematics", "Senior 6"): {
        "sec_a_count": 0,  "sec_a_marks": 0,
        "sec_b_count": 15, "sec_b_marks": 150,
        "total_marks": 150, "duration": "3 HRS",
        "description": "Mathematics UACE Paper (Pure & Applied)",
        "sec_b_note": "Answer 5 compulsory questions + choose from optional sections"
    },
    ("Physics", "Senior 6"): {
        "sec_a_count": 0,  "sec_a_marks": 0,
        "sec_b_count": 8,  "sec_b_marks": 100,
        "total_marks": 100, "duration": "3 HRS",
        "description": "Physics UACE Paper",
        "sec_b_note": "Answer any 5 questions"
    },

    # ─── GEOGRAPHY ────────────────────────────────────────────────────────
    ("Geography", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Geography UCE Paper",
        "sec_b_note": "Answer any 6 questions in Section B"
    },
    ("Geography", "Senior 6"): {
        "sec_a_count": 0,  "sec_a_marks": 0,
        "sec_b_count": 8,  "sec_b_marks": 100,
        "total_marks": 100, "duration": "3 HRS",
        "description": "Geography UACE Paper",
        "sec_b_note": "Answer any 5 questions"
    },

    # ─── HISTORY ──────────────────────────────────────────────────────────
    ("History", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "History UCE Paper",
        "sec_b_note": "Answer any 6 essay questions in Section B"
    },
    ("History", "Senior 6"): {
        "sec_a_count": 0,  "sec_a_marks": 0,
        "sec_b_count": 8,  "sec_b_marks": 100,
        "total_marks": 100, "duration": "3 HRS",
        "description": "History UACE Paper",
        "sec_b_note": "Answer any 5 questions"
    },

    # ─── COMMERCE ─────────────────────────────────────────────────────────
    ("Commerce", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Commerce UCE Paper",
        "sec_b_note": "Answer any 6 questions in Section B"
    },

    # ─── ACCOUNTING ───────────────────────────────────────────────────────
    ("Accounting", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Accounting UCE Paper",
        "sec_b_note": "Answer any 6 questions in Section B"
    },
    ("Accounting", "Senior 6"): {
        "sec_a_count": 0,  "sec_a_marks": 0,
        "sec_b_count": 8,  "sec_b_marks": 100,
        "total_marks": 100, "duration": "3 HRS",
        "description": "Accounting UACE Paper",
        "sec_b_note": "Answer any 5 questions"
    },

    # ─── ECONOMICS ────────────────────────────────────────────────────────
    ("Economics", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Economics UCE Paper",
        "sec_b_note": "Answer any 6 questions in Section B"
    },
    ("Economics", "Senior 6"): {
        "sec_a_count": 0,  "sec_a_marks": 0,
        "sec_b_count": 8,  "sec_b_marks": 100,
        "total_marks": 100, "duration": "3 HRS",
        "description": "Economics UACE Paper",
        "sec_b_note": "Answer any 5 questions"
    },

    # ─── AGRICULTURE ──────────────────────────────────────────────────────
    ("Agriculture", "Primary 7"): {
        "sec_a_count": 30, "sec_a_marks": 30,
        "sec_b_count": 10, "sec_b_marks": 40,
        "total_marks": 70,  "duration": "2 HRS",
        "description": "Agriculture Promotional Examination (PLE)"
    },
    ("Agriculture", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Agriculture UCE Paper",
        "sec_b_note": "Answer any 6 questions in Section B"
    },

    # ─── ICT ──────────────────────────────────────────────────────────────
    ("ICT", "Primary 7"): {
        "sec_a_count": 30, "sec_a_marks": 30,
        "sec_b_count": 10, "sec_b_marks": 40,
        "total_marks": 70,  "duration": "2 HRS",
        "description": "ICT Promotional Examination"
    },
    ("ICT", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "ICT UCE Paper",
        "sec_b_note": "Answer any 6 questions in Section B"
    },

    # ─── CHRISTIAN RELIGIOUS EDUCATION ────────────────────────────────────
    ("Christian Religious Education", "Primary 7"): {
        "sec_a_count": 40, "sec_a_marks": 40,
        "sec_b_count": 15, "sec_b_marks": 60,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "CRE Paper (PLE)",
        "sec_b_note": "Answer 15 questions in Section B"
    },
    ("Christian Religious Education", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "CRE UCE Paper",
        "sec_b_note": "Answer any 6 essay questions"
    },

    # ─── ISLAMIC RELIGIOUS EDUCATION ──────────────────────────────────────
    ("Islamic Religious Education", "Primary 7"): {
        "sec_a_count": 40, "sec_a_marks": 40,
        "sec_b_count": 15, "sec_b_marks": 60,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "IRE Paper (PLE)",
        "sec_b_note": "Answer 15 questions in Section B"
    },
    ("Islamic Religious Education", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "IRE UCE Paper",
        "sec_b_note": "Answer any 6 essay questions"
    },

    # ─── LITERATURE IN ENGLISH ────────────────────────────────────────────
    ("Literature in English", "Senior 4"): {
        "sec_a_count": 0,  "sec_a_marks": 0,
        "sec_b_count": 8,  "sec_b_marks": 100,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Literature in English UCE Paper",
        "sec_b_note": "Answer 4 questions, at least one from each section"
    },
    ("Literature in English", "Senior 6"): {
        "sec_a_count": 0,  "sec_a_marks": 0,
        "sec_b_count": 8,  "sec_b_marks": 100,
        "total_marks": 100, "duration": "3 HRS",
        "description": "Literature in English UACE Paper",
        "sec_b_note": "Answer any 4 questions"
    },

    # ─── FRENCH ───────────────────────────────────────────────────────────
    ("French", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "French UCE Paper",
        "sec_b_note": "Section B: Comprehension, Translation, Composition"
    },

    # ─── KISWAHILI ────────────────────────────────────────────────────────
    ("Kiswahili", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Kiswahili UCE Paper",
        "sec_b_note": "Section B: Ufahamu, Insha, Sarufi"
    },

    # ─── HOME ECONOMICS ───────────────────────────────────────────────────
    ("Home Economics", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Home Economics UCE Paper",
        "sec_b_note": "Answer any 6 questions in Section B"
    },

    # ─── FINE ART ─────────────────────────────────────────────────────────
    ("Fine Art", "Senior 4"): {
        "sec_a_count": 10, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Fine Art UCE Theory Paper",
        "sec_b_note": "Answer any 4 questions in Section B"
    },

    # ─── MUSIC ────────────────────────────────────────────────────────────
    ("Music", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Music UCE Theory Paper",
        "sec_b_note": "Answer any 4 questions in Section B"
    },

    # ─── TECHNICAL DRAWING ────────────────────────────────────────────────
    ("Technical Drawing", "Senior 4"): {
        "sec_a_count": 10, "sec_a_marks": 20,
        "sec_b_count": 5,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "3 HRS",
        "description": "Technical Drawing UCE Paper",
        "sec_b_note": "Answer any 4 questions requiring drawn solutions"
    },

    # ─── ENTREPRENEURSHIP EDUCATION ───────────────────────────────────────
    ("Entrepreneurship Education", "Senior 4"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 8,  "sec_b_marks": 80,
        "total_marks": 100, "duration": "2 HRS 30 MIN",
        "description": "Entrepreneurship Education UCE Paper",
        "sec_b_note": "Answer any 6 questions in Section B"
    },

    # ─── ECD (Internal Assessment) ───────────────────────────────
    ("ECD", "Baby Class"): {
        "sec_a_count": 10, "sec_a_marks": 10,
        "sec_b_count": 0,  "sec_b_marks": 0,
        "total_marks": 10,  "duration": "30 MIN",
        "description": "Baby Class Internal Assessment"
    },
    ("ECD", "Middle Class"): {
        "sec_a_count": 15, "sec_a_marks": 15,
        "sec_b_count": 0,  "sec_b_marks": 0,
        "total_marks": 15,  "duration": "45 MIN",
        "description": "Middle Class Internal Assessment"
    },
    ("ECD", "Top Class"): {
        "sec_a_count": 20, "sec_a_marks": 20,
        "sec_b_count": 0,  "sec_b_marks": 0,
        "total_marks": 20,  "duration": "1 HR",
        "description": "Top Class Internal Assessment"
    },
}

# ─── DEFAULT (fallback for unlisted combinations) ─────────────────────────
DEFAULT_STRUCTURE = {
    "sec_a_count": 40, "sec_a_marks": 40,
    "sec_b_count": 15, "sec_b_marks": 60,
    "total_marks": 100, "duration": "2 HRS 30 MIN",
    "description": "Standard Examination Paper",
}


def get_paper_structure(subject: str, level: str) -> dict:
    """Returns the official UNEB paper structure for the given subject/level."""
    s_clean = subject
    if "english" in str(subject).lower():
        s_clean = "English"
    elif "science" in str(subject).lower():
        s_clean = "Science"
    elif "social" in str(subject).lower() or "sst" in str(subject).lower():
        s_clean = "Social Studies"
    elif "math" in str(subject).lower():
        s_clean = "Mathematics"

    # Intercept ECD levels regardless of subject to enforce single-section ECD format
    if level in ["Baby Class", "Middle Class", "Top Class"]:
        return PAPER_STRUCTURES.get(("ECD", level))
        
    structure = PAPER_STRUCTURES.get((s_clean, level)) or PAPER_STRUCTURES.get((subject, level))
    if structure:
        return structure
        
    # Provide a sane fallback for Lower Primary (P1-P3) to avoid huge 55-question exams
    if level in ["Primary 1", "Primary 2", "Primary 3"]:
        return {
            "sec_a_count": 20, "sec_a_marks": 20,
            "sec_b_count": 5,  "sec_b_marks": 30,
            "total_marks": 50,  "duration": "1 HR 30 MIN",
            "description": f"{subject} Lower Primary Assessment"
        }
        
    # Provide sane structure for Lower Secondary (Senior 1-4 Competency Assessments)
    if any(s in str(level) for s in ["Senior 1", "Senior 2", "Senior 3", "Senior 4", "S.1", "S.2", "S.3", "S.4"]):
        return {
            "sec_a_count": 0, "sec_a_marks": 0,
            "sec_b_count": 3, "sec_b_marks": 50,
            "total_marks": 50, "duration": "1 ½ HR",
            "description": f"{subject} UCE Competency Assessment",
            "sec_b_note": "Respond to only two items."
        }

    return DEFAULT_STRUCTURE


def get_total_questions(subject: str, level: str) -> int:
    """Returns the official total question count (A + B) for the paper."""
    s = get_paper_structure(subject, level)
    return s["sec_a_count"] + s["sec_b_count"]


# ─── SUBJECT COMPETENCY BLUEPRINTS (NCDC / UNEB GUIDES) ──────────────────────
SUBJECT_COMPETENCY_BLUEPRINTS = {
    "Physics": {
        "persona_role": "Task:",
        "support_type": "Given numerical parameters, physical constants (e.g. initial velocity, mass, braking deceleration, apparent depth), motion graphs, apparatus diagrams.",
        "cognitive_progression": [
            "(a) Quantitative calculation or direct physical law determination (3 marks)",
            "(b) Physical mechanism explanation or principle evaluation (4 marks)",
            "(c) Energy loss, efficiency calculation, or safety gear assessment (3 marks)",
            "(d) Real-world practical application, impulse/force safety analysis, or optical implication (5 marks)"
        ],
        "forbidden_constraints": "FORBID non-scientific fluff. FORBID subjective opinion questions without physical laws."
    },
    "Chemistry": {
        "persona_role": "Task:",
        "support_type": "Chemical reaction equations, molar masses, solution concentrations, pH values, laboratory setup diagrams.",
        "cognitive_progression": [
            "(a) Chemical equation balancing or product identification (3 marks)",
            "(b) Reaction rate or stoichiometry calculation / experiment evaluation (4 marks)",
            "(c) Industrial yield optimization or environmental pollution assessment (3 marks)",
            "(d) Practical industrial, household, or environmental chemical impact (5 marks)"
        ],
        "forbidden_constraints": "FORBID non-chemical trivia. FORBID math calculations unrelated to chemistry."
    },
    "Biology": {
        "persona_role": "Task:",
        "support_type": "Anatomical/physiological diagrams, ecological food webs, genetic cross tables, plant/animal adaptation data.",
        "cognitive_progression": [
            "(a) Biological process identification or organ/structure function (3 marks)",
            "(b) Physiological mechanism explanation or adaptation evaluation (4 marks)",
            "(c) Ecological impact, disease control, or genetic trait assessment (3 marks)",
            "(d) Health, environmental conservation, or agricultural productivity implication (5 marks)"
        ],
        "forbidden_constraints": "FORBID math date subtraction. FORBID generic non-biological stories."
    },
    "Mathematics": {
        "persona_role": "Task:",
        "support_type": "Geometric dimensions, coordinate data, network lengths, statistical tables, algebraic constraints.",
        "cognitive_progression": [
            "(a) Initial parameter calculation or geometric length/area determination (3 marks)",
            "(b) Geometric/algebraic layout optimization or statistical measure calculation (4 marks)",
            "(c) Cost reduction, percentage variation, or rate of output evaluation (3 marks)",
            "(d) Real-world system efficiency, long-term trend, or practical community synthesis (5 marks)"
        ],
        "forbidden_constraints": "FORBID essay writing or subjective history trivia. MANDATORY step-by-step working."
    },
    "History": {
        "persona_role": "Task:",
        "support_type": "Historical source extracts, primary quotes, administrator diaries, colonial agreement clauses, pre-colonial kingdom records.",
        "cognitive_progression": [
            "(a) Specific historical cause, treaty clause, or primary source analysis (3 marks)",
            "(b) Socio-economic impact, diplomatic strategy, or colonial policy evaluation (4 marks)",
            "(c) Critical assessment of historical evidence, bias, or kingdom resistance (3 marks)",
            "(d) Long-term national development, unity, or modern relevance implication (5 marks)"
        ],
        "forbidden_constraints": "CRITICAL BAN: FORBID date subtraction arithmetic (e.g. 'Calculate years from 1950 to 2023'). FORBID media/event management tasks (e.g. 'design museum tour' or 'suggest radio presentation')."
    },
    "Geography": {
        "persona_role": "Task:",
        "support_type": "Topographic map excerpts, climate graphs, rainfall/temperature tables, landform diagrams, trade statistics.",
        "cognitive_progression": [
            "(a) Geographic feature identification, climate data reading, or location factor (3 marks)",
            "(b) Formation mechanism explanation or land-use pattern assessment (4 marks)",
            "(c) Environmental hazard, erosion control, or resource conflict evaluation (3 marks)",
            "(d) Sustainable regional development, conservation policy, or economic planning implication (5 marks)"
        ],
        "forbidden_constraints": "FORBID math date subtraction. FORBID non-geographical trivia."
    },
    "Economics": {
        "persona_role": "Task:",
        "support_type": "Supply/demand price tables, inflation rates, market equilibrium charts, tax rates, trade balance figures.",
        "cognitive_progression": [
            "(a) Equilibrium price/quantity calculation or elasticity determination (3 marks)",
            "(b) Market structure or government fiscal policy impact assessment (4 marks)",
            "(c) Trade deficit, inflation control, or resource allocation evaluation (3 marks)",
            "(d) National economic development, employment policy, or poverty alleviation synthesis (5 marks)"
        ],
        "forbidden_constraints": "FORBID non-economic story filler."
    },
    "Entrepreneurship": {
        "persona_role": "Task:",
        "support_type": "Business cash flow statements, cost tables, customer survey data, product production metrics.",
        "cognitive_progression": [
            "(a) Profit/loss or break-even volume calculation (3 marks)",
            "(b) Business opportunity & marketing strategy evaluation (4 marks)",
            "(c) Risk management or financial resource optimization (3 marks)",
            "(d) Long-term business sustainability & community value creation (5 marks)"
        ],
        "forbidden_constraints": "FORBID non-business story filler."
    },
    "English": {
        "persona_role": "Task:",
        "support_type": "Passage text, poem, dialogue excerpt, official notice, speech transcript.",
        "cognitive_progression": [
            "(a) Passage comprehension / contextual vocabulary extraction (3 marks)",
            "(b) Character motivation or literary device analysis (4 marks)",
            "(c) Summary & main argument synthesis (3 marks)",
            "(d) Guided composition / formal letter writing / critical reflection (5 marks)"
        ],
        "forbidden_constraints": "FORBID science formulas and math calculations."
    }
}


def get_subject_blueprint(subject: str) -> dict:
    """Returns the official UNEB Subject Competency Blueprint for a given subject."""
    from core.secondary_engine import get_secondary_blueprint
    bp = get_secondary_blueprint(subject)
    return {
        "persona_role": "Task:",
        "support_type": bp.stimulus_type + " (" + ", ".join(bp.stimulus_examples[:2]) + ")",
        "cognitive_progression": [
            f"{p['label']} {p['text']} ({p['marks']} marks)" for p in bp.cognitive_progression
        ],
        "forbidden_constraints": " ".join(bp.negative_constraints)
    }
