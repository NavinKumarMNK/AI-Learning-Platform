FROM ml_service 
ARG DEBIAN_FRONTEND=noninteractive

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8000

CMD  ["serve"]