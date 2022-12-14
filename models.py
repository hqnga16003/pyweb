import datetime
import hashlib

from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from pyweb import db, app
from datetime import datetime
from enum import Enum as UserEnum
from enum import Enum as Sex
from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    BACSI = 2
    YTA = 3
    THUNGAN = 4
    NGUOIDUNG = 5


class Sex(Sex):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)  #id tự tăng


class User(BaseModel, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.NGUOIDUNG)
    userinfo = relationship("UserInfo", uselist=False, backref="user")


class UserInfo(BaseModel):
    lastname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    dateofbirth = Column(DateTime)
    sex = Column(Enum(Sex), default=Sex.OTHER)
    address = Column(String(50))
    phonenumber = Column(String(50))
    image = Column(String(100))
    user_id = Column(Integer, ForeignKey(User.id), unique=True)


class Patient(BaseModel):  # benh nhan
    name = Column(String(50), nullable=False)
    sex = Column(String(50))
    dateofbirth = Column(DateTime)
    address = Column(String(50))
    phonenumber = Column(String(50))
    identitycard = Column(String(50), unique=True)
    patienthistory = relationship('PatientHistory', backref='patient', lazy=True)
    receipts = relationship('Receipt', backref='patient', lazy=True)

class PatientRegulations(BaseModel):  # quy dinh so benh nhan
    amount = Column(Integer, default=40)
    startday = Column(DateTime)
    endday = Column(DateTime)
    admin_id = Column(Integer, ForeignKey(User.id), nullable=False)
    medicalist = relationship('MedicaList', backref='patientregulations', lazy=True)


class MedicaList(BaseModel):  # danh sach kham
    name = Column((DateTime), nullable=False, unique=True)
    nurse_id = Column(Integer, ForeignKey(User.id), nullable=False)
    patientregulations_id = Column(Integer, ForeignKey(PatientRegulations.id))  # , nullable=False


class Patient_MedicaList(BaseModel):  # benh nhan_ danh sach benh nhan
    patient_id = Column(ForeignKey(Patient.id), primary_key=True)
    medicalist_id = Column(ForeignKey(MedicaList.id), primary_key=True)
    medicalreport = relationship('MedicalReport', backref='medicalreport', uselist=False)


class MedicalReport(BaseModel):  # phieu kham
    symptom = Column(String(50))
    diseaseprediction = Column(String(50))
    created_date = Column(DateTime, default=datetime.now())
    patient_medicalist_id = Column(ForeignKey(Patient_MedicaList.id), unique=True)
    doctor_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('DetailMedicalReport', backref='medicalreport', lazy=True)
    receipt = relationship('Receipt', backref='receipt', uselist=False)
    patienthistorys = relationship('PatientHistory', backref='medicalreport', uselist=False)


class PatientHistory(BaseModel):  # lich su benh nhan
    medicalreport_id = Column(Integer, ForeignKey(MedicalReport.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)


class Category(BaseModel):
    name = Column(String(50), nullable=False)
    medicines = relationship('Medicine', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Unit(BaseModel):
    name = Column(String(50), nullable=False, unique=True)
    medicines = relationship('Medicine', backref='unit', lazy=True)

    def __str__(self):
        return self.name


class Medicine(BaseModel):
    name = Column(String(50), nullable=False)
    describe = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    unit_id = Column(Integer, ForeignKey(Unit.id), nullable=False)
    detail_medical_report = relationship('DetailMedicalReport', backref='medicine', lazy=True)

    def __str__(self):
        return self.name


class RegulationsMedicalExpenses(BaseModel):  # quy dinh tien kham benh
    medicalexpenses = Column(Integer, default=100000)
    startday = Column(DateTime)
    endday = Column(DateTime)
    admin_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt = relationship('Receipt', backref='regulationsmedicalexpenses', lazy=True)


class Receipt(BaseModel):  # hoa don

    created_date = Column(DateTime, default=datetime.now())
    medicinecash = Column(Integer)
    medicalcash = Column(Integer)
    medicalreport_id = Column(ForeignKey(MedicalReport.id), unique=True)
    cashier_id = Column(Integer, ForeignKey(User.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    regulationsmedicalexpenses_id = Column(Integer, ForeignKey(RegulationsMedicalExpenses.id))

class DetailMedicalReport(BaseModel):  # chi tiet phieu kham
    quantity = Column(Integer)
    unitprice = Column(Integer)
    medicalreport_id = Column(Integer, ForeignKey(MedicalReport.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    use = Column(String(100))


if __name__ == '__main__':
    with app.app_context():
        import hashlib

        #db.create_all()

    # dskham = MedicaList(name="danh sach 2", nurse_id=1)
    # db.session.add(dskham)
    # db.session.commit()

        password = str(hashlib.md5('1'.encode('utf-8')).hexdigest())
        u = User(username='admin', password=password, user_role=UserRole.ADMIN, email="admin@gmail.com")
        db.session.add(u)
        db.session.commit()

    # info = UserInfo(lastname='yta', firstname="yta", user_id=2)
    # db.session.add(info)
    # db.session.commit()

    # yta = Nurse(user_id = 2)
    # db.session.add(yta)
    # db.session.commit()

    # c1 = Category(name='Loại Thuốc 1')
    # c2 = Category(name='Loại Thuốc 2')
    # db.session.add_all([c1, c2])
    # db.session.commit()
