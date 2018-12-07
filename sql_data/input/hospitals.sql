-- Data set: https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings (22 Dec 2016)

-- DROP DATABASE hospital_pricing;

-- CREATE DATABASE hospital_pricing;
-- USE hospital_pricing;
--
-- 1.0 Setup. Delete tables after every build iteration.
--
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS city, hospital, temp_hospital;
SET FOREIGN_KEY_CHECKS=1;

--
-- 2.0 ENTITIES
-- Serve as lookup tables
--

-- Provider ID,Hospital Name,Address,City,State,ZIP Code,Hospital Type,Hospital Ownership,
-- Hospital overall rating,Mortality national comparison,Safety of care national comparison,
-- Readmission national comparison,Effectiveness of care national comparison

--
-- 2.1 temp_hospital table
--
CREATE TABLE IF NOT EXISTS temp_hospital (
  hospital_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  hospital_provider_identifier CHAR(6) NOT NULL UNIQUE,
  hospital_name VARCHAR(255) NOT NULL,
  address VARCHAR(255) NULL,
  city_name VARCHAR(255) NULL,
  zip_code CHAR(10) NULL,
  PRIMARY KEY (hospital_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/output/hospital_info_trimmed.csv' 
INTO TABLE temp_hospital
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (hospital_provider_identifier, hospital_name,
  address, city_name, zip_code, @dummy, @dummy,
  @dummy, @dummy, @dummy, @dummy, @dummy, @dummy
  );

-- city table

CREATE TABLE IF NOT EXISTS city (
  city_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  city_name VARCHAR(255) NOT NULL,
  PRIMARY KEY (city_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/output/hosp_city.csv'
INTO TABLE city
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (city_name);

-- 2.3 hospital table
 
CREATE TABLE IF NOT EXISTS hospital (
  hospital_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  hospital_provider_identifier CHAR(6) NOT NULL UNIQUE,
  hospital_name VARCHAR(255) NOT NULL,
  address VARCHAR(255) NOT NULL,
  city_id INTEGER NOT NULL,
  zip_code CHAR(10) NOT NULL,
  PRIMARY KEY (hospital_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO hospital (
      hospital_provider_identifier,
      hospital_name,
      address,
      city_id,
      zip_code
)
SELECT th.hospital_provider_identifier,
       th.hospital_name, th.address, cit.city_id, th.zip_code
  FROM temp_hospital th
       LEFT JOIN city cit
              ON TRIM(th.city_name) = TRIM(cit.city_name)
ORDER BY th.hospital_provider_identifier;


-- 3.0 ENTITIES
--
-- DRG Definition, Provider Id, Provider Name,  Provider Street Address,  Provider City,  Provider State,  Provider Zip Code,
-- Hospital Referral Region Description, Total Discharges , Average Covered Charges , Average Total Payments ,Average Medicare Payments
-- 12 columns total

-- 3.1 temp_pricing
-- DROP TABLE temp_pricing;
CREATE TABLE IF NOT EXISTS temp_pricing (
  pricing_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  drg_definition CHAR(250) NOT NULL,                   -- Put drg_definition before provider id because thats the order in the csv
  pricing_provider_identifier CHAR(6) NOT NULL,
  zip_code CHAR(10) NULL,
  price DECIMAL(10,2) NULL,
  PRIMARY KEY (pricing_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/output/pricing_trimmed.csv' 
INTO TABLE temp_pricing
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (drg_definition, pricing_provider_identifier, @dummy, @dummy, @dummy, @dummy, zip_code, 
  @dummy, @dummy, price, @dummy, @dummy
  );


-- 3.2 charge_amount  this table is similar to the city table that has 1 entity that comes from its own csv
-- DROP TABLE charge_amount;
CREATE TABLE IF NOT EXISTS charge_amount (
  charge_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  charge DECIMAL(10,2) NOT NULL UNIQUE,
  PRIMARY KEY (charge_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/output/price.csv'
INTO TABLE charge_amount
  CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
  LINES TERMINATED BY '\n'
  IGNORE 1 LINES
  (charge);


-- 3.3 pricing table
-- DROP TABLE pricing;
CREATE TABLE IF NOT EXISTS pricing (
  price_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
  pricing_provider_identifier CHAR(6) NOT NULL UNIQUE,
  charge_id INTEGER(10) NOT NULL,
  drg_code VARCHAR(3) DEFAULT '313',
  drg_definition CHAR(20) DEFAULT 'Chest Pain',
  zip_code CHAR(10) NOT NULL,
  PRIMARY KEY (price_id)
)
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO pricing (
      pricing_provider_identifier,
      charge_id,
      zip_code
)
SELECT tp.pricing_provider_identifier,
       ch.charge_id, tp.zip_code
  FROM temp_pricing tp
       LEFT JOIN charge_amount ch
              ON TRIM(tp.price) = TRIM(ch.charge)
  WHERE tp.drg_definition = '313 - CHEST PAIN'
ORDER BY tp.pricing_provider_identifier;
