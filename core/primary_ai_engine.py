# Deep Authentic NCDC / UNEB Primary AI Pedagogical Engine (P.1 - P.7 / PLE)
# Implements Bloom's Taxonomy balancing, topic blueprint distributions, integer math calibration, and English Section B literary prompts

import json
from typing import Dict, List, Any

class PrimaryPedagogicalEngine:
    """
    Pedagogical engine enforcing official NCDC Primary Curriculum guidelines and UNEB PLE national exam standards.
    """

    @staticmethod
    def get_topic_distribution(subject: str, level: str) -> List[str]:
        """Returns topic blueprint distributions according to NCDC Primary Curriculum."""
        subj_lower = (subject or "Mathematics").lower()
        
        if "math" in subj_lower:
            return [
                "Numeracy, Place Value & Operations",
                "Fractions, Decimals & Percentages",
                "Algebraic Expressions & Equations",
                "Geometry, Perimeter, Area & Volume",
                "Sets & Venn Diagram Problems",
                "Money, Transactions & UGX Commercial Math",
                "Time, Speed, Distance & Units",
                "Data Handling, Pie Charts & Averages"
            ]
        elif "science" in subj_lower:
            return [
                "Human Physiology, Excretion & Health",
                "Disease Vectors, Malaria & Sanitation",
                "Crop Husbandry, Soil & Agriculture",
                "Livestock, Poultry & Animal Husbandry",
                "Environment, Water Cycle & Forestry",
                "Matter, Air, Sound & Light Energy",
                "Electricity, Dry Cells & Simple Circuits",
                "Simple Machines, Levers & Pulleys"
            ]
        elif "english" in subj_lower:
            return [
                "Vocabulary & Preposition Completion",
                "Word Formations, Plurals & Opposites",
                "Sentence Rewriting & Transformation",
                "Comprehension Reading & Critical Thinking",
                "Poetry & Dialogue Analysis",
                "Official Notices & Timetable Interpretation",
                "Jumbled Sentences & Coherent Ordering",
                "Guided Composition & Letter Writing"
            ]
        else: # SST
            return [
                "Physical Features & Climate of East Africa",
                "Map Reading, Compass Rose & Scales",
                "People & Ethnic Migrations in East Africa",
                "Economic Development & Regional Trade (EAC)",
                "Ugandan Governance, Arms of Government & Civics",
                "Natural Resources & Environmental Conservation",
                "Religious Education Principles (CRE / IRE)",
                "National Symbols & Citizenship Duties"
            ]

    @staticmethod
    def build_prompt(subject: str, level: str, theme: str, topic: str, section: str, start_num: int, count: int) -> str:
        """Synthesizes deep, authentic UNEB examination prompts using Bloom's Taxonomy balancing."""
        subj_lower = (subject or "Mathematics").lower()
        topics = PrimaryPedagogicalEngine.get_topic_distribution(subject, level)
        topic_str = ", ".join(topics)

        # Subject-specific directive blocks
        if "math" in subj_lower:
            subject_directives = """
MATHEMATICS SPECIALIST RULES:
- EVERY QUESTION MUST CONTAIN EXACT NUMERICAL DATA ($3x - 5 = 10$, $45 \text{ pupils}$, $\frac{3}{4} - \frac{1}{2}$, UGX 720,000).
- SOLVABILITY GUARANTEE: All numerical calculations MUST yield clean integer answers or exact simple fractions (no unworkable figures or infinite decimals!).
- Section A (2 marks each): Test numerical operations, fraction simplification, linear equations, Venn diagrams, perimeter/area, and unit conversions.
- Section B (4-5 marks each): Contextual multi-part word problems with sub-questions (a), (b), (c) involving local Ugandan contexts (Ugandan Shillings UGX, local distances in km, market trading).
"""
        elif "english" in subj_lower:
            subject_directives = """
ENGLISH LANGUAGE SPECIALIST RULES:
- Section A Sub-part I (Q1-15): Fill in the blank space with a suitable word ("Neither... nor", "prefer... to", "since").
- Section A Sub-part II (Q16-30): Correct word form in brackets (tenses, plurals, adverbs).
- Section A Sub-part III (Q31-50): Sentence rewriting ("Re-write as instructed in brackets: Begin: Unless...", "Use: ...so...that...", "Begin: No sooner...").
- Section B (Q51-55):
  * If Section B contains Q51: Provide a FULL ORIGINAL 10-LINE COMPREHENSION STORY about a local Ugandan village/pupil + 5-10 sub-questions (a to j).
  * If Section B contains Q52: Provide a 4-stanza poem or dialogue + 5 sub-questions.
  * If Section B contains Q53: Provide an official public notice or timetable + 5 sub-questions.
  * If Section B contains Q54: Provide 10 JUMBLED SENTENCES (numbered 1-10) to re-arrange into a logical story.
  * If Section B contains Q55: Provide a guided composition or formal letter prompt.
"""
        elif "science" in subj_lower:
            subject_directives = """
INTEGRATED SCIENCE SPECIALIST RULES:
- Section A (1 mark each): Direct, concise application questions ("Name the organ...", "State one function of...", "Which vector transmits...", "Give one reason why...").
- Section B (4 marks each): Experimental setups, dry cell circuit diagrams, crop disease control, respiratory/digestive system functions, and sanitation.
"""
        else: # SST
            subject_directives = """
SOCIAL STUDIES SPECIALIST RULES:
- Section A (1 mark each): Direct geographic, historical, civic, and CRE/IRE items ("Name the river...", "State the main economic activity...", "Which arm of government...").
- Section B (4-5 marks each): Maps of East Africa/Uganda, climate zones, East African Community (EAC), Constitution, and religious moral values.
"""

        prompt = f"""
You are the Chief Senior Examiner for the UGANDA NATIONAL EXAMINATIONS BOARD (UNEB) constructing the official {level} National Examination paper for {subject.upper()}.

EXAM BLUEPRINT SPECIFICATIONS:
- SUBJECT: {subject.upper()}
- LEVEL: {level}
- SECTION: Section {section}
- QUESTION NUMBERS: Question {start_num} to Question {start_num + count - 1} ({count} items total)
- SYLLABUS TOPIC COVERAGE: {topic_str}

BLOOM'S REVISED TAXONOMY COGNITIVE DISTRIBUTION:
1. Knowledge & Recall (20%): Direct facts, definitions, and identifications.
2. Comprehension & Explanation (30%): Scientific mechanisms, grammar rules, geographic phenomena.
3. Application & Calculation (35%): Real-world Ugandan word problems, UGX transactions, sentence transformations.
4. Analysis & Evaluation (15%): Experimental data analysis, multi-part contextual problem solving.

{subject_directives}

LOCAL UGANDAN CONTEXT ENFORCEMENT:
Use authentic Ugandan names (Kato, Babirye, Okello, Mukasa, Akello, Namubiru), local towns (Kampala, Jinja, Mbale, Mbarara, Gulu, Kasese), local produce (coffee, maize, bananas/matooke), and currency (UGX).

OUTPUT REQUIREMENT:
Return ONLY a valid JSON object with key 'questions' as a list of items starting at question number {start_num}.
Each item must have:
- 'number': integer ({start_num} to {start_num + count - 1})
- 'text': string (authentic question stem)
- 'hint': string (expected answer / step-by-step working)
- 'type': 'short_answer' for Section A, 'structured' for Section B
- 'marks': integer (Section A: 1 or 2 marks; Section B: 4 to 10 marks)
- 'sub_questions': list (for Section B: list of sub-question dicts with 'label', 'text', 'marks')
"""
        return prompt
