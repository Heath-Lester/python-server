
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
    return CUSTOMERS


def get_single_customer(id):

    requested_customer = None

    for customer in CUSTOMERS:

        if customer["id"] == id:
            requested_customer = customer

    return requested_customer


def create_customer(customer):

    max_id = CUSTOMERS[-1]["id"]

    new_id = max_id + 1

    customer["id"] = new_id

    CUSTOMERS.append(customer)

    return customer