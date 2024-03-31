FROM ray-vllm AS ml-service
ARG DEBIAN_FRONTEND=noninteractive

RUN apt install -y rsync
#COPY ./requirements.txt /app/requirements.txt
#RUN pip install -r /app/requirements.txt

#WORKDIR /app
#COPY . /app

#EXPOSE 8000
WORKDIR /app/

#CMD  ["serve"]