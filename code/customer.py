from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from ttkthemes import ThemedTk
from tkcalendar import DateEntry
from globalloginvar import *


class CustomerPage:

    def __init__(self,root,customer_window):
        self.root=root 
        self.root.title("customer page")
        self.root.geometry("800x550+350+70")
        self.root.resizable(False, False)
        # print('Val:', global_useremail)
        self.customer_window=customer_window

        self.style = ttk.Style()
        self.style.theme_use("black")

        self.style.configure(".", padding=(0))

        self.style.configure(".", font=("TkDefaultFont", 12))

        self.header_customer=Frame(self.root,bg="blue")
        self.header_customer.place(x=0,y=0,width=800,height=70)

        self.welcome=Label(self.header_customer,text="Customer Booking", font=("Bold", 32), bg="blue", fg="white")
        self.welcome.place(x=220,y=15)

        self.back=Button(self.header_customer,text="logout",command=self.customer_page_to_login,padx=10,pady=5)
        self.back.place(x=700,y=30)

        self.background_color_customer=Frame(self.root,bg="white")
        self.background_color_customer.place(x=0,y=70,width=800,height=600)

        self.select_date=ttk.Label(self.background_color_customer,text="Date:")
        self.select_date.place(x=20,y=10)

        self.calendar=DateEntry(self.background_color_customer)
        self.calendar.place(x=65,y=10)

        self.pickup_time=ttk.Label(self.background_color_customer,text="pickup time:")
        self.pickup_time.place(x=20,y=40)

        self.entry_pickup_time=ttk.Entry(self.background_color_customer)
        self.entry_pickup_time.place(x=110,y=40)

        self.drop_time=ttk.Label(self.background_color_customer,text="drop time:")
        self.drop_time.place(x=300,y=40)

        self.entry_drop_time=ttk.Entry(self.background_color_customer)
        self.entry_drop_time.place(x=375,y=40)

        self.pickup_address=ttk.Label(self.background_color_customer,text="pickup address:")
        self.pickup_address.place(x=20,y=70)

        self.entry_pickup_address=ttk.Entry(self.background_color_customer)
        self.entry_pickup_address.place(x=140,y=70)

        self.drop_address=ttk.Label(self.background_color_customer,text="drop address:")
        self.drop_address.place(x=20,y=100)

        self.entry_drop_address=ttk.Entry(self.background_color_customer)
        self.entry_drop_address.place(x=125,y=100)

        # database
        self.conn = sqlite3.connect("user_accounts.db")
        self.cursor = self.conn.cursor()

        # Create table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS customerrecords
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date INTEGER, 
                            pickuptime INTEGER, 
                            droptime INTEGER, 
                            pickupaddress INTEGER, 
                            dropaddress INTEGER,
                            name TEXT
                            status TEXT)''')
        self.conn.commit()

        # Treeview
        self.tree = ttk.Treeview(self.background_color_customer, columns=("ID", "pickup date", "pickup time", "drop time", "pickup address", "drop address","name","status"),
                                 show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("pickup date", text="pickup date")
        self.tree.heading("pickup time", text="pickup time")
        self.tree.heading("drop time", text="drop time")
        self.tree.heading("pickup address", text="pickup address")
        self.tree.heading("drop address", text="drop address")
        self.tree.heading("name", text="name")
        self.tree.heading("status", text="status")
        self.tree.place(x=10, y=220)

        # Set the width of each column
        self.tree.column("ID", width=50)
        self.tree.column("pickup date", width=100)
        self.tree.column("pickup time", width=100)
        self.tree.column("drop time", width=100)
        self.tree.column("pickup address", width=100)
        self.tree.column("drop address", width=100)
        self.tree.column("name", width=100)
        self.tree.column("status", width=100)

        # Buttons
        self.btn_save = Button(self.background_color_customer, text="save", padx=15,pady=5,bg="gray",command=self.create_record,width=4)
        self.btn_save.place(x=20,y=150)

        self.btn_update = Button(self.background_color_customer, text="Update", padx=15,pady=5,bg="gray", command=self.update_record,width=6)
        self.btn_update.place(x=100,y=150)

        self.btn_delete = Button(self.background_color_customer, text="Delete", padx=15,pady=5,bg="gray", command=self.delete_record,width=5)
        self.btn_delete.place(x=190,y=150)

        self.btn_clear = Button(self.background_color_customer,text="clear", padx=15,pady=5,bg="gray",command=self.clear_entries,width=4)
        self.btn_clear.place(x=270,y=150)

        self.read_records()
    
    def create_record(self):
        date = self.calendar.get()
        pickuptime = self.entry_pickup_time.get()
        droptime = self.entry_drop_time.get()
        pickupaddress = self.entry_pickup_address.get()
        dropaddress = self.entry_drop_address.get()
        name=getglobalusername()

        if date and pickuptime and droptime and pickupaddress and dropaddress:
            self.tree.insert("", "end", values=(None, date, pickuptime, droptime, pickupaddress, dropaddress, name, "pending"))
            self.cursor.execute('''INSERT INTO customerrecords (date, pickuptime, droptime, pickupaddress, dropaddress,name,status) VALUES (?, ?, ?, ?, ?, ?, ?)''',(date, pickuptime, droptime, pickupaddress, dropaddress,name,'pending'))
            self.conn.commit()
            messagebox.showinfo("Success", "Record created successfully!")
            self.clear_entries()
            self.read_records()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def delete_record(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete.")
            return

        selected_id = self.tree.item(selected_item, "values")[0]

        self.cursor.execute('''DELETE FROM customerrecords WHERE id=?''', (selected_id,))
        self.conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
        self.clear_entries()
        self.read_records()

    def clear_entries(self):
        self.entry_pickup_time.delete(0, tk.END)
        self.entry_drop_time.delete(0, tk.END)
        self.entry_pickup_address.delete(0, tk.END)
        self.entry_drop_address.delete(0, tk.END)

    def read_records(self):
        self.tree.delete(*self.tree.get_children())

        self.cursor.execute('''SELECT * FROM customerrecords''')
        records = self.cursor.fetchall()

        if records:
            for record in records:
                self.tree.insert("", "end", values=record)

    def update_record(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a record to update.")
            return

        selected_id = self.tree.item(selected_item, "values")[0]
        date = self.calendar.get()
        pickuptime = self.entry_pickup_time.get()
        droptime = self.entry_drop_time.get()
        pickupaddress = self.entry_pickup_address.get()
        dropaddress = self.entry_drop_address.get()

        self.cursor.execute('''UPDATE customerrecords SET date=?,pickuptime=?, droptime=?, pickupaddress=?,dropaddress=? WHERE id=?''', (date, pickuptime, droptime, pickupaddress, dropaddress, selected_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
        self.clear_entries()
        self.read_records()

    def customer_page_to_login(self):
        self.root.destroy()
        self.customer_window.deiconify()
        self.style = ttk.Style()
        self.style.theme_use("clam")

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
        app = CustomerPage(root, customer_window=None)
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")