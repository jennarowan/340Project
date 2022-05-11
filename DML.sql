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
SELECT * FROM Orders;

-----------------Stores-------------------
-- Create
INSERT INTO Stores(storeID, addressStreet, addressCity, addressState, addressZip)
VALUES(:storeID_input, :addressStreet_input, :addressCity_input, :addressState_input, :addressZip_input);

-- Read
SELECT * FROM Stores;

-- Update
UPDATE Stores SET
    addressStreet = :addressStreet_input, addressCity = :addressCity_input, addressState = :addressState_input, 
    addressZip = :addressZip
    WHERE storeID = :storeID_input;

-- Delete
DELETE FROM Stores WHERE Stores.storeID = :storeID_input;


-----------------Customers-------------------
-- Create
INSERT INTO Customers(customerID, email, firstName, lastName, addressStreet, addressCity, addressState, addressZip, totalSales, rewardsTierId)
VALUES(:customerID_input, :email_input, :firstName_input, :lastName_input, :addressStreet_input, :addressCity_input, :addressState_input, :addressZip_input, :totalSales_input, :rewardsTierId_input);

-- Read
SELECT * FROM Customers;

-- Update
UPDATE Customers SET
    customerID = :customerID_input, email = :email_input, first_name = :firstName_input, lastname = :lastName_input, 
    addressStreet = :addressStreet_input, addressCity = :addressCity_input, addressState = :addressState_input, addressZip = :addressZip_input, totalSales = :totalSales_input, rewardsTierId = :rewardsTierId_input
    WHERE customerID = :customerID_input;

-- Delete
DELETE FROM Customers WHERE Customers.customerId = :customerID_input;



-----------------Employees-------------------
-- Create
INSERT INTO Employees(employeeID, SocialSecurityNumber, firstName, lastName, phoneNumber, addressStreet, addressCity, addressState, addressZip)
VALUES(:employeeID_input, :SocialSecurityNumber, :firstName_input, :lastName_input, :phoneNumber_input, :addressStreet_input, :addressCity_input, :addressState_input, :addressZip_input);

-- Read
SELECT * FROM Employees;

-- Update
UPDATE Employees SET
    employeeID = :employeeID_input, SocialSecurityNumber = :SocialSecurityNumber, first_name = :firstName_input, lastname = :lastName_input, 
    addressStreet = :addressStreet_input, addressCity = :addressCity_input, addressState = :addressState_input, addressZip = :addressZip_input
    WHERE employeeID = :employeeID_input;

-- Delete
DELETE FROM Employees WHERE Employees.employeeId = :employeeID_input;



-----------------Liquors-------------------
-- Create
INSERT INTO Liquors(productID, productName, productSize, productPrice)
VALUES(:productID_input, :productName_input, :productSize_input, :productPrice_input);

-- Read
SELECT * FROM Liquors;

-- Update
UPDATE Liquors SET
    productID = :productID_input, productName = :productName_input, productSize = :productSize_input, productPrice = :productPrice_input
    WHERE productID = :productID_input;

-- Delete
DELETE FROM Liquors WHERE Liquors.productID = :prodcutID_input;



-----------------RewardsTiers-------------------

-- Create
INSERT INTO RewardsTiers(rewardsTierID, rewardsTierName, rewardsTierDiscount, rewardsTierMinPurchase)
VALUES(:rewardsTierID_input, :rewardsTierName_input, :rewardsTierDiscount_input, :rewardsTierMinPurchase_input);

-- Read
SELECT * FROM RewardsTiers;

-- Update
UPDATE RewardsTiers SET
    produrewardsTierID = :rewardsTierID_input, rewardsTierName = :rewardsTierName_input, rewardsTierDiscount = :rewardsTierDiscount_input, rewardsTierMinPurchase = :rewardsTierMinPurchase_input
    WHERE RewardsTiersID = :RewardsTiersID_input;

-- Delete
DELETE FROM RewardsTiers WHERE RewardsTiers.RewardsTiersID = :RewardsTiersID_input;



-------------------LiquorsOrders-------------------

-- Create
INSERT INTO LiquorsOrders(productID, OrderID, productQuantity)
VALUES(:productID_input, :OrderID_input, :productQuantity_input);

-- Read
SELECT * FROM LiquorsOrders;

-- Update
-- Change this to cascade?
UPDATE LiquorsOrders SET
    productID = :productID, OrderID = :OrderID, productQuantity = :productQuantity_input
    WHERE productID = :productID_input and orderID = :orderID_input;


-- Delete
DELETE FROM LiquorsOrders WHERE LiquorsOrders.LiquorsOrdersID = :LiquorsOrdersID_input;