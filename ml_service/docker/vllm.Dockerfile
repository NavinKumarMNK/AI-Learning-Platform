# Path: docker/vllm.Dockerfile

FROM vllm/vllm-openai:0.3.0
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y -no-install-recocommends \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

WORKDIR /app
COPY . /app


RUN chmod -R +x /app
RUN source ./prefetch.sh  

EXPOSE 8000

CMD ["serve", "run", "vllm_serve:app"]