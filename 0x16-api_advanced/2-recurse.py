#!/usr/bin/python3
"""Script gets titles of the hot posts for a give subreddit"""
import requests

URL = 'https://www.reddit.com/r/{}/hot.json'
USER_AGENT = 'Safari 12.1'


def recurse(subreddit, titles=[], **kwargs):
    """Gets reddit for all hot posts of a subreddit"""
    params = {
            'after': kwargs.setdefault('after'),
            'count': kwargs.setdefault('count', 0),
            'limit': kwargs.setdefault('limit', 100)
            }
    resp = requests.get(
            URL.format(subreddit),
            headers={'User-Agent': USER_AGENT},
            params=params,
            allowed_redirects=False,
            timeout=30,
            )
    if resp.status_code == 200:
        results = r.json()['data']
        titles.extend(post['data']['title'] for post in results['children'])
        if results['after'] is not None:
            kwargs['after'] = results['after']
            kwargs['count'] += kwargs['limit']
            return recurse(subreddit, titles, **kwargs)
        return titles
    return None
