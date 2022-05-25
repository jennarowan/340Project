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
        employees, stores, customers= ordersDropdownDatasets()        

        return render_template("orders.j2", orders=orders, employees=employees, stores=stores, customers=customers)

    if request.method == "POST":

        # Fires if user presses the New button
        if request.form.get("Add_Order"):
            employeeID = request.form["employeeID"]
            storeID = request.form["storeID"]
            orderTotal = request.form["orderTotal"]
            customer = request.form["customerID"]

        # Grabs the next order number in line, so the user doesn't need to know what the correct order number is for Insert functions
        nextOrderQuery = """
        SELECT MAX(orderID) + 1 AS "nextOrderNum" FROM Orders
        """

        cursor = mysql.connection.cursor()
        cursor.execute(nextOrderQuery)
        orderID = cursor.fetchall()

        insertQuery = """
        INSERT INTO Orders (orderID, Employees_employeeID, Stores_storeID, Customers_customerID, orderTotal) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (orderID, employeeID, storeID, customer, orderTotal))
        mysql.connection.commit()

        # Send user back to the main orders page
        return redirect("/orders")

@app.route("/orders-edit/<int:id>/<employeeName>/<total>", methods=["POST", "GET"])
def edit_order(id, employeeName, total):

    # Remove dollar sign from total
    total = total.replace('$', '')
    
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
        WHERE orderId = %s
        """ % (id)

        cur = mysql.connection.cursor()
        cur.execute(orderQuery)
        orders = cur.fetchall()

        # Call the dropdown creation function to query the database and pass values to the orders
        employees, stores, customers = ordersDropdownDatasets()

        return render_template("orders-edit.j2", orders=orders, employees=employees, stores=stores, customers=customers, orderNum=id, employeeName=employeeName, total=total)

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

@app.route("/orders-delete/<int:id>", methods=["POST", "GET"])
def delete_order(id):
    
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

        return render_template("orders-delete.j2", orders=orders, orderNum=id)

    if request.method == "POST":

         # Fires if user presses the Edit button
        if request.form.get("Delete_Order"):
            orderID = request.form["orderID"]
        
        deleteQuery = """
        DELETE FROM Orders
        WHERE
        Orders.orderID = %s
        """
        cursor = mysql.connection.cursor()
        cursor.execute(deleteQuery, (orderID))
        mysql.connection.commit()

        return redirect("/orders")

