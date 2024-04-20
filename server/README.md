# AI-Learning Platform

## Dev Server
- First, build the `frontend` from `../app/*`, the build files will be directly moved here `./static/` and its ready for `collectstatic`.
- before running the server's docker compose make the `entrypoint.sh` file executable
```bash
chmod +x entrypoint.sh
```
```bash
make run-dev  # run the docker-compose up
```
- view the `Makefile` for commands like `stop`, `clean`, `rmi`, `shell` etc.,
- Access the Qdrant Server commands through the qdrant web dashboard `localhost:6333/dashboard`. Mainly needed to create the collections

## Environment Variables Schema
```env
POSTGRES_DB=megacad
POSTGRES_USER=megacad
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
CASSANDRA_HOST=cassandra
CASSANDRA_USER=cassandra
CASSANDRA_PASSWORD=cassandra
CASSANDRA_CLUSTER_NAME=cassandra
CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
CASSANDRA_KEYSPACE=megacad
QDRANT_COLLECTION_NAME=megacad
QDRANT_HOST=qdrant
DJANGO_SECRET_KEY=django
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_EMAIL_ID=admin
DJANGO_ADMIN_PASSWORD=admin
ML_SERVICE_HOST=ml_service
ML_SERVICE_PORT=5000
ROOT_PATH=
WEB_ADDRESS=megacad.com
DJANGO_HOST=django
LLM_ENDPOINT=/v1/llm
EMBEDDING_ENDPOINT=/v1/embed
```

