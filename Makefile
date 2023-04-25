COMPOSE = docker-compose
SERVICE = flask_app


build:
	$(COMPOSE) build

build-no-cache:
	$(COMPOSE) build --no-cache $(SERVICE)

up:
	$(COMPOSE) up

up-d:
	$(COMPOSE) up -d

prune:
	docker volume prune -f

bash:
	$(COMPOSE) exec -it $(SERVICE) bash

down:
	$(COMPOSE) down