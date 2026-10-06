import time
from duckduckgo_search import DDGS

def fetch_twitter_trends(keyword, max_results=20):
    """
    Fetches recent tweets using keyword via DuckDuckGo Search.
    Bypasses the restrictive Twitter API 402 Error.
    """
    print(f"Fetching Twitter discussions using DuckDuckGo (Free alternative)...")
    results = []
    
    try:
        ddgs = DDGS()
        # Searching text on site:twitter.com
        ddg_results = ddgs.text(f"site:twitter.com {keyword}", max_results=max_results)
        
        for r in ddg_results:
            results.append({
                'title': r.get('body', ''),
                'likes': 0, # Cannot scrape likes efficiently via DDG
                'retweets': 0,
                'platform': 'Twitter (via DDG)'
            })
            
    except Exception as e:
        print(f"DuckDuckGo Search Error: {e}")
        
    return results