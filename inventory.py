import tabulate

class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"Country: {self.country}, Code: {self.code}, Product: {self.product}, Cost: {self.cost}, Quantity: {self.quantity}"

def read_shoes_data():
    shoe_data_list = []
    try:
        with open('inventory.txt', 'r') as read_shoes_file:
            next(read_shoes_file)  # Skip the first two lines
            next(read_shoes_file)
            for line in read_shoes_file:
                country, code, product, cost, quantity = line.strip().split(',')
                shoe_object = Shoe(country, code, product, float(cost), int(quantity))
                shoe_data_list.append(shoe_object)
    except FileNotFoundError:
        print("The inventory.txt file that needs to be accessed does not exist.")
    return shoe_data_list

def capture_shoes():
    country = input("Enter country:\n")
    code = input("Enter code:\n")
    product = input("Enter product name:\n")
    cost = float(input("Enter product cost:\n"))
    quantity = int(input("Enter product quantity:\n"))
    with open('inventory.txt', 'a') as shoe_file_addition:
        shoe_file_addition.write(f"\n{country},{code},{product},{cost},{quantity}")
    print("Shoe data added successfully.")
    return read_shoes_data()

def view_all():
    shoe_data_list = read_shoes_data()
    if shoe_data_list:
        headers = ["Country", "Code", "Product", "Cost", "Quantity"]
        table = tabulate.tabulate(
            [(shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity) for shoe in shoe_data_list],
            headers, tablefmt="fancy_grid"
        )
        print(table)
    else:
        print("No shoe data available.")

def re_stock():
    shoe_data_list = read_shoes_data()
    
    if not shoe_data_list:
        print("No shoe data available for restocking.")
        return

    # Find the shoe with the lowest quantity
    lowest_quantity_shoe = min(shoe_data_list, key=lambda shoe: shoe.quantity)

    print("Shoe with the lowest quantity:")
    print(lowest_quantity_shoe)

    try:
        quantity_to_add = int(input(f"Enter the quantity to add to restock {lowest_quantity_shoe.product}: "))
    except ValueError:
        print("Invalid input. Please enter a valid quantity.")
        return

    if quantity_to_add <= 0:
        print("Quantity to add must be greater than 0.")
        return

    # Update the quantity for the chosen shoe
    lowest_quantity_shoe.quantity += quantity_to_add

    # Update the file with the new quantity
    with open('inventory.txt', 'r') as file:
        lines = file.readlines()

    with open('inventory.txt', 'w') as file:
        for line in lines:
            country, code, product, cost, quantity = line.strip().split(',')
            if product == lowest_quantity_shoe.product:
                # Update the quantity in this line
                quantity = str(lowest_quantity_shoe.quantity)
            file.write(f"{country},{code},{product},{cost},{quantity}\n")

    print(f"{quantity_to_add} {lowest_quantity_shoe.product} added for restocking.")
    print("Inventory file updated.")
    print("Invetory updated.")
    

def shoe_search():
    shoe_code = input("Enter product code for the item your are searching for:\n")
    shoe_data_list = read_shoes_data()

    if not shoe_data_list:
        print("No shoe data available for searching.")
        return None

    # Find the shoe with the matching code
    for shoe in shoe_data_list:
        if shoe.code == shoe_code:
            print(shoe)
            break
    else:
        print(f"No shoe with code {shoe_code} found.")
# Calculate value of each product in stock
def value_per_item():
    shoe_data_list = read_shoes_data()
    for shoe in shoe_data_list:
        value = shoe.cost * shoe.quantity
        print(f"{shoe.product}: R{value}")
# Find the product with highest quantity count
def highest_qty():
    shoe_data_list = read_shoes_data()
    highest_quantity_shoe = max(shoe_data_list, key=lambda shoe: shoe.quantity)

    print(f"The shoe with the highest quantity is {highest_quantity_shoe.product}. This shoe is for sale!")


#==========Main Menu=============

while True:
    print('''Welcome to the inventory menu.
    1 - Capture new shoe data
    2 - View all shoes in stock information
    3 - Re-stock shoes
    4 - Search for a shoe
    5 - Calculate stock values
    6 - View shoe with highest quatity, to be on sale
    7 - Exit''')
    selection = input("Choose an applicable action and enter the number corresponding to it:\n")
    if selection == '1':
        capture_shoes()
    elif selection == '2':
        view_all()
    elif selection == '3':
        re_stock()
    elif selection == '4':
        shoe_search()
    elif selection == '5':
        value_per_item()
    elif selection == '6':
        highest_qty()
    elif selection == '7':
        print("Goodbye.")
    else:
        print("Invalid choice. Please select 1, 2, 3, 4, 5, 6, or 7.")