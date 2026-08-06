# Dynamic Secondary Competency Assessment Engine (UCE & UACE)
# Data-Driven Blueprint Registry & Universal Prompt Synthesizer for Ugandan Secondary Education

import re
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class SecondarySubjectBlueprint:
    subject_key: str
    name: str
    domain: str  # STEM, Humanities, Business, Languages, Vocational
    stimulus_type: str
    stimulus_examples: List[str]
    cognitive_progression: List[Dict[str, str]]
    negative_constraints: List[str]

# ── SECONDARY SUBJECT BLUEPRINTS REGISTRY ──
SECONDARY_BLUEPRINTS: Dict[str, SecondarySubjectBlueprint] = {

    "mathematics": SecondarySubjectBlueprint(
        subject_key="mathematics",
        name="Mathematics",
        domain="STEM",
        stimulus_type="QUANTITATIVE_GEOMETRIC_DATA",
        stimulus_examples=[
            "Geometric dimensions and network lengths",
            "Coordinate grid vertices and transformation vectors",
            "Statistical frequency distributions and probability tables",
            "Algebraic constraint equations and business interest/tax data",
            "Kinematic speed-time or rate-of-output graphs"
        ],
        cognitive_progression=[
            {"label": "(a)", "text": "Initial parameter calculation or geometric length/area determination", "marks": "3"},
            {"label": "(b)", "text": "Geometric/algebraic layout optimization or statistical measure calculation", "marks": "4"},
            {"label": "(c)", "text": "Cost reduction, percentage variation, or rate of output evaluation", "marks": "3"},
            {"label": "(d)", "text": "Real-world system efficiency, long-term trend analysis, or practical community recommendation", "marks": "5"}
        ],
        negative_constraints=[
            "FORBID essay writing or subjective history/humanities trivia.",
            "FORBID date subtraction or historical timeline questions.",
            "MANDATORY step-by-step mathematical working and numerical calculations."
        ]
    ),

    "physics": SecondarySubjectBlueprint(
        subject_key="physics",
        name="Physics",
        domain="STEM",
        stimulus_type="PHYSICAL_CONSTANTS_AND_MOTION_DATA",
        stimulus_examples=[
            "Numerical physical parameters (mass, velocity, force, braking deceleration)",
            "Optical indices, focal lengths, and ray path diagrams",
            "Electrical circuit values (voltage, resistance, power, magnetic fields)",
            "Kinematic motion graphs and heat capacity data"
        ],
        cognitive_progression=[
            {"label": "(a)", "text": "Quantitative calculation or direct physical law determination", "marks": "3"},
            {"label": "(b)", "text": "Physical mechanism explanation or principle evaluation", "marks": "4"},
            {"label": "(c)", "text": "Energy loss, efficiency calculation, or safety gear assessment", "marks": "3"},
            {"label": "(d)", "text": "Real-world practical application, impulse/force safety analysis, or optical implication", "marks": "5"}
        ],
        negative_constraints=[
            "FORBID non-scientific fluff or subjective opinions without physical laws.",
            "MANDATORY step-by-step physical formula derivations and numerical calculations."
        ]
    ),

    "chemistry": SecondarySubjectBlueprint(
        subject_key="chemistry",
        name="Chemistry",
        domain="STEM",
        stimulus_type="CHEMICAL_REACTIONS_AND_STOICHIOMETRY",
        stimulus_examples=[
            "Chemical reaction equations and molar masses",
            "Solution concentrations, pH values, and titration volumes",
            "Gas volumes at STP and rate-of-reaction data",
            "Laboratory setup diagrams and industrial extraction schematics"
        ],
        cognitive_progression=[
            {"label": "(a)", "text": "Chemical equation balancing or product identification", "marks": "3"},
            {"label": "(b)", "text": "Reaction rate or stoichiometry calculation / experiment evaluation", "marks": "4"},
            {"label": "(c)", "text": "Industrial yield optimization or environmental pollution assessment", "marks": "3"},
            {"label": "(d)", "text": "Practical industrial, household, or environmental chemical impact analysis", "marks": "5"}
        ],
        negative_constraints=[
            "FORBID non-chemical trivia or non-scientific stories.",
            "MANDATORY chemical equations and quantitative stoichiometric calculations."
        ]
    ),

    "biology": SecondarySubjectBlueprint(
        subject_key="biology",
        name="Biology",
        domain="STEM",
        stimulus_type="PHYSIOLOGICAL_ECOLOGICAL_DATA",
        stimulus_examples=[
            "Anatomical and physiological organ system diagrams",
            "Ecological food webs and population growth curves",
            "Genetic cross tables and inheritance ratios",
            "Plant and animal structural adaptation data"
        ],
        cognitive_progression=[
            {"label": "(a)", "text": "Biological process identification or organ/structure function analysis", "marks": "3"},
            {"label": "(b)", "text": "Physiological mechanism explanation or adaptation evaluation", "marks": "4"},
            {"label": "(c)", "text": "Ecological impact, disease control, or genetic trait assessment", "marks": "3"},
            {"label": "(d)", "text": "Health, environmental conservation, or agricultural productivity synthesis", "marks": "5"}
        ],
        negative_constraints=[
            "FORBID date subtraction or non-biological story filler.",
            "MANDATORY biological diagrams, physiological processes, or biological data analysis."
        ]
    ),

    "history": SecondarySubjectBlueprint(
        subject_key="history",
        name="History",
        domain="Humanities",
        stimulus_type="PRIMARY_SOURCES_AND_HISTORICAL_DOCUMENTS",
        stimulus_examples=[
            "Historical primary source extracts and quotes from speeches or treaties",
            "Colonial administrator diaries and pre-colonial kingdom agreements",
            "Trade route timelines and diplomatic correspondence excerpts"
        ],
        cognitive_progression=[
            {"label": "(a)", "text": "Specific historical cause, treaty clause, or primary source analysis", "marks": "3"},
            {"label": "(b)", "text": "Socio-economic impact, diplomatic strategy, or colonial policy evaluation", "marks": "4"},
            {"label": "(c)", "text": "Critical assessment of historical evidence, bias, or kingdom resistance", "marks": "3"},
            {"label": "(d)", "text": "Long-term national development, unity, or modern relevance implication", "marks": "5"}
        ],
        negative_constraints=[
            "CRITICAL BAN: FORBID date subtraction arithmetic (e.g. 'Calculate years from 1950 to 2023'). Subtracting years is NOT History.",
            "CRITICAL BAN: FORBID media/event management tasks (e.g. 'design museum tour' or 'suggest radio presentation').",
            "MANDATORY authentic historical cause, policy evaluation, and primary source analysis."
        ]
    ),

    "geography": SecondarySubjectBlueprint(
        subject_key="geography",
        name="Geography",
        domain="Humanities",
        stimulus_type="SPATIAL_CLIMATIC_MAP_DATA",
        stimulus_examples=[
            "Topographic map excerpts and contour line features",
            "Climate graphs, temperature/rainfall data tables",
            "Landform formation diagrams and soil profile sketches",
            "Trade balance figures and population distribution maps"
        ],
        cognitive_progression=[
            {"label": "(a)", "text": "Geographic feature identification, climate data reading, or location factor", "marks": "3"},
            {"label": "(b)", "text": "Formation mechanism explanation or land-use pattern assessment", "marks": "4"},
            {"label": "(c)", "text": "Environmental hazard, erosion control, or resource conflict evaluation", "marks": "3"},
            {"label": "(d)", "text": "Sustainable regional development, conservation policy, or economic planning synthesis", "marks": "5"}
        ],
        negative_constraints=[
            "FORBID date subtraction or non-geographical trivia.",
            "MANDATORY spatial, climatic, or landform analysis."
        ]
    ),

    "economics": SecondarySubjectBlueprint(
        subject_key="economics",
        name="Economics",
        domain="Business",
        stimulus_type="MACRO_MICRO_ECONOMIC_METRICS",
        stimulus_examples=[
            "Supply and demand price/quantity schedules",
            "Inflation rates, exchange rates, and tax metrics",
            "Market equilibrium charts and trade balance figures",
            "National income and employment data tables"
        ],
        cognitive_progression=[
            {"label": "(a)", "text": "Equilibrium price/quantity calculation or elasticity determination", "marks": "3"},
            {"label": "(b)", "text": "Market structure or government fiscal policy impact assessment", "marks": "4"},
            {"label": "(c)", "text": "Trade deficit, inflation control, or resource allocation evaluation", "marks": "3"},
            {"label": "(d)", "text": "National economic development, employment policy, or poverty alleviation synthesis", "marks": "5"}
        ],
        negative_constraints=[
            "FORBID non-economic story filler.",
            "MANDATORY economic principles, calculations, or market graph analyses."
        ]
    ),

    "entrepreneurship": SecondarySubjectBlueprint(
        subject_key="entrepreneurship",
        name="Entrepreneurship Education",
        domain="Business",
        stimulus_type="BUSINESS_FINANCIAL_OPERATIONAL_DATA",
        stimulus_examples=[
            "Business cash flow projections and income statements",
            "Production cost tables and pricing schedules",
            "Customer survey feedback and market feasibility metrics"
        ],
        cognitive_progression=[
            {"label": "(a)", "text": "Profit/loss or break-even volume calculation", "marks": "3"},
            {"label": "(b)", "text": "Business opportunity and marketing strategy evaluation", "marks": "4"},
            {"label": "(c)", "text": "Risk management or financial resource optimization", "marks": "3"},
            {"label": "(d)", "text": "Long-term business sustainability and community value creation synthesis", "marks": "5"}
        ],
        negative_constraints=[
            "FORBID non-business story filler.",
            "MANDATORY business financial calculation, strategy evaluation, or cash flow analysis."
        ]
    ),

    "english": SecondarySubjectBlueprint(
        subject_key="english",
        name="English Language",
        domain="Languages",
        stimulus_type="LITERARY_TEXT_AND_COMPREHENSION_STIMULUS",
        stimulus_examples=[
            "Passage texts, official notices, and speech transcripts",
            "Contextual dialogue excerpts and persuasive essays",
            "Poem extracts and formal correspondence letters"
        ],
        cognitive_progression=[
            {"label": "(a)", "text": "Passage comprehension and contextual vocabulary extraction", "marks": "3"},
            {"label": "(b)", "text": "Character motivation or literary device analysis", "marks": "4"},
            {"label": "(c)", "text": "Summary & main argument synthesis", "marks": "3"},
            {"label": "(d)", "text": "Guided composition / formal letter writing / critical reflection", "marks": "5"}
        ],
        negative_constraints=[
            "FORBID science formulas or mathematical calculations.",
            "MANDATORY English grammar, comprehension, or literary analysis."
        ]
    ),

    "agriculture": SecondarySubjectBlueprint(
        subject_key="agriculture",
        name="Agriculture",
        domain="Vocational",
        stimulus_type="FARM_PRODUCTION_SOIL_DATA",
        stimulus_examples=[
            "Crop yield statistics and fertilizer application rates",
            "Livestock feeding schedules and disease symptom records",
            "Soil PH test results and erosion control layouts"
        ],
        cognitive_progression=[
            {"label": "(a)", "text": "Agricultural input calculation or crop/livestock symptom identification", "marks": "3"},
            {"label": "(b)", "text": "Farming technique or soil management practice evaluation", "marks": "4"},
            {"label": "(c)", "text": "Pest/disease control or post-harvest loss reduction strategy", "marks": "3"},
            {"label": "(d)", "text": "Agribusiness profitability and sustainable farming synthesis", "marks": "5"}
        ],
        negative_constraints=[
            "FORBID non-agricultural stories.",
            "MANDATORY agricultural techniques, livestock, soil, or crop management focus."
        ]
    )
}

