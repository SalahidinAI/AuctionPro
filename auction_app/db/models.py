from .database import Base
from typing import Optional, List
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Enum, DECIMAL
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime
from enum import Enum as PyEnum
from passlib.hash import bcrypt


class RoleChoices(str, PyEnum):
    seller = 'seller'
    buyer = 'buyer'


class FuelChoices(str, PyEnum):
    benzine = 'benzine'
    electro = 'electro'
    gas = 'gas'


class TransmissionChoices(str, PyEnum):
    auto = 'auto'
    manually = 'manually'


class AuctionStatus(str, PyEnum):
    waiting = 'waiting'
    started = 'started'
    completed = 'completed'
    canceled = 'canceled'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(Enum(RoleChoices))
    date_registered: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cars: Mapped[List['Car']] = relationship('Car', back_populates='seller',
                                             cascade='all, delete-orphan')
    feedbacks: Mapped[List['Feedback']] = relationship('Feedback', back_populates='seller', foreign_keys='Feedback.seller_id',
                                                       cascade="all, delete-orphan")


def set_password(self, password: str):
    self.password = bcrypt.hash(password)


def check_password(self, password: str):
    return bcrypt.verify(password, self.password)


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped['UserProfile'] = relationship('UserProfile')


class Brand(Base):
    __tablename__ = 'brand'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand_name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)

    brand_cars: Mapped[List['Car']] = relationship('Car', back_populates='brand',
                                                   cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.brand_name}'


class Model(Base):
    __tablename__ = 'model'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'))

    brand: Mapped['Brand'] = relationship('Brand')
    model_cars: Mapped[List['Car']] = relationship('Car', back_populates='model',
                                                   cascade='all, delete-orphan')

    def __str__(self):
        return f'brand: {self.brand_id} model: {self.model_name}'


class Car(Base):
    __tablename__ = 'car'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'))
    model_id: Mapped[int] = mapped_column(ForeignKey('model.id'))
    description: Mapped[str] = mapped_column(Text)
    fuel_type: Mapped[FuelChoices] = mapped_column(Enum(FuelChoices))
    transmission: Mapped[TransmissionChoices] = mapped_column(Enum(TransmissionChoices))
    mileage: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    seller_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))

    brand: Mapped['Brand'] = relationship('Brand', back_populates='brand_cars')
    model: Mapped['Model'] = relationship('Model', back_populates='model_cars')
    image_url: Mapped[List['CarImage']] = relationship('CarImage', back_populates='car',
                                                        cascade='all, delete-orphan')
    seller: Mapped['UserProfile'] = relationship('UserProfile', back_populates='cars')
    auctions: Mapped[List['Auction']] = relationship('Auction', back_populates='car',
                                                     cascade='all, delete-orphan')


class CarImage(Base):
    __tablename__ = 'car_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    car_image: Mapped[str] = mapped_column(String, nullable=False)
    car_id: Mapped[int] = mapped_column(ForeignKey('car.id'))

    car: Mapped['Car'] = relationship('Car', back_populates='image_url')


class Auction(Base):
    __tablename__ = 'auction'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    car_id: Mapped[int] = mapped_column(ForeignKey('car.id'))
    start_price : Mapped[float] = mapped_column(DECIMAL(10, 2), default=0)
    min_price: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[AuctionStatus] = mapped_column(Enum(AuctionStatus), default=AuctionStatus.waiting.value)

    car: Mapped['Car'] = relationship('Car', back_populates='auctions')
    bids: Mapped[List['Bid']] = relationship('Bid', back_populates='auction',
                                             cascade='all, delete-orphan')


class Bid(Base):
    __tablename__ = 'bid'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    auction_id: Mapped[int] = mapped_column(ForeignKey('auction.id'))
    buyer_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    auction: Mapped['Auction'] = relationship('Auction', back_populates='bids')
    buyer: Mapped['UserProfile'] = relationship('UserProfile')


class Feedback(Base):
    __tablename__ = 'feedback'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    buyer_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    # add constraint  both can't be null
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    seller: Mapped['UserProfile'] = relationship('UserProfile', back_populates='feedbacks',
                                                 foreign_keys=[seller_id])
    buyer: Mapped['UserProfile'] = relationship('UserProfile', foreign_keys=[buyer_id])
