DEV_ENV_NAME = ailp-dev
PROD_ENV_NAME = ailp-prod

.PHONY = dev prod run-dev run-prod stop-dev stop-prod clean logs restart images build-dev build-prod up-dev up-prod


build-dev:
	docker-compose -p $(DEV_ENV_NAME) -f docker-compose.yaml build

build-prod:
	docker-compose -p $(PROD_ENV_NAME) -f docker-compose.prod.yaml build

up-dev:
	docker-compose -p $(DEV_ENV_NAME) -f docker-compose.yaml up

up-prod:
	docker-compose -p $(PROD_ENV_NAME) -f docker-compose.prod.yaml up

run-dev:
	make build-dev
	make up-dev

run-prod:
	make build-prod
	make up-prod  


stop-dev:
	docker-compose -p $(DEV_ENV_NAME) down

stop-prod:
	docker-compose -p $(PROD_ENV_NAME) down

clean:
	docker-compose down --volumes

rmi:
	docker-compose down --volumes --rmi all

logs: 
	docker-compose -p $(DEV_ENV_NAME) logs -f

shell:
	docker-compose -p $(DEV_ENV_NAME) exec web bash

restart:
	make stop-dev
	make run-dev  

images:
	docker images

local-run:
	gunicorn -w 4 -k uvicorn.workers.UvicornWorker server:app --bind 0.0.0.0:8000 --reload


local-migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

