from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()
Session = sessionmaker()
