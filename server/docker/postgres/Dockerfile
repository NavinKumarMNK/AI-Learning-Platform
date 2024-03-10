FROM postgres

COPY init-postgres.sh /docker-entrypoint-initdb.d/
EXPOSE 5432

RUN chmod +x /docker-entrypoint-initdb.d/init-postgres.sh 