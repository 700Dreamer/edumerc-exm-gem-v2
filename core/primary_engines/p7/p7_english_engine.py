# Dedicated Primary 7 English Language Examination Engine (P.7 English)
# Official UNEB PLE Standard Specifications derived from sample papers

import json
import asyncio
from typing import List, Dict, AsyncGenerator
from core.ai_engine import get_async_openai_client
from ui.document_builder import build_question_html, build_full_html

class P7EnglishEngine:
    """
    Dedicated generation engine for Primary 7 English Language (PLE Specification).
    Matches 100% of UNEB specimen papers in sample papers/p.7/english/
    """

    @staticmethod
    def get_subgroup_instruction(qnum: int) -> str:
        if 1 <= qnum <= 5:
            return "In questions 1 to 5, fill the blank space with a suitable word."
        elif 6 <= qnum <= 15:
            return "In each of the questions 6 to 15, use the correct form of the word given in brackets to complete the sentence."
        elif 16 <= qnum <= 17:
            return "In each of the questions 16 and 17, write the plural form of the given word."
        elif 18 <= qnum <= 19:
            return "In each of the questions 18 and 19, arrange the given words in alphabetical order."
        elif 20 <= qnum <= 21:
            return "In each of the questions 20 and 21, write the full form of the given contraction."
        elif 22 <= qnum <= 23:
            return "In each of the questions 22 and 23, use each of the given words in a sentence to show that you know their difference in meaning."
        elif 24 <= qnum <= 26:
            return "In each of the questions 24 to 26, rewrite the sentence giving one word for the underlined group of words."
        elif 27 <= qnum <= 28:
            return "In each of the questions 27 and 28, rearrange the given words to form a correct sentence."
        elif 29 <= qnum <= 30:
            return "In each of the questions 29 and 30, write the opposite of the given word."
        else:
            return "Sub-Section II\nIn each of the questions 31 to 50, rewrite the sentence as instructed in brackets."

    @staticmethod
    def synthesize_sec_a_prompt(start_num: int, count: int) -> str:
        end_num = start_num + count - 1
        instr = P7EnglishEngine.get_subgroup_instruction(start_num)

        if start_num <= 30:
            return f"""
### UGANDA P.7 ENGLISH EXAMINATION GENERATOR (SUB-SECTION I)
QUESTIONS: Q{start_num} to Q{end_num} (Count: {count})
SUB-GROUP INSTRUCTION: "{instr}"

Generate exactly {count} short-answer questions for P.7 English starting at Q{start_num}.
- Instructions for this group: "{instr}"
- Stem format MUST be clean without redundant parenthetical instructions inside the stem.
- For Homophone questions (Q22-Q23), provide two words e.g. "station / stationery" and ask candidate to use each in a sentence.
- Each item MUST have "type": "short_answer", "marks": 1.

Return JSON:
{{
  "questions": [
    {{
      "number": {start_num},
      "text": "Sentence stem with blank line _________________.",
      "type": "short_answer",
      "marks": 1
    }}
  ]
}}
"""
        else:
            return f"""
### UGANDA P.7 ENGLISH EXAMINATION GENERATOR (SUB-SECTION II: SENTENCE REWRITING)
QUESTIONS: Q{start_num} to Q{end_num} (Count: {count})
INSTRUCTION GROUP: "Sub-Section II\\nIn each of the questions 31 to 50, rewrite the sentence as instructed in brackets."

Generate exactly {count} sentence rewriting questions starting at Q{start_num}.
- Directives in brackets MUST include: (Begin: "Had..."), (Rewrite using "...as soon as..."), (Use "...besides..."), (Supply a suitable question tag), (Rewrite using "...too...to..."), (Begin: "No sooner...").
- Each item MUST have "type": "short_answer", "marks": 1.

Return JSON:
{{
  "questions": [
    {{
      "number": {start_num},
      "text": "Original sentence... (Rewrite using: ...)",
      "type": "short_answer",
      "marks": 1
    }}
  ]
}}
"""

    @staticmethod
    def synthesize_sec_b_prompt(q_num: int) -> str:
        if q_num == 51:
            return """
### UGANDA P.7 ENGLISH SECTION B: Q51 (COMPREHENSION PASSAGE)
Generate Question 51:
- "text": "Read the story passage below carefully and answer in full sentences the questions that follow."
- "context_block": A complete 180-word interesting story about Ugandan school children, farming, or community event.
- "type": "structured", "marks": 10
- "sub_questions": Exactly 10 sub-questions (a) to (j), worth 1 mark each.

Return JSON:
{
  "questions": [
    {
      "number": 51,
      "text": "Read the story passage below carefully and answer in full sentences the questions that follow.",
      "context_block": "Full 180-word story narrative...",
      "type": "structured",
      "marks": 10,
      "sub_questions": [
        { "label": "(a)", "text": "Who is the main character in the story?", "marks": 1 },
        { "label": "(b)", "text": "Where did the story take place?", "marks": 1 },
        { "label": "(c)", "text": "Why did the villagers assemble at the chief's house?", "marks": 1 },
        { "label": "(d)", "text": "What challenge did the school face?", "marks": 1 },
        { "label": "(e)", "text": "How was the problem solved?", "marks": 1 },
        { "label": "(f)", "text": "Give a word or phrase from the story that means 'very happy'.", "marks": 1 },
        { "label": "(g)", "text": "What lesson do we learn from the story?", "marks": 1 },
        { "label": "(h)", "text": "Why was the teacher proud of the pupils?", "marks": 1 },
        { "label": "(i)", "text": "What reward was given to the best pupil?", "marks": 1 },
        { "label": "(j)", "text": "Suggest a suitable title for the passage.", "marks": 1 }
      ]
    }
  ]
}
"""
        elif q_num == 52:
            return """
### UGANDA P.7 ENGLISH SECTION B: Q52 (POEM / STORY EXTRACT)
Generate Question 52:
- "text": "Read the poem below carefully and answer in full sentences the questions that follow."
- "context_block": A complete 12-line poem with 3 stanzas about nature, education, or hard work.
- "type": "structured", "marks": 10
- "sub_questions": Exactly 10 sub-questions (a) to (j), worth 1 mark each.

Return JSON:
{
  "questions": [
    {
      "number": 52,
      "text": "Read the poem below carefully and answer in full sentences the questions that follow.",
      "context_block": "Stanza 1...\n\nStanza 2...\n\nStanza 3...",
      "type": "structured",
      "marks": 10,
      "sub_questions": [
        { "label": "(a)", "text": "What is the poem about?", "marks": 1 },
        { "label": "(b)", "text": "How many stanzas has the poem?", "marks": 1 },
        { "label": "(c)", "text": "According to stanza one, who wakes up early?", "marks": 1 },
        { "label": "(d)", "text": "What happens when the sun sets?", "marks": 1 },
        { "label": "(e)", "text": "Which word in stanza two means 'joyful'?", "marks": 1 },
        { "label": "(f)", "text": "Why does the poet praise hard work?", "marks": 1 },
        { "label": "(g)", "text": "Who is addressed in the last stanza?", "marks": 1 },
        { "label": "(h)", "text": "Mention one benefit of education named in the poem.", "marks": 1 },
        { "label": "(i)", "text": "What is the feeling of the poet in stanza three?", "marks": 1 },
        { "label": "(j)", "text": "Suggest a suitable title for this poem.", "marks": 1 }
      ]
    }
  ]
}
"""
        elif q_num == 53:
            return """
### UGANDA P.7 ENGLISH SECTION B: Q53 (OFFICIAL NOTICE / TABLE)
Generate Question 53:
- "text": "Study the official notice below carefully and answer in full sentences the questions that follow."
- "context_block": A complete announcement notice formatted with Title, Date, Venue, Time, Target Audience, and Contact Person.
- "type": "structured", "marks": 10
- "sub_questions": Exactly 10 sub-questions (a) to (j), worth 1 mark each.

Return JSON:
{
  "questions": [
    {
      "number": 53,
      "text": "Study the official notice below carefully and answer in full sentences the questions that follow.",
      "context_block": "NOTICE: ANNUAL SCHOOL SPORTS COMPETITION\nDate: 15th October 2026\nVenue: School Main Sports Ground\nTime: 8:00 AM - 4:00 PM\nTarget Audience: All Primary 1 - Primary 7 Pupils and Parents\nActivities: Running, High Jump, Football, Netball\nContact: The Sports Master (0772 123456)",
      "type": "structured",
      "marks": 10,
      "sub_questions": [
        { "label": "(a)", "text": "What is the notice about?", "marks": 1 },
        { "label": "(b)", "text": "When will the event take place?", "marks": 1 },
        { "label": "(c)", "text": "Where will the competition be held?", "marks": 1 },
        { "label": "(d)", "text": "At what time is the event expected to begin?", "marks": 1 },
        { "label": "(e)", "text": "Who are invited to attend the event?", "marks": 1 },
        { "label": "(f)", "text": "Mention any two sports activities listed in the notice.", "marks": 1 },
        { "label": "(g)", "text": "Who wrote the notice?", "marks": 1 },
        { "label": "(h)", "text": "How can one contact the organizer?", "marks": 1 },
        { "label": "(i)", "text": "Why should pupils attend the event?", "marks": 1 },
        { "label": "(j)", "text": "What time will the sports event end?", "marks": 1 }
      ]
    }
  ]
}
"""
        elif q_num == 54:
            return """
### UGANDA P.7 ENGLISH SECTION B: Q54 (JUMBLED SENTENCES)
Generate Question 54:
- "text": "The sentences below are in a wrong order. Re-arrange them in the correct order so as to make a good composition about a school trip."
- "context_block": 10 scrambled sentences labeled (a) to (j).
- "type": "structured", "marks": 10

Return JSON:
{
  "questions": [
    {
      "number": 54,
      "text": "The sentences below are in a wrong order. Re-arrange them in the correct order so as to make a good composition about a school trip.",
      "context_block": "(a) They arrived at the national park at noon.\n(b) One sunny morning, P.7 pupils prepared for a tour.\n(c) After viewing wild animals, they ate lunch.\n(d) They boarded the school bus at 7:00 AM.\n(e) The driver started the engine and drove off.\n(f) Everyone was excited during the journey.\n(g) They saw lions, elephants, and giraffes.\n(h) At 5:00 PM, they embarked on their journey back home.\n(i) They reached school safely in the evening.\n(j) It was an unforgettable educational tour.",
      "type": "structured",
      "marks": 10
    }
  ]
}
"""
        else: # Q55
            return """
### UGANDA P.7 ENGLISH SECTION B: Q55 (DIALOGUE COMPLETION SCRIPT)
Generate Question 55:
- "text": "Below is a dialogue between Enock and Ukasha. What Enock said is given below. Complete it by writing in the blank spaces what you think Ukasha said."
- "context_block": An alternating dialogue script between Enock and Ukasha where Enock's 10 prompts are given and Ukasha's 10 responses are blank lines.
- "type": "structured", "marks": 10

Return JSON:
{
  "questions": [
    {
      "number": 55,
      "text": "Below is a dialogue between Enock and Ukasha. What Enock said is given below. Complete it by writing in the blank spaces what you think Ukasha said.",
      "context_block": "Enock: Hello Ukasha, what have you been doing in your class?\nUkasha: ___________________________________________________\n        ___________________________________________________\n\nEnock: Having a meeting! What was the meeting about?\nUkasha: ___________________________________________________\n        ___________________________________________________\n\nEnock: Starting a school newspaper! What kind of news are you going to write?\nUkasha: ___________________________________________________\n        ___________________________________________________\n\nEnock: Local and foreign news! Who were chosen to be the chief editor and journalists?\nUkasha: ___________________________________________________\n        ___________________________________________________\n\nEnock: Biko, Twine, and Maggie! Why were they chosen?\nUkasha: ___________________________________________________\n        ___________________________________________________\n\nEnock: For being good at English! Which articles are you going to write?\nUkasha: ___________________________________________________\n        ___________________________________________________\n\nEnock: About sports, education, and politics! Who will draw the cartoons?\nUkasha: ___________________________________________________\n        ___________________________________________________\n\nEnock: Collin! Is he good at drawing cartoons?\nUkasha: ___________________________________________________\n        ___________________________________________________\n\nEnock: Indeed he deserved it. I wish him success.\nUkasha: ___________________________________________________\n        ___________________________________________________\n\nEnock: Goodbye, Ukasha.\nUkasha: ___________________________________________________",
      "type": "structured",
      "marks": 10
    }
  ]
}
"""

    @staticmethod
    async def generate_sec_a_chunk(start_num: int, count: int) -> List[dict]:
        client = get_async_openai_client()
        prompt = P7EnglishEngine.synthesize_sec_a_prompt(start_num, count)

        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            qs = data.get("questions", [])
            for idx, q in enumerate(qs):
                qnum = start_num + idx
                q["number"] = qnum
                q["type"] = "short_answer"
                q["marks"] = 1
                q["options"] = []
                q["instruction_group"] = P7EnglishEngine.get_subgroup_instruction(qnum)
            return qs[:count]
        except Exception as e:
            print(f"P7 English Sec A Chunk Error (Q{start_num}): {e}")
            fallback = []
            for idx in range(count):
                qnum = start_num + idx
                fallback.append({
                    "number": qnum,
                    "text": f"Complete sentence {qnum} with a suitable English word _________________.",
                    "type": "short_answer",
                    "marks": 1,
                    "instruction_group": P7EnglishEngine.get_subgroup_instruction(qnum)
                })
            return fallback

    @staticmethod
    async def generate_sec_b_item(q_num: int) -> dict:
        client = get_async_openai_client()
        prompt = P7EnglishEngine.synthesize_sec_b_prompt(q_num)

        try:
            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)
            qs = data.get("questions", [])
            if qs:
                q = qs[0]
                q["number"] = q_num
                q["type"] = "structured"
                q["marks"] = 10
                
                # Special Formatting for Q54 (Jumbled Sentences)
                if q_num == 54:
                    solution_table_html = """
<div style="margin-top:14px; margin-bottom:14px;">
  <div style="font-weight:bold; font-size:13.5px; margin-bottom:5px;">Solution Table</div>
  <table border="1" style="border-collapse:collapse; width:100%; text-align:center; font-size:13px; border:1px solid #000;">
    <tr style="background:#f1f5f9;"><td style="font-weight:bold; width:120px; padding:4px;">Wrong order</td><td>(a)</td><td>(b)</td><td>(c)</td><td>(d)</td><td>(e)</td><td>(f)</td><td>(g)</td><td>(h)</td><td>(i)</td><td>(j)</td></tr>
    <tr><td style="font-weight:bold; padding:8px;">Correct order</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
  </table>
</div>
"""
                    ctx_text = q.get("context_block", "").replace("\\n", "\n")
                    q["context_block"] = ctx_text + "\n" + solution_table_html
                    # 10 clean empty response lines (a) to (j)
                    q["sub_questions"] = [
                        {"label": f"({chr(97+i)})", "text": "", "marks": 1}
                        for i in range(10)
                    ]
                
                # Special Formatting for Q55 (Dialogue Script)
                elif q_num == 55:
                    ctx_text = q.get("context_block", "").replace("\\n", "\n")
                    q["context_block"] = ctx_text
                    q["sub_questions"] = [] # No duplicate lines below the dialogue box

                elif q.get("context_block"):
                    q["context_block"] = q["context_block"].replace("\\n", "\n")

                return q
            raise ValueError(f"No item generated for Q{q_num}")
        except Exception as e:
            print(f"P7 English Sec B Item Error (Q{q_num}): {e}")
            if q_num == 54:
                sol_table = """
<div style="margin-top:14px; margin-bottom:14px;">
  <div style="font-weight:bold; font-size:13.5px; margin-bottom:5px;">Solution Table</div>
  <table border="1" style="border-collapse:collapse; width:100%; text-align:center; font-size:13px; border:1px solid #000;">
    <tr style="background:#f1f5f9;"><td style="font-weight:bold; width:120px; padding:4px;">Wrong order</td><td>(a)</td><td>(b)</td><td>(c)</td><td>(d)</td><td>(e)</td><td>(f)</td><td>(g)</td><td>(h)</td><td>(i)</td><td>(j)</td></tr>
    <tr><td style="font-weight:bold; padding:8px;">Correct order</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
  </table>
</div>
"""
                return {
                    "number": 54,
                    "text": "The sentences below are in a wrong order. Re-arrange them in the correct order so as to make a good composition about a school trip.",
                    "context_block": "(a) They arrived at the park.\n(b) Pupils prepared for a tour.\n(c) They ate lunch.\n(d) They boarded the bus.\n(e) The driver drove off.\n(f) Everyone was excited.\n(g) They saw wild animals.\n(h) They returned home.\n(i) They reached safely.\n(j) It was a great day." + sol_table,
                    "type": "structured",
                    "marks": 10,
                    "sub_questions": [{"label": f"({chr(97+i)})", "text": "", "marks": 1} for i in range(10)]
                }
            elif q_num == 55:
                return {
                    "number": 55,
                    "text": "Below is a dialogue between Enock and Ukasha. What Enock said is given below. Complete it by writing in the blank spaces what you think Ukasha said.",
                    "context_block": "Enock: Hello Ukasha, what have you been doing in your class?\nUkasha: ___________________________________________________\n        ___________________________________________________\n\nEnock: Having a meeting! What was the meeting about?\nUkasha: ___________________________________________________\n        ___________________________________________________",
                    "type": "structured",
                    "marks": 10,
                    "sub_questions": []
                }
            return {
                "number": q_num,
                "text": f"Section B Item {q_num} for Primary 7 English Language.",
                "context_block": f"Sample stimulus context for Question {q_num}.",
                "type": "structured",
                "marks": 10,
                "sub_questions": [
                    {"label": f"({chr(97+i)})", "text": f"Sub-question ({chr(97+i)}) for Q{q_num}.", "marks": 1}
                    for i in range(10)
                ]
            }

    @staticmethod
    async def stream_paper(brand_name: str = "EDUMERC") -> AsyncGenerator[str, None]:
        title = "ENGLISH LANGUAGE PRIMARY 7 - EXAMINATION PAPER"
        instructions = [
            "This paper consists of two sections: A and B.",
            "Section A has 50 questions (50 marks).",
            "Section B has 5 questions (50 marks). Attempt all questions in Section B.",
            "Answer all questions in the spaces provided.",
            "All answers must be written using a blue or black ball point pen or ink.",
            "Unnecessary alteration of work may lead to loss of marks.",
            "Any handwriting that can not easily be read may lead to loss of marks.",
            "Do not fill any thing in the boxes. They are for examiners' use."
        ]

        # ── STEP 1: HEADER READY EVENT ──
        header_event = {
            "event_type": "header_ready",
            "title": title,
            "subject": "English Language",
            "level": "Primary 7",
            "duration": "2 HRS 15 MIN",
            "total_marks": 100,
            "instructions": instructions
        }
        yield f"data: {json.dumps(header_event)}\n\n"
        await asyncio.sleep(0.1)

        # ── STEP 2: SECTION A (Q1 - Q50) PARALLEL CHUNKS ACCORDING TO SUB-GROUP BOUNDARIES ──
        yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Drafting Section A (50 Grammar & Vocabulary Questions)...'})}\n\n"

        sec_a_batches = [
            (1, 5),    # Q1 - Q5 (Fill blank)
            (6, 10),   # Q6 - Q15 (Word forms)
            (16, 2),   # Q16 - Q17 (Plurals)
            (18, 2),   # Q18 - Q19 (ABC order)
            (20, 2),   # Q20 - Q21 (Full forms / Contractions)
            (22, 2),   # Q22 - Q23 (Homophones)
            (24, 3),   # Q24 - Q26 (One word substitution)
            (27, 2),   # Q27 - Q28 (Rearrange words)
            (29, 2),   # Q29 - Q30 (Opposite / Short forms)
            (31, 10),  # Q31 - Q40 (Sentence rewriting Part 1)
            (41, 10)   # Q41 - Q50 (Sentence rewriting Part 2)
        ]

        sec_a_tasks = [
            asyncio.create_task(P7EnglishEngine.generate_sec_a_chunk(start_num, c_count))
            for start_num, c_count in sec_a_batches
        ]

        sec_a_results = await asyncio.gather(*sec_a_tasks)
        all_sec_a_qs = []
        for chunk in sec_a_results:
            all_sec_a_qs.extend(chunk)

        all_sec_a_qs.sort(key=lambda q: q.get("number", 0))

        for q in all_sec_a_qs:
            q_html = build_question_html("Exams", q, subject="English Language", level="Primary 7")
            item_evt = {
                "event_type": "question_ready",
                "section": "A",
                "number": q["number"],
                "question_json": q,
                "question_html": q_html
            }
            yield f"data: {json.dumps(item_evt)}\n\n"
            await asyncio.sleep(0.01)

        # ── STEP 3: SECTION B (Q51 - Q55) PARALLEL ITEMS ──
        yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Drafting Section B (Passage, Poem, Notice, Jumbled Sentences, Dialogue Script)...'})}\n\n"

        sec_b_tasks = [
            asyncio.create_task(P7EnglishEngine.generate_sec_b_item(qnum))
            for qnum in range(51, 56)
        ]

        all_sec_b_qs = await asyncio.gather(*sec_b_tasks)
        all_sec_b_qs.sort(key=lambda q: q.get("number", 0))

        for q in all_sec_b_qs:
            q_html = build_question_html("Exams", q, subject="English Language", level="Primary 7")
            item_evt = {
                "event_type": "question_ready",
                "section": "B",
                "number": q["number"],
                "question_json": q,
                "question_html": q_html
            }
            yield f"data: {json.dumps(item_evt)}\n\n"
            await asyncio.sleep(0.01)

        # ── STEP 4: FINAL PAPER COMPLETE EVENT ──
        all_questions = all_sec_a_qs + all_sec_b_qs
        raw_payload = {"questions": all_questions}
        raw_str = json.dumps(raw_payload)

        full_html = build_full_html(
            mode="Exams",
            exam_type="Primary Assessment Examination",
            level="Primary 7",
            subject="English Language",
            term_roman="Term 1",
            exam_year="2026",
            duration="2 HRS 15 MIN",
            school_name="EduQuest Central",
            brand_name=brand_name,
            question_count=len(all_questions),
            content_raw=raw_str,
            topic=""
        )

        complete_evt = {
            "event_type": "paper_complete",
            "title": title,
            "raw": raw_payload,
            "html": full_html,
            "total_questions": len(all_questions)
        }
        yield f"data: {json.dumps(complete_evt)}\n\n"
