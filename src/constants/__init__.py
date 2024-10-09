# Environments setup
from sys import argv
from dotenv import load_dotenv

# Environment config
DEVELOP_ARGS = "develop"
PRODUCTION_ARGS = "production"
DEVELOP_ENV = ".env.test"
PRODUCTION_ENV = ".env.production"

# Setup environment
if len(argv) > 1 and argv[1] == DEVELOP_ARGS:
    load_dotenv(DEVELOP_ENV)
if len(argv) > 1 and argv[1] == PRODUCTION_ARGS:
    load_dotenv(PRODUCTION_ENV)
