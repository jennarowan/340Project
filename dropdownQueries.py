from flask import Flask
from flask_mysqldb import MySQL
import os
import database.db_connector as db
from dotenv import load_dotenv, find_dotenv

# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())

app = Flask(__name__)
db_connection = db.connect_to_database()

# Grab all database credentials
app.config['MYSQL_HOST'] = os.environ.get("340DBHOST")
app.config['MYSQL_USER'] = os.environ.get("340DBUSER")
app.config['MYSQL_PASSWORD'] = os.environ.get("340DBPW")
app.config['MYSQL_DB'] = database = os.environ.get("340DB")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

def ordersDropdownDatasets():

    # Grabs the employee names to use in a dropdown
    employeeQuery = """
    SELECT
    employeeID, CONCAT(firstName, " ", lastName) AS "Employee"
    FROM Employees
    """

    cursor = mysql.connection.cursor()
    cursor.execute(employeeQuery)
    employees = cursor.fetchall()

    # Grabs the store locations to use in a dropdown
    storeQuery = """
    SELECT
    storeID, addressStreet AS "Store Location"
    FROM Stores
    """

    cursor = mysql.connection.cursor()
    cursor.execute(storeQuery)
    stores = cursor.fetchall()

    # Grabs the customer names to use in a dropdown
    customerQuery = """
    SELECT
    customerID, CONCAT(firstName, " ", lastName) AS "Customer"
    FROM Customers
    """

    cursor = mysql.connection.cursor()
    cursor.execute(customerQuery)
    customers = cursor.fetchall()

    return employees, stores, customers

def customersDropDowns():

    # Grabs the rewards tiers to use in an Insert dropdown
    tierQuery = """
    SELECT
    rewardsTierID,
    rewardsTierName
    FROM RewardsTiers
    """

    cursor = mysql.connection.cursor()
    cursor.execute(tierQuery)
    tiers = cursor.fetchall()

    return tiers