import os
import numpy as np

from ray.serve import Application
from fastapi import FastAPI
from fastembed import TextEmbedding
from ray import serve
from starlette.responses import JSONResponse, Response
from starlette.requests import Request
from utils.base import load_env
from utils.loggers import Logger, load_loggers
from utils.parsers import DictObjectParser, YamlParser
from utils.exception import ConfigFileMissingError
from typing import Dict, List
from fastapi.exceptions import RequestValidationError
from utils.http import create_error_response
from http import HTTPStatus

# FastAPI app
APP = FastAPI()


@APP.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return create_error_response(HTTPStatus.BAD_REQUEST, str(exc))


@serve.deployment()
@serve.ingress(app=APP)
class EMBDeployment:
    """Embedding Generate Deployment Class"""

    def __init__(self, config: DictObjectParser, logger: Logger):
        """Construct

        Parameters
        ----------
        config : DictObjectParser
            contains config for the deployment of llm
        logger : Logger
            object which will be used for logging
        """
        self.logger = logger
        print("inside class")
        self.logger.error("EMB Deployment Initialized")
        self.model = TextEmbedding(**config.serve_config.to_dict())

    @APP.get("/health")
    async def health(self) -> Response:
        """Health check endpoint."""
        return Response(status_code=200)

    @APP.post("/embed")
    async def generate_embedding(self, request: Request, raw_request):
        print(request)
        self.logger.info(request)
        req_type = request.query_params.get("type")
        if req_type == "PASSAGE_EMBED":
            embedding: List[np.ndarray] = list(
                self.model.passage_embed(request.query_params.get("data"))
            )
        elif req_type == "QUERY_EMBED":
            embedding = list(
                self.model.query_embed(query=request.query_params.get("data"))
            )[0]
        elif req_type == "PLAIN_EMBED":
            embedding = list(self.model.embed(query=request.query_params.get("data")))[
                0
            ]
        self.logger.info(embedding)
        return JSONResponse(content={"embedding": embedding})


def main(args: Dict[str, str]) -> Application:
    # load env
    load_env()
    EMB_PATH = os.getcwd()
    CONFIG_FILE = os.path.join(EMB_PATH, "config.yaml")
    if os.path.exists(CONFIG_FILE) is None:
        raise ConfigFileMissingError(
            "MAIN_CONFIG_FILE_PATH environmental variable is missing."
        )

    # load main config file
    yaml_parser = YamlParser(filepath=CONFIG_FILE)
    CONFIG: DictObjectParser = yaml_parser.get_data()

    # load loggers
    logger: Logger = load_loggers(CONFIG.loggers, name=__name__)
    config_key: str = args.get("config_key")

    return EMBDeployment.bind(getattr(CONFIG, config_key, None), logger=logger)


if __name__ == "__main__":
    app = main({"config_key": "llm"})
    serve.run(app)
