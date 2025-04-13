from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from db.models import Tables, Reservations, get_session, ReservationCreate
from datetime import timedelta

router = APIRouter()

# добавить бронь 


@router.post("/reservations/", response_model=Reservations)
def create_reservation(reservation_data: ReservationCreate, session: Session = Depends(get_session)):
    table = session.get(Tables, reservation_data.tables_id)
    if not table:
        raise HTTPException(status_code=404, detail="Стол не найден")

    new_start = reservation_data.reservation_time
    new_end = new_start + timedelta(minutes=reservation_data.duration_minutes)

    # Проверка на перекрытие с другими бронями
    overlapping_reservation = session.exec(
        select(Reservations).where(
            Reservations.tables_id == reservation_data.tables_id,
            Reservations.reservation_time < new_end,  # старт существующей < конец новой
            (Reservations.reservation_time + timedelta(minutes=Reservations.duration_minutes)) > new_start  # конец существующей > старт новой
        )
    ).first()

    if overlapping_reservation:
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