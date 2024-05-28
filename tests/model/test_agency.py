import pytest



from src.database import Employee, Customer, Country, Activity, db



from tests.fixtures import app, client, agency


def test_add_supervisor(agency):
        before = Employee.query.count()

        new_supervisor = Employee(employee_id= 12, name="Terry Pratchett", address="Penny Lane 23, 1255 Liverpool",email="John.Grisham@hammertrips.com", salary=8000, nationality="England", role="supervisor")
        agency.add_supervisor(new_supervisor)

        supervisor = db.session.query(Employee).filter_by(employee_id = 12).first()


        assert Employee.query.count() == before + 1

        assert supervisor.employee_id == 12
        assert supervisor.name == "Terry Pratchett"
        assert supervisor.address == "Penny Lane 23, 1255 Liverpool"
        assert supervisor.email == "John.Grisham@hammertrips.com"
        assert supervisor.salary == 8000
        assert supervisor.nationality == "England"
        assert supervisor.role == "supervisor"



