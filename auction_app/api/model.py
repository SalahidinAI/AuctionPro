from auction_app.db.models import Model, Car
from auction_app.db.schema import ModelSchema, ModelDetailSchema
from auction_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException


model_router = APIRouter(prefix='/model', tags=['Models'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@model_router.get('/', response_model=List[ModelSchema])
async def model_list(db: Session = Depends(get_db)):
    return db.query(Model).all()


@model_router.get('/{model_id}/', response_model=ModelDetailSchema)
async def model_detail(model_id: int, db: Session = Depends(get_db)):
    model_db = db.query(Model).filter(Model.id == model_id).first()
    if not model_db:
        raise HTTPException(status_code=404, detail='Model not found')

    cars_db = db.query(Car).filter(Car.model_id == model_id).all()
    return {
        'model_name': model_db.model_name,
        'model_cars': cars_db,
    }
