FROM python:3.8.18-slim-bullseye
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install poetry

# Turn off Poetry's virtualenv to ensure dependencies are installed in the system Python environment
RUN poetry config virtualenvs.create false

# peotry install
COPY . /app
WORKDIR /app

ARG INSTALL_DEV=false
RUN if [ "$INSTALL_DEV" = "true" ]; then poetry install; else poetry install --only main; fi

EXPOSE 8000

# Run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]