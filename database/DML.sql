/*
Draft Version of DML queries for JL Liquor
Author: Liam Maloney and Jenna Rowan
Creation Date: May 5th, 2022
Last Updated Date: May 19th, 2022
*/

-----------------Orders-------------------

-- Create
INSERT INTO Orders (
orderID, 
Employees_employeeID, 
Stores_storeID, 
Customers_customerID, 
orderTotal) 
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

-- Update Total Sales on Customers table when an order is added
UPDATE Customers
JOIN RewardsTiers
ON Customers.RewardsTiers_rewardsTierId = RewardsTiers.rewardsTierId
SET 
Customers.cusTotalSales = Customers.cusTotalSales + %s
WHERE
Customers.customerID = %s

-- Update Total Sales on Customers table when an order is edited
UPDATE Customers
JOIN RewardsTiers
ON Customers.RewardsTiers_rewardsTierId = RewardsTiers.rewardsTierId
SET 
Customers.cusTotalSales = Customers.cusTotalSales - %s + %s 
WHERE
Customers.customerID = %s

-- Update Total Sales on Customers table when an order is deleted
UPDATE Customers
JOIN RewardsTiers
ON Customers.RewardsTiers_rewardsTierId = RewardsTiers.rewardsTierId
SET 
Customers.cusTotalSales = Customers.cusTotalSales - %s
WHERE
Customers.customerID = %s

-- Delete
DELETE FROM Orders
WHERE
Orders.orderID = %s


-----------------Stores-------------------
-- Create
INSERT INTO Stores (
storeID, 
addressStreet, 
addressCity, 
addressState, 
addressZip) 
VALUES (%s, %s, %s, %s, %s);

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
DELETE FROM Customers
WHERE
Customers.customerID = %s

-----------------Employees-------------------
-- Create
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
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);

-- Read
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

-- Update
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

-- Delete
DELETE FROM Employees
WHERE
Employees.employeeID = %s


-----------------Liquors-------------------
-- Create
INSERT INTO Liquors(productID, productName, productSizeMl, productPrice)
VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);

-- Read
SELECT 
Liquors.productID as "Product #",
Liquors.productName as "Name",
Liquors.productSizeMl as "Size (in ml)",
Liquors.productPrice as "Price ($)"
FROM Liquors;

-- Update
UPDATE Liquors
SET 
Liquors.productID = %s,
Liquors.productName = %s,
Liquors.productSizeMl = %s,
Liquors.productPrice = %s
WHERE 
Liquors.productID = %s

-- Delete
DELETE FROM Liquors
WHERE
Liquors.productID = %s


-----------------RewardsTiers-------------------

-- Create
INSERT INTO RewardsTiers(rewardsTierID, rewardsTierName, rewardsTierDiscount, rewardsTierMinPurchase)
VALUES(%s, %s, %s, %s);

-- Read
SELECT 
RewardsTiers.rewardsTierID as 'Reward Tier #',
RewardsTiers.rewardsTierName as 'Reward Tier Name',
RewardsTiers.rewardsTierDiscount as 'Reward Tier Discount (%)',
RewardsTiers.rewardsTierMinPurchase as 'Reward Tier Min Purchase'
FROM RewardsTiers;



-------------------LiquorsOrders-------------------

-- Create
INSERT INTO LiquorsOrders(productID, orderID, productQuantity)
VALUES(%s, %s, %s);

-- Read
SELECT 
LiquorsOrders.productID as 'Product #',
LiquorsOrders.orderID as 'Order #',
LiquorsOrders.productQuantity as 'Product Quantity (EA)'
FROM LiquorsOrders;

-- -- Update
-- UPDATE LiquorsOrders SET
--     productID = :productID, OrderID = :OrderID, productQuantity = :productQuantity_input
--     WHERE productID = :productID_input and orderID = :orderID_input;

-- -- Delete
-- DELETE FROM LiquorsOrders WHERE LiquorsOrders.LiquorsOrdersID = :LiquorsOrdersID_input;