
import sqlite3
import json
from models import Customer

CUSTOMERS = [
    {
        "email": "doglover@gmail.com",
        "password": "ilovedogs",
        "name": "Marcus Aurelius",
        "id": 1
    },
    {
        "email": "billiswild@yahoo.com",
        "password": "dogsloveme",
        "name": "Wild Bill",
        "id": 2
    },
    {
        "email": "iamthelord@god.com",
        "password": "hellfire",
        "name": "Baby Jesus",
        "id": 3
    }
]


def get_all_customers():
    
    with sqlite3.connect("./kennel.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.name,
            a.address,
            a.email,
            a.password,
            a.id
        FROM customer a
        """)

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['name'], row['address'],
                                row['email'], row['password'], row['id'])

            customers.append(customer.__dict__)

    return json.dumps(customers)


def get_single_customer(id):

    with sqlite3.connect("./kennel.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.name,
            a.address,
            a.email,
            a.password,
            a.id
        FROM customer a
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        customer = Customer(data['name'], data['address'],
                            data['email'], data['password'], data['id'])

        return json.dumps(customer.__dict__)


def create_customer(customer):

    max_id = CUSTOMERS[-1]["id"]

    new_id = max_id + 1

    customer["id"] = new_id

    CUSTOMERS.append(customer)

    return customer


def delete_customer(id):

    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM customer
        WHERE id = ?
        """, (id, ))


def update_customer(id, new_customer):
   with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE customer
            SET
                name = ?,
                address = ?,
                email = ?,
                password = ?
        WHERE id = ?
        """, (new_customer['id'], new_customer['name'], 
              new_customer['address'], new_customer['email'], 
              new_customer['password'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            # Forces 404 response by main module
            return False
        else:
            # Forces 204 response by main module
            return True


def get_customers_by_email(email):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.name,
            c.address,
            c.email,
            c.password,
            c.id
        FROM Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['name'], row['address'], row['email'] , row['password'], row['id'])
            customers.append(customer.__dict__)

    return json.dumps(customers)

     # # # # PRE-SQL VERSION # # # #
    # def delete_customer(id):

    # customer_index = -1

    # for index, customer in enumerate(CUSTOMERS):
    #     if customer["id"] == id:

    #         customer_index = index

    # if customer_index >= 0:
    #     CUSTOMERS.pop(customer_index)