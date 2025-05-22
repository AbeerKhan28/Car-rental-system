from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, username, password, first_name, last_name, address):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    @abstractmethod
    def display_info(self):
        pass
