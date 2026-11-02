"""
Review summarizer — works with plain-string reviews from the uploaded dataset.
Infers sentiment from positive/negative keywords.
"""

POSITIVE_WORDS = {
    "perfect", "excellent", "amazing", "love", "best", "fantastic", "great",
    "outstanding", "superb", "brilliant", "incredible", "awesome", "wonderful",
    "good", "solid", "worth", "recommend", "smooth", "fast", "easy", "clean",
    "accurate", "impressive", "convenient", "beautiful", "crisp", "responsive",
    "durable", "reliable", "comfortable", "long", "bright", "sharp", "premium",
    "versatile", "professional", "intuitive", "quiet", "efficient", "powerful",
}

NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "poor", "horrible", "disappointing", "slow",
    "expensive", "heavy", "difficult", "confusing", "limited", "noisy",
    "issue", "problem", "bug", "inconsistent", "lacking", "worse", "waste",
    "grainy", "wobble", "wobbly", "cheap", "basic", "mediocre", "unstable",
    "overpriced", "fragile", "flimsy", "complicated", "delay", "lag",
}


def _score_review(text: str) -> str:
    words = set(text.lower().split())
    pos = len(words & POSITIVE_WORDS)
    neg = len(words & NEGATIVE_WORDS)
    if pos > neg:
        return "positive"
    elif neg > pos:
        return "negative"
    return "neutral"


def analyze_reviews(reviews):
    """
    Accept a list of plain strings (the uploaded dataset format).
    Returns dict with pros, cons, verdict, counts.
    """
    if not reviews:
        return {
            "pros": [], "cons": [], "verdict": "⚪ No reviews yet",
            "verdict_label": "neutral",
            "positive_count": 0, "negative_count": 0,
            "neutral_count": 0, "total": 0,
        }

    pros, cons, neutrals = [], [], []
    for r in reviews:
        text = r.strip() if isinstance(r, str) else r.get("text", "").strip()
        sentiment = _score_review(text)
        if sentiment == "positive":
            pros.append(text)
        elif sentiment == "negative":
            cons.append(text)
        else:
            neutrals.append(text)

    total = len(pros) + len(cons) + len(neutrals)
    pos_ratio = len(pros) / total if total else 0

    if pos_ratio >= 0.75:
        verdict, verdict_label = "🌟 Highly Recommended", "positive"
    elif pos_ratio >= 0.5:
        verdict, verdict_label = "👍 Generally Positive", "positive"
    elif pos_ratio >= 0.3:
        verdict, verdict_label = "🤔 Mixed Reviews", "neutral"
    else:
        verdict, verdict_label = "👎 Mostly Negative", "negative"

    # Fill cons from neutral if we have nothing negative
    display_cons = cons[:3] if cons else neutrals[:2]

    return {
        "pros": pros[:3],
        "cons": display_cons,
        "verdict": verdict,
        "verdict_label": verdict_label,
        "positive_count": len(pros),
        "negative_count": len(cons),
        "neutral_count": len(neutrals),
        "total": total,
    }


def get_overall_sentiment(reviews):
    if not reviews:
        return 50
    scored = [_score_review(r if isinstance(r, str) else r.get("text", "")) for r in reviews]
    pos = scored.count("positive")
    return int(pos / len(scored) * 100)
