# Dedicated Primary 7 English Language Examination Engine (P.7 English)
# Official UNEB PLE Standard Specifications derived from sample papers in sample papers/p.7/english/

import json
import re
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
            return "In each of the questions 1 to 5, fill in the blank space with a suitable word."
        elif 6 <= qnum <= 15:
            return "In each of the questions 6 to 15, use the correct form of the word given in brackets to complete the sentence."
        elif 16 <= qnum <= 17:
            return "In questions 16 and 17, write the full form of the given abbreviation."
        elif 18 <= qnum <= 20:
            return "In questions 18 to 20, rewrite the sentences giving a single word for the underlined group of words."
        elif 21 <= qnum <= 22:
            return "For questions 21 and 22, rewrite the sentences giving the plural form of the underlined word."
        elif 23 <= qnum <= 24:
            return "In questions 23 and 24, use each of the given words in a sentence to show that you know their difference in meaning."
        elif 25 <= qnum <= 26:
            return "In questions 25 and 26, rearrange the given words to form a correct sentence."
        elif 27 <= qnum <= 28:
            return "In questions 27 and 28, rearrange the given words in alphabetical order."
        elif 29 <= qnum <= 30:
            return "For questions 29 and 30, rewrite the sentences giving the opposite of the underlined word."
        else:
            return "Sub-section II\nIn each of the questions 31 to 50, rewrite the sentences as instructed in brackets."

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
- For Homophones (Q23-24): Provide word pair e.g. "Weight / Wait" and ask candidate to use each in a sentence.
- For Underlined words (Q18-20, Q21-22, Q29-30): Wrap target words in HTML <u> tags e.g. "The referee told the player to <u>start again the game</u>."
- For Sentence Rearranging (Q25-26): Format words separated by slashes e.g. "how / to / know / I / ride / a / bicycle."
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
INSTRUCTION GROUP: "Sub-section II\\nIn each of the questions 31 to 50, rewrite the sentences as instructed in brackets."

Generate exactly {count} sentence rewriting questions starting at Q{start_num}.
- Directives in brackets MUST include: (Rewrite as one sentence using: ...... where ......), (Rewrite using: ...... mine), (Rewrite beginning: You must ......), (Rewrite beginning: Much as ......), (Rewrite beginning: If ......), (Rewrite without using "and" or "which"), (Rewrite using: ...... neither ...... nor ......), (Rewrite beginning: The candidates said ......), (Rewrite using: ...... just ......).
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
- "text": "Read the passage below carefully and then answer in full sentences the questions that follow."
- "context_block": A complete 180-word interesting story about Ugandan school children, farming, or community event.
- "type": "structured", "marks": 10
- "sub_questions": Exactly 10 sub-questions (a) to (j), worth 1 mark each.

