import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from ttkthemes import ThemedTk
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from globalloginvar import *

class DriverPage:
    def __init__(self,root,driver_window):
        self.root=root
        self.root.title("driver page")
        self.root.geometry("950x400+100+20")
        self.root.resizable(False, False)

        self.driver_window=driver_window

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(".", padding=(0))
        self.style.configure(".", font=("Helvetica", 14))

        self.top_bar=Frame(self.root,bg="blue")
        self.top_bar.place(x=0,y=20,width=950,height=70)

        self.welcome=Label(self.top_bar,text="Booking Offers", font=("Bold", 36), bg="blue", fg="white")
        self.welcome.place(x=350,y=15)

        self.logout_button=Button(self.top_bar,text="logout",command=self.back_to_login)
        self.logout_button.place(x=900,y=30)

        self.sidebar=Frame(self.root, bg="gray")
        self.sidebar.place(x=800,y=90,width=300,height=900)

        self.complete_ride=Button(self.sidebar,text="complete",command=self.complete,bg="#ffffff",bd=0,cursor="hand2",activebackground="gray",font=("",13,"bold"),width=15)
        self.complete_ride.place(x=0,y=20)

        self.payment_button=Button(self.sidebar,text="payment",command=self.payment,bg="#ffffff",bd=0,cursor="hand2",activebackground="gray",font=("",13,"bold"),width=15)
        self.payment_button.place(x=0,y=50)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("ID", "pickup date", "pickup time", "drop time", "pickup address", "drop address","name","status"),
                                 show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("pickup date", text="pickup date")
        self.tree.heading("pickup time", text="pickup time")
        self.tree.heading("drop time", text="drop time")
        self.tree.heading("pickup address", text="pickup address")
        self.tree.heading("drop address", text="drop address")
        self.tree.heading("name",text="name")
        self.tree.heading("status",text="status")
        self.tree.place(x=30, y=120)

        # Set the width of each column
        self.tree.column("ID", width=50)
        self.tree.column("pickup date", width=100)
        self.tree.column("pickup time", width=100)
        self.tree.column("drop time", width=100)
        self.tree.column("pickup address", width=100)
        self.tree.column("drop address", width=100)
        self.tree.column("name", width=100)
        self.tree.column("status", width=100)

        self.tree_driver_read()

    def complete(self):
        # Get the selected item from the tree
        selected_item = self.tree.selection()
    
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record.")
            return
        try:
             # Get the values of the selected item
            record_id = self.tree.item(selected_item, "values")[0]

            self.conn=sqlite3.connect("user_accounts.db")
            self.cursor =self.conn.cursor()

            self.cursor.execute("UPDATE assigned SET status='completed' WHERE id=?", (record_id,))
            self.conn.commit()
            
            self.tree.set(selected_item, "status", "completed")

            messagebox.showinfo("Success", "Data updated successfully!")
         
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            self.conn.close()

    def tree_driver_read(self):
        driver=getglobaldriver()
        print("drivername:",driver)
        self.tree.delete(*self.tree.get_children())

        self.conn=sqlite3.connect("user_accounts.db")
        self.cursor =self.conn.cursor()

        self.cursor.execute('''SELECT * FROM assigned WHERE assigned_to=?''', (driver,))
        records = self.cursor.fetchall()

        if records:
            for record in records:
                # Insert each record into the treeview
                self.tree.insert("", "end", values=record)
        else:
            # Display a message if no records are found
            messagebox.showinfo("No Records", "No customers assigned")

    def back_to_login(self):
        self.root.destroy()
        self.driver_window.deiconify()
        self.style = ttk.Style()
        self.style.theme_use("clam")

    def payment(self):
        selected_item = self.tree.selection()
    
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record.")
            return
        try:
            # Get the values of the selected item
            record_id = self.tree.item(selected_item, "values")[0]
            # Call the pay function
            self.pay()
             # Get the values of the selected item
            record_id = self.tree.item(selected_item, "values")[0]

            self.conn=sqlite3.connect("user_accounts.db")
            self.cursor =self.conn.cursor()

            self.cursor.execute("UPDATE assigned SET status='paid' WHERE id=?", (record_id,))
            self.conn.commit()
            
            self.tree.set(selected_item, "status", "paid")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")  

    def pay(self):
        # Create a new top-level window for payment
        payment_window = Toplevel(self.root)
        payment_window.title("Payment Processing")
        payment_window.geometry("400x250+500+70")
        payment_window.resizable(False, False)  

        self.top_bar2=Frame(payment_window,bg="blue")
        self.top_bar2.place(x=0,y=0,width=550,height=70)

        self.welcome=Label(self.top_bar2,text="Payment", font=("Helvetica", 26), bg="blue", fg="white")
        self.welcome.place(x=120,y=20)

        # Label for entering distance
        self.distance_label = Label(payment_window, text="Enter Distance Travelled:")
        self.distance_label.place(x=25,y=100)

        # Entry box for entering distance (only allows integer input)
        distance_var = StringVar()

        self.distance_entry = Entry(payment_window, textvariable=distance_var, validate="key", validatecommand=(self.root.register(self.validate_entry), "%P"),width=5)
        self.distance_entry.place(x=175,y=100)

        self.kilometer_label=Label(payment_window,text="km")
        self.kilometer_label.place(x=200,y=100)

        self.calculate_button = Button(payment_window, text="Calculate", command=self.calculate_payment)
        self.calculate_button.place(x=230,y=90)

        self.fees=Label(payment_window,text="total fees:")
        self.fees.place(x=55,y=150)

        self.fees_display = Entry(payment_window)
        self.fees_display.place(x=120, y=150)

        # You can also add a button to close the payment window
        self.close_button = Button(payment_window, text="Complete", command=payment_window.destroy)
        self.close_button.place(x=200,y=200)

    # Validation function to allow only integer input in the entry box
    def validate_entry(self, new_value):
        try:
            int(new_value)
            return True
        except ValueError:
            return False  

    def calculate_payment(self):
        try:
            distance_value = int(self.distance_entry.get())
            payment_amount = distance_value * 35

            # Display the calculated payment in the Entry widget
            self.fees_display.delete(0, END)  # Clear previous content
            self.fees_display.insert(0, "Rs.{}".format(payment_amount))

        except ValueError:
            messagebox.showerror("Error", "Invalid distance value. Please enter a valid integer.")

if __name__ == "__main__":
    root = ThemedTk(theme="clam")  # Change to a different color theme
    driver_window = tk.Toplevel(root)  # Create a Toplevel window for admin
    app = DriverPage(root, driver_window)
    root.mainloop()
