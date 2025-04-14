from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from db.models import Tables, Reservations, ReservationCreate
import datetime
import pytz
from db.session import get_session
utc = pytz.utc
router = APIRouter()

# добавить бронь 


@router.post("/reservations/", response_model=Reservations)
def create_reservation(reservation_data: ReservationCreate, session: Session = Depends(get_session)):
    table = session.get(Tables, reservation_data.tables_id)
    if not table:
        raise HTTPException(status_code=404, detail="Стол не найден")

    new_start = reservation_data.reservation_time
    new_end = new_start + datetime.timedelta(minutes=reservation_data.duration_minutes)

    overlapping = session.exec(
        select(Reservations).where(
            Reservations.tables_id == reservation_data.tables_id,
            Reservations.reservation_time < new_end,
        )
    ).all()

    for res in overlapping:
        existing_start = utc.localize(res.reservation_time)
        existing_end = existing_start + datetime.timedelta(minutes=res.duration_minutes)
        if existing_end > new_start:
            raise HTTPException(status_code=400, detail="На это время столик уже забронирован")

    new_reservation = Reservations(**reservation_data.dict())
    session.add(new_reservation)
    session.commit()
    session.refresh(new_reservation)
    return new_reservation
    

# список всех броней

@router.get("/reservations/")
def read_reservations(session: Session = Depends(get_session)):
    reservations = session.exec(select(Reservations)).all()
    return reservations

# удалить бронь 

@router.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservations, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    session.delete(reservation)
    session.commit()
    return {"ok": True}