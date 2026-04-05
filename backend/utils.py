import re
import numpy as np
from typing import List, Dict, Any

# Keyword Lists
JOB_KEYWORDS = ["developer", "engineer", "api", "python", "backend", "frontend", "fullstack", "data", "ml", "ai", "cloud", "devops", "security", "software"]
POLITE_WORDS = ["please", "would", "appreciate", "thank you", "if you have time", "best regards", "looking forward"]
SPAM_WORDS = ["urgent", "immediately", "best ever", "guaranteed", "click here", "limited offer", "winner", "cash"]
COMPANY_KEYWORDS = ["company", "role", "team", "growth", "culture", "position", "scaling", "mission"]
POSITIVE_SENTIMENT = ["great", "love", "impressive", "excellent", "amazing", "happy", "excited", "interest", "help"]
NEGATIVE_SENTIMENT = ["bad", "wrong", "issue", "problem", "difficult", "fail", "slow", "expensive", "hate"]

def extract_features(text: str) -> np.ndarray:
    """
    Extracts structured numerical features from email text.
    Returns a numpy array of 12 features for the v3.14 model.
    """
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)
    
    # Base Features
    avg_sentence_length = word_count / max(sentence_count, 1)
    
    if sentence_count > 1:
        sentence_lengths = [len(s.split()) for s in sentences]
        sentence_variance = np.var(sentence_lengths)
    else:
        sentence_variance = 0
        
    name_patterns = [r"hi\s+[a-z][a-z]+", r"dear\s+[a-z][a-z]+", r"hello\s+[a-z][a-z]+", r"hey\s+[a-z][a-z]+"]
    has_name = 1 if any(re.search(p, text_lower) for p in name_patterns) else 0
    has_company = 1 if any(kw in text_lower for kw in COMPANY_KEYWORDS) else 0
    keyword_matches = sum(1 for kw in JOB_KEYWORDS if kw in text_lower)
    polite_count = sum(1 for w in POLITE_WORDS if w in text_lower)
    spam_count = sum(1 for w in SPAM_WORDS if w in text_lower)
    
    # NEW v3.14 Features
    # 1. Readability Proxy (Flesch-like: shorter sentences + common words = better)
    # Simplifying: (Words/Sentences) + (Chars/Words)
    char_count = len(text.replace(" ", ""))
    avg_word_len = char_count / max(word_count, 1)
    readability = (avg_sentence_length + avg_word_len) 
    
    # 2. Sentiment Polarity
    pos_score = sum(1 for w in POSITIVE_SENTIMENT if w in text_lower)
    neg_score = sum(1 for w in NEGATIVE_SENTIMENT if w in text_lower)
    sentiment = pos_score - neg_score
    
    # 3. Personalization Depth (Composite)
    pers_depth = has_name + has_company + (1 if "you" in text_lower or "your" in text_lower else 0)

    return np.array([
        word_count,
        sentence_count,
        avg_sentence_length,
        sentence_variance,
        has_name,
        has_company,
        keyword_matches,
        polite_count,
        spam_count,
        readability,
        sentiment,
        pers_depth
    ])

def compute_breakdown(text: str) -> Dict[str, int]:
    """
    Computes explainable 0-100 scores for different categories.
    """
    text_lower = text.lower()
    words = text.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)
    
    # Personalization Score
    name_patterns = [r"hi\s+[a-z][a-z]+", r"dear\s+[a-z][a-z]+", r"hello\s+[a-z][a-z]+", r"hey\s+[a-z][a-z]+"]
    has_name = any(re.search(p, text_lower) for p in name_patterns)
    has_company = any(kw in text_lower for kw in COMPANY_KEYWORDS)
    pers_score = 0
    if has_name: pers_score += 50
    if has_company: pers_score += 30
    if "you" in text_lower or "your" in text_lower: pers_score += 20
    pers_score = min(pers_score, 100)
    
    # Length Score (Optimal 50-120 words)
    if 50 <= word_count <= 120:
        length_score = 100
    elif word_count < 50:
        length_score = max(0, word_count * 2)
    else:
        length_score = max(0, 100 - (word_count - 120) // 2)
        
    # Clarity Score
    avg_len = word_count / max(sentence_count, 1)
    if 10 <= avg_len <= 18:
        clarity_score = 100
    else:
        clarity_score = max(0, 100 - abs(avg_len - 14) * 6)
        
    # Relevance Score
    keyword_matches = sum(1 for kw in JOB_KEYWORDS if kw in text_lower)
    relevance_score = min(keyword_matches * 20, 100)
    
    # Tone Score (Improved with sentiment)
    polite_count = sum(1 for w in POLITE_WORDS if w in text_lower)
    spam_count = sum(1 for w in SPAM_WORDS if w in text_lower)
    pos_score = sum(1 for w in POSITIVE_SENTIMENT if w in text_lower)
    
    tone_score = 50 
    tone_score += polite_count * 15
    tone_score += pos_score * 5
    tone_score -= spam_count * 25
    tone_score = max(0, min(tone_score, 100))
    
    return {
        "personalization": int(pers_score),
        "clarity": int(clarity_score),
        "relevance": int(relevance_score),
        "tone": int(tone_score),
        "length": int(length_score)
    }

def get_recommendations(breakdown: Dict[str, int]) -> List[str]:
    suggestions = []
    if breakdown['personalization'] < 60:
        suggestions.append("Hyper-personalize. Reference a specific project or achievement.")
    if breakdown['length'] < 70:
        suggestions.append("Too brief? Add more value before the call to action.")
    elif breakdown['length'] < 90 and breakdown['length'] > 70:
        pass
    elif breakdown['length'] < 70:
        suggestions.append("Keep it concise. Decision makers have limited time.")
    
    if breakdown['relevance'] < 40:
        suggestions.append("Align your vocabulary with the recipient's industry (e.g., 'scaling', 'efficiency').")
    if breakdown['tone'] < 60:
        suggestions.append("Tone seems aggressive or spammy. Use softer transitions.")
    
    if not suggestions:
        suggestions.append("Premium quality detected. Recommended for immediate outreach.")
    return suggestions

def get_full_analysis(text: str, model_proba: float) -> Dict[str, Any]:
    breakdown = compute_breakdown(text)
    base_score = model_proba * 100
    
    # Versioning logic (v3.14)
    if breakdown['personalization'] < 30: base_score -= 20
    if breakdown['tone'] < 40: base_score -= 15
    if breakdown['relevance'] > 80: base_score += 10
    
    final_score = max(0, min(int(base_score), 100))
    
    if final_score < 45: label = "WEAK EMAIL"
    elif final_score < 75: label = "AVERAGE EMAIL"
    else: label = "STRONG EMAIL"
        
    return {
        "score": final_score,
        "label": label,
        "confidence": round(float(model_proba), 2),
        "breakdown": breakdown,
        "insights": [f"Linguistic Clarity: {breakdown['clarity']}%", f"Tone Intensity: {breakdown['tone']}/100"],
        "suggestions": get_recommendations(breakdown)
    }
