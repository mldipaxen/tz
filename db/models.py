from sqlmodel import  SQLModel, create_engine, Session, Field
from datetime import datetime
from pydantic import BaseModel



class Tables (SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    seats: int = Field(default=None)
    location: str = Field(default=None)

class Reservations (SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    customer_name: str = Field(default=None, max_length=20)
    tables_id: int = Field(default=None, foreign_key='tables.id')
    reservation_time: datetime = Field(default=None)
    duration_minutes: int = Field(default=None)

class ReservationCreate(BaseModel):
    customer_name: str
    tables_id: int
    reservation_time: datetime
    duration_minutes: int





# with Session(engine) as session:
#     table1 = Table(id = 1, name = 'Table 1', seats = 4, location='Стол у окна')
#     table2 = Table(id = 2, name = 'Table 2', seats = 3, location='Стол в центре зала')
#     table3 = Table(id = 3, name = 'Table 3', seats = 2, location='Стол у входа')
#     table4 = Table(id = 4, name = 'Table 4', seats = 1, location='Стол на веранде')
#     session.add_all([table1, table2, table3, table4])
#     session.commit()
