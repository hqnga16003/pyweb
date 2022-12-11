from datetime import datetime

from flask_login import current_user

from pyweb.models import User, Patient, MedicaList, Patient_MedicaList, Category, Medicine, MedicalReport, Unit
from pyweb import db
from sqlalchemy import or_
import hashlib  # để băm


def load_medicalist():
    return MedicaList.query.all()


def load_categories():
    return Category.query.all()


def load_medical_report(medicalist_id):
    query = MedicalReport.query
    query = query.filter(MedicalReport.id.__eq__(medicalist_id))


def load_unit():
    return Unit.query.all()


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


# lay benh nhan theo cccd
def get_patient_by_identityycard(identitycard):
    p = Patient.query.filter_by(identitycard='identitycard').first()
    return p


def get_date_now():  # lay id ngay hien tai
    date = datetime(2022, 1, 30).date().today()
    m = MedicaList.query.filter_by(name=date).first()
    return m.id


def get_id_patient_medica_list():  # lay id ngay hien tai
    date = get_date_now()
    m = Patient_MedicaList.query.filter_by(medicalist_id=date).all()
    return m


def lay_ten_benh_nhan(danhsachkham_benhnhan_id):
    query = Patient.query.join(Patient_MedicaList, Patient.id == Patient_MedicaList.patient_id).filter(
        Patient_MedicaList.id == danhsachkham_benhnhan_id).first()
    return query.name


def load_patient(date=None, patient_medicaList_id=None):
    query = Patient.query
    if date:
        query = query.join(Patient_MedicaList, Patient.id == Patient_MedicaList.patient_id).filter(
            Patient_MedicaList.medicalist_id == date).all()

    if patient_medicaList_id:
        query = query.join(Patient_MedicaList, Patient.id == Patient_MedicaList.patient_id).filter(
            Patient_MedicaList.medicalist_id == patient_medicaList_id).all()
    return query


def load_medicines(cate_id=None, kw=None):
    query = Medicine.query

    if cate_id:
        query = query.filter(Medicine.category_id.__eq__(cate_id))

    if kw:
        query = query.filter(Medicine.name.contains(kw))

    return query.all()


def test():
    query = db.session.query(Medicine.name, Unit.name).join(Unit, Medicine.unit_id == Unit.id)
    query = query.group_by(Medicine.name, Unit.name).all()
    return query


def load_patient_in_patient_medicaList():
    date_id = get_date_now()

    query = db.session.query(Patient_MedicaList.id, Patient.name).join(Patient,
                                                                       Patient.id == Patient_MedicaList.patient_id) \
        .filter(Patient_MedicaList.medicalist_id == date_id).all()

    # query = query.group_by(Patient_MedicaList.id, Patient.name).all()

    return query


def create_medical_report(symptom, diseaseprediction, patient_medicalist_id):
    mr = MedicalReport(symptom=symptom, diseaseprediction=diseaseprediction,
                       patient_medicalist_id=patient_medicalist_id, doctor_id=current_user.id)
    db.session.add(mr)
    db.session.commit()


def count(medicinerepost):
    total_quantity, total_amount = 0, 0

    if medicinerepost:
        for c in medicinerepost.values():
            total_quantity += c['total_quantity']
            total_amount += c['total_quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }


if __name__ == '__main__':
    from pyweb import app

    with app.app_context():
        print(load_patient(2))
