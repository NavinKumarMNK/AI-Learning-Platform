FROM python:3.8.18-slim-bullseye
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install poetry

# Turn off Poetry's virtualenv to ensure dependencies are installed in the system Python environment
RUN poetry config virtualenvs.create false

# Poetry install
COPY . /app
WORKDIR /app

ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry install; else poetry install --no-dev; fi

EXPOSE 8000

ENV DJANGO_DEBUG=False

# Run Django commands
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --no-input

# Run the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
