# Imports
import csv
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../docker_setup/.env')
host_name = os.environ.get("mysql_host")
database_name = os.environ.get("mysql_db")
user_name = os.environ.get("mysql_user")
user_password = os.environ.get("mysql_pass")

    

# Save product list
def save_products_list(list):
    products_csv = "..\data\products.csv"

    try:
        with open(products_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['name', 'price'])
            writer.writeheader()

            # Write each dictionary as a row in the CSV file
            for row in list:
                writer.writerow(row)
    except Exception as e:
        print("The following error occured: " + str(e))

# Save couriers list
def save_couriers_list(list):
    couriers_csv = "..\data\couriers.csv"

    try:
        with open(couriers_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['name', 'phone'])
            writer.writeheader()

            # Write each dictionary as a row in the CSV file
            for row in list:
                writer.writerow(row)
    except Exception as e:
        print("The following error occured: " + str(e))

# Save orders list
def save_orders_list(list):
    orders_csv = "..\data\orders.csv"

    try:
        with open(orders_csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['name', 'address', 'phone', 'courier', 'status', 'items'])
            writer.writeheader()

            # Write each dictionary as a row in the CSV file
            for row in list:
                writer.writerow(row)
    except Exception as e:
        print("The following error occured: " + str(e))