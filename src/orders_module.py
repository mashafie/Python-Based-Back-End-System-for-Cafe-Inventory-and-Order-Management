# Imports
from general_funcs import *
from save_data_module import *
from products_module import display_product_list
from couriers_module import display_couriers
from database import *

# Print orders list       
def display_orders(orders):
    # calculate the width of each column
    max_index_length = max([len(str(order['order_id'])) for order in orders] + [len('Order ID')])
    max_name_length = max([len(str(order['customer_name'])) for order in orders] + [len('Customer Name')])
    max_address_length = max([len(str(order['customer_address'])) for order in orders] + [len('Customer Address')])
    max_phone_length = max([len(str(order['customer_phone'])) for order in orders] + [len('Customer Phone')])
    max_courier_length = max([len(str(order['courier'])) for order in orders] + [len('Courier')])
    max_status_length = max([len(str(order['status'])) for order in orders] + [len('Order Status')])
    max_items_length = max([len(str(order['items'])) for order in orders] + [len('Product Items')])

    # display each order in a table format with an index column
    header_format = f"| {'Order ID':^{max_index_length}} | {'Customer Name':^{max_name_length}} | {'Customer Address':^{max_address_length}} | {'Customer Phone':^{max_phone_length}} | {'Courier':^{max_courier_length}} | {'Status':^{max_status_length}} | {'Product Items':^{max_items_length}} |"
    line_format = f"+{'-'*(max_index_length+2)}+{'-'*(max_name_length+2)}+{'-'*(max_address_length+2)}+{'-'*(max_phone_length+2)}+{'-'*(max_courier_length+2)}+{'-'*(max_status_length+2)}+{'-'*(max_items_length+2)}+"

    print(line_format)
    print(header_format)
    print(line_format)

    for order in orders:
        name = order['customer_name']
        address = order['customer_address']
        index = str(order['order_id'])
        phone = order['customer_phone']
        courier = str(order['courier'])
        status = str(order['status'])
        items = order['items']
        row_format = f"| {index:<{max_index_length}} | {name:<{max_name_length}} | {address:<{max_address_length}} | {phone:<{max_phone_length}} | {courier:<{max_courier_length}} | {status:<{max_status_length}} | {items:<{max_items_length}} |"
        print(row_format)

    print(line_format)

# Load products
def load_orders_list():
    orders = []

    try:
        connection = get_connection()

        # create a cursor to execute SQL queries
        cursor = connection.cursor()

        # execute a SELECT query to retrieve the products from the database
        cursor.execute("SELECT order_id, customer_name, customer_address, customer_phone, courier, status, items FROM orders")


        # fetch all rows and append them to the products list
        rows = cursor.fetchall()
        for row in rows:
            order = {
                "order_id": row[0],
                "customer_name": row[1],
                "customer_address": row[2],
                "customer_phone": row[3],
                "courier": row[4],
                "status": row[5],
                "items": row[6],
            }
            orders.append(order)
        
        cursor.close()
        close_connection()
    except Exception as e:
        print("The following error occured: " + str(e))
    
    
    return orders

# Save new order
def save_new_order(order):
    try:
        connection = get_connection()

        sql = "INSERT INTO orders (customer_name, customer_address, customer_phone, courier, status, items) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (order["customer_name"], order["customer_address"], order["customer_phone"], order["courier"], order["status"], order["items"])

        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()

        success_message = f"[[green-background]] {order['customer_name']} order has been successfully added! [[end]]"
        colorText(success_message)

        cursor.close()
        close_connection()
    except Exception as e:
        message = f"[[red-background]] Failed to open connection: {e} [[end]]"
        colorText(message)


