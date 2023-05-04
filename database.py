from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
#from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

SQL_ALCHEMY_URL = os.getenv("DATABASE_URL")


engine = create_engine(SQL_ALCHEMY_URL)
session_local = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()


# declarative_base() has been mooved to  sqlalchemy.orm.declarative_base()