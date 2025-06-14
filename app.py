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

# get social sentiment from Reddit

def reddit_sentiment(ticker):
    if not reddit:
        return {'count': 0, 'sentiment': 0}
    query = ticker.upper()
    posts = reddit.subreddit('stocks').search(query, limit=25)
    scores = []
    for post in posts:
        vs = analyzer.polarity_scores(post.title)
        scores.append(vs['compound'])
    if not scores:
        return {'count': 0, 'sentiment': 0}
    return {'count': len(scores), 'sentiment': np.mean(scores)}


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
    hist_recent = hist['Close'].tail(365)
    dates = hist_recent.index.strftime('%Y-%m-%d').tolist()
    prices = [round(p, 2) for p in hist_recent.values]
    return {
        'current_price': current_price,
        'avg_price': avg_price,
        'pe_ratio': pe_ratio,
        'pb_ratio': pb_ratio,
        'fair_value': fair_value,
        'dates': dates,
        'prices': prices,
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
