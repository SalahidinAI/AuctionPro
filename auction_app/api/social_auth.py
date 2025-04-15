from sqlalchemy.orm import Session
from auction_app.db.database import SessionLocal
from fastapi import APIRouter, Depends
from starlette.requests import Request
from auction_app.config import settings
from authlib.integrations.starlette_client import OAuth

social_router = APIRouter(prefix="/oauth", tags=["Oauth"])

oauth = OAuth()
oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_KEY,
    authorize_url='https://github.com/login/oauth/authorize',
)

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_KEY,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid email profile"},
)


@social_router.get("/github/")
async def github_login(request: Request):
    redirect_uri = settings.GITHUB_LOGIN_CALLBACK
    return await oauth.github.authorize_redirect(request, redirect_uri)


@social_router.get("/google/")
async def google_login(request: Request):
    redirect_uri = settings.GOOGLE_LOGIN_CALLBACK
    return await oauth.google.authorize_redirect(request, redirect_uri)
