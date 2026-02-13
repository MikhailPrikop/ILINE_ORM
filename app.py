#!/usr/bin/env python

import os
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from database import db, Employee

import webbrowser
webbrowser.open('http://127.0.0.1:5000')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", 'postgresql://postgres@localhost/postgres')

db.init_app(app)

@app.route("/")
def all_employees():
    employees = Employee.query.all()
    return render_template("employess.html", employees=employees)

if __name__ == '__main__':
    app.run(debug=True)