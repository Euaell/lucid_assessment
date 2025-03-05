.PHONY: build up down logs shell db-shell help

help:
	@echo Makefile for FastAPI project
	@echo Usage:
	@echo   make build (build docker image)
	@echo   make up (start docker container)
	@echo   make down (stop docker container)
	@echo   make logs (show logs)
	@echo   make shell (connect to app container)
	@echo   make db-shell (connect to db container)
	@echo   make migrate (run migrations)

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec app bash

db-shell:
	docker-compose exec db mysql -uuser -ppassword fastapi_db

migrate:
	docker-compose exec app alembic upgrade head