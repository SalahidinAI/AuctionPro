from sqladmin import ModelView
from auction_app.db.models import (UserProfile, Brand, Model,
                                   Car, CarImage, Auction, Bid, Feedback)


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.first_name, UserProfile.last_name, UserProfile.username]


class BrandAdmin(ModelView, model=Brand):
    column_list = [Brand.id, Brand.brand_name]


class ModelAdmin(ModelView, model=Model):
    column_list = [Model.id, Model.model_name, Model.brand_id]

