import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
from ttkthemes import ThemedTk
from PIL import ImageTk, Image
from tkcalendar import DateEntry

class AdminPage:
    def __init__(self,root,admin_window):
        self.root=root
        self.root.title("admin page")
        self.root.geometry("1440x900")

        self.admin_window=admin_window

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(".", padding=(0))
        self.style.configure(".", font=("Helvetica", 14))

        self.header= Frame(self.root,bg="blue")
        self.header.place(x=300,y=0,width=1000,height=100)

        self.head_Text=Label(self.header,text="Taxi Booking System", font=("Bold", 36), bg="blue", fg="white")
        self.head_Text.place(x=70,y=20)

        self.back=ttk.Button(self.header,text="logout",command=self.admin_account_to_login)
        self.back.place(x=800,y=25)
    
        self.sidebar=Frame(self.root, bg="gray")
        self.sidebar.place(x=0,y=0,width=300,height=900)

        self.img = ImageTk.PhotoImage(Image.open("profile.jpeg"))
        self.img_label = Label(self.sidebar, image=self.img,bg="gray")
        self.img_label.place(x=70,y=80)
        
        self.text1=Button(self.sidebar,text="customers",bg="#ffffff",bd=0,cursor="hand2",activebackground="gray",font=("",13,"bold"),
        width=30,command=self.view_customer)
        self.text1.place(x=0,y=290) 

        self.text2=Button(self.sidebar,text="driver",bg="#ffffff",bd=0,cursor="hand2",activebackground="gray",font=("",13,"bold"),width=30,command=self.view_driver)
        self.text2.place(x=0,y=320)
        
        self.text3=Button(self.sidebar,text="assign driver",bg="#ffffff",bd=0,cursor="hand2",activebackground="gray",font=("",13,"bold"),width=30,command=self.assign_driver)
        self.text3.place(x=0,y=350)
        
        self.dashboard_frame=Frame(self.root)
        self.dashboard_frame.place(x=305,y=105,width=1200,height=900)

        self.dashboard_text=Label(self.dashboard_frame,text="Dashboard", font=("Bold", 16), fg="blue")
        self.dashboard_text.place(x=20,y=20)

        self.frame1=Frame(self.dashboard_frame,bg="red")
        self.frame1.place(x=10,y=70,width=300,height=200)

         # Add label to display the count
        self.customer_count_label = Label(self.frame1, text="Number of Customers:", fg="white", bg="red",font=("Bold", 16))
        self.customer_count_label.place(x=20,y=70)

        # Call the count_customers function and update the label text
        count = self.count_customers()
        self.customer_count_label.config(text=f"Number of Customers: {count}")

        self.frame2=Frame(self.dashboard_frame,bg="orange")
        self.frame2.place(x=330,y=70,width=300,height=200)

        self.driver_count_label = Label(self.frame2, text="Number of Drivers:", fg="white", bg="orange",font=("Bold", 16))
        self.driver_count_label.place(x=20,y=70)

        count_driver = self.count_drivers()
        self.driver_count_label.config(text=f"Number of Drivers: {count_driver}")

        self.frame3=Frame(self.dashboard_frame,bg="green")
        self.frame3.place(x=650,y=70,width=300,height=200)

        self.customer_bookings_count_label = Label(self.frame3, text="Number of Bookings:", fg="white", bg="green",font=("Bold", 16))
        self.customer_bookings_count_label.place(x=20,y=70)

        count_customer_booking = self.count_customer_bookings()
        self.customer_bookings_count_label.config(text=f"Number of Bookings: {count_customer_booking}")

    def admin_account_to_login(self):
        self.root.destroy()
        self.admin_window.deiconify()
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", font=("Helvetica", 14))

    def view_customer(self):
        self.conn =sqlite3.connect("user_accounts.db")
        self.cursor =self.conn.cursor()

        self.customer_display=Toplevel()
        self.customer_display.title("customer database")
        self.customer_display.geometry("650x300+270+120")

        self.label_search = tk.Label(self.customer_display, text="Search:")
        self.label_search.place(x=150,y=10)

        self.entry_search = tk.Entry(self.customer_display)
        self.entry_search.place(x=210,y=10)

        self.btn_search = tk.Button(self.customer_display, text="Search", command=self.search_records_view_customer)
        self.btn_search.place(x=350,y=10)

        self.btn_clear= tk.Button(self.customer_display,text="clear",command=self.clear_search_view_customer)
        self.btn_clear.place(x=400,y=10)

        #tree
        self.tree = ttk.Treeview(self.customer_display, columns=("name","gender","age","email","password","role"),
                                 show="headings")
        self.tree.heading("name", text="name")
        self.tree.heading("gender", text="gender")
        self.tree.heading("age", text="age")
        self.tree.heading("email", text="email")
        self.tree.heading("password", text="password")
        self.tree.heading("role",text="role")
        self.tree.place(x=10, y=50)

        # Set the width of each column
        self.tree.column("name", width=100)
        self.tree.column("gender", width=100)
        self.tree.column("age", width=100)
        self.tree.column("email", width=100)
        self.tree.column("password", width=100)
        self.tree.column("role", width=100)

        self.read_records_view_customer()


    def read_records_view_customer(self):
        self.tree.delete(*self.tree.get_children())
 
        # Fetch records where the role is "customer"
        self.cursor.execute('''
        SELECT name, gender, age, email, password, role 
        FROM users 
        WHERE role = "customer"
        ''')
    
        records = self.cursor.fetchall()

        if records:
            for record in records:
                # Insert each record into the treeview
                self.tree.insert("", "end", values=record)
        else:
            # Display a message if no records are found
            messagebox.showinfo("No Records", "No customer records found.")

    def search_records_view_customer(self):
        search_term = self.entry_search.get().lower()
        self.tree.delete(*self.tree.get_children())

        self.cursor.execute('''SELECT * FROM users''')
        records = self.cursor.fetchall()

        if records:
            for record in records:
                if search_term in str(record).lower():
                    self.tree.insert("", "end", values=record)

        else:
            messagebox.showinfo("No Records", "No records found.")

    def clear_search_view_customer(self):
        self.tree.delete(*self.tree.get_children())
        self.read_records_view_customer()
        self.entry_search.delete(0, tk.END)

    #for driver:
    def view_driver(self):
        self.conn =sqlite3.connect("user_accounts.db")
        self.cursor =self.conn.cursor()

        self.customer_display=Toplevel()
        self.customer_display.title("driver database")
        self.customer_display.geometry("650x300+270+120")

        self.label_search = tk.Label(self.customer_display, text="Search:")
        self.label_search.place(x=150,y=10)

        self.entry_search = tk.Entry(self.customer_display)
        self.entry_search.place(x=210,y=10)

        self.btn_search = tk.Button(self.customer_display, text="Search", command=self.search_records_view_driver)
        self.btn_search.place(x=350,y=10)

        self.btn_clear= tk.Button(self.customer_display,text="clear",command=self.clear_search_view_driver)
        self.btn_clear.place(x=400,y=10)

        #tree
        self.tree = ttk.Treeview(self.customer_display, columns=("name","gender","age","email","password","role"),
                                 show="headings")
        self.tree.heading("name", text="name")
        self.tree.heading("gender", text="gender")
        self.tree.heading("age", text="age")
        self.tree.heading("email", text="email")
        self.tree.heading("password", text="password")
        self.tree.heading("role",text="role")
        self.tree.place(x=10, y=50)

        # Set the width of each column
        self.tree.column("name", width=100)
        self.tree.column("gender", width=100)
        self.tree.column("age", width=100)
        self.tree.column("email", width=100)
        self.tree.column("password", width=100)
        self.tree.column("role", width=100)

        self.read_records_view_driver()


    def read_records_view_driver(self):
        self.tree.delete(*self.tree.get_children())
 
        # Fetch records where the role is "driver"
        self.cursor.execute('''
        SELECT name, gender, age, email, password, role 
        FROM users 
        WHERE role = "driver"
        ''')
    
        records = self.cursor.fetchall()

        if records:
            for record in records:
                # Insert each record into the treeview
                self.tree.insert("", "end", values=record)
        else:
            # Display a message if no records are found
            messagebox.showinfo("No Records", "No driver records found.")

    def search_records_view_driver(self):
        search_term = self.entry_search.get().lower()
        self.tree.delete(*self.tree.get_children())

        self.cursor.execute('''SELECT * FROM users''')
        records = self.cursor.fetchall()

        if records:
            for record in records:
                if search_term in str(record).lower():
                    self.tree.insert("", "end", values=record)

        else:
            messagebox.showinfo("No Records", "No records found.")

    def clear_search_view_driver(self):
        self.tree.delete(*self.tree.get_children())
        self.read_records_view_driver()
        self.entry_search.delete(0, tk.END)

    #assigning part:
    def assign_driver(self):
        # database
        self.conn = sqlite3.connect("user_accounts.db")
        self.cursor = self.conn.cursor()

        self.customer_display=Toplevel()
        self.customer_display.title("assign driver")
        self.customer_display.geometry("1200x600")

        self.assign_driver_frame=Frame(self.customer_display,bg="gray")
        self.assign_driver_frame.place(x=0,y=0,width=250,height=600)

         # Search Bar
        self.label_search = tk.Label(self.assign_driver_frame, text="Search:")
        self.label_search.place(x=10,y=50)

        # Create a StringVar to store the selected value from the dropdown
        self.selected_driver = tk.StringVar()
        
        # Fetch driver names using the new function
        self.driver_names = self.fetch_driver_names()

        # Create a Combobox with the fetched driver names
        self.search_options = ttk.Combobox(self.assign_driver_frame, values=self.driver_names, textvariable=self.selected_driver)
        self.search_options.set("Select Driver")  # Set the default value
        self.search_options.place(x=60, y=50)

        # Treeview
        self.tree = ttk.Treeview(self.customer_display, columns=("ID", "pickup date", "pickup time", "drop time", "pickup address", "drop address","name","status"),
                                 show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("pickup date", text="pickup date")
        self.tree.heading("pickup time", text="pickup time")
        self.tree.heading("drop time", text="drop time")
        self.tree.heading("pickup address", text="pickup address")
        self.tree.heading("drop address", text="drop address")
        self.tree.heading("name",text="name")
        self.tree.heading("status",text="status")
        self.tree.place(x=300, y=50)

        # Set the width of each column
        self.tree.column("ID", width=50)
        self.tree.column("pickup date", width=100)
        self.tree.column("pickup time", width=100)
        self.tree.column("drop time", width=100)
        self.tree.column("pickup address", width=100)
        self.tree.column("drop address", width=100)
        self.tree.column("name", width=100)
        self.tree.column("status", width=100)

        self.read_records_assign_driver()

        #database for assigned status

        self.conn = sqlite3.connect("user_accounts.db")
        self.cursor = self.conn.cursor()

        # Create table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS assigned
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date INTEGER, 
                            pickuptime INTEGER, 
                            droptime INTEGER, 
                            pickupaddress INTEGER, 
                            dropaddress INTEGER,
                            name TEXT
                            status TEXT)''')
        self.conn.commit()

        self.btn_move_data = tk.Button(self.assign_driver_frame, text="Assign", command=self.move_data,bg="#ffffff",bd=0,cursor="hand2",activebackground="gray",font=("",13,"bold"),width=25)
        self.btn_move_data.place(x=0, y=120)

        self.tree_assigned = ttk.Treeview(self.customer_display, columns=("ID", "pickup date", "pickup time", "drop time", "pickup address", "drop address","name","status","assigned to"),
                                 show="headings")
        self.tree_assigned.heading("ID", text="ID")
        self.tree_assigned.heading("pickup date", text="pickup date")
        self.tree_assigned.heading("pickup time", text="pickup time")
        self.tree_assigned.heading("drop time", text="drop time")
        self.tree_assigned.heading("pickup address", text="pickup address")
        self.tree_assigned.heading("drop address", text="drop address")
        self.tree_assigned.heading("name",text="name")
        self.tree_assigned.heading("status",text="status")
        self.tree_assigned.heading("assigned to",text="assigned to")
        self.tree_assigned.place(x=300, y=320)

        # Set the width of each column
        self.tree_assigned.column("ID", width=50)
        self.tree_assigned.column("pickup date", width=100)
        self.tree_assigned.column("pickup time", width=100)
        self.tree_assigned.column("drop time", width=100)
        self.tree_assigned.column("pickup address", width=100)
        self.tree_assigned.column("drop address", width=100)
        self.tree_assigned.column("name", width=100)
        self.tree_assigned.column("status", width=100)
        self.tree_assigned.column("assigned to", width=100)

        self.read_records_assigned_driver()

        self.btn_delete_record = tk.Button(self.assign_driver_frame, text="Delete Record", command=self.delete_selected_record,bg="#ffffff",bd=0,cursor="hand2",activebackground="gray",font=("",13,"bold"),width=25)
        self.btn_delete_record.place(x=0, y=150)

    def fetch_driver_names(self):
        self.driver_names = []

        try:
            # Open a new connection within the function
            with sqlite3.connect("user_accounts.db") as driver_connection:
                driver_cursor = driver_connection.cursor()
                driver_cursor.execute('''
                    SELECT name
                    FROM users
                    WHERE role = "driver"
                ''')
                driver_names = [row[0] for row in driver_cursor.fetchall()]

        except Exception as e:
            # Handle the exception within the function (e.g., show an error message)
            messagebox.showerror("Database Error", f"Error fetching driver names: {e}")

        return driver_names


    def read_records_assign_driver(self):
        self.tree.delete(*self.tree.get_children())

        self.cursor.execute('''SELECT * FROM customerrecords''')
        records = self.cursor.fetchall()

        if records:
            for record in records:
                self.tree.insert("", "end", values=record)  

    def read_records_assigned_driver(self):
        self.tree_assigned.delete(*self.tree_assigned.get_children())

        self.cursor.execute('''SELECT * FROM assigned''')
        records = self.cursor.fetchall()

        if records:
            for record in records:
                self.tree_assigned.insert("", "end", values=record)      

    #

    def move_data(self):
        # Get the selected item from the tree
        selected_item = self.tree.selection()
    
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record.")
            return
        try:
            # Get the values of the selected item
            record_id = self.tree.item(selected_item, "values")[0]
            self.move_data_to_assigned(record_id)
            messagebox.showinfo("Success", "Assigned successfully!")

            # Clear the first tree and update the second tree with the moved record
            self.tree.delete(*self.tree.get_children())
            self.read_records_assign_driver()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        

    def move_data_to_assigned(self, record_id):
        driver_assigned=self.search_options.get()
        conn = sqlite3.connect("user_accounts.db")
        cursor = conn.cursor()

        try:
            # Read data from customerrecords for the selected record_id
            cursor.execute("SELECT * FROM customerrecords WHERE id=?", (record_id,))
            records_to_move = cursor.fetchall()

            if not records_to_move:
                messagebox.showwarning("Warning", "No record found for the selected ID.")
                return

            # Insert data into assigned table and delete from customerrecords
            for record in records_to_move:
                cursor.execute('''
                    INSERT INTO assigned
                    (date, pickuptime, droptime, pickupaddress, dropaddress, name, status, assigned_to)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', record[1:]+(driver_assigned,))  # Exclude the ID column
                assigned_record_id = cursor.lastrowid
                cursor.execute("DELETE FROM customerrecords WHERE id=?", (record[0],))

            cursor.execute("UPDATE assigned SET status='assigned' WHERE id=?", (assigned_record_id,))

            # Commit changes to the database
            conn.commit()

            # Close the connection
            conn.close()



            # Clear the second tree and update with the moved record
            self.tree_assigned.delete(*self.tree_assigned.get_children())
            self.read_records_assigned_driver()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_selected_record(self):
        # Get the selected item from the tree_assigned
        selected_item = self.tree_assigned.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record.")
            return

        try:
            # Get the values of the selected item
            record_id = self.tree_assigned.item(selected_item, "values")[0]
            self.delete_record_from_assigned(record_id)
            messagebox.showinfo("Success", "Record deleted successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_record_from_assigned(self, record_id):
        conn = sqlite3.connect("user_accounts.db")
        cursor = conn.cursor()

        try:
            # Delete the record from the 'assigned' table
            cursor.execute("DELETE FROM assigned WHERE id=?", (record_id,))
            conn.commit()

            # Refresh the treeview to reflect the changes
            self.read_records_assigned_driver()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            # Close the connection
            conn.close()

    def count_customers(self):
        count = 0
        try:
            # Connect to the SQLite database
            self.conn = sqlite3.connect("user_accounts.db")

        # Create a cursor object
            self.cursor = self.conn.cursor()

            # SQL query to count the number of records with role='customer'
            sql = "SELECT COUNT(*) FROM users WHERE role = 'customer'"

            # Execute the query
            self.cursor.execute(sql)

            # Fetch the result
            count = self.cursor.fetchone()[0]
            print("count",count)

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            # Close the cursor and connection
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

        return count
    
    def count_drivers(self):
        count_driver= 0
        try:
            # Connect to the SQLite database
            self.conn = sqlite3.connect("user_accounts.db")

        # Create a cursor object
            self.cursor = self.conn.cursor()

            # SQL query to count the number of records with role='customer'
            sql_driver = "SELECT COUNT(*) FROM users WHERE role = 'driver'"

            # Execute the query
            self.cursor.execute(sql_driver)

            # Fetch the result
            count_driver = self.cursor.fetchone()[0]
            print("count2",count_driver)

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            # Close the cursor and connection
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

        return count_driver
    
    def count_customer_bookings(self):
        count_customer_booking= 0
        try:
            # Connect to the SQLite database
            self.conn = sqlite3.connect("user_accounts.db")

        # Create a cursor object
            self.cursor = self.conn.cursor()

            # SQL query to count the number of records with role='customer'
            sql_cusrec = "SELECT COUNT(*) FROM customerrecords WHERE status = 'pending'"

            # Execute the query
            self.cursor.execute(sql_cusrec)

            # Fetch the result
            count_customer_booking = self.cursor.fetchone()[0]
            print("count3",count_customer_booking)

        except sqlite3.Error as e:
            print(f"Error: {e}")

        finally:
            # Close the cursor and connection
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

        return count_customer_booking
    
        

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
        admin_window = tk.Toplevel(root)  # Create a Toplevel window for admin
        app = AdminPage(root, admin_window)
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")