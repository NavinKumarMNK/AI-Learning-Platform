FROM ray-vllm AS ml-service
ARG DEBIAN_FRONTEND=noninteractive

RUN apt install -y rsync
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip install fastembed==0.2.5 --no-deps
RUN conda install -y rocketce::onnxruntime

# COPY . /app
ENV RAY_DEDUP_LOGS=1

RUN printenv | awk -F= '{print "export " $1 "=\"" $2 "\""}' >> ~/.bashrc

WORKDIR /app/