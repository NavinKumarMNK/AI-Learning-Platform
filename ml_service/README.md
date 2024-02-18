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
```bash
docker build -t your_image_name -f dev.Dockerfile .
```

Run the container
```bash
docker run -it -p 22:22 -p 8080:8080 -v /path:/app image-name bash
```