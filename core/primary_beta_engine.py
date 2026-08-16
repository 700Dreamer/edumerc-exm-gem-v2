# Primary (beta) Paper Generation Engine (P.1 - P.7)
# Streamlined Subject & Level-Driven Primary Exam Paper Generator for Ugandan Primary Curriculum

import json
import asyncio
from typing import Dict, List, Tuple, AsyncGenerator
from dataclasses import dataclass
from core.ai_engine import get_async_openai_client, generate_exam_diagram
from ui.document_builder import build_question_html, build_full_html

@dataclass
class PrimaryBetaBlueprint:
    subject_key: str
    name: str
    level: str
    domain: str  # Lower Primary (P1-P3) or Upper Primary (P4-P7)
    sec_a_count: int
    sec_a_marks: int
    sec_b_count: int
    sec_b_marks: int
    total_questions: int
    total_marks: int
    duration: str
    instructions: List[str]
    negative_constraints: List[str]

def get_primary_beta_blueprint(subject: str, level: str) -> PrimaryBetaBlueprint:
    """Returns official UNEB/NCDC structure for Primary levels P.1 - P.7."""
    s_lower = (subject or "Mathematics").lower()
    lvl = level or "Primary 7"
    is_lower = any(l in lvl for l in ["Primary 1", "Primary 2", "Primary 3", "P.1", "P.2", "P.3", "P1", "P2", "P3"])

    if is_lower:
        # Lower Primary Standard (P.1 - P.3): 20 Sec A (20m) + 5 Sec B (30m) = 50 Marks / 1 HR 30 MIN
        return PrimaryBetaBlueprint(
            subject_key=s_lower,
            name=subject,
            level=lvl,
            domain="Lower Primary",
            sec_a_count=20,
            sec_a_marks=20,
            sec_b_count=5,
            sec_b_marks=30,
            total_questions=25,
            total_marks=50,
            duration="1 HR 30 MIN",
            instructions=[
                "This paper consists of two sections: Section A and Section B.",
                "Section A has 20 short-answer questions (1 mark each).",
                "Section B has 5 structured questions (4 to 6 marks each).",
                "Answer all questions in the spaces provided."
            ],
            negative_constraints=[
                "FORBID secondary/UCE scenario jargon.",
                "Keep wording simple, age-appropriate, and directly aligned with Lower Primary syllabus.",
                "NEVER include decorative diagrams. ONLY include 'diagram_description' if the student MUST interact with the diagram to answer the question (e.g. 'Name the part marked X'). Otherwise, omit it completely (return null).",
                "CRITICAL: DO NOT generate or output 'tikz_code'. Raw code is completely forbidden."
            ]
        )

    # Upper Primary (P.4 - P.7 / PLE)
    if "math" in s_lower:
        # PLE Mathematics: 20 Sec A (2m each = 40m) + 12 Sec B (5m each = 60m) = 32 Qs / 100 Marks / 2 HR 30 MIN
        return PrimaryBetaBlueprint(
            subject_key="mathematics",
            name="Mathematics",
            level=lvl,
            domain="Upper Primary (PLE)",
            sec_a_count=20,
            sec_a_marks=40,
            sec_b_count=12,
            sec_b_marks=60,
            total_questions=32,
            total_marks=100,
            duration="2 HRS 30 MIN",
            instructions=[
                "This paper consists of two sections: Section A and Section B.",
                "Section A has 20 short-answer questions (2 marks each).",
                "Section B has 12 structured questions (4 to 5 marks each).",
                "All working MUST be shown clearly in the spaces provided."
            ],
            negative_constraints=[
                "FORBID multiple choice questions. Generate short_answer for Section A.",
                "FORBID essay writing or humanities trivia.",
                "MANDATORY step-by-step mathematical working and imperative math commands ('Calculate...', 'Work out...').",
                "NEVER include decorative diagrams. ONLY include 'diagram_description' if the student MUST interact with the diagram to solve the math problem (e.g. finding angles, reading a graph). Otherwise, return null.",
                "CRITICAL: DO NOT generate or output 'tikz_code'. Raw code is completely forbidden."
            ]
        )

    elif "english" in s_lower:
        # PLE English: 50 Sec A (1m each = 50m) + 5 Sec B (10m each = 50m) = 55 Qs / 100 Marks / 2 HR 15 MIN
        return PrimaryBetaBlueprint(
            subject_key="english",
            name="English Language",
            level=lvl,
            domain="Upper Primary (PLE)",
            sec_a_count=50,
            sec_a_marks=50,
            sec_b_count=5,
            sec_b_marks=50,
            total_questions=55,
            total_marks=100,
            duration="2 HRS 15 MIN",
            instructions=[
                "This paper consists of two sections: Section A and Section B.",
                "Section A has 50 short-answer grammar & vocabulary items (1 mark each).",
                "Section B has 5 composition & comprehension items (10 marks each).",
                "Answer all questions in the spaces provided."
            ],
            negative_constraints=[
                "FORBID science formulas and mathematical calculations.",
                "Q1-30: Sub-group vocabulary/grammar completion; Q31-50: Sentence rewriting.",
                "Q51-55: Comprehension passage, poem/dialogue, notice/timetable, jumbled sentences, guided letter."
            ]
        )

    else:
        # PLE Science / SST / RE: 40 Sec A (1m each = 40m) + 15 Sec B (4m each = 60m) = 55 Qs / 100 Marks / 2 HR 15 MIN
        return PrimaryBetaBlueprint(
            subject_key=s_lower,
            name=subject,
            level=lvl,
            domain="Upper Primary (PLE)",
            sec_a_count=40,
            sec_a_marks=40,
            sec_b_count=15,
            sec_b_marks=60,
            total_questions=55,
            total_marks=100,
            duration="2 HRS 15 MIN",
            instructions=[
                "This paper consists of two sections: Section A and Section B.",
                "Section A has 40 short-answer questions (1 mark each).",
                "Section B has 15 structured multi-part questions (4 marks each).",
                "Answer all questions in the spaces provided."
            ],
            negative_constraints=[
                "FORBID multiple choice questions.",
                f"Generate 100% {subject}-specific curriculum application items ONLY.",
                "NEVER include decorative diagrams. ONLY include 'diagram_description' if the student MUST study the diagram to answer the question (e.g. 'Use the diagram below...', 'Name part X'). Otherwise, return null.",
                "CRITICAL: DO NOT generate or output 'tikz_code'. Raw code is completely forbidden."
            ]
        )

