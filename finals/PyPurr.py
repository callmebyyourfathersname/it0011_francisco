import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage
import json
import os
from datetime import datetime

# Constants
RECORDS_FILE = "records.json"
THEME_COLOR = "#3498db"
BG_COLOR = "#ecf0f1"
TEXT_COLOR = "#2c3e50"

class RecordManager:
    def __init__(self, filename=RECORDS_FILE):
        self.filename = filename
        
    def load_records(self):
        """Load records from JSON file"""
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except:
            return []

    def save_records(self, records):
        """Save records to JSON file"""
        with open(self.filename, "w") as file:
            json.dump(records, file, indent=4)

    def add_record(self, record):
        """Add a new record"""
        records = self.load_records()
        records.append(record)
        self.save_records(records)
        return True

    def search_records(self, search_term):
        """Search records by first or last name"""
        records = self.load_records()
        search_term = search_term.lower()
        return [r for r in records if search_term in r["first_name"].lower() 
                or search_term in r["last_name"].lower()]


class RecordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Record Management System")
        self.root.geometry("700x500")
        self.root.configure(bg=BG_COLOR)
        
        # Center window
        self.center_window(700, 500)
        
        self.record_manager = RecordManager()
        
        # Configure styles
        self.setup_styles()
        
        # Create main UI
        self.create_main_menu()
    
    def center_window(self, width, height):
        """Center the window on the screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_styles(self):
        """Configure ttk styles for UI"""
        style = ttk.Style()
        style.configure("TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("Treeview", font=("Helvetica", 11), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        
    def create_main_menu(self):
        """Create the main menu interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Header
        header_frame = tk.Frame(self.root, bg=THEME_COLOR, height=80)
        header_frame.pack(fill=tk.X)
        
        # Try to load a logo image
        try:
            # Replace "logo.png" with your actual logo file
            logo_img = PhotoImage(file="logo.png")
            logo_label = tk.Label(header_frame, image=logo_img, bg=THEME_COLOR)
            logo_label.image = logo_img  # Keep a reference
            logo_label.pack(pady=10)
        except:
            # Fallback to text
            title_label = tk.Label(header_frame, text="Record Management System", 
                                  font=("Helvetica", 20, "bold"), bg=THEME_COLOR, fg="white")
            title_label.pack(pady=20)
        
        # Main buttons frame
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=30)
        
        # Create menu buttons
        buttons = [
            ("Sign Up", self.show_signup_form),
            ("View All Records", self.view_records),
            ("Search Records", self.search_records),
            ("Exit", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, font=("Helvetica", 14), 
                          bg=THEME_COLOR, fg="white", padx=20, pady=10,
                          command=command, relief=tk.RAISED, borderwidth=2)
            btn.pack(fill=tk.X, pady=10)
            # Add hover effect
            btn.bind("<Enter>", lambda e, btn=btn: btn.config(bg="#2980b9"))
            btn.bind("<Leave>", lambda e, btn=btn: btn.config(bg=THEME_COLOR))
    
    def validate_form(self, fields):
        """Validate form fields"""
        # Check required fields
        if not fields["first_name"] or not fields["last_name"] or not fields["birthday"]:
            messagebox.showerror("Error", "First name, last name and birthday are required!")
            return False
        
        # Validate date format
        try:
            datetime.strptime(fields["birthday"], "%Y-%m-%d")
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
            return False
    
    def show_signup_form(self):
        """Display signup form window"""
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.geometry("500x400")
        signup_window.configure(bg=BG_COLOR)
        signup_window.transient(self.root)
        signup_window.grab_set()  # Modal window
        
        # Center the window
        self.center_window_on_parent(signup_window, 500, 400)
        
        # Header
        header = tk.Frame(signup_window, bg=THEME_COLOR)
        header.pack(fill=tk.X)
        tk.Label(header, text="Sign Up Form", font=("Helvetica", 16, "bold"), 
               bg=THEME_COLOR, fg="white").pack(pady=10)
        
        # Form frame
        form = tk.Frame(signup_window, bg=BG_COLOR)
        form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Form fields
        fields = {}
        row = 0
        
        # Define field mappings for consistent key naming
        field_mappings = {
            "First Name": "first_name",
            "Middle Name": "middle_name",
            "Last Name": "last_name",
            "Birthday (YYYY-MM-DD)": "birthday",
            "Gender": "gender"
        }
        
        for field, field_key in field_mappings.items():
            tk.Label(form, text=f"{field}:", bg=BG_COLOR).grid(row=row, column=0, sticky="e", padx=10, pady=10)
            
            if field == "Gender":
                var = tk.StringVar(value="Male")
                dropdown = ttk.Combobox(form, textvariable=var, values=["Male", "Female", "Other"], state="readonly")
                dropdown.grid(row=row, column=1, sticky="w", padx=10, pady=10)
                fields[field_key] = var
            else:
                entry = tk.Entry(form, font=("Helvetica", 12))
                entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
                fields[field_key] = entry
            
            row += 1
        
        # Buttons
        btn_frame = tk.Frame(form, bg=BG_COLOR)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        def submit_form():
            # Get values from form
            form_data = {
                "first_name": fields["first_name"].get().strip(),
                "middle_name": fields["middle_name"].get().strip(),
                "last_name": fields["last_name"].get().strip(),
                "birthday": fields["birthday"].get().strip(),
                "gender": fields["gender"].get()
            }
            
            if self.validate_form(form_data):
                if self.record_manager.add_record(form_data):
                    messagebox.showinfo("Success", "Record added successfully!")
                    signup_window.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save record!")
        
        tk.Button(btn_frame, text="Submit", bg=THEME_COLOR, fg="white", 
                font=("Helvetica", 12), padx=10, pady=5, command=submit_form).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Cancel", bg=THEME_COLOR, fg="white",
                font=("Helvetica", 12), padx=10, pady=5, command=signup_window.destroy).pack(side=tk.LEFT, padx=10)
    
    def center_window_on_parent(self, window, width, height):
        """Center a window relative to its parent"""
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_record_table(self, parent, records):
        """Create a table to display records"""
        # Create treeview
        columns = ("First Name", "Middle Name", "Last Name", "Birthday", "Gender")
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        # Set column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add records
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
        
        return tree
    
    def view_records(self):
        """Show all records"""
        view_window = tk.Toplevel(self.root)
        view_window.title("All Records")
        view_window.geometry("800x500")
        view_window.configure(bg=BG_COLOR)
        
        # Center the window
        self.center_window_on_parent(view_window, 800, 500)
        
        # Header
        header = tk.Frame(view_window, bg=THEME_COLOR)
        header.pack(fill=tk.X)
        tk.Label(header, text="All Records", font=("Helvetica", 16, "bold"), 
               bg=THEME_COLOR, fg="white").pack(pady=10)
        
        # Table frame
        table_frame = tk.Frame(view_window, bg=BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create table
        records = self.record_manager.load_records()
        self.create_record_table(table_frame, records)
        
        # Close button
        tk.Button(view_window, text="Close", bg=THEME_COLOR, fg="white",
                font=("Helvetica", 12), padx=10, pady=5, command=view_window.destroy).pack(pady=10)
    
    def search_records(self):
        """Search for records"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Records")
        search_window.geometry("800x500")
        search_window.configure(bg=BG_COLOR)
        
        # Center the window
        self.center_window_on_parent(search_window, 800, 500)
        
        # Header
        header = tk.Frame(search_window, bg=THEME_COLOR)
        header.pack(fill=tk.X)
        tk.Label(header, text="Search Records", font=("Helvetica", 16, "bold"), 
               bg=THEME_COLOR, fg="white").pack(pady=10)
        
        # Search frame
        search_frame = tk.Frame(search_window, bg=BG_COLOR)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(search_frame, text="Search by name:", bg=BG_COLOR).pack(side=tk.LEFT, padx=5)
        search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = tk.Frame(search_window, bg=BG_COLOR)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create empty table
        tree = self.create_record_table(results_frame, [])
        
        def perform_search():
            # Clear current results
            for item in tree.get_children():
                tree.delete(item)
                
            search_term = search_entry.get().strip()
            if not search_term:
                messagebox.showinfo("Info", "Please enter a search term")
                return
                
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
        
        # Search button
        tk.Button(search_frame, text="Search", bg=THEME_COLOR, fg="white",
                font=("Helvetica", 12), padx=10, pady=5, command=perform_search).pack(side=tk.LEFT, padx=5)
        
        # Close button
        tk.Button(search_window, text="Close", bg=THEME_COLOR, fg="white",
                font=("Helvetica", 12), padx=10, pady=5, command=search_window.destroy).pack(pady=10)

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = RecordApp(root)
    root.mainloop()