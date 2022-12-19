from datetime import datetime

from flask_login import current_user

from pyweb.models import User, Patient, MedicaList, Patient_MedicaList, Category, Medicine, MedicalReport, Unit, \
    Receipt, DetailMedicalReport, PatientHistory
from pyweb import db
from sqlalchemy import or_, func
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
        pm = Patient_MedicaList(patient_id=patient_id, medicalist_id=date)
        db.session.add(pm)
        db.session.commit()



# lấy ds kham theo ngay
def get_medicalist_by_date(date):
    m = MedicaList.query.filter_by(name=date).first()
    if m:
        return m.id
    return None


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


def load_patient_in_patient_medicaList():
    date_id = get_date_now()

    query = db.session.query(Patient_MedicaList.id, Patient.id, Patient.name).join(Patient,
                                                                                   Patient.id == Patient_MedicaList.patient_id) \
        .filter(Patient_MedicaList.medicalist_id == date_id).all()

    # query = db.session.query(Patient_MedicaList.id,Patient.id,Patient.name).join(Patient.id==Patient_MedicaList.patient_id)\
    #     .filter(Patient_MedicaList.medicalist_id == date_id).all()

    return query


def create_medical_report(symptom, diseaseprediction, patient_medicalist_id):
    mr = MedicalReport(symptom=symptom, diseaseprediction=diseaseprediction,
                       patient_medicalist_id=patient_medicalist_id, doctor_id=current_user.id)
    db.session.add(mr)
    db.session.commit()


def save_DetailMedicalReport(medical_report, medicalreport_id, patient_id):
    # r = Receipt(cashier_id=current_user.id, patient_id=patient_id)
    # db.session.add(r)
    # db.session.commit()
    if medical_report:
        for c in medical_report.values():
            d = DetailMedicalReport(quantity=c['quantity'], unitprice=c['price']
                                    , medicalreport_id=medicalreport_id, medicine_id=c['id']
                                    )
            db.session.add(d)

        db.session.commit()


def lay_id_phieukham_by_id_benhnhan_dskham(patient_medicalist_id):
    id = MedicalReport.query.filter_by(patient_medicalist_id=patient_medicalist_id).first()
    return id.id


def tao_hoa_don(medicalreport_id, patient_id, medicinecash=0, medicalcash=100000):
    r = Receipt(medicalreport_id=medicalreport_id, medicinecash=medicinecash, medicalcash=medicalcash,
                cashier_id=current_user.id, patient_id=patient_id)
    db.session.add(r)
    db.session.commit()


def kiem_tra_danh_sach_kham(date):
    query = MedicaList.query.filter_by(name=date).first()
    return query


def tao_lich_su_benh_nhan(medicalreport_id, patient_id):
    p = PatientHistory(medicalreport_id=medicalreport_id, patient_id=patient_id)
    db.session.add(p)
    db.session.commit()


def load_lich_su_benh_nhan(benhnhan_id):
    query = db.session.query(MedicalReport) \
        .join(Patient_MedicaList, MedicalReport.patient_medicalist_id == Patient_MedicaList.id) \
        .join(Patient, Patient_MedicaList.patient_id == benhnhan_id).all()

    return query


def load_hoa_don(patient_medicalist_id):
    query = db.session.query(Patient.name, func.sum(DetailMedicalReport.unitprice * DetailMedicalReport.quantity)) \
        .join(MedicalReport, MedicalReport.patient_medicalist_id == patient_medicalist_id) \
        .join(DetailMedicalReport, DetailMedicalReport.medicalreport_id == MedicalReport.id).first()
    return query


def get_id_phieukham(patient_medicalist_id):
    query = MedicalReport.query.filter(MedicalReport.patient_medicalist_id == patient_medicalist_id).first()
    return query.id


def thanhtoan(patient_medicalist_id, patient_id):
    medicalreport_id = lay_id_phieukham_by_id_benhnhan_dskham(patient_medicalist_id)
    tao_hoa_don(medicalreport_id, patient_id, medicinecash=tinh_tien(medicalreport_id))


def tinh_tien(medicalreport_id):
    query = db.session.query(
        func.sum(DetailMedicalReport.unitprice * DetailMedicalReport.quantity)) \
        .filter(DetailMedicalReport.medicalreport_id == medicalreport_id).first()
    return query


def load_danh_sach_hoa_don():
    date_id = get_date_now()

    query = db.session.query(MedicalReport.id, Patient.name, Receipt.medicinecash, Receipt.medicalcash) \
        .join(Patient_MedicaList, Patient_MedicaList.id == MedicalReport.patient_medicalist_id) \
        .join(Patient, Patient.id == Patient_MedicaList.patient_id) \
        .join(Receipt, Receipt.medicalreport_id == MedicalReport.id) \
        .filter(Patient_MedicaList.medicalist_id == date_id).all()

    return query


def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(Medicine.id, Medicine.name, func.sum(DetailMedicalReport.quantity)) \
        .join(DetailMedicalReport, DetailMedicalReport.medicine_id.__eq__(Medicine.id)) \
        .join(MedicalReport, DetailMedicalReport.medicalreport_id.__eq__(MedicalReport.id))

    if kw:
        query = query.filter(Medicine.name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Medicine.id).order_by(-Medicine.id).all()


def baocaodoanhthu(input=None):
    from_date = None
    to_date = None
    query = db.session.query(MedicaList.name, func.count(MedicalReport.id),
                             func.sum(Receipt.medicalcash + Receipt.medicinecash)) \
        .join(Patient_MedicaList, MedicaList.id == Patient_MedicaList.medicalist_id) \
        .join(MedicalReport, MedicalReport.patient_medicalist_id == Patient_MedicaList.id) \
        .join(Receipt, Receipt.medicalreport_id == MedicalReport.id)

    return query.group_by(MedicaList.id).all()


def thongke(from_date=None, to_date=None):
    query = db.session.query(Medicine.id,Medicine.name,Unit.name,func.sum(DetailMedicalReport.quantity))\
        .join(Unit,Unit.id==Medicine.unit_id)\
        .join(DetailMedicalReport,DetailMedicalReport.medicine_id==Medicine.id)\
        .join(MedicalReport,MedicalReport.id==DetailMedicalReport.medicalreport_id)


    if from_date:
        query = query.filter(MedicalReport.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(MedicalReport.created_date.__le__(to_date))

    return   query.group_by(Medicine.id).all()



if __name__ == '__main__':
    from pyweb import app

    with app.app_context():
        print(thongke())
