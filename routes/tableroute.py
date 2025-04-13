from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from db.models import Tables, get_session

router = APIRouter()

# Создать столик

@router.post("/tables/")
def create_table(table: Tables, session: Session = Depends(get_session)):
    session.add(table)
    session.commit()
    session.refresh(table)
    return table


# Удалить столик

@router.delete("/tables/{tables_id}")
def delete_table(tables_id: int, session: Session = Depends(get_session)):
    table = session.get(Tables, tables_id)
    if not table:
        raise HTTPException(status_code=404, detail="Столик не найден")
    session.delete(table)
    session.commit()
    return {"ok": True}

# Просмотр всех столиков

@router.get("/tables/")
def read_tables(session: Session = Depends(get_session)):
    table = session.exec(select(Tables)).all()
    return table