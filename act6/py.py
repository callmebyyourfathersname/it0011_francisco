class Item:
    def __init__(self, item_id, name, description, price):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.price = price

    def __str__(self):
        return f"ID: {self.item_id}, Name: {self.name}, Description: {self.description}, Price: ${self.price:.2f}"

class ItemManager:
    def __init__(self):
        self.items = {}

    def add_item(self, item_id, name, description, price):
        try:
            if item_id in self.items:
                raise ValueError("Item ID already exists.")
            if price < 0:
                raise ValueError("Price cannot be negative.")
            self.items[item_id] = Item(item_id, name, description, price)
            print("Item added successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def update_item(self, item_id, name=None, description=None, price=None):
        try:
            if item_id not in self.items:
                raise ValueError("Item ID not found.")
            if price is not None and price < 0:
                raise ValueError("Price cannot be negative.")
            
            item = self.items[item_id]
            if name:
                item.name = name
            if description:
                item.description = description
            if price is not None:
                item.price = price
            print("Item updated successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def delete_item(self, item_id):
        try:
            if item_id not in self.items:
                raise ValueError("Item ID not found.")
            del self.items[item_id]
            print("Item deleted successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def view_items(self):
        if not self.items:
            print("No items available.")
        else:
            for item in self.items.values():
                print(item)

if __name__ == "__main__":
    manager = ItemManager()
    while True:
        print("\nItem Management System")
        print("1. Add Item")
        print("2. Update Item")
        print("3. Delete Item")
        print("4. View Items")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                item_id = int(input("Enter Item ID: "))
                name = input("Enter Item Name: ")
                description = input("Enter Item Description: ")
                price = float(input("Enter Item Price: "))
                manager.add_item(item_id, name, description, price)
            except ValueError:
                print("Invalid input. Please enter correct values.")
        elif choice == "2":
            try:
                item_id = int(input("Enter Item ID to update: "))
                name = input("Enter new name (press enter to skip): ") or None
                description = input("Enter new description (press enter to skip): ") or None
                price_input = input("Enter new price (press enter to skip): ")
                price = float(price_input) if price_input else None
                manager.update_item(item_id, name, description, price)
            except ValueError:
                print("Invalid input. Please enter correct values.")
        elif choice == "3":
            try:
                item_id = int(input("Enter Item ID to delete: "))
                manager.delete_item(item_id)
            except ValueError:
                print("Invalid input. Please enter a valid Item ID.")
        elif choice == "4":
            manager.view_items()
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
