from fastapi import FastAPI
import uvicorn
from auction_app.api import (brand, model, car, auth, car_image,
                             auction, bid, feedback, profile, social_auth)
from auction_app.admin.setup import setup_admin
from starlette.middleware.sessions import SessionMiddleware
import redis.asyncio as aioredis
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter

async def init_redis():
    return aioredis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


auction_app = FastAPI(title='Auction', lifespan=lifespan)
auction_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")
setup_admin(auction_app)

auction_app.include_router(auth.auth_router)
auction_app.include_router(profile.user_router)
auction_app.include_router(brand.brand_router)
auction_app.include_router(model.model_router)
auction_app.include_router(car.car_router)
auction_app.include_router(car_image.image_router)
auction_app.include_router(auction.auction_router)
auction_app.include_router(bid.bid_router)
auction_app.include_router(feedback.feedback_router)
auction_app.include_router(social_auth.social_router)


if __name__ == '__main__':
    uvicorn.run(auction_app, host='127.0.0.1', port=8000)
