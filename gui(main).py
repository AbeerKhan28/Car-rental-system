import tkinter as tk
from tkinter import messagebox
from rentalsystem import RentalSystem
from user import User
from admin import Admin
from car import Car
from datetime import datetime

# Centering function
def center_window(window, width=400, height=300):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# System Setup
system = RentalSystem()
admin_user = Admin("admin", "admin123", "Ali", "Raza", "Karachi", 0)
system.add_admin(admin_user)

system.add_car(Car(1, "Toyota", "Corolla", 5, 3000))
system.add_car(Car(2, "Suzuki", "Cultus", 4, 2500))
system.add_car(Car(3, "Honda", "Civic", 5, 3500))
system.add_car(Car(4, "Ford", "Explorer", 4, 2000))
system.add_car(Car(5, "Hyundai", "Sonata", 5, 2500))
system.add_car(Car(6, "Kia", "City", 5, 2000))
system.add_car(Car(7, "Nissan", "Altima", 5, 3000))
system.add_car(Car(8, "Mercedes", "C-Class", 4, 4000))


# Root window
root = tk.Tk()
root.title("Car Rental System")
center_window(root, 400, 300)

def register_user():
        def submit():
            uname = entry_username.get()
            pwd = entry_password.get()
            fname = entry_fname.get()
            lname = entry_lname.get()
            addr = entry_address.get()
            try:
                balance = int(entry_balance.get())
            except:
                messagebox.showerror("Error", "Invalid balance")
                return

            user = User(uname, pwd, fname, lname, addr, balance)
            system.register_user(user)
            messagebox.showinfo("Success", "User registered successfully!")
            register_window.destroy()

        register_window = tk.Toplevel(root)
        register_window.title("Register")
        center_window(register_window, 400, 400)

        tk.Label(register_window, text="Username").pack()
        entry_username = tk.Entry(register_window)
        entry_username.pack()

        tk.Label(register_window, text="Password").pack()
        entry_password = tk.Entry(register_window, show="*")
        entry_password.pack()

        tk.Label(register_window, text="First Name").pack()
        entry_fname = tk.Entry(register_window)
        entry_fname.pack()

        tk.Label(register_window, text="Last Name").pack()
        entry_lname = tk.Entry(register_window)
        entry_lname.pack()

        tk.Label(register_window, text="Address").pack()
        entry_address = tk.Entry(register_window)
        entry_address.pack()

        tk.Label(register_window, text="Balance").pack()
        entry_balance = tk.Entry(register_window)
        entry_balance.pack()

        tk.Button(register_window, text="Submit", command=submit).pack(pady=10)


def login_user():
    def submit_login():
        uname = entry_uname.get()
        pwd = entry_pwd.get()
        try:
            user = system.find_user(uname, pwd)
            messagebox.showinfo("Success", f"Welcome, {user.first_name}!")
            login_window.destroy()
            open_dashboard(user)
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    center_window(login_window, 350, 250)

    tk.Label(login_window, text="Username").pack()
    entry_uname = tk.Entry(login_window)
    entry_uname.pack()

    tk.Label(login_window, text="Password").pack()
    entry_pwd = tk.Entry(login_window, show="*")
    entry_pwd.pack()

    tk.Button(login_window, text="Login", command=submit_login).pack(pady=10)

def open_dashboard(user):
    dash = tk.Toplevel(root)
    dash.title("Dashboard")
    center_window(dash, 400, 350)

    balance_var = tk.StringVar()
    balance_var.set(f"Hello {user.first_name}, Balance: Rs.{user.balance}")
    tk.Label(dash, textvariable=balance_var).pack(pady=10)

    tk.Button(dash, text="View Available Cars", command=lambda: view_available(user)).pack(pady=5)
    tk.Button(dash, text="View Rental History", command=lambda: view_history(user)).pack(pady=5)
    tk.Button(dash, text="Return Car", command=lambda: return_car(user)).pack(pady=5)
    tk.Button(dash, text="Rent a Car", command=lambda: rent_car(user, balance_var)).pack(pady=5)
    tk.Button(dash, text="Add Balance", command=lambda: add_balance(user, balance_var)).pack(pady=5)

def view_available(user):
    top = tk.Toplevel(root)
    top.title("Available Cars")
    center_window(top, 450, 400)

    for car in system.cars:
        if car.is_available:
            tk.Label(top, text=str(car)).pack()

