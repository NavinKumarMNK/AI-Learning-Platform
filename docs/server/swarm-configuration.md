# Docker Swarm
Orchestration Tool used to scale the docker containers based on our needs. We use this to scale up the `django-server`, `postgres`, `cassandra` & `qdrant` services in the components

Swarm configurations are in `docker-compose.swarm.yaml` These configurations are pretty much similar to the `docker-compose.yaml` & `docker-compose.prod.yaml` except this it contains the hardcoded build image which is build using the `make build` (build of docker-compose-yaml) & the network is managed by the swarm itself.

Unlike the `docker-compose` this doesn't convert the `key:value` pairs in the `.env` file into environment variables, so before starting the orchestration we need to manually set the env variables. See the below command to do that.

```bash
set -a
source .env
set +a
```
Once the env variables are set we can straight away start the orchestration

```bash
docker swarm init

docker stack deploy -c docker-compose.swarm.yaml ailp-prod
docker service scale ailp-prod_web=2     # example: scale the service
```

The above set of commands will start the backend server. Here `ailp-prod` is the name of the stack. Every service will be named as `<stack-name>_<service>.<prod-no>.<id>`  