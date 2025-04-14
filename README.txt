в проекте использованы : FastAPI, uvicorn, alembic, sqlmodel, pytest
запуск всех сервисов:
docker-compose up
применить миграции
docker-compose up alembic
всего поднимается три сервиса: сервис с базой данных, само приложение и сервис с миграциями 
бизнес-логика реализована согласно тз (при попытке бронировать столик учитывается его id, дата и длительность прошлой брони)
ps. файл пытался реализовать чтение базы данных через переменную DATABASE_URL, но docker-compose
отказывается :(
версия docker-compose, которая должна была быть
services:
  app:
    build:
      context: ./routes
    ports:
      - "8888:8080"
    depends_on:
      - db
    env_file:
      - var.env
    environment:
      - DATABASE_URL=${DATABASE_URL}

  db:
    image: postgres:15
    ports:
      - "5444:5432"

  alembic:
    build:
      context: .
      dockerfile: alembic.Dockerfile
    depends_on:
      - db
    env_file:
      - var.env
    environment:
      - DATABASE_URL=${DATABASE_URL}
