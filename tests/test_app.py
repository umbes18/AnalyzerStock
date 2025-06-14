import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import app
from unittest.mock import patch
import numpy as np


def test_get_index():
    client = app.app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b"Analyzer Stock" in resp.data


@patch('app.reddit_sentiment')
@patch('app.fair_value_estimate')
def test_post_index(mock_fair, mock_sentiment):
    mock_fair.return_value = {
        'current_price': 10.0,
        'avg_price': 9.0,
        'pe_ratio': 5,
        'pb_ratio': 1,
        'fair_value': 9.5,
    }
    mock_sentiment.return_value = {
        'count': 5,
        'sentiment': 0.1,
        'engagement': 12,
        'score': 0.5,
    }
    client = app.app.test_client()
    resp = client.post('/', data={'ticker': 'AAPL'})
    assert resp.status_code == 200
    assert b"Fair value stimato" in resp.data
    mock_fair.assert_called_once_with('AAPL')


@patch.object(app.analyzer, 'polarity_scores')
@patch.object(app, 'reddit')
def test_reddit_sentiment_algorithm(mock_reddit, mock_polarity):
    post = type('Post', (), {'title': 'x', 'score': 10, 'num_comments': 2})
    post2 = type('Post', (), {'title': 'y', 'score': 5, 'num_comments': 1})
    mock_reddit.subreddit.return_value.search.return_value = [post, post2]
    mock_polarity.side_effect = [{'compound': 0.5}, {'compound': -0.3}] * 3

    result = app.reddit_sentiment('AAPL')
    assert result['count'] == 6
    assert round(result['sentiment'], 2) == 0.10
    assert result['engagement'] == 54
    expected_score = 0.1 * np.log1p(54)
    assert abs(result['score'] - expected_score) < 1e-6


