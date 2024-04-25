build:
	docker build . -t ml-train

train:
	docker run -it --rm --runtime=nvidia --gpus all -v /data/navin-kumar-m:/data -v .:/app --ipc=host --privileged ml-service