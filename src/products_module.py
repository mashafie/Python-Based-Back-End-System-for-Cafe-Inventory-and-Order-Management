# Imports
from general_funcs import *
from save_data_module import *
from database import *

# Print product list       
def display_product_list(items):
    name_length = max([len(item['name']) for item in items] + [len('Name')])
    price_length = max([len(str(item['price'])) for item in items] + [len('Price')])
    index_length = max([len(str(item['price'])) for item in items] + [len('Product ID')])
    header_format = f"| {'Product ID':<{index_length}} | {'Name':<{name_length}} | {'Price':>{price_length}} |"
    line_format = f"+{'-'*(index_length+2)}+{'-'*(name_length+2)}+{'-'*(price_length+2)}+"

    print(line_format)
    print(header_format)
    print(line_format)

    for i, item in enumerate(items):
        name = item['name']
        price = str(item['price'])
        index = str(item['product_id'])
        row_format = f"| {index:<{index_length}} | {name:<{name_length}} | {price:>{price_length}} |"
        print(row_format)
    
    print(line_format)

# Load products
def load_product_list():
    products = []

    try:
        connection = get_connection()

        # create a cursor to execute SQL queries
        cursor = connection.cursor()

        # execute a SELECT query to retrieve the products from the database
        cursor.execute("SELECT product_id, name, price FROM products")


        # fetch all rows and append them to the products list
        rows = cursor.fetchall()
        for row in rows:
            product = {
                "product_id": row[0],
                "name": row[1],
                "price": row[2]
            }
            products.append(product)
        
        cursor.close()
        close_connection()
    except Exception as e:
        print("The following error occured: " + str(e))
    
    
    return products

# Save new product
def save_new_product(product):
    try:
        connection = get_connection()

        sql = "INSERT INTO products (name, price) VALUES (%s, %s)"
        val = (product["name"], product["price"])

        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()

        success_message = f"[[green-background]] {product['name']} has been successfully added! [[end]]"
        colorText(success_message)

        cursor.close()
        close_connection()
    except Exception as e:
        message = f"[[red-background]] Failed to open connection: {e} [[end]]"
        colorText(message)



# Create new product
def add_new_product():
    while True:
        try:
            new_product_name = str(input("Enter a new product name (0 to go back): "))
            if new_product_name == "0":
                clear_screen()
                break
            else:
                while True:
                    try:
                        new_product_price = float(input(f"Enter the price for {new_product_name}: "))
                        new_product = {"name": new_product_name, "price": new_product_price}
                        save_new_product(new_product)
                        clear_screen()
                        success_message = f"[[green-background]] {new_product_name} has been successfully added! [[end]]"
                        colorText(success_message)
                        break   
                    except ValueError:
                        message = f"[[red-background]] Invalid input: please enter a valid price [[end]]"
                        colorText(message)
                    except Exception as e:
                        message = f"[[red-background]] Error: {e} [[end]]"
                        colorText(message)
                break
        except ValueError:
            message = f"[[red-background]] Invalid input: please enter a valid name [[end]]"
            colorText(message)

# Update Product
def update_product(product_list):
    while True:
        product_id = input("\nEnter product ID to update (or enter 0 to cancel): ")
        try:
            product_id = int(product_id)
            if product_id == 0:
                product = None
                break
            else:
                product = None
                for p in product_list:
                    if p["product_id"] == product_id:
                        product = p
                        break
                if product:
                    break
                else:
                    message = f"[[red-background]] Invalid product ID. Please try again [[end]]"
                    colorText(message)
        except ValueError:
            message = f"[[red-background]] Invalid input. Please enter a number [[end]]"
            colorText(message)

    if product_id != 0:
    
        new_name = input(f"Enter a new name for {product['name']} (enter nothing to keep the same name): ") or product['name']
        while True:
            try:
                input_price = input(f"Enter a new price for {product['price']} (enter nothing to keep the same price): ")
                if input_price.strip(): 
                    new_price = float(input_price)
                else:
                    new_price = float(product['price'])
                break
            except ValueError:
                message = f"[[red-background]] Invalid input: please enter a valid price [[end]]"
                colorText(message)


        # update the dictionary with the new values (or keep the same if user entered nothing)
        product['name'] = new_name
        product['price'] = new_price

        connection = get_connection()
        cursor = connection.cursor() 
        sql = "UPDATE products SET name = %s, price = %s WHERE product_id = %s"
        val = (new_name, new_price, product_id)
        cursor.execute(sql, val)
        connection.commit()

        clear_screen()
        success_message = f"[[green-background]] {product['name']} has been successfully updated! [[end]]"
        colorText(success_message)

        cursor.close()
        close_connection()
    else:
        clear_screen()

# Delete Product
def delete_product(product_list):
    while True:
        product_id = input("\nSelect the index of the product you want to delete (or enter 0 to cancel): ")
        try:
            product_id = int(product_id)
            if product_id == 0:
                product = None
                break
            else:
                product = None
                for p in product_list:
                    if p["product_id"] == product_id:
                        product = p
                        break
                if product:
                    break
                else:
                    message = f"[[red-background]] Invalid product ID. Please try again [[end]]"
                    colorText(message)
        except ValueError:
            message = f"[[red-background]] Invalid input. Please enter a number [[end]]"
            colorText(message)

    if product_id != 0:    
        connection = get_connection()

        cursor = connection.cursor()
        sql_delete = "DELETE FROM products WHERE product_id = %s"
        val_delete = (product_id,)
        cursor.execute(sql_delete, val_delete)

        sql_update = "UPDATE products SET product_id = product_id - 1 WHERE product_id > %s"
        val_update = (product_id,)
        cursor.execute(sql_update, val_update)

        sql_reset = "ALTER TABLE products AUTO_INCREMENT = 1"
        cursor.execute(sql_reset)

        connection.commit()

        clear_screen()
        success_message = f"[[green-background]] {product['name']} has been successfully deleted! [[end]]"
        colorText(success_message)

        cursor.close()
        close_connection()
    else:
        clear_screen()
