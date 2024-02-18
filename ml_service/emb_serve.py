import os

from fastapi import FastAPI
from fastembed.embedding import DefaultEmbedding
from ray import serve
from starlette.responses import JSONResponse

from utils import load_env
from utils.exception import ConfigFileMissingError
from utils.loggers import Logger, load_loggers
from utils.parsers import DictObjectParser, YamlParser

# load env
load_env()
MAIN_CONFIG_FILE_PATH = os.getenv("MAIN_CONFIG_FILE_PATH")
if MAIN_CONFIG_FILE_PATH is None:
    raise ConfigFileMissingError(
        "MAIN_CONFIG_FILE_PATH environemental variable is missing."
    )
# load main config file
yaml_parser = YamlParser(filepath=MAIN_CONFIG_FILE_PATH)
CONFIG: DictObjectParser = yaml_parser.get_data()

# load loggers
if CONFIG.loggers.log:
    logger: Logger = load_loggers(CONFIG.loggers)

# FastAPI app
APP = FastAPI()


@serve.deployment()
@serve.ingress(app=APP)
class EMBDeployment:
    def __init__(self):
        self.model_path = "small.en"
        self.emb = DefaultEmbedding()

    @APP.post("/embed")
    async def generate_embedding(self, request, raw_request):
        print(request)
        embedding = self.emb.query_embed(query=request)
        return JSONResponse(content={"embedding": embedding})


app = EMBDeployment.bind()
serve.run(app)
