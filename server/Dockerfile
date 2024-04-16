FROM python:3.10.13-slim-bullseye
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc \
    libpq-dev \
    curl \
    wget \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip setuptools


# env to build the cryptography msgpack package
ENV PKG_CONFIG_PATH=/usr/lib/pkgconfig:/usr/local/lib/pkgconfig
ENV OPENSSL_DIR=/root/miniconda3/ssl
ENV POWERPC64LE_UNKNOWN_LINUX_GNU_OPENSSL_LIB_DIR=/usr/lib/powerpc64le-linux-gnu
ENV OPENSSL_LIB_DIR=/usr/lib/powerpc64le-linux-gnu
ENV POWERPC64LE_UNKNOWN_LINUX_GNU_OPENSSL_INCLUDE_DIR=/usr/include/openssl
ENV OPENSSL_INCLUDE_DIR=/usr/include/openssl

RUN pip install poetry

# Turn off Poetry's virtualenv to ensure dependencies are installed in the system Python environment
RUN poetry config virtualenvs.create false

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY README.md pyproject.toml poetry.lock /app/

# Poetry install
ARG INSTALL_DEV=false
RUN poetry update
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry install; else poetry install --only main; fi

# install library
COPY ./lib /app/lib
WORKDIR /app/lib
RUN pip install .
RUN rm -rf /app/lib

# Make server
WORKDIR /app
COPY . /app
EXPOSE 8000
ENV DJANGO_DEBUG=false

ENTRYPOINT [ "/app/entrypoint.sh" ]
