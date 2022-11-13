from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
# thanh
#rep nga
app = Flask(__name__)
app.secret_key = '32342sdfsfsdfdsfsdf'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/flashweb?charset=utf8mb4' % quote('luonghuy2k2')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/flashweb?charset=utf8mb4' % quote('12345678')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

login = LoginManager(app=app)
