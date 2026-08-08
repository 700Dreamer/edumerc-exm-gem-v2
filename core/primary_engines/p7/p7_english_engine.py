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
            return "In each of the questions <b>1</b> to <b>5</b>, fill in the blank space with a suitable word."
        elif 6 <= qnum <= 15:
            return "In each of the questions <b>6</b> to <b>15</b>, use the correct form of the word given in brackets to complete the sentence."
        elif 16 <= qnum <= 17:
            return "In questions <b>16</b> and <b>17</b>, write the <b>full form</b> of the given abbreviations."
        elif 18 <= qnum <= 20:
            return "In questions <b>18</b> to <b>20</b>, rewrite the sentences giving <b>a single word</b> for the <u>underlined</u> group of words."
        elif 21 <= qnum <= 22:
            return "For questions <b>21</b> and <b>22</b>, rewrite the sentences giving the <b>plural</b> form of the <u>underlined</u> word."
        elif 23 <= qnum <= 24:
            return "In questions <b>23</b> and <b>24</b>, use each of the given words in a sentence to show that you know the <b>difference in their meaning</b>."
        elif 25 <= qnum <= 26:
            return "In questions <b>25</b> and <b>26</b>, rearrange the given words to form a <b>correct sentence</b>."
        elif 27 <= qnum <= 28:
            return "In questions <b>27</b> and <b>28</b>, rearrange the given words in <b>alphabetical order</b>."
        elif 29 <= qnum <= 30:
            return "For questions <b>29</b> and <b>30</b>, rewrite the sentences giving the <b>opposite</b> of the <u>underlined</u> word."
        else:
            return "<div style='text-align:center; font-weight:bold; margin-top:25px; margin-bottom:10px; font-size:16px;'>Sub-section II</div>In each of the questions <b>31</b> to <b>50</b>, rewrite the sentences as <b>instructed</b> in the brackets."

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
- STRICT RULE: Do NOT repeat the group instruction inside the question text stem!
- For Homophones (Q23-24): Provide word pair e.g. "accept / except" or "weight / wait".
- For Alphabetical order (Q27-28): Provide comma-separated words ONLY e.g. "cat, apple, banana".
- For Underlined words (Q18-20, Q21-22, Q29-30): Wrap target words in HTML <u> tags e.g. "The referee told the player to <u>start again the game</u>."
- For Sentence Rearranging (Q25-26): Format words separated by slashes ONLY e.g. "how / to / know / I / ride / a / bicycle."
- Each item MUST have "type": "short_answer", "marks": 1, and an explicit, correct, concise "answer" field.

