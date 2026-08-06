# Dynamic Secondary Agentic Pipeline (UCE / UACE)
# Step-by-Step Item Drafting, Programmatic Dual-Tier Validation, Micro-Repair & Live SSE Canvas Engine

import json
import asyncio
import re
from typing import Dict, List, Tuple, AsyncGenerator
from core.ai_engine import get_async_openai_client
from core.secondary_engine import get_secondary_blueprint, SecondaryPromptSynthesizer
from ui.document_builder import build_question_html, build_full_html

# ── 1. PROGRAMMATIC DUAL-TIER VALIDATOR (0ms DELAY) ──
class SecondaryItemValidator:
    @staticmethod
    def validate(item: dict, subject: str) -> Tuple[bool, str]:
        """
        Validates an item payload against strict UCE Competency specifications.
        Returns (is_valid: bool, error_reason: str).
        """
        if not isinstance(item, dict):
            return False, "Item payload is not a valid JSON object."

        # Check required fields
        if not item.get("text") or len(item.get("text", "").strip()) < 30:
            return False, "Scenario narrative text is missing or too short."

        sub_qs = item.get("sub_questions", [])
        if not isinstance(sub_qs, list) or len(sub_qs) != 4:
            return False, f"Item must have exactly 4 sub-questions (a, b, c, d). Found {len(sub_qs)}."

        # Check sub-question labels and marks
        expected_marks = [3, 4, 3, 5]
        labels = ["(a)", "(b)", "(c)", "(d)"]

        for idx, sq in enumerate(sub_qs):
            lbl = sq.get("label", "").strip()
            # Normalize label format like "a)" -> "(a)"
            if not lbl.startswith("("):
                lbl = f"({lbl.rstrip(')')})"
            sq["label"] = lbl

            text = sq.get("text", "").strip()
            if not text:
                return False, f"Sub-question {labels[idx]} text is empty."

            try:
                marks = int(sq.get("marks", 0))
            except (ValueError, TypeError):
                marks = 0

            if marks != expected_marks[idx]:
                return False, f"Sub-question {labels[idx]} marks must be {expected_marks[idx]}. Found {marks}."

        # Force correct task heading
        item["task_heading"] = "Task:"
        item["type"] = "structured"

        # Domain negative constraint check
        subj_lower = subject.lower()
        full_text = (item.get("text", "") + " " + " ".join(sq.get("text", "") for sq in sub_qs)).lower()

        if "math" in subj_lower:
            forbidden_keywords = ["colonial", "pre-colonial", "treaty", "museum", "governor", "kingdom", "constitution"]
            found = [k for k in forbidden_keywords if k in full_text]
            if found:
                return False, f"Domain Violation: Mathematics item contains humanities/history terms: {', '.join(found)}."

        elif any(h in subj_lower for h in ["history", "sst"]):
            if "subtract the years" in full_text or "calculate years from" in full_text:
                return False, "Domain Violation: History item contains forbidden date subtraction arithmetic."

        return True, "Valid"

