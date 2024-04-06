FROM ray-vllm AS ml-service
ARG DEBIAN_FRONTEND=noninteractive

RUN apt install -y rsync
#RUN conda install -y rocketce::onnxruntime
#COPY ./requirements.txt /app/requirements.txt
#RUN pip install -r /app/requirements.txt
#RUN pip install fastembed==0.2.5 --no-deps

COPY . /app

WORKDIR /app/