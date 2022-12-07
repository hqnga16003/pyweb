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
    id = Column(Integer, primary_key=True, autoincrement=True)


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
    identitycard= Column(String(50),unique = True)
    patienthistory = relationship('PatientHistory', backref='patienthistory', uselist=False)
    receipt = relationship('Receipt', backref='patient', lazy=True)


class PatientHistory(BaseModel):  # lich su benh nhan
    kindofdisease = Column(String(100))
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False, unique=True)

class PatientRegulations(BaseModel): # quy dinh so benh nhan
    amount = Column(Integer, default=40)
    startday = Column(DateTime)
    endday = Column(DateTime)
    admin_id = Column(Integer, ForeignKey(User.id), nullable=False)
    medicalist = relationship('MedicaList', backref='patientregulations', lazy=True)

class MedicaList(BaseModel):  # danh sach kham
    name = Column((DateTime), nullable=False,unique = True)
    nurse_id = Column(Integer, ForeignKey(User.id), nullable=False)
    patientregulations_id = Column(Integer, ForeignKey(PatientRegulations.id)) #, nullable=False



class Patient_MedicaList(BaseModel):  # benh nhan_ danh sach benh nhan
    patient_id = Column(ForeignKey(Patient.id), primary_key=True)
    medicalist_id = Column(ForeignKey(MedicaList.id), primary_key=True)
    medicalreport = relationship('MedicalReport', backref='medicalreport', uselist=False)


class MedicalReport(BaseModel):  # phieu kham
    symptom = Column(String(50))
    diseaseprediction = Column(String(50))
    patient_medicalist_id = Column(ForeignKey(Patient_MedicaList.id), unique=True)
    doctor_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('DetailMedicalReport', backref='medicalreport', lazy=True)


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
    dateofmanufacture = Column(DateTime)
    expirydate = Column(DateTime)
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    unit_id = Column(Integer, ForeignKey(Unit.id), nullable=False)

    detail_medical_report = relationship('DetailMedicalReport', backref='medicine', lazy=True)
    def __str__(self):
        return self.name






class RegulationsMedicalExpenses(BaseModel): # quy dinh tien kham benh
    medicalexpenses = Column(Integer, default=100000)
    startday = Column(DateTime)
    endday = Column(DateTime)
    admin_id = Column(Integer, ForeignKey(User.id), nullable=False)
    receipt = relationship('Receipt', backref='regulationsmedicalexpenses', lazy=True)

class Receipt(BaseModel):  # hoa don
    medicinecash = Column(Integer)
    datecreated = Column(DateTime)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    detailmedicalreports = relationship('DetailMedicalReport', backref='receipt', lazy=True)
    cashier_id = Column(Integer, ForeignKey(User.id), nullable=False)
    regulationsmedicalexpenses_id = Column(Integer, ForeignKey(RegulationsMedicalExpenses.id), nullable=False)


class DetailMedicalReport(BaseModel):  # chi tiet phieu kham
    quantity = Column(Integer)
    unitprice = Column(Integer)
    medicalreport_id = Column(Integer, ForeignKey(MedicalReport.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    use = Column(String(100))
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)










if __name__ == '__main__':
    with app.app_context():
        import hashlib

        # db.create_all()


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

    # c1 = Category(name='Đau dạ dày')
    # c2 = Category(name='Giảm sốt')
    # c3 = Category(name='Giảm đau bụng')
    # db.session.add_all([c1, c2, c3])
    # db.session.commit()
