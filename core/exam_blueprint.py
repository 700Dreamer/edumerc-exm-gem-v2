import math
from core.syllabus_master import get_master_topics

def generate_exam_blueprint(subject: str, level: str, term: str, question_count: int, specific_topic: str = "", max_questions_per_topic: int = 2) -> dict:
    """
    Generates a deterministic mapping of Question Numbers to specific syllabus topics.
    STRICT RULE: Include a maximum of 2 questions per topic across the exam paper.
    Returns a dictionary like: {"Q1": "Sets", "Q2": "Whole Numbers", ...}
    """
    blueprint = {}
    master_topics = get_master_topics(subject, level) or []
    
    # Build list of available topic candidates
    if specific_topic and specific_topic.strip():
        base_topic = specific_topic.strip()
        candidates = [
            f"{base_topic} - Concept & Definition",
            f"{base_topic} - Computation & Working",
            f"{base_topic} - Word Problems & Application",
            f"{base_topic} - Analysis & Reasoning",
            f"{base_topic} - Data Interpretation",
            f"{base_topic} - Advanced Synthesis",
        ] + [t for t in master_topics if t != base_topic]
    else:
        candidates = list(master_topics)

    # Filter topics based on Term if no specific topic specified
    if not specific_topic:
        term_lower = term.lower()
        if "term 1" in term_lower or "bot" in term_lower:
            cutoff = math.ceil(len(candidates) * 0.33)
            candidates = candidates[:cutoff]
        elif "term 2" in term_lower:
            cutoff = math.ceil(len(candidates) * 0.66)
            candidates = candidates[:cutoff]

    if not candidates:
        candidates = [f"{subject} Topic {i+1}" for i in range(math.ceil(question_count / max_questions_per_topic))]

    # Expand candidate sub-aspects if total capacity (len * max) is less than question_count
    while question_count > len(candidates) * max_questions_per_topic:
        expanded = []
        for idx, t in enumerate(candidates):
            expanded.append(f"{t} (Aspect A)")
            expanded.append(f"{t} (Aspect B)")
        candidates = expanded

    # Assign topics ensuring no topic appears more than max_questions_per_topic times
    topic_counts = {}
    candidate_idx = 0

    for i in range(1, question_count + 1):
        assigned = False
        for _ in range(len(candidates)):
            curr_topic = candidates[candidate_idx % len(candidates)]
            if topic_counts.get(curr_topic, 0) < max_questions_per_topic:
                topic_counts[curr_topic] = topic_counts.get(curr_topic, 0) + 1
                blueprint[f"Q{i}"] = curr_topic
                candidate_idx += 1
                assigned = True
                break
            candidate_idx += 1
        
        if not assigned:
            # Unique fallback topic
            curr_topic = candidates[(i - 1) % len(candidates)]
            unique_topic = f"{curr_topic} (Var {i})"
            blueprint[f"Q{i}"] = unique_topic
            topic_counts[unique_topic] = 1

    return blueprint
