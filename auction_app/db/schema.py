from pydantic import BaseModel, Field, EmailStr
from .models import AuctionStatus, RoleChoices, FuelChoices, TransmissionChoices
from typing import Optional, List
from datetime import datetime


class UserProfileSchema(BaseModel):
    username: str
    first_name: str
    last_name: Optional[str]
    password: str
    email: EmailStr
    phone_number: Optional[str]
    profile_image: str
    role: RoleChoices

    class Config:
        from_attributes = True


class UserProfileGetSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    phone_number: Optional[str]
    profile_image: str
    role: RoleChoices

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class BrandSchema(BaseModel):
    id: int
    brand_name: str

    class Config:
        from_attributes = True


class ModelSchema(BaseModel):
    id: int
    model_name: str
    brand_id: int

    class Config:
        from_attributes = True


class CarSchema(BaseModel):
    brand_id: int
    model_id: int
    description: str
    fuel_type: FuelChoices
    transmission: TransmissionChoices
    mileage: int
    price: float
    seller_id: int

    class Config:
        from_attributes = True


class CarImageGetSchema(BaseModel):
    car_image: str

    class Config:
        from_attributes = True


class CarGetSchema(BaseModel):
    id: int
    brand_id: int
    model_id: int
    description: str
    fuel_type: FuelChoices
    transmission: TransmissionChoices
    mileage: int
    price: float
    seller_id: int
    image_url: List[CarImageGetSchema] = []

    class Config:
        from_attributes = True


class BrandDetailSchema(BaseModel):
    id: int
    brand_name: str
    brand_cars: List[CarSchema] = []

    class Config:
        from_attributes = True


class ModelDetailSchema(BaseModel):
    model_name: str
    model_cars: List[CarSchema] = []


class CarImageSchema(BaseModel):
    car_image: str
    car_id: int

    class Config:
        from_attributes = True


class AuctionSchema(BaseModel):
    car_id: int
    start_price: float
    min_price: Optional[int]
    start_time: datetime
    end_time: datetime
    status: AuctionStatus

    class Config:
        from_attributes = True


class AuctionGetSchema(BaseModel):
    id: int
    car_id: int
    start_price: float
    min_price: Optional[int]
    start_time: datetime
    end_time: datetime
    status: AuctionStatus

    class Config:
        from_attributes = True


class BidSchema(BaseModel):
    auction_id: int
    buyer_id: int
    amount: float
    created_date: datetime

    class Config:
        from_attributes = True


class FeedbackSchema(BaseModel):
    seller_id: int
    buyer_id: int
    rating: Optional[int] = Field(None, gt=0, lt=6)
    comment: str

    class Config:
        from_attributes = True
