# AI Learning Management System

    - Code is written to be run on a local linux PC machine on the lab.

## Plan
- [ ] Full website of Video Tutorials
- [ ] Deployed Website 
- [ ] Deployed LLM Model
- [ ] LLM Model SFT, DPO
- [ ] Dataset
- [ ] PDF parsing
- [ ] Speech-to-text (transcript)
- [ ] LLM Chat integeration with webiste

## Stack
### ML
- Python 
- Pytorch
- Ray

### Backend
- Go
- PostgreSQL

### Frontend
- React.js

## Setup

For development
- before building the image, get the cudnn.tar.xz and place in the main directory. this is done to avoid authentication while downloading the library 
- rename the `*.tar.xz` -> `cudnn.tar.xz`. so the dockerfile could pick it up while building the image.
```bash
docker build . -t your_image_name 
```

Run the container
```bash
docker run -it --runtime=nvidia --gpus all  --privileged nvidia-cuda
```