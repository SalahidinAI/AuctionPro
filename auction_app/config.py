import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 3
ALGORITHM = 'HS256'

class Settings:
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_KEY = os.getenv('GITHUB_KEY')
    GITHUB_LOGIN_CALLBACK = os.getenv('GITHUB_LOGIN_CALLBACK')

    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_KEY = os.getenv('GOOGLE_KEY')
    GOOGLE_LOGIN_CALLBACK = os.getenv('GOOGLE_LOGIN_CALLBACK')


settings = Settings()
