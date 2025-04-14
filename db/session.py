from sqlmodel import  SQLModel, create_engine, Session
from db.models import Tables

engine = create_engine('sqlite:///tabres.db')

def get_session():
    with Session(engine) as session:
        yield session

