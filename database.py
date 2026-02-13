from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship

db = SQLAlchemy()

#модель
class Employee(db.Model):
    __tablename__ = 'state_company'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    full_name = db.Column(db.String(200), nullable=True)
    position = db.Column(db.String(200), nullable=False)
    date_employment = db.Column(db.Date, nullable=True)
    salary = db.Column(db.Integer)
    parent_id = db.Column(db.Integer, db.ForeignKey('state_company.id'), nullable=True)

    # связка
    manager = db.relationship(
        'Employee', remote_side=[id],
        back_populates='subordinates', uselist=False)

    subordinates = db.relationship(
        'Employee', back_populates='manager')


    def __repr__(self):
        return f'<Employee {self.full_name} [{self.position}]>'