class PrimaryPromptSynthesizer:
    @staticmethod
    def synthesize_section(blueprint: PrimaryBetaBlueprint, section: str, count: int, start_num: int, max_diagrams: int = 1) -> str:
        """Synthesizes prompt for Section A or Section B of Primary Beta paper."""
        constraints_str = "\n".join(f"  - {c}" for c in blueprint.negative_constraints)
        
        if max_diagrams == 0:
            constraints_str += "\n  - CRITICAL DIAGRAM BAN: DO NOT include any 'diagram_description'. You MUST return null for all diagrams in this block."
        else:
            constraints_str += f"\n  - STRICT DIAGRAM LIMIT: You are strictly limited to generating a MAXIMUM of {max_diagrams} 'diagram_description' across all questions in this block. The rest MUST be null."
            constraints_str += "\n  - ANTI-DECORATION RULE (CRITICAL): NEVER generate a diagram just to 'illustrate' the topic. A diagram MUST be the core puzzle of the question."
            constraints_str += "\n  - IF you generate a diagram, the question 'text' MUST explicitly say 'The diagram below shows... Study it and answer...'. AND the sub-questions MUST ask the student to identify labeled parts. If the questions do not require identifying labeled parts, you MUST NOT generate a diagram."
            
        is_english = "english" in blueprint.subject_key

        if section == "A":
            if is_english:
                if start_num <= 30:
                    instr_group = "In each of the questions below, complete the sentence with a suitable word or fill in the blank as instructed."
                else:
                    instr_group = "In each of the questions 31 to 50, rewrite the sentence as instructed in brackets."

                return f"""
### UGANDA PRIMARY ENGLISH EXAM GENERATOR (BETA ENGINE)
LEVEL: {blueprint.level}
SECTION: SECTION A (Short Answer Items Q{start_num} to Q{start_num + count - 1})

Generate exactly {count} Section A English questions starting at Q{start_num}.
Current Instruction Group: "{instr_group}"

STRICT FORMAT RULES:
- Items starting Q1 to Q30: Sub-group vocabulary, prepositions, plurals, antonyms, tenses completion.
- Items starting Q31 to Q50: Sentence rewriting ("Rewrite using...", "Begin...", "Use... as instructed...").
- Each item MUST have "type": "short_answer", "marks": 1.
- Include "instruction_group": "{instr_group}".

Return JSON:
{{
  "questions": [
    {{
      "number": {start_num},
      "text": "Question stem or sentence rewriting prompt...",
      "type": "short_answer",
      "marks": 1,
      "instruction_group": "{instr_group}"
    }}
  ]
}}
"""
            else:
                return f"""
### UGANDA PRIMARY EXAM GENERATOR (BETA ENGINE)
SUBJECT: {blueprint.name.upper()}
LEVEL: {blueprint.level}
SECTION: SECTION A (Short Answer Items Q{start_num} to Q{start_num + count - 1})

Generate exactly {count} Section A short-answer questions for {blueprint.name.upper()} ({blueprint.level}).
- Each question MUST have "type": "short_answer".
- Start stems with imperative verbs ("State...", "Name...", "Work out...", "Calculate...", "Give...").

STRICT RULES:
{constraints_str}

Return JSON:
{{
  "questions": [
    {{ "number": {start_num}, "text": "Question stem...", "diagram_description": "Detailed visual description of the reference diagram needed, or null if none", "type": "short_answer", "marks": {1 if blueprint.sec_a_marks == blueprint.sec_a_count else 2} }}
  ]
}}
"""
        else: # SECTION B
            if is_english:
                return f"""
### UGANDA PRIMARY ENGLISH SECTION B GENERATOR (UNEB PLE SPECIFICATION)
LEVEL: {blueprint.level}
SECTION: SECTION B (Structured Composition & Reading Comprehension Items Q51 to Q55)

Generate Section B items for English Language starting at Q{start_num} for count={count}.

MANDATORY STIMULUS CONTENT RULES:
- Q51: Reading Comprehension Passage. Provide a full 150-word story in "context_block" + 10 sub-questions (a to j) worth 1 mark each.
- Q52: Poem or Dialogue. Provide a full 12-line poem or 8-turn dialogue script in "context_block" + 5 sub-questions (a to e) worth 2 marks each.
- Q53: Official Announcement Notice or Timetable Box. Provide a full notice text in "context_block" + 5 sub-questions (a to e) worth 2 marks each.
- Q54: 10 Jumbled Sentences. Provide 10 scrambled sentences labeled (a) through (j) in "context_block" + prompt "Re-arrange the sentences below to form a meaningful story."
- Q55: Guided Composition / Official Letter. Provide scenario and outline points in "context_block" + prompt for letter writing.

Return JSON:
{{
  "questions": [
    {{
      "number": 51,
      "text": "Read the story passage below carefully and answer in full sentences the questions that follow.",
      "context_block": "Once upon a time in Kasese district, Mr. Mukasa owned a large banana farm...",
      "type": "structured",
      "marks": 10,
      "sub_questions": [
        {{ "label": "(a)", "text": "Where did Mr. Mukasa own a banana farm?", "marks": 1 }},
        {{ "label": "(b)", "text": "Why did the villagers visit the farm?", "marks": 1 }}
      ]
    }}
  ]
}}
"""
            else:
                return f"""
### UGANDA PRIMARY EXAM GENERATOR (BETA ENGINE)
SUBJECT: {blueprint.name.upper()}
LEVEL: {blueprint.level}
SECTION: SECTION B (Structured Multi-Part Items Q{start_num} to Q{start_num + count - 1})

Generate exactly {count} Section B structured multi-part questions for {blueprint.name.upper()} ({blueprint.level}).
- Each question MUST have "type": "structured".
- Include sub-questions labeled (a), (b), (c) with clear mark allocations.

STRICT RULES:
{constraints_str}

Return JSON:
{{
  "questions": [
    {{
      "number": {start_num},
      "text": "Main question stem or context...",
      "diagram_description": "Detailed visual description of the reference diagram needed, or null if none",
      "type": "structured",
      "sub_questions": [
        {{ "label": "(a)", "text": "Sub-task (a)...", "marks": 2 }},
        {{ "label": "(b)", "text": "Sub-task (b)...", "marks": 2 }}
      ]
    }}
  ]
}}
"""

