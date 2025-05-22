class Car:
    def __init__(self, car_id, brand, model, seats, price_per_day):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.seats = seats
        self.price_per_day = price_per_day
        self.is_available = True

    def __str__(self):
        return f"[{self.car_id}] {self.brand} {self.model}, Seats: {self.seats}, Rs.{self.price_per_day}/day, Available: {self.is_available}"
