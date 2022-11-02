import hashlib

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from pyweb import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


# class Category(BaseModel):
#     __tablename__ = 'category'
#
#     name = Column(String(50), nullable=False)
#     products = relationship('Product', backref='category', lazy=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Product(BaseModel):
#     name = Column(String(50), nullable=False)
#     description = Column(Text)
#     price = Column(Float, default=0)
#     image = Column(String(100))
#     active = Column(Boolean, default=True)
#     category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
#
#     def __str__(self):
#         return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    image = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        # c1 = Category(name='Điện thoại')
        # c2 = Category(name='Máy tính bảng')
        # c3 = Category(name='Phụ kiện')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()

        # p1 = Product(name='iPhone 13', price=27000000, description='Apple, 128GB',
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=1)
        # p2 = Product(name='iPhone 13 Pro Max', price=32000000, description='Apple, 512GB',
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg',
        #              category_id=1)
        # p3 = Product(name='iPPad Pro 2022', price=22000000, description='Apple, 128GB',
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=2)
        # p4 = Product(name='Galaxy Tab S8', price=24000000, description='Samsung, 128GB',
        #              image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
        #              category_id=2)

        import hashlib

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(name='nga', username='admin2', password=password,
                 user_role=UserRole.ADMIN,
                 image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        db.session.add(u)
        db.session.commit()
        # db.create_all()
