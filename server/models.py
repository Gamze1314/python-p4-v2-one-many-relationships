# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hire_date = db.Column(db.Date)

    # add a relationship to the Employee model to reference a list of Review objects
    # 'employee' refers to the variable employee in Review model.
    reviews = db.relationship(
        'Review', back_populates="employee", cascade='all, delete-orphan')

    # Relationship mapping employee to related onboarding. set uselist=False => maps to a single related object rather than a list.(one to one)
    onboarding = db.relationship(
        'Onboarding', uselist=False, back_populates='employee', cascade='all, delete-orphan') # all-delete orphan for one -to-many.

    def __repr__(self):
        return f"<Employee {self.id}, {self.name}, {self.hire_date}>"


class Onboarding(db.Model):
    __tablename__ = "onboardings"

    id = db.Column(db.Integer, primary_key=True)
    orientation = db.Column(db.DateTime)
    forms_complete = db.Column(db.Boolean, default=False)

    # foreign key to store the employee id (3rd migration) => run flask db stamp head if it does not create a new migration script.
    # the name of the table onboarding belongs to. employees.id
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))

    # #Each employee has one onboarding, onboardings "belongs to" an employee. "belongs to" holds to foreign key.
    employee = db.relationship('Employee', back_populates='onboarding')

    def __repr__(self):
        return f"<Onboarding {self.id}, {self.orientation}, {self.forms_complete}>"


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    summary = db.Column(db.String)

    # one to many relationship between employee and review.
    # the name of the table review belongs to. employees.id
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"))
    # new column represent a schema change => new migration.

    # relationship mapping the review to related employee
    # one employee is being stored here.
    # bidirectional relationship ?
    employee = db.relationship("Employee", back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.id}, {self.year}, {self.summary}>"


# define relationships between 3 models.
