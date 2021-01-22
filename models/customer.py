class Customer():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, name, address, email = "", password = "", id = ""):
        self.name = name
        self.address = address
        self.email = email
        self.password = password
        if id != "":
            self.id = id