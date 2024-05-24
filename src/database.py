from flask_sqlalchemy import SQLAlchemy



# Initialize the database
db = SQLAlchemy()
# add database tables

class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable = False)
    address = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100),nullable = False, unique=True)
    salary = db.Column(db.Integer,nullable=False)
    nationality = db.Column(db.String(20),nullable=False)
    role = db.Column(db.String(20),nullable=False, default="travelAgent")


class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable = False)
    address = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100),nullable = False, unique = True)
    budget = db.Column(db.Integer, nullable = False)
    preference = db.Column(db.String(20), default="None")


class Country(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)


class Activity(db.Model):
    activity_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Integer,nullable = False)