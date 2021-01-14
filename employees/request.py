
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
    return EMPLOYEES


def get_single_employee(id):

    requested_location = None

    for employee in EMPLOYEES:

        if employee["id"] == id:
            requested_employee = employee

    return requested_employee


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
