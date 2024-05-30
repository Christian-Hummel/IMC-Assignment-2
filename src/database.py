from flask_sqlalchemy import SQLAlchemy



# Initialize the database
db = SQLAlchemy()
# add database tables


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    manager_id = db.Column(db.Integer, db.ForeignKey('supervisor.employee_id'))

class Supervisor(db.Model):
    __tablename__ = "supervisor"
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable = False)
    address = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100),nullable = False, unique=True)
    salary = db.Column(db.Integer,nullable=False)
    nationality = db.Column(db.String(20),nullable=False)
    role = db.Column(db.String(20),nullable=False, default='supervisor')

    account = db.relationship('User', backref='Supervisor', uselist=False)
    teammembers = db.relationship('TravelAgent', backref='Supervisor')


class TravelAgent(db.Model):
    __tablename__ = "travel_agent"
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable = False)
    address = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100),nullable = False, unique=True)
    salary = db.Column(db.Integer,nullable=False)
    nationality = db.Column(db.String(20),nullable=False)
    role = db.Column(db.String(20),nullable=False, default='travelAgent')

    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.employee_id'), nullable=False)
    customers = db.relationship('Customer', backref='TravelAgent')



class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable = False)
    address = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100),nullable = False, unique = True)
    budget = db.Column(db.Integer, nullable = False)
    preference = db.Column(db.String(20), default='None')

    agent_id = db.Column(db.Integer, db.ForeignKey('travel_agent.employee_id'), nullable=False)




class Country(db.Model):
    __tablename__ = "country"
    country_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)

    activity = db.relationship('Activity', secondary='country_activity', back_populates='country')

class Activity(db.Model):
    __tablename__ = "activity"
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Integer,nullable = False)

    country = db.relationship('Country', secondary='country_activity', back_populates='activity')


#joined table

country_activity = db.Table(
    'country_activity',
    db.Column('country_id', db.Integer, db.ForeignKey('country.country_id')),
    db.Column('activity_id', db.Integer, db.ForeignKey('activity.activity_id'))
)
