from flask import render_template, request, redirect, url_for
from flask import session
from pyweb import app, dao, admin, login,utils
from flask_login import login_user,logout_user
from pyweb.decorators import annonymous_user
from pyweb import utils


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/dklk")
def dklk():
    return render_template('dklk.html')

@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        # email = request.form.get('email')
        confirm = request.form.get('confirm')
    try:
        if password.strip().__eq__(confirm.strip()):
            utils.add_user(name=name,username=username,password=password,email=email)
            # nếu ko có lỗi sẽ trả về trang login
            return redirect(url_for('login.html'))
        else :
            err_msg = "Mat khau ko khop"

    except Exception as ex:
        err_msg = "He thong dang co loi: " + str(ex)

    # err_msg = ''
    # if request.method.__eq__('POST'):
    #     password = request.form['password']
    #     confirm = request.form['confirm']
    #     if password.__eq__(confirm):
    #        try:
    #            dao.register(name=request.form['name'],
    #                         username=request.form['username'],
    #                         password=password)
    #            return redirect('/login')
    #        except:
    #            err_msg='Hệ thống đang có lỗi'
    #
    #     else:
    #         err_msg = 'Mật khẩu không khớp'

    return render_template("register.html", err_msg=err_msg)



@app.route('/login',methods=['get', 'post'])
@annonymous_user
def login_my_user():
    # if request.method.__eq__('POST'):
    #     username=request.form['username']
    #     password=request.form['password']
    #
    #     user = dao.auth_user(username=username,password=password)
    #     if user:
    #         login_user(user=user)
    #         return redirect('/')

    return render_template("login.html")


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')
@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.route("/logout")
def log_out():
    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)
