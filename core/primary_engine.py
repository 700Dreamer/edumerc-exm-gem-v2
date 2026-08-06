# Dedicated Primary Section Engine (Primary 1 - Primary 7 / PLE)
# UNEB PLE & NCDC Lower Primary Paper Structure Registry and Blueprint Manager

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class PrimarySubjectBlueprint:
    subject_key: str
    name: str
    domain: str  # STEM, Humanities, Languages, LowerPrimary
    sec_a_count: int
    sec_a_marks: int
    sec_b_count: int
    sec_b_marks: int
    total_marks: int
    duration: str
    description: str
    instructions: List[str]
    question_guidelines: List[str]

# ── PRIMARY PAPER STRUCTURE REGISTRY ──
PRIMARY_BLUEPRINTS: Dict[Tuple[str, str], PrimarySubjectBlueprint] = {}

def _init_primary_registry():
    # ── 1. LOWER PRIMARY (Primary 1 - Primary 3) ──
    lower_subjects = ["Mathematics", "English", "Literacy 1", "Literacy 2", "Reading", "Social Studies", "Science", "Religious Education"]
    for lvl in ["Primary 1", "Primary 2", "Primary 3"]:
        for subj in lower_subjects:
            key = (subj.lower(), lvl.lower())
            PRIMARY_BLUEPRINTS[key] = PrimarySubjectBlueprint(
                subject_key=subj.lower(),
                name=subj,
                domain="LowerPrimary",
                sec_a_count=20,
                sec_a_marks=20,
                sec_b_count=5,
                sec_b_marks=30,
                total_marks=50,
                duration="1 HR 30 MIN",
                description=f"{subj} Lower Primary Promotional Examination ({lvl})",
                instructions=[
                    "Answer all 20 questions in Section A.",
                    "Answer all 5 questions in Section B.",
                    "All work must be clear and legible."
                ],
                question_guidelines=[
                    "Section A: Short direct answer questions (1 mark each).",
                    "Section B: Structured 4-6 mark items matching NCDC Lower Primary theme syllabus."
                ]
            )

    # ── 2. UPPER PRIMARY & PLE (Primary 4 - Primary 7) ──
    for lvl in ["Primary 4", "Primary 5", "Primary 6", "Primary 7"]:
        # Mathematics PLE / Promotional
        PRIMARY_BLUEPRINTS[("mathematics", lvl.lower())] = PrimarySubjectBlueprint(
            subject_key="mathematics",
            name="Mathematics",
            domain="STEM",
            sec_a_count=20,
            sec_a_marks=40,
            sec_b_count=12,
            sec_b_marks=60,
            total_marks=100,
            duration="2 HRS 30 MIN",
            description=f"Mathematics Examination ({lvl})",
            instructions=[
                "Section A has 20 short answer questions (40 marks).",
                "Section B has 12 structured multi-step questions (60 marks).",
                "Answer ALL questions in both sections.",
                "All working MUST be shown clearly in the spaces provided."
            ],
            question_guidelines=[
                "Section A: Single/double-step calculation problems beginning with imperative commands ('Calculate...', 'Work out...', 'Find...', 'Simplify...', 'Solve...').",
                "Section B: Multi-step structured mathematical working (geometry, fractions, ratios, algebra, statistics, business arithmetic)."
            ]
        )

        # Integrated Science
        PRIMARY_BLUEPRINTS[("integrated science", lvl.lower())] = PrimarySubjectBlueprint(
            subject_key="integrated science",
            name="Integrated Science",
            domain="STEM",
            sec_a_count=40,
            sec_a_marks=40,
            sec_b_count=15,
            sec_b_marks=60,
            total_marks=100,
            duration="2 HRS 15 MIN",
            description=f"Integrated Science Examination ({lvl})",
            instructions=[
                "Section A has 40 short answer questions (40 marks).",
                "Section B has 15 structured multi-part questions (60 marks).",
                "Answer ALL questions in both sections."
            ],
            question_guidelines=[
                "Section A: Direct scientific application items ('State one function of...', 'Give any one reason why...', 'How does...').",
                "Section B: Multi-part structured scientific reasoning testing experiments, biological systems, plants, matter, and health."
            ]
        )

        # Social Studies & Religious Education
        PRIMARY_BLUEPRINTS[("social studies", lvl.lower())] = PrimarySubjectBlueprint(
            subject_key="social studies",
            name="Social Studies with Religious Education",
            domain="Humanities",
            sec_a_count=40,
            sec_a_marks=40,
            sec_b_count=15,
            sec_b_marks=60,
            total_marks=100,
            duration="2 HRS 15 MIN",
            description=f"Social Studies Examination ({lvl})",
            instructions=[
                "Section A has 40 short answer questions (40 marks).",
                "Section B has 15 structured multi-part questions (60 marks).",
                "Answer ALL questions in both sections."
            ],
            question_guidelines=[
                "Section A: Geographic, historical, and civic application items ('State the main reason why...', 'Identify the impact of...').",
                "Section B: Structured items evaluating spatial maps, history, governance, trade, climate, and religious education."
            ]
        )

        # English Language
        PRIMARY_BLUEPRINTS[("english", lvl.lower())] = PrimarySubjectBlueprint(
            subject_key="english",
            name="English Language",
            domain="Languages",
            sec_a_count=50,
            sec_a_marks=50,
            sec_b_count=5,
            sec_b_marks=50,
            total_marks=100,
            duration="2 HRS 15 MIN",
            description=f"English Language Examination ({lvl})",
            instructions=[
                "Section A Sub-part 1 (Q1-30): Sub-group grammar & vocabulary completion.",
                "Section A Sub-part 2 (Q31-50): Sentence rewriting as instructed in brackets.",
                "Section B (Q51-55): Composition, Letter Writing, Notice, Poem, and Comprehension Passage."
            ],
            question_guidelines=[
                "Section A (Q1-30): Fill in the blank space with a suitable word.",
                "Section A (Q31-50): Re-write the sentences as instructed in brackets.",
                "Section B Q51: Comprehension story + 10 sub-questions (a-j).",
                "Section B Q52: Poem / Dialogue + 5 sub-questions.",
                "Section B Q53: Notice / Table + 5 sub-questions.",
                "Section B Q54: 10 Jumbled sentences to re-arrange into a story.",
                "Section B Q55: Guided composition / Formal letter writing."
            ]
        )

