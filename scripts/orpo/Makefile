build:
	docker build . -t ml-train

train:
	docker run -it --rm --runtime=nvidia --gpus all -v /data/navin-kumar-m:/data --ipc=host --privileged ml-train