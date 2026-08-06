from fastapi import FastAPI
from utils.logger import logger
from api.routes import router
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback

app = FastAPI(
    title="Zecpath AI ATS API",
    version="1.0.0",
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    logger.error(f"Unhandled Exception: {str(exc)}")
    logger.error(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    logger.warning(f"Validation Error: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Invalid request data",
            "errors": exc.errors()
        }
    )

logger.info("AI Recruitment System Started")
logger.info("Loading AI modules...")

app.include_router(router, prefix="/api", tags=["ATS"])


@app.get("/")
def home():
    return {"message": "Welcome to Zecpath AI ATS API"}