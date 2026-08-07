# Dedicated Primary 7 Integrated Science Examination Engine (P.7 Science)
# Official UNEB PLE Standard Specifications derived from sample papers in sample papers/p.7/

import json
import re
import asyncio
from typing import List, Dict, AsyncGenerator
from core.ai_engine import get_async_openai_client
from ui.document_builder import build_question_html, build_full_html

class P7ScienceEngine:
    """
    Dedicated generation engine for Primary 7 Integrated Science (PLE Specification).
    Matches 100% of UNEB specimen papers in sample papers/p.7/
    - Section A: Q1 - Q40 (40 Marks, 1 mark each)
    - Section B: Q41 - Q55 (60 Marks, 4 marks each across 15 distinct topics)
    """

    @staticmethod
    def synthesize_sec_a_prompt(start_num: int, count: int) -> str:
        end_num = start_num + count - 1
        return f"""
### UGANDA P.7 INTEGRATED SCIENCE GENERATOR (SECTION A)
QUESTIONS: Q{start_num} to Q{end_num} (Count: {count})
INSTRUCTION: "In each of the questions {start_num} to {end_num}, answer the question in brief."

Generate exactly {count} short-answer primary science questions for Primary 7 starting at Q{start_num}.
- Directly test core Ugandan P.7 Science syllabus strands: Human body & Health, Energy & Matter, Agriculture & Environment, Living things & Classification.
- Each item MUST have "type": "short_answer", "marks": 1.
- Provide dotted line fill space at the end of each stem: "..........................................".

Return JSON:
{{
  "questions": [
    {{
      "number": {start_num},
      "text": "State the main function of the human heart. ..........................................",
      "type": "short_answer",
      "marks": 1
    }}
  ]
}}
"""

    @staticmethod
    def synthesize_sec_b_prompt(q_num: int) -> str:
        topics = {
            41: ("The list below shows cassava, sweet potatoes, and coco yams.", "Crop Husbandry (Cassava, Yams, Tuber crops care and processing)"),
            42: ("The diagram below shows the human eye. Study and use it to answer the questions that follow.", "Human Organ System (Eye / Ear anatomy, functions and care)"),
            43: ("Poultry farming is an important agricultural activity in Uganda.", "Poultry Keeping (Systems of poultry, perches, vices, disease control)"),
            44: ("The table below shows energy resources and their primary sources. Complete the table correctly.", "Energy Resources (Energy sources completion table: Biomass, Solar, Wind, Uranium)"),
            45: ("You are provided with toothpaste, clean water, and a toothbrush. Describe four steps you would follow to clean your teeth correctly.", "Personal Hygiene (Teeth care steps: Toothpaste, toothbrush, water)"),
            46: ("Matter exists in three main states: solids, liquids, and gases.", "Properties of Matter & Heat Transfer (States of matter, Conduction, Convection, Radiation)"),
            47: ("The diagram below shows a water cycle. Study and use it to answer the questions that follow.", "Water Cycle (Diagram of evaporation, condensation, precipitation, transpiration)"),
            48: ("The excretory system removes metabolic waste products from the body.", "Excretory System (Kidneys, nitrogenous wastes in urine, wetland conservation)"),
            49: ("Answer the calculation questions below about volume and density.", "Density & Volume Calculations (Calculation of volume = mass/density with working steps)"),
            50: ("The table below shows different types of seed germination. Study it carefully and answer the questions that follow.", "Seed Germination (Comparison table of Epigeal vs Hypogeal germination in maize/beans)"),
            51: ("Worms are classified into different groups according to their body structure.", "Worm Classification (Flatworms, Roundworms, Annelids, environmental importance)"),
            52: ("Simple machines help to make work easier by reducing the effort needed.", "Simple Machines (Levers, Pulleys, Mechanical Advantage applications)"),
            53: ("Electric circuits are used to power electrical appliances safely.", "Electricity & Magnetism (Series vs Parallel circuits, switches, magnetic properties)"),
            54: ("Soil fertility is essential for good crop yield in farming.", "Soil Erosion & Fertility (Human impacts, fertilizers, sustainable soil management)"),
            55: ("Immunization protects infants and children against dangerous childhood killer diseases.", "Immunization & Vaccination (Vaccination schedule table: Tetanus, BCG, DPT, Measles)")
        }
        statement, topic_desc = topics.get(q_num, ("Study the topic below and answer the questions that follow.", "Integrated Science Strand"))
        return f"""
### UGANDA P.7 INTEGRATED SCIENCE GENERATOR (SECTION B: Q{q_num})
TOPIC STRAND: {topic_desc}
REQUIREMENT: Exactly 4 MARKS TOTAL for Q{q_num}.

Generate Question {q_num} for Section B:
- "text": MUST be the introductory context statement: "{statement}"
- "type": "structured", "marks": 4
- "sub_questions": Exactly 3 to 4 sub-questions (a), (b), (c), (d) containing the actual questions and totaling exactly 4 marks.
- Include HTML tables or SVG diagrams in "context_block" where applicable.

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
        {{ "label": "(a)", "text": "State the main function...", "marks": 1 }},
        {{ "label": "(b)", "text": "Give two reasons...", "marks": 2 }},
        {{ "label": "(c)", "text": "Name one example...", "marks": 1 }}
      ]
    }}
  ]
}}
"""

    @staticmethod
    async def generate_sec_a_chunk(start_num: int, count: int) -> List[dict]:
        client = get_async_openai_client()
        prompt = P7ScienceEngine.synthesize_sec_a_prompt(start_num, count)

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
            print(f"P7 Science Sec A Chunk Error (Q{start_num}): {e}")
            fallback = []
            sample_science_qs = {
                1: "Name the type of latrine that separates faeces from urine. ..........................................",
                2: "Identify the source of kinetic energy used in the production of electricity at a geothermal power station. ..........................................",
                3: "Give the meaning of the term soil erosion. ..........................................",
                4: "Identify the role of the liver as an excretory organ. ..........................................",
                5: "Name the property of magnets used in a magnetic compass. ..........................................",
                6: "Give one way in which a compass is useful to pilots. ..........................................",
                7: "Apart from adolescent girls, give one other group of people who receive Tetanus Toxoid vaccine during immunization. ..........................................",
                8: "Mention any one human activity that can lead to soil exhaustion. ..........................................",
                9: "Name the germ that causes bilharzia in humans. ..........................................",
                10: "Identify the group of living things to which a butterfly belongs. ..........................................",
                11: "Give any one exotic breed of rabbits kept in your community. ..........................................",
                12: "Identify any one example of non-living resources in the environment. ..........................................",
                13: "Mention any one example of common accidents on roads. ..........................................",
                14: "Give any one way in which fungi are harmful to people in the environment. ..........................................",
                15: "State any one way in which friction can be reduced in machines. ..........................................",
                16: "Name the organ in the human body responsible for filtering blood to produce urine. ..........................................",
                17: "Identify the part of an insect which performs the same function as the human lung. ..........................................",
                18: "State any one condition that leads to swarming of bees. ..........................................",
                19: "Identify any one example of plant habitats. ..........................................",
                20: "Mention any one type of chicken kept for egg production. ..........................................",
                21: "State the danger of teenage pregnancy to young girls. ..........................................",
                22: "Give any one reason why sheep farmers carry out docking. ..........................................",
                23: "State the cause of marasmus in young children. ..........................................",
                24: "State how isolation of infected animals prevents viral diseases in cattle. ..........................................",
                25: "Give any one activity at home that requires the filtration method. ..........................................",
                26: "State any one way conducting health parades promotes health at school. ..........................................",
                27: "Give any one characteristic of living things. ..........................................",
                28: "Identify one material used for keeping the human body clean. ..........................................",
                29: "Give any one advantage of breast feeding to the family. ..........................................",
                30: "Mention any one way roughage helps to prevent constipation. ..........................................",
                31: "State the function of red blood cells in the human body. ..........................................",
                32: "Identify the gas absorbed by green plants during photosynthesis. ..........................................",
                33: "State the primary source of energy for the water cycle. ..........................................",
                34: "Give any one example of an inclined plane used at school. ..........................................",
                35: "Name the vector that spreads malaria fever to humans. ..........................................",
                36: "State any one danger of wind in the environment. ..........................................",
                37: "Give any one use of animal cow dung to people. ..........................................",
                38: "Name any one disease that spreads due to poor disposal of refuse. ..........................................",
                39: "Why should people spread out their beddings regularly in sunlight? ..........................................",
                40: "State the function of the fuse in an electric circuit. .........................................."
            }
            for idx in range(count):
                qnum = start_num + idx
                fallback.append({
                    "number": qnum,
                    "text": sample_science_qs.get(qnum, f"State one importance of science in daily life. .........................................."),
                    "type": "short_answer",
                    "marks": 1
                })
            return fallback

    @staticmethod
    async def generate_sec_b_item(q_num: int) -> dict:
        client = get_async_openai_client()
        prompt = P7ScienceEngine.synthesize_sec_b_prompt(q_num)

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
            print(f"P7 Science Sec B Item Error (Q{q_num}): {e}")
            # Pre-built authentic UNEB 4-mark Section B items Q41 to Q55
            fallback_sec_b = {
                41: {
                    "number": 41,
                    "text": "The list below shows cassava, sweet potatoes, and coco yams.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "State any one way of caring for cassava crops in the garden.", "marks": 1 },
                        { "label": "(b)", "text": "State any one way of caring for coco yams.", "marks": 1 },
                        { "label": "(c)", "text": "Mention any two ways of processing cassava after harvesting.", "marks": 2 }
                    ]
                },
                42: {
                    "number": 42,
                    "text": "The diagram below shows the human eye. Study and use it to answer the questions that follow.",
                    "context_block": "<div style='text-align:center; margin:10px 0;'><svg width='260' height='160' viewBox='0 0 260 160' style='border:1px solid #ccc; background:#fff;'><circle cx='130' cy='80' r='60' stroke='#000' stroke-width='2' fill='none'/><path d='M70,80 Q100,50 130,50 Q160,50 190,80' stroke='#000' stroke-width='1.5' fill='none'/><ellipse cx='85' cy='80' rx='10' ry='25' stroke='#000' stroke-width='2' fill='#f1f5f9'/><text x='75' y='45' font-size='12' font-weight='bold'>A (Lens)</text><text x='185' y='85' font-size='12' font-weight='bold'>K (Retina)</text></svg></div>",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the part marked A in the diagram.", "marks": 1 },
                        { "label": "(b)", "text": "State the function of the part marked A.", "marks": 1 },
                        { "label": "(c)", "text": "State any one characteristic of the image formed at part K.", "marks": 1 },
                        { "label": "(d)", "text": "Give one defect of the human eye.", "marks": 1 }
                    ]
                },
                43: {
                    "number": 43,
                    "text": "Poultry farming is an important agricultural activity in Uganda.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Apart from deep litter system, give any two other systems of keeping poultry.", "marks": 2 },
                        { "label": "(b)", "text": "Explain one way in which perches control poultry vices in a deep litter system.", "marks": 1 },
                        { "label": "(c)", "text": "Mention one common disease that affects poultry.", "marks": 1 }
                    ]
                },
                44: {
                    "number": 44,
                    "text": "The table below shows energy resources and their primary sources. Complete the table correctly.",
                    "context_block": "<table border='1' style='border-collapse:collapse; width:100%; text-align:center; font-size:13px; border:1px solid #000;'><tr style='background:#f1f5f9;'><th>Energy Resource</th><th>Source</th></tr><tr><td>Biomass energy</td><td>(i) ..........................................</td></tr><tr><td>Uranium</td><td>(ii) ..........................................</td></tr><tr><td>Biogas</td><td>(iii) ..........................................</td></tr><tr><td>Wind energy</td><td>(iv) ..........................................</td></tr></table>",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": []
                },
                45: {
                    "number": 45,
                    "text": "You are provided with toothpaste, clean water, and a toothbrush. Describe four steps you would follow to clean your teeth correctly.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(i)", "text": "Step 1: ....................................................................................................", "marks": 1 },
                        { "label": "(ii)", "text": "Step 2: ....................................................................................................", "marks": 1 },
                        { "label": "(iii)", "text": "Step 3: ....................................................................................................", "marks": 1 },
                        { "label": "(iv)", "text": "Step 4: ....................................................................................................", "marks": 1 }
                    ]
                },
                46: {
                    "number": 46,
                    "text": "Matter exists in three main states: solids, liquids, and gases.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Identify any two properties of matter.", "marks": 2 },
                        { "label": "(b)", "text": "Name the state of matter in which heat travels fastest by convection.", "marks": 1 },
                        { "label": "(c)", "text": "Name the state of matter in which heat travels fastest by conduction.", "marks": 1 }
                    ]
                },
                47: {
                    "number": 47,
                    "text": "The diagram below shows a water cycle. Study and use it to answer the questions that follow.",
                    "context_block": "<div style='text-align:center; margin:10px 0;'><svg width='280' height='150' viewBox='0 0 280 150' style='border:1px solid #ccc; background:#e0f2fe;'><circle cx='40' cy='35' r='20' fill='#fde047' stroke='#ca8a04'/><text x='30' y='38' font-size='10' font-weight='bold'>SUN</text><path d='M160,30 Q180,15 200,30 Q220,15 240,30 Q250,45 230,55 Q200,60 160,50 Z' fill='#94a3b8'/><text x='180' y='42' font-size='11' font-weight='bold' fill='#fff'>Clouds (Condensation)</text><path d='M20,120 Q140,110 260,120 L260,150 L20,150 Z' fill='#0284c7'/><text x='110' y='140' font-size='11' font-weight='bold' fill='#fff'>Water Body</text><text x='90' y='85' font-size='12' font-weight='bold' fill='#0369a1'>B (Evaporation ↑)</text></svg></div>",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Identify the process that is taking place at B.", "marks": 1 },
                        { "label": "(b)", "text": "State any one danger of prolonged hot sun in the environment.", "marks": 1 },
                        { "label": "(c)", "text": "State any one danger of heavy dark clouds in the environment.", "marks": 1 },
                        { "label": "(d)", "text": "Give one way in which plants are important in the water cycle.", "marks": 1 }
                    ]
                },
                48: {
                    "number": 48,
                    "text": "The excretory system removes metabolic waste products from the body.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Identify the nitrogenous waste found in human urine.", "marks": 1 },
                        { "label": "(b)", "text": "State any one function of the kidney in the human body.", "marks": 1 },
                        { "label": "(c)", "text": "Give a reason why wetlands are referred to as the natural kidney of the Earth.", "marks": 1 },
                        { "label": "(d)", "text": "Mention any one way of keeping the excretory system healthy.", "marks": 1 }
                    ]
                },
                49: {
                    "number": 49,
                    "text": "Answer the calculation questions below about volume and density.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the method used to find the volume of an irregular object.", "marks": 1 },
                        { "label": "(b)", "text": "Find the volume of a stone of density 8 g/cm³ and mass 160 g. (Show your working clearly)", "marks": 3 }
                    ]
                },
                50: {
                    "number": 50,
                    "text": "The table below shows different types of seed germination. Study it carefully and answer the questions that follow.",
                    "context_block": "<table border='1' style='border-collapse:collapse; width:100%; text-align:center; font-size:13px; border:1px solid #000;'><tr style='background:#f1f5f9;'><th>Crop</th><th>Type of Germination</th></tr><tr><td>Groundnuts / Beans</td><td>(R) ..........................................</td></tr><tr><td>Maize / Millet / Peas</td><td>Hypogeal germination</td></tr></table>",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the type of germination marked R.", "marks": 1 },
                        { "label": "(b)", "text": "Give a reason why groundnuts are grouped under the germination type marked R.", "marks": 1 },
                        { "label": "(c)", "text": "Identify any two conditions needed for seed germination to take place.", "marks": 2 }
                    ]
                },
                51: {
                    "number": 51,
                    "text": "Worms are classified into different groups according to their body structure.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Identify the group of worms to which an earthworm belongs.", "marks": 1 },
                        { "label": "(b)", "text": "Give any one way of controlling tapeworms in humans.", "marks": 1 },
                        { "label": "(c)", "text": "State any two ways in which earthworms are important in the soil environment.", "marks": 2 }
                    ]
                },
                52: {
                    "number": 52,
                    "text": "Simple machines help to make work easier by reducing the effort needed.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Define what a simple machine is.", "marks": 1 },
                        { "label": "(b)", "text": "Give any two examples of simple machines used at home.", "marks": 2 },
                        { "label": "(c)", "text": "State one way friction affects the efficiency of machines.", "marks": 1 }
                    ]
                },
                53: {
                    "number": 53,
                    "text": "Electric circuits are used to power electrical appliances safely.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Differentiate between a series circuit and a parallel circuit.", "marks": 2 },
                        { "label": "(b)", "text": "State the function of a switch in an electric circuit.", "marks": 1 },
                        { "label": "(c)", "text": "Give one safety device used to prevent electric shock in a house.", "marks": 1 }
                    ]
                },
                54: {
                    "number": 54,
                    "text": "Soil fertility is essential for good crop yield in farming.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Identify two human activities that negatively affect soil fertility.", "marks": 2 },
                        { "label": "(b)", "text": "Describe how organic manure improves soil structure.", "marks": 1 },
                        { "label": "(c)", "text": "State one sustainable farming practice that prevents soil erosion.", "marks": 1 }
                    ]
                },
                55: {
                    "number": 55,
                    "text": "Immunization protects infants and children against dangerous childhood killer diseases.",
                    "context_block": "",
                    "type": "structured",
                    "marks": 4,
                    "sub_questions": [
                        { "label": "(a)", "text": "Name the vaccine given at birth to protect against Tuberculosis.", "marks": 1 },
                        { "label": "(b)", "text": "State the site on the body where Measles vaccine is administered.", "marks": 1 },
                        { "label": "(c)", "text": "Mention any two childhood killer diseases immunized against using DPT vaccine.", "marks": 2 }
                    ]
                }
            }
            return fallback_sec_b.get(q_num, {
                "number": q_num,
                "text": f"Study the Integrated Science item {q_num} and answer the questions that follow.",
                "context_block": "",
                "type": "structured",
                "marks": 4,
                "sub_questions": [
                    { "label": "(a)", "text": "State the main function...", "marks": 1 },
                    { "label": "(b)", "text": "Give two reasons...", "marks": 2 },
                    { "label": "(c)", "text": "Name one example...", "marks": 1 }
                ]
            })

    @staticmethod
    async def stream_paper(brand_name: str = "EDUMERC") -> AsyncGenerator[str, None]:
        title = "INTEGRATED SCIENCE"
        instructions = [
            "Do not write your <b>school</b> or <b>district name</b> anywhere on this paper.",
            "This paper has two sections: <b>A</b> and <b>B</b>.<br>Section <b>A</b> has <b>40</b> questions and section <b>B</b> has <b>15</b> questions. The paper has <b>16 printed pages</b> altogether.",
            "Answer <b>all</b> questions. All answers to both sections <b>A</b> and <b>B</b> must be shown in the spaces provided.",
            "All answers must be written using a <b>blue</b> or <b>black</b> ball point pen or ink. Any work written in pencil other than drawing will <u><b>NOT</b></u> be marked.",
            "Unnecessary <b>changes</b> in your work and handwriting that cannot easily be read may lead to loss of marks.",
            "Do not fill anything in the boxes. They are for <b>examiners' use</b>."
        ]

        # ── STEP 1: HEADER READY EVENT ──
        header_event = {
            "event_type": "header_ready",
            "title": title,
            "subject": "INTEGRATED SCIENCE",
            "level": "PRIMARY LEAVING EXAMINATIONS",
            "duration": "2 hours 15 minutes",
            "total_marks": 100,
            "instructions": instructions
        }
        yield f"data: {json.dumps(header_event)}\n\n"
        await asyncio.sleep(0.1)

        # ── STEP 2: SECTION A (Q1 - Q40) PARALLEL CHUNKS ──
        yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Drafting Section A (40 Integrated Science Questions)...'})}\n\n"

        sec_a_batches = [
            (1, 10),
            (11, 10),
            (21, 10),
            (31, 10)
        ]

        sec_a_tasks = [
            asyncio.create_task(P7ScienceEngine.generate_sec_a_chunk(start_num, c_count))
            for start_num, c_count in sec_a_batches
        ]

        sec_a_results = await asyncio.gather(*sec_a_tasks)
        all_sec_a_qs = []
        for chunk in sec_a_results:
            all_sec_a_qs.extend(chunk)

        all_sec_a_qs.sort(key=lambda q: q.get("number", 0))

        for q in all_sec_a_qs:
            q_html = build_question_html("Exams", q, subject="INTEGRATED SCIENCE", level="PRIMARY 7")
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
        yield f"data: {json.dumps({'event_type': 'status_update', 'message': 'Drafting Section B (15 Science Structured & Diagram Questions)...'})}\n\n"

        sec_b_tasks = [
            asyncio.create_task(P7ScienceEngine.generate_sec_b_item(qnum))
            for qnum in range(41, 56)
        ]

        all_sec_b_qs = await asyncio.gather(*sec_b_tasks)
        all_sec_b_qs.sort(key=lambda q: q.get("number", 0))

        for q in all_sec_b_qs:
            q_html = build_question_html("Exams", q, subject="INTEGRATED SCIENCE", level="PRIMARY 7")
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
            subject="INTEGRATED SCIENCE",
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