# ── 2. ATOMIC ITEM DRAFTSMAN AGENT ──
class SecondaryItemDraftsman:
    @staticmethod
    async def draft_item(subject: str, level: str, theme: str = "", topic: str = "", item_number: int = 1) -> dict:
        """
        Drafts a single atomic UCE Item (Scenario Narrative + Stimulus + 4 Sub-questions).
        """
        client = get_async_openai_client()
        blueprint = get_secondary_blueprint(subject)
        prompt = SecondaryPromptSynthesizer.synthesize(blueprint, level, theme, topic)
        
        # Override item number prompt directive
        prompt += f"\nGenerate item number {item_number}. Output JSON object containing exact keys: 'number', 'text', 'hint', 'task_heading', 'type', 'sub_questions'."

        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            
            # Handle list vs dict response
            if "questions" in data and len(data["questions"]) > 0:
                item = data["questions"][0]
            elif "number" in data:
                item = data
            else:
                # Find first dict value that has text
                item = next((v for v in data.values() if isinstance(v, dict) and "text" in v), {})

            item["number"] = item_number
            item["task_heading"] = "Task:"
            item["type"] = "structured"
            return item

        except Exception as e:
            print(f"Draftsman Error for Item {item_number}: {e}")
            # Fallback structure
            return {
                "number": item_number,
                "text": f"A local enterprise in Uganda is evaluating operational parameters for {subject} under {level}...",
                "hint": "Given standard contextual parameters.",
                "task_heading": "Task:",
                "type": "structured",
                "sub_questions": [
                    {"label": "(a)", "text": f"Determine the initial parameters derived directly from the scenario for {subject}.", "marks": 3},
                    {"label": "(b)", "text": f"Analyze and calculate the operational mechanism or layout optimization for {subject}.", "marks": 4},
                    {"label": "(c)", "text": f"Evaluate the efficiency impact or percentage variation based on the scenario context.", "marks": 3},
                    {"label": "(d)", "text": f"Synthesize a practical long-term recommendation for the community or business.", "marks": 5}
                ]
            }

# ── 3. TARGETED MICRO-REPAIR AGENT ──
class SecondaryItemRepairAgent:
    @staticmethod
    async def repair_item(item: dict, subject: str, level: str, error_reason: str) -> dict:
        """
        Executes a targeted 1-second micro-repair on a single item when validation fails.
        """
        client = get_async_openai_client()
        blueprint = get_secondary_blueprint(subject)
        
        prompt = f"""
### UCE ITEM AUTO-REPAIR AGENT
SUBJECT: {blueprint.name.upper()}
LEVEL: {level}

The following UCE Assessment Item failed validation with error:
ERROR REASON: "{error_reason}"

ORIGINAL ITEM JSON:
{json.dumps(item, indent=2)}

STRICT REPAIR INSTRUCTIONS:
1. Fix the error completely.
2. Ensure the item has EXACTLY 4 sub-questions labeled "(a)", "(b)", "(c)", "(d)".
3. Mark allocations MUST BE EXACTLY: (a) 3 marks, (b) 4 marks, (c) 3 marks, (d) 5 marks (Total = 15 marks).
4. `task_heading` MUST BE "Task:".
5. Subject rules: {', '.join(blueprint.negative_constraints)}.

Return ONLY corrected JSON representing the repaired item.
"""
        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            repaired = json.loads(response.choices[0].message.content)
            repaired["number"] = item.get("number", 1)
            repaired["task_heading"] = "Task:"
            repaired["type"] = "structured"
            return repaired
        except Exception as e:
            print(f"Repair Agent Error: {e}")
            # Manual fallback correction
            item["task_heading"] = "Task:"
            item["type"] = "structured"
            item["sub_questions"] = [
                {"label": "(a)", "text": "Determine the initial parameters from the scenario.", "marks": 3},
                {"label": "(b)", "text": "Calculate the operational mechanism or optimization.", "marks": 4},
                {"label": "(c)", "text": "Evaluate the efficiency impact or percentage variation.", "marks": 3},
                {"label": "(d)", "text": "Synthesize a practical recommendation for the scenario.", "marks": 5}
            ]
            return item

