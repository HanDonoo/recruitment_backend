def normalize_tags(tags: str | None):
    if not tags:
        return set()
    return set(t.strip().lower() for t in tags.split(",") if t.strip())

def calc_match_score(applicant_skill_tags: str | None, job_skill_tags: str | None, same_location: bool=False) -> int:
    a = normalize_tags(applicant_skill_tags)
    j = normalize_tags(job_skill_tags)
    if not j:
        return 0
    inter = len(a & j)
    score = (inter / len(j)) * 100
    if same_location:
        score += 5
    return min(100, round(score))
