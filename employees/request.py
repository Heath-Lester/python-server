
import sqlite3
import json
from models import Employee
from models import Location

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
            a.animal_id,
            l.name location_name,
            l.address location_address
        FROM employee a
        JOIN Location l
            ON l.id = a.location_id
        """)

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'],
                                row['location_id'], row['animal_id'])

            location = Location(row['location_name'], row['location_address'])

            employee.location = location.__dict__

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


def create_employee(new_employee):

    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            ( name, address, location_id, animal_id )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_employee['name'], new_employee['address'],
            new_employee['location_id'], new_employee['animal_id'] ))

        id = db_cursor.lastrowid

        new_employee['id'] = id

    return json.dumps(new_employee)


def delete_employee(id):

    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, (id, ))


def update_employee(id, new_employee):
   with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE employee
            SET
                name = ?,
                address = ?,
                location_id = ?,
                animal_id = ?
        WHERE id = ?
        """, (new_employee['id'], new_employee['name'], 
              new_employee['address'], new_employee['location_id'], 
              new_employee['animal_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            # Forces 404 response by main module
            return False
        else:
            # Forces 204 response by main module
            return True


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