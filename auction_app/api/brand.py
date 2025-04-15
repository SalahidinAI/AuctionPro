from auction_app.db.models import Brand, Car
from auction_app.db.schema import BrandSchema, BrandDetailSchema
from auction_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException, APIRouter

brand_router = APIRouter(prefix='/brand', tags=['Brands'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@brand_router.get('/', response_model=List[BrandSchema])
async def brand_list(db: Session = Depends(get_db)):
    return db.query(Brand).all()


@brand_router.get('/{brand_id}/', response_model=BrandDetailSchema)
async def brand_detail(brand_id: int, db: Session = Depends(get_db)):
    brand_db = db.query(Brand).filter(Brand.id == brand_id).first()

    if not brand_db:
        raise HTTPException(status_code=404, detail='Brand not found')

    cars_db = db.query(Car).filter(Car.brand_id == brand_id).all()
    return {
        'id': brand_db.id,
        'brand_name': brand_db.brand_name,
        'brand_cars': cars_db,
    }
