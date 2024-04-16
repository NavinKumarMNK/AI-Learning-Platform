import random
import asyncio
import logging

from fastapi import FastAPI, Body
from starlette.responses import Response, JSONResponse, StreamingResponse
from typing import Optional, List, Literal
from pydantic import BaseModel
from starlette.requests import Request
from fastapi.exceptions import RequestValidationError
from http import HTTPStatus
from pydantic import ValidationError
from pydantic import BaseModel

app = FastAPI()

logger = logging.getLogger("uvicorn")


def create_error_response(status_code: HTTPStatus, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code.value, content={"detail": message})


string = "Hi, This is ML-Service Test server"


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )


class Message(BaseModel):
    role: Literal["system", "assistant", "user"]
    content: str

    def __str__(self):
        return self.content


class GenerateRequest(BaseModel):
    prompt: Optional[str]
    messages: Optional[List[Message]]
    stream: Optional[bool] = False
    max_tokens: Optional[int] = 128
    temperature: Optional[float] = 0.7
    ignore_eos: Optional[bool] = False


class GenerateResponse(BaseModel):
    output: str
    prompt_tokens: int
    output_tokens: int
    finish_reason: Optional[str] = None


async def simulate_llm_stream():
    """Simulates an LLM stream for the provided request."""

    async def async_generator(list_items):
        for item in list_items:
            yield item

    async for token in async_generator(string.split()):
        response = GenerateResponse(
            output=token + " ",
            prompt_tokens=1,
            output_tokens=1,
            finish_reason="stop",
        )
        await asyncio.sleep(0.01)
        yield (response.json() + "\n").encode("utf-8")


@app.post("/v1/llm")
async def generate(request: GenerateRequest, raw_request: Request) -> GenerateResponse:
    """Processes a generation request and returns the output (simulated)."""
    logger.info(request)
    if not request.prompt and not request.messages:
        return create_error_response(
            status_code=400,
            message="Either prompt or messages must be provided.",
        )

    if request.stream:
        return StreamingResponse(
            content=simulate_llm_stream(),
        )

    else:
        return GenerateResponse(
            output=string,
            prompt_tokens=1,
            output_tokens=len(string.split()),
            finish_reason="stop",
        )


@app.get("/v1/llm/health")
async def llm_health():
    """Returns a 200 status code for health check."""
    return Response(status_code=200)


@app.post("/v1/embed")
async def embed_endpoint(request: Request):
    """Returns a stream of 1024 random float vectors (placeholder)."""
    data = await request.json()
    req_type = data.get("type")

    if req_type not in ["PASSAGE_EMBED", "QUERY_EMBED", "PLAIN_EMBED"]:
        detail = "Invalid embedding type. Valid types are: PASSAGE_EMBED, QUERY_EMBED, PLAIN_EMBED"
        raise RequestValidationError(
            [{"loc": ("query", "type"), "msg": detail, "type": "value_error"}]
        )

    embedding = [float(random.randint(-100, 100)) for _ in range(1024)]
    return JSONResponse(content={"embedding": embedding})


@app.get("/v1/embed/health")
async def embed_health():
    """Returns a 200 status code for health check."""
    return Response(status_code=200)


# Run the server on port 5000 (modify "host" for external access)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=5000)
