# 🚗 Online Car Rental System (OOP Project)

This is a Python-based GUI project for an **Online Car Rental System**, developed using **Object-Oriented Programming (OOP)** principles and **Tkinter**. The system allows users to rent and return cars, manage their balance, and keep track of rental history, while admins can manage cars and view reports.

## 📌 Features

### 👤 User Functionalities
- Register and log in as a user
- View available cars
- Rent a car for specific dates
- Return rented car
- View rental history
- Recharge account balance
- Only **one car can be rented at a time**

### 🛠️ Admin Functionalities
- Log in as an admin
- Add new cars to the system
- Remove cars (⚠️ *A rented car cannot be removed until it is returned*)
- View list of currently rented cars
- View user rental reports

## 🧱 OOP Concepts Used

- **Classes and Objects** – `User`, `Admin`, `Car`, and `RentalSystem` classes
- **Inheritance** – `Admin` and `User` inherit from a common base class
- **Method Overriding** – `display_info()` is overridden in both `Admin` and `User`
- **Association** – `RentalSystem` class interacts with `User`, `Admin`, and `Car`
- **Exception Handling** – Duplicate usernames, login errors, insufficient balance, invalid car removal
- **File Handling** – Optional (if saving/loading is added)
- **Encapsulation** – Internal data like balance, rental history, etc., managed within classes

## 🖼️ GUI Features (Tkinter)
- Easy-to-use graphical interface
- Dropdown to select cars
- Pop-up messages for actions like success, errors, and warnings
- Input validation (e.g., prevents removing a rented car)

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** (for GUI)
- **datetime** module (for rental dates)

## 🧪 Sample Validations and Logic

- Renting checks if the car is available and user has enough balance
- Cars are marked unavailable when rented and available when returned
- Admin cannot remove a car currently rented by a user
- Duplicate usernames not allowed at registration
- Only valid username-password pairs can log in


