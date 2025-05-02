"""
created an erd, awkward in mac to setup and diagram not great,
used intellij datagrip as it was cleaner leaving this for right now
"""
import sys
import os
from sqlalchemy import create_engine
from eralchemy2 import render_er

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from oso_demo.models import Base

# This engine is for local dev/ERD only. Swap to Postgres in your app config.
engine = create_engine("sqlite:///tmp.db", echo=True)
base = Base()

base.metadata.create_all(engine)
render_er("sqlite:///tmp.db", 'erd_from_sqlite.png')