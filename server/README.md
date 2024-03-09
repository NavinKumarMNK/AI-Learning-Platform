# AI-Learning Platform

## Dev Server
- before running the server's docker compose make the `entrypoint.sh` file executable
```bash
chmod +x entrypoint.sh
```
```bash
make run-dev  # run the docker-compose up
```
- view the `Makefile` for commands like `stop`, `clean`, `rmi`, `shell` etc.,

## Environment Variables Schema
```env
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=postgres
CASSANDRA_NAME=cassandra
CASSANDRA_HOST=cassandra
CASSANDRA_USER=cassandra
CASSANDRA_PASSWORD=cassandra
DJANGO_SECRET_KEY=django
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_EMAIL_ID=admin
DJANGO_ADMIN_PASSWORD=admin
```