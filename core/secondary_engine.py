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
    cognitive_progression: List[str]
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
            "Level 1 - Understand: Initial parameter calculation or geometric length/area determination",
            "Level 2 - Apply: Geometric/algebraic layout optimization or statistical measure calculation",
            "Level 3 - Analyze: Cost reduction, percentage variation, or rate of output evaluation",
            "Level 4 - Evaluate: Real-world system efficiency, long-term trend analysis, or practical community recommendation",
            "Level 5 - Create: Design a solution, financial model, or structural plan"
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
            "Level 1 - Understand: Direct physical law determination",
            "Level 2 - Apply: Quantitative calculation using physical laws",
            "Level 3 - Analyze: Energy loss, efficiency calculation, or safety gear assessment",
            "Level 4 - Evaluate: Real-world practical application, impulse/force safety analysis, or optical implication",
            "Level 5 - Create: Design an experiment, safety system, or circuit layout"
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
            "Level 1 - Understand: Product identification and property definition",
            "Level 2 - Apply: Chemical equation balancing and stoichiometry calculation",
            "Level 3 - Analyze: Reaction rate evaluation or experimental yield analysis",
            "Level 4 - Evaluate: Environmental pollution assessment or industrial process efficiency",
            "Level 5 - Create: Design a safe laboratory setup or industrial extraction schematic"
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
            "Level 1 - Understand: Biological process identification or structure function analysis",
            "Level 2 - Apply: Physiological mechanism explanation",
            "Level 3 - Analyze: Ecological impact, disease control, or genetic trait assessment",
            "Level 4 - Evaluate: Environmental conservation or agricultural productivity synthesis",
            "Level 5 - Create: Design an ecological experiment, dietary plan, or public health intervention"
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
            "Level 1 - Understand: Identify historical figures, events, or primary source context",
            "Level 2 - Apply: Explain specific historical causes or treaty clauses",
            "Level 3 - Analyze: Socio-economic impact, diplomatic strategy, or colonial policy evaluation",
            "Level 4 - Evaluate: Critical assessment of historical evidence, bias, or kingdom resistance",
            "Level 5 - Create: Long-term national development, unity, or modern relevance synthesis"
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
            "Level 1 - Understand: Geographic feature identification or climate data reading",
            "Level 2 - Apply: Formation mechanism explanation or map data calculation",
            "Level 3 - Analyze: Land-use pattern assessment or environmental hazard evaluation",
            "Level 4 - Evaluate: Resource conflict resolution or erosion control policy evaluation",
            "Level 5 - Create: Sustainable regional development or conservation plan design"
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
            "Level 1 - Understand: Define economic terms or identify market structures",
            "Level 2 - Apply: Equilibrium price/quantity calculation or elasticity determination",
            "Level 3 - Analyze: Government fiscal policy impact or trade deficit assessment",
            "Level 4 - Evaluate: Inflation control, resource allocation, or taxation policy evaluation",
            "Level 5 - Create: National economic development or poverty alleviation policy proposal"
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
            "Level 1 - Understand: Identify business opportunities or market feasibility metrics",
            "Level 2 - Apply: Profit/loss or break-even volume calculation",
            "Level 3 - Analyze: Risk management or marketing strategy assessment",
            "Level 4 - Evaluate: Financial resource optimization or competitor analysis",
            "Level 5 - Create: Business plan creation or long-term sustainability modeling"
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
            "Level 1 - Understand: Passage comprehension and vocabulary extraction",
            "Level 2 - Apply: Character motivation or rhetorical device identification",
            "Level 3 - Analyze: Thematic analysis or persuasive argument breakdown",
            "Level 4 - Evaluate: Critical reflection or tone/bias assessment",
            "Level 5 - Create: Guided composition, formal letter writing, or speech drafting"
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
            "Level 1 - Understand: Agricultural input calculation or symptom identification",
            "Level 2 - Apply: Farming technique or soil management practice implementation",
            "Level 3 - Analyze: Pest/disease control or post-harvest loss causes",
            "Level 4 - Evaluate: Agribusiness profitability or environmental sustainability assessment",
            "Level 5 - Create: Farm plan design or integrated pest management strategy"
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
            "Level 1 - Understand: Direct contextual analysis",
            "Level 2 - Apply: Method evaluation and mechanism explanation",
            "Level 3 - Analyze: Optimization and critical assessment",
            "Level 4 - Evaluate: Real-world synthesis and long-term practical recommendation",
            "Level 5 - Create: Strategic plan or comprehensive solution design"
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
        progression_str = "\n".join(f"  - {p}" for p in blueprint.cognitive_progression)
        constraints_str = "\n".join(f"  - {c}" for c in blueprint.negative_constraints)
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
- BLOOM'S TAXONOMY PROGRESSION FRAMEWORK:
{progression_str}

STRICT NEGATIVE CONSTRAINTS (FORBIDDEN):
{constraints_str}

CRITICAL STRUCTURE & DERIVATION RULE:
1. Each item MUST strictly follow the new Scenario -> Context -> Task -> Questions framework. 
2. SCENARIO LENGTH: The `scenario` MUST be a rich, extended narrative of at least 2 to 3 PARAGRAPHS. It must include specific characters, locations, numerical data, and practical complications.
3. NO ROTE RECALL: Every single sub-question MUST directly reference the scenario and test how the student would approach solving the specific problem presented. Do not ask generic recall questions (e.g. "What is X?"). Instead, ask applied questions (e.g. "Based on the farmer's situation, explain how...").
4. Sub-questions must progressively escalate in difficulty according to the Bloom's Taxonomy framework above. Assign realistic marks for each sub-question based on cognitive difficulty (e.g. 1-2 marks for Understand/Apply, 3-5 marks for Analyze/Evaluate/Create).

Each item MUST be structured as a JSON object:
{{
  "number": 1,
  "scenario": "A highly detailed, extended real-world scenario narrative (MUST BE AT LEAST 2-3 PARAGRAPHS) setting up a complex, practical situation in Uganda for {blueprint.name.upper()}.",
  "context": "Additional background information, data, or context necessary to solve the problem.",
  "resources": "Describe any required image, table, graph, map, or document (or empty string if none).",
  "task": "A clear statement of what the learner is expected to do.",
  "task_heading": "Tasks:",
  "difficulty": "Medium",
  "time": "20 minutes",
  "competency": "Application, analysis, evaluation, problem solving",
  "type": "structured",
  "sub_questions": [
    {{ 
      "label": "(a)", 
      "text": "Sub-question asking the student to Understand/Apply based on the scenario...", 
      "marks": 2,
      "expected_answer": "Model answer / marking points here."
    }},
    {{ 
      "label": "(b)", 
      "text": "Sub-question asking the student to Analyze based on the scenario...", 
      "marks": 3,
      "expected_answer": "Model answer / marking points here."
    }},
    {{ 
      "label": "(c)", 
      "text": "Sub-question asking the student to Evaluate/Create based on the scenario...", 
      "marks": 4,
      "expected_answer": "Model answer / marking points here."
    }}
  ]
}}

Return JSON:
{{
  "questions": [ ... ]
}}
"""
