SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- -----------------------------------------------------
-- Table Employees
-- -----------------------------------------------------

DROP TABLE IF EXISTS Employees;

CREATE TABLE IF NOT EXISTS Employees (
  employeeID INT NOT NULL AUTO_INCREMENT,
  socialSecurityNumber INT NOT NULL,
  firstName VARCHAR(45) NOT NULL,
  lastName VARCHAR(45) NOT NULL,
  phoneNumber INT NOT NULL,
  addressStreet VARCHAR(100) NOT NULL,
  addressCity VARCHAR(45) NOT NULL,
  addressState VARCHAR(45) NOT NULL,
  addressZip INT NOT NULL,
  PRIMARY KEY (employeeID))
ENGINE = InnoDB;

INSERT INTO Employees (
  socialSecurityNumber,
  firstName,
  lastName,
  phoneNumber,
  addressStreet,
  addressCity,
  addressState,
  addressZip
) VALUES (
  111223333,
  "Hank",
  "Schrader",
  5016204338,
  "4901 Cumbre Del Sur Court",
  "Albuquerque",
  "NM",
  87106
),
(
  222334444,
  "Walter",
  "White",
  5051930809,
  "308 Negra Arroyo Lane",
  "Albuquerque",
  "NM",
  87111
),
(
  333445555,
  "Jesse",
  "Pinkman",
  5051483369,
  "9809 Margo St",
  "Albuquerque",
  "NM",
  87104
);


-- -----------------------------------------------------
-- Table Stores
-- -----------------------------------------------------

DROP TABLE IF EXISTS Stores;

CREATE TABLE IF NOT EXISTS Stores (
  storeID INT NOT NULL AUTO_INCREMENT,
  addressStreet VARCHAR(100) NOT NULL,
  addressCity VARCHAR(45) NOT NULL,
  addressState VARCHAR(45) NOT NULL,
  addressZip INT NOT NULL,
  PRIMARY KEY (storeID))
ENGINE = InnoDB;

INSERT INTO Stores (
  addressStreet,
  addressCity,
  addressState,
  addressZip
) VALUES (
  "9516 Snow Heights Cir NE",
  "Albuquerque",
  "NM",
  87112
),
(
  "322 16th St SW",
  "Albuquerque",
  "NM",
  87104
),
(
  "2660 Fritts Crossing SE",
  "Albuquerque",
  "NM",
  87105
);


-- -----------------------------------------------------
-- Table RewardsTiers
-- -----------------------------------------------------

DROP TABLE IF EXISTS RewardsTiers;

CREATE TABLE IF NOT EXISTS RewardsTiers (
  rewardsTierId INT NOT NULL AUTO_INCREMENT,
  rewardsTierName VARCHAR(45) NOT NULL DEFAULT 'Bronze',
  rewardsTierDiscount DECIMAL(10,2) NOT NULL DEFAULT .995,
  rewardsTierMinPurchase INT NOT NULL,
  PRIMARY KEY (rewardsTierId))
ENGINE = InnoDB;

INSERT INTO RewardsTiers(
  rewardsTierName,
  rewardsTierDiscount,
  rewardsTierMinPurchase
) VALUES (
  "Bronze",
  .995,
  100
),
(
  "Silver",
  .9875,
  500
),
(
  "Gold",
  .98,
  1000
);

-- -----------------------------------------------------
-- Table Customers
-- -----------------------------------------------------

DROP TABLE IF EXISTS Customers;

CREATE TABLE IF NOT EXISTS Customers (
  customerID INT NOT NULL AUTO_INCREMENT,
  email VARCHAR(45) NOT NULL,
  firstName VARCHAR(45) NOT NULL,
  lastName VARCHAR(45) NOT NULL,
  addressStreet VARCHAR(100) NOT NULL,
  addressCity VARCHAR(45) NOT NULL,
  addressState VARCHAR(45) NOT NULL,
  addressZip INT NOT NULL,
  cusTotalSales DECIMAL(10, 2) NOT NULL DEFAULT 0,
  RewardsTiers_rewardsTierId INT,
  PRIMARY KEY (customerID),
  INDEX fk_Customers_RewardsTiers1_idx (RewardsTiers_rewardsTierId ASC) VISIBLE,
  CONSTRAINT fk_Customers_RewardsTiers1
    FOREIGN KEY (RewardsTiers_rewardsTierId)
    REFERENCES RewardsTiers (rewardsTierId)
    ON DELETE CASCADE)