@app.route('/stores', methods=["POST", "GET"])
def stores():

    if request.method == "GET":

        readQuery = """
        SELECT 
        Stores.storeID AS "Store #",
        Stores.addressStreet AS "Street",
        Stores.addressCity AS "City",
        Stores.addressState AS "State",
        Stores.addressZip AS "Zip Code"
        FROM Stores;
        """

        cursor = mysql.connection.cursor()
        cursor.execute(readQuery)
        stores = cursor.fetchall()

        return render_template("stores.j2", stores=stores)

    if request.method == "POST":

        # Fires if user presses the New button
        if request.form.get("Add_Store"):
            street = request.form["addressStreet"]
            city = request.form["addressCity"]
            state = request.form["addressState"]
            zip = request.form["addressZip"]

        # Grabs the next store number in line, so the user doesn't need to know what the correct store number is for Insert functions
        nextStoreQuery = """
        SELECT MAX(storeID) + 1 FROM Stores
        """

        cursor = mysql.connection.cursor()
        cursor.execute(nextStoreQuery)
        storeID = cursor.fetchall()

        insertQuery = """
        INSERT INTO Stores (storeID, addressStreet, addressCity, addressState, addressZip) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (storeID, street, city, state, zip))
        mysql.connection.commit()

        # Send user back to the main stores page
        return redirect("/stores")

@app.route("/stores-edit/<int:id>", methods=["POST", "GET"])
def edit_store(id):

    if request.method == "GET":

        orderQuery = """
        SELECT 
        Stores.storeID AS "Store #",
        Stores.addressStreet AS "Street",
        Stores.addressCity AS "City",
        Stores.addressState AS "State",
        Stores.addressZip AS "Zip Code"
        FROM Stores
        WHERE storeID = %s
        """ % (id)

        cur = mysql.connection.cursor()
        cur.execute(orderQuery)
        stores = cur.fetchall()

        return render_template("stores-edit.j2", stores=stores, storeNum=id)


    if request.method == "POST":

        # Fires if user presses the Edit button
        if request.form.get("Edit_Store"):
            storeID = request.form["storeID"]
            street = request.form["street"]
            city = request.form["city"]
            state = request.form["state"]
            zip = request.form["zip"]

        updateQuery = """
        UPDATE Stores
        SET 
        Stores.addressStreet = %s,
        Stores.addressCity = %s,
        Stores.addressState = %s,
        Stores.addressZip = %s
        WHERE
        Stores.storeID = %s
        """
        cursor = mysql.connection.cursor()
        cursor.execute(updateQuery, (street, city, state, zip, storeID))
        mysql.connection.commit()

        return redirect("/stores")

@app.route("/stores-delete/<int:id>", methods=["POST", "GET"])
def delete_store(id):
    
    if request.method == "GET":

        storeQuery = """
        SELECT 
        Stores.storeID AS "Store #",
        Stores.addressStreet AS "Street",
        Stores.addressCity AS "City",
        Stores.addressState AS "State",
        Stores.addressZip AS "Zip Code"
        FROM Stores
        WHERE storeId = %s""" % (id)
        cur = mysql.connection.cursor()
        cur.execute(storeQuery)
        stores = cur.fetchall()

        return render_template("stores-delete.j2", stores=stores, storeNum=id)

    if request.method == "POST":

         # Fires if user presses the Edit button
        if request.form.get("Delete_Store"):
            storeID = request.form["storeID"]
        
        deleteQuery = """
        DELETE FROM Stores
        WHERE
        Stores.storeID = %s
        """
        cursor = mysql.connection.cursor()
        cursor.execute(deleteQuery, (storeID))
        mysql.connection.commit()

        return redirect("/stores")

@app.route('/customers', methods=["POST", "GET"])
def customers():

    if request.method == "GET":

        # Grabs all data for the main Customers table
        readQuery = """
        SELECT 
        Customers.customerID AS "Customer #",
        Customers.email AS "Email Address",
        Customers.firstName AS "First",
        Customers.lastName AS "Last",
        Customers.addressStreet AS "Street",
        Customers.addressCity AS "City",
        Customers.addressState AS "State",
        Customers.addressZip AS "Zip",
        Customers.cusTotalSales AS "Total Sales",
        RewardsTiers.rewardsTierName AS "Rewards Tier"
        FROM Customers
        INNER JOIN RewardsTiers ON Customers.RewardsTiers_rewardsTierId = RewardsTiers.rewardsTierId
        ORDER BY Customers.customerID ASC;
        """

        cursor = mysql.connection.cursor()
        cursor.execute(readQuery)
        customers = cursor.fetchall()

        tiers = customersDropDowns()

        return render_template("customers.j2", customers=customers, tiers=tiers)

    if request.method == "POST":

        # Fires if user presses the New button
        if request.form.get("Add_Customer"):
            email = request.form["emailAddress"]
            first = request.form["firstName"]
            last = request.form["lastName"]
            street = request.form["addressStreet"]
            city = request.form["addressCity"]
            state = request.form["addressState"]
            zip = request.form["addressZip"]
            sales = request.form["totalSales"]
            tier = request.form["rewardsTier"]

        # Grabs the next customer number in line, so the user doesn't need to know what the correct order number is for Insert functions
        nextCustomerQuery = """
        SELECT MAX(customerID) + 1 AS "nextCustomerNum" FROM Customers
        """

        cursor = mysql.connection.cursor()
        cursor.execute(nextCustomerQuery)
        customerID = cursor.fetchall()

        insertQuery = """
        INSERT INTO Customers(
        customerID, 
        email, 
        firstName, 
        lastName, 
        addressStreet, 
        addressCity, 
        addressState, 
        addressZip, 
        cusTotalSales, 
        RewardsTiers_rewardsTierId)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (customerID, email, first, last, street, city, state, zip, sales, tier))
        mysql.connection.commit()

        # Send user back to the main stores page
        return redirect("/customers")



@app.route("/customers-delete/<int:id>", methods=["POST", "GET"])
def delete_customer(id):
    
    if request.method == "GET":

        customerQuery = """
        SELECT
        Customers.customerID AS "Customer #",
        Customers.email AS "Email Address",
        Customers.firstName AS "First",
        Customers.lastName AS "Last",
        Customers.addressStreet AS "Street",
        Customers.addressCity AS "City",
        Customers.addressState AS "State",
        Customers.addressZip AS "Zip",
        Customers.cusTotalSales AS "Total Sales",
        RewardsTiers.rewardsTierName AS "Rewards Tier"
        FROM Customers
        INNER JOIN RewardsTiers ON Customers.RewardsTiers_rewardsTierId = RewardsTiers.rewardsTierId
        WHERE customerId = %s""" % (id)
        cur = mysql.connection.cursor()
        cur.execute(customerQuery)
        customers = cur.fetchall()

        return render_template("customers-delete.j2", customers=customers, customerNum=id)

    if request.method == "POST":

         # Fires if user presses the Edit button
        if request.form.get("Delete_Customer"):
            customerID = request.form["customerID"]
        
        deleteQuery = """
        DELETE FROM Customers
        WHERE
        Customers.customerID = %s
        """
        cursor = mysql.connection.cursor()
        cursor.execute(deleteQuery, (customerID))
        mysql.connection.commit()

        return redirect("/customers")

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