from user import User

class Admin(User):
    def display_info(self):
        print(f"Admin: {self.first_name} {self.last_name}")
