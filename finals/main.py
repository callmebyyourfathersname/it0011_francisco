import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, PhotoImage
import os
from datetime import datetime
import json
from tkinter.font import Font

# Constants
RECORDS_FILE = "records.json"
THEME_COLOR = "#3498db"  # Primary blue color
SECONDARY_COLOR = "#2980b9"  # Darker blue for contrast
BG_COLOR = "#ecf0f1"  # Light background
TEXT_COLOR = "#2c3e50"  # Dark text for readability

# Base class for Person
class Person:
    def __init__(self, first_name, middle_name, last_name, birthday, gender):
        self._first_name = first_name  # Protected
        self._middle_name = middle_name
        self._last_name = last_name
        self._birthday = birthday
        self._gender = gender

    def to_dict(self):
        """Convert person data to dictionary for JSON storage"""
        return {
            "first_name": self._first_name,
            "middle_name": self._middle_name,
            "last_name": self._last_name,
            "birthday": self._birthday,
            "gender": self._gender
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Person instance from dictionary"""
        return cls(
            data["first_name"],
            data["middle_name"],
            data["last_name"],
            data["birthday"],
            data["gender"]
        )

    def __str__(self):
        return f"{self._first_name} {self._middle_name} {self._last_name}"

# Admin class with full control
class Admin(Person):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._role = "admin"
    
    def to_dict(self):
        data = super().to_dict()
        data["role"] = self._role
        return data

# User class with limited privileges
class User(Person):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._role = "user"
    
    def to_dict(self):
        data = super().to_dict()
        data["role"] = self._role
        return data

# Record Manager with private filename
class RecordManager:
    def __init__(self, filename=RECORDS_FILE):
        self.__filename = filename  # Private

    def load_records(self):
        """Load records from JSON file"""
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupted or doesn't exist, return empty list
            return []

    def save_records(self, records):
        """Save records to JSON file"""
        with open(self.__filename, "w") as file:
            json.dump(records, file, indent=4)

    def add_record(self, record):
        """Add a new record"""
        records = self.load_records()
        records.append(record)
        self.save_records(records)
        return True

    def delete_record(self, record_to_delete):
        """Delete a record by comparing all fields"""
        records = self.load_records()
        # Find matching record
        for i, record in enumerate(records):
            if (record["first_name"].lower() == record_to_delete["first_name"].lower() and
                record["last_name"].lower() == record_to_delete["last_name"].lower()):
                del records[i]
                self.save_records(records)
                return True
        return False

    def search_records(self, search_term):
        """Search records by first or last name"""
        records = self.load_records()
        search_term = search_term.lower()
        return [r for r in records if search_term in r["first_name"].lower() 
                or search_term in r["last_name"].lower()]

# Custom styles and widgets
class CustomButton(tk.Button):
    """Custom styled button for consistent UI"""
    def __init__(self, master, **kwargs):
        kwargs.setdefault('bg', THEME_COLOR)
        kwargs.setdefault('fg', 'white')
        kwargs.setdefault('activebackground', SECONDARY_COLOR)
        kwargs.setdefault('activeforeground', 'white')
        kwargs.setdefault('relief', tk.RAISED)
        kwargs.setdefault('borderwidth', 2)
        kwargs.setdefault('padx', 10)
        kwargs.setdefault('pady', 5)
        super().__init__(master, **kwargs)
        
        # Hover effect
        self.bind("<Enter>", lambda e: self.config(bg=SECONDARY_COLOR))
        self.bind("<Leave>", lambda e: self.config(bg=THEME_COLOR))

# Main Application
class GUIApp:
    def __init__(self, root, role):
        self.root = root
        self.role = role  # Admin or User
        self.root.title("PYPURR - Record Management System")
        self.root.configure(bg=BG_COLOR)
        
        # Set app icon (placeholder)
        try:
            # This would be replaced with your actual icon
            self.root.iconbitmap("furry.jpg")
        except:
            pass  # Silently fail if icon not found
            
        self.record_manager = RecordManager()
        
        # Configure ttk styles
        self.setup_styles()
        
        # Setup main UI
        self.setup_menu()

    def setup_styles(self):
        """Configure ttk styles for consistent UI"""
        style = ttk.Style()
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12), background=THEME_COLOR)
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TCombobox", font=("Helvetica", 12))
        style.configure("Treeview", font=("Helvetica", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

    def setup_menu(self):
        """Setup the main application interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set the fixed window size
        window_width = 800
        window_height = 600
        
        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate the x and y coordinates to center the window
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        
        # Position the window at the center
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Configure grid
        for i in range(5):
            self.root.rowconfigure(i, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        
        # Create header frame
        header_frame = tk.Frame(self.root, bg=THEME_COLOR, height=100)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="new")
        header_frame.pack_propagate(False)
        
        # Add logo placeholder
        # Add logo 
        try:
            # Lo    ad your image
            logo_image = PhotoImage(file="furry.jpg")
            logo_label = tk.Label(header_frame, image=logo_image, bg=THEME_COLOR)
            logo_label.image = logo_image  # Keep a reference to prevent garbage collection
            logo_label.pack(side=tk.LEFT, padx=20)
    
            # Display role information
            role_label = tk.Label(header_frame, text=f"Role: {self.role.capitalize()}", 
                                 bg=THEME_COLOR, fg="white", font=("Helvetica", 14))
            role_label.pack(side=tk.RIGHT, padx=20)
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback if image loading fails
            title_label = tk.Label(header_frame, text="PYPURR", bg=THEME_COLOR, fg="white",
                                  font=("Helvetica", 32, "bold"))
            title_label.pack(pady=20)
        # Main Frame to hold buttons with proper spacing
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
        
        for i in range(2):
            main_frame.rowconfigure(i, weight=1)
            main_frame.columnconfigure(i, weight=1)
        
        # Button Configuration
        button_font = ("Helvetica", 16)
        button_width = 15
        button_height = 2
        
        # Create buttons based on role
        if self.role == "admin":
            # Admin has all 4 buttons
            btn_record = CustomButton(main_frame, text="ADD RECORD", font=button_font, 
                                    width=button_width, height=button_height, command=self.add_new_record)
            btn_record.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
            
            btn_view_all = CustomButton(main_frame, text="VIEW ALL RECORDS", font=button_font, 
                                      width=button_width, height=button_height, command=self.view_records)
            btn_view_all.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            
            btn_delete = CustomButton(main_frame, text="DELETE RECORD", font=button_font, 
                                    width=button_width, height=button_height, command=self.delete_record)
            btn_delete.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
            
            btn_search = CustomButton(main_frame, text="SEARCH RECORDS", font=button_font, 
                                    width=button_width, height=button_height, command=self.search_record)
            btn_search.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
            
        else:
            # User has only 2 buttons - center them
            btn_view_all = CustomButton(main_frame, text="VIEW ALL RECORDS", font=button_font, 
                                      width=button_width, height=button_height, command=self.view_records)
            btn_view_all.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
            
            btn_search = CustomButton(main_frame, text="SEARCH RECORDS", font=button_font, 
                                    width=button_width, height=button_height, command=self.search_record)
            btn_search.grid(row=1, column=0, columnspan=2, padx=20, pady=20)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg=SECONDARY_COLOR, height=30)
        status_frame.grid(row=3, column=0, columnspan=2, sticky="sew")
        status_label = tk.Label(status_frame, text="Ready", bg=SECONDARY_COLOR, fg="white", anchor="w")
        status_label.pack(side=tk.LEFT, padx=10)
        
        # Exit button
        btn_exit = CustomButton(self.root, text="EXIT", font=button_font, 
                              width=button_width, height=1, command=self.root.quit)
        btn_exit.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

    def validate_date(self, date_str):
        """Validate date format YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_new_record(self):
        """Open window to add a new record"""
        def submit():
            first_name = entry_first_name.get().strip()
            middle_name = entry_middle_name.get().strip()
            last_name = entry_last_name.get().strip()
            birthday = entry_birthday.get().strip()
            gender = gender_var.get()

            # Form validation
            if not first_name or not last_name or not birthday or not gender:
                messagebox.showerror("Error", "All fields except Middle Name are required!")
                return
            
            # Validate date format
            if not self.validate_date(birthday):
                messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD format.")
                return
            
            # Create record as dictionary for JSON storage
            record = {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "birthday": birthday,
                "gender": gender
            }
            
            if self.record_manager.add_record(record):
                messagebox.showinfo("Success", "Record added successfully!")
                add_record_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to add record!")

        add_record_window = tk.Toplevel(self.root)
        add_record_window.title("Add New Record")
        add_record_window.geometry("500x400")
        add_record_window.configure(bg=BG_COLOR)
        add_record_window.transient(self.root)  # Set as dialog
        add_record_window.grab_set()  # Modal behavior

        font_style = ("Helvetica", 12)
        padding = {"padx": 10, "pady": 10}
        
        # Header with image placeholder
        header_frame = tk.Frame(add_record_window, bg=THEME_COLOR)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        header_label = tk.Label(header_frame, text="Add New Record", 
                              font=("Helvetica", 16, "bold"), bg=THEME_COLOR, fg="white")
        header_label.pack(pady=10)

        # Form fields
        form_frame = tk.Frame(add_record_window, bg=BG_COLOR)
        form_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # First Name
        tk.Label(form_frame, text="First Name:", font=font_style, bg=BG_COLOR).grid(row=0, column=0, **padding, sticky="e")
        entry_first_name = tk.Entry(form_frame, font=font_style)
        entry_first_name.grid(row=0, column=1, **padding, sticky="w")

        # Middle Name
        tk.Label(form_frame, text="Middle Name:", font=font_style, bg=BG_COLOR).grid(row=1, column=0, **padding, sticky="e")
        entry_middle_name = tk.Entry(form_frame, font=font_style)
        entry_middle_name.grid(row=1, column=1, **padding, sticky="w")

        # Last Name
        tk.Label(form_frame, text="Last Name:", font=font_style, bg=BG_COLOR).grid(row=2, column=0, **padding, sticky="e")
        entry_last_name = tk.Entry(form_frame, font=font_style)
        entry_last_name.grid(row=2, column=1, **padding, sticky="w")

        # Birthday
        tk.Label(form_frame, text="Birthday (YYYY-MM-DD):", font=font_style, bg=BG_COLOR).grid(row=3, column=0, **padding, sticky="e")
        entry_birthday = tk.Entry(form_frame, font=font_style)
        entry_birthday.grid(row=3, column=1, **padding, sticky="w")

        # Gender
        tk.Label(form_frame, text="Gender:", font=font_style, bg=BG_COLOR).grid(row=4, column=0, **padding, sticky="e")
        gender_var = tk.StringVar(value="Male")
        gender_dropdown = ttk.Combobox(form_frame, textvariable=gender_var, 
                                      values=["Male", "Female", "Non-binary", "Rather not say"], 
                                      font=font_style, state="readonly")
        gender_dropdown.grid(row=4, column=1, **padding, sticky="w")

        # Buttons frame
        button_frame = tk.Frame(add_record_window, bg=BG_COLOR)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        submit_btn = CustomButton(button_frame, text="Submit", font=font_style, command=submit)
        submit_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = CustomButton(button_frame, text="Cancel", font=font_style, 
                                command=add_record_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def view_records(self):
        """Display all records in a scrollable table"""
        view_window = tk.Toplevel(self.root)
        view_window.title("View All Records")
        view_window.geometry("800x500")
        view_window.configure(bg=BG_COLOR)
        view_window.transient(self.root)  # Set as dialog
        
        # Header
        header_frame = tk.Frame(view_window, bg=THEME_COLOR)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(header_frame, text="All Records", font=("Helvetica", 16, "bold"), 
                              bg=THEME_COLOR, fg="white")
        header_label.pack(pady=10)
        
        # Table frame
        table_frame = tk.Frame(view_window, bg=BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ("First Name", "Middle Name", "Last Name", "Birthday", "Gender")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Load records
        records = self.record_manager.load_records()
        if not records:
            tree.insert("", tk.END, values=("No records found", "", "", "", ""))
        else:
            for record in records:
                tree.insert("", tk.END, values=(
                    record["first_name"],
                    record["middle_name"],
                    record["last_name"],
                    record["birthday"],
                    record["gender"]
                ))
        
        # Close button
        close_button = CustomButton(view_window, text="Close", command=view_window.destroy)
        close_button.pack(pady=10)

    def search_record(self):
        """Search for records by first or last name"""
        def perform_search():
            search_term = search_entry.get().strip()
            if not search_term:
                messagebox.showinfo("Info", "Please enter a search term.")
                return
            
            # Clear previous results
            for item in tree.get_children():
                tree.delete(item)
            
            results = self.record_manager.search_records(search_term)
            if not results:
                tree.insert("", tk.END, values=("No matching records found", "", "", "", ""))
            else:
                for record in results:
                    tree.insert("", tk.END, values=(
                        record["first_name"],
                        record["middle_name"],
                        record["last_name"],
                        record["birthday"],
                        record["gender"]
                    ))
        
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Records")
        search_window.geometry("800x500")
        search_window.configure(bg=BG_COLOR)
        search_window.transient(self.root)
        
        # Header
        header_frame = tk.Frame(search_window, bg=THEME_COLOR)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(header_frame, text="Search Records", font=("Helvetica", 16, "bold"), 
                              bg=THEME_COLOR, fg="white")
        header_label.pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(search_window, bg=BG_COLOR)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        search_label = tk.Label(search_frame, text="Enter first or last name:", bg=BG_COLOR)
        search_label.pack(side=tk.LEFT, padx=5)
        
        search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = CustomButton(search_frame, text="Search", command=perform_search)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        result_frame = tk.Frame(search_window, bg=BG_COLOR)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for results
        columns = ("First Name", "Middle Name", "Last Name", "Birthday", "Gender")
        tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Default message
        tree.insert("", tk.END, values=("Enter search term and click Search", "", "", "", ""))
        
        # Close button
        close_button = CustomButton(search_window, text="Close", command=search_window.destroy)
        close_button.pack(pady=10)

    def delete_record(self):
        """Delete a record after confirmation"""
        def perform_search():
            search_term = search_entry.get().strip()
            if not search_term:
                messagebox.showinfo("Info", "Please enter a search term.")
                return
            
            # Clear previous results
            for item in tree.get_children():
                tree.delete(item)
            
            global results
            results = self.record_manager.search_records(search_term)
            if not results:
                tree.insert("", tk.END, values=("No matching records found", "", "", "", ""))
                delete_button.config(state=tk.DISABLED)
            else:
                for record in results:
                    tree.insert("", tk.END, values=(
                        record["first_name"],
                        record["middle_name"],
                        record["last_name"],
                        record["birthday"],
                        record["gender"]
                    ))
                delete_button.config(state=tk.NORMAL)
        
        def delete_selected():
            selection = tree.selection()
            if not selection:
                messagebox.showinfo("Info", "Please select a record to delete.")
                return
            
            # Get the index of the selected item
            index = tree.index(selection[0])
            if index >= len(results):
                messagebox.showerror("Error", "Invalid selection.")
                return
            
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete", 
                                        f"Are you sure you want to delete the record for {results[index]['first_name']} {results[index]['last_name']}?")
            if not confirm:
                return
            
            # Delete record
            if self.record_manager.delete_record(results[index]):
                messagebox.showinfo("Success", "Record deleted successfully!")
                # Refresh the list
                perform_search()
            else:
                messagebox.showerror("Error", "Failed to delete record.")
        
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Record")
        delete_window.geometry("800x500")
        delete_window.configure(bg=BG_COLOR)
        delete_window.transient(self.root)
        
        # Global variable to store search results
        global results
        results = []
        
        # Header
        header_frame = tk.Frame(delete_window, bg=THEME_COLOR)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(header_frame, text="Delete Records", font=("Helvetica", 16, "bold"), 
                              bg=THEME_COLOR, fg="white")
        header_label.pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(delete_window, bg=BG_COLOR)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        search_label = tk.Label(search_frame, text="Enter first or last name:", bg=BG_COLOR)
        search_label.pack(side=tk.LEFT, padx=5)
        
        search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        search_button = CustomButton(search_frame, text="Search", command=perform_search)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        result_frame = tk.Frame(delete_window, bg=BG_COLOR)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for results
        columns = ("First Name", "Middle Name", "Last Name", "Birthday", "Gender")
        tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Default message
        tree.insert("", tk.END, values=("Search for records to delete", "", "", "", ""))
        
        # Button frame
        button_frame = tk.Frame(delete_window, bg=BG_COLOR)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        delete_button = CustomButton(button_frame, text="Delete Selected", command=delete_selected, state=tk.DISABLED)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        close_button = CustomButton(button_frame, text="Close", command=delete_window.destroy)
        close_button.pack(side=tk.LEFT, padx=5)

# Login Window class with improved UI
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("PYPURR - Login")
        self.root.geometry("400x300")
        self.root.configure(bg=BG_COLOR)
        
        # Center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (400 / 2))
        y = int((screen_height / 2) - (300 / 2))
        self.root.geometry(f"400x300+{x}+{y}")
        
        # Create frames
        self.header_frame = tk.Frame(root, bg=THEME_COLOR)
        self.header_frame.pack(fill=tk.X)
        
        self.login_frame = tk.Frame(root, bg=BG_COLOR)
        self.login_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Header with logo placeholder
        self.title_label = tk.Label(self.header_frame, text="PYPURR", 
                                  font=("Helvetica", 24, "bold"), bg=THEME_COLOR, fg="white")
        self.title_label.pack(pady=10)
        
        # Login form
        tk.Label(self.login_frame, text="Username:", font=("Helvetica", 12), bg=BG_COLOR).pack(anchor="w", pady=(10, 5))
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12), width=30)
        self.username_entry.pack(fill=tk.X, pady=5)
        
        tk.Label(self.login_frame, text="Password:", font=("Helvetica", 12), bg=BG_COLOR).pack(anchor="w", pady=(10, 5))
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Helvetica", 12), width=30)
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Login button
        self.login_button = CustomButton(self.login_frame, text="Login", font=("Helvetica", 12), 
                                       command=self.check_login)
        self.login_button.pack(pady=20)
        
        # Instructions
        instructions = "Admin login: username=admin, password=admin\nUser login: username=user, password=user"
        tk.Label(self.login_frame, text=instructions, bg=BG_COLOR, font=("Helvetica", 8)).pack()
        
        # Bind enter key to login
        self.root.bind('<Return>', lambda event: self.check_login())

    def check_login(self):
        """Verify login credentials"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return
            
        if username == "admin" and password == "admin":
            self.root.destroy()
            root = tk.Tk()
            app = GUIApp(root, "admin")
            root.mainloop()
        elif username == "user" and password == "user":
            self.root.destroy()
            root = tk.Tk()
            app = GUIApp(root, "user")
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
            # Clear password field
            self.password_entry.delete(0, tk.END)
            # Focus on username field
            self.username_entry.focus_set()

# Application entry point
if __name__ == "__main__":
    # Create and configure the main application window
    root = tk.Tk()
    
    # Set app title
    root.title("PYPURR Login")
    
    # Try to set the app icon
    try:
        # This would be replaced with your actual icon
        root.iconbitmap("furry.jpg")
    except:
        pass  # Silently fail if icon not found
    
    # Initialize the login window
    login_window = LoginWindow(root)
    
    # Start the main event loop
    root.mainloop()