from flask import render_template, request, redirect, url_for
from flask import session
from pyweb import app, dao, admin, login
from flask_login import login_user, logout_user
from pyweb.decorators import annonymous_user
from pyweb.models import UserRole


# import cloudinary.uploader
# import cloudinary


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/taodskham", methods=['get', 'post'])
def taodskham():
    date = request.args.get('date')
    patients = dao.load_patient(date)
    if request.method.__eq__('POST'):
        dao.create_medicalist(name=request.form.get('medicalexaminationday'))

    return render_template('taodskham.html',patients=patients)


@app.route("/dsbs")
def dsbs():
    return render_template('dsbs.html')


@app.route("/dklk", methods=['get', 'post'])
def dklk():
    err_msg = ''
    if request.method.__eq__('POST'):
        dao.add_patient_medicalist(
            patient_id=dao.add_patient(name=request.form.get('name'), dateofbirth=request.form.get('dateofbirth'),
                                       sex=request.form.get('sex'),
                                       phonenumber=request.form.get('phonenumber'),
                                       address=request.form.get('address'),
                                       identitycard=request.form.get('identitycard')),
            date=request.form.get('medicaday'))
        return render_template('index.html')

    return render_template('dklk.html')


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password,
                             email=request.form.get('email'))
                return redirect('/login')
            except Exception as ex:
                err_msg = "He thong dang co loi: " + str(ex)
        else:
            err_msg = 'Mật khẩu không khớp'
    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
@annonymous_user
def login_my_user():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get("next")
            return redirect(n if n else '/')
        else:
            err_msg = 'Username hoac password ko chinh xac!'
    return render_template("login.html", err_msg=err_msg)


# @annonymous_admin
@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.check_login(username=username, password=password)
    if user and user.user_role == UserRole.ADMIN:
        login_user(user=user)
    return redirect('/admin')


@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect('/')


@app.route("/logout")
def log_out():
    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)
