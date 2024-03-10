#!/bin/bash

# Load environment variables from .env file (if it exists)
if [ -f .env ]; then
  . .env  # Source the .env file
fi

until </dev/tcp/$CASSANDRA_HOST/9042 > /dev/null 2>&1; do
  sleep 5
done


# echo "Cassandra is up - executing command"

# Run Django commands
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input

exec uvicorn server:app --host 0.0.0.0 --port 8000 --reload