# -----------------------------------------------
# Stage 2: vllm+ray Build

FROM pytorch-triton AS ray-vllm

WORKDIR /root/
RUN git clone https://github.com/NavinKumarMNK/vllm.git 
RUN conda install -y -c conda-forge llvmlite=0.42.0

WORKDIR /root/vllm
RUN pip install -r requirements.txt
RUN conda install -y rocketce::ray-serve
RUN python3 setup.py develop
RUN python3 setup.py install

RUN conda install -y -c conda-forge prometheus_client=0.20.0
RUN conda install -y -c conda-forge nccl=2.20.5.1

WORKDIR /root/