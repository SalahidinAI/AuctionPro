from auction_app.db.models import Feedback, UserProfile
from auction_app.db.schema import FeedbackSchema
from auction_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException


feedback_router = APIRouter(prefix='/feedback', tags=['Feedbacks'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@feedback_router.post('/', response_model=FeedbackSchema)
async def feedback_create(feedback: FeedbackSchema, db: Session = Depends(get_db)):
    seller_db = db.query(UserProfile).filter(UserProfile.id == feedback.seller_id).first()
    if not seller_db:
        raise HTTPException(status_code=404, detail='Seller not found')

    buyer_db = db.query(UserProfile).filter(UserProfile.id == feedback.buyer_id).first()
    if not buyer_db:
        raise HTTPException(status_code=404, detail='Buyer not found')

    feedback_db = Feedback(**feedback.dict())
    db.add(feedback_db)
    db.commit()
    db.refresh(feedback_db)
    return feedback_db


@feedback_router.get('/', response_model=List[FeedbackSchema])
async def feedback_list(db: Session = Depends(get_db)):
    return db.query(Feedback).all()


@feedback_router.get('/{feedback_id}/', response_model=FeedbackSchema)
async def feedback_detail(feedback_id: int, db: Session = Depends(get_db)):
    feedback_db = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback_db:
        raise HTTPException(status_code=404, detail='Feedback not found')
    return feedback_db


@feedback_router.delete('/{feedback_id}/')
async def feedback_delete(feedback_id: int, db: Session = Depends(get_db)):
    feedback_db = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback_db:
        raise HTTPException(status_code=404, detail='Feedback not found')

    db.delete(feedback_db)
    db.commit()
    return {'message': 'Deleted'}