ENGINE = InnoDB;

INSERT INTO Customers (
  email,
  firstName,
  lastName,
  addressStreet,
  addressCity,
  addressState,
  addressZip,
  cusTotalSales,
  RewardsTiers_rewardsTierId
) VALUES (
  "gaslover@aol.com",
  "Hank",
  "Hill",
  "72 Desert Rose Lane",
  "Arlen",
  "TX",
  73104,
  3450,
  3
),
(
  "watchoutfornsa@protonmail.com",
  "Dale",
  "Gribble",
  "63 Desert Rose Lane",
  "Arlen",
  "TX",
  73104,
  7288.37,
  3
),
(
  "lonelybill@gmail.com",
  "Bill",
  "Dauterive",
  "68 Desert Rose Lane",
  "Arlen",
  "TX",
  73104,
  867.21,
  2
);


-- -----------------------------------------------------
-- Table Orders
-- -----------------------------------------------------

DROP TABLE IF EXISTS Orders;

CREATE TABLE IF NOT EXISTS Orders (
  orderID INT NOT NULL AUTO_INCREMENT,
  Employees_employeeID INT NOT NULL,
  Stores_storeID INT NOT NULL,
  Customers_customerID INT NOT NULL,
  orderTotal DECIMAL(10, 2) NOT NULL DEFAULT 0,
  PRIMARY KEY (orderID),
  INDEX fk_Orders_Employees_idx (Employees_employeeID ASC) VISIBLE,
  INDEX fk_Orders_Stores1_idx (Stores_storeID ASC) VISIBLE,
  INDEX fk_Orders_Customers1_idx (Customers_customerID ASC) VISIBLE,
  CONSTRAINT fk_Orders_Employees
    FOREIGN KEY (Employees_employeeID)
    REFERENCES Employees (employeeID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Orders_Stores1
    FOREIGN KEY (Stores_storeID)
    REFERENCES Stores (storeID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Orders_Customers1
    FOREIGN KEY (Customers_customerID)
    REFERENCES Customers (customerID)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

INSERT INTO Orders(
  Employees_employeeID,
  Stores_storeID,
  Customers_customerID,
  orderTotal
) VALUES (
  1,
  1,
  1,
  39.18
),
(
  2,
  2,
  2,
  109.72
),
(
  3,
  3,
  3,
  12.93
);


-- -----------------------------------------------------
-- Table Liquors
-- -----------------------------------------------------

DROP TABLE IF EXISTS Liquors;

CREATE TABLE IF NOT EXISTS Liquors (
  productID INT NOT NULL AUTO_INCREMENT,
  productName VARCHAR(100) NOT NULL,
  productSizeMl INT NOT NULL DEFAULT 0,
  productPrice DECIMAL(10,2) NULL,
  PRIMARY KEY (productID))
ENGINE = InnoDB;

INSERT INTO Liquors(
  productName,
  productSizeMl,
  productPrice
) VALUES (
  "100 Stories Gold Rush",
  750,
  19.99
),
(
  "1792 Small Batch",
  750,
  27.99
),
(
  "360 Vodka",
  1000,
  12.99
);

-- -----------------------------------------------------
-- Table LiquorsOrders
-- -----------------------------------------------------

DROP TABLE IF EXISTS LiquorsOrders;

CREATE TABLE IF NOT EXISTS LiquorsOrders (
  Liquors_productID INT NOT NULL,
  Orders_orderID INT NOT NULL,
  productQuantity INT NULL,
  PRIMARY KEY (Liquors_productID, Orders_orderID),
  INDEX fk_Orders_has_Liquors_Liquors1_idx (Liquors_productID ASC) VISIBLE,
  INDEX fk_LiquorsOrders_Orders1_idx (Orders_orderID ASC) VISIBLE,
  CONSTRAINT fk_Orders_has_Liquors_Liquors1
    FOREIGN KEY (Liquors_productID)
    REFERENCES Liquors (productID)
    ON DELETE CASCADE,
  CONSTRAINT fk_LiquorsOrders_Orders1
    FOREIGN KEY (Orders_orderID)
    REFERENCES Orders (orderID)
    ON DELETE CASCADE)
ENGINE = InnoDB;

INSERT INTO LiquorsOrders(
  Liquors_productID,
  Orders_orderID,
  productQuantity
) VALUES (
  1,
  1,
  2
),
(
  2,
  2,
  4
),
(
  3,
  3,
  1
);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;