from textblob import TextBlob

SCAM_KEYWORDS = [
    "lottery", "prize", "winner", "urgent",
    "bank account", "credit card", "click here",
    "limited offer", "act now", "free money",
    "investment", "bitcoin", "crypto",
    "password", "verify account"
]

def analyze_content(text):

    text_lower = text.lower()

    keyword_hits = sum(1 for word in SCAM_KEYWORDS if word in text_lower)

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    risk_score = min(100, keyword_hits * 15)

    if polarity > 0.7 or polarity < -0.7:
        risk_score += 10

    risk_score = min(100, risk_score)

    if risk_score > 70:
        level = "High Risk ⚠️"
    elif risk_score > 40:
        level = "Medium Risk"
    else:
        level = "Low Risk ✔️"

    explanation = f"""
Keyword matches detected: {keyword_hits}.
Sentiment polarity: {round(polarity, 2)}.
Risk level classified as: {level}.
"""

    return {
        "risk_score": risk_score,
        "explanation": explanation.strip()
    }
