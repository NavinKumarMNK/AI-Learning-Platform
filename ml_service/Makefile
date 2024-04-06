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
	docker build -f ./docker/triton.Dockerfile -t pytorch-triton .

build-ray-vllm:
	docker build -f ./docker/vllm.Dockerfile -t ray-vllm .

# main docker image as llm service
build: 
	docker build . -t ml-service

run:
	docker run -it --runtime=nvidia --gpus all -v /data/:/workspace --ipc=host --privileged ml-service

run-vllm-ray:
	docker run -it --runtime=nvidia --gpus all -v /data/:/workspace  --ipc=host --privileged ray-vllm

ray-up:
	ray up -y config/ray-cluster.yaml --no-config-cache -v

ray-down:
	ray down -y config/ray-cluster.yaml

ray-attach:
	ray attach config/ray-cluster.yaml

RAY_BASH_CODE ?= 'python -c "import ray; ray.init()"'  # Default Python code
ray-exec:
	ray exec config/ray-cluster.yaml $(RAY_BASH_CODE)

ray-serve-deploy:
	serve deploy config/ray-serve.yaml -v

ray-serve-run:
	serve run config/ray-serve.yaml

ray-serve-status:
	serve status

ray-log:
	ray logs config/ray-cluster.yaml

ray-rsync-up:
	ray rsync-up config/ray-cluster.yaml -v

ray-rsync-down:
	ray rsync-downs config/ray-cluster.yaml
