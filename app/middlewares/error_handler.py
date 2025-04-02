from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

async def custom_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    if isinstance(exc, IntegrityError):
        return JSONResponse(status_code=400, content={"detail": "Database integrity error - duplicate or constraint violation"})

    if isinstance(exc, SQLAlchemyError):
        return JSONResponse(status_code=500, content={"detail": "Database operation failed"})

    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

def add_exception_handlers(app):
    app.add_exception_handler(Exception, custom_exception_handler)
