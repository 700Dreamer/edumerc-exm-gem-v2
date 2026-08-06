# Authentic UNEB Primary Examination Exemplar Bank (P.1 - P.7 / PLE)
# Provides real UNEB PLE past paper question structures and numerical items

import random
from typing import Dict, List

# ── MATHEMATICS PLE EXEMPLARS (P.4 - P.7) ──
MATH_SEC_A_EXEMPLARS = [
    {"text": "Add: 432 + 158", "marks": 2, "hint": "Line up place values: 432 + 158 = 590"},
    {"text": "Simplify: 3/4 - 1/2", "marks": 2, "hint": "LCM of 4 and 2 is 4: (3 - 2)/4 = 1/4"},
    {"text": "Find the next number in the sequence: 2, 5, 10, 17, _____.", "marks": 2, "hint": "Pattern adds +3, +5, +7, +9 = 26"},
    {"text": "Given that set A = {1, 2, 3, 5, 7} and set B = {2, 4, 6, 7}, find n(A ∩ B).", "marks": 2, "hint": "A ∩ B = {2, 7}, so n(A ∩ B) = 2"},
    {"text": "Change 25% to a fraction in its simplest form.", "marks": 2, "hint": "25/100 = 1/4"},
    {"text": "Find the value of x in the equation: 3x - 5 = 10", "marks": 2, "hint": "3x = 15 => x = 5"},
    {"text": "Express 4:50 p.m. in 24-hour clock system.", "marks": 2, "hint": "4:50 + 12:00 = 1650 hours"},
    {"text": "Work out: (-8) - (-3)", "marks": 2, "hint": "-8 + 3 = -5"},
    {"text": "A trader bought a shirt for UGX 20,000 and sold it for UGX 25,000. Calculate the percentage profit.", "marks": 2, "hint": "Profit = 5,000; % Profit = (5000/20000)*100 = 25%"},
    {"text": "Find the area of a right-angled triangle whose base is 8 cm and height is 6 cm.", "marks": 2, "hint": "Area = 1/2 * b * h = 1/2 * 8 * 6 = 24 cm²"},
    {"text": "Find the median of the numbers: 7, 3, 9, 2, 5.", "marks": 2, "hint": "Arrange in order: 2, 3, 5, 7, 9. Median = 5"},
    {"text": "Calculate the simple interest on UGX 60,000 at a rate of 10% per annum for 2 years.", "marks": 2, "hint": "I = P * R * T = 60000 * 0.10 * 2 = UGX 12,000"},
    {"text": "Find the circumference of a circle whose diameter is 14 cm. (Take π = 22/7)", "marks": 2, "hint": "C = π * d = (22/7) * 14 = 44 cm"},
    {"text": "Solve for y: 2(y + 3) = 14", "marks": 2, "hint": "2y + 6 = 14 => 2y = 8 => y = 4"},
    {"text": "Write 45,089 in words.", "marks": 2, "hint": "Forty-five thousand eighty-nine"}
]

MATH_SEC_B_EXEMPLARS = [
    {
        "text": "In a class of 45 pupils, 25 like English (E), 20 like Mathematics (M), and x like both subjects. 5 pupils like neither subject.",
        "marks": 5,
        "hint": "Use Venn diagram equation: (25 - x) + x + (20 - x) + 5 = 45",
        "sub_questions": [
            {"label": "(a)", "text": "Represent the above information on a Venn diagram.", "marks": 3},
            {"label": "(b)", "text": "Find the value of x.", "marks": 2}
        ]
    },
    {
        "text": "A motorist traveled from Kampala to Masaka, a distance of 120 km, in 2 hours.",
        "marks": 5,
        "hint": "Speed = Distance / Time = 120 / 2 = 60 km/h",
        "sub_questions": [
            {"label": "(a)", "text": "Calculate his average speed in km/h.", "marks": 2},
            {"label": "(b)", "text": "Express his average speed in metres per second (m/s).", "marks": 3}
        ]
    },
    {
        "text": "The pie chart below shows how a farmer spent his monthly income of UGX 720,000 on Food, School Fees, and Savings.",
        "marks": 5,
        "hint": "Total angle = 360 degrees",
        "sub_questions": [
            {"label": "(a)", "text": "If the sector angle for Food is 180°, calculate the amount spent on Food.", "marks": 2},
            {"label": "(b)", "text": "Find the sector angle for School Fees if he spent UGX 240,000 on Fees.", "marks": 3}
        ]
    }
]

# ── INTEGRATED SCIENCE PLE EXEMPLARS ──
SCIENCE_SEC_A_EXEMPLARS = [
    {"text": "Name the organ in the human body responsible for filtering waste from blood.", "marks": 1, "hint": "Kidney"},
    {"text": "State one condition necessary for seed germination.", "marks": 1, "hint": "Water / Oxygen / Suitable temperature"},
    {"text": "Which vector transmits malaria to human beings?", "marks": 1, "hint": "Female Anopheles mosquito"},
    {"text": "Give one reason why farmers weed their crops.", "marks": 1, "hint": "To reduce competition for nutrients"},
    {"text": "State the type of simple machine to which a pair of scissors belongs.", "marks": 1, "hint": "First class lever"},
    {"text": "Why is carbon dioxide gas used in fire extinguishers?", "marks": 1, "hint": "It does not support combustion"},
    {"text": "State the function of red blood cells in the human body.", "marks": 1, "hint": "To transport oxygen"}
]

