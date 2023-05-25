# Imports
import csv
import pymysql
import os

# Load orders list
def load_orders_list():
    orders = []

    try:
        orders_csv = "..\data\orders.csv"
        with open(orders_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                orders.append(row)
    except Exception as e:
        print("The following error occured: " + str(e))
    
    return orders

# Load couriers list
def load_couriers_list():
    couriers = []

    try:
        couriers_csv = "..\data\couriers.csv"
        with open(couriers_csv, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                couriers.append(row)
    except Exception as e:
        print("The following error occured: " + str(e))
    
    return couriers