#!/usr/bin/env python

import os
import threading
import webbrowser
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import aliased
from sqlalchemy import asc, desc
from database import db, Employee

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", 'postgresql://postgres@localhost/postgres')
db.init_app(app)

### основной запрос
@app.route("/")
def employees_list():
    query = Employee.query

    #поиск
    search_term = request.args.get('search', '').strip()
    if search_term:
        query = query.filter(Employee.full_name.ilike(f'%{search_term}%'))

    sort_field = request.args.get('sort', 'id')
    sort_order = request.args.get('order', 'asc')

    #cортировка
    valid_fields = ['id', 'full_name', 'position', 'date_employment', 'salary', 'manager']
    if sort_field not in valid_fields:
        sort_field = 'id'


    if sort_field == 'manager':
        manager_alias = aliased(Employee)
        query = query.outerjoin(manager_alias, Employee.manager)
        if sort_order == 'asc':
            query = query.order_by(asc(manager_alias.full_name))
        else:
            query = query.order_by(desc(manager_alias.full_name))
    else:
        column = getattr(Employee, sort_field)
        if sort_order == 'asc':
            query = query.order_by(asc(column))
        else:
            query = query.order_by(desc(column))

    employees = query.all()

    return render_template(
        'employees.html',
        employees=employees,
        sort_field=sort_field,
        sort_order=sort_order,
        search_term=search_term
    )
### выбор начальника
@app.route("/employee/<int:id>/edit_manager", methods=['GET', 'POST'])
def edit_manager(id):
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        new_manager_id = request.form.get('manager_id')
        if new_manager_id:
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

    #djpvj;yst yfxfkmybrb
    possible_managers = Employee.query.filter(Employee.id != id).all()
    return render_template('edit_manager.html', employee=employee, employees=possible_managers)

if __name__ == '__main__':
    # Открываем браузер через 1.25 секунды после запуска сервера
    threading.Timer(1.25, lambda: webbrowser.open('http://127.0.0.1:5000')).start()
    app.run(debug=True)