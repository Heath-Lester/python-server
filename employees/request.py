
import sqlite3
import json
from models import Employee

EMPLOYEES = [
    {
        "name": "Jeremy Bakker",
        "locationId": 2,
        "animalId": 1,
        "id": 1
    },
    {
        "name": "Marge Thatcher",
        "locationId": 2,
        "animalId": 4,
        "id": 2
    },
    {
        "name": "Tommy Jefferson",
        "locationId": 1,
        "animalId": 3,
        "id": 3
    },
    {
        "name": "Rupert Murdok",
        "locationId": 1,
        "animalId": 2,
        "id": 4
    },
    {
        "name": "Melissa Garvy",
        "locationId": 1,
        "animalId": 1,
        "id": 5
    }
]


def get_all_employees():
    
    with sqlite3.connect("./kennel.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.location_id,
            a.animal_id
        FROM employee a
        """)

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'],
                                row['location_id'], row['animal_id'])

            employees.append(employee.__dict__)

    return json.dumps(employees)


def get_single_employee(id):

    with sqlite3.connect("./kennel.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.location_id,
            a.animal_id
        FROM employee a
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        employee = Employee(data['id'], data['name'], data['address'],
                            data['location_id'], data['animal_id'])

        return json.dumps(employee.__dict__)


def create_employee(employee):

    max_id = EMPLOYEES[-1]["id"]

    new_id = max_id + 1

    employee["id"] = new_id

    EMPLOYEES.append(employee)

    return employee


def delete_employee(id):

    employee_index = -1

    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:

            employee_index = index

        if employee_index >= 0:
            EMPLOYEES.pop(employee_index)


def update_empoloyee(id, new_employee):

    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index] = new_employee
            break


def get_employees_by_location(location_id):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        

        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.location_id,
            c.animal_id
        FROM Employee c
        WHERE c.location_id = ?
        """, ( location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'], 
                                row['location_id'], row['animal_id'])
            employees.append(employee.__dict__)

    return json.dumps(employees)