# Create new order
def create_new_order(product_list, couriers_list):
    while True:
        try:
            customer_name = input("Enter customer name: ")
            if type(customer_name) != str or len(customer_name) <= 1:
                raise ValueError
            break
        except ValueError:
            message = f"[[red-background]] Invalid input: please enter a valid name [[end]]"
            colorText(message)

    while True:
        try:
            customer_address = input("Enter customer address: ")
            if len(customer_address) <= 5:
                raise ValueError
            break
        except ValueError:
            message = f"[[red-background]] Invalid input: please enter a valid address [[end]]"
            colorText(message)

    while True:
        try:
            customer_phone = int(input("Enter customer phone: "))
            if len(str(customer_phone)) <= 9 or type(customer_phone) != int:
                raise ValueError
            break
        except ValueError:
            message = f"[[red-background]] Invalid input: please enter a valid number [[end]]"
            colorText(message)

    # Display product list
    clear_screen()

    display_product_list(product_list)

    user_input_list = []

    while True:
        user_input = input(f"Enter the index of the product you want to add to {customer_name}'s order (or '0' if you're finished): ")

        if user_input == "0":
            break

        try:
            index = int(user_input)

            if index > 0 and index <= len(product_list):
                product = product_list[index - 1]["name"]
                user_input_list.append(str(index))
                success_message = f"[[green-background]] {product} has been successfully added! [[end]]"
                colorText(success_message)   
            else:
                raise ValueError
        except ValueError:
            message = f"[[red-background]] Invalid input: please enter a valid index [[end]]"
            colorText(message)

    product_string = ",".join(user_input_list)

    clear_screen()
    display_couriers(couriers_list)

    while True:
        try:
            courier_choice = int(input("\nSelect the index of the courier: ")) 
            if courier_choice > 0 and courier_choice <= len(couriers_list):
                break
            else:
                raise ValueError
        except ValueError:
            message = f"[[red-background]] Invalid input: please enter a valid index [[end]]"
            colorText(message)

    # create a new order dictionary with the user input values and the 'PREPARING' status
    new_order = {
        "customer_name": customer_name,
        "customer_address": customer_address,
        "customer_phone": customer_phone,
        "courier" : courier_choice,
        "status": 1,
        "items" : product_string
    }

    save_new_order(new_order)
    clear_screen()
    success_message = "[[green-background]] Order Successfully Added :) [[end]]"
    colorText(success_message)


# Update existing order status
def update_order_status(orders_list):
    while True:
        order_id = input("\nEnter Order ID status to update (or enter 0 to cancel): ")
        try:
            order_id = int(order_id)
            if order_id == 0:
                order = None
                break
            else:
                order = None
                for o in orders_list:
                    if o["order_id"] == order_id:
                        order = o
                        break
                if order:
                    break
                else:
                    message = f"[[red-background]] Invalid Order ID. Please try again [[end]]"
                    colorText(message)
        except ValueError:
            message = f"[[red-background]] Invalid input. Please enter a number [[end]]"
            colorText(message)

    if order_id != -1:
        clear_screen()
        while True:
            try:
                status_list = ["PREPARING", "READY", "DELIVERED", "CANCELLED"]
                for i, status in enumerate(status_list):
                    print(f"{i+1}: {status}")
                status_index = int(input("\nEnter the index of the new status: "))
                if status_index < 1 or status_index > len(status_list):
                    raise ValueError
                break
            except ValueError:
                clear_screen()
                message = f"[[red-background]] Invalid input: please enter a valid price [[end]]"
                colorText(message)

        # update the status for the selected order
        order['status'] = status_index

        connection = get_connection()
        cursor = connection.cursor() 
        sql = "UPDATE orders SET status = %s WHERE order_id = %s"
        val = (status_index, order_id)
        cursor.execute(sql, val)
        connection.commit()
        
        clear_screen()
        success_message = "[[green-background]] Order Status Successfully Updated :) [[end]]"
        colorText(success_message)
    else:
        clear_screen()

