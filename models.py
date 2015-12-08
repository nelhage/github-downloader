import sqlalchemy
from sqlalchemy import *

metadata = sqlalchemy.MetaData()

repos = Table('repositories', metadata,
              Column('id', Integer, primary_key=True),
              Column('owner', String),
              Column('description', String),
              Column('name', String),
              Column('fork', Boolean))

starred = Table('starred', metadata,
                Column('id', Integer, primary_key=True),
                Column('owner', String),
                Column('description', String),
                Column('name', String),
                Column('fork', Boolean),
                Column('language', String),
                Column('size', Integer),
                Column('stars', Integer),
                Column('forks', Integer),
                Column('watchers', Integer))
