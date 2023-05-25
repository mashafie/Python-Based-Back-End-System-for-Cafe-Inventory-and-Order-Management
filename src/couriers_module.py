# Imports
from general_funcs import *
from save_data_module import *
from database import *

# Print couriers list
def display_couriers(couriers_list):
    max_index_length = max([len(str(courier['courier_id'])) for courier in couriers_list] + [len('Courier ID')])
    
    if couriers_list:
        max_name_length = max(max(len(courier['name']), len('Name')) for courier in couriers_list)
    else:
        max_name_length = len('Name')

    if couriers_list:
        max_phone_length = max(max(len(str(courier['phone'])), len('Phone')) for courier in couriers_list)
    else:
        max_phone_length = len('Phone')
    
    header_format = f"| {'Courier ID':<{max_index_length}} | {'Name':^{max_name_length}} | {'Phone':^{max_phone_length}} |"
    line_format = f"+{'-'*(max_index_length+2)}+{'-'*(max_name_length+2)}+{'-'*(max_phone_length+2)}+"

    print(line_format)
    print(header_format)
    print(line_format)

    # display each courier in a table format with an index column
    for i, courier in enumerate(couriers_list):
        name = courier['name']
        phone = str(courier['phone'])
        index = str(courier['courier_id'])
        row_format = f"| {index: <{max_index_length}} | {name: <{max_name_length}} | {phone: <{max_phone_length}} |"
        print(row_format)

    print(line_format)

# Load couriers
def load_couriers_list():
    couriers = []

    try:
        connection = get_connection()

        # create a cursor to execute SQL queries
        cursor = connection.cursor()

        # execute a SELECT query to retrieve the products from the database
        cursor.execute("SELECT courier_id, name, phone FROM couriers")

        # fetch all rows and append them to the products list
        rows = cursor.fetchall()
        for row in rows:
            product = {
                "courier_id": row[0],
                "name": row[1],
                "phone": row[2]
            }
            couriers.append(product)
        
        cursor.close()
        close_connection()
    except Exception as e:
        print("The following error occured: " + str(e))
    
    
    return couriers

# Save new courier
def save_new_courier(courier):
    try:
        connection = get_connection()

        sql = "INSERT INTO couriers (name, phone) VALUES (%s, %s)"
        val = (courier["name"], courier["phone"])

        cursor = connection.cursor()
        cursor.execute(sql, val)
        connection.commit()

        success_message = f"[[green-background]] {courier['name']} has been successfully added! [[end]]"
        colorText(success_message)

        cursor.close()
        close_connection()
    except Exception as e:
        message = f"[[red-background]] Failed to open connection: {e} [[end]]"
        colorText(message)

# Create new courier
def add_new_courier():
    while True:
        try:
            courier_name = str(input("Enter couriers name (0 to go back): "))
            if courier_name == "0":
                clear_screen()
                break
            elif len(courier_name) <= 1:
                raise ValueError
            else:
                while True:
                    try:
                        courier_phone = str(input("Enter courier phone: "))
                        if len(courier_phone) <= 9:
                            raise ValueError
                        new_courier = {"name": courier_name, "phone": courier_phone}
                        save_new_courier(new_courier)
                        clear_screen()
                        success_message = f"[[green-background]] {courier_name} has been successfully added! [[end]]"
                        colorText(success_message)
                        break   
                    except ValueError:
                        message = f"[[red-background]] Invalid input: please enter a valid phone number [[end]]"
                        colorText(message)
                break
        except ValueError:
            message = f"[[red-background]] Invalid input: please enter a valid name [[end]]"
            colorText(message)

