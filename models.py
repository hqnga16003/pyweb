import datetime
import hashlib

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from pyweb import db, app
from datetime import datetime
from enum import Enum as UserEnum
from enum import Enum as TypeEnum
from enum import Enum as Sex

from flask_login import UserMixin


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    DOCTOR = 3
    NURSE = 4
    CASHIER = 5


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


class LoaiThuoc(BaseModel):
    __tablename__ = 'loaiThuoc'
    ten = Column(String(50), nullable=False)
    dsthuoc = relationship('Thuoc', backref='loaithuoc', lazy=True)

    def __str__(self):
        return self.ten


class Thuoc(BaseModel):
    ten = Column(String(50), nullable=False)
    mota = Column(Text)
    gia = Column(Float, default=0)
    anh = Column(String(100))
    active = Column(Boolean, default=True)
    donvi = Column(Enum(TypeMedicine), default=TypeMedicine.VI)
    id_loaithuoc = Column(Integer, ForeignKey(LoaiThuoc.id), nullable=False)

    def __str__(self):
        return self.ten


class BenhNhan(BaseModel):
    __tablename__ = 'benhnhan'
    ten = Column(String(50), nullable=False)
    gioitinh = Column(Enum(Sex), default=Sex.OTHER)
    namsinh = Column(DateTime, nullable=False)
    diachi = Column(Text)


class DanhSachKham(BaseModel):
    __tablename__ = 'danhsachkham'
    tends = Column(String(50), nullable=False)
    ngaykham = Column(DateTime)



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
        import hashlib

        # db.create_all()

        # date_time_str = '13-07-2022'
        # date_time_obj = datetime.strptime(date_time_str, "%d-%m-%Y")
        # a1 = DanhSachKham(tends="ds3", ngaykham=date_time_obj)
        # db.session.add_all([a1])
        # db.session.commit()

        # date_time_str = '11-07-2002'
        # date_time_obj = datetime.strptime(date_time_str, "%d-%m-%Y")
        # p1 = BenhNhan(ten='Hoang Quang Nga', gioitinh=Sex.MALE, namsinh=date_time_obj,
        #               diachi="Gò vấp Thành Phố HCM")
        # p2 = BenhNhan(ten='Luong Van Huy', gioitinh=Sex.MALE, namsinh=date_time_obj, diachi="Quận 9 Thành Phố HCM")
        # p3 = BenhNhan(ten='xxxxxxxx', gioitinh=Sex.OTHER, namsinh=date_time_obj, diachi="Gò vấp Thành Phố HCM")
        # db.session.add_all([p1, p2, p3])
        # db.session.commit()

        # password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        # u = User(name='nga', username='admin2', password=password,
        #          user_role=UserRole.ADMIN,
        #          image='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        # db.session.add(u)
        # db.session.commit()

    #  m1 = Thuoc(ten='thuoc 1', gia=20000, mota='****',
    #                 anh='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
    #                donvi = TypeMedicine.VI,id_loaithuoc=1)
    #  m2 = Thuoc(ten='thuoc 2', gia=20000, mota='****',
    #             anh='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
    #             donvi=TypeMedicine.VI, id_loaithuoc=2)
    #  m3 = Thuoc(ten='thuoc 3', gia=20000, mota='****',
    #             anh='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg',
    #             donvi=TypeMedicine.CHAI, id_loaithuoc=3)
    #
    #  db.session.add_all([m2,m3])
    #  db.session.commit()

    #  c1 = LoaiThuoc(ten='Đau dạ dày')
    #  c2 = LoaiThuoc(ten='Giảm sốt')
    #  c3 = LoaiThuoc(ten='Giảm đau bụng')
    #  db.session.add_all([c1, c2, c3])
    #  db.session.commit()

    # c = Category()
