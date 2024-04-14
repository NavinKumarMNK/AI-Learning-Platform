# -----------------------------------------------
# Stage 1: Base Image with CUDA and cuDNN
FROM ubuntu:22.04 AS nvidia-cuda
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y wget g++ nano build-essential gcc bzip2 software-properties-common git


RUN mkdir -p ~/miniconda3 && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.10.0-1-Linux-ppc64le.sh -O ~/miniconda3/miniconda.sh && \
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3 && \
    rm -rf ~/miniconda3/miniconda.sh 

ENV PATH=/root/miniconda3/bin:$PATH 
ENV CUDA_VERSION=12.2.0 
ENV CUDA_DOWNLOAD_URL=https://developer.download.nvidia.com/compute/cuda/${CUDA_VERSION}/local_installers/cuda_${CUDA_VERSION}_535.54.03_linux_ppc64le.run
ENV CUDNN_VERSION=8.9.5

RUN wget ${CUDA_DOWNLOAD_URL} -O cuda_installer.run && \
    chmod +x cuda_installer.run && \
    ./cuda_installer.run --silent --toolkit --no-opengl-libs && \
    rm cuda_installer.run && \
    bash -c "echo /usr/local/cuda/lib64 > /etc/ld.so.conf" && \
    ldconfig 

ENV PATH=/usr/local/cuda/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

COPY cudnn.tar.xz /root/
WORKDIR /root/

RUN mkdir cudnn && \
    tar -xvf cudnn.tar.xz -C cudnn --strip-components=1 && \
    rm cudnn.tar.xz && \
    cp cudnn/include/cudnn*.h /usr/local/cuda/include/ && \
    cp cudnn/lib/libcudnn* /usr/local/cuda/lib64/ && \
    rm -rf cudnn  

ENV CMAKE_CUDA_ARCHITECTURES=70 

RUN conda --version
RUN conda install -y -c open-ce open-ce-builder && \
    conda install -y -c conda-forge magma && \
    conda install cmake ninja