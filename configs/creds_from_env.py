import os

from dotenv import load_dotenv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
full_path = os.path.join(PROJECT_DIR, ".env")
normal_path = os.path.normpath(full_path)

env = load_dotenv(normal_path)
API_ENV_HOST: str = os.getenv("API_ENV_HOST")
API_ENV_PORT: int = int(os.getenv("API_ENV_PORT"))

API_DEFAULT_LOGIN = os.getenv("API_DEFAULT_LOGIN")
API_DEFAULT_PASSWORD = os.getenv("API_DEFAULT_PASSWORD")
