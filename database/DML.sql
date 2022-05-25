/*
Draft Version of DML queries for JL Liquor
Author: Liam Maloney and Jenna Rowan
Creation Date: May 5th, 2022
Last Updated Date: May 19th, 2022
*/

-----------------Orders-------------------

-- Create
INSERT INTO Orders (orderID, Employees_employeeID, Stores_storeID, Customers_customerID, orderTotal) 
VALUES (%s, %s, %s, %s, %s)

-- Read
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

-- Update
UPDATE Orders
SET 
Orders.Employees_employeeID = %s,
Orders.Stores_storeID = %s,
Orders.Customers_customerID = %s,
Orders.orderTotal = %s
WHERE
Orders.orderID = %s

-- Delete
DELETE FROM Orders
WHERE
Orders.orderID = %s


-----------------Stores-------------------
-- Create
INSERT INTO Stores(storeID, addressStreet, addressCity, addressState, addressZip)
VALUES(:storeID_input, :addressStreet_input, :addressCity_input, :addressState_input, :addressZip_input);

-- Read
SELECT 
Stores.storeID AS "Store #",
Stores.addressStreet AS "Street",
Stores.addressCity AS "City",
Stores.addressState AS "State",
Stores.addressZip AS "Zip Code"
FROM Stores;

-- Update
UPDATE Stores
SET 
Stores.addressStreet = %s,
Stores.addressCity = %s,
Stores.addressState = %s,
Stores.addressZip = %s
WHERE
Stores.storeID = %s

-- Delete
DELETE FROM Stores
WHERE
Stores.storeID = %s

-----------------Customers-------------------
-- Create
INSERT INTO Customers(customerID, email, firstName, lastName, addressStreet, addressCity, addressState, addressZip, cusTotalSales, RewardsTiers_rewardsTierId)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

-- Read
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

-- Update
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
Customers.RewardsTiers_rewardsTierId = %s,
WHERE
Customers.customerID = %s

-- Delete


-----------------Employees-------------------
-- Create
INSERT INTO Employees(employeeID, SocialSecurityNumber, firstName, lastName, phoneNumber, addressStreet, addressCity, addressState, addressZip)
VALUES(:employeeID_input, :SocialSecurityNumber, :firstName_input, :lastName_input, :phoneNumber_input, :addressStreet_input, :addressCity_input, :addressState_input, :addressZip_input);

-- Read
SELECT * FROM Employees;



-----------------Liquors-------------------
-- Create
INSERT INTO Liquors(productID, productName, productSize, productPrice)
VALUES(:productID_input, :productName_input, :productSize_input, :productPrice_input);

-- Read
SELECT * FROM Liquors;



-----------------RewardsTiers-------------------

-- Create
INSERT INTO RewardsTiers(rewardsTierID, rewardsTierName, rewardsTierDiscount, rewardsTierMinPurchase)
VALUES(:rewardsTierID_input, :rewardsTierName_input, :rewardsTierDiscount_input, :rewardsTierMinPurchase_input);

-- Read
SELECT * FROM RewardsTiers;



-------------------LiquorsOrders-------------------

-- Create
INSERT INTO LiquorsOrders(productID, OrderID, productQuantity)
VALUES(:productID_input, :OrderID_input, :productQuantity_input);

-- Read
SELECT * FROM LiquorsOrders;

-- Update
UPDATE LiquorsOrders SET
    productID = :productID, OrderID = :OrderID, productQuantity = :productQuantity_input
    WHERE productID = :productID_input and orderID = :orderID_input;

-- Delete
DELETE FROM LiquorsOrders WHERE LiquorsOrders.LiquorsOrdersID = :LiquorsOrdersID_input;