import sqlalchemy
from sqlalchemy import *

metadata = sqlalchemy.MetaData()

repos = Table('repositories', metadata,
              Column('id', Integer, primary_key=True),
              Column('owner', String),
              Column('description', String),
              Column('name', String),
              Column('fork', Boolean))
