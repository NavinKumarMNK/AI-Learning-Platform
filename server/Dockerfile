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

# below two lines are required for ppc64le server
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH /root/.cargo/bin:$PATH


RUN pip install poetry

# Turn off Poetry's virtualenv to ensure dependencies are installed in the system Python environment
RUN poetry config virtualenvs.create false

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Poetry install
ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry install; else poetry install --no-dev; fi

# Copy all files
COPY . /app

EXPOSE 8000

ENV DJANGO_DEBUG=false

ENTRYPOINT [ "/app/entrypoint.sh" ]
