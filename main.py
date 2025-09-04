from fastapi import FastAPI
import settings
from contextlib import asynccontextmanager
from logging import getLogger
from utils.database import is_postgres_healthy
from api.router import api_router


logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application is running up...")
    logger.info("Checking for postgres availability...")
    if not await is_postgres_healthy(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB
    ):
        raise RuntimeError(
            f"Failed to connect to PostgreSQL DB"
        )
        
    yield
    logger.info("Application is shut down")



app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# healthcheck function

@app.get("/health")
async def health():
    return {"status": "ok"}


tasg_metadata = [
    {"name": "users", "description": "Users management"}
]

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level="info"
    )