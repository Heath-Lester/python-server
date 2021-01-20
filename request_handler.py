
from http.server import BaseHTTPRequestHandler, HTTPServer
from locations import get_all_locations, get_single_location, create_location, delete_location, update_location
from employees import get_all_employees, get_single_employee, create_employee, delete_employee, update_empoloyee, get_employees_by_location
from customers import get_all_customers, get_single_customer, create_customer, delete_customer, update_customer, get_customers_by_email
from animals import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, get_animals_by_location
import json


# Here's a class. It inherits from another class.
class HandleRequests(BaseHTTPRequestHandler):

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        
         # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )
        else:
            id = None

            # Try to get the item at index 2
            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)  # This is a tuple

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):

        self._set_headers(200)
        response = {}  # Default response

        print(self.path)

         # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Parse the URL and capture the tuple that is returned
        # (resource, id) = self.parse_url(self.path)

         # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)
            
            elif key == "location_id" and resource == "animals":
                response = get_animals_by_location(int(value))

            elif key == "location_id" and resource == "employees":
                response = get_employees_by_location(int(value))

        self.wfile.write(response.encode())

        ##### COMMENTED VERSION #####
        # Set the response code to 'Ok'
        # self._set_headers(200)

        # Your new console.log() that outputs to the terminal
        # print(self.path)

        # It's an if..else statement
        # if self.path == "/animals":
        # response = get_all_animals()
        # else:
        # response = []

        # This weird code sends a response back to the client
        # self.wfile.write(f"{response}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.

    def do_POST(self):
        # Set response code to 'Created'
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_employee = None
        new_customer = None
        new_location = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)

            # Encode the new animal and send in response
            self.wfile.write(f"{new_animal}".encode())

        if resource == "employees":
            new_employee = create_employee(post_body)

            self.wfile.write(f"{new_employee}".encode())

        if resource == "customers":
            new_customer = create_customer(post_body)

            self.wfile.write(f"{new_customer}".encode())

        if resource == "locations":
            new_location = create_location(post_body)

            self.wfile.write(f"{new_location}".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

        if resource == "customers":
            delete_customer(id)

        self.wfile.write("".encode())

        if resource == "employee":
            delete_employee(id)

        self.wfile.write("".encode())

        if resource == "location":
            delete_location(id)

        self.wfile.write("".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        self.do_POST()
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

        if resource == "customers":
            update_customer(id, post_body)

        self.wfile.write("".encode())

        if resource == "employees":
            update_empoloyee(id, post_body)

        self.wfile.write("".encode())

        if resource == "locations":
            update_location(id, post_body)

        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
