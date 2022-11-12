from pyweb.models import TaiKhoan
import hashlib


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username.strip()),
                             TaiKhoan.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return TaiKhoan.query.get(user_id)
