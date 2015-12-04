import requests
import time
import datetime
import os
import sys
import json

CHUNK = 1000000
current_chunk = None
out = None

key = os.environ['GITHUB_OAUTH_TOKEN']
u = 'https://api.github.com/repositories'

if len(sys.argv) > 1:
    u += "?since=" + sys.argv[1]

s = requests.Session()

def write_repo(repo):
    global current_chunk, out
    id = repo['id']
    base = id - id%CHUNK
    if base != current_chunk:
        if out is not None:
            out.close()
        out = open('repos/repos.' + str(base/CHUNK) + '.json', 'a')
    out.write(json.dumps(repo))

while True:
    print "GET %s" % (u,)
    r = s.get(u, headers={'Authorization': "token %s" % (key,)})
    if r.status_code != 200:
        if r.status_code == 403:
            delay = int(r.headers['x-ratelimit-reset']) - time.time()
            if delay > 0:
                print "ratelimited, sleeping %fs until %s..." % (delay, datetime.datetime.utcfromtimestamp(int(r.headers['x-ratelimit-reset'])))
                time.sleep(delay + 1)
        elif r.status_code >= 500:
            print "server error: %s" % (r.content,)
            time.sleep(10)
        else:
            print "unknown error: %s" % (repr(r),)
        continue

    for repo in r.json():
        write_repo(repo)
    out.flush()
    if 'next' not in r.links:
        break
    u = r.links['next']['url']