# ── BLUEPRINT RESOLVER FUNCTION ──
def get_secondary_blueprint(subject: str) -> SecondarySubjectBlueprint:
    """Dynamically resolves any subject string to its canonical SecondarySubjectBlueprint."""
    if not subject:
        return SECONDARY_BLUEPRINTS["mathematics"]
        
    s = subject.strip().lower()

    # Exact key match
    if s in SECONDARY_BLUEPRINTS:
        return SECONDARY_BLUEPRINTS[s]

    # Alias mapping
    alias_map = {
        "math": "mathematics",
        "maths": "mathematics",
        "numeracy": "mathematics",
        "phys": "physics",
        "chem": "chemistry",
        "bio": "biology",
        "hist": "history",
        "geog": "geography",
        "econ": "economics",
        "ent": "entrepreneurship",
        "entrepreneurship education": "entrepreneurship",
        "eng": "english",
        "english language": "english",
        "agric": "agriculture"
    }

    canon_key = alias_map.get(s)
    if canon_key and canon_key in SECONDARY_BLUEPRINTS:
        return SECONDARY_BLUEPRINTS[canon_key]

    # Partial substring match
    for key, bp in SECONDARY_BLUEPRINTS.items():
        if key in s or s in key:
            return bp

    # Default fallback to Mathematics blueprint for STEM/general fallback
    return SecondarySubjectBlueprint(
        subject_key=s,
        name=subject,
        domain="General Secondary",
        stimulus_type="CONTEXTUAL_CASE_STUDY_DATA",
        stimulus_examples=["Contextual case study data", "Reference table or diagram"],
        cognitive_progression=[
            {"label": "(a)", "text": f"Direct contextual analysis for {subject}", "marks": "3"},
            {"label": "(b)", "text": f"Method evaluation and mechanism explanation for {subject}", "marks": "4"},
            {"label": "(c)", "text": f"Optimization and critical assessment for {subject}", "marks": "3"},
            {"label": "(d)", "text": f"Real-world synthesis and long-term practical recommendation for {subject}", "marks": "5"}
        ],
        negative_constraints=[f"FORBID non-{subject} fluff. Every item must be scenario-anchored."]
    )

