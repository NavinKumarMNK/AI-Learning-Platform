FROM python:3.8.18-slim-bullseye
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install poetry

# Turn off Poetry's virtualenv to ensure dependencies are installed in the system Python environment
RUN poetry config virtualenvs.create false

# Poetry install
COPY . /app
WORKDIR /app 
# ENV PYTHONPATH=/

ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry install; else poetry install --no-dev; fi

EXPOSE 8000

ENV DJANGO_DEBUG=false

ENTRYPOINT [ "/app/entrypoint.sh" ]