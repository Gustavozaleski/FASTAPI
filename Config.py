import os
import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE = int(os.getenv("ACCESS_TOKEN_EXPIRE"))
REFRESH_TOKEN_EXPIRE = int(os.getenv("REFRESH_TOKEN_EXPIRE"))
RATELIMITER_SECONDS = int(os.getenv("RATELIMITER_SECONDS"))
RATELIMITER_TIME = int(os.getenv("RATELIMITER_TIME"))