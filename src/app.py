# Imports
from general_funcs import *
from load_data_module import *
from save_data_module import *
from products_module import *
from orders_module import *
from couriers_module import *

# Main App
while True:
    # Clear Screen
    clear_screen()

    # Main menu options 
    print_menu('main')
    main_menu_choice = get_menu_choice(0, 3)

    if main_menu_choice == 0:
        clear_screen()
        message = "[[green-background]] Thanks for using the app :) [[end]]"
        colorText(message)
        break

    # Product menu
    elif main_menu_choice == 1:
        clear_screen()
        while True:
            # Print product Menu
            print_menu('product')
            product_menu_choice = get_menu_choice(0, 4)

            # Return to Main Menu
            if product_menu_choice == 0:
                clear_screen()
                break

            # Show Product List    
            elif product_menu_choice == 1:
                clear_screen()
                products = load_product_list()
                display_product_list(products)
                input("\nPress Enter to return to Product Menu: ")
                clear_screen()
            
            # Create new product
            elif product_menu_choice == 2:
                clear_screen()
                products = load_product_list()
                add_new_product()
                
            # Update existing    
            elif product_menu_choice == 3:
                clear_screen() 
                products = load_product_list()
                display_product_list(products)
                update_product(products)
            
            # Delete product
            elif product_menu_choice == 4:
                clear_screen()
                products = load_product_list()
                display_product_list(products)
                delete_product(products)

    # Orders Menu
    elif main_menu_choice == 2:
        # Clear Screen
        clear_screen()

        while True:

            # Print Order Menu
            print_menu('order')
            order_menu_choice = get_menu_choice(0, 6)
            
            # Return to Main Menu
            if order_menu_choice == 0:
                break

            # Show orders 
            if order_menu_choice == 1:
                clear_screen()
                orders = load_orders_list()
                display_orders(orders)
                input("\nPress Enter to return to Order Menu: ")
                clear_screen()
                
            # Add order
            if order_menu_choice == 2:
                clear_screen()
                products = load_product_list()
                couriers = load_couriers_list()
                create_new_order(products, couriers)
                
            # Update existing order status 
            if order_menu_choice == 3:
                clear_screen()
                orders = load_orders_list()
                display_orders(orders)
                update_order_status(orders)
                
            # Update existing order
            if order_menu_choice == 4:
                clear_screen()
                orders = load_orders_list()
                products = load_product_list()
                couriers = load_couriers_list()
                display_orders(orders)
                update_order(orders, couriers, products)
                
            # Delete an order
            if order_menu_choice == 5:
                clear_screen()
                orders = load_orders_list()
                display_orders(orders)
                delete_order(orders)
            
            if order_menu_choice == 6:
                clear_screen()
                orders = load_orders_list()
                sort_orders(orders)

    # couriers menu
    elif main_menu_choice == 3:
        # Clear Screen
        clear_screen()

        while True:

            # Print Order Menu
            print_menu('courier')
            courier_menu_option = get_menu_choice(0, 4)
            
            # Return to Main Menu
            if courier_menu_option == 0:
                break

            # Print couriers list    
            if courier_menu_option == 1:
                clear_screen()
                couriers = load_couriers_list()
                display_couriers(couriers)
                input("\nPress Enter to return to Product Menu: ")
                clear_screen()

            # Create new courier
            if courier_menu_option == 2:
                clear_screen()
                couriers = load_couriers_list()
                add_new_courier()
            
            # Update existing courier 
            if courier_menu_option == 3:
                clear_screen() 
                couriers = load_couriers_list()
                display_couriers(couriers)
                update_courier(couriers)

            # Delete courier 
            if courier_menu_option == 4:
                clear_screen()
                couriers = load_couriers_list()
                display_couriers(couriers)
                delete_courier(couriers)