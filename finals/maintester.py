import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk  # For furry image
import os
import re  # For validating birthday format

# File to store records
RECORDS_FILE = "records.txt"

# Base class for Person
class Person:
    def __init__(self, first_name, middle_name, last_name, birthday, gender):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.birthday = birthday
        self.gender = gender

    def __str__(self):
        return f"{self.first_name},{self.middle_name},{self.last_name},{self.birthday},{self.gender}"

# Derived class for Admin
class Admin(Person):
    def delete_record(self, record_manager, record):
        try:
            records = record_manager.load_records()
            if record in records:
                records.remove(record)
                record_manager.save_records(records)
                messagebox.showinfo("Success", "Record deleted successfully!")
            else:
                messagebox.showerror("Error", "Record not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record: {e}")

# Derived class for User
class User(Person):
    pass  # Users have no additional functionality in this example

# Class for record management
class RecordManager:
    def __init__(self, filename="records.txt"):
        self._filename = filename  # Encapsulated attribute

    def load_records(self):
        """Load records from the file."""
        try:
            if not os.path.exists(self._filename):
                return []
            with open(self._filename, "r") as file:
                records = [line.strip().split(",") for line in file.readlines()]
            return records
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load records: {e}")
            return []

    def save_records(self, records):
        """Save records to the file."""
        try:
            with open(self._filename, "w") as file:
                for record in records:
                    file.write(",".join(record) + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save records: {e}")

    def add_record(self, record):
        """Add a new record."""
        try:
            records = self.load_records()
            records.append(record)
            self.save_records(records)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add record: {e}")

    def search_records(self, search_term):
        """Search for records matching the search term."""
        try:
            records = self.load_records()
            return [record for record in records if any(search_term.lower() in field.lower() for field in record)]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search records: {e}")
            return []

# Class for GUI application
class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Record Management System")
        self.root.geometry("800x500")
        self.record_manager = RecordManager()
        self.setup_background()
        self.setup_menu()

    def setup_background(self):
        """Set up the furry image."""
        try:
            self.bg_image = Image.open("furry.jpg")  # Replace with your image path
            self.bg_image = self.bg_image.resize((800, 500), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load furry image: {e}")

    def setup_menu(self):
        """Set up the menu for the application."""
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, font=("Helvetica", 12))
        menu.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="Sign Up", command=self.sign_up)
        file_menu.add_command(label="View All Records", command=self.view_records)
        file_menu.add_command(label="Search a Record", command=self.search_record)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

    def sign_up(self):
        """Open the sign-up form."""
        def submit():
            try:
                first_name = entry_first_name.get()
                middle_name = entry_middle_name.get()
                last_name = entry_last_name.get()
                birthday = entry_birthday.get()
                gender = gender_var.get()

                # Validate birthday format (YYYY-MM-DD)
                if not re.match(r"^\d{4}-\d{2}-\d{2}$", birthday):
                    raise ValueError("Birthday must be in the format YYYY-MM-DD and contain only digits.")

                if not first_name or not last_name or not birthday or not gender:
                    raise ValueError("All fields are required!")

                record = [first_name, middle_name, last_name, birthday, gender]
                self.record_manager.add_record(record)
                messagebox.showinfo("Success", "Record added successfully!")
                sign_up_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to submit form: {e}")

        sign_up_window = tk.Toplevel(self.root)
        sign_up_window.title("Sign Up")
        sign_up_window.geometry("500x400")

        # furry Image
        try:
            bg_image = Image.open("furry.jpg")  # Replace with your image path
            bg_image = bg_image.resize((500, 400), Image.Resampling.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(sign_up_window, image=bg_photo)
            bg_label.place(relwidth=1, relheight=1)
            bg_label.image = bg_photo  # Keep a reference
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load furry image: {e}")

        # Font and Padding
        font_style = ("Helvetica", 14)
        padding = {"padx": 10, "pady": 10}

        tk.Label(sign_up_window, text="First Name:", font=font_style, bg="white").grid(row=0, column=0, **padding)
        entry_first_name = tk.Entry(sign_up_window, font=font_style)
        entry_first_name.grid(row=0, column=1, **padding)

        tk.Label(sign_up_window, text="Middle Name:", font=font_style, bg="white").grid(row=1, column=0, **padding)
        entry_middle_name = tk.Entry(sign_up_window, font=font_style)
        entry_middle_name.grid(row=1, column=1, **padding)

        tk.Label(sign_up_window, text="Last Name:", font=font_style, bg="white").grid(row=2, column=0, **padding)
        entry_last_name = tk.Entry(sign_up_window, font=font_style)
        entry_last_name.grid(row=2, column=1, **padding)

        tk.Label(sign_up_window, text="Birthday (YYYY-MM-DD):", font=font_style, bg="white").grid(row=3, column=0, **padding)
        entry_birthday = tk.Entry(sign_up_window, font=font_style)
        entry_birthday.grid(row=3, column=1, **padding)

        tk.Label(sign_up_window, text="Gender:", font=font_style, bg="white").grid(row=4, column=0, **padding)
        gender_var = tk.StringVar(value="Male")  # Default value
        gender_dropdown = ttk.Combobox(sign_up_window, textvariable=gender_var, values=["Male", "Female", "Rather not say"], font=font_style)
        gender_dropdown.grid(row=4, column=1, **padding)

        tk.Button(sign_up_window, text="Submit", font=font_style, command=submit).grid(row=5, column=0, columnspan=2, **padding)

    def view_records(self):
        """Display all records."""
        try:
            records = self.record_manager.load_records()
            if not records:
                messagebox.showinfo("Records", "No records found!")
                return

            records_window = tk.Toplevel(self.root)
            records_window.title("All Records")
            records_window.geometry("600x400")

            # furry Image
            try:
                bg_image = Image.open("furry.jpg")  # Replace with your image path
                bg_image = bg_image.resize((600, 400), Image.Resampling.LANCZOS)
                bg_photo = ImageTk.PhotoImage(bg_image)
                bg_label = tk.Label(records_window, image=bg_photo)
                bg_label.place(relwidth=1, relheight=1)
                bg_label.image = bg_photo  # Keep a reference
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load furry image: {e}")

            # Font and Padding
            font_style = ("Helvetica", 14)
            padding = {"padx": 10, "pady": 10}

            for i, record in enumerate(records):
                tk.Label(records_window, text=f"Record {i+1}: {', '.join(record)}", font=font_style, bg="white").pack(**padding)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view records: {e}")

    def search_record(self):
        """Search for a specific record."""
        try:
            search_term = simpledialog.askstring("Search", "Enter search term:")
            if not search_term:
                return

            found_records = self.record_manager.search_records(search_term)
            if not found_records:
                messagebox.showinfo("Search Result", "No matching records found!")
                return

            search_window = tk.Toplevel(self.root)
            search_window.title("Search Results")
            search_window.geometry("600x400")

            # furry Image
            try:
                bg_image = Image.open("furry.jpg")  # Replace with your image path
                bg_image = bg_image.resize((600, 400), Image.Resampling.LANCZOS)
                bg_photo = ImageTk.PhotoImage(bg_image)
                bg_label = tk.Label(search_window, image=bg_photo)
                bg_label.place(relwidth=1, relheight=1)
                bg_label.image = bg_photo  # Keep a reference
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load furry image: {e}")

            # Font and Padding
            font_style = ("Helvetica", 14)
            padding = {"padx": 10, "pady": 10}

            for i, record in enumerate(found_records):
                tk.Label(search_window, text=f"Record {i+1}: {', '.join(record)}", font=font_style, bg="white").pack(**padding)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search records: {e}")

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()