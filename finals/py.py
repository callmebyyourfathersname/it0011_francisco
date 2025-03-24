import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os
from datetime import datetime

# File to store records
RECORDS_FILE = "records.txt"

# Base class for Person
class Person:
    def __init__(self, first_name, middle_name, last_name, birthday, gender):
        self._first_name = first_name  # Protected
        self._middle_name = middle_name
        self._last_name = last_name
        self._birthday = birthday
        self._gender = gender

    def __str__(self):
        return ",".join([self._first_name, self._middle_name, self._last_name, self._birthday, self._gender])

# Admin class with full control
class Admin(Person):
    pass  # Admin has all capabilities from GUIApp

# User class with limited privileges
class User(Person):
    pass  # Users can only view and search records

# Record Manager with private filename
class RecordManager:
    def __init__(self, filename="records.txt"):
        self.__filename = filename  # Private

    def load_records(self):
        if not os.path.exists(self.__filename):
            return []
        with open(self.__filename, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]

    def save_records(self, records):
        with open(self.__filename, "w") as file:
            for record in records:
                file.write(",".join(record) + "\n")

    def add_record(self, record):
        records = self.load_records()
        records.append(record)
        self.save_records(records)

    def delete_record(self, record):
        records = self.load_records()
        if record in records:
            records.remove(record)
            self.save_records(records)
            return True
        return False

# Main Application
class GUIApp:
    def __init__(self, root, role):
        self.root = root
        self.role = role  # Admin or User
        self.root.title("Record Management System")
        self.record_manager = RecordManager()
        self.setup_menu()

    def setup_menu(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set the fixed window size
        window_width = 600
        window_height = 400
        
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate the x and y coordinates to center the window
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        
        # Position the window at the center
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(self.root, text="PYPURR", font=("Helvetica", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Main Frame to hold buttons
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Button Configuration
        button_font = ("Helvetica", 16)
        button_width = 10
        button_height = 2
        
        # Create buttons based on role
        if self.role == "admin":
            # Admin has all 4 buttons
            btn_record = tk.Button(main_frame, text="RECORD", font=button_font, 
                                   width=button_width, height=button_height, command=self.add_new_record)
            btn_record.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            
            btn_view_all = tk.Button(main_frame, text="VIEW ALL", font=button_font, 
                                    width=button_width, height=button_height, command=self.view_records)
            btn_view_all.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            
            btn_delete = tk.Button(main_frame, text="DELETE", font=button_font, 
                                  width=button_width, height=button_height, command=self.delete_record)
            btn_delete.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
            
            btn_search = tk.Button(main_frame, text="SEARCH", font=button_font, 
                                  width=button_width, height=button_height, command=self.search_record)
            btn_search.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
            
        else:
            # User has only 2 buttons - center them
            btn_view_all = tk.Button(main_frame, text="VIEW ALL", font=button_font, 
                                    width=button_width, height=button_height, command=self.view_records)
            btn_view_all.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
            
            btn_search = tk.Button(main_frame, text="SEARCH", font=button_font, 
                                  width=button_width, height=button_height, command=self.search_record)
            btn_search.grid(row=1, column=0, columnspan=2, padx=20, pady=20)
        
        # Exit button for both roles
        btn_exit = tk.Button(self.root, text="EXIT", font=button_font, 
                            width=button_width, height=1, command=self.root.quit)
        btn_exit.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_new_record(self):
        def submit():
            first_name = entry_first_name.get()
            middle_name = entry_middle_name.get()
            last_name = entry_last_name.get()
            birthday = entry_birthday.get()
            gender = gender_var.get()

            if not first_name or not last_name or not birthday or not gender:
                messagebox.showerror("Error", "All fields are required!")
                return
            
            # Validate date format
            if not self.validate_date(birthday):
                messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD format.")
                return
            
            record = [first_name, middle_name, last_name, birthday, gender]
            self.record_manager.add_record(record)
            messagebox.showinfo("Success", "Record added successfully!")
            add_record_window.destroy()

        add_record_window = tk.Toplevel(self.root)
        add_record_window.title("Add New Record")
        add_record_window.geometry("500x400")

        font_style = ("Helvetica", 14)
        padding = {"padx": 10, "pady": 10}

        tk.Label(add_record_window, text="First Name:", font=font_style).grid(row=0, column=0, **padding)
        entry_first_name = tk.Entry(add_record_window, font=font_style)
        entry_first_name.grid(row=0, column=1, **padding)

        tk.Label(add_record_window, text="Middle Name:", font=font_style).grid(row=1, column=0, **padding)
        entry_middle_name = tk.Entry(add_record_window, font=font_style)
        entry_middle_name.grid(row=1, column=1, **padding)

        tk.Label(add_record_window, text="Last Name:", font=font_style).grid(row=2, column=0, **padding)
        entry_last_name = tk.Entry(add_record_window, font=font_style)
        entry_last_name.grid(row=2, column=1, **padding)

        tk.Label(add_record_window, text="Birthday (YYYY-MM-DD):", font=font_style).grid(row=3, column=0, **padding)
        entry_birthday = tk.Entry(add_record_window, font=font_style)
        entry_birthday.grid(row=3, column=1, **padding)

        tk.Label(add_record_window, text="Gender:", font=font_style).grid(row=4, column=0, **padding)
        gender_var = tk.StringVar(value="Male")
        gender_dropdown = ttk.Combobox(add_record_window, textvariable=gender_var, values=["Male", "Female", "Rather not say"], font=font_style)
        gender_dropdown.grid(row=4, column=1, **padding)

        tk.Button(add_record_window, text="Submit", font=font_style, command=submit).grid(row=5, column=0, columnspan=2, **padding)

    def view_records(self):
        records = self.record_manager.load_records()
        messagebox.showinfo("Records", "\n".join([" | ".join(record) for record in records]))

    def search_record(self):
        search_term = simpledialog.askstring("Search", "Enter first name or last name:")
        if not search_term:
            return
        
        records = self.record_manager.load_records()
        found = [r for r in records if search_term.lower() in [r[0].lower(), r[2].lower()]]
        messagebox.showinfo("Search Results", "\n".join([" | ".join(r) for r in found]) if found else "No records found.")

    def delete_record(self):
        search_term = simpledialog.askstring("Delete", "Enter first name or last name to delete:")
        if not search_term:
            return
        
        records = self.record_manager.load_records()
        filtered_records = [r for r in records if search_term.lower() in [r[0].lower(), r[2].lower()]]
        
        if not filtered_records:
            messagebox.showerror("Error", "Record not found!")
            return
        
        if self.record_manager.delete_record(filtered_records[0]):
            messagebox.showinfo("Success", "Record deleted successfully!")

# Login Window
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")

        tk.Label(root, text="Username:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password:").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.check_login).pack()

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin":
            self.root.destroy()
            root = tk.Tk()
            GUIApp(root, "admin")
            root.mainloop()
        elif username == "user" and password == "user":
            self.root.destroy()
            root = tk.Tk()
            GUIApp(root, "user")
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

# Run the login window
root = tk.Tk()
LoginWindow(root)
root.mainloop()