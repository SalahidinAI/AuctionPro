from auction_app.db.models import Auction, Car
from auction_app.db.schema import AuctionSchema, AuctionGetSchema
from auction_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException


auction_router = APIRouter(prefix='/auction', tags=['Auctions'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auction_router.post('/', response_model=AuctionSchema)
async def auction_create(auction: AuctionSchema, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id == auction.car_id).first()
    if not car_db:
        raise HTTPException(status_code=404, detail='Car not found')

    auction_db = Auction(**auction.dict())
    db.add(auction_db)
    db.commit()
    db.refresh(auction_db)
    return auction_db


@auction_router.get('/', response_model=List[AuctionGetSchema])
async def auction_list(db: Session = Depends(get_db)):
    return db.query(Auction).all()


@auction_router.get('/{auction_id}/', response_model=AuctionSchema)
async def auction_detail(auction_id: int, db: Session = Depends(get_db)):
    auction_db = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction_db:
        raise HTTPException(status_code=404, detail='Auction not found')
    return auction_db


@auction_router.put('/{auction_id}/', response_model=AuctionSchema)
async def auction_update(auction_id: int, auction: AuctionSchema, db: Session = Depends(get_db)):
    auction_db = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction_db:
        raise HTTPException(status_code=404, detail='Car not found')

    for auction_key, auction_value in auction.dict().items():
        setattr(auction_db, auction_key, auction_value)

    db.add(auction_db)
    db.commit()
    db.refresh(auction_db)
    return auction_db


@auction_router.delete('/{auction_id}/')
async def auction_delete(auction_id: int, db: Session = Depends(get_db)):
    auction_db = db.query(Auction).filter(Auction.id == auction_id).first()
    if not auction_db:
        raise HTTPException(status_code=404, detail='Auction not found')

    db.delete(auction_db)
    db.commit()
    return {'message': 'Deleted'}
