from flask import Flask, render_template, url_for, redirect
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
    image_file = url_for('static', filename="liquor.jpg")

    return render_template("index.j2", image_file=image_file)

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
        INSERT INTO Orders (
        orderID, 
        Employees_employeeID, 
        Stores_storeID, 
        Customers_customerID, 
        orderTotal) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (orderID, employeeID, storeID, customer, orderTotal))
        mysql.connection.commit()

        # Updates the total sales for the given customer on the customers table by adding the total of the new order
        # The rewards tier join is for multiplying the order total by the correct discount (doesn't currently work)
        updateCustomersQuery = """
        UPDATE Customers
        JOIN RewardsTiers
        ON Customers.RewardsTiers_rewardsTierId = RewardsTiers.rewardsTierId
        SET 
        Customers.cusTotalSales = Customers.cusTotalSales + %s
        WHERE
        Customers.customerID = %s
        """
        cursor = mysql.connection.cursor()
        cursor.execute(updateCustomersQuery, (orderTotal, customer))
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
        
        # Updates the order information in the orders table
        updateOrdersQuery = """
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
        cursor.execute(updateOrdersQuery, (employeeID, storeID, customer, orderTotal, orderID))
        mysql.connection.commit()

        # Updates the total sales for the given customer on the customers table by subtracting the original order total and adding the new one
        updateCustomersQuery = """
        UPDATE Customers
        JOIN RewardsTiers
        ON Customers.RewardsTiers_rewardsTierId = RewardsTiers.rewardsTierId
        SET 
        Customers.cusTotalSales = Customers.cusTotalSales - %s + %s 
        WHERE
        Customers.customerID = %s
        """
        cursor = mysql.connection.cursor()
        cursor.execute(updateCustomersQuery, (total, orderTotal, customer))
        mysql.connection.commit()

        return redirect("/orders")

@app.route("/orders-delete/<int:id>/<orderTotal>", methods=["POST", "GET"])
def delete_order(id, orderTotal):
    
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

        return render_template("orders-delete.j2", orders=orders, orderNum=id, orderTotal=orderTotal)

    if request.method == "POST":

         # Fires if user presses the Edit button
        if request.form.get("Delete_Order"):
            orderID = request.form["orderID"]

        # Remove dollar sign from total
        orderTotal = orderTotal.replace('$', '')
        
        ############# DOES NOT WORK #############################

        # Updates the total sales for the given customer on the customers table by subtracting the original order total and adding the new one

        # Grabs customer ID given order ID
        # customerQuery = """
        # SELECT
        # Customers_customerID
        # FROM Orders
        # WHERE orderID = %s
        # """

        # cursor = mysql.connection.cursor()
        # cursor.execute(customerQuery, (orderID))
        # customer = cursor.fetchall()

        # # "customer" is a tuple object at this point instead of being a simple integer

        # # orderTotal is perfect
        
        # updateCustomersQuery = """
        # UPDATE Customers
        # SET 
        # Customers.cusTotalSales = Customers.cusTotalSales - %s
        # WHERE
        # Customers.customerID = %s
        # """
        # cursor = mysql.connection.cursor()
        # cursor.execute(updateCustomersQuery, (orderTotal, customer))
        # mysql.connection.commit()

        ########################################################

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
        INSERT INTO Stores (
        storeID, 
        addressStreet, 
        addressCity, 
        addressState, 
        addressZip) 
        VALUES (%s, %s, %s, %s, %s);
        """
        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (storeID, street, city, state, zip))
        mysql.connection.commit()

        # Send user back to the main stores page
        return redirect("/stores")

@app.route("/stores-edit/<int:id>/<addressStreet>/<addressCity>/<addressState>/<addressZip>", methods=["POST", "GET"])
def edit_store(id, addressStreet, addressCity, addressState, addressZip):

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
        store = cur.fetchall()

        return render_template("stores-edit.j2", store=store, storeNum=id, addressStreet=addressStreet, addressCity=addressCity, addressState=addressState, addressZip=addressZip)


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
        CONCAT("$", Customers.cusTotalSales) AS "Total Sales",
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

@app.route("/customers-edit/<int:id>/<emailAddress>/<firstName>/<lastName>/<addressStreet>/<addressCity>/<addressState>/<addressZip>/<totalSales>/<rewardsTier>", methods=["POST", "GET"])
def edit_customer(id, emailAddress, firstName, lastName, addressStreet, addressCity, addressState, addressZip, totalSales, rewardsTier):

    # Remove dollar sign from total
    totalSales = totalSales.replace('$', '')
    
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
        CONCAT("$", Customers.cusTotalSales) AS "Total Sales",
        RewardsTiers.rewardsTierName AS "Rewards Tier"
        FROM Customers
        INNER JOIN RewardsTiers ON Customers.RewardsTiers_rewardsTierId = RewardsTiers.rewardsTierId
        WHERE customerId = %s
        """ % (id)

        cur = mysql.connection.cursor()
        cur.execute(customerQuery)
        customers = cur.fetchall()

        # Call the dropdown creation function to query the database and pass values to the customers
        tiers = customersDropDowns()

        return render_template("customers-edit.j2", customers=customers, customerNum=id, emailAddress=emailAddress, firstName=firstName, lastName=lastName, addressStreet=addressStreet, addressCity=addressCity, addressState=addressState, addressZip=addressZip, totalSales=totalSales, rewardsTier=rewardsTier, tiers=tiers)

    if request.method == "POST":

         # Fires if user presses the Edit button
        if request.form.get("Edit_Customer"):
            customerID = request.form["customerID"]
            email = request.form["emailAddress"]
            first = request.form["firstName"]
            last = request.form["lastName"]
            street = request.form["street"]
            city = request.form["city"]
            state = request.form["state"]
            zip = request.form["zip"]
            sales = request.form["sales"]
            tier = request.form["tier"]
        
        updateQuery = """
        UPDATE Customers
        SET 
        Customers.email = %s,
        Customers.firstName = %s,
        Customers.lastName = %s,
        Customers.addressStreet = %s,
        Customers.addressCity = %s,
        Customers.addressState = %s,
        Customers.addressZip = %s,
        Customers.cusTotalSales = %s,
        Customers.RewardsTiers_rewardsTierId = %s
        WHERE
        Customers.customerID = %s
        """
        cursor = mysql.connection.cursor()
        cursor.execute(updateQuery, (email, first, last, street, city, state, zip, sales, tier, customerID))
        mysql.connection.commit()

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

