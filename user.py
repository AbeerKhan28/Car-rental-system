from person import Person

class User(Person):
    def __init__(self, username, password, first_name, last_name, address, balance):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.balance = balance
        self.rented_car = None
        self.rental_history = []

    def display_info(self):
        print(f"User: {self.first_name} {self.last_name}, Balance: Rs.{self.balance}")

    def __add__(self, amount):
        self.balance += amount
        return self
