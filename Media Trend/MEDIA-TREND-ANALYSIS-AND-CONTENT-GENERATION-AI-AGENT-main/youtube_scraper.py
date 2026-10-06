from googleapiclient.discovery import build
from datetime import datetime, timedelta

def fetch_youtube_trends(keyword, max_results=50):
    # Base developer key - Replace with your valid API key
    YOUTUBE_API_KEY = 'AIzaSyBgF7dWqqnHZeSEkJ1Mq6y4T2dZRJL65Qk'
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    request = youtube.search().list(
        q=keyword,
        part='snippet',
        maxResults=max_results,
        order='viewCount',
        publishedAfter=week_ago,
        type='video'
    )
    response = request.execute()
    
    results = []
    for item in response.get('items', []):
        results.append({
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'platform': 'YouTube'
        })
    return results