def rent_car(user, balance_var):
    rent_win = tk.Toplevel(root)
    rent_win.title("Rent a Car")
    center_window(rent_win, 400, 400)

    tk.Label(rent_win, text="Select Car:").pack()
    car_options = [car for car in system.cars if car.is_available]
    car_var = tk.StringVar(rent_win)
    car_var.set("Select a car")

    car_map = {}
    for car in car_options:
        label = f"{car.car_id} - {car.brand} {car.model} - Rs.{car.price_per_day}/day"
        car_map[label] = car

    dropdown = tk.OptionMenu(rent_win, car_var, *car_map.keys())
    dropdown.pack(pady=5)

    tk.Label(rent_win, text="Start Date (YYYY-MM-DD):").pack()
    entry_start = tk.Entry(rent_win)
    entry_start.pack()

    tk.Label(rent_win, text="End Date (YYYY-MM-DD):").pack()
    entry_end = tk.Entry(rent_win)
    entry_end.pack()

    def confirm_rent():
        try:
            selected_car_label = car_var.get()
            if selected_car_label not in car_map:
                messagebox.showerror("Error", "Please select a valid car.")
                return

            car = car_map[selected_car_label]
            start = datetime.strptime(entry_start.get(), "%Y-%m-%d")
            end = datetime.strptime(entry_end.get(), "%Y-%m-%d")

            if end <= start:
                messagebox.showerror("Error", "End date must be after start date.")
                return

            days = (end - start).days
            total_cost = days * car.price_per_day

            if user.balance < total_cost:
                messagebox.showerror("Error", "Insufficient balance.")
                return

            if user.rented_car:
                messagebox.showerror("Error", "You already rented a car.")
                return

            car.is_available = False
            user.balance -= total_cost
            user.rented_car = car
            user.rental_history.append({
                'car': car,
                'start_date': start,
                'end_date': end,
                'cost': total_cost
            })
            balance_var.set(f"Hello {user.first_name}, Balance: Rs.{user.balance}")
            messagebox.showinfo("Success", f"Car rented successfully!\nRs.{total_cost} deducted.")
            rent_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(rent_win, text="Confirm Rental", command=confirm_rent).pack(pady=10)

def add_balance(user, balance_var):
    top = tk.Toplevel(root)
    top.title("Add Balance")
    center_window(top, 300, 200)

    tk.Label(top, text="Enter amount to add:").pack()
    entry = tk.Entry(top)
    entry.pack()

    def confirm_add():
        try:
            amount = int(entry.get())
            if amount <= 0:
                raise ValueError
            user.balance += amount
            balance_var.set(f"Hello {user.first_name}, Balance: Rs.{user.balance}")
            messagebox.showinfo("Success", f"Rs.{amount} added successfully.")
            top.destroy()
        except:
            messagebox.showerror("Error", "Please enter a valid positive number.")

    tk.Button(top, text="Add", command=confirm_add).pack(pady=5)

def view_history(user):
    top = tk.Toplevel(root)
    top.title("Rental History")
    center_window(top, 450, 350)

    for rental in user.rental_history:
        tk.Label(top, text=f"{rental['car'].brand} from {rental['start_date']} to {rental['end_date']} - Rs.{rental['cost']}").pack()

def admin_login():
    win = tk.Toplevel(root)
    win.title("Admin Login")
    center_window(win, 350, 250)

    tk.Label(win, text="Username").pack()
    entry_user = tk.Entry(win)
    entry_user.pack()

    tk.Label(win, text="Password").pack()
    entry_pass = tk.Entry(win, show="*")
    entry_pass.pack()

    def submit():
        uname = entry_user.get()
        pwd = entry_pass.get()
        try:
            admin = system.find_user(uname, pwd)
            if not isinstance(admin, Admin):
                raise Exception("Not an admin")
            messagebox.showinfo("Login Successful", f"Welcome, {admin.first_name}")
            win.destroy()
            open_admin_dashboard(admin)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(win, text="Login", command=submit).pack(pady=10)

