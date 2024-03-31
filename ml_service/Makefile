# install requirements
install:
	pip install -r requirements.txt

# build ml-service Docker image
build-llm-base:
	build-cuda build-pytorch build-triton build-ray-vllm 
	
build-cuda:
	docker build -f ./docker/cuda.Dockerfile -t nvidia-cuda .

build-pytorch:
	docker build -f ./docker/pytorch.Dockerfile -t pytorch .

build-triton:
	DOCKER_BUILDKIT=0 docker build -f ./docker/triton.Dockerfile -t pytorch-triton .

build-ray-vllm:
	DOCKER_BUILDKIT=0 docker build -f ./docker/vllm.Dockerfile -t ray-vllm .

# main docker image as llm service
build: 
	docker build . -t llm-serve

run-llm:
	docker run -it --runtime=nvidia --gpus all -v /data/:/workspace --ipc=host --privileged llm_serve

run-vllm-ray:
	docker run -it --runtime=nvidia --gpus all -v /data/:/workspace  --ipc=host --privileged ray-vllm

