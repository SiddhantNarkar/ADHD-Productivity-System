import numpy as np

def build_features(session):

    # -------------------------
    # AGE
    # -------------------------
    age = session.age_at_assessment
    age_group = 0 if age <= 16 else 1

    # -------------------------
    # MCQ DOMAIN CALCULATION
    # -------------------------
    responses = session.mcqresponse_set.select_related("question")

    inattention = []
    hyperactivity = []
    impulsivity = []

    for r in responses:
        score_map = {"A": 0, "B": 1, "C": 2, "D": 3}
        score = score_map.get(r.selected_option, 0)

        domain = r.question.domain

        if domain == "Inattention":
            inattention.append(score)
        elif domain == "Hyperactivity":
            hyperactivity.append(score)
        elif domain == "Impulsivity":
            impulsivity.append(score)

    def percent(domain_scores, max_items):
        if not domain_scores:
            return 0
        return (sum(domain_scores) / (max_items * 3)) * 100

    inattention_pct = percent(inattention, len(inattention))
    hyperactivity_pct = percent(hyperactivity, len(hyperactivity))
    impulsivity_pct = percent(impulsivity, len(impulsivity))

    impairment_flag = 0  # If you implement impairment questions, compute here

    # -------------------------
    # GAME 1
    # -------------------------
    g1 = session.game1result

    attention_accuracy = (
        (g1.correct_presses / g1.total_targets) * 100
        if g1.total_targets > 0 else 0
    )

    false_press_rate = (
        (g1.false_presses / g1.total_stimuli) * 100
        if g1.total_stimuli > 0 else 0
    )

    reaction_time = g1.average_reaction_time_ms or 0

    reaction_time_variability = 0  # If you store per-trial RT, compute std here

    # -------------------------
    # GAME 2
    # -------------------------
    levels = session.game2_levels.all()

    level_scores = {1: 0, 2: 0, 3: 0}

    for level in levels:
        level_scores[level.level] = level.score

    level1_score = level_scores[1]
    level2_score = level_scores[2]
    level3_score = level_scores[3]

    memory_drop = level1_score - level3_score
    avg_completion_time = np.mean(
        [lvl.completion_time_seconds for lvl in levels]
    ) if levels else 0

    # -------------------------
    # FINAL FEATURE VECTOR
    # -------------------------

    return [[
        age,
        age_group,
        inattention_pct,
        hyperactivity_pct,
        impulsivity_pct,
        impairment_flag,
        attention_accuracy,
        false_press_rate,
        reaction_time,
        reaction_time_variability,
        level1_score,
        level2_score,
        level3_score,
        memory_drop,
        avg_completion_time
    ]]