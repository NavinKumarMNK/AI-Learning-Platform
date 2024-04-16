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
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
CASSANDRA_HOST=cassandra
CASSANDRA_USER=cassandra
CASSANDRA_PASSWORD=cassandra
CASSANDRA_CLUSTER_NAME=cassandra
CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch
CASSANDRA_KEYSPACE=megacad
DJANGO_SECRET_KEY=django
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_EMAIL_ID=admin
DJANGO_ADMIN_PASSWORD=admin
QDRANT_COLLECTION_NAME=qdrant
QDRANT_HOST=qdrant
ML_SERVICE_HOST=localhost
ML_SERVICE_PORT=port
```

