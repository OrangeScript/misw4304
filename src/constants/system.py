from os import getenv

# Server Configuration
APP_HOST = "127.0.0.1"
APP_PORT = getenv("APP_PORT", 3000)
APP_TOKEN = getenv("APP_TOKEN", "token")
APP_THREADS = 2

# Environment variables
VERSION = getenv("VERSION")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")

# Database URLs
DEVELOP_URL_DB = "sqlite:///microservice_test.db"
PRODUCTION_URL_DB = (
    f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
