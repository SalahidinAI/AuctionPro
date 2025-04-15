from auction_app.db.models import Bid, Auction, UserProfile
from auction_app.db.schema import BidSchema
from auction_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException

bid_router = APIRouter(prefix='/bid', tags=['Bids'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@bid_router.post('/', response_model=BidSchema)
async def bid_create(bid: BidSchema, db: Session = Depends(get_db)):
    auction_db = db.query(Auction).filter(Auction.id == bid.auction_id).first()
    if not auction_db:
        raise HTTPException(status_code=404, detail='Seller not found')

    buyer_db = db.query(UserProfile).filter(UserProfile.id == bid.buyer_id).first()
    if not buyer_db:
        raise HTTPException(status_code=404, detail='Buyer not found')

    bid_db = Bid(**bid.dict())
    db.add(bid_db)
    db.commit()
    db.refresh(bid_db)
    return bid_db


@bid_router.get('/', response_model=List[BidSchema])
async def bid_list(db: Session = Depends(get_db)):
    return db.query(Bid).all()
