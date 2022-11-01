from flask import render_template, request
from __init__ import app


@app.route("/index/")
def Hello():
    return render_template('index.html')

@app.route("/dsbs/")
def Bac_si():
    return render_template('dsbs.html')

if __name__ == "__main__":
    app.run(debug=True)
