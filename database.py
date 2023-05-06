from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

SQL_ALCHEMY_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQL_ALCHEMY_URL)
session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# Create a base class for declarative models.
# This is used by SQLAlchemy to generate the database schema.
# See https://docs.sqlalchemy.org/en/14/orm/extensions/declarative/index.html
