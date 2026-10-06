from sklearn.feature_extraction.text import TfidfVectorizer
from scrapers.rl_scraper import rl_supervised_scrape

def analyze_trends(keyword, platforms=None):
    """
    Uses the RL Scraper Agent (MDP based) to self-supervise the content scraping
    and identifies trending topics from the gathered results.
    """
    # The platforms argument is kept for compatibility, but the RL agent 
    # will autonomously choose the best platforms and query variations.
    all_content = rl_supervised_scrape(keyword, steps=3)
    
    if not all_content:
        return ["No trends found"]

    # Simple TF-IDF to find common themes in titles/text
    texts = [item['title'] for item in all_content]
    # token_pattern forces the math algorithm to only accept actual alphabetical words, banning numbers like '39' or '2026'
    vectorizer = TfidfVectorizer(max_features=10, stop_words='english', token_pattern=r'(?u)\b[A-Za-z]+\b')
    
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
        top_keywords = vectorizer.get_feature_names_out()
        return list(top_keywords[:5])
    except:
        # Fallback if text is too sparse
        return [texts[0]] if texts else ["General " + keyword]