from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel
DATABASE_URL = 'sqlite:///db_users.sqlite'

engine = create_engine(url=DATABASE_URL,echo = True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
