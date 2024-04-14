

## Setup
> **Note:** Look at the `Makefile` for available commands.

Fill the configuration in .env
```env
ROOT_PATH=
```

For development
- before building the image, get the cudnn.tar.xz and place in the main directory. this is done to avoid authentication while downloading the library 
- rename the `*.tar.xz` -> `cudnn.tar.xz`. so the dockerfile could pick it up while building the image.

```bash
docker build . -t <image_name>
```

Run the container
```bash
docker run -it --runtime=nvidia --gpus all --ipc=host --privileged ml_service
```

Setup Using Ray:
```bash
make ray-up  # starts the cluster (add -dev) if need to perfom dev env
make ray-attach # attach to the container shell
make ray-serve-run  # to start the ray deployments
```
