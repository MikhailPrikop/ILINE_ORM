#!/usr/bin/env python

import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from database import db, Employee

import webbrowser
webbrowser.open('http://127.0.0.1:5000')

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", 'postgresql://postgres@localhost/postgres')

db.init_app(app)

### вызов всей таблицы с возможностью сортировки
@app.route("/")
def employees_list():
    #основной запрос
    query = Employee.query


    #поиск
    search_term = request.args.get('search', '').strip()
    if search_term:
        query = query.filter(Employee.full_name.ilike(f'%{search_term}%'))

    sort_field = request.args.get('sort','full_name')
    sort_order = request.args.get('order', 'asc')

    #поля сортировки
    valid_fields = ['id', 'full_name', 'position', 'date_employment', 'salary', 'manager']

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
        'employees.html', employees=query,
        sort_field=sort_field, sort_order=sort_order)

### Изменение начальника
@app.route("/employee/<int:id>/edit_manager", methods=['GET', 'POST'])
def edit_manager(id):
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        new_manager_id = request.form.get('manager_id')
        if new_manager_id:
            # проверка существования сотрудника
            manager = Employee.query.get(new_manager_id)
            if manager is None:
                return "Начальник не найден", 400
            if int(new_manager_id) == employee.id:
                return "Нельзя назначить начальником самого себя", 400
            employee.parent_id = new_manager_id
        else:
            employee.parent_id = None

        db.session.commit()
        return redirect(url_for('employees_list'))

    employees = Employee.query.filter(Employee.id != id).all()
    return render_template('edit_manager.html', employee=employee, employees=employees)

if __name__ == '__main__':
    app.run(debug=True)