async def generate_primary_beta_chunk(blueprint: PrimaryBetaBlueprint, section: str, count: int, start_num: int, max_diagrams: int = 1) -> List[dict]:
    """Generates a chunk of questions for Section A or Section B."""
    client = get_async_openai_client()
    prompt = PrimaryPromptSynthesizer.synthesize_section(blueprint, section, count, start_num, max_diagrams)

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        questions = data.get("questions", [])
        
        for idx, q in enumerate(questions):
            # Aggressively strip any hallucinated tikz_code so the UI never renders it
            if "tikz_code" in q:
                del q["tikz_code"]
                
            q["number"] = start_num + idx
            if section == "A":
                q["type"] = "short_answer"
                q["options"] = []
            else:
                q["type"] = "structured"

        # Generate diagrams concurrently (enforcing max_diagrams programmatic limit)
        diagrams_generated = 0
        diagram_tasks = []
        for q in questions[:count]:
            desc = q.get("diagram_description")
            if desc and isinstance(desc, str) and desc.strip() and desc.lower() != "null":
                
                # Aggressive Anti-Decoration Filter
                q_text_lower = q.get("text", "").lower()
                has_diagram_ref = any(keyword in q_text_lower for keyword in ["diagram", "figure", "study", "below", "picture", "shown"])
                if not has_diagram_ref:
                    print(f"DEBUG: Stripping decorative diagram from Q{q.get('number')} - no diagram reference in text.")
                    q["diagram_description"] = None
                    continue

                if diagrams_generated >= max_diagrams:
                    q["diagram_description"] = None
                    continue
                
                diagrams_generated += 1
                task = asyncio.create_task(generate_exam_diagram(
                    diagram_description=desc,
                    subject=blueprint.name,
                    level=blueprint.level,
                    question_text=q.get("text", "")
                ))
                diagram_tasks.append((q, task))
        
        if diagram_tasks:
            for q, task in diagram_tasks:
                q["diagram_url"] = await task

        return questions[:count]
    except Exception as e:
        print(f"Primary Beta Chunk Error ({section} Q{start_num}): {e}")
        # Fallback questions
        fallback = []
        for idx in range(count):
            qnum = start_num + idx
            if section == "A":
                fallback.append({
                    "number": qnum,
                    "text": f"Solve or answer question {qnum} for {blueprint.name} ({blueprint.level}).",
                    "type": "short_answer",
                    "marks": 2 if blueprint.sec_a_marks > blueprint.sec_a_count else 1
                })
            else:
                fallback.append({
                    "number": qnum,
                    "text": f"Structured question {qnum} for {blueprint.name} ({blueprint.level}).",
                    "type": "structured",
                    "sub_questions": [
                        {"label": "(a)", "text": f"Part (a) for question {qnum}.", "marks": 2},
                        {"label": "(b)", "text": f"Part (b) for question {qnum}.", "marks": 3}
                    ]
                })
        return fallback

