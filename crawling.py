import praw
import re
import logging
from collections import Counter
from transformers import pipeline

logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)
# Initialize Reddit API client
def initialize_reddit():
    return praw.Reddit(
        client_id="5NDwPo9pB8YunVljUq-qbQ",  # Your client ID
        client_secret="E7dkXk5wlMlZ4C1a4YErGgOiyvVnVg",  # Your client secret
        user_agent="myBoxOfficeBot/1.0 by MasterofImbalances"  # Your user agent
    )

# Fetch comments from r/boxoffice using Reddit API
def get_comments(subreddit="boxoffice", comment_limit=2000):
    reddit = initialize_reddit()
    comments = []
    
    # Scrape the latest posts in the subreddit and get comments
    for submission in reddit.subreddit(subreddit).hot(limit=1000):  
        submission.comments.replace_more(limit=0)  # Get all comments
        for comment in submission.comments.list():
            comments.append(comment.body)
            if len(comments) >= comment_limit:
                break
        if len(comments) >= comment_limit:
            break
    
    return comments if comments else ["No comments found."]

movies = set()
with open("movies.txt", encoding="utf-8") as file:
    for line in file:
        movies.add(line.strip().lower()) 

def extract_movie_trends(comments):
    all_titles = []
    for comment in comments:
        comment_lower = comment.lower()
        for movie in movies:
            # Match full movie titles as a phrase (not just individual words)
            if re.search(rf'\b{re.escape(movie)}\b', comment_lower):  
                all_titles.append(movie)
    
    top_movies = Counter(all_titles).most_common(10)  # Get top 10 mentioned movies
    return top_movies

def get_movie_sentiment(movie, comments):
    sentiment_model = pipeline("sentiment-analysis", framework="pt", model="nlptown/bert-base-multilingual-uncased-sentiment")  # Specify PyTorch as framework
    
    movie_comments = [comment for comment in comments if movie.lower() in comment.lower()]
    
    if not movie_comments:
        return "No comments mentioning this movie"
    
    positive, negative = 0, 0
    for comment in movie_comments:
        sentiment = sentiment_model(comment[:512])[0]  # Use the first 512 characters of the comment
        if sentiment["label"] == "5 stars" or sentiment["label"] == "4 stars" or sentiment["label"] == "3 stars":
            positive += 1
        else:
            negative += 1
    
    total = positive + negative
    sentiment_percentage = {
        "positive": round(100 * positive / total, 2),
        "negative": round(100 * negative / total, 2),
    }
    
    return sentiment_percentage



if __name__ == "__main__":
    comments = get_comments()
    
    movie_trends = extract_movie_trends(comments)
    
    print("\n🎬 Top Trending Movies with Sentiment Analysis:")
    print("="*50)
    for movie, count in movie_trends:
        sentiment = get_movie_sentiment(movie, comments)
        if isinstance(sentiment, dict):
            sentiment_str = f"Positive: {sentiment['positive']}% | Negative: {sentiment['negative']}%"
        else:
            sentiment_str = sentiment
        print(f"{movie:<25} | Mentions: {count:<3} | Sentiment: {sentiment_str}")
    print("="*50)
    