import functools
import logging
from fastapi import HTTPException
from pydantic import ValidationError
from prisma.errors import PrismaError

logger = logging.getLogger(__name__)

def handle_service_exceptions(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except (PrismaError, ValidationError) as e:
            logger.error(f"Service error in {func.__name__}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    return wrapper