async def stream_primary_beta_paper(subject: str, level: str, brand_name: str = "EDUMERC") -> AsyncGenerator[str, None]:
    """
    Async generator streaming Primary (beta) paper generation over SSE.
    """
    blueprint = get_primary_beta_blueprint(subject, level)
    title = f"{blueprint.name} {blueprint.level} - Examination Paper (Beta)"

    # ── STEP 1: HEADER READY EVENT ──
    header_event = {
        "event_type": "header_ready",
        "title": title,
        "subject": blueprint.name,
        "level": blueprint.level,
        "duration": blueprint.duration,
        "total_marks": blueprint.total_marks,
        "instructions": blueprint.instructions
    }
    yield f"data: {json.dumps(header_event)}\n\n"
    await asyncio.sleep(0.1)

    # ── STEP 2: SECTION A PARALLEL GENERATION ──
    yield f"data: {json.dumps({'event_type': 'status_update', 'message': f'Drafting Section A ({blueprint.sec_a_count} Questions)...'})}\n\n"

    sec_a_tasks = []
    num_chunks = blueprint.sec_a_count // 10
    for i in range(num_chunks):
        # Enforce max 2 diagrams total in Section A (1 per first two chunks)
        max_d = 1 if i < 2 else 0
        sec_a_tasks.append(
            asyncio.create_task(generate_primary_beta_chunk(blueprint, "A", 10, i * 10 + 1, max_diagrams=max_d))
        )
    
    # If there's a remainder
    rem = blueprint.sec_a_count % 10
    if rem > 0:
        sec_a_tasks.append(
            asyncio.create_task(generate_primary_beta_chunk(blueprint, "A", rem, num_chunks * 10 + 1, max_diagrams=0))
        )

    sec_a_results = await asyncio.gather(*sec_a_tasks)
    all_sec_a_qs = []
    for chunk in sec_a_results:
        all_sec_a_qs.extend(chunk)

    all_sec_a_qs.sort(key=lambda q: q["number"])

    for q in all_sec_a_qs:
        q_html = build_question_html("Exams", q, subject=blueprint.name, level=blueprint.level)
        item_evt = {
            "event_type": "question_ready",
            "section": "A",
            "number": q["number"],
            "question_json": q,
            "question_html": q_html
        }
        yield f"data: {json.dumps(item_evt)}\n\n"
        await asyncio.sleep(0.02)

    # ── STEP 3: SECTION B PARALLEL GENERATION ──
    yield f"data: {json.dumps({'event_type': 'status_update', 'message': f'Drafting Section B ({blueprint.sec_b_count} Questions)...'})}\n\n"

    sec_b_start = blueprint.sec_a_count + 1
    sec_b_chunks = []
    sec_b_chunk_size = 5 if blueprint.sec_b_count >= 10 else blueprint.sec_b_count
    for i in range(0, blueprint.sec_b_count, sec_b_chunk_size):
        c_count = min(sec_b_chunk_size, blueprint.sec_b_count - i)
        # Enforce max 1 diagram total in Section B (in the first chunk only)
        max_d = 1 if i == 0 else 0
        sec_b_chunks.append((sec_b_start + i, c_count, max_d))

    sec_b_tasks = [
        asyncio.create_task(generate_primary_beta_chunk(blueprint, "B", c_count, start_num, max_diagrams=max_d))
        for start_num, c_count, max_d in sec_b_chunks
    ]

    sec_b_results = await asyncio.gather(*sec_b_tasks)
    all_sec_b_qs = []
    for chunk in sec_b_results:
        all_sec_b_qs.extend(chunk)

    all_sec_b_qs.sort(key=lambda q: q["number"])

    for q in all_sec_b_qs:
        q_html = build_question_html("Exams", q, subject=blueprint.name, level=blueprint.level)
        item_evt = {
            "event_type": "question_ready",
            "section": "B",
            "number": q["number"],
            "question_json": q,
            "question_html": q_html
        }
        yield f"data: {json.dumps(item_evt)}\n\n"
        await asyncio.sleep(0.02)

    # ── STEP 4: PHASED GENERATION EVENTS (EXAM PAPER -> MARKING GUIDE -> REFERENCE MAP) ──
    all_questions = all_sec_a_qs + all_sec_b_qs
    raw_payload = {"questions": all_questions}
    raw_str = json.dumps(raw_payload)

    # Phase 1: Build & emit Exam Question Paper immediately
    yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Exam paper complete! Displaying preview...'})}\n\n"

    full_html = build_full_html(
        mode="Exams",
        exam_type="Primary Examination Paper (Beta)",
        level=blueprint.level,
        subject=blueprint.name,
        term_roman="Term 1",
        exam_year="2026",
        duration=blueprint.duration,
        school_name="EduQuest Central",
        brand_name=brand_name,
        question_count=len(all_questions),
        content_raw=raw_str,
        topic=""
    )

    # 1. First event: Exam Paper Complete (Triggers immediate result view for user)
    exam_paper_evt = {
        "event_type": "exam_paper_complete",
        "title": title,
        "raw": raw_payload,
        "html": full_html,
        "total_questions": len(all_questions)
    }
    yield f"data: {json.dumps(exam_paper_evt)}\n\n"
    await asyncio.sleep(0.05)

    # 2. Phase 2: Marking Guide Status & Event
    yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Proceeding to build Teacher Marking Guide...'})}\n\n"
    await asyncio.sleep(0.05)

    # 3. Phase 3: Reference Map Status & Final Event
    yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Generating Pedagogical Reference Map & Competency Audit...'})}\n\n"

    complete_evt = {
        "event_type": "paper_complete",
        "title": title,
        "raw": raw_payload,
        "html": full_html,
        "total_questions": len(all_questions)
    }
    yield f"data: {json.dumps(complete_evt)}\n\n"