@app.route('/employees', methods=["POST", "GET"])
def employees():

    if request.method == "GET":

        readQuery = """
        SELECT
        Employees.employeeID AS "Employee #",
        Employees.socialSecurityNumber AS "SSN",
        Employees.firstName AS "First",
        Employees.lastName AS "Last",
        Employees.phoneNumber AS "Phone #",
        Employees.addressStreet AS "Street",
        Employees.addressCity AS "City",
        Employees.addressState AS "State",
        Employees.addressZip AS "Zip Code"
        FROM Employees;
        """

        cursor = mysql.connection.cursor()
        cursor.execute(readQuery)
        employees = cursor.fetchall()

        return render_template("employees.j2", employees=employees)

    if request.method == "POST":

        # Fires if user presses the New button
        if request.form.get("Add_Employee"):
            ssn = request.form["socialSecurityNumber"]
            first = request.form["firstName"]
            last = request.form["lastName"]
            phone = request.form["phoneNumber"]
            street = request.form["addressStreet"]
            city = request.form["addressCity"]
            state = request.form["addressState"]
            zip = request.form["addressZip"]

        # Grabs the next employee number in line, so the user doesn't need to know what the correct order number is for Insert functions
        nextEmployeeQuery = """
        SELECT MAX(employeeID) + 1 AS "nextEmployeeNum" FROM Employees
        """

        cursor = mysql.connection.cursor()
        cursor.execute(nextEmployeeQuery)
        employeeID = cursor.fetchall()

        insertQuery = """
        INSERT INTO Employees(
        employeeID, 
        socialSecurityNumber, 
        firstName, 
        lastName, 
        phoneNumber,
        addressStreet, 
        addressCity, 
        addressState, 
        addressZip)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (employeeID, ssn, first, last, phone, street, city, state, zip))
        mysql.connection.commit()

        # Send user back to the main employees page
        return redirect("/employees")

@app.route("/employees-edit/<int:id>/<ssn>/<firstName>/<lastName>/<phone>/<addressStreet>/<addressCity>/<addressState>/<addressZip>", methods=["POST", "GET"])
def edit_employee(id, ssn, firstName, lastName, phone, addressStreet, addressCity, addressState, addressZip):
    
    if request.method == "GET":

        employeeQuery = """
        SELECT 
        Employees.employeeID AS "Employee #",
        Employees.socialSecurityNumber AS "SSN",
        Employees.firstName AS "First",
        Employees.lastName AS "Last",
        Employees.phoneNumber AS "Phone #",
        Employees.addressStreet AS "Street",
        Employees.addressCity AS "City",
        Employees.addressState AS "State",
        Employees.addressZip AS "Zip Code"
        FROM Employees
        WHERE employeeId = %s
        """ % (id)

        cur = mysql.connection.cursor()
        cur.execute(employeeQuery)
        employees = cur.fetchall()

        return render_template("employees-edit.j2", employees=employees, employeeNum=id, ssn=ssn, firstName=firstName, lastName=lastName, phone=phone, addressStreet=addressStreet, addressCity=addressCity, addressState=addressState, addressZip=addressZip)

    if request.method == "POST":

         # Fires if user presses the Edit button
        if request.form.get("Edit_Employee"):
            employeeID = request.form["employeeID"]
            social = request.form["ssn"]
            first = request.form["firstName"]
            last = request.form["lastName"]
            phoneNum = request.form["phoneNumber"]
            street = request.form["street"]
            city = request.form["city"]
            state = request.form["state"]
            zip = request.form["zip"]
        
        updateQuery = """
        UPDATE Employees
        SET 
        Employees.socialSecurityNumber = %s,
        Employees.firstName = %s,
        Employees.lastName = %s,
        Employees.phoneNumber = %s,
        Employees.addressStreet = %s,
        Employees.addressCity = %s,
        Employees.addressState = %s,
        Employees.addressZip = %s
        WHERE
        Employees.employeeID = %s
        """
        cursor = mysql.connection.cursor()
        cursor.execute(updateQuery, (social, first, last, phoneNum, street, city, state, zip, employeeID))
        mysql.connection.commit()

        return redirect("/employees")

@app.route("/employees-delete/<int:id>", methods=["POST", "GET"])
def delete_employee(id):
    
    if request.method == "GET":

        employeeQuery = """
        SELECT
        Employees.employeeID AS "Employee #",
        Employees.socialSecurityNumber AS "SSN",
        Employees.firstName AS "First",
        Employees.lastName AS "Last",
        Employees.phoneNumber AS "Phone #",
        Employees.addressStreet AS "Street",
        Employees.addressCity AS "City",
        Employees.addressState AS "State",
        Employees.addressZip AS "Zip Code"
        FROM Employees
        WHERE employeeId = %s""" % (id)
        cur = mysql.connection.cursor()
        cur.execute(employeeQuery)
        employees = cur.fetchall()

        return render_template("employees-delete.j2", employees=employees, employeeNum=id)

    if request.method == "POST":

         # Fires if user presses the Edit button
        if request.form.get("Delete_Employee"):
            employeeID = request.form["employeeID"]
        
        deleteQuery = """
        DELETE FROM Employees
        WHERE
        Employees.employeeID = %s
        """
        cursor = mysql.connection.cursor()
        cursor.execute(deleteQuery, (employeeID))
        mysql.connection.commit()

        return redirect("/employees")

@app.route('/liquors', methods=["POST", "GET"])
def liquors():

    if request.method == "GET":

        # Read
        readQuery = """
        SELECT 
        Liquors.productID as "Product #",
        Liquors.productName as "Name",
        Liquors.productSizeMl as "Size (in ml)",
        Liquors.productPrice as "Price ($)"
        FROM Liquors;
        """

        cursor = mysql.connection.cursor()
        cursor.execute(readQuery)
        liquors = cursor.fetchall()
    

        return render_template("liquors.j2", liquors=liquors)
    
    if request.method =="POST":

        # Create
        if request.form.get("Add_Liquor"): # Find where this is coming from?
            productID = request.form["productID"]
            productName = request.form["productName"]
            productSizeMl = request.form["productSize(ML)"]
            productPrice = request.form["productPrice"]

        # Sets next productID, so user doesn't need to look
        nextProductIDQuery = """
        SELECT MAX(productID) + 1 AS "nextProductID" FROM Liquors
        """

        cursor = mysql.connection.cursor()
        cursor.execute(nextProductIDQuery)
        productID = cursor.fetchall()

        insertQuery = """
        INSERT INTO Liquors(
            productID, 
            productName, 
            productSizeMl, 
            productPrice)
        VALUES(%s, %s, %s, %s);
        """

        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (productID, productName, productSizeMl, productPrice))
        mysql.connection.commit()

        # Send user back to main liquors page
        return redirect("/liquors")

@app.route('/liquors-edit/<int:productID>/<productName>/<productSizeMl>/<productPrice>', methods=["POST", "GET"]) # Look back to make sure the string is correct, not sure..
def edit_liquor(productID, productName, productSizeMl, productPrice):

    if request.method == "GET":

        liquorsQuery = """
        UPDATE Liquors
        SET 
        Liquors.productID = %s,
        Liquors.productName = %s,
        Liquors.productSizeMl = %s,
        Liquors.productPrice = %s
        WHERE 
        Liquors.productID = %s
        """ % (productID)

        cur = mysql.connection.cursor()
        cur.execute(liquorsQuery)
        liquors = cur.fetchall()

        return render_template("liquors-edit.j2", productID = productID, productName = productName, productSizeMl = productSizeMl, productPrice = productPrice)
    
    if request.method == "POST":

        updateQuery = """
        UPDATE Liquors
        SET 
        Liquors.productID = %s,
        Liquors.productName = %s,
        Liquors.productSizeMl = %s,
        Liquors.productPrice = %s
        WHERE 
        Liquors.productID = %s
        """

        cursor = mysql.connection.cursor()
        cursor.execute(updateQuery, (productID, productName, productSizeMl, productPrice))
        mysql.connection.commit()

        return redirect("/liquors")

@app.route('/liquors-delete/<int:productID>', methods=["POST","GET"])
def delete_liquor(productID):

    if request.method == "GET":

        liquorQuery = """
        SELECT 
        Liquors.productID as "Product #",
        Liquors.productName as "Name",
        Liquors.productSizeMl as "Size (in ml)",
        Liquors.productPrice as "Price ($)"
        FROM Liquors
        WHERE productID = %s""" % (productID)

        cur = mysql.connection.cursor()
        cur.execute(liquorQuery)
        liquors = cur.fetchall()

        return render_template("liquors-delete.j2", liquors=liquors, productID = productID)
    
    if request.method == "POST":

        if request.form.get("Delete_Liquor"):
            productID = request.form["productID"]

        deleteQuery = """
        DELETE FROM Liquors
        WHERE
        Liquors.productID = %s
        """

        cursor = mysql.connection.cursor()
        cursor.execute(deleteQuery, (productID))
        mysql.connection.commit()

        return redirect('/liquors')


@app.route('/rewardtiers', methods = ["POST", "GET"])
def rewardstiers():

    if request.method == "GET":

        #Read
        readQuery = """
        SELECT 
        RewardsTiers.rewardsTierId as 'Reward Tier #',
        RewardsTiers.rewardsTierName as 'Reward Tier Name',
        RewardsTiers.rewardsTierDiscount as 'Reward Tier Discount (%)',
        RewardsTiers.rewardsTierMinPurchase as 'Reward Tier Min Purchase'
        FROM RewardsTiers;
        """

        cursor = mysql.connection.cursor()
        cursor.execute(readQuery)
        rewardstiers = cursor.fetchall()

        return render_template("rewardstiers.j2", rewardstiers=rewardstiers)

    if request.method == "POST":

        #Create
        if request.form.get("Add_RewardsTiers"):
            rewardsTierID = request.form["rewardsTierId"]
            rewardsTierName = request.form["rewardsTierName"]
            rewardsTierDiscount = request.form["rewardsTierDiscount"]
            rewardsTierMinPurchase = request.form["rewardsTierMinPurchase"]
        
        # Tier Ids are Already genereated, we automatically are creating 1-3 (Bronze-Gold), 4 will be made by user
        # !! THIS IS AUTOINCREMENTED DO I NEED THIS STEP?
        # nextrewardsTierIDQuery = """
        # SELECT MAX(rewardsTierID) + 1 AS "nextrewardsTierID" FROM RewardsTiers
        # """

        # cursor = mysql.connection.cursor()
        # cursor.execute(nextrewardsTierIDQuery)
        # rewardsTierID = cursor.fetchall()


        insertQuery = """
        INSERT INTO RewardsTiers(
            rewardsTierId, 
            rewardsTierName, 
            rewardsTierDiscount, 
            rewardsTierMinPurchase)
        VALUES(%s, %s, %s, %s);
        """

        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (rewardsTierID, rewardsTierName, rewardsTierDiscount, rewardsTierMinPurchase))
        mysql.connection.commit()

        # Send user back to main rewardstiers page
        return redirect("/rewardtiers")


