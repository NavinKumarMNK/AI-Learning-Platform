# -----------------------------------------------
# Stage 2: vllm+ray Build

FROM pytorch-triton AS ray-vllm

WORKDIR /root/
RUN rm -rf vllm
RUN git clone https://github.com/NavinKumarMNK/vllm.git
RUN conda install -y conda-forge::llvmlite

WORKDIR /root/vllm
RUN git pull
RUN pip install -r requirements.txt
RUN conda install -y rocketce::ray-serve
RUN python3 setup.py develop
RUN python3 setup.py install

RUN conda install conda-forge::prometheus_client
RUN conda install -y -c conda-forge nccl

WORKDIR /root/