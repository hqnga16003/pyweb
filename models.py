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
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.BENHNHAN)
    userinfo = relationship("UserInfo", uselist=False, backref="user")

class Nurse(BaseModel):

    medicalist = relationship('MedicaList', backref='nurse', lazy=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=True)
    user = relationship(User, uselist=False, backref="user")

class Doctor(BaseModel):

    medicalreport = relationship('MedicalReport', backref='doctor', lazy=True)
    user_id = Column(Integer, ForeignKey(User.id), unique=True)
    user = relationship(User, uselist=False, backref="user")




class Patient(BaseModel): #benh nhan
    name = Column(String(50), nullable=False)
    sex = Column(Enum(Sex), default=Sex.OTHER)
    dateofbirth = Column(DateTime)
    address = Column(String(50))
    phonenumber = Column(String(50))
    MedicaList = relationship("PatientMedicaList", backref="patient")






class UserInfo(BaseModel):
    lastname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    dateofbirth = Column(DateTime)
    sex = Column(Enum(Sex), default=Sex.OTHER)
    address = Column(String(50))
    phonenumber = Column(String(50))
    image = Column(String(100))
    user_id = Column(Integer, ForeignKey(User.id), unique=True)




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


class MedicaList(BaseModel): #danh sach kham
    name = Column(String(50), nullable=False)
    medicaday = Column(DateTime)
    nurse_id = Column(Integer, ForeignKey(Nurse.id), nullable=False)
    patient = relationship("PatientMedicaList", backref="medicaList")


class MedicalReport(BaseModel): #phieu kham
    patient_id = Column(ForeignKey(Patient.id), primary_key=True)
    medicalist = Column(ForeignKey(MedicaList.id), primary_key=True)
    symptom = Column(String(50))
    diseaseprediction = Column(String(50))
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)







if __name__ == '__main__':
    with app.app_context():
        import hashlib
        db.create_all()


        # benhnhan = Patient(name = "hoang quang nga1")
        # db.session.add(benhnhan)
        # db.session.commit()


        # dskham = MedicaList(name="danh sach 2", nurse_id=1)
        # db.session.add(dskham)
        # db.session.commit()






        # password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        # u = User(username='yta', password=password, user_role=UserRole.YTA, email="admin@gmail.com")
        # db.session.add(u)
        # db.session.commit()

            # info = UserInfo(lastname='yta', firstname="yta", user_id=2)
            # db.session.add(info)
            # db.session.commit()

        # yta = Nurse(user_id = 2)
        # db.session.add(yta)
        # db.session.commit()

    # c1 = Category(name='Đau dạ dày')
    # c2 = Category(name='Giảm sốt')
    # c3 = Category(name='Giảm đau bụng')
    # db.session.add_all([c1, c2, c3])
    # db.session.commit()
