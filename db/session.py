from sqlmodel import  SQLModel, create_engine, Session, Field

engine = create_engine('sqlite:///tabres.db')

def get_session():
    with Session(engine) as session:
        yield session