_init_primary_registry()

def get_primary_blueprint(subject: str, level: str) -> PrimarySubjectBlueprint:
    """Returns the dedicated PrimarySubjectBlueprint for a given subject and level."""
    subj_clean = (subject or "Mathematics").strip().lower()
    lvl_clean = (level or "Primary 7").strip().lower()

    # Alias normalization
    alias_map = {
        "math": "mathematics",
        "maths": "mathematics",
        "science": "integrated science",
        "integrated science": "integrated science",
        "sst": "social studies",
        "social studies": "social studies",
        "social studies with religious education": "social studies",
        "cre": "social studies",
        "ire": "social studies",
        "eng": "english",
        "english language": "english"
    }
    subj_norm = alias_map.get(subj_clean, subj_clean)

    key = (subj_norm, lvl_clean)
    if key in PRIMARY_BLUEPRINTS:
        return PRIMARY_BLUEPRINTS[key]

    # Partial level/subject matching for P1-P7
    for (s, l), bp in PRIMARY_BLUEPRINTS.items():
        if (s == subj_norm or s in subj_norm or subj_norm in s) and (l == lvl_clean or l in lvl_clean or lvl_clean in l):
            return bp

    # Fallback default for Upper Primary
    return PrimarySubjectBlueprint(
        subject_key=subj_norm,
        name=subject,
        domain="General Primary",
        sec_a_count=20,
        sec_a_marks=40 if "math" in subj_norm else 20,
        sec_b_count=12 if "math" in subj_norm else 5,
        sec_b_marks=60 if "math" in subj_norm else 30,
        total_marks=100 if "math" in subj_norm else 50,
        duration="2 HRS 30 MIN" if "math" in subj_norm else "1 HR 30 MIN",
        description=f"{subject} Primary Examination ({level})",
        instructions=["Answer all questions in Section A and Section B."],
        question_guidelines=[f"Section A: Short answer items for {subject}.", f"Section B: Structured items for {subject}."]
    )

def get_primary_paper_structure(subject: str, level: str) -> dict:
    """Returns the official paper structure dictionary for Primary levels."""
    bp = get_primary_blueprint(subject, level)
    return {
        "sec_a_count": bp.sec_a_count,
        "sec_a_marks": bp.sec_a_marks,
        "sec_b_count": bp.sec_b_count,
        "sec_b_marks": bp.sec_b_marks,
        "total_marks": bp.total_marks,
        "duration": bp.duration,
        "description": bp.description,
        "sec_b_note": f"Answer all {bp.sec_b_count} questions in Section B"
    }
