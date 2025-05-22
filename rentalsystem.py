from datetime import datetime
from user import User
from admin import Admin
from car import Car

class RentalSystem:
    def __init__(self):
        self.users = []
        self.cars = []
        self.admins = []

    def register_user(self, user):
            if any(u.username == user.username for u in self.users):
                raise Exception("Username already taken")
            self.users.append(user)

    def add_admin(self, admin):
        self.admins.append(admin)

    def add_car(self, car):
        self.cars.append(car)

    def remove_car(self, car_id):
        # Check if the car is rented by any user
        for user in self.users:
            if user.rented_car and user.rented_car.car_id == car_id:
                print("Cannot remove this car. It is currently rented by a user.")
                return False

        # If not rented, remove it
        self.cars = [car for car in self.cars if car.car_id != car_id]
        print(f"Car with ID {car_id} removed successfully.")
        return True

    def list_available_cars(self):
        print("Available Cars:")
        for car in self.cars:
            if car.is_available:
                print(car)

    def find_user(self, username, password):
        for user in self.users + self.admins:
            if user.username == username and user.password == password:
                return user
        raise Exception("Invalid login credentials")

    def rent_car(self, user, car_id, start_date, end_date):
        if user.rented_car:
            print("You already have a car rented.")
            return

        for car in self.cars:
            if car.car_id == car_id and car.is_available:
                days = (end_date - start_date).days
                total_cost = days * car.price_per_day
                if user.balance >= total_cost:
                    car.is_available = False
                    user.balance -= total_cost
                    user.rented_car = car
                    rental = {
                        'car': car,
                        'start_date': start_date,
                        'end_date': end_date,
                        'cost': total_cost
                    }
                    user.rental_history.append(rental)
                    print(f"Rental successful! Rs.{total_cost} deducted.")
                    return
                else:
                    print("Insufficient balance.")
                    return
        print("Car not available.")

    def return_car(self, user):
        if user.rented_car:
            user.rented_car.is_available = True
            user.rented_car = None
            print("Car returned successfully.")
        else:
            print("No car to return.")

    def print_user_report(self):
        for user in self.users:
            print(f"{user.first_name} {user.last_name} - {user.username}")
            for rental in user.rental_history:
                print(f"  Car: {rental['car'].brand} {rental['car'].model}, Rs.{rental['cost']}, From {rental['start_date']} To {rental['end_date']}")

    def print_reserved_cars(self):
        for car in self.cars:
            if not car.is_available:
                print(car)
