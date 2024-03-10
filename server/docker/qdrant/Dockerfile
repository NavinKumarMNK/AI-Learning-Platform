FROM qdrant/qdrant 

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 6333 6334 

# COPY qdrant.conf.yaml /qdrant/config/config.yaml
