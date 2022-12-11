from flask import render_template, request, redirect, url_for, jsonify
from flask import session
from pyweb import app, dao, admin, login
from flask_login import login_user, logout_user
from pyweb.decorators import annonymous_user
from pyweb.models import UserRole
from twilio.rest import Client
import keys


# import cloudinary.uploader
# import cloudinary


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/taodanhsachkham', methods=['get', 'post'])
def tdsk():
    if request.method.__eq__('POST'):
        dao.create_medicalist(name=request.form.get('medicalexaminationday'))
    return render_template('taodanhsachkham.html')


@app.route("/xemdanhsachkham", methods=['get', 'post'])
def xemdanhsachkham():
    medicalists = dao.load_medicalist()
    medi_id = request.args.get('medicalist_id')
    patients = dao.load_patient(medi_id)

    return render_template('xemdanhsachkham.html', medicalists=medicalists, patients=patients)


@app.route('/phieukham', methods=['get', 'post'])
def phieukham():
    medicines = dao.load_medicines()
    p = dao.load_patient_in_patient_medicaList()
    patient_medicalist_id = request.args.get('patient_medicalist_id')
    if request.method.__eq__('POST'):
        dao.create_medical_report(symptom=request.form.get('trieuchung'),
                                  diseaseprediction=request.form.get('dudoanbenh'),
                                  patient_medicalist_id=patient_medicalist_id)

    return render_template('phieukham.html', p=p, medicines=medicines)


@app.route("/dsbs")
def dsbs():
    return render_template('dsbs.html')


@app.route("/dklk", methods=['get', 'post'])
def dklk():
    medicalists = dao.load_medicalist()
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

    return render_template('dklk.html', medicalists=medicalists)


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


@app.route('/login-cashier', methods=['post'])
def login_cashier():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.check_login(username=username, password=password)
    if user and user.user_role == UserRole.THUNGAN:
        login_user(user=user)
    return redirect('/cashier')


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


@app.route('/api/add-medicine', methods=['post'])
def add_medicine_to_medical_report():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    unit = data.get('unit')
    price = data.get('price')

    medical_report = session.get('medical_report')
    if not medical_report:
        medical_report = {}

    if id in medical_report:
        quantity = medical_report[id]['quantity'] = quantity = medical_report[id]['quantity'] + 1
    else:
        medical_report[id] = {
            'id': id,
            'name': name,
            'unit': unit,
            'quantity': 1,
            'price': price

        }

    session['medical_report'] = medical_report
    return jsonify(dao.count(medical_report))


if __name__ == "__main__":
    app.run(debug=True)
