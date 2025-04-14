FROM python:3.11

WORKDIR /alembic

COPY alembic.ini .
COPY alembic alembic
COPY app app
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["alembic", "upgrade", "head"]