def open_admin_dashboard(admin):
    dash = tk.Toplevel(root)
    dash.title("Admin Dashboard")
    center_window(dash, 400, 350)

    tk.Label(dash, text=f"Admin: {admin.first_name} {admin.last_name}").pack(pady=10)
    tk.Button(dash, text="Add New Car", command=add_new_car).pack(pady=5)
    tk.Button(dash, text="Remove Car", command=remove_car).pack(pady=5)
    tk.Button(dash, text="View All Users & Rentals", command=view_all_users).pack(pady=5)
    tk.Button(dash, text="View Reserved Cars", command=view_reserved_cars).pack(pady=5)

def add_new_car():
    win = tk.Toplevel(root)
    win.title("Add New Car")
    center_window(win, 400, 400)

    labels = ["Car ID", "Brand", "Model", "Seating Capacity", "Price per Day (Rs.)"]
    entries = []

    for label in labels:
        tk.Label(win, text=label).pack()
        entry = tk.Entry(win)
        entry.pack()
        entries.append(entry)

    def submit_car():
        try:
            car_id = int(entries[0].get())
            brand = entries[1].get()
            model = entries[2].get()
            seats = int(entries[3].get())
            price = int(entries[4].get())

            new_car = Car(car_id, brand, model, seats, price)
            system.add_car(new_car)
            messagebox.showinfo("Success", "Car added successfully.")
            win.destroy()
        except:
            messagebox.showerror("Error", "Please enter valid details.")

    tk.Button(win, text="Add Car", command=submit_car).pack(pady=10)

def remove_car():
    win = tk.Toplevel(root)
    win.title("Remove Car")
    center_window(win, 400, 250)

    tk.Label(win, text="Select Car to Remove:").pack()
    available_cars = system.cars
    if not available_cars:
        tk.Label(win, text="No cars in the system.").pack()
        return

    car_map = {}
    for car in available_cars:
        label = f"{car.car_id} - {car.brand} {car.model}"
        car_map[label] = car.car_id

    car_var = tk.StringVar(win)
    car_var.set("Select a car")
    dropdown = tk.OptionMenu(win, car_var, *car_map.keys())
    dropdown.pack(pady=5)

    def confirm_remove():
            selected = car_var.get()
            if selected not in car_map:
                messagebox.showerror("Error", "Please select a valid car.")
                return

            car_id = car_map[selected]
            success = system.remove_car(car_id)  # Get True/False from method

            if success:
                messagebox.showinfo("Removed", f"Car ID {car_id} has been removed.")
                win.destroy()
            else:
                messagebox.showwarning("Failed", f"Car ID {car_id} is currently rented and cannot be removed.")

    tk.Button(win, text="Remove", command=confirm_remove).pack(pady=10)

def view_all_users():
    win = tk.Toplevel(root)
    win.title("All Users & Rental History")
    center_window(win, 600, 450)

    if not system.users:
        tk.Label(win, text="No users registered yet.").pack()
        return

    for user in system.users:
        user_info = f"{user.first_name} {user.last_name} ({user.username}) - Balance: Rs.{user.balance}"
        tk.Label(win, text=user_info, font=("Arial", 10, "bold")).pack(anchor='w', padx=10, pady=2)
        if user.rental_history:
            for rental in user.rental_history:
                rental_info = (
                    f"  Car: {rental['car'].brand} {rental['car'].model} | "
                    f"From: {rental['start_date'].strftime('%Y-%m-%d')} To: {rental['end_date'].strftime('%Y-%m-%d')} | "
                    f"Rs.{rental['cost']}"
                )
                tk.Label(win, text=rental_info).pack(anchor='w', padx=30)
        else:
            tk.Label(win, text="  No rentals.").pack(anchor='w', padx=30)

def view_reserved_cars():
    win = tk.Toplevel(root)
    win.title("Reserved Cars")
    center_window(win, 450, 350)

    reserved = [car for car in system.cars if not car.is_available]
    if not reserved:
        tk.Label(win, text="No cars are currently reserved.").pack(pady=10)
        return

    for car in reserved:
        info = f"{car.car_id} - {car.brand} {car.model}, Rs.{car.price_per_day}/day"
        tk.Label(win, text=info).pack(anchor='w', padx=10, pady=2)

def return_car(user):
    system.return_car(user)
    messagebox.showinfo("Returned", "Car returned successfully.")

# Main Menu Buttons
tk.Button(root, text="Register", command=register_user, width=20).pack(pady=10)
tk.Button(root, text="Login", command=login_user, width=20).pack(pady=10)
tk.Button(root, text="Admin Login", command=admin_login, width=20).pack(pady=10)

root.mainloop()