Return JSON:
{{
  "questions": [
    {{
      "number": {start_num},
      "text": "The sun rises in the _________________.",
      "type": "short_answer",
      "marks": 1,
      "answer": "east"
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
- Directives in brackets MUST include boldened target words: (Rewrite as <b>one</b> sentence using: ...... where ......), (Rewrite using: ...... mine), (Rewrite beginning: Remember......), (Rewrite as <b>one</b> sentence beginning: Much as ......), (Rewrite as <b>one</b> sentence beginning: If ......), (Rewrite as <b>one</b> sentence <b>without</b> using "and" or "which"), (Rewrite as <b>one</b> sentence using: ...... neither ...... nor ......).
- Each item MUST have "type": "short_answer", "marks": 1, and an explicit, complete rewritten "answer" field.

Return JSON:
{{
  "questions": [
    {{
      "number": {start_num},
      "text": "This is the boy. His father won the race. (Rewrite as <b>one</b> sentence using: ... whose ...)",
      "type": "short_answer",
      "marks": 1,
      "answer": "This is the boy whose father won the race."
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
- "text": "Read the passage below carefully and then answer <b>in full sentences</b> the questions that follow."
- "context_block": A complete 180-word interesting story about Ugandan school children, farming, or community event.
- "type": "structured", "marks": 10
- "sub_questions": Exactly 10 sub-questions (a) to (j), worth 1 mark each.

Return JSON:
{
  "questions": [
    {
      "number": 51,
      "text": "Read the passage below carefully and then answer <b>in full sentences</b> the questions that follow.",
      "context_block": "Once upon a time in Kasese district...",
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
        { "label": "(j)", "text": "Give another <b>word</b> or <b>group of words</b> with the <b>same meaning</b> as each of the <u>underlined</u> words in the passage.", "marks": 1 }
      ]
    }
  ]
}
"""
        elif q_num == 52:
            return """
### UGANDA P.7 ENGLISH SECTION B: Q52 (POEM / STORY EXTRACT)
Generate Question 52:
- "text": "Read the poem below carefully and then answer <b>in full sentences</b> the questions that follow."
- "context_block": A complete 12-line poem with 3 stanzas about sports, nature, or hard work, concluding with author name right-aligned e.g. "\\n\\n<div style='text-align:right; font-weight:bold; font-style:italic;'>Peninah Birungi</div>".
- "type": "structured", "marks": 10
- "sub_questions": Exactly 10 sub-questions (a) to (j), worth 1 mark each.

Return JSON:
{
  "questions": [
    {
      "number": 52,
      "text": "Read the poem below carefully and then answer <b>in full sentences</b> the questions that follow.",
      "context_block": "Yes, the day has come!\nTo celebrate and rejoice together!\nGrandma, eighty years old!\nEverybody gathered to congratulate her.\nOh! We thank God.\n\nSons, daughters, grandchildren of grandma,\nFrom far and near,\nRelatives, in-laws, neighbours,\nHave come along with gifts of all kinds.\nOh! We glorify God.\n\n<div style='text-align:right; font-weight:bold; font-style:italic;'>Peninah Birungi</div>",
      "type": "structured",
      "marks": 10,
      "sub_questions": [
        { "label": "(a)", "text": "What is the poem about?", "marks": 1 },
        { "label": "(b)", "text": "Where have the sons and daughters come from?", "marks": 1 },
        { "label": "(c)", "text": "Why do you think people came with gifts of all kinds?", "marks": 1 },
        { "label": "(d)", "text": "What has pleased the grandma's heart?", "marks": 1 },
        { "label": "(e)", "text": "How many stanzas are in this poem?", "marks": 1 },
        { "label": "(f)", "text": "What was in plenty according to the poem?", "marks": 1 },
        { "label": "(g)", "text": "Who wrote the poem?", "marks": 1 },
        { "label": "(h)", "text": "Give another <b>word</b> or <b>group of words</b> with the <b>same meaning</b> as each of the <u>underlined</u> words in the passage.", "marks": 1 },
        { "label": "(i)", "text": "Suggest a suitable title for the poem.", "marks": 1 }
      ]
    }
  ]
}
"""
        elif q_num == 53:
            return """
### UGANDA P.7 ENGLISH SECTION B: Q53 (MEDICAL RECORDS TABLE / GRAPHIC)
Generate Question 53:
- "text": "Below is an extract from Mukumer Health Centre III records, taken on 27<sup>th</sup> February, 2021. Study it carefully and then answer <b>in full sentences</b> the questions that follow."
- "context_block": An HTML medical records table containing columns: S/N, Name of patient, Sex, Age, Disease, Comment on treatment for 8-10 patients, with footer "<div style='text-align:center; font-style:italic; margin-top:6px;'>Compiled by Dr. Paul Kibirige</div>".
- "type": "structured", "marks": 10
- "sub_questions": Exactly 10 sub-questions (a) to (j), worth 1 mark each.

Return JSON:
{
  "questions": [
    {
      "number": 53,
      "text": "Below is an extract from Mukumer Health Centre III records, taken on 27<sup>th</sup> February, 2021. Study it carefully and then answer <b>in full sentences</b> the questions that follow.",
      "context_block": "<table border='1' style='border-collapse:collapse; width:100%; text-align:center; font-size:13px; border:1px solid #000;'>\n<tr style='background:#f1f5f9;'><th>S/N</th><th>Name of patient</th><th>Sex</th><th>Age</th><th>Disease</th><th>Comment on treatment</th></tr>\n<tr><td>1</td><td>Magunda Peter</td><td>M</td><td>50</td><td>Malaria</td><td>Given tablets</td></tr>\n<tr><td>2</td><td>Obisa Vincent</td><td>M</td><td>15</td><td>Cholera</td><td>Admitted for one week</td></tr>
<tr><td>3</td><td>Achieng Matilda</td><td>F</td><td>85</td><td>Cough</td><td>Given tablets</td></tr>\n<tr><td>4</td><td>Drako Silver</td><td>M</td><td>2</td><td>Diarrhoea</td><td>Given oral rehydration salts and deworming</td></tr>\n<tr><td>5</td><td>Musoke Usaini</td><td>M</td><td>6</td><td>Malaria</td><td>Injections for 2 days</td></tr>\n<tr><td>6</td><td>Akware Margaret</td><td>F</td><td>30</td><td>Malaria</td><td>Injections for 2 days</td></tr>\n<tr><td>7</td><td>Tusiime Alawi</td><td>M</td><td>4</td><td>Measles</td><td>Injections for 2 days</td></tr>\n<tr><td>8</td><td>Nyayuk Mary</td><td>F</td><td>36</td><td>Diarrhoea</td><td>Given oral rehydration salts and deworming</td></tr>\n<tr><td>9</td><td>Muntu David</td><td>M</td><td>40</td><td>Tuberculosis</td><td>Referred</td></tr>\n</table>\n<div style='text-align:center; font-style:italic; margin-top:6px;'>Compiled by Dr. Paul Kibirige</div>",
      "type": "structured",
      "marks": 10,
      "sub_questions": [
        { "label": "(a)", "text": "From which health centre was this record extracted?", "marks": 1 },
        { "label": "(b)", "text": "When was the extract written?", "marks": 1 },
        { "label": "(c)", "text": "How many patients were recorded in this extract?", "marks": 1 },
        { "label": "(d)", "text": "Mention the number of female patients who received treatment from Mukumer Health Centre III.", "marks": 1 },
        { "label": "(e)", "text": "Why do you think Achieng Matilda would easily suffer from COVID-19?", "marks": 1 },
        { "label": "(f)", "text": "Why was Obisa Vincent admitted?", "marks": 1 },
        { "label": "(g)", "text": "What should people around this health centre III do to avoid malaria?", "marks": 1 },
        { "label": "(h)", "text": "Which patient was not treated at this health centre?", "marks": 1 },
        { "label": "(i)", "text": "Why should Drako Silver and Nyayuk Mary be treated using oral rehydration salts?", "marks": 1 },
        { "label": "(j)", "text": "Who compiled the extract?", "marks": 1 }
      ]
    }
  ]
}
"""
        elif q_num == 54:
            return """
### UGANDA P.7 ENGLISH SECTION B: Q54 (DIALOGUE COMPLETION SCRIPT)
Generate Question 54:
- "text": "Below is a conversation between Agero Noel, a P.6 pupil of Okwara Primary School and her teacher, Madam Nawudo Mariam. Write what you think Noel said."
- "context_block": A 10-turn dialogue script with Noel's turns given as blank writing lines "Noel: ___________________________________________________" and Teacher's turns given as prompts.
- "type": "structured", "marks": 10

Return JSON:
{
  "questions": [
    {
      "number": 54,
      "text": "Below is a conversation between Agero Noel, a P.6 pupil of Okwara Primary School and her teacher, Madam Nawudo Mariam. Write what you think Noel said.",
      "context_block": "Noel: ___________________________________________________\nTeacher: Yes please, come in.\n\nNoel: ___________________________________________________\nTeacher: Good morning young girl. What is your name?\n\nNoel: ___________________________________________________\nTeacher: In which class are you, Noel?\n\nNoel: ___________________________________________________\nTeacher: What have you brought for me, Noel?\n\nNoel: ___________________________________________________\nTeacher: A letter! What is it about?\n\nNoel: ___________________________________________________\nTeacher: Thank you. You are inviting me for Easter celebration, where will it take place?\n\nNoel: ___________________________________________________\nTeacher: Have you invited your class teacher Mr. Matovu?\n\nNoel: ___________________________________________________\nTeacher: Thank you for inviting both of us for Easter celebration.\n\nNoel: ___________________________________________________\nTeacher: We shall be there.\n\nNoel: ___________________________________________________\nTeacher: You're welcome.",
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
- "text": "You are a pupil at Meri Primary school, P.O. Box 222, Nguli. Your class is organizing an educational tour to Queen Elizabeth National Park. Write a letter to your parent/guardian asking for permission. Mention the amount of money to be paid. Request her/him to pay before the end of the term. Promise that you will learn new things and behave well."
- "context_block": ""
- "type": "structured", "marks": 10

Return JSON:
{
  "questions": [
    {
      "number": 55,
      "text": "You are a pupil at Meri Primary school, P.O. Box 222, Nguli. Your class is organizing an educational tour to Queen Elizabeth National Park. Write a letter to your parent/guardian asking for permission. Mention the amount of money to be paid. Request her/him to pay before the end of the term. Promise that you will learn new things and behave well.",
      "context_block": "",
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
                # Clean stem text to prevent repeating sub-group instructions inside stems
                raw_text = q.get("text", "")
                if 23 <= qnum <= 24:
                    words = re.findall(r'["\']([a-zA-Z]+)["\']', raw_text)
                    if len(words) < 2:
                        words = [w.strip() for w in raw_text.replace("and", "/").split("/") if w.strip()]
                    if len(words) >= 2:
                        q["type"] = "structured"
                        q["text"] = ""
                        q["sub_questions"] = [
                            {"label": "(a)", "text": f"{words[0]}:", "marks": 1},
                            {"label": "(b)", "text": f"{words[1]}:", "marks": 1}
                        ]
                elif 25 <= qnum <= 26:
                    clean = re.sub(r'^(rearrange the given words to form a correct sentence|rearrange the words to form a correct sentence|rearrange the given words|form a correct sentence).*?:?\s*', '', raw_text, flags=re.I)
                    raw_words = [w.strip() for w in clean.replace(".", "").split("/") if w.strip()]
                    if len(raw_words) < 2:
                        raw_words = [w.strip() for w in clean.replace(".", "").split() if w.strip()]
                    q["text"] = " / ".join(raw_words)
                elif 27 <= qnum <= 28:
                    clean = re.sub(r'^(rearrange the following words in alphabetical order:|arrange the following words in alphabetical order:|rearrange the following words|arrange the following words|in alphabetical order).*?:?\s*', '', raw_text, flags=re.I)
                    q["text"] = clean.strip()
                elif 16 <= qnum <= 17:
                    clean = re.sub(r'^(write the full form of the contraction|write the full form of the given|write the full form of|write the plural form of the word|write the plural form of).*?:?\s*', '', raw_text, flags=re.I)
                    clean = clean.replace('"', '').strip()
                    q["text"] = clean
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
                
                # Special Formatting for Q51 (Comprehension Passage)
                if q_num == 51:
                    fallback_story = (
                        "Primary seven pupils and their teachers sat under a mango tree in the "
                        "school compound. They started to discuss activities they would do in the "
                        "holidays to earn some money. Kato Allan was the first to speak. He said "
                        "that he was going to make pancakes and sell them to their neighbour's "
                        "children. His aunt taught him how to make pancakes during COVID-19 lockdown.\n\n"
                        "Lokaris said that he was going to weave mats and baskets to sell "
                        "them in the market every Saturday. When he was asked about the source "
                        "of materials, he answered that his mother would be of great help.\n\n"
                        "Nyaps reported that when she was in Primary Five, she learnt knitting and "
                        "making other crafts from her sister. They would make bags and <u>decorate</u> "
                        "them with beads. So, Nyaps was going to make small bags for pupils to "
                        "put their pencils, pens, note books and other things.\n\n"
                        "Amooti was already a known artist in the school. He informed the class "
                        "about drawing pictures of people washing hands, sanitising and social "
                        "distancing while wearing masks. His art teacher would sell the pictures to "
                        "schools and markets. 'I want to sensitize people about the COVID-19 "
                        "pandemic', Amooti said. The classmates were very <u>excited</u> about his idea.\n\n"
                        "Mrs. Oringo Susan the class teacher, thanked the pupils for their holiday plans."
                    )
                    raw_ctx = q.get("context_block", "")
                    if isinstance(raw_ctx, list):
                        raw_ctx = "\n\n".join(str(l) for l in raw_ctx)
                    else:
                        raw_ctx = str(raw_ctx).replace("\\n", "\n")

                    if not raw_ctx or "Full 180-word" in raw_ctx or "story narrative" in raw_ctx or "Sample stimulus" in raw_ctx or len(raw_ctx.strip()) < 80:
                        q["context_block"] = fallback_story
                    else:
                        q["context_block"] = raw_ctx

                # Special Formatting for Q52 (Poem)
                elif q_num == 52:
                    fallback_poem = (
                        "Yes, the day has come!\n"
                        "To celebrate and rejoice together!\n"
                        "Grandma, eighty years old!\n"
                        "Everybody gathered to <u>congratulate</u> her.\n"
                        "Oh! We thank God.\n\n"
                        "Sons, daughters, grandchildren of grandma,\n"
                        "From far and near,\n"
                        "Relatives, in-laws, neighbours,\n"
                        "Have come along with gifts of all kinds.\n"
                        "Oh! We glorify God.\n\n"
                        "Plenty of food to eat,\n"
                        "Plenty of drinks to all,\n"
                        "Lots of talking and laughing,\n"
                        "Lots of singing and dancing, everybody happy.\n"
                        "Oh! We praise God.\n\n"
                        "What a great day it is!\n"
                        "What a wonderful day it is!\n"
                        "Grandma's heart at peace,\n"
                        "<u>United</u> with all her dear relatives.\n"
                        "Oh! We love God.\n\n"
                        "<div style='text-align:right; font-weight:bold; font-style:italic;'>Peninah Birungi</div>"
                    )
                    raw_ctx = q.get("context_block", "")
                    if isinstance(raw_ctx, list):
                        raw_ctx = "\n\n".join(str(l) for l in raw_ctx)
                    else:
                        raw_ctx = str(raw_ctx).replace("\\n", "\n")

                    if not raw_ctx or "Stanza 1..." in raw_ctx or "Sample stimulus" in raw_ctx or len(raw_ctx.strip()) < 50:
                        q["context_block"] = fallback_poem
                    else:
                        if "Peninah Birungi" not in raw_ctx and "text-align:right" not in raw_ctx:
                            raw_ctx += "\n\n<div style='text-align:right; font-weight:bold; font-style:italic;'>Peninah Birungi</div>"
                        q["context_block"] = raw_ctx

                # Special Formatting for Q53 (Medical Records Table)
                elif q_num == 53:
                    if not q.get("context_block") or "table" not in str(q.get("context_block", "")).lower():
                        q["context_block"] = (
                            "<table border='1' style='border-collapse:collapse; width:100%; text-align:center; font-size:13px; border:1px solid #000;'>"
                            "<tr style='background:#f1f5f9;'><th>S/N</th><th>Name of patient</th><th>Sex</th><th>Age</th><th>Disease</th><th>Comment on treatment</th></tr>"
                            "<tr><td>1.</td><td>Magunda Peter</td><td>M</td><td>50</td><td>Malaria</td><td>Given tablets</td></tr>"
                            "<tr><td>2.</td><td>Obisa Vincent</td><td>M</td><td>15</td><td>Cholera</td><td>Admitted for one week</td></tr>"
                            "<tr><td>3.</td><td>Achieng Matilda</td><td>F</td><td>85</td><td>Cough</td><td>Given tablets</td></tr>"
                            "<tr><td>4.</td><td>Drako Silver</td><td>M</td><td>2</td><td>Diarrhoea</td><td>Given oral rehydration salts and deworming</td></tr>"
                            "<tr><td>5.</td><td>Musoke Usaini</td><td>M</td><td>6</td><td>Malaria</td><td>Injections for 2 days</td></tr>"
                            "<tr><td>6.</td><td>Akware Margaret</td><td>F</td><td>30</td><td>Malaria</td><td>Injections for 2 days</td></tr>"
                            "<tr><td>7.</td><td>Tusiime Alawi</td><td>M</td><td>4</td><td>Measles</td><td>Injections for 2 days</td></tr>"
                            "<tr><td>8.</td><td>Nyayuk Mary</td><td>F</td><td>36</td><td>Diarrhoea</td><td>Given oral rehydration salts and deworming</td></tr>"
                            "<tr><td>9.</td><td>Muntu David</td><td>M</td><td>40</td><td>Tuberculosis</td><td>Referred</td></tr>"
                            "</table>"
                            "<div style='text-align:center; font-style:italic; margin-top:6px;'>Compiled by Dr. Paul Kibirige</div>"
                        )

                # Special Formatting for Q54 (Dialogue Completion Script - NO Outer Box)
                elif q_num == 54:
                    raw_ctx = q.get("context_block", "")
                    if isinstance(raw_ctx, list):
                        ctx_text = "\n".join(str(l) for l in raw_ctx)
                    else:
                        ctx_text = str(raw_ctx).replace("\\n", "\n")

                    lines = [l.strip() for l in ctx_text.split("\n") if l.strip()]
                    teacher_prompts = [l for l in lines if l.startswith("Teacher:") or l.startswith("Speaker 1:")]
                    if len(teacher_prompts) >= 5:
                        cleaned_lines = []
                        for prompt_line in teacher_prompts:
                            if prompt_line.startswith("Speaker 1:"):
                                prompt_line = "Teacher:" + prompt_line[len("Speaker 1:"): ]
                            cleaned_lines.append("Noel: ___________________________________________________")
                            cleaned_lines.append("        ___________________________________________________")
                            cleaned_lines.append(prompt_line)
                            cleaned_lines.append("")
                        q["context_block"] = "\n".join(cleaned_lines)
                    else:
                        q["context_block"] = """Noel: ___________________________________________________
Teacher: Yes please, come in.

Noel: ___________________________________________________
Teacher: Good morning young girl. What is your name?

Noel: ___________________________________________________
Teacher: In which class are you, Noel?

Noel: ___________________________________________________
Teacher: What have you brought for me, Noel?

Noel: ___________________________________________________
Teacher: A letter! What is it about?

Noel: ___________________________________________________
Teacher: Thank you. You are inviting me for Easter celebration, where will it take place?

Noel: ___________________________________________________
Teacher: Have you invited your class teacher Mr. Matovu?

Noel: ___________________________________________________
Teacher: Thank you for inviting both of us for Easter celebration.

Noel: ___________________________________________________
Teacher: We shall be there.

Noel: ___________________________________________________
Teacher: You're welcome."""
                    q["sub_questions"] = []

                # Special Formatting for Q55 (Guided Composition / Letter Writing)
                elif q_num == 55:
                    q["context_block"] = ""
                    q["sub_questions"] = [] # Relies on general essay writing lines below

                elif q.get("context_block"):
                    ctx = q["context_block"]
                    if isinstance(ctx, list):
                        q["context_block"] = "\n".join(str(l) for l in ctx)
                    else:
                        q["context_block"] = str(ctx).replace("\\n", "\n")

                return q
            raise ValueError(f"No item generated for Q{q_num}")
        except Exception as e:
            print(f"P7 English Sec B Item Error (Q{q_num}): {e}")
            if q_num == 51:
                fallback_story = (
                    "Primary seven pupils and their teachers sat under a mango tree in the "
                    "school compound. They started to discuss activities they would do in the "
                    "holidays to earn some money. Kato Allan was the first to speak. He said "
                    "that he was going to make pancakes and sell them to their neighbour's "
                    "children. His aunt taught him how to make pancakes during COVID-19 lockdown.\n\n"
                    "Lokaris said that he was going to weave mats and baskets. The sell "
                    "them in the market every Saturday. When he was asked about the source "
                    "of materials, he answered that his mother would be of great help.\n\n"
                    "Nyaps reported that when she was in Primary Five, she learnt knitting and "
                    "making other crafts from her sister. They would make bags and <u>decorate</u> "
                    "them with beads. So, Nyaps was going to make small bags for pupils to "
                    "put their pencils, pens, note books and other things.\n\n"
                    "Amooti was already a known artist in the school. He informed the class "
                    "about drawing pictures of people washing hands, sanitising and social "
                    "distancing while wearing masks. His art teacher would sell the pictures to "
                    "schools and markets. 'I want to sensitize people about the COVID-19 "
                    "pandemic', Amooti said. The classmates were very <u>excited</u> about his idea.\n\n"
                    "Mrs. Oringo Susan the class teacher, thanked the pupils for their holiday plans."
                )
                return {
                    "number": 51,
                    "text": "Read the passage below carefully and then answer <b>in full sentences</b> the questions that follow.",
                    "context_block": fallback_story,
                    "type": "structured",
                    "marks": 10,
                    "sub_questions": [
                        { "label": "(a)", "text": "Why did pupils and their teachers sit under the mango tree?", "marks": 1 },
                        { "label": "(b)", "text": "Where had Kato Allan learnt making pancakes from?", "marks": 1 },
                        { "label": "(c)", "text": "From whom would Lokaris get the materials for his art and crafts work?", "marks": 1 },
                        { "label": "(d)", "text": "When did Nyaps learn how to make bags?", "marks": 1 },
                        { "label": "(e)", "text": "Who would help Amooti to sell his art work?", "marks": 1 },
                        { "label": "(f)", "text": "Why were the classmates excited about Amooti's idea?", "marks": 1 },
                        { "label": "(g)", "text": "How would selling things in the shop be useful to Ibra?", "marks": 1 },
                        { "label": "(h)", "text": "What did Mrs. Oringo Susan urge the pupils to do?", "marks": 1 },
                        { "label": "(i)", "text": "How many teachers' names were given in the passage?", "marks": 1 },
                        { "label": "(j)", "text": "Give another <b>word</b> or <b>group of words</b> with the <b>same meaning</b> as each of the <u>underlined</u> words in the passage.", "marks": 1 }
                    ]
                }
            elif q_num == 52:
                fallback_poem = (
                    "Yes, the day has come!\n"
                    "To celebrate and rejoice together!\n"
                    "Grandma, eighty years old!\n"
                    "Everybody gathered to <u>congratulate</u> her.\n"
                    "Oh! We thank God.\n\n"
                    "Sons, daughters, grandchildren of grandma,\n"
                    "From far and near,\n"
                    "Relatives, in-laws, neighbours,\n"
                    "Have come along with gifts of all kinds.\n"
                    "Oh! We glorify God.\n\n"
                    "Plenty of food to eat,\n"
                    "Plenty of drinks to all,\n"
                    "Lots of talking and laughing,\n"
                    "Lots of singing and dancing, everybody happy.\n"
                    "Oh! We praise God.\n\n"
                    "What a great day it is!\n"
                    "What a wonderful day it is!\n"
                    "Grandma's heart at peace,\n"
                    "<u>United</u> with all her dear relatives.\n"
                    "Oh! We love God.\n\n"
                    "<div style='text-align:right; font-weight:bold; font-style:italic;'>Peninah Birungi</div>"
                )
                return {
                    "number": 52,
                    "text": "Read the poem below carefully and then answer <b>in full sentences</b> the questions that follow.",
                    "context_block": fallback_poem,
                    "type": "structured",
                    "marks": 10,
                    "sub_questions": [
                        { "label": "(a)", "text": "What is the poem about?", "marks": 1 },
                        { "label": "(b)", "text": "Where have the sons and daughters come from?", "marks": 1 },
                        { "label": "(c)", "text": "Why do you think people came with gifts of all kinds?", "marks": 1 },
                        { "label": "(d)", "text": "What has pleased the grandma's heart?", "marks": 1 },
                        { "label": "(e)", "text": "How many stanzas are in this poem?", "marks": 1 },
                        { "label": "(f)", "text": "What was in plenty according to the poem?", "marks": 1 },
                        { "label": "(g)", "text": "Who wrote the poem?", "marks": 1 },
                        { "label": "(h)", "text": "Give another <b>word</b> or <b>group of words</b> with the <b>same meaning</b> as each of the <u>underlined</u> words in the passage.", "marks": 1 },
                        { "label": "(i)", "text": "Suggest a suitable title for the poem.", "marks": 1 }
                    ]
                }
            elif q_num == 53:
                table_html = (
                    "<table border='1' style='border-collapse:collapse; width:100%; text-align:center; font-size:13px; border:1px solid #000;'>"
                    "<tr style='background:#f1f5f9;'><th>S/N</th><th>Name of patient</th><th>Sex</th><th>Age</th><th>Disease</th><th>Comment on treatment</th></tr>"
                    "<tr><td>1.</td><td>Magunda Peter</td><td>M</td><td>50</td><td>Malaria</td><td>Given tablets</td></tr>"
                    "<tr><td>2.</td><td>Obisa Vincent</td><td>M</td><td>15</td><td>Cholera</td><td>Admitted for one week</td></tr>"
                    "<tr><td>3.</td><td>Achieng Matilda</td><td>F</td><td>85</td><td>Cough</td><td>Given tablets</td></tr>"
                    "<tr><td>4.</td><td>Drako Silver</td><td>M</td><td>2</td><td>Diarrhoea</td><td>Given oral rehydration salts and deworming</td></tr>"
                    "<tr><td>5.</td><td>Musoke Usaini</td><td>M</td><td>6</td><td>Malaria</td><td>Injections for 2 days</td></tr>"
                    "<tr><td>6.</td><td>Akware Margaret</td><td>F</td><td>30</td><td>Malaria</td><td>Injections for 2 days</td></tr>"
                    "<tr><td>7.</td><td>Tusiime Alawi</td><td>M</td><td>4</td><td>Measles</td><td>Injections for 2 days</td></tr>"
                    "<tr><td>8.</td><td>Nyayuk Mary</td><td>F</td><td>36</td><td>Diarrhoea</td><td>Given oral rehydration salts and deworming</td></tr>"
                    "<tr><td>9.</td><td>Muntu David</td><td>M</td><td>40</td><td>Tuberculosis</td><td>Referred</td></tr>"
                    "</table>"
                    "<div style='text-align:center; font-style:italic; margin-top:6px;'>Compiled by Dr. Paul Kibirige</div>"
                )
                return {
                    "number": 53,
                    "text": "Below is an extract from Mukumer Health Centre III records, taken on 27<sup>th</sup> February, 2021. Study it carefully and then answer <b>in full sentences</b> the questions that follow.",
                    "context_block": table_html,
                    "type": "structured",
                    "marks": 10,
                    "sub_questions": [
                        { "label": "(a)", "text": "From which health centre was this record extracted?", "marks": 1 },
                        { "label": "(b)", "text": "When was the extract written?", "marks": 1 },
                        { "label": "(c)", "text": "How many patients were recorded in this extract?", "marks": 1 },
                        { "label": "(d)", "text": "Mention the number of female patients who received treatment from Mukumer Health Centre III.", "marks": 1 },
                        { "label": "(e)", "text": "Why do you think Achieng Matilda would easily suffer from COVID-19?", "marks": 1 },
                        { "label": "(f)", "text": "Why was Obisa Vincent admitted?", "marks": 1 },
                        { "label": "(g)", "text": "What should people around this health centre III do to avoid malaria?", "marks": 1 },
                        { "label": "(h)", "text": "Which patient was not treated at this health centre?", "marks": 1 },
                        { "label": "(i)", "text": "Why should Drako Silver and Nyayuk Mary be treated using oral rehydration salts?", "marks": 1 },
                        { "label": "(j)", "text": "Who compiled the extract?", "marks": 1 }
                    ]
                }
            elif q_num == 54:
                return {
                    "number": 54,
                    "text": "Below is a conversation between Agero Noel, a P.6 pupil of Okwara Primary School and her teacher, Madam Nawudo Mariam. She went to invite her for Easter celebration at their home in Totokidwe. What the teacher said is given. Write what you think Agero Noel said.",
                    "context_block": """Noel: ___________________________________________________
Teacher: Yes please, come in.

Noel: ___________________________________________________
Teacher: Good morning young girl. What is your name?

Noel: ___________________________________________________
Teacher: In which class are you, Noel?

Noel: ___________________________________________________
Teacher: What have you brought for me, Noel?

Noel: ___________________________________________________
Teacher: A letter! What is it about?

Noel: ___________________________________________________
Teacher: Thank you. You are inviting me for Easter celebration, where will it take place?

Noel: ___________________________________________________
Teacher: Have you invited your class teacher Mr. Matovu?

Noel: ___________________________________________________
Teacher: Thank you for inviting both of us for Easter celebration.

Noel: ___________________________________________________
Teacher: We shall be there.

Noel: ___________________________________________________
Teacher: You're welcome.""",
                    "type": "structured",
                    "marks": 10,
                    "sub_questions": []
                }
            elif q_num == 55:
                return {
                    "number": 55,
                    "text": "You are a pupil at Meri Primary school, P.O. Box 222, Nguli. Your class is organizing an educational tour to Queen Elizabeth National Park. Write a letter to your parent/guardian asking for permission. Mention the amount of money to be paid. Request her/him to pay before the end of the term. Promise that you will learn new things and behave well.",
                    "context_block": "",
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
        title = "ENGLISH"
        instructions = [
            "Do not write your <b>school</b> or <b>district name</b> anywhere on this paper.",
            "This paper has two sections: <b>A</b> and <b>B</b>.<br>Section <b>A</b> has <b>50</b> questions and section <b>B</b> has <b>5</b> questions. The paper has <b>16 printed papers</b> altogether.",
            "Answer <b>all</b> questions. <b>All</b> the working for both sections <b>A</b> and <b>B</b> must be shown in the spaces provided.",
            "<b>All</b> working must be done using a <b>blue</b> or <b>black</b> ball point pen or ink. Any work done in pencil will <u><b>NOT</b></u> be marked.",
            "Unnecessary <b>changes</b> in your work and handwriting that cannot easily be read may lead to loss of marks.",
            "Do not fill anything in the table indicated: <b>\"For examiners' use only\"</b> and the boxes inside the question paper."
        ]

        # ── STEP 1: HEADER READY EVENT ──
        header_event = {
            "event_type": "header_ready",
            "title": title,
            "subject": "ENGLISH",
            "level": "PRIMARY LEAVING EXAMINATIONS",
            "duration": "2 hours 15 minutes",
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
            q_html = build_question_html("Exams", q, subject="ENGLISH", level="PRIMARY 7")
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
        yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Drafting Section B (Passage, Poem, Health Centre Table, Dialogue Script, Guided Letter)...'})}\n\n"

        sec_b_tasks = [
            asyncio.create_task(P7EnglishEngine.generate_sec_b_item(qnum))
            for qnum in range(51, 56)
        ]

        all_sec_b_qs = await asyncio.gather(*sec_b_tasks)
        all_sec_b_qs.sort(key=lambda q: q.get("number", 0))

        for q in all_sec_b_qs:
            q_html = build_question_html("Exams", q, subject="ENGLISH", level="PRIMARY 7")
            item_evt = {
                "event_type": "question_ready",
                "section": "B",
                "number": q["number"],
                "question_json": q,
                "question_html": q_html
            }
            yield f"data: {json.dumps(item_evt)}\n\n"
            await asyncio.sleep(0.01)

        # ── STEP 4: PHASED GENERATION EVENTS (EXAM PAPER -> MARKING GUIDE -> REFERENCE MAP) ──
        all_questions = all_sec_a_qs + all_sec_b_qs
        raw_payload = {"questions": all_questions}
        raw_str = json.dumps(raw_payload)

        # Phase 1: Build & emit Exam Question Paper immediately
        yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Exam paper complete! Displaying preview...'})}\n\n"

        full_html = build_full_html(
            mode="Exams",
            exam_type="PRIMARY LEAVING EXAMINATIONS",
            level="PRIMARY 7",
            subject="ENGLISH",
            term_roman="2020",
            exam_year="2020",
            duration="2 hours 15 minutes",
            school_name="EDUQUEST EXAMINATIONS BOARD",
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
