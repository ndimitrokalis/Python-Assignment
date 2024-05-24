from datetime import datetime
import csv
import shutil
import os

def get_staff():
    """
    Reads employees from the staff.csv file and returns a 
    dictionary with username as the key and a the respective user's
    credentials and classification as a value.
    """
    file = open("staff.csv")
    reader = csv.DictReader(file)
    users = {}
    for row in reader:
        users[row['username']] = row
    return users

def login():
    """
    Asks user for credentials and calls a fuction with the values to
    verify them. If it succeeds the user successfully login as the
    respected role, else it asks the user to try again.
    """
    users = get_staff()
    # Loops until the credentials are correct.
    while True:
        print("\nWelcome to Coffee Addict\n")
        username = input("Username: ").lower()
        password = input("Password: ")
        if username in users:
            if password == users[username]['password']:
                role = users[username]['role']
                # Welcomes the user with their respected role and name.
                print("\nWelcome", role.upper() , username.capitalize())
                break
            else:
                role = None
                print("\nYour username or password is wrong!\nPlease try again")
        else:
            role = None
            print("\nYour username or password is wrong!\nPlease try again")
    return username, role

def add_orders():
    """
    Creates a new order, reads the orders.csv file
    and assigns it a new ID then saves it back into
    the orders.csv file.
    """
    # Write customer's data and order's details
    name = str(input("\nEnter name: ")).lower()
    address = str(input("Enter address: ")).lower()
    description = str(input("Enter description: "))
    # Loops until date is given in correct format.
    while True:
        date = str(input("Enter date (YYYY/MM/DD): "))
        try:
            datetime_object = datetime.strptime(date, "%Y/%m/%d")
            date = datetime_object.strftime("%Y/%m/%d")
            break
        except ValueError:
            print("\nInvalid date format. Please enter the date in the format (YYYY/MM/DD)!\n")
    price = float(input("Enter price: "))
    completed = str(0)
    file = open("orders.csv", 'r+')
    reader = csv.DictReader(file)
    orders = {}
    for row in reader:
        orders[row['id']] = row
    order_id = len(orders) + 1
    file.write(f"{order_id},{name},{address},{description},{date},{price},{completed}\n")
    file.close
    print("\nOrder have been successfully added")

def get_pending_orders():
    """
    Reads orders from the orders.csv file and
    returns pending orders.
    """
    file = open("orders.csv")
    reader = csv.DictReader(file)
    print("\n<<PENDING ORDERS>>")
    for row in reader:
        if row['completed'] == '0':
            print("\nID:", row['id'] , "\nName:",row['name'], "\nAddress:", row['address'], "\nDescription:", row['description'], "\nDate:", row['date'], "\nPrice:", row['price'])
    file.close

def get_order_id(order_id):
    """
    Reads order's ID from the orders.csv file and looks for the ID
    the user has provided, if it finds it, it returns it else 
    returns value as None.
    """
    file = open("orders.csv")
    reader = csv.DictReader(file)
    for row in reader:
        if row['id'] == order_id:
            return row
    file.close()
    return None

def get_orders():
    """
    Reads orders from the orders.csv file and returns
    a dictionary with the customer's data and order's
    details.
    """
    file = open("orders.csv")
    reader = csv.DictReader(file)
    orders = {}
    for row in reader:
        orders[row['id']] = row
    file.close()
    return orders

def complete_orders():
    """
    Asks user for order's ID and calls for a function to
    look it up, if the ID exists, it returns the order and 
    checks if it is completed. If the order does not exist
    or it is completed it informs the user else it updates
    the order as completed.
    """
    order_id = str(input("\nEnter ID: "))
    order = get_order_id(order_id)
    # Checks if order exists.
    if order is None:
        print("\nThere is no pending order with such ID!")
        print("Please try again")
    # Checks if order is completed.
    elif order['completed'] == '1':
        print("\nThe order with the provided ID is already completed.")
    # Copies the values of the orders.csv in a temp file.
    else:
        temp_file = open("temp_orders.csv", "w")
        orders = get_orders()
        temp_file.write("id,name,address,description,date,price,completed\n")
        for key in orders:
            if key == order_id:
                # Updates the order as completed
                orders[key]['completed'] = '1'
                temp_file.write(key+','+orders[key]['name']+','
                                +orders[key]['address']+','
                                +orders[key]['description']+','
                                +orders[key]['date']+','
                                +orders[key]['price']+','
                                +orders[key]['completed']+'\n')
            else:
                temp_file.write(key+','+orders[key]['name']+','
                                +orders[key]['address']+','
                                +orders[key]['description']+','
                                +orders[key]['date']+','
                                +orders[key]['price']+','
                                +orders[key]['completed']+'\n')
        temp_file.close()
        # Overwrites orders.csv with new values.
        shutil.copyfile("temp_orders.csv", "orders.csv")
        # Deletes temp file.
        os.remove("temp_orders.csv")
        print("\nThe order has been successfully completed")

