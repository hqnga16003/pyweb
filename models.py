import datetime
import hashlib

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from pyweb import db, app
from datetime import datetime
from enum import Enum as UserEnum
from enum import Enum as TypeEnum
from enum import Enum as Sex

from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    BACSI = 2
    YTA = 3
    THUNGAN = 4
    BENHNHAN = 5


class TypeMedicine(TypeEnum):
    VIEN = 1
    CHAI = 2
    VI = 3


class Sex(Sex):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    # avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.BENHNHAN)


class Category(BaseModel):
    name = Column(String(50), nullable=False)
    medicines = relationship('Medicine', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Medicine(BaseModel):
    name = Column(String(50), nullable=False)
    describe = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    type = Column(Enum(TypeMedicine), default=TypeMedicine.VI)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        import hashlib


        # password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        # u = User(name = 'admin',username='admin', password=password, user_role=UserRole.ADMIN, email="admin@gmail.com")
        # db.session.add(u)
        # db.session.commit()


    # c1 = Category(name='Đau dạ dày')
    # c2 = Category(name='Giảm sốt')
    # c3 = Category(name='Giảm đau bụng')
    # db.session.add_all([c1, c2, c3])
    # db.session.commit()

