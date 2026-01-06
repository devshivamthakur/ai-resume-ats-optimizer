def normalize(k: str) -> str:
    return k.strip().lower()


def enforce_jd_only_keywords(ats):
    jd = {normalize(k) for k in ats.jd_keywords if len(k.strip()) >= 3}
    present = {normalize(k) for k in ats.present_keywords}
    
    # Present must come from JD
    present = present.intersection(jd)

    # Missing = JD - Present
    missing = jd - present

    # Recompute score safely
    score = int((len(present) / len(jd)) * 100) if jd else 0

    return {
        "jd_keywords": sorted(jd),
        "present_keywords": sorted(present),
        "missing_keywords": sorted(missing),
        "match_score": score,
    }
