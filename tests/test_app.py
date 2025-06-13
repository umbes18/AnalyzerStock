import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import app
from unittest.mock import patch


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
    mock_sentiment.return_value = {'count': 5, 'sentiment': 0.1}
    client = app.app.test_client()
    resp = client.post('/', data={'ticker': 'AAPL'})
    assert resp.status_code == 200
    assert b"Fair value stimato" in resp.data
    mock_fair.assert_called_once_with('AAPL')
