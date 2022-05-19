from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db
from dotenv import load_dotenv, find_dotenv
from dropdownQueries import *

# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Grab all database credentials
app.config['MYSQL_HOST'] = os.environ.get("340DBHOST")
app.config['MYSQL_USER'] = os.environ.get("340DBUSER")
app.config['MYSQL_PASSWORD'] = os.environ.get("340DBPW")
app.config['MYSQL_DB'] = database = os.environ.get("340DB")
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

        # Call the dropdown creation function to query the database and pass values to the orders
        employees, stores, customers, nextOrderNum = createDropdownDatasets()        

        return render_template("orders.j2", orders=orders, employees=employees, stores=stores, customers=customers, nextOrderNum=nextOrderNum)

    if request.method == "POST":

        # Fires if user presses the New button
        if request.form.get("Add_Order"):
            orderID = request.form["orderID"]
            employeeID = request.form["employeeID"]
            storeID = request.form["storeID"]
            orderTotal = request.form["orderTotal"]
            customer = request.form["customerID"]

        insertQuery = """
        INSERT INTO Orders (orderID, Employees_employeeID, Stores_storeID, Customers_customerID, orderTotal) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (orderID, employeeID, storeID, customer, orderTotal))
        mysql.connection.commit()

        # Send user back to the main orders page
        return redirect("/orders")

@app.route("/edit_order/<int:id>", methods=["POST", "GET"])
def edit_order(id):
    
    if request.method == "GET":

        orderQuery = """
        SELECT 
        Orders.orderID AS "Order #", 
        CONCAT(Employees.firstName, " ", Employees.lastName) AS "Employee", 
        Stores.addressStreet AS "Store Location", 
        CONCAT(Customers.firstName, " ", Customers.lastName) AS "Customer",
        CONCAT("$", Orders.orderTotal) AS "Total"
        FROM Orders
        INNER JOIN Employees ON Orders.Employees_employeeID = Employees.employeeID
        INNER JOIN Stores ON Orders.Stores_storeID = Stores.storeID
        INNER JOIN Customers ON Orders.Customers_customerID = Customers.customerID
        WHERE orderId = %s""" % (id)
        cur = mysql.connection.cursor()
        cur.execute(orderQuery)
        orders = cur.fetchall()

        # Call the dropdown creation function to query the database and pass values to the orders
        employees, stores, customers, nextOrderNum = createDropdownDatasets()

        return render_template("edit_order.j2", orders=orders, employees=employees, stores=stores, customers=customers, orderNum=id)

    if request.method == "POST":

         # Fires if user presses the Edit button
        if request.form.get("Edit_Order"):
            employeeID = request.form["employeeID"]
            storeID = request.form["storeID"]
            customer = request.form["customerID"]
            orderTotal = request.form["orderTotal"]
            orderID = request.form["orderID"]
        
        updateQuery = """
        UPDATE Orders
        SET 
        Orders.Employees_employeeID = %s,
        Orders.Stores_storeID = %s,
        Orders.Customers_customerID = %s,
        Orders.orderTotal = %s
        WHERE
        Orders.orderID = %s
        """
        cursor = mysql.connection.cursor()
        cursor.execute(updateQuery, (employeeID, storeID, customer, orderTotal, orderID))
        mysql.connection.commit()

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