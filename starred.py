import requests
import os
import json
import datetime
import time
import sqlalchemy
import models as m

key = os.environ.get('GITHUB_OAUTH_TOKEN', None)
auth_headers = {}
if key:
    auth_headers['Authorization'] = "token %s" % (key,)
u = 'https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc&per_page=100'

s = requests.Session()

engine = sqlalchemy.create_engine('sqlite:///repos/repos.sqlite',
                                  poolclass=sqlalchemy.pool.SingletonThreadPool)
m.metadata.create_all(engine)
conn = engine.connect()

while True:
    print("GET %s" % (u,))
    r = s.get(u, headers=auth_headers)
    if r.status_code != 200:
        if r.status_code == 403:
            delay = int(r.headers['x-ratelimit-reset']) - time.time()
            if delay > 0:
                print("ratelimited, sleeping %fs until %s..." % (delay, datetime.datetime.utcfromtimestamp(int(r.headers['x-ratelimit-reset']))))
                time.sleep(delay + 1)
        elif r.status_code >= 500:
            print("server error: %s" % (r.content,))
            time.sleep(10)
        else:
            print("unknown error: %s" % (repr(r),))
            print(r.text)
        continue
    buf = []
    for repo in r.json()['items']:
        row = dict(
            id=int(repo['id']),
            owner=repo['owner']['login'],
            name=repo['name'],
            description=repo['description'],
            fork=repo['fork'],
            language=repo['language'],
            size=repo['size'],
            stars=repo['stargazers_count'],
            forks=repo['forks_count'],
            watchers=repo['watchers_count'],
        )
        buf.append(row)
    insert = m.starred.insert().prefix_with('OR REPLACE')
    conn.execute(insert, buf)
    if 'next' not in r.links:
        break
    u = r.links['next']['url']
