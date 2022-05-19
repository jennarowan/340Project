from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db
from dotenv import load_dotenv, find_dotenv

# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())

# Set the variables in our application with those environment variables
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
database = os.environ.get("340DB")

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = passwd
app.config['MYSQL_DB'] = database
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 

@app.route('/')
def root():
    return render_template("index.j2")

@app.route('/orders', methods=["POST", "GET"])
def orders():

    if request.method == "GET":

        # Grabs all data for the main Orders table
        readQuery = """
        SELECT 
        Orders.orderID AS "Order #", 
        CONCAT(Employees.firstName, " ", Employees.lastName) AS "Employee", 
        Stores.addressStreet AS "Store Location", 
        CONCAT(Customers.firstName, " ", Customers.lastName) AS "Customer",
        CONCAT("$", Orders.orderTotal) AS "Total"
        FROM Orders
        INNER JOIN Employees ON Orders.Employees_employeeID = Employees.employeeID
        INNER JOIN Stores ON Orders.Stores_storeID = Stores.storeID
        INNER JOIN Customers ON Orders.Customers_customerID = Customers.customerID;
        """

        cursor = mysql.connection.cursor()
        cursor.execute(readQuery)
        orders = cursor.fetchall()

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
        storeID, addressStreet
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

        return render_template("orders.j2", Orders=orders, Employees=employees, Stores=stores, Customers=customers)

    if request.method == "POST":

        # Fires if user presses the New button
        if request.form.get("newOrder"):
            orderID = request.form["orderID"]
            employeeID = request.form["employeeID"]
            storeID = request.form["storeID"]
            orderTotal = request.form["orderTotal"]

        insertQuery = "INSERT INTO Orders (orderID, employeeID, storeID, orderTotal) VALUES (%s, %s, %s, %s)"
        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (orderID, employeeID, storeID, orderTotal))
        mysql.connection.commit()

        # Send user back to the main orders page
        return redirect("/orders")

@app.route('/stores')
def stores():

    readQuery = """
    SELECT * FROM Stores;
    """

    return render_template("stores.j2")

@app.route('/customers')
def customers():
    return render_template("customers.j2")

@app.route('/employees')
def employees():
    return render_template("employees.j2")

@app.route('/liquors')
def liquors():
    return render_template("liquors.j2")

@app.route('/rewardtiers')
def rewardtiers():
    return render_template("rewardtiers.j2")

@app.route('/liquorsorders')
def liquorsorders():
    return render_template("liquorsorders.j2")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 