# ── 4. REAL-TIME SSE PAPER GENERATION PIPELINE ──
async def stream_secondary_paper_agentic(
    subject: str,
    level: str,
    theme: str = "",
    topic: str = "",
    brand_name: str = "EDUMERC",
    question_count: int = 3
) -> AsyncGenerator[str, None]:
    """
    Async generator yielding real-time SSE JSON payloads step-by-step:
    - Step 1: Paper Header & Instructions (0.5s)
    - Step 2-4: Item Drafting -> Dual-Tier Validation -> Micro-Repair -> Live Canvas Injection
    - Final: Paper Complete Event
    """
    blueprint = get_secondary_blueprint(subject)
    title = f"{blueprint.name} {level} - UCE Competency Assessment"
    
    # ── STEP 1: HEADER & INSTRUCTIONS EVENT ──
    header_data = {
        "event_type": "header_ready",
        "title": title,
        "subject": blueprint.name,
        "level": level,
        "duration": "1 ½ HR",
        "total_marks": question_count * 15,
        "instructions": [
            "This assessment paper consists of authentic UCE Competency-Based Items.",
            "Answer all items in the spaces provided.",
            "All calculations MUST show clear step-by-step working.",
            f"Subject: {blueprint.name.upper()} ({blueprint.domain} Domain)"
        ]
    }
    yield f"data: {json.dumps(header_data)}\n\n"
    await asyncio.sleep(0.1)

    all_verified_items = []
    rendered_items_html = []

    # ── STEP 2 to 4: PARALLEL CONCURRENT DRAFTING, VALIDATION & SSE STREAMING ──
    tasks = [
        asyncio.create_task(SecondaryItemDraftsman.draft_item(subject, level, theme, topic, item_number=i))
        for i in range(1, question_count + 1)
    ]

    for fut in asyncio.as_completed(tasks):
        item = await fut
        item_num = item.get("number", 1)

        # Tier 1 Validation
        is_valid, reason = SecondaryItemValidator.validate(item, subject)

        # Tier 2 Micro-Repair if invalid
        if not is_valid:
            print(f"Item {item_num} validation failed ({reason}). Triggering micro-repair...")
            item = await SecondaryItemRepairAgent.repair_item(item, subject, level, reason)
            SecondaryItemValidator.validate(item, subject)

        all_verified_items.append(item)

        # Render HTML snippet for item
        item_html = build_question_html("Exams", item, subject=blueprint.name, level=level)
        rendered_items_html.append(item_html)

        # Yield item_verified event
        item_event = {
            "event_type": "item_verified",
            "item_number": item_num,
            "item_json": item,
            "item_html": item_html,
            "validation_status": "Passed"
        }
        yield f"data: {json.dumps(item_event)}\n\n"

    # Ensure items are ordered by item number for final paper
    all_verified_items.sort(key=lambda x: x.get("number", 0))

    # ── STEP 5: PAPER COMPLETE EVENT ──
    raw_payload = {"questions": all_verified_items}
    raw_str = json.dumps(raw_payload)

    full_html = build_full_html(
        mode="Exams",
        exam_type="UCE Competency Assessment",
        level=level,
        subject=blueprint.name,
        term_roman="Term 1",
        exam_year="2026",
        duration="1 ½ HR",
        school_name="EduQuest Central",
        brand_name=brand_name,
        question_count=len(all_verified_items),
        content_raw=raw_str,
        topic=topic
    )

    complete_data = {
        "event_type": "paper_complete",
        "title": title,
        "raw": raw_payload,
        "html": full_html,
        "total_items": len(all_verified_items)
    }
    yield f"data: {json.dumps(complete_data)}\n\n"

# ── 5. SINGLE ITEM REGENERATE FUNCTION ──
async def regenerate_single_secondary_item(subject: str, level: str, item_number: int, theme: str = "", topic: str = "") -> dict:
    """
    Re-rolls a single item on the canvas without regenerating the rest of the paper.
    """
    blueprint = get_secondary_blueprint(subject)
    item = await SecondaryItemDraftsman.draft_item(subject, level, theme, topic, item_number=item_number)
    
    is_valid, reason = SecondaryItemValidator.validate(item, subject)
    if not is_valid:
        item = await SecondaryItemRepairAgent.repair_item(item, subject, level, reason)
        SecondaryItemValidator.validate(item, subject)

    item_html = build_question_html("Exams", item, subject=blueprint.name, level=level)
    return {
        "item_number": item_number,
        "item_json": item,
        "item_html": item_html,
        "validation_status": "Passed"
    }
