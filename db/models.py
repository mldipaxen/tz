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






