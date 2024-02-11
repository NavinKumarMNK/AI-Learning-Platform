import logging
import os
import uuid
from http import HTTPStatus
from typing import AsyncGenerator, Dict, List, Optional, Tuple

# from langchain_community.llms import VLLM
import ray
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from ray import serve
from ray.serve import Application
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.sampling_params import SamplingParams

from ml.llm.engine import VLLMConfig, get_vllm_engine_config
from ml.llm.model_config import load_model_config
from ml.llm.protocol import GenerateRequest, GenerateResponse

# from vllm import LLM
from utils import load_env
from utils.exception import ConfigFileMissingError, MaximumContextLengthError
from utils.http import create_error_response
from utils.loggers import Logger, load_loggers
from utils.parsers import DictObjectParser, YamlParser

# FastAPI APP
APP = FastAPI()


@APP.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return create_error_response(HTTPStatus.BAD_REQUEST, str(exc))


# VLLM Server Deployment
@serve.deployment()
@serve.ingress(APP)
class VLLMDeployment:
    """VLLM Generate Deployment Class for Ray Serve."""

    def __init__(self, config: DictObjectParser, logger: Logger) -> None:
        """Construct

        Parameters
        ----------
        config : DictObjectParser
            contains config for the deployment of llm
        """
        self.logger = logger
        self.logger.info("VLLM Deployment Initialized")

        self.config = config
        async_engine_args = AsyncEngineArgs(**config.serve_config.to_dict())
        self.logger.info(async_engine_args)
        # Engine Args
        self.engine = AsyncLLMEngine.from_engine_args(async_engine_args)
        self.engine_model_config = self.engine.engine.get_model_config()
        self.tokenizer = self.engine.engine.tokenizer
        self.max_model_len: float = self.config.serve_config.max_model_len

        self.logger.info(f"VLLM Engine Config: {self.engine_model_config}")
        print(f"VLLM Engine Config: {self.engine_model_config}")

        try:
            self.model_config = load_model_config(self.engine_model_config.model)
        except FileNotFoundError:
            self.logger.warning(
                f"No Model Config for: {self.config.serve_config.model}"
            )
            self.model_config = None

        print(self.model_config, "Deployment Inititalized")

    def _next_request_id(self) -> str:
        # produce unique id using host ID, sequence number and time
        return str(uuid.uuid1().hex)

    def _convert_prompt_to_tokens(
        self, prompt: str, request: GenerateRequest
    ) -> List[int]:
        input_ids = self.tokenizer(prompt).input_ids
        if self._check_length(input_ids=input_ids, request=request):
            return input_ids

    def _check_length(self, input_ids, request: GenerateRequest) -> List[int]:
        prompt_len = len(input_ids)  # total num of tokens in input

        if request.max_tokens is None:
            request.max_tokens = (
                self.max_model_len - prompt_len
            )  # assigining max_tokens that can be generated if not assigned
        if prompt_len - request.max_tokens > self.max_model_len:
            raise MaximumContextLengthError(
                max_model_len=self.max_model_len,
                prompt_len=prompt_len,
                request_max_len=request.max_tokens,
            )  # if input_tokens + tokens need to be generated > max_context_length of model

        self.logger.debug(
            f"Maximum context length of the model is {self.max_model_len}, Message length is {prompt_len}",
        )
        return True

    async def _stream_results(self, output_generator) -> AsyncGenerator[bytes, None]:
        """Stream the results of the output generator"""
        num_returned = 0
        async for request_output in output_generator:
            output = request_output.output[0]
            text_output = output.text[num_returned:]
            response = GenerateResponse(
                output=text_output,
                prompt_tokens=len(request_output.prompt_token_ids),
                output_tokens=1,
                finish_reason=output.finish_reason,
            )
            yield (response.json() + "\n").encode("utf-8")
            num_returned += len(text_output)

    async def _abort_request(self, request_id) -> None:
        await self.engine.abort(request_id=request_id)

    @APP.get("/health")
    async def health(self) -> Response:
        """Health check endpoint."""
        return Response(status_code=200)

    @APP.post("/generate")
    async def generate(
        self, request: GenerateRequest, raw_request: Request
    ) -> Response:
        """Generate Completion for the requested prompt"""
        try:
            # either prompt or messages is provided
            if not request.prompt and not request.messages:
                return create_error_response(
                    status_code=400,
                    message="Either prompt or messages must be provided.",
                )

            # Handling cases based on either prompt or messages is provided
            if request.prompt:
                prompt = request.prompt
            elif self.model_config:
                prompt = self.model_config.prompt_format.generate_prompt(
                    request.message
                )
            else:
                return create_error_response(
                    status_code=400,
                    message="Parameter 'messages' requires a model config ",
                )

            prompt_token_ids = self._convert_prompt_to_tokens(
                prompt=prompt, request=request
            )
            request_dict = request.dict(exclude=set(["prompt", "messages", "stream"]))
            sampling_params = SamplingParams(**request_dict)
            request_id = self._next_request_id()

            output_generator = self.engine.generate(
                prompt=None,
                sampling_params=sampling_params,
                request_id=request_id,
                prompt_token_ids=prompt_token_ids,
            )

            # Handle streaming, if the socket connection drops then abort the request processing
            if request.stream:
                background_tasks = BackgroundTasks()
                background_tasks.add_task(self._abort_request, request_id)
                return StreamingResponse(
                    self._stream_results(output_generator),
                    background=background_tasks,
                )
            else:
                final_output = None
                async for request_output in output_generator:
                    if await raw_request.is_disconnected():
                        await self.engine.abort(request_id=request_id)
                        return Response(status_code=200)
                    final_output = request_output

                text_outputs = final_output.output[0].text
                prompt_tokens = len(final_output.prompt_token_ids)
                output_tokens = len(final_output.output[0].token_ids)
                finish_reason = final_output.output[0].finish_reason

                return GenerateResponse(
                    output=text_outputs,
                    prompt_tokens=prompt_tokens,
                    output_tokens=output_tokens,
                    finish_reason=finish_reason,
                )

        except MaximumContextLengthError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            self.logger.error("Error in generating completion", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))


def main(args: Dict[str, str]) -> Application:
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

    config_key: str = args.get("config_key")
    return VLLMDeployment.bind(getattr(CONFIG, config_key, None), logger=logger)


if __name__ == "__main__":
    """
    ray.init(runtime_env={"working_dir": os.path.join(os.getcwd())})
    serve.run(
        main({"config_key": "llm"}),
    )
    """
