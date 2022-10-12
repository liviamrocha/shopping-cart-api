from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from shopping_cart.routers import api_router
from shopping_cart.core.settings import get_environment_variables
from shopping_cart.server.database import connect_db, close_conn_db
from shopping_cart.controllers.exceptions.custom_exceptions import (
    AlreadyExistException,
    NotFoundException,
    DataConflictException,
    NotAvailableException,
    NotValidException
)

env = get_environment_variables()
app = FastAPI(
    title=env.APP_NAME,
    version=1.0
)

# Add conection database
app.add_event_handler('startup', connect_db)
app.add_event_handler('shutdown', close_conn_db)

# Add API routes
app.include_router(api_router)

# Add exception handlers
@app.exception_handler(AlreadyExistException)
async def already_exist_handler(request: Request, exc: AlreadyExistException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message},
    )

@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )

@app.exception_handler(DataConflictException)
async def data_conflict_handler(request: Request, exc: DataConflictException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )

@app.exception_handler(NotAvailableException)
async def not_available_handler(request: Request, exc: NotAvailableException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )

@app.exception_handler(NotValidException)
async def not_available_handler(request: Request, exc: NotValidException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )


