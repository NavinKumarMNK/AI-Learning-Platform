from http import HTTPStatus

from starlette.responses import JSONResponse


def create_error_response(status_code: HTTPStatus, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code.value, content={"detail": message})
