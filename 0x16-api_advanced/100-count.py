#!/usr/bin/python3
"""Script parses the title of all hot articles, and prints a sorted count of given keywords"""
import requests
import re

URL = 'https://www.reddit.com/r/{}/hot.json'
USER_AGENT = 'Safari 12.1'


def count_words(subreddit, wordlist, nums=None, after=None):
    """Gets reddit for hot posts and print total occurances of each keyword"""
    resp = requests.get(
            URL.format(subreddit),
            headers={'User-Agent': USER_AGENT},
            params={'after': after, 'limit': 100},
            allow_redirects=False,
            )
    if resp.status_code == 200:
        nums = nums or dict.fromkeys(wordlist, 0)
        data = resp.json()['data']
        page = [word for post in data['children']
                for word in post['data']['title'].split()]
        for key in wordlist:
            for word in page:
                if key.casefold() == word.casefold():
                    nums[key] += 1
        if data['after'] is None:
            keys = sorted(filter(nums.get, nums), key=lambda k: (-nums[k], k))
            for key in keys:
                print('{}: {}'.format(key, nums[key]))
        else:
            count_words(subreddit, wordlist, nums, data['after'])
