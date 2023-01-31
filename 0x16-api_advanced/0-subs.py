#!/user/bin/python3
"""Script returns the number of subscribers"""
import requests

URL = 'https://www.reddit.com/r/{}/about.json'
USER_AGENT = 'Safari 12.1'


def number_of_subscribers(subreddit):
    """Get number of subreddit subscribers"""
    resp = requests.get(
            URL.format(subreddit),
            headers={'User-Agent': USER_AGENT},
            allow_redirects=False,
            timeout=10
            )
    if resp.status_code == 200:
        return resp.json()['data']['subscribers']
    else:
        return 0
