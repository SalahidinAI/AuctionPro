from auction_app.db.models import CarImage, Car
from auction_app.db.schema import CarImageSchema, CarImageGetSchema
from auction_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException


image_router = APIRouter(prefix='/car_image', tags=['CarImages'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@image_router.post('/', response_model=CarImageSchema)
async def car_image_create(image: CarImageSchema, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id == image.car_id).first()
    if not car_db:
        raise HTTPException(status_code=404, detail='Car not found')

    image_db = CarImage(**image.dict())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return image_db


@image_router.get('/', response_model=List[CarImageGetSchema])
async def car_image_list(db: Session = Depends(get_db)):
    return db.query(CarImage).all()


@image_router.delete('/{image_id}/')
async def car_image_delete(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(CarImage).filter(CarImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail='Image not found')

    db.delete(image_db)
    db.commit()
    return {'message': 'Image is deleted'}
