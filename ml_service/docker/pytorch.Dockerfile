# -----------------------------------------------
# Stage 2: Pytorch Build

FROM nvidia-cuda AS pytorch

RUN git clone --branch ppc64le https://github.com/NavinKumarMNK/pytorch.git --recursive

# ENV PYTORCH_VERSION 2.1.2
ENV PYTORCH_BUILD_NUMBER 0
ENV PYTORCH_BUILD_VERSION 2.1.2
ENV PYTORCH_VERSION 2.1.2
ENV TORCH_CUDA_ARCH_LIST="7.0"

WORKDIR /root/pytorch
RUN python setup.py develop


RUN git pull origin ppc64le
RUN pip install -r requirements.txt
RUN python setup.py install

WORKDIR /usr/local/cuda/lib64
RUN ln -sf libcudnn.so.8.9.5 libcudnn.so.8 && \
    ln -sf libcudnn_adv_infer.so.8.9.5 libcudnn_adv_infer.so.8 && \
    ln -sf libcudnn_ops_infer.so.8.9.5 libcudnn_ops_infer.so.8 && \
    ln -sf libcudnn_ops_train.so.8.9.5 libcudnn_ops_train.so.8 && \
    ln -sf libcudnn_adv_train.so.8.9.5 libcudnn_adv_train.so.8 && \
    ln -sf libcudnn_cnn_train.so.8.9.5 libcudnn_cnn_train.so.8 && \
    ln -sf libcudnn_cnn_infer.so.8.9.5 libcudnn_cnn_infer.so.8

RUN rm -rf /root/miniconda3/lib/libtinfo.so.6
RUN apt-get install -y zlib1g-dev gfortran libopenblas-dev pkg-config