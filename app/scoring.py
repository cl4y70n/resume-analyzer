def simple_skill_match_score(candidate, vacancy_profile):
    cand_skills = set([s.lower() for s in candidate.get('skills', [])])
    vac = set([s.lower() for s in vacancy_profile.get('skills', [])])
    if not vac:
        return 0.0, {}
    matched = cand_skills & vac
    score = len(matched) / max(len(vac), 1)
    breakdown = {
        'required_skills_total': len(vac),
        'matched': list(matched),
        'matched_count': len(matched)
    }
    return float(score), breakdown

def score_candidate(candidate, vacancy_profile):
    skill_score, breakdown = simple_skill_match_score(candidate, vacancy_profile)
    final = skill_score
    return final, breakdown
