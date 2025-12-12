from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from app.core.exceptions import AppException
from app.core.response import error_response
import traceback
import logging

logger = logging.getLogger("app")


async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"[AppException] {exc.message} {request.url}")
    return error_response(exc.message, exc.status_code)


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"[UnhandledException] {str(exc)} {request.url}\n{traceback.format_exc()}")
    return error_response("서버 내부 오류가 발생했습니다.", 500)


async def http_exception_handler(request: Request, exc: HTTPException):
    return error_response(exc.detail, exc.status_code)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return error_response(str(exc.errors()[0]["msg"]), 422)
