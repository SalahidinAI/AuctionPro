from tkinter.tix import IMAGE

from auction_app.db.models import Car, UserProfile, Model, CarImage
from auction_app.db.schema import CarSchema, CarGetSchema, CarImageSchema
from auction_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException


car_router = APIRouter(prefix='/car', tags=['Cars'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@car_router.post('/', response_model=CarSchema)
async def car_create(car: CarSchema, db: Session = Depends(get_db)):
    seller_db = db.query(UserProfile).filter(UserProfile.id == car.seller_id).first()
    if not seller_db:
        raise HTTPException(status_code=404, detail='Seller not found')

    brands_model = db.query(Model).filter(Model.id == car.model_id,
                                          Model.brand_id == car.brand_id).first()
    if not brands_model:
        raise HTTPException(status_code=404, detail='Brand or model does not match')

    car_db = Car(**car.dict())
    db.add(car_db)
    db.commit()
    db.refresh(car_db)
    return car_db


@car_router.get('/')
async def car_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 3):
    cars_query = db.query(Car).offset(skip).limit(limit).all()

    car_list = []
    for car in cars_query:
        image = db.query(CarImage).filter(CarImage.car_id == car.id).all()
        car_list.append({
            'id': car.id,
            'brand_id': car.brand_id,
            'model_id': car.model_id,
            'description': car.description,
            'fuel_type': car.fuel_type,
            'transmission': car.transmission,
            'mileage': car.mileage,
            'price': car.price,
            'seller_id': car.seller_id,
            'image_url': [{"image": i.car_image} for i in image] if image else None
        })

    return {
        'total': db.query(Car).count(),
        'skip': skip,
        'limit': limit,
        'cars': car_list
    }
    # return db.query(Car).offset(skip).limit(limit).all()


@car_router.get('/{car_id}/', response_model=CarGetSchema)
async def car_detail(car_id: int, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id == car_id).first()
    if not car_db:
        raise HTTPException(status_code=404, detail='Car not found')

    images = db.query(CarImage).filter(CarImage.car_id == car_id).all()
    return {
        'id': car_db.id,
        'brand_id': car_db.brand_id,
        'model_id': car_db.model_id,
        'description': car_db.description,
        'fuel_type': car_db.fuel_type,
        'transmission': car_db.transmission,
        'mileage': car_db.mileage,
        'price': car_db.price,
        'seller_id': car_db.seller_id,
        'image_url': images,
    }


@car_router.put('/{car_id}/', response_model=CarSchema)
async def car_update(car_id: int, car: CarSchema, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id == car_id).first()
    if not car_db:
        raise HTTPException(status_code=404, detail='Car not found')

    brand_model = db.query(Model).filter(Model.id == car_db.model_id,
                                         Model.brand_id == car_db.brand_id).first()
    if not brand_model:
        raise HTTPException(status_code=404, detail='Brand or model does not match')

    seller_db = db.query(UserProfile).filter(UserProfile.id == car_db.seller_id).first()
    if not seller_db:
        raise HTTPException(status_code=404, detail='Seller not found')

    for car_key, car_value in car.dict().items():
        setattr(car_db, car_key, car_value)

    db.add(car_db)
    db.commit()
    db.refresh(car_db)
    return car_db


@car_router.delete('/{car_id}/')
async def car_delete(car_id: int, db: Session = Depends(get_db)):
    car_db = db.query(Car).filter(Car.id == car_id).first()
    if not car_db:
        raise HTTPException(status_code=404, detail='Car not found')

    db.delete(car_db)
    db.commit()
    return {'message': 'Deleted'}
