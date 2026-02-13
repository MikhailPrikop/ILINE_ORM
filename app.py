#!/usr/bin/env python

import os
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from database import db, Employee

import webbrowser
webbrowser.open('http://127.0.0.1:5000')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", 'postgresql://postgres@localhost/postgres')

db.init_app(app)

### вызов сей таблицы с возможностью сортировки
@app.route("/")
def all_employees():
    #основной запрос
    query = Employee.query

    sort_field = request.args.get('sort','full_name')
    sort_order = request.args.get('order', 'asc')

    #поля сортировки
    valid_fields = ['id', 'full_name', 'position', 'date_employment', 'salary']

    if sort_field not in valid_fields:
        sort_field = 'full_name'
    #выбор колонки сортировки
    order_col = getattr(Employee, sort_field)

    #направление сортировки
    if sort_order == 'desc':
        order_col = order_col.desc()
    else:
        order_col = order_col.asc()

    query = query.order_by(order_col)
    employees = query.all()

    return render_template(
        'employees.html', employees=employees,
        sort_field=sort_field, sort_order=sort_order)

if __name__ == '__main__':
    app.run(debug=True)