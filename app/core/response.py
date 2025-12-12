from fastapi.responses import JSONResponse


def error_response(message: str, code: int = 400):
    return JSONResponse(
        status_code=code,
        content={
            "success": False,
            "message": message,
            "data": None,
        }
    )
