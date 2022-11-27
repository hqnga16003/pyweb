from pyweb.models import User, Patient
from pyweb import db
import hashlib  # để băm


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


def add_patient(name, sex, dateofbirth, address, phonenumber, identitycard):
    patient = Patient(name=name, sex=sex, dateofbirth=dateofbirth,
                      address=address, phonenumber=phonenumber, identitycard=identitycard)
    db.session.add(patient)
    db.session.commit()
