# -----------------------------------------------
# Stage 1: pytorch-triton Build

FROM pytorch AS pytorch-triton
WORKDIR /root/

RUN git clone https://github.com/llvm/llvm-project
RUN apt-get install -y clang lld

WORKDIR /root/llvm-project
RUN git checkout c5dede880d175f7229c9b2923f4753e12702305d

RUN mkdir build
WORKDIR ./build

RUN rm -rf /root/miniconda3/lib/libz.so.1 && \
    rm -rf /root/miniconda3/lib/libxml2.so.2

RUN cmake -G Ninja ../llvm \
   -DLLVM_ENABLE_PROJECTS="mlir;llvm" \
   -DLLVM_BUILD_EXAMPLES=ON \
   -DLLVM_TARGETS_TO_BUILD="PowerPC;NVPTX;X86;AMDGPU;RISCV" \
   -DMLIR_ENABLE_CUDA_RUNNER=ON \
   -DCMAKE_BUILD_TYPE=Release \
   -DLLVM_ENABLE_ASSERTIONS=ON \
   -DCMAKE_C_COMPILER=clang \
   -DCMAKE_CXX_COMPILER=clang++ \
   -DLLVM_ENABLE_RTTI=ON \
   -DLLVM_INSTALL_UTILS=ON \
   -DMLIR_INCLUDE_INTEGRATION_TESTS=ON

RUN ninja && ninja install

RUN rm -rf /usr/lib/llvm-14/
ENV LLVM_EXTERNAL_LIT=/root/llvm-project/build/bin/llvm-lit
ENV LLVM_BUILD_DIR=/root/llvm-project/build/

WORKDIR /root/
RUN git clone https://github.com/pybind/pybind11.git
RUN pip install pytest
WORKDIR /root/pybind11
RUN mkdir build
WORKDIR /root/pybind11/build
RUN cmake .. && make check && make install

# install triton
WORKDIR /root/
RUN git clone https://github.com/NavinKumarMNK/triton.git
WORKDIR /root/triton/
RUN mkdir build
WORKDIR ./build
RUN cmake .. && make
RUN mv libtriton.so /root/triton/python/triton/_C/
WORKDIR /root/triton/python
RUN python3 download_ptxas.py

ENV TRITON_HOME=/root/triton/
ENV PYTHONPATH=/root/triton/python:${PYTHONPATH}

WORKDIR /root