def get_number_of_orders_by_customer():
    """
    Reads orders from orders.csv file and counts
    number of orders by a given customer. If a
    customer doesn't exist warns the user.
    """
    file = open("orders.csv")
    reader = csv.DictReader(file)
    counter = 0
    name = str(input("\nGive name : ")).lower()
    for row in reader:
        if row['name'].lower() == name:
            counter += 1
    if counter == 1:
        print("\nThere is",counter,"order placed by",name.capitalize())
    elif counter > 1:
        print("\nThere are",counter,"orders placed by",name.capitalize())
    else:
        print("\nThere is no customer by that name!")
        print("Please try again")

def get_number_of_orders_by_day():
    """
    Reads orders from orders.csv file and counts
    number of orders placed on a specific day.
    """
    file = open("orders.csv")
    reader = csv.DictReader(file)
    counter = 0
    # Loop until user provides a date with the correct format.
    while True:
        date = str(input("Enter date (YYYY/MM/DD): "))
        try:
            datetime_object = datetime.strptime(date, "%Y/%m/%d")
            date = datetime_object.strftime("%Y/%m/%d")
            break
        except ValueError:
            print("\nInvalid date format. Please enter the date in the format (YYYY/MM/DD)!\n")
    for row in reader:
        if row['date'] == date:
            counter += 1
    if counter == 1:
        print("\nThere was",counter,"order placed in",date)
    elif counter > 1:
        print("\nThere were",counter,"orders placed in",date)
    else:
        print("\nThere were no orders placed in",date)

def get_revenue_of_delivered_orders():
    """
    Reads orders from orders.csv and saves in a
    dictionary the delivered orders, then it adds up
    the total amount and returns it to the user.
    """
    file = open("orders.csv")
    reader = csv.DictReader(file)
    revenue = 0
    for row in reader:
        if row['completed'] == '1':
            revenue += float(row['price'])
    print("\nThe total revenue of all delivered orders is",revenue,"$")

def get_revenue_of_placed_orders_by_customer():
    """
    Reads orders from orders.csv file and saves in a
    dictionary the orders placed in by a given customer,
    then adds up the total amount and returns it to user.
    If the customer provided doesn't exist it warns the user.
    """
    file = open("orders.csv")
    reader = csv.DictReader(file)
    revenue = 0
    name = str(input("\nGive name : ")).lower()
    for row in reader:
        if row['name'] == name:
            revenue += float(row['price'])
    if revenue == 0:
        print("\nThere is no customer by that name!")
        print("Please try again")
    else:
        print("\nThe total revenue of all orders placed by",name,"is",revenue,"$")

def get_revenue_of_placed_orders_by_day():
    """
    Reads orders from orders.csv file and saves in a
    dictionary the orders placed in a given date, then
    adds up the total amount of the orders and returns
    it to the user.
    """
    file = open("orders.csv")
    reader = csv.DictReader(file)
    revenue = 0
    # Loop until user provides date with correct format.
    while True:
        date = str(input("Enter date (YYYY/MM/DD): "))
        try:
            datetime_object = datetime.strptime(date, "%Y/%m/%d")
            date = datetime_object.strftime("%Y/%m/%d")
            break
        except ValueError:
            print("\nInvalid date format. Please enter the date in the format (YYYY/MM/DD)!\n")
    for row in reader:
        if row['date'] == date:
            revenue += float(row['price'])
    if revenue != 0:
        print("\nThe total revenue of all orders placed in",date,"is",revenue,"$")
    else:
        print("\nThere were no orders placed in",date)
    
def list_customer_names():
    """
    Reads customers from orders.csv and returns
    the unique names to the user.
    """
    file = open("orders.csv")
    reader = csv.DictReader(file)
    unique_names = []
    for row in reader:
        name = row['name']
        # Checks if the name of the customer is unique.
        if name not in unique_names:
            unique_names.append(name)
    print("\nCustomer Names:\n")
    for name in unique_names:
        print(name)

