import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from ttkthemes import ThemedTk
from tkinter import *

class RegistrationPage:
    def __init__(self, root, main_login_window):
        self.root = root
        self.root.title("Taxi Booking System - Registration")
        self.root.geometry("350x550+250+50")  # Adjusted root size
        self.root.resizable(False, False)

        # Variables to store user input
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Store a reference to the main login window
        self.main_login_window = main_login_window

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("black")  # Change to a different color theme

        # Increase font size( self.style.configure
        self.style.configure(".", font=("Helvetica", 14))

        # Add more padding
        self.style.configure(".", padding=(10, 10, 10, 10))

        self.background_color=Frame(self.root,bg="gray")
        self.background_color.place(x=0,y=0,width=400,height=600)
        # GUI Components for Register
        self.label_name = ttk.Label(self.background_color, text="Name:")
        self.label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.entry_name = ttk.Entry(self.background_color)
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)

        self.label_gender = ttk.Label(self.background_color, text="Gender:")
        self.label_gender.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.gender_var = tk.StringVar()
        self.gender_combobox = ttk.Combobox(self.background_color, textvariable=self.gender_var, values=["Male", "Female", "Other"])
        self.gender_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.label_age = ttk.Label(self.background_color, text="Age:")
        self.label_age.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.entry_age = ttk.Entry(self.background_color)
        self.entry_age.grid(row=2, column=1, padx=10, pady=10)

        self.label_email_register = ttk.Label(self.background_color, text="Email:")
        self.label_email_register.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.entry_email_register = ttk.Entry(self.background_color)
        self.entry_email_register.grid(row=3, column=1, padx=10, pady=10)

        self.label_password_register = ttk.Label(self.background_color, text="Password:")
        self.label_password_register.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.entry_password_register = ttk.Entry(self.background_color, show="*")
        self.entry_password_register.grid(row=4, column=1, padx=10, pady=10)    

        self.label_role = ttk.Label(self.background_color, text="role:")
        self.label_role.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.role_var = tk.StringVar()
        self.role_combobox = ttk.Combobox(self.background_color, textvariable=self.role_var, values=["customer", "driver", "admin"])
        self.role_combobox.grid(row=5, column=1, padx=10, pady=10)

        self.button_submit_register = ttk.Button(self.background_color, text="Submit", command=self.register_user)
        self.button_submit_register.grid(row=6, column=0, columnspan=2, pady=20)

        self.button_back_to_login = ttk.Button(self.background_color, text="Back to Login", command=self.show_login_page)
        self.button_back_to_login.grid(row=7, column=0, columnspan=2, pady=10)

    def show_login_page(self):
        # Close the registration window
        self.root.destroy()

        # Deiconify the main login window
        self.main_login_window.deiconify()
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def register_user(self):
        # Get user input
        name = self.entry_name.get()
        gender = self.gender_var.get()
        age = self.entry_age.get()
        email = self.entry_email_register.get()
        password = self.entry_password_register.get()
        role = self.role_var.get()
 
        # Validate input
        if not name or not gender or not age or not email or not password or not role:
            messagebox.showerror("Registration Failed", "Please fill in all fields.")
            return

        # Register the user in the database
        connection = sqlite3.connect("user_accounts.db")
        cursor = connection.cursor()

        # Check if the user already exists
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            messagebox.showerror("Registration Failed", "User with this email already exists.")
        else:
            cursor.execute("INSERT INTO users (name, gender, age, email, password,role) VALUES (?, ?, ?, ?,?,?)",
                           (name, gender, age, email, password,role))
            connection.commit()
            messagebox.showinfo("Registration Successful", "Account created successfully!")

        connection.close()
        self.root.destroy()
        self.main_login_window.deiconify()
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Increase font size
        self.style.configure(".", font=("Helvetica", 14))

        pass


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
        app = RegistrationPage(root, main_login_window=None)
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
