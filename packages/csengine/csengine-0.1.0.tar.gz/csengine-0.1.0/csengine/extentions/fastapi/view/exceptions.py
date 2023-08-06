import logging
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


async def handle_error(request: Request, exc: ValueError):
    logger.exception(exc)
    return JSONResponse(status_code=400, content={"details": str(exc)})
