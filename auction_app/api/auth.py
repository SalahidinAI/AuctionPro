from auction_app.db.database import SessionLocal
from auction_app.db.schema import UserProfileSchema, LoginSchema
from auction_app.db.models import UserProfile, RefreshToken
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta, datetime
from fastapi_limiter.depends import RateLimiter
from auction_app.config import SECRET_KEY, REFRESH_EXPIRE_DAYS, ALGORITHM, ACCESS_EXPIRE_MINUTES
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

auth_router = APIRouter(prefix='/auth', tags=['Authorization'])

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login/')
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_EXPIRE_DAYS))


def verify_password(plain_password, hash_password):
    return password_context.verify(plain_password, hash_password)


def get_password_hash(password):
    return password_context.hash(password)


@auth_router.post('/register/', response_model=UserProfileSchema)
async def register(user_form: UserProfileSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user_form.username).first()
    if user_db:
        raise HTTPException(status_code=404, detail='Username already exists')

    email_db = db.query(UserProfile).filter(UserProfile.email == user_form.email).first()
    if email_db:
        raise HTTPException(status_code=404, detail='Email is busy')

    hashed_password = get_password_hash(user_form.password)
    new_user = UserProfile(
        username=user_form.username,
        first_name=user_form.first_name,
        last_name=user_form.last_name,
        email=user_form.email,
        phone_number=user_form.phone_number,
        profile_image=user_form.profile_image,
        role=user_form.role,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@auth_router.post('/login/', response_model=dict, dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def login(form: LoginSchema = Depends(), db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.email == form.email).first()
    if not user_db or not verify_password(form.password, user_db.password):
        raise HTTPException(status_code=404, detail='Wrong data')

    access_token = create_access_token({'sub': user_db.username})
    refresh_token = create_refresh_token({'sub': user_db.username})
    refresh_db = RefreshToken(token=refresh_token, user_id=user_db.id)
    db.add(refresh_db)
    db.commit()
    db.refresh(refresh_db)
    return {'access': access_token, 'refresh': refresh_token, 'type': 'bearer'}


@auth_router.post('/logout/', response_model=dict)
async def logout(token: str, db: Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not token_db:
        raise HTTPException(status_code=404, detail='Token not found')

    db.delete(token_db)
    db.commit()
    return {'message': 'Logged out'}


@auth_router.post('/refresh/')
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not token_db:
        raise HTTPException(status_code=404, detail='Token not found')

    access_token = create_access_token({'sub': token_db.user_id})

    return {'access_token': access_token, 'token_type': 'bearer'}
