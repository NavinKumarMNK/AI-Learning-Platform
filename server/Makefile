DEV_ENV_NAME = ailp-dev
PROD_ENV_NAME = ailp-prod

build:
	docker-compose -p $(DEV_ENV_NAME) -f docker-compose.yaml build

build-prod:
	docker-compose -p $(PROD_ENV_NAME) -f docker-compose.prod.yaml build

up:
	docker-compose -p $(DEV_ENV_NAME) -f docker-compose.yaml up

up-prod:
	docker-compose -p $(PROD_ENV_NAME) -f docker-compose.prod.yaml up

run:
	make build
	make up

run-prod:
	make build-prod
	make up-prod  

clean-pycache:
	find . -type d -name __pycache__ -exec rm -rf {} +


stop:
	docker-compose -p $(DEV_ENV_NAME) down

stop-prod:
	docker-compose -p $(PROD_ENV_NAME) down

clean:
	docker-compose down --volumes 
	docker-compose down --volumes --remove-orphans
	docker-compose rm -f

rmi:
	docker-compose down --volumes --rmi all

logs: 
	docker-compose -p $(DEV_ENV_NAME) logs -f

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

attach:
	docker-compose -p $(DEV_ENV_NAME) exec web bash

attach-cassandra:
	docker-compose -p $(DEV_ENV_NAME) exec cassandra bash

attach-postgres:
	docker-compose -p $(DEV_ENV_NAME) exec postgres bash

attach-prod:
	docker-compose -p $(PROD_ENV_NAME) exec web bash

attach-cassandra-prod:
	docker-compose -p $(PROD_ENV_NAME) exec cassandra bash

attach-postgres-prod:
	docker-compose -p $(PROD_ENV_NAME) exec postgres bash

app-build:
	bash download_static_files.sh

rm-pycache:
	find . -type d -name __pycache__ -exec rm -r {} +

ssh-copy:
	@echo "Copying file..."
	scp -i /Users/mnk/.ssh/id_rsa_vit $(FILE) root@172.16.0.57:/root/navin-kumar/AI-Learning-Platform/server/temp/
	@echo "File copied successfully."	