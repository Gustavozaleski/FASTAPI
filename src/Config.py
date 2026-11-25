import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".env").resolve()

load_dotenv(env_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE = os.getenv("ACCESS_TOKEN_EXPIRE")
REFRESH_TOKEN_EXPIRE = os.getenv("REFRESH_TOKEN_EXPIRE")


if ACCESS_TOKEN_EXPIRE is None or REFRESH_TOKEN_EXPIRE is None:
    raise ValueError("Configurações de expiração não encontradas no .env")

ACCESS_TOKEN_EXPIRE = int(ACCESS_TOKEN_EXPIRE)
REFRESH_TOKEN_EXPIRE = int(REFRESH_TOKEN_EXPIRE)
print(ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE)
