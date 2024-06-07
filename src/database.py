from flask_sqlalchemy import SQLAlchemy




# Initialize the database
db = SQLAlchemy()
# add database tables


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))

    manager_id = db.Column(db.Integer, db.ForeignKey('supervisor.employee_id'))

class Supervisor(db.Model):
    __tablename__ = "supervisor"
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    salary = db.Column(db.Integer,nullable=False)
    nationality = db.Column(db.String(20),nullable=False)
    role = db.Column(db.String(20),nullable=False, default='supervisor')

    account = db.relationship('User', backref='Supervisor', uselist=False)
    teammembers = db.relationship('TravelAgent', backref='Supervisor')


# joined table travelAgent and country

agent_country = db.Table(
    'agent_country',
    db.Column('country_id', db.Integer, db.ForeignKey('country.country_id')),
    db.Column('employee_id', db.Integer, db.ForeignKey('travel_agent.employee_id'))

)



class TravelAgent(db.Model):
    __tablename__ = "travel_agent"
    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    salary = db.Column(db.Integer,nullable=False)
    nationality = db.Column(db.String(20),nullable=False)
    role = db.Column(db.String(20),nullable=False, default='travelAgent')

    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.employee_id'), nullable=False)
    countries = db.relationship('Country', secondary='agent_country', back_populates='agents')
    customers = db.relationship('Customer', backref='TravelAgent')



class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    budget = db.Column(db.Integer, nullable=False)
    preference = db.Column(db.String(20), default='None')
    expert = db.Column(db.Boolean, unique=False, default=False)

    agent_id = db.Column(db.Integer, db.ForeignKey('travel_agent.employee_id'), nullable=False)

# joined table country and activity
country_activity = db.Table(
    'country_activity',
    db.Column('country_id', db.Integer, db.ForeignKey('country.country_id')),
    db.Column('activity_id', db.Integer, db.ForeignKey('activity.activity_id'))
)

class Country(db.Model):
    __tablename__ = "country"
    country_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    activities = db.relationship('Activity', secondary='country_activity', back_populates='countries')
    agents = db.relationship('TravelAgent', secondary='agent_country', back_populates='countries')

class Activity(db.Model):
    __tablename__ = "activity"
    activity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer,nullable=False)

    countries = db.relationship('Country', secondary='country_activity', back_populates='activities')


