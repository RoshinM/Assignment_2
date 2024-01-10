from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from ttkthemes import ThemedTk
from PIL import ImageTk, Image
from registration import RegistrationPage
from customer import CustomerPage
from admin import AdminPage
from driver import DriverPage
from globalloginvar import getglobalEmail,getglobalusername,getglobaldriver, global_useremail, global_username, global_drivername, set_global_data, testglobal

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Taxi Booking System - Login")
        self.root.geometry("900x500+250+70")
        self.root.resizable(False, False)

        # image
        self.img = ImageTk.PhotoImage(Image.open("1.jpeg"))
        self.img_label = Label(self.root, image=self.img)
        self.img_label.place(x=0, y=0, width=500)

        # side frame
        self.sideframe = tk.Frame(self.root, bg='grey', width=400, height=300, padx=50, pady=50)
        self.sideframe.place(x=470, y=0, width=500, height=500)

        # Variables to store user input
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Change style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Increase font size
        
        self.style.configure(".", font=("Helvetica", 14))

        # GUI Components for Login
        self.label_email = ttk.Label(self.sideframe, text="Email:")
        self.label_email.grid(row=0, column=0, sticky="e")

        self.entry_email = ttk.Entry(self.sideframe, textvariable=self.email_var)
        self.entry_email.grid(row=0, column=1, padx=10)

        self.label_password = ttk.Label(self.sideframe, text="Password:")
        self.label_password.grid(row=1, column=0, pady=20, sticky="e")

        self.entry_password = ttk.Entry(self.sideframe, textvariable=self.password_var, show="*")
        self.entry_password.grid(row=1, column=1, padx=10)

        self.button_login = ttk.Button(self.sideframe, text="Login", command=self.login, width=5)
        self.button_login.grid(row=2, column=0, pady=20)

        self.button_register = ttk.Button(self.sideframe, text="Register", command=self.register, width=7)
        self.button_register.grid(row=2, column=1, pady=20)

    def login(self):
        # Get user input
            email = self.email_var.get()
            password = self.password_var.get()
            user_data = self.check_credentials(email, password)
            

        # Check login credentials
            
            if user_data:
                user_name=user_data[0]
                driver=user_data[0]
                # Extract the user's name from the fetched data
                set_global_data(email, user_name,driver)
                testglobal()
                #user_name = user_data[0]
                messagebox.showinfo("Login Successful", f"Welcome to the Taxi Booking System, {user_name}!")
                self.redirect()
            else:
                messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")

    def check_credentials(self, email, password):
        # Check login credentials in the database
        connection = sqlite3.connect("user_accounts.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user_data = cursor.fetchone()
        print(user_data)

        connection.close()

        return user_data
    
    
    def redirect(self):
        self.root.withdraw()

        # Get the user role from the check_role method
        self.role_var = tk.StringVar()
        role=self.role_var.get()
        user_role = self.check_role(self.role_var.get())

        if user_role and user_role[5] == "customer":
            self.customer()
        elif user_role and user_role[5] == "driver":
            self.driver()
        elif user_role and user_role[5] == "admin":
            self.admin()

    def check_role(self, role):
        connection = sqlite3.connect("user_accounts.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE email=?"
        cursor.execute(query, (self.email_var.get(),))
        user_data = cursor.fetchone()

        connection.close()

        return user_data

    def register(self):
        self.root.withdraw()
        self.register_frame = Toplevel()
        self.registration_page = RegistrationPage(self.register_frame, main_login_window=self.root)
    
    def customer(self):
        self.root.withdraw()
        self.customer_frame = Toplevel()
        self.registration_page = CustomerPage(self.customer_frame, customer_window=self.root)

    def admin(self):
        self.root.withdraw()
        self.admin_frame= Toplevel()
        self.admin_page = AdminPage(self.admin_frame, admin_window=self.root)

    def driver(self):
        self.root.withdraw()
        self.driver_frame= Toplevel()
        self.driver_page = DriverPage(self.driver_frame, driver_window=self.root)

if __name__ == "__main__":
    try:
        # Create a database table for users
        connection = sqlite3.connect("user_accounts.db")
        cursor = connection.cursor()

        # Create a new table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                name TEXT,
                gender TEXT,
                age INTEGER,
                email TEXT PRIMARY KEY,
                password TEXT,
                role TEXT
            )
        """)

        connection.commit()
        connection.close()

        root = ThemedTk(theme="clam")  # Change to a different color theme
        app = LoginPage(root)
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")




