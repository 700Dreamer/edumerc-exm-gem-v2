# Dedicated Primary 7 Social Studies with Religious Education Examination Engine (P.7 SST)
# Official UNEB PLE Standard Specifications derived from sample papers in sample papers/p.7/

import json
import re
import asyncio
from typing import List, Dict, AsyncGenerator
from core.ai_engine import get_async_openai_client
from ui.document_builder import build_question_html, build_full_html

class P7SSTEngine:
    """
    Dedicated generation engine for Primary 7 Social Studies with Religious Education (PLE Specification).
    Matches 100% of UNEB specimen papers in sample papers/p.7/
    - Section A: Q1 - Q40 (40 Marks, 1 mark each)
    - Section B: Q41 - Q55 (60 Marks, 4 marks each across 15 distinct topics including Christian/Islamic alternatives)
    """

    @staticmethod
    def synthesize_sec_a_prompt(start_num: int, count: int) -> str:
        end_num = start_num + count - 1
        return f"""
### UGANDA P.7 SOCIAL STUDIES & RELIGIOUS EDUCATION GENERATOR (SECTION A)
QUESTIONS: Q{start_num} to Q{end_num} (Count: {count})
INSTRUCTION: "In each of the questions {start_num} to {end_num}, answer the question in brief."

Generate exactly {count} short-answer primary SST questions for Primary 7 starting at Q{start_num}.
- Directly test core Ugandan P.7 SST syllabus strands: Location & Geography of East Africa & Africa, Climate & Vegetation, Economic Development & Trade, History & Pan-African Movement, Government & Civics, Peace & Security.
- Each item MUST have "type": "short_answer", "marks": 1.
- Provide dotted line fill space at the end of each stem: "..........................................".

Return JSON:
{{
  "questions": [
    {{
      "number": {start_num},
      "text": "Give one way a school motto is important. ..........................................",
      "type": "short_answer",
      "marks": 1
    }}
  ]
}}
"""

    @staticmethod
    def synthesize_sec_b_prompt(q_num: int) -> str:
        topics = {
            41: ("The sketch map of Africa below shows regional economic groupings.", "Regional Economic Organizations (EAC, ECOWAS, COMESA, SADC)"),
            42: ("Vegetation zones in Africa are distributed according to climate.", "Vegetation Zones & Climate of Africa (Equatorial, Savanna, Mediterranean)"),
            43: ("Transportation network plays a key role in regional trade.", "Transport & Communication Systems in Africa (Road, Water, Air, Rail)"),
            44: ("Foreign influence in Africa led to colonization and scramble for territories.", "Scramble & Partition of Africa (European colonial administration policies)"),
            45: ("Pan-African leaders fought tirelessly for independence across African states.", "Pan-African Movement & Independence Leaders (Nkrumah, Nyerere, Garvey, Kenyatta)"),
            46: ("The Gezira Irrigation Scheme is located in Sudan between the Blue Nile and White Nile.", "Irrigation Schemes in Africa (Gezira, Kilombero, Mwea-Tebere)"),
            47: ("The Organization of African Unity (OAU) was formed in 1963 and later transformed into the African Union (AU).", "OAU & African Union (AU organs, achievements, and challenges)"),
            48: ("Mining is an important economic activity in South Africa, Zambia, and Democratic Republic of Congo.", "Mining & Mineral Resources in Africa (Gold, Copper, Diamonds, Petroleum)"),
            49: ("Weather elements are measured using different instruments kept at a weather station.", "Weather & Climate Measuring Instruments (Stevenson Screen, Barometer, Rain gauge)"),
            50: ("Study the sketch map of Africa below and use it to answer the questions that follow.", "Map Work & Physical Features of Africa (Rivers, Lakes, Mountains, Enclave states)"),
            51: ("Answer Either the Christian OR Islamic option for Question 51.", "RE Option 51: Concept of Success & Faith in Life (Either: Christian / OR: Islamic)"),
            52: ("Answer Either the Christian OR Islamic option for Question 52.", "RE Option 52: Exemplary Persons & Showing Mercy (Either: Christian / OR: Islamic)"),
            53: ("Answer Either the Christian OR Islamic option for Question 53.", "RE Option 53: Religious Laws & Moral Commandments (Either: Christian / OR: Islamic)"),
            54: ("Answer Either the Christian OR Islamic option for Question 54.", "RE Option 54: Religious Organizations & National Development (Either: Christian / OR: Islamic)"),
            55: ("The question below is for Both Christians and Muslims.", "RE Joint Option 55: Day of Judgment & Shared Religious Values (For Both)")
        }
        statement, topic_desc = topics.get(q_num, ("Study the topic below and answer the questions that follow.", "SST & RE Strand"))
        return f"""
### UGANDA P.7 SST & RELIGIOUS EDUCATION GENERATOR (SECTION B: Q{q_num})
TOPIC STRAND: {topic_desc}
REQUIREMENT: Exactly 4 MARKS TOTAL for Q{q_num}.

Generate Question {q_num} for Section B:
- "text": MUST be the introductory context statement: "{statement}"
- "type": "structured", "marks": 4
- "sub_questions": Exactly 3 to 4 sub-questions (a), (b), (c), (d) containing the actual questions and totaling exactly 4 marks.
- For RE Options Q51-Q54, format with Either (Christian) / OR (Islamic) options clearly labeled.

Return JSON:
{{
  "questions": [
    {{
      "number": {q_num},
      "text": "{statement}",
      "context_block": "",
      "type": "structured",
      "marks": 4,
      "sub_questions": [
        {{ "label": "(a)", "text": "Name the country marked...", "marks": 1 }},
        {{ "label": "(b)", "text": "State two reasons...", "marks": 2 }},
        {{ "label": "(c)", "text": "Give one importance...", "marks": 1 }}
      ]
    }}
  ]
}}
"""

    @staticmethod
    async def generate_sec_a_chunk(start_num: int, count: int) -> List[dict]:
        client = get_async_openai_client()
        prompt = P7SSTEngine.synthesize_sec_a_prompt(start_num, count)

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
                raw_text = q.get("text", "")
                if "...." not in raw_text and "____" not in raw_text:
                    raw_text += " .........................................."
                else:
                    raw_text = re.sub(r'_{3,}', '..........................................', raw_text)
                q["text"] = raw_text
            return qs[:count]
        except Exception as e:
            print(f"P7 SST Sec A Chunk Error (Q{start_num}): {e}")
            fallback = []
            sample_sst_qs = {
                1: "Give one way a school motto is important. ..........................................",
                2: "Why are the Miombo woodlands of central Tanzania suitable for bee keeping? ..........................................",
                3: "Mention any one social importance of cattle to the Karimojong people. ..........................................",
                4: "How did the introduction of ABEK improve livelihood in Karamoja sub-region? ..........................................",
                5: "How is a caterer different from a seamstress? ..........................................",
                6: "Write one way a national constitution helps to promote peace. ..........................................",
                7: "Why is air transport suitable in areas with high traffic and urgent goods? ..........................................",
                8: "Give a reason why the government introduced digitalized vehicle number plates. ..........................................",
                9: "Write one economic activity carried out at the senile stage of a river. ..........................................",
                10: "State the reason why agricultural mechanization is difficult in some parts of Kabale. ..........................................",
                11: "Mention one reason why donkeys are mainly reared in mountainous areas. ..........................................",
                12: "How did the Great Trek affect urban development in the interior of South Africa? ..........................................",
                13: "Write one way the government of Uganda is trying to solve the challenge of corruption. ..........................................",
                14: "State the reason why Rwanda uses French as an official language. ..........................................",
                15: "Define the term 'time zone'. ..........................................",
                16: "How do water hyacinth beetles help to improve water transport on Lake Victoria? ..........................................",
                17: "Mention one way sand dunes are dangerous to people living in desert areas. ..........................................",
                18: "How does the United Nations Security Council promote world peace? ..........................................",
                19: "Mention one way Tanzania helped to fight against the apartheid policy in South Africa. ..........................................",
                20: "State the political reason for the transfer of the capital city of Burundi from Bujumbura to Gitega. ..........................................",
                21: "State the main line of latitude marked 0 degrees on the globe. ..........................................",
                22: "Give one challenge faced during national electoral processes in Uganda. ..........................................",
                23: "How have hotels and hospitality industries promoted trade in Uganda? ..........................................",
                24: "Mention one way dictatorship governance is dangerous to a country. ..........................................",
                25: "Name any one example of material culture in East Africa. ..........................................",
                26: "Write one ethnic group under plain Nilotes that lives in both Kenya and Tanzania. ..........................................",
                27: "How did Marcus Garvey promote Pan-African development in Africa? ..........................................",
                28: "State the main reason why the French used Assimilation policy in West Africa. ..........................................",
                29: "Apart from interpreting laws, state one other role of the judiciary in Uganda. ..........................................",
                30: "State one reason that delayed Uganda's attainment of independence before 1962. ..........................................",
                31: "Name the military monitoring wing that promotes security in ECOWAS member states. ..........................................",
                32: "Write one way good security in rural areas promotes urban-rural migration. ..........................................",
                33: "State one reason why lions are mainly found in savanna grasslands. ..........................................",
                34: "Give one reason why Ghana was the first country in Black Africa to gain independence. ..........................................",
                35: "Name the economic grouping that unites Eastern and Southern African states. ..........................................",
                36: "State the importance of a compass rose on a map. ..........................................",
                37: "Mention one human activity that leads to desertification in Africa. ..........................................",
                38: "Give one duty of a police officer in maintaining law and order. ..........................................",
                39: "State the main cash crop grown on the Gezira Irrigation Scheme in Sudan. ..........................................",
                40: "Name the European explorer who renamed Lake Lutu Nzige as Lake Albert. .........................................."
            }
            for idx in range(count):
                qnum = start_num + idx
                fallback.append({
                    "number": qnum,
                    "text": sample_sst_qs.get(qnum, f"State one importance of Social Studies in daily life. .........................................."),
                    "type": "short_answer",
                    "marks": 1
                })
            return fallback

    @staticmethod
    async def generate_sec_b_item(q_num: int) -> dict:
        client = get_async_openai_client()
        prompt = P7SSTEngine.synthesize_sec_b_prompt(q_num)

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
                q["marks"] = 4
                return q
            raise ValueError(f"No item generated for Q{q_num}")
        except Exception as e:
            print(f"P7 SST Sec B Item Error (Q{q_num}): {e}")
            fallback_sec_b = {
                41: {
                    "number": 41,
                    "text": "The sketch map of Africa below shows regional economic groupings.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the regional economic grouping that unites West African states.", "marks": 1 },
                        { "label": "(b)", "text": "State any two member countries of the East African Community (EAC).", "marks": 2 },
                        { "label": "(c)", "text": "Give one benefit of economic integration to trade in Africa.", "marks": 1 }
                    ]
                },
                42: {
                    "number": 42,
                    "text": "Vegetation zones in Africa are distributed according to climatic regions.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the vegetation zone that experiences hot and wet climate throughout the year.", "marks": 1 },
                        { "label": "(b)", "text": "Mention any two economic activities carried out in Savanna vegetation zones.", "marks": 2 },
                        { "label": "(c)", "text": "Give one reason why desert vegetation consists mainly of thorny plants.", "marks": 1 }
                    ]
                },
                43: {
                    "number": 43,
                    "text": "Transportation network plays a key role in regional trade across African countries.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "State the most common means of transport used to carry heavy goods in landlocked countries.", "marks": 1 },
                        { "label": "(b)", "text": "Mention any two challenges facing railway transport in East Africa.", "marks": 2 },
                        { "label": "(c)", "text": "Give one way pipeline transport is advantageous over road transport.", "marks": 1 }
                    ]
                },
                44: {
                    "number": 44,
                    "text": "Foreign influence in Africa led to colonization and scramble for African territories.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the European conference held in 1884-1885 to partition Africa.", "marks": 1 },
                        { "label": "(b)", "text": "State the colonial administration policy used by the British in Uganda and Nigeria.", "marks": 1 },
                        { "label": "(c)", "text": "Give any two negative effects of colonial rule on African societies.", "marks": 2 }
                    ]
                },
                45: {
                    "number": 45,
                    "text": "Pan-African leaders fought tirelessly for independence across African states.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the Pan-African leader who led Ghana to independence in 1957.", "marks": 1 },
                        { "label": "(b)", "text": "Mention the Pan-African leader who founded Tanganyika African National Union (TANU).", "marks": 1 },
                        { "label": "(c)", "text": "State any two objectives of the Pan-African Movement.", "marks": 2 }
                    ]
                },
                46: {
                    "number": 46,
                    "text": "The Gezira Irrigation Scheme is located in Sudan between the Blue Nile and White Nile.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Mention any two roles of tenant farmers on the Gezira Irrigation Scheme.", "marks": 2 },
                        { "label": "(b)", "text": "How have outgrower farmers benefited from the Gezira Scheme?", "marks": 1 },
                        { "label": "(c)", "text": "Write one way the challenge of silting of canals has been solved on the Gezira Scheme.", "marks": 1 }
                    ]
                },
                47: {
                    "number": 47,
                    "text": "The Organization of African Unity (OAU) was formed in 1963 in Addis Ababa.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the headquarters of the African Union (AU).", "marks": 1 },
                        { "label": "(b)", "text": "Mention any two achievements of the OAU in African history.", "marks": 2 },
                        { "label": "(c)", "text": "State one challenge currently facing the African Union.", "marks": 1 }
                    ]
                },
                48: {
                    "number": 48,
                    "text": "Mining is an important economic activity in South Africa, Zambia, and DR Congo.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the main mineral mined in Witwatersrand in South Africa.", "marks": 1 },
                        { "label": "(b)", "text": "Mention the mineral mined in the Copperbelt region of Zambia.", "marks": 1 },
                        { "label": "(c)", "text": "State any two environmental dangers associated with open-cast mining.", "marks": 2 }
                    ]
                },
                49: {
                    "number": 49,
                    "text": "Weather elements are measured using different instruments kept at a weather station.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "How is the work of a windsock different from that of a wind vane?", "marks": 1 },
                        { "label": "(b)", "text": "Mention the reason why rainfall is measured in millimeters (mm).", "marks": 1 },
                        { "label": "(c)", "text": "How is weather forecasting important to a crop farmer?", "marks": 1 },
                        { "label": "(d)", "text": "Why is a barometer kept inside a Stevenson screen?", "marks": 1 }
                    ]
                },
                50: {
                    "number": 50,
                    "text": "Study the sketch map of Africa below and answer question number 50.",
                    "context_block": "<div style='text-align:center; margin:10px 0;'><svg width='260' height='200' viewBox='0 0 260 200' style='border:1px solid #ccc; background:#e0f2fe;'><path d='M80,20 Q140,15 200,30 Q240,60 220,120 Q180,180 130,190 Q90,160 60,110 Q50,60 80,20 Z' fill='#d97706' stroke='#78350f'/><text x='110' y='160' font-size='12' font-weight='bold' fill='#fff'>Lesotho (Z)</text><path d='M90,50 Q110,70 130,60' stroke='#0284c7' stroke-width='2' fill='none'/><text x='135' y='65' font-size='10' font-weight='bold' fill='#0284c7'>R. Benue (M)</text></svg></div>",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the enclave country marked Z in South Africa.", "marks": 1 },
                        { "label": "(b)", "text": "Why is the country marked Z called an enclave state?", "marks": 1 },
                        { "label": "(c)", "text": "How is the river marked M related to River Niger?", "marks": 1 },
                        { "label": "(d)", "text": "Name the water body that borders Africa to the East.", "marks": 1 }
                    ]
                },
                51: {
                    "number": 51,
                    "text": "For Question 51, answer Either the Christian OR Islamic option.",
                    "context_block": "<div style='margin-bottom:10px;'><b>Either (Christian):</b></div><div style='margin-left:15px;'>(a) What is success according to Christian teaching?<br>(b) Give any two ways a Christian can be successful in life.<br>(c) Write any one sign of success to a Christian.</div><div style='margin-top:15px; margin-bottom:10px;'><b>OR (Islamic):</b></div><div style='margin-left:15px;'>(a) What is success according to Islamic teaching?<br>(b) Give any two ways a Muslim can be successful in life.<br>(c) Write any one sign of success to a Muslim.</div>",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": []
                },
                52: {
                    "number": 52,
                    "text": "For Question 52, answer Either the Christian OR Islamic option.",
                    "context_block": "<div style='margin-bottom:10px;'><b>Either (Christian):</b></div><div style='margin-left:15px;'>(a) Write short notes about Mother Theresa and Princess Diana in Christianity.<br>(b) State any two ways of showing mercy to needy people.</div><div style='margin-top:15px; margin-bottom:10px;'><b>OR (Islamic):</b></div><div style='margin-left:15px;'>(a) Write short notes about Prophet Ayyub and Sulaiman in Islam.<br>(b) State any two ways of showing mercy to needy people.</div>",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": []
                },
                53: {
                    "number": 53,
                    "text": "For Question 53, answer Either the Christian OR Islamic option.",
                    "context_block": "<div style='margin-bottom:10px;'><b>Either (Christian):</b></div><div style='margin-left:15px;'>(a) Name the two greatest commandments as summarized by Jesus Christ.<br>(b) How does reading the Holy Bible promote peace in society?<br>(c) Name one way God communicates to His people.</div><div style='margin-top:15px; margin-bottom:10px;'><b>OR (Islamic):</b></div><div style='margin-left:15px;'>(a) Name any two punishments recommended under Sharia law.<br>(b) Name any two ways of observing Islamic laws in daily life.</div>",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": []
                },
                54: {
                    "number": 54,
                    "text": "For Question 54, answer Either the Christian OR Islamic option.",
                    "context_block": "<div style='margin-bottom:10px;'><b>Either (Christian):</b></div><div style='margin-left:15px;'>(a) Name any two Christian religious organizations in Uganda.<br>(b) How have religious organizations promoted development in Uganda?<br>(c) State one challenge facing Christian organizations in Uganda.</div><div style='margin-top:15px; margin-bottom:10px;'><b>OR (Islamic):</b></div><div style='margin-left:15px;'>(a) Name any two Islamic organizations in Uganda.<br>(b) How have Islamic organizations promoted development in Uganda?<br>(c) State one challenge facing Islamic organizations in Uganda.</div>",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": []
                },
                55: {
                    "number": 55,
                    "text": "The question below is for Both Christians and Muslims.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "State one common belief shared among Christians and Muslims.", "marks": 1 },
                        { "label": "(b)", "text": "Give one reason why believers fear the Day of Judgment.", "marks": 1 },
                        { "label": "(c)", "text": "How should believers prepare for the Day of Judgment?", "marks": 1 },
                        { "label": "(d)", "text": "Mention any one obligation of a good believer in society.", "marks": 1 }
                    ]
                }
            }
            return fallback_sec_b.get(q_num, {
                "number": q_num,
                "text": f"Study the Social Studies item {q_num} and answer the questions that follow.",
                "context_block": "",
                "type": "structured",
                "marks": 4,
                "sub_questions": [
                    { "label": "(a)", "text": "Name the country...", "marks": 1 },
                    { "label": "(b)", "text": "State two reasons...", "marks": 2 },
                    { "label": "(c)", "text": "Give one importance...", "marks": 1 }
                ]
            })

    @staticmethod
    async def stream_paper(brand_name: str = "EDUMERC") -> AsyncGenerator[str, None]:
        title = "SOCIAL STUDIES WITH RELIGIOUS EDUCATION"
        instructions = [
            "Do not write your <b>school</b> or <b>district name</b> anywhere on this paper.",
            "This paper has two sections: <b>A</b> and <b>B</b>.<br>Section <b>A</b> has <b>40</b> questions and section <b>B</b> has <b>15</b> questions. The paper has <b>12 printed pages</b> altogether.",
            "Answer <b>all</b> questions. All answers to both sections <b>A</b> and <b>B</b> must be shown in the spaces provided.",
            "All answers must be written using a <b>blue</b> or <b>black</b> ball point pen or ink. Any work written in pencil will <u><b>NOT</b></u> be marked.",
            "Unnecessary <b>changes</b> in your work and handwriting that cannot easily be read may lead to loss of marks.",
            "Do not fill anything in the boxes. They are for <b>examiners' use</b>."
        ]

        # ── STEP 1: HEADER READY EVENT ──
        header_event = {
            "event_type": "header_ready",
            "title": title,
            "subject": "SOCIAL STUDIES WITH RELIGIOUS EDUCATION",
            "level": "PRIMARY LEAVING EXAMINATIONS",
            "duration": "2 hours 15 minutes",
            "total_marks": 100,
            "instructions": instructions
        }
        yield f"data: {json.dumps(header_event)}\n\n"
        await asyncio.sleep(0.1)

        # ── STEP 2: SECTION A (Q1 - Q40) PARALLEL CHUNKS ──
        yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Drafting Section A (40 SST Questions)...'})}\n\n"

        sec_a_batches = [
            (1, 10),
            (11, 10),
            (21, 10),
            (31, 10)
        ]

        sec_a_tasks = [
            asyncio.create_task(P7SSTEngine.generate_sec_a_chunk(start_num, c_count))
            for start_num, c_count in sec_a_batches
        ]

        sec_a_results = await asyncio.gather(*sec_a_tasks)
        all_sec_a_qs = []
        for chunk in sec_a_results:
            all_sec_a_qs.extend(chunk)

        all_sec_a_qs.sort(key=lambda q: q.get("number", 0))

        for q in all_sec_a_qs:
            q_html = build_question_html("Exams", q, subject="SOCIAL STUDIES WITH RELIGIOUS EDUCATION", level="PRIMARY 7")
            item_evt = {
                "event_type": "question_ready",
                "section": "A",
                "number": q["number"],
                "question_json": q,
                "question_html": q_html
            }
            yield f"data: {json.dumps(item_evt)}\n\n"
            await asyncio.sleep(0.01)

        # ── STEP 3: SECTION B (Q41 - Q55) PARALLEL ITEMS ──
        yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Drafting Section B (15 SST & RE Option Questions)...'})}\n\n"

        sec_b_tasks = [
            asyncio.create_task(P7SSTEngine.generate_sec_b_item(qnum))
            for qnum in range(41, 56)
        ]

        all_sec_b_qs = await asyncio.gather(*sec_b_tasks)
        all_sec_b_qs.sort(key=lambda q: q.get("number", 0))

        for q in all_sec_b_qs:
            q_html = build_question_html("Exams", q, subject="SOCIAL STUDIES WITH RELIGIOUS EDUCATION", level="PRIMARY 7")
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
            exam_type="PRIMARY LEAVING EXAMINATIONS",
            level="PRIMARY 7",
            subject="SOCIAL STUDIES WITH RELIGIOUS EDUCATION",
            term_roman="2025",
            exam_year="2025",
            duration="2 hours 15 minutes",
            school_name="UGANDA NATIONAL EXAMINATIONS BOARD",
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