Return JSON:
{
  "questions": [
    {
      "number": 51,
      "text": "Read the passage below carefully and then answer in full sentences the questions that follow.",
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
- "text": "Read the poem below carefully and then answer in full sentences the questions that follow."
- "context_block": A complete 12-line poem with 3 stanzas about sports, nature, or hard work.
- "type": "structured", "marks": 10
- "sub_questions": Exactly 10 sub-questions (a) to (j), worth 1 mark each.

Return JSON:
{
  "questions": [
    {
      "number": 52,
      "text": "Read the poem below carefully and then answer in full sentences the questions that follow.",
      "context_block": "A DREAM OF BEING A SPORTS CELEBRITY\n\nI must be a football champion,\nJust like Christiano Ronaldo the captain,\nWhose first goal helped Portugal,\nTo qualify for the 2004 World Cup.\n\nGrowing as an orphan is never a limit,\nI will make it just like Lionel Messi did,\nThe top scorer in the premier league ever,\nWho is paid highly and famous everywhere.\n\nI must be a real champion,\nDreaming to be the captain of Uganda Cranes,\nJust like Mbappe and his country France,\nThe best football dribbler in the world.",
      "type": "structured",
      "marks": 10,
      "sub_questions": [
        { "label": "(a)", "text": "What is the poem about?", "marks": 1 },
        { "label": "(b)", "text": "How many stanzas has the poem?", "marks": 1 },
        { "label": "(c)", "text": "Which sport is mentioned in the poem?", "marks": 1 },
        { "label": "(d)", "text": "Who is the captain of Portugal mentioned in stanza one?", "marks": 1 },
        { "label": "(e)", "text": "Which player grew up as an orphan according to stanza two?", "marks": 1 },
        { "label": "(f)", "text": "Why does the poet want to be like Lionel Messi?", "marks": 1 },
        { "label": "(g)", "text": "Which national team does the poet dream to captain?", "marks": 1 },
        { "label": "(h)", "text": "From which country is Mbappe?", "marks": 1 },
        { "label": "(i)", "text": "Who is described as the best dribbler in the world?", "marks": 1 },
        { "label": "(j)", "text": "Suggest a suitable title for this poem.", "marks": 1 }
      ]
    }
  ]
}
"""
        elif q_num == 53:
            return """
### UGANDA P.7 ENGLISH SECTION B: Q53 (MEDICAL RECORDS TABLE / GRAPHIC)
Generate Question 53:
- "text": "Study the extract from Mukumer Health Centre III records below carefully and then answer in full sentences the questions that follow."
- "context_block": An HTML medical records table containing columns: No., Name, Sex, Age, Sickness, Treatment Given for 8-10 patients.
- "type": "structured", "marks": 10
- "sub_questions": Exactly 10 sub-questions (a) to (j), worth 1 mark each.

Return JSON:
{
  "questions": [
    {
      "number": 53,
      "text": "Study the extract from Mukumer Health Centre III records below carefully and then answer in full sentences the questions that follow.",
      "context_block": "<table border='1' style='border-collapse:collapse; width:100%; text-align:center; font-size:13px; border:1px solid #000;'>\n<tr style='background:#f1f5f9;'><th>No.</th><th>Name</th><th>Sex</th><th>Age</th><th>Sickness</th><th>Treatment Given</th></tr>\n<tr><td>1</td><td>Magunda Peter</td><td>M</td><td>50</td><td>Malaria</td><td>Given tablets</td></tr>\n<tr><td>2</td><td>Obisa Vincent</td><td>M</td><td>15</td><td>Cholera</td><td>Admitted for one week</td></tr>\n<tr><td>3</td><td>Achieng Matilda</td><td>F</td><td>85</td><td>Cough</td><td>Given tablets</td></tr>\n<tr><td>4</td><td>Drako Silver</td><td>M</td><td>2</td><td>Diarrhoea</td><td>Given oral rehydration</td></tr>\n<tr><td>5</td><td>Musoke Usaini</td><td>M</td><td>6</td><td>Malaria</td><td>Injections for 2 days</td></tr>\n<tr><td>6</td><td>Akware Margaret</td><td>F</td><td>30</td><td>Malaria</td><td>Injections for 2 days</td></tr>\n<tr><td>7</td><td>Tusiime Alawi</td><td>M</td><td>4</td><td>Measles</td><td>Injections for 2 days</td></tr>\n<tr><td>8</td><td>Nyayuk Mary</td><td>F</td><td>36</td><td>Diarrhoea</td><td>Given oral rehydration</td></tr>\n</table>",
      "type": "structured",
      "marks": 10,
      "sub_questions": [
        { "label": "(a)", "text": "From which health centre was the extract taken?", "marks": 1 },
        { "label": "(b)", "text": "How many patients are shown on the record extract?", "marks": 1 },
        { "label": "(c)", "text": "Which patient was admitted for one week?", "marks": 1 },
        { "label": "(d)", "text": "What sickness was Drako Silver suffering from?", "marks": 1 },
        { "label": "(e)", "text": "Who is the oldest patient listed on the record?", "marks": 1 },
        { "label": "(f)", "text": "How many patients were suffering from malaria?", "marks": 1 },
        { "label": "(g)", "text": "What treatment was given to Nyayuk Mary?", "marks": 1 },
        { "label": "(h)", "text": "How many female patients are listed on the record?", "marks": 1 },
        { "label": "(i)", "text": "Which sickness affected the youngest child?", "marks": 1 },
        { "label": "(j)", "text": "Why do you think Drako Silver was given oral rehydration?", "marks": 1 }
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
### UGANDA P.7 ENGLISH SECTION B: Q55 (GUIDED COMPOSITION / LETTER WRITING SCENARIO)
Generate Question 55:
- "text": "You are a pupil at Meri Primary School, P.O. Box 222, Nguli. Your class is hosting a cultural day event. Write a letter to your uncle inviting him to attend the event. Use the outline points below to guide your letter."
- "context_block": A complete scenario box with Outline Points: - Introduce yourself and your class. - State the date, time, and venue of the cultural day. - Describe activities planned (traditional dances, music, drama). - Explain why your uncle's presence will be special. - Conclude with a warm closing.
- "type": "structured", "marks": 10

Return JSON:
{
  "questions": [
    {
      "number": 55,
      "text": "You are a pupil at Meri Primary School, P.O. Box 222, Nguli. Your class is hosting a cultural day event. Write a letter to your uncle inviting him to attend the event.",
      "context_block": "Scenario: Your class is hosting a cultural day event at school.\n\nOutline Points to guide your letter:\n- Introduce yourself and your position in Primary 7.\n- State the date, time, and venue of the cultural day.\n- Highlight the main activities planned (dances, songs, exhibition).\n- Request your uncle to attend as a guest.\n- Express your gratitude and warm regards.",
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
                q["instruction_group"] = P7EnglishEngine.get_subgroup_instruction(qnum)
                if 25 <= qnum <= 26 and "/" not in q.get("text", ""):
                    words = [w.strip() for w in q.get("text", "").replace(".", "").split() if w.strip()]
                    q["text"] = " / ".join(words)
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
                
                # Special Formatting for Q52 (Poem)
                if q_num == 52:
                    fallback_poem = """A DREAM OF BEING A SPORTS CELEBRITY\n\nI must be a football champion,\nJust like Christiano Ronaldo the captain,\nWhose first goal helped Portugal,\nTo qualify for the 2004 World Cup.\n\nGrowing as an orphan is never a limit,\nI will make it just like Lionel Messi did,\nThe top scorer in the premier league ever,\nWho is paid highly and famous everywhere.\n\nI must be a real champion,\nDreaming to be the captain of Uganda Cranes,\nJust like Mbappe and his country France,\nThe best football dribbler in the world."""
                    raw_ctx = q.get("context_block", "").replace("\\n", "\n")
                    if not raw_ctx or "Stanza 1..." in raw_ctx or "Sample stimulus" in raw_ctx or len(raw_ctx.strip()) < 50:
                        q["context_block"] = fallback_poem
                    else:
                        q["context_block"] = raw_ctx

                # Special Formatting for Q53 (Medical Records Table)
                elif q_num == 53:
                    if not q.get("context_block") or "table" not in q.get("context_block", "").lower():
                        q["context_block"] = """<table border='1' style='border-collapse:collapse; width:100%; text-align:center; font-size:13px; border:1px solid #000;'>
<tr style='background:#f1f5f9;'><th>No.</th><th>Name</th><th>Sex</th><th>Age</th><th>Sickness</th><th>Treatment Given</th></tr>
<tr><td>1</td><td>Magunda Peter</td><td>M</td><td>50</td><td>Malaria</td><td>Given tablets</td></tr>
<tr><td>2</td><td>Obisa Vincent</td><td>M</td><td>15</td><td>Cholera</td><td>Admitted for one week</td></tr>
<tr><td>3</td><td>Achieng Matilda</td><td>F</td><td>85</td><td>Cough</td><td>Given tablets</td></tr>
<tr><td>4</td><td>Drako Silver</td><td>M</td><td>2</td><td>Diarrhoea</td><td>Given oral rehydration</td></tr>
<tr><td>5</td><td>Musoke Usaini</td><td>M</td><td>6</td><td>Malaria</td><td>Injections for 2 days</td></tr>
<tr><td>6</td><td>Akware Margaret</td><td>F</td><td>30</td><td>Malaria</td><td>Injections for 2 days</td></tr>
<tr><td>7</td><td>Tusiime Alawi</td><td>M</td><td>4</td><td>Measles</td><td>Injections for 2 days</td></tr>
<tr><td>8</td><td>Nyayuk Mary</td><td>F</td><td>36</td><td>Diarrhoea</td><td>Given oral rehydration</td></tr>
</table>"""

                # Special Formatting for Q54 (Jumbled Sentences)
                elif q_num == 54:
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
                    raw_sents = [l.strip() for l in ctx_text.split("\n") if l.strip() and not "Solution Table" in l and not "<table>" in l]
                    norm_lines = []
                    for idx, line in enumerate(raw_sents[:10]):
                        clean_sent = re.sub(r'^\([a-jA-J]\)\s*', '', line)
                        clean_sent = re.sub(r'^[a-jA-J][\.\)]\s*', '', clean_sent)
                        label = f"({chr(97+idx)})"
                        norm_lines.append(f"{label} {clean_sent}")
                    ctx_normalized = "\n".join(norm_lines)
                    q["context_block"] = ctx_normalized + "\n" + solution_table_html
                    q["sub_questions"] = []

                # Special Formatting for Q55 (Guided Composition / Letter Writing)
                elif q_num == 55:
                    q["sub_questions"] = [] # Relies on general essay writing lines below

                elif q.get("context_block"):
                    q["context_block"] = q["context_block"].replace("\\n", "\n")

                return q
            raise ValueError(f"No item generated for Q{q_num}")
        except Exception as e:
            print(f"P7 English Sec B Item Error (Q{q_num}): {e}")
            if q_num == 51:
                fallback_story = """Once upon a time in Kasese district, Mr. Mukasa owned a large banana farm. The farm was known for producing the sweetest bananas in the region. People from nearby villages often visited to buy fresh bananas directly from Mr. Mukasa. One day, a strong storm hit Kasese, causing significant damage to the farm. Many banana trees were uprooted, and Mr. Mukasa was deeply worried about his livelihood. Fortunately, the villagers came together to help him. They worked tirelessly for days to clear the debris and replant new banana trees. Their hard work and unity paid off, as the farm soon began to thrive once again. Mr. Mukasa was grateful and decided to organize a feast to thank the villagers for their support. From that day on, the farm not only became a source of income but also a symbol of community strength and resilience."""
                return {
                    "number": 51,
                    "text": "Read the passage below carefully and then answer in full sentences the questions that follow.",
                    "context_block": fallback_story,
                    "type": "structured",
                    "marks": 10,
                    "sub_questions": [
                        { "label": "(a)", "text": "Where did Mr. Mukasa own a banana farm?", "marks": 1 },
                        { "label": "(b)", "text": "Why did the villagers visit the farm?", "marks": 1 },
                        { "label": "(c)", "text": "What natural event caused damage to the farm?", "marks": 1 },
                        { "label": "(d)", "text": "How did the storm affect the farm?", "marks": 1 },
                        { "label": "(e)", "text": "What did the villagers do to help Mr. Mukasa?", "marks": 1 },
                        { "label": "(f)", "text": "What was the result of the villagers' efforts?", "marks": 1 },
                        { "label": "(g)", "text": "How did Mr. Mukasa show his gratitude?", "marks": 1 },
                        { "label": "(h)", "text": "What did the farm become a symbol of?", "marks": 1 },
                        { "label": "(i)", "text": "Why was the farm important to Mr. Mukasa?", "marks": 1 },
                        { "label": "(j)", "text": "Describe the community's reaction to the farm's misfortune.", "marks": 1 }
                    ]
                }
            elif q_num == 52:
                fallback_poem = """A DREAM OF BEING A SPORTS CELEBRITY\n\nI must be a football champion,\nJust like Christiano Ronaldo the captain,\nWhose first goal helped Portugal,\nTo qualify for the 2004 World Cup.\n\nGrowing as an orphan is never a limit,\nI will make it just like Lionel Messi did,\nThe top scorer in the premier league ever,\nWho is paid highly and famous everywhere.\n\nI must be a real champion,\nDreaming to be the captain of Uganda Cranes,\nJust like Mbappe and his country France,\nThe best football dribbler in the world."""
                return {
                    "number": 52,
                    "text": "Read the poem below carefully and then answer in full sentences the questions that follow.",
                    "context_block": fallback_poem,
                    "type": "structured",
                    "marks": 10,
                    "sub_questions": [
                        { "label": "(a)", "text": "What is the poem about?", "marks": 1 },
                        { "label": "(b)", "text": "How many stanzas has the poem?", "marks": 1 },
                        { "label": "(c)", "text": "Which sport is mentioned in the poem?", "marks": 1 },
                        { "label": "(d)", "text": "Who is the captain of Portugal mentioned in stanza one?", "marks": 1 },
                        { "label": "(e)", "text": "Which player grew up as an orphan according to stanza two?", "marks": 1 },
                        { "label": "(f)", "text": "Why does the poet want to be like Lionel Messi?", "marks": 1 },
                        { "label": "(g)", "text": "Which national team does the poet dream to captain?", "marks": 1 },
                        { "label": "(h)", "text": "From which country is Mbappe?", "marks": 1 },
                        { "label": "(i)", "text": "Who is described as the best dribbler in the world?", "marks": 1 },
                        { "label": "(j)", "text": "Suggest a suitable title for the poem.", "marks": 1 }
                    ]
                }
            elif q_num == 53:
                return {
                    "number": 53,
                    "text": "Study the extract from Mukumer Health Centre III records below carefully and then answer in full sentences the questions that follow.",
                    "context_block": """<table border='1' style='border-collapse:collapse; width:100%; text-align:center; font-size:13px; border:1px solid #000;'>
<tr style='background:#f1f5f9;'><th>No.</th><th>Name</th><th>Sex</th><th>Age</th><th>Sickness</th><th>Treatment Given</th></tr>
<tr><td>1</td><td>Magunda Peter</td><td>M</td><td>50</td><td>Malaria</td><td>Given tablets</td></tr>
<tr><td>2</td><td>Obisa Vincent</td><td>M</td><td>15</td><td>Cholera</td><td>Admitted for one week</td></tr>
<tr><td>3</td><td>Achieng Matilda</td><td>F</td><td>85</td><td>Cough</td><td>Given tablets</td></tr>
<tr><td>4</td><td>Drako Silver</td><td>M</td><td>2</td><td>Diarrhoea</td><td>Given oral rehydration</td></tr>
<tr><td>5</td><td>Musoke Usaini</td><td>M</td><td>6</td><td>Malaria</td><td>Injections for 2 days</td></tr>
<tr><td>6</td><td>Akware Margaret</td><td>F</td><td>30</td><td>Malaria</td><td>Injections for 2 days</td></tr>
<tr><td>7</td><td>Tusiime Alawi</td><td>M</td><td>4</td><td>Measles</td><td>Injections for 2 days</td></tr>
<tr><td>8</td><td>Nyayuk Mary</td><td>F</td><td>36</td><td>Diarrhoea</td><td>Given oral rehydration</td></tr>
</table>""",
                    "type": "structured",
                    "marks": 10,
                    "sub_questions": [
                        { "label": "(a)", "text": "From which health centre was the extract taken?", "marks": 1 },
                        { "label": "(b)", "text": "How many patients are shown on the record extract?", "marks": 1 },
                        { "label": "(c)", "text": "Which patient was admitted for one week?", "marks": 1 },
                        { "label": "(d)", "text": "What sickness was Drako Silver suffering from?", "marks": 1 },
                        { "label": "(e)", "text": "Who is the oldest patient listed on the record?", "marks": 1 },
                        { "label": "(f)", "text": "How many patients were suffering from malaria?", "marks": 1 },
                        { "label": "(g)", "text": "What treatment was given to Nyayuk Mary?", "marks": 1 },
                        { "label": "(h)", "text": "How many female patients are listed on the record?", "marks": 1 },
                        { "label": "(i)", "text": "Which sickness affected the youngest child?", "marks": 1 },
                        { "label": "(j)", "text": "Why do you think Drako Silver was given oral rehydration?", "marks": 1 }
                    ]
                }
            elif q_num == 54:
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
                    "sub_questions": []
                }
            elif q_num == 55:
                return {
                    "number": 55,
                    "text": "You are a pupil at Meri Primary School, P.O. Box 222, Nguli. Your class is hosting a cultural day event. Write a letter to your uncle inviting him to attend the event.",
                    "context_block": "Scenario: Your class is hosting a cultural day event at school.\n\nOutline Points to guide your letter:\n- Introduce yourself and your position in Primary 7.\n- State the date, time, and venue of the cultural day.\n- Highlight the main activities planned (dances, songs, exhibition).\n- Request your uncle to attend as a guest.\n- Express your gratitude and warm regards.",
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
            "Section B has 5 questions (50 marks). Section B: Composition, Letter Writing, Comprehension",
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

        # ── STEP 2: SECTION A (Q1 - Q50) PARALLEL CHUNKS ACCORDING TO UNEB SUB-GROUP BOUNDARIES ──
        yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Drafting Section A (50 Grammar & Vocabulary Questions)...'})}\n\n"

        sec_a_batches = [
            (1, 5),    # Q1 - Q5 (Fill blank)
            (6, 10),   # Q6 - Q15 (Word forms)
            (16, 2),   # Q16 - Q17 (Abbreviations)
            (18, 3),   # Q18 - Q20 (One word for underlined phrase)
            (21, 2),   # Q21 - Q22 (Plural of underlined word)
            (23, 2),   # Q23 - Q24 (Homophones)
            (25, 2),   # Q25 - Q26 (Rearrange words - slash separated)
            (27, 2),   # Q27 - Q28 (Alphabetical order)
            (29, 2),   # Q29 - Q30 (Opposite of underlined word)
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
        yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Drafting Section B (Passage, Poem, Medical Records Table, Jumbled Sentences, Guided Composition)...'})}\n\n"

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