# Update Courier
def update_courier(couriers):
    while True:
        courier_id = input("\nEnter courier ID to update (or enter 0 to cancel): ")
        try:
            courier_id = int(courier_id)
            if courier_id == 0:
                courier = None
                break
            else:
                courier = None
                for c in couriers:
                    if c["courier_id"] == courier_id:
                        courier = c
                        break
                if courier:
                    break
                else:
                    message = f"[[red-background]] Invalid Courier ID. Please try again [[end]]"
                    colorText(message)
        except ValueError:
            message = f"[[red-background]] Invalid input. Please enter a number [[end]]"
            colorText(message)

    if courier_id != 0:
    
        new_name = str(input(f"Enter a new name for {courier['name']} (enter nothing to keep the same name): ")) or courier['name']
       
        while True:
            try:
                input_phone = input(f"Enter a new phone number for {courier['phone']} (enter nothing to keep the same number): ")
                if input_phone == "":
                    new_phone = courier['phone']
                elif len(input_phone) < 10:
                    raise ValueError
                else:
                    new_phone = input_phone
                courier['phone'] = new_phone
                break
            except ValueError:
                message = "[[red-background]]Invalid input: please enter a valid phone number[[end]]"
                print(message)



        # update the dictionary with the new values (or keep the same if user entered nothing)
        courier['name'] = new_name
        courier['phone'] = new_phone

        connection = get_connection()
        cursor = connection.cursor() 
        sql = "UPDATE couriers SET name = %s, phone = %s WHERE courier_id = %s"
        val = (new_name, new_phone, courier_id)
        cursor.execute(sql, val)
        connection.commit()

        clear_screen()
        success_message = f"[[green-background]] {courier['name']} has been successfully updated! [[end]]"
        colorText(success_message)

        cursor.close()
        close_connection()
    else:
        clear_screen()


# # Update existing courier status 
# def update_existing_courier_status(couriers_list):
#     # get user input for the courier index value
#     while True:
#         try:
#             courier_index = int(input("\nEnter the index of the courier (0 to go back): ")) - 1
#             if courier_index < -1 or courier_index >= len(couriers_list) or type(courier_index) != int:
#                 raise ValueError
#             break
#         except ValueError:
#             message = f"[[red-background]] Invalid input: please enter a valid index [[end]]"
#             colorText(message)

#     if courier_index != -1:
#         for key, value in couriers_list[courier_index].items():
#                 # get user input for the updated property value
#                 updated_value = input(f"\nEnter new {key} (leave blank to keep the current value '{value}'): ")
#                 # if the user input is not blank, update the property value
#                 if updated_value != "":
#                     couriers_list[courier_index][key] = updated_value
#         save_couriers_list(couriers_list)
#         clear_screen()
#         success_message = "[[green-background]] Courier Successfully Updated :) [[end]]"
#         colorText(success_message)
#     else:
#         clear_screen()

# Delete Courier
def delete_courier(couriers):
    while True:
        courier_id = input("\nSelect the index of the courier you want to delete (or enter 0 to cancel): ")
        try:
            courier_id = int(courier_id)
            if courier_id == 0:
                courier = None
                break
            else:
                courier = None
                for c in couriers:
                    if c["courier_id"] == courier_id:
                        courier = c
                        break
                if courier:
                    break
                else:
                    message = f"[[red-background]] Invalid Courier ID. Please try again [[end]]"
                    colorText(message)
        except ValueError:
            message = f"[[red-background]] Invalid input. Please enter a number [[end]]"
            colorText(message)

    if courier_id != 0:    
        connection = get_connection()

        cursor = connection.cursor()
        sql_delete = "DELETE FROM couriers WHERE courier_id = %s"
        val_delete = (courier_id,)
        cursor.execute(sql_delete, val_delete)

        sql_update = "UPDATE couriers SET courier_id = courier_id - 1 WHERE courier_id > %s"
        val_update = (courier_id,)
        cursor.execute(sql_update, val_update)

        sql_reset = "ALTER TABLE couriers AUTO_INCREMENT = 1"
        cursor.execute(sql_reset)

        connection.commit()

        clear_screen()
        success_message = f"[[green-background]] {courier['name']} Successfully Deleted :) [[end]]"
        colorText(success_message)

        cursor.close()
        close_connection()
    else:
        clear_screen()