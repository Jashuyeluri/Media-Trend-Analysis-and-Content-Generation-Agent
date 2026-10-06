from agents.trend_agent import analyze_trends
from agents.content_crew import generate_content
from agents.landing_crew import generate_landing_page
from database.db import init_db, log_run

def run_pipeline(niche, platforms):
    init_db()
    
    print(f"--- Starting Analysis for: {niche} ---")
    trends = analyze_trends(niche, platforms)
    top_trend = trends[0]
    
    print(f"Top Trend Identified: {top_trend}")
    
    # Combine user's explicit niche with the mathematical trend to keep AI strictly on topic
    combined_topic = f"{niche} (specifically focusing on: {top_trend})"
    
    print("--- Generating Social Content ---")
    social_content = generate_content(combined_topic)
    
    print("--- Generating Landing Page ---")
    landing_copy = generate_landing_page(combined_topic)
    
    import re
    social_content_str = str(social_content)
    
    # Extract the full 4+ word phrase from the AI's output
    match = re.search(r'Trending Topic Found:\s*([^\n]+)', social_content_str, re.IGNORECASE)
    
    if match:
        display_trend = match.group(1).strip()
        # Enforce minimum 4 words and inclusion of the niche
        if len(display_trend.split()) < 4 or niche.lower() not in display_trend.lower():
            display_trend = f"The Impact of {top_trend.title()} on {niche.title()}"
    else:
        display_trend = f"The Impact of {top_trend.title()} on {niche.title()}"
    
    log_run(niche, top_trend)
    
    # Strip internal backend metadata from the final frontend outputs
    cleaned_social = re.sub(r'(?i)^(Trending Topic Found:|Source:|Relevance:|Fact Check Status:|Trend Analysis Report|─────────────────────────────).*$\n?', '', social_content_str, flags=re.MULTILINE)
    cleaned_social = re.sub(r'\(specifically focusing on:.*?\)', '', cleaned_social, flags=re.IGNORECASE)
    cleaned_social = cleaned_social.strip()
    
    landing_copy_str = str(landing_copy)
    cleaned_landing = re.sub(r'(?i)^(Trending Topic Found:|Source:|Relevance:|Fact Check Status:|Trend Analysis Report|─────────────────────────────).*$\n?', '', landing_copy_str, flags=re.MULTILINE)
    cleaned_landing = re.sub(r'\(specifically focusing on:.*?\)', '', cleaned_landing, flags=re.IGNORECASE)
    cleaned_landing = cleaned_landing.strip()
    
    return {
        "trend": display_trend,
        "social": cleaned_social,
        "landing": cleaned_landing
    }

if __name__ == "__main__":
    # Test run
    results = run_pipeline("AI SaaS tools", ["youtube", "twitter"])
    print(results)