from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

app.config['MYSQL_HOST'] = 'flip3.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_rowanje'
app.config['MYSQL_PASSWORD'] = '7573' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_rowanje'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 

@app.route('/')
def root():
    return render_template("index.j2")

@app.route('/orders')
def orders():

    #Read
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

    cursor = db.execute_query(db_connection=db_connection, query=readQuery)

    results = cursor.fetchall()

    return render_template("orders.j2", Orders=results)

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