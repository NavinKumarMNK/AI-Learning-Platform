# install requirements
install:
	pip install -r requirements.txt

# build ml-service Docker image
build-full:
	build-pytorch build-vllm build 
	

# build vllm Docker image
build-ray-vllm:
	DOCKER_BUILDKIT=0 docker build -f ./docker/vllm.Dockerfile -t ray-vllm .

# build pytorch Docker image
build-pytorch:
	docker build -f ./docker/pytorch.Dockerfile -t pytorch .
	
# build all Docker images
build: 
	docker build . -t ml-service