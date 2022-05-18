/*
Draft Version of DML queries for JL Liquor
Author: Liam Maloney
Date: May 5th, 2022
*/

-----------------Orders-------------------

-- Create
INSERT INTO Orders(orderID, employeeID, storeID, customerID, orderTotal)
VALUES(:orderID_input, :employyeID_input, :storeID_input, :customerID_input, orderTotal);

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



-----------------Stores-------------------
-- Create
INSERT INTO Stores(storeID, addressStreet, addressCity, addressState, addressZip)
VALUES(:storeID_input, :addressStreet_input, :addressCity_input, :addressState_input, :addressZip_input);

-- Read
SELECT * FROM Stores;



-----------------Customers-------------------
-- Create
INSERT INTO Customers(customerID, email, firstName, lastName, addressStreet, addressCity, addressState, addressZip, totalSales, rewardsTierId)
VALUES(:customerID_input, :email_input, :firstName_input, :lastName_input, :addressStreet_input, :addressCity_input, :addressState_input, :addressZip_input, :totalSales_input, :rewardsTierId_input);

-- Read
SELECT 
Customers.customerID,
Customers.email,
Customers.firstName,
Customers.lastName,
Customers.addressStreet,
Customers.addressCity,
Customers.addressState,
Customers.addressZip,
Customers.cusTotalSales,
RewardsTiers.rewardsTierName
FROM Customers
INNER JOIN RewardsTiers ON Customers.RewardsTiers_rewardsTierId = RewardsTiers.rewardsTierId
ORDER BY Customers.customerID ASC;



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