def list_number_of_orders_placed_per_customer():
    """
    Reads orders from orders.csv and returns a
    dictionary with the unique names of customers
    and the number of orders placed by them.
    """
    file = open("orders.csv", 'r')
    reader = csv.DictReader(file)
    statistics = {}
    for row in reader:
        name = row['name']
        if name in statistics:
            statistics[name] += 1
        else:
            statistics[name] = 1
    print("\nNumber of orders per customer:\n")
    for name, count in statistics.items():
        print(f"{name}: {count}")

def list_all_data():
    """
    Reads orders.csv file and returns all orders
    ever placed.
    """
    file = open("orders.csv")
    reader = csv.DictReader(file)
    for row in reader:
        print("\nID:", row['id'] , "|Name:",row['name'], "|Address:", row['address'], "|Description:", row['description'], "|Date:", row['date'], "|Price:", row['price'], "|completed = ",row['completed'])

def get_revenue_of_orders_per_day():
    """
    Reads orders from orders.csv file and saves
    in a dictionary all orders placed, then adds
    up the total amount per day and returns it to
    the user.
    """
    file = open("orders.csv", 'r')
    reader = csv.DictReader(file)
    statistics = {}
    for row in reader:
        date = row['date']
        price = float(row['price'])
        if date in statistics:
            statistics[date] += price
        else:
            statistics[date] = price
    print("\nTotal revenue of orders per day:\n")
    for date, price in statistics.items():
        print(f"In {date} the total revenue was: {price} $")

def clerk_menu():
    """
    Lists all clerk's options and asks
    for user's choice.
    """
    print("\n1. Add order")
    print("2. Check pending orders")
    print("3. Log out")
    print("0. Exit\n")
    while True:
        try:
            choice = int(input("> "))
            break
        except ValueError:
            continue
    return choice

def delivery_menu():
    """
    Lists all delivery's options and asks
    for user's choice.
    """
    print("\n1. Complete order")
    print("2. Check pending orders")
    print("3. Log out")
    print("0. Exit\n")
    while True:
        try:
            choice = int(input("> "))
            break
        except ValueError:
            continue
    return choice

def manager_menu():
    """
    Lists all manager's options and asks
    for user's choice.
    """
    print("\n1. Check number of orders placed by a customer")
    print("2. Check number of orders placed on a specific day")
    print("3. Check total revenue of all orders delivered")
    print("4. Check total revenue of all orders placed by a customer")
    print("5. Check total revenue of all orders placed on a specific day")
    print("6. List names of all customers")
    print("7. List number of orders placed per customer")
    print("8. List all data entered")
    print("9. Check total revenue of orders per day")
    print("10. Log out")
    print("0. Exit\n")
    while True:
        try:
            choice = int(input("> "))
            break
        except ValueError:
            continue
    return choice

username, role = login()
# Loop until user's choice
while True:
    """
After a successful login calls for the
respected class menu and user's choice
of option.
"""
    if role == 'clerk':
        choice = clerk_menu()
        if choice == 1:
            add_orders()
        elif choice == 2:
            get_pending_orders()
        elif choice == 3:
            username, role = login()
            continue
        elif choice == 0:
            break
        else:
            print("\nInvalid choice")
    elif role == 'delivery':
        choice = delivery_menu()
        if choice == 1:
            complete_orders()
        elif choice == 2:
            get_pending_orders()
        elif choice == 3:
            username, role = login()
            continue
        elif choice == 0:
            break
        else:
            print("\nInvalid choice")
    elif role == 'manager':
        choice = manager_menu()
        if choice == 1:
            get_number_of_orders_by_customer()
        elif choice == 2:
            get_number_of_orders_by_day()
        elif choice == 3:
            get_revenue_of_delivered_orders()
        elif choice == 4:
            get_revenue_of_placed_orders_by_customer()
        elif choice == 5:
            get_revenue_of_placed_orders_by_day()
        elif choice == 6:
            list_customer_names()
        elif choice == 7:
            list_number_of_orders_placed_per_customer()
        elif choice == 8:
            list_all_data()
        elif choice == 9:
            get_revenue_of_orders_per_day()
        elif choice == 10:
            username, role = login()
            continue
        elif choice == 0:
            break
        else:
            print("\nInvalid choice")
    else:
        print("\nInvalid role")
        break
print("\nGoodbye!\n")