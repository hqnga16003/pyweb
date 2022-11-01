from flask import render_template, request
from __init__ import app


@app.route("/")
def Hello():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
