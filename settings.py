import os
from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv()

def require(key: str, cast=str):
    value = os.getenv(key)
    if value is None:
        raise RuntimeError(f"{key} is required but not set in environment variables!")
    try:
        return cast(value)
    except Exception as e:
        raise RuntimeError(f"Failed to cast {key}: {e}") from e
    

# Mandatory settings
APP_PORT = require("APP_PORT", cast=int)
APP_HOST = require("APP_HOST")

POSTGRES_USER = require("POSTGRES_USER")
POSTGRES_PASSWORD = require("POSTGRES_PASSWORD")
POSTGRES_HOST = require("POSTGRES_HOST")
POSTGRES_PORT = require("POSTGRES_PORT", cast=int)
POSTGRES_DB = require("POSTGRES_DB")


# Logging settings and loggers

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": True
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default"}
    },
    "root": {"level": "INFO", "handlers": ["console"]},
})

# Not Mandatory settings:
APP_NAME = os.getenv("APP_NAME", default="fast-api-application-development")
APP_VERSION = os.getenv("APP_VERSION", default="1.0.0")