@app.route('/liquorsorders', methods=["POST","GET"])
def liquorsorders():
    
    if request.method == "GET":

        # Read
        readQuery = """
        SELECT 
        LiquorsOrders.Liquors_productID as 'Product #',
        LiquorsOrders.Orders_orderID as 'Order #',
        LiquorsOrders.productQuantity as 'Product Quantity (EA)'
        FROM LiquorsOrders;
        """

        cursor = mysql.connection.cursor()
        cursor.execute(readQuery)
        liquorsorders = cursor.fetchall()
        
        return render_template("liquorsorders.j2", liquorsorders=liquorsorders)
    
    if request.method == "POST":

        # Create
        if request.form.get("Add_LiquorsOrders"):
            Liquors_productID = request.form["Liquors_productID"]
            Orders_orderID = request.form["Orders_orderID"]
            productQuantity = request.form["productQuantity"]
        
        insertQuery = """
        INSERT INTO LiquorsOrders(
            Liquors_productID, 
            Orders_orderID, 
            productQuantity)
        VALUES(%s, %s, %s);
        """
        
        cursor = mysql.connection.cursor()
        cursor.execute(insertQuery, (Liquors_productID, Orders_orderID, productQuantity))
        mysql.connection.commit()

        # Send user back to main liquorsorders page
        return redirect('/liquorsorders')

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 