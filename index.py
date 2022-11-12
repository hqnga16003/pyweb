from flask import render_template, request, redirect
from pyweb import app, dao, admin, login
from flask_login import login_user


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@app.route()
def huy():
    pass

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)
