# Server Config
We have `django-web-server`, `postgres`, `cassandra`, `qdrant` services running in the server. Here `postgres`, `cassandra`, `qdrant` are the database thats needed for this application. 

<div style="background-color: #e0f2fe; color: #005080; padding: 15px; border: 1px solid #add8e6; border-radius: 5px; margin-bottom: 15px;">
  <strong>Note:</strong><br>
It also includes ml-service in the development environment. This is a simulated ml-service, since every time we can't have access or test in the prod environment. This ml-service have two endpoints as in real prod where every time it gives the same response.
</div>

<div style="background-color: #fcf8e3; color: #8a6d3b; padding: 15px; border: 1px solid #faebcc;">
  <strong>Important : </strong> Always use `Makefile` commands. You can have a look at it for more clarity.
  Any command attached with the `-dev` or `-prod` is specific to that environment. 
</div>

- For `dev` use the `docker-compose.yaml` commands when you are working on dev environment. So start the server with docker compose. Starting individual components produce some errors.

- For `prod` env, I recommend you to use `docker-swarm.yaml` over the `docker-compose.prod.yaml` 

### Example .env file
The below code block is the example how the `.env` file looks like. This should be in the root directory of server `$ROOT/server`. This should be present for the server to run (both in dev & prod environments)

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

### Build
Since the server is running on a `ppc64le` architecture, many of the python packages wont directly get installed. So the docker files for the each service which don't support the `ppc64le` environments are build from the source. This is not hte case for the `dev` environment. `dev` environment is build keeping `mac-os` and `linux-os` in the mind. So it can handle `x64` builds.

`Qdrant-DB` is running as x64 container on top of the `QEMU` virtualizer, even in the `production` environment. Anyone could try to improve the `qemu` overhead by try writing a dockerfile code to build the `qdrant-db` form the source
that works on the `ppc64le` architecture