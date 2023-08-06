import logging
import re
import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

from bogmark.logger import get_logger
from bogmark.structures.context import set_current_request_id

logger = get_logger(module=__name__)
uvicorn_logger = logging.getLogger("uvicorn.access")
uvicorn_logger.addFilter(lambda record: "/metrics" not in record.getMessage())
uvicorn_logger.addFilter(lambda record: "/readiness" not in record.getMessage())
uvicorn_logger.addFilter(lambda record: "/liveness" not in record.getMessage())

is_system_handler_re = re.compile("(readiness|liveness|metrics)")


async def log_request(request: Request, call_next):
    request_headers = dict(request.headers)

    curr_rid = request_headers.get("x-request-id")
    if curr_rid is None:
        curr_rid = str(uuid.uuid4())
    set_current_request_id(curr_rid)

    is_need_to_log = not is_system_handler_re.findall(request.scope["path"])
    if is_need_to_log:
        logger.info(
            msg="Request",
            extra={
                "x-service-name": request_headers.get("x-service-name", ""),
                "x-request-id": curr_rid,
                "method": request.method,
                "path": request.scope["path"],
                "url": str(request.url),
                "query_params": str(request.query_params),
                "status_code": 0,
            },
        )

    response = await call_next(request)

    if is_need_to_log:
        logger.info(
            msg="Response",
            extra={
                "x-service-name": request_headers.get("x-service-name", ""),
                "x-request-id": curr_rid,
                "method": request.method,
                "path": request.scope["path"],
                "url": str(request.url),
                "query_params": str(request.query_params),
                "status_code": response.status_code,
            },
        )
    return response


def register(app: FastAPI):
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_request)
