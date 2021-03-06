
import sqlite3
import json
from models import Location

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]


def get_all_locations():
    
    with sqlite3.connect("./kennel.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.name,
            a.address,
            a.id
        FROM location a
        """)

        locations = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            location = Location(row['name'], row['address'], row['id'])

            locations.append(location.__dict__)

    return json.dumps(locations)

def get_single_location(id):

    with sqlite3.connect("./kennel.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.name,
            a.address,
            a.id
        FROM location a
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        location = Location(data['name'], data['address'], data['id'])

        return json.dumps(location.__dict__)


def create_location(new_location):

    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Location
            ( name, address )
        VALUES
            ( ?, ?);
        """, (new_location['name'], new_location['address'] ))

        id = db_cursor.lastrowid

        new_location['id'] = id

    return json.dumps(new_location)


def delete_location(id):

    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM location
        WHERE id = ?
        """, (id, ))


def update_location(id, new_location):
   with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Location
            SET
                name = ?,
                address = ?
        WHERE id = ?
        """, (new_location['name'], new_location['address'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            # Forces 404 response by main module
            return False
        else:
            # Forces 204 response by main module
            return True

# def update_location(id, new_location):

#     for index, location in enumerate(LOCATIONS):
#         if location["id"] == id:
#             LOCATIONS[index] = new_location
#             break