# ── UNIVERSAL SECONDARY PROMPT SYNTHESIZER ──
class SecondaryPromptSynthesizer:
    @staticmethod
    def synthesize(blueprint: SecondarySubjectBlueprint, level: str, theme: str = "", topic: str = "") -> str:
        """
        Synthesizes a 100% subject-isolated, zero-bleed UCE competency prompt.
        """
        progression_str = "\n".join(
            f"  {p['label']} {p['text']} ({p['marks']} marks)"
            for p in blueprint.cognitive_progression
        )
        constraints_str = "\n".join(
            f"  - {c}" for c in blueprint.negative_constraints
        )
        stimulus_str = ", ".join(blueprint.stimulus_examples[:3])

        topic_clause = f"ASSIGNED SYLLABUS TOPIC: {topic}" if topic else f"Select 3 distinct core syllabus topics for {blueprint.name.upper()} in {level}."

        return f"""
### UGANDA CERTIFICATE OF EDUCATION (UCE) COMPETENCY ASSESSMENT
SUBJECT: {blueprint.name.upper()} ({blueprint.domain} DOMAIN)
LEVEL: {level}
THEME CONTEXT: {theme or "Ugandan Real-World Community Scenario"}
{topic_clause}

Generate 3 authentic UCE Competency-Based Assessment ITEMS for {blueprint.name.upper()}.
EVERY SINGLE ITEM MUST HAVE ITS OWN UNIQUE, INDEPENDENT REAL-WORLD SCENARIO NARRATIVE MATCHING {blueprint.name.upper()}.

SUBJECT COMPETENCY BLUEPRINT ({blueprint.name.upper()}):
- STIMULUS DATA TYPE ({blueprint.stimulus_type}): {stimulus_str}
- COGNITIVE SUB-QUESTION PROGRESSION:
{progression_str}

STRICT NEGATIVE CONSTRAINTS (FORBIDDEN):
{constraints_str}

CRITICAL DERIVATION RULE:
EVERY SUB-QUESTION (a, b, c, d) MUST BE DIRECTLY DERIVED FROM AND EXPLICITLY REFERENCE THE SPECIFIC CHARACTERS, LOCATIONS, NUMERICAL DATA, AND EVENTS DESCRIBED IN THE ITEM'S SCENARIO NARRATIVE.

Each item MUST be structured as:
{{
  "number": 1,
  "text": "A rich, detailed real-world scenario narrative (1-2 paragraphs) setting up a practical situation in Uganda for {blueprint.name.upper()}...",
  "hint": "Given numerical parameters, formulas, constants, or reference text (or empty string)",
  "task_heading": "Task:",
  "type": "structured",
  "sub_questions": [
    {{ "label": "(a)", "text": "Sub-task (a) following cognitive progression for {blueprint.name.upper()} derived directly from the scenario...", "marks": 3 }},
    {{ "label": "(b)", "text": "Sub-task (b) following cognitive progression for {blueprint.name.upper()} derived directly from the scenario...", "marks": 4 }},
    {{ "label": "(c)", "text": "Sub-task (c) following cognitive progression for {blueprint.name.upper()} derived directly from the scenario...", "marks": 3 }},
    {{ "label": "(d)", "text": "Sub-task (d) following cognitive progression for {blueprint.name.upper()} derived directly from the scenario...", "marks": 5 }}
  ]
}}

Return JSON:
{{
  "questions": [ ... ]
}}
"""
