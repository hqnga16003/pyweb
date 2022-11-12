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


class TaiKhoan(BaseModel, UserMixin):
    __tablename__ = 'taikhoan'
    tentk = Column(String(50), nullable=False)
    matkhau = Column(String(50), nullable=False)
    hoatdong = Column(Boolean, default=True)


class NguoiDung(BaseModel):
    __tablename__ = 'nguoidung'
    ten = Column(String(50), nullable=False)
    ho = Column(String(50), nullable=False)
    gioitinh = Column(Enum(Sex), default=Sex.OTHER)
    namsinh = Column(Integer, nullable=False)
    diachi = Column(Text)
    image = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.BENHNHAN)
    id_taikhoan = Column(Integer, ForeignKey(TaiKhoan.id), unique=True)
    taikhoan = relationship("TaiKhoan", backref=backref("nguoidung", uselist=False))


class DanhSachKham(BaseModel):
    __tablename__ = 'danhsachkham'
    tends = Column(String(50), nullable=False)
    ngaykham = Column(DateTime)

    def __str__(self):
        return self.tends


# phieu_kham = db.Table('phieukham', Column('idbenhnhan', Integer, ForeignKey(NguoiDung.id), primary_key=True)
#                       , Column('iddanhsach', Integer, ForeignKey(DanhSachKham.id), primary_key=True))

# class BenhNhan(BaseModel):
#     __tablename__ = 'benhnhan'
#     id_nguoidung = Column(Integer, ForeignKey(NguoiDung.id),primary_key=True,unique=True, nullable=False)
#     benhnhan=relationship("NguoiDung",backref=backref("benhnhan", uselist=False))
#
# class Yta(BaseModel):
#     __tablename__ = 'yta'
#     id_nguoidung = Column(Integer, ForeignKey(NguoiDung.id),primary_key=True,unique=True, nullable=False)
#     yta=relationship("NguoiDung",backref=backref("yta", uselist=False))
#
# class BacSi(BaseModel):
#     __tablename__ = 'bacsi'
#     id_nguoidung = Column(Integer, ForeignKey(NguoiDung.id),primary_key=True,unique=True, nullable=False)
#     bacsi=relationship("NguoiDung",backref=backref("bacsi", uselist=False))


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




class HoaDon(BaseModel):
    tienkham = Column(Float)
    tongtien = Column(Float)
    id_benhnhan = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)


#
# class ChiTietPhieuKham(BaseModel):
#     __tablename__ = 'chitietphieukham'
#     id_phieukham = Column(Integer, ForeignKey(PhieuKham.id), primary_key=True, nullable=False)
#     id_thuoc = Column(Integer, ForeignKey(Thuoc.id), primary_key=True, nullable=False)
#     soluong = Column(Integer)
#     cachdung = Column(Text)
#     thanhTien = Column(Float)
#     id_hoadon = Column(Integer, ForeignKey(HoaDon.id), primary_key=True, nullable=False)
#
#


# def __str__(self):
#     return self.name

if __name__ == '__main__':
    with app.app_context():
        import hashlib


        #db.create_all()



# date_time_str = '11-07-2002'
# date_time_obj = datetime.strptime(date_time_str, "%d-%m-%Y")
# nd = NguoiDung(ten="*****", ho="***** ", gioitinh=Sex.MALE, namsinh=date_time_obj.year, diachi="*********",
#             user_role=UserRole.BENHNHAN,id_taikhoan=1)
# db.session.add(nd)
# db.session.commit()


# password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
# u = TaiKhoan(tentk='bacsi', matkhau=password)
# db.session.add(u)
# db.session.commit()

# db.create_all()

# yta1= BenhNhan(id_nguoidung=6)
# db.session.add(yta1)
# db.session.commit()



# date_time_str = '14-07-2022'
# date_time_obj = datetime.strptime(date_time_str, "%d-%m-%Y")
# a1 = DanhSachKham(tends="ds2", ngaykham=date_time_obj)
# db.session.add_all([a1])
# db.session.commit()

# bn1 = BenhNhan(id_nguoidung=3)
# db.session.add(bn1)
# db.session.commit()

# date_time_str = '11-07-2002'
# date_time_obj = datetime.strptime(date_time_str, "%d-%m-%Y")
# nd = NguoiDung(ten="quan", ho="hoang ", gioitinh=Sex.MALE, namsinh=date_time_obj.year, diachi="*********" )
# db.session.add(nd)
# db.session.commit()

#  date_time_str = '11-07-2002'
#  date_time_obj = datetime.strptime(date_time_str, "%d-%m-%Y")
#  p1 = BenhNhan(ten='Hoang Quang Nga', gioitinh=Sex.MALE, namsinh=date_time_obj.year,
#                diachi="Gò vấp Thành Phố HCM",id_taikhoan=2)
#

# p1 = PhieuKham(id_benhnhan=1, id_danhsachkham=1, trieuchung="Dau bung", dudoanbenh="dau bung")
# db.session.add_all([p1])
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