SCIENCE_SEC_B_EXEMPLARS = [
    {
        "text": "The diagram below shows a simple electric circuit comprising a dry cell, a switch, and a bulb.",
        "marks": 4,
        "hint": "Circuit components and current flow",
        "sub_questions": [
            {"label": "(a)", "text": "Identify the component that provides electrical energy in the circuit.", "marks": 1},
            {"label": "(b)", "text": "State the energy change that occurs in the bulb when the switch is closed.", "marks": 2},
            {"label": "(c)", "text": "Why is copper wire commonly used for electrical connections?", "marks": 1}
        ]
    }
]

# ── SOCIAL STUDIES PLE EXEMPLARS ──
SST_SEC_A_EXEMPLARS = [
    {"text": "Name the major river that flows out of Lake Victoria in Uganda.", "marks": 1, "hint": "River Nile"},
    {"text": "State the main economic activity carried out in pastoral areas of East Africa.", "marks": 1, "hint": "Cattle rearing / Livestock farming"},
    {"text": "Why is a compass rose important to a map reader?", "marks": 1, "hint": "To show direction of places"},
    {"text": "Name the arm of government responsible for making laws in Uganda.", "marks": 1, "hint": "Legislature / Parliament"},
    {"text": "State one quality of a good citizen.", "marks": 1, "hint": "Law-abiding / Honest / Respectful"}
]

# ── ENGLISH PLE EXEMPLARS ──
ENGLISH_SEC_A_EXEMPLARS = [
    {"text": "Fill in the blank space with a suitable word: Neither John _______ Peter attended the school assembly yesterday.", "marks": 1, "hint": "nor"},
    {"text": "Fill in the blank space with a suitable word: She has been studying for the examination _______ morning.", "marks": 1, "hint": "since"},
    {"text": "Use the correct form of the word in brackets to complete the sentence: The pupils sang _______ during the music festival. (beautiful)", "marks": 1, "hint": "beautifully"},
    {"text": "Re-write the sentence as instructed in brackets: The weather was very cold. We could not play outside. (Use: ...so...that...)", "marks": 1, "hint": "The weather was so cold that we could not play outside."}
]

ENGLISH_SEC_B_EXEMPLARS = [
    {
        "text": "Read the story passage below carefully and answer in full sentences the questions that follow:\n\nOnce upon a time in Kasese village, a hardworking farmer named Kato lived with his family near the foot of Mount Rwenzori. Every morning, Kato woke up at dawn to tend to his coffee crops...",
        "marks": 10,
        "hint": "Comprehension passage answers",
        "sub_questions": [
            {"label": "(a)", "text": "Where did Kato live with his family?", "marks": 1},
            {"label": "(b)", "text": "What time did Kato wake up every morning?", "marks": 1},
            {"label": "(c)", "text": "Which crop did Kato grow on his farm?", "marks": 1},
            {"label": "(d)", "text": "Give a suitable title for this story.", "marks": 1}
        ]
    },
    {
        "text": "The sentences below are in jumbled order. Re-arrange them to form a coherent story:\n1. He packed his school bag and put on his uniform.\n2. When he arrived at school, the morning bell was ringing.\n3. Moses woke up early at six o'clock in the morning.\n4. He greeted his teacher and took his seat in class.\n5. He ate a healthy breakfast prepared by his mother.",
        "marks": 10,
        "hint": "Correct sequence: 3, 5, 1, 2, 4",
        "sub_questions": [
            {"label": "(a)", "text": "Write down the correctly ordered story from sentence 1 to 5.", "marks": 10}
        ]
    }
]

def get_authentic_primary_items(subject: str, level: str, section: str = "A", count: int = 5, start_num: int = 1) -> List[dict]:
    """Retrieves authentic UNEB question items for Primary papers."""
    subj_lower = subject.lower()
    
    if "math" in subj_lower:
        bank = MATH_SEC_A_EXEMPLARS if section == "A" else MATH_SEC_B_EXEMPLARS
    elif "science" in subj_lower:
        bank = SCIENCE_SEC_A_EXEMPLARS if section == "A" else SCIENCE_SEC_B_EXEMPLARS
    elif "english" in subj_lower:
        bank = ENGLISH_SEC_A_EXEMPLARS if section == "A" else ENGLISH_SEC_B_EXEMPLARS
    else:
        bank = SST_SEC_A_EXEMPLARS if section == "A" else SST_SEC_A_EXEMPLARS

    results = []
    for idx in range(count):
        q_num = start_num + idx
        base_item = bank[idx % len(bank)].copy()
        base_item["number"] = q_num
        base_item["type"] = "short_answer" if section == "A" else "structured"
        results.append(base_item)

    return results
