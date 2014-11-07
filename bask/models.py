from sqlalchemy import Column, Integer, String

from db import BaseModel

class CommandModel(BaseModel):
    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    url = Column(String)

