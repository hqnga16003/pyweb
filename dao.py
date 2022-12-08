from datetime import datetime

from flask_login import current_user

from pyweb.models import User, Patient, MedicaList, Patient_MedicaList,Category,Medicine
from pyweb import db
from sqlalchemy import or_
import hashlib  # để băm


def load_medicalist():
    return MedicaList.query.all()

def load_categories():
    return Category.query.all()

def load_medicines(cate_id=None, kw=None):
    query = Medicine.query

    if cate_id:
        query = query.filter(Medicine.category_id.__eq__(cate_id))

    if kw:
        query = query.filter(Medicine.name.contains(kw))

    return query.all()

def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


# thêm user
def add_user(username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(
        username=username.strip(),
        password=password,
        email=kwargs.get('email'),
    )

    db.session.add(user)
    db.session.commit()


# thêm benh nhan
def add_patient(name, sex, dateofbirth, address, phonenumber, identitycard):
    patient = Patient.query.filter_by(identitycard=identitycard).first()

    if patient:
        return patient.id
    else:
        patient = Patient(name=name, sex=sex, dateofbirth=dateofbirth,
                          address=address, phonenumber=phonenumber, identitycard=identitycard)
        db.session.add(patient)
        db.session.commit()
        return patient.id


def create_medicalist(name):  # tao danh sach kham
    m = MedicaList(name=name, nurse_id=current_user.id)
    db.session.add(m)
    db.session.commit()


# thêm bệnh nhân-bac si
def add_patient_medicalist(date, patient_id):
    pm = Patient_MedicaList(patient_id=patient_id, medicalist_id=get_medicalist_by_date(date))
    db.session.add(pm)
    db.session.commit()


# lấy ds kham theo ngay
def get_medicalist_by_date(date):
    m = MedicaList.query.filter_by(name=date).first()
    return m.id


def load_patient(date=None):
    query = Patient.query
    if date:
        query = query.join(Patient_MedicaList, Patient.id == Patient_MedicaList.patient_id).filter(
            Patient_MedicaList.medicalist_id == date).all()

    return query


# lay benh nhan theo cccd
def get_patient_by_identityycard(identitycard):
    p = Patient.query.filter_by(identitycard='identitycard').first()
    return p


def get_date_now():  # lay id ngay hien tai
    date = datetime(2022, 1, 30).date().today()
    m = MedicaList.query.filter_by(name=date).first()
    return m.id

if __name__ == '__main__':
    from pyweb import app
    with app.app_context():
        print(load_medicines())

