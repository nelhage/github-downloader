#!/usr/bin/env python
import sqlalchemy
import gzip
import json
import sys

import models as m

engine = sqlalchemy.create_engine('sqlite:///repos/repos.sqlite',
                                  poolclass=sqlalchemy.pool.SingletonThreadPool)
m.metadata.create_all(engine)
conn = engine.connect()

for path in sys.argv[1:]:
    print "reading %s..." % (path,)
    if path.endswith('.gz'):
        f = gzip.GzipFile(path, 'r')
    else:
        f = file(path)
    buf = []
    for line in f:
        repo = json.loads(line)
        if repo['owner'] is None:
            print "no owner id=%r" % (repo['id'],)
            continue
        try:
            buf.append(dict(
                id=int(repo['id']),
                owner=repo['owner']['login'],
                name=repo['name'],
                description=repo['description'],
                fork=repo['fork'],
            ))
        except TypeError as te:
            import traceback
            traceback.print_exc()
            print "line=%r repo=%r" % (line, repo)
            raise
        if len(buf) >= 100:
            insert = m.repos.insert().prefix_with('OR REPLACE')
            engine.connect().execute(insert, buf)
            del buf[:]
    f.close()
    insert = m.repos.insert().prefix_with('OR REPLACE')
    engine.connect().execute(insert, buf)
