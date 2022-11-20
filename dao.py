from pyweb.models import User
from pyweb import db
import hashlib


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)

def register(name,username,password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u=User(name=name,username=username.strip(),password=password)
    db.session.add(u)
    db.session.commit()
