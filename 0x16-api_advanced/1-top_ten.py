#!/usr/bin/python3
"""Script prints the first 10 hot posts listed for a given subreddit"""
import requests

URL = 'https//www.reddit.com/r/{}/hot.json'
USER_AGENT = 'Safari 12.1'


def top_ten(subreddit):
    """Gets and prints the titles of the first 10 hot posts"""
    resp = requests.get(
            URL.format(subreddit),
            headers={'User-Agent': USER_AGENT},
            params={'limit': 10},
            allow_redirects=False,
            timeout=10
            )
    if resp.status_code == 200:
        for post in resp.json()['data']['children']:
            print(post['data']['title'])
    else:
        print('None')
