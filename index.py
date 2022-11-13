from flask import render_template, request, redirect
from pyweb import app, dao, admin, login
from flask_login import login_user


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/dklk")
def dklk():
    return render_template("dklk.html")

@app.route("/dsbs")
def dsbs():
    return render_template("dsbs.html")

@app.route("/dangnhap")
def dangnhap():
    return render_template("dangnhap.html")

@app.route("/dn", methods = ["POST","GET"])
def dn():
    if request.method == "POST":
        user_name = request.form["name"]
        user_password = request.form["password"]

        if user_name:
            session["user"] = user_name
            session["password"] = user_password


            return redirect("/dk")
    return render_template("dn.html")

@app.route("/dk")
def dk():
    if "user"and"password" in session:
        name = session["user"]
        password = session["password"]
        return f"<h1>Đăng kí thành công!!</h1>"
    else:
        return redirect(url_for("dn"))

@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)
