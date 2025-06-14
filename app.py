from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import numpy as np
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

app = Flask(__name__)

# configure Reddit API (free)
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'stock analyzer app')

if REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET:
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                         client_secret=REDDIT_CLIENT_SECRET,
                         user_agent=REDDIT_USER_AGENT)
else:
    reddit = None

analyzer = SentimentIntensityAnalyzer()

# get social sentiment and engagement from Reddit across multiple subreddits

def reddit_sentiment(ticker):
    """Return sentiment, engagement and a social score for a ticker."""
    if not reddit:
        return {'count': 0, 'sentiment': 0, 'engagement': 0, 'score': 0}

    query = ticker.upper()
    subreddits = ['stocks', 'wallstreetbets', 'investing']
    posts_data = []
    for sub in subreddits:
        for post in reddit.subreddit(sub).search(query, limit=15):
            vs = analyzer.polarity_scores(post.title)
            posts_data.append({
                'compound': vs['compound'],
                'upvotes': getattr(post, 'score', 0),
                'comments': getattr(post, 'num_comments', 0),
            })

    if not posts_data:
        return {'count': 0, 'sentiment': 0, 'engagement': 0, 'score': 0}

    sentiment = np.mean([p['compound'] for p in posts_data])
    engagement = sum(p['upvotes'] + p['comments'] for p in posts_data)
    social_score = float(sentiment) * np.log1p(engagement)

    return {
        'count': len(posts_data),
        'sentiment': sentiment,
        'engagement': engagement,
        'score': social_score,
    }


def fair_value_estimate(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period='5y')
    if hist.empty:
        return None
    avg_price = hist['Close'].mean()
    current_price = hist['Close'].iloc[-1]
    pe_ratio = data.info.get('trailingPE') or 0
    pb_ratio = data.info.get('priceToBook') or 0
    # simple fair value formula
    fair_value = (avg_price * 0.6) + (current_price * 0.3) + ((pe_ratio + pb_ratio) * 0.1)
    return {
        'current_price': current_price,
        'avg_price': avg_price,
        'pe_ratio': pe_ratio,
        'pb_ratio': pb_ratio,
        'fair_value': fair_value,
    }


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    sentiment = None
    ticker = ''
    if request.method == 'POST':
        ticker = request.form.get('ticker')
        if ticker:
            result = fair_value_estimate(ticker)
            sentiment = reddit_sentiment(ticker)
    return render_template('index.html', result=result, ticker=ticker.upper(), sentiment=sentiment)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