# Update existing order
def update_order(orders_list, couriers_list, products_list):
    while True:
        order_id = input("\nEnter Order ID status to update (or enter 0 to cancel): ")
        try:
            order_id = int(order_id)
            if order_id == 0:
                order = None
                break
            else:
                order = None
                for o in orders_list:
                    if o["order_id"] == order_id:
                        order = o
                        break
                if order:
                    break
                else:
                    message = f"[[red-background]] Invalid Order ID. Please try again [[end]]"
                    colorText(message)
        except ValueError:
            message = f"[[red-background]] Invalid input. Please enter a number [[end]]"
            colorText(message)


    if order_id != -1:
        # iterate over the key-value pairs in the selected order dictionary
        for key, value in order.items():
            if key == 'customer_name' or key == 'customer_address' or key == 'customer_phone':
                # get user input for the updated property value
                updated_value = input(f"\nEnter new {key} (leave blank to keep the current value '{value}'): ")
                # if the user input is not blank, update the property value
                if updated_value != "":
                    order[key] = updated_value
            elif key == 'courier':
                clear_screen()
                display_couriers(couriers_list)
                while True:
                    try:
                        current_courier_index = int(value) - 1
                        courier_choice = int(input(f"\nSelect the index of the courier for this order (Current courier is '{couriers_list[current_courier_index]['name']}'): "))
                        if courier_choice > 0 and courier_choice <= len(couriers_list):
                            break
                        if courier_choice == "":
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        message = f"[[red-background]] Invalid input: please enter a valid index [[end]]"
                        colorText(message)
                if courier_choice != "":
                    order[key] = courier_choice
            elif key == 'items':
                clear_screen()
                while True:
                    user_choice = input("Do you want to update the order items? (y/n): ")

                    if user_choice == 'y':
                        display_product_list(products_list)

                        user_input_list = []

                        while True:

                            user_input = input(f"\nEnter the index of the product you want to add the order (or '0' if you're finished): ")

                            if user_input == "0":
                                break

                            try:
                                index = int(user_input)

                                if index > 0 and index <= len(products_list):
                                    product = products_list[index - 1]["name"]
                                    user_input_list.append(str(index))
                                    success_message = f"[[green-background]] {product} has been successfully added! [[end]]"
                                    colorText(success_message)   
                                else:
                                    raise ValueError
                            except ValueError:
                                message = f"[[red-background]] Invalid input: please enter a valid index [[end]]"
                                colorText(message)

                        product_string = ",".join(user_input_list)

                        if courier_choice != "":
                            order[key] = product_string
                        break
                    elif user_choice == 'n':
                        break
                    else:
                        message = f"[[red-background]] Invalid input: please enter a y or n [[end]]"
                        colorText(message)
            else:
                continue

        connection = get_connection()
        cursor = connection.cursor() 
        sql = "UPDATE orders SET customer_name = %s, customer_address = %s, customer_phone = %s, courier = %s, status = %s, items = %s WHERE order_id = %s"
        val = (order['customer_name'], order['customer_address'], order['customer_phone'], order['courier'], order['status'], order['items'], order_id)
        cursor.execute(sql, val)
        connection.commit()     
               
        clear_screen()
        success_message = "[[green-background]] Order Successfully Updated :) [[end]]"
        colorText(success_message)
    else:
        clear_screen()

# Delete Order
def delete_order(orders_list):
    while True:
        order_id = input("\nEnter Order ID status to update (or enter 0 to cancel): ")
        try:
            order_id = int(order_id)
            if order_id == 0:
                order = None
                break
            else:
                order = None
                for o in orders_list:
                    if o["order_id"] == order_id:
                        order = o
                        break
                if order:
                    break
                else:
                    message = f"[[red-background]] Invalid Order ID. Please try again [[end]]"
                    colorText(message)
        except ValueError:
            message = f"[[red-background]] Invalid input. Please enter a number [[end]]"
            colorText(message)

    if order_id != 0:    
        connection = get_connection()

        cursor = connection.cursor()
        sql_delete = "DELETE FROM orders WHERE order_id = %s"
        val_delete = (order_id,)
        cursor.execute(sql_delete, val_delete)

        sql_update = "UPDATE orders SET order_id = order_id - 1 WHERE order_id > %s"
        val_update = (order_id,)
        cursor.execute(sql_update, val_update)

        sql_reset = "ALTER TABLE orders AUTO_INCREMENT = 1"
        cursor.execute(sql_reset)

        connection.commit()

        clear_screen()
        success_message = f"[[green-background]] Order has been successfully deleted! [[end]]"
        colorText(success_message)

        cursor.close()
        close_connection()
    else:
        clear_screen()

# Display orders by courier or list
def sort_orders(orders):
    while True:
        try:
            sort_key = int(input("Enter 1 to sort by courier or 2 to sort by status: "))
            if sort_key < 0 or sort_key > 2:
                raise ValueError
            break
        except ValueError:
            message = f"[[red-background]] Invalid input. Please enter a 0, 1 or 2 [[end]]"
            colorText(message)

    if sort_key == 1:
        orders.sort(key=lambda x: x["courier"])
    elif sort_key == 2:
        orders.sort(key=lambda x: x["status"])
    
    clear_screen()
    display_orders(orders)
    input("\nPress Enter to return to Product Menu: ")
    clear_screen()
