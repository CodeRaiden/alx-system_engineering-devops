#!/usr/bin/python3
"""
Script summarize the TODO lists of employees and writes it to a file as JSON
"""
from json import dump
from requests import get

USERS = 'https://jsonplaceholder.typicode.com/users'
TODOS = 'https://jsonplaceholder.typicode.com/todos'

if __name__ == '__main__':
    with open('todo_all_employees.json', 'w') as ostream:
        dump({
            str(user['id']): [{
                "username": user['username'],
                "task": task['title'],
                "completed": task['completed'],
            } for task in get(TODOS, params={'userId': user['id']}).json()]
            for user in get(USERS).json()
        }, ostream)
