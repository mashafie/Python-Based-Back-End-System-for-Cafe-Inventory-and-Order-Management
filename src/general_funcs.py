from os import system, name

# Colour codes
colours_dict = {
"black":"\u001b[30;1m",
"red": "\u001b[31;1m",
"green":"\u001b[32m",
"yellow":"\u001b[33;1m",
"blue":"\u001b[34;1m",
"magenta":"\u001b[35m",
"cyan": "\u001b[36m",
"white":"\u001b[37m",
"yellow-background":"\u001b[43m",
"black-background":"\u001b[40m",
"green-background":"\u001b[42;1m",
"red-background":"\u001b[41;1m",
"end":"\u001b[0m"
}

# Clears the terminal window text
def clear_screen():
    system("cls" if name == "nt" else "clear")

# To show coloured text
def colorText(text):
    for color in colours_dict:
        text = text.replace("[[" + color + "]]", colours_dict[color])
    print(text)

# To show menu's
def print_menu(menu):
    
    if menu == 'main':
        print(
        """
        ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
            Main Menu
        ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
        0 => Exit
        1 => Product menu
        2 => Order Menu
        3 => Courier Menu
        """
    )
    
    if menu == 'product':
        print(
                """
            ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
                    Product Menu
            ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
            0 => Main Menu
            1 => Show Product List
            2 => Create New Product
            3 => Update Existing Product
            4 => Delete Product 
            """
            )
        
    if menu == 'order':
        print(
                """
            ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
                        Order Menu
            ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
            0 => Main Menu
            1 => Show Orders
            2 => Add New order
            3 => Update Existing Order Status
            4 => Update Existing Order
            5 => Delete Order
            6 => Sort orders by Courier/Status 
            """
            )
    
    if menu == 'courier':
        print(
                """
            ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
                    Couriers Menu
            ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
            0 => Main Menu
            1 => Show Couriers List
            2 => Create New Courier
            3 => Update Existing Courier
            4 => Delete Courier
            """
            )

# Menu user input
def get_menu_choice(lower_limit, upper_limit):
    
    while True:
        try:
            user_option = int(input("Enter Option: "))
            if user_option < lower_limit or user_option > upper_limit:
                raise ValueError
            break
        except ValueError:
            message = f"[[red-background]] Invalid input: please enter a valid integer index within the listed range [[end]]"
            colorText(message)

    return user_option
