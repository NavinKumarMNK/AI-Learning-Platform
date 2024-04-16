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
	docker build . -t ml-service

run:
	docker run -it --runtime=nvidia --gpus all -v /data/navin-kumar-m:/data --ipc=host --privileged ml-service

run-vllm-ray:
	docker run -it --runtime=nvidia --gpus all -v /data/navin-kumar-m:/data --ipc=host --privileged ray-vllm

ray-up:
	ray up -y config/ray/ray-cluster.yaml --no-config-cache -v

ray-down:
	ray down -y config/ray/ray-cluster.yaml

ray-attach:
	ray attach config/ray/ray-cluster.yaml

RAY_BASH_CODE ?= 'python -c "import ray; ray.init()"'  # Default Python code
ray-exec:
	ray exec config/ray/ray-cluster.yaml $(RAY_BASH_CODE)

ray-serve-deploy:
	serve deploy config/ray/ray-serve.yaml -v

ray-serve-run:
	serve run config/ray/ray-serve.yaml

ray-serve-status:
	serve status

ray-log:
	ray logs config/ray/ray-cluster.yaml

ray-rsync-up:
	ray rsync-up config/ray/ray-cluster.yaml

ray-rsync-down:
	ray rsync-downs config/ray/ray-cluster.yaml

ray-up-dev:
	ray up -y config/ray/ray-cluster.dev.yaml --no-config-cache -v

ray-down-dev:
	ray down -y config/ray/ray-cluster.dev.yaml

ray-attach-dev:
	ray attach config/ray/ray-cluster.dev.yaml

ray-dev-ssh-rmkey:
	ssh-keygen -f "$(KH_PATH)" -R "[$(IP)]:$(PORT)"

ray-dev-ssh:
	ssh -p $(PORT) root@$(IP)

rm-pycache:
	find . -type d -name __pycache__ -exec rm -r {} +

llm_chat:
	python3 ./test/llm_client_http.py