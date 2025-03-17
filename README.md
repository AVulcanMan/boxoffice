# boxoffice
# Box Office Sentiment Analysis

This project uses Python to scrape and analyze movie discussions from the **r/boxoffice** subreddit. It identifies trending movies and performs sentiment analysis on the comments to understand public sentiment towards various films.

## Technologies & APIs Used

- **Reddit API (via `praw`)**: 
  - Used to interact with Reddit and fetch comments from the **r/boxoffice** subreddit.
  - Allows the script to gather recent posts and comments to identify movie mentions.

- **Transformers Library (`transformers` by Hugging Face)**: 
  - Used for sentiment analysis.
  - Specifically leverages a pre-trained BERT model (`nlptown/bert-base-multilingual-uncased-sentiment`) to classify comments as positive, negative, or neutral based on user feedback.

- **Regular Expressions (`re`)**:
  - Utilized to search for movie titles within the comments.
  - Ensures that full movie names (not just individual words) are detected.

- **Collections Library (`Counter`)**:
  - Used to count the frequency of movie mentions across the collected comments.

## Functionality

- **Trending Movie Detection**: Analyzes the most mentioned movies from comments on **r/boxoffice**.
- **Sentiment Analysis**: Applies the sentiment model to assess whether comments are positive or negative regarding a particular movie.
- **Output**: Displays the top trending movies along with sentiment percentages.

Example Output:
🎬 Top Trending Movies with Sentiment Analysis:
Avengers Endgame | Mentions: 30 | Sentiment: Positive: 70% | Negative: 30% 
Spider-Man No Way Home | Mentions: 25 | Sentiment: Positive: 80% | Negative: 20% 
Joker | Mentions: 20 | Sentiment: Positive: 50% | Negative: 50%
