-- Show how different U.S. Hospitals charge the Center for Medicare and Medicaid Services (CMS) for 
-- a Diagnosis Related Group (DRG) related to Chest Pain. Compare the prices to the national averages for quality and safety.
-- Source: https://www.kaggle.com/center-for-medicare-and-medicaid/hospital-ratings
-- Source: https://data.cms.gov/Medicare-Inpatient/Inpatient-Prospective-Payment-System-IPPS-Provider/97k6-zzx3 
-- Source: https://www.kaggle.com/cms/cms-hpsa-low-income-zip-code-database 

--
-- Create database
--
CREATE DATABASE IF NOT EXISTS hospital_pricing;
USE hospital_pricing;

--
-- Drop tables
-- turn off FK checks temporarily to eliminate drop order issues
--

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS hospital, city, state, zip_code, zip_code_designation,
  hospital_ownership, hospital_drg, diagnosis_related_group, drg_charge_amount, hospital_quality_summary,
  hospital_quality_score, hospital_safety_rating, hospital_readmission_rate, temp_zip_code, temp_hospital;
SET FOREIGN_KEY_CHECKS=1;


-- DROP TEMPORARY TABLE IF EXISTS
--  temp_zip_code, temp_hospital;

--
-- City
--

CREATE TABLE IF NOT EXISTS city
  (
    city_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    city_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (city_id)
      )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


-- Load data from external file. 'C:\ProgramData\MySQL\MySQL Server 8.0\Uploads\output\hosp_city.csv'
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/output/hosp_city.csv'
INTO TABLE city
	CHARACTER SET utf8mb4
    FIELDS TERMINATED BY '\t'
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    -- LINES TERMINATED BY '\r\n'
    -- IGNORE 1 LINES
    (city_name);



CREATE TABLE IF NOT EXISTS state
  (
    state_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    state_abbreviation VARCHAR(3) NOT NULL UNIQUE,
    PRIMARY KEY (state_id)
      )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


-- Load data from external file.
-- Check for blank entries and set to NULL.
LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/output/hosp_state.csv'
INTO TABLE state
	CHARACTER SET utf8mb4
    FIELDS TERMINATED BY '\t'
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    -- LINES TERMINATED BY '\n'
    LINES TERMINATED BY '\r\n'
    -- IGNORE 1 LINES
    (state_abbreviation);





CREATE TABLE IF NOT EXISTS hospital_ownership
  (
    hospital_ownership_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    hospital_ownership_description VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (hospital_ownership_id)
      )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


-- Load data from external file. Check for blank entries and set to NULL.
-- INSERT IGNORE INTO zip_code_designation (zip_code_designation) VALUES

INSERT IGNORE INTO  hospital_ownership (hospital_ownership_description) VALUES
("Government - Federal"),
("Government - Hospital District or Authority"),
("Government - Local"),
("Government - State"),
("Physician"),
("Proprietary"),
("Tribal"),
("Voluntary non-profit - Church"),
("Voluntary non-profit - Other"),
("Voluntary non-profit - Private");



CREATE TABLE IF NOT EXISTS zip_code_designation
  (
    zip_code_designation_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    zip_code_designation VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (zip_code_designation_id)
      )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT IGNORE INTO zip_code_designation (zip_code_designation) VALUES
  ('HSPA'),
  ('Low Income Area'),
  ('Low Income Area/HSPA');




CREATE TABLE IF NOT EXISTS drg_charge_amount
  (
    drg_charge_amount_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    charge_amount VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (drg_charge_amount_id)
      )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/output/drg_charge.csv'
INTO TABLE drg_charge_amount
	CHARACTER SET utf8mb4
    FIELDS TERMINATED BY '\t'
    -- FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    -- LINES TERMINATED BY '\r\n'
    -- IGNORE 1 LINES
    (charge_amount);


 

CREATE TABLE IF NOT EXISTS hospital_quality_score
  (
    hospital_quality_score_id INTEGER UNIQUE NOT NULL AUTO_INCREMENT,
    hospital_quality_score VARCHAR(50),
    PRIMARY KEY (hospital_quality_score_id)
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;
    
INSERT INTO hospital_quality_score (hospital_quality_score) VALUES
  ('0'),
  ('1'),
  ('2'),
  ('3'),
  ('4'),
  ('5'),
  ('NOT AVAILABLE');
  

CREATE TABLE IF NOT EXISTS hospital_readmission_rate
  (
    hospital_readmission_rate_id INTEGER UNIQUE NOT NULL AUTO_INCREMENT,
    hospital_readmission_rate VARCHAR(50),
    PRIMARY KEY (hospital_readmission_rate_id)
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

INSERT INTO hospital_readmission_rate (hospital_readmission_rate) VALUES
	('Above the national average'),
	('Below the national average'),
	('Not Available'),
	('Same as the national average');
    

CREATE TABLE IF NOT EXISTS hospital_safety_rating
  (
    hospital_safety_rating_id INTEGER UNIQUE NOT NULL AUTO_INCREMENT,
    hospital_safety_rating VARCHAR(50),
    PRIMARY KEY (hospital_safety_rating_id)
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;
    
INSERT INTO hospital_safety_rating (hospital_safety_rating) VALUES
	('Above the national average'),
	('Below the national average'),
	('Not Available'),
	('Same as the national average');


CREATE TABLE IF NOT EXISTS zip_code
  (
    zip_code_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    zip_code VARCHAR(5) NOT NULL UNIQUE,
    city VARCHAR(30),
    state VARCHAR(3),
    zip_code_designation VARCHAR(35), 
    PRIMARY KEY (zip_code_id)
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/input/zip_code_desig_cleaned.csv'
INTO TABLE zip_code
  CHARACTER SET utf8mb4
    -- FIELDS TERMINATED BY '\t'
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    -- LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (zip_code, city, state, zip_code_designation)



-- CREATE TABLE temp_zip_code (
--     zip_code_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
--     zip_code VARCHAR(5) NOT NULL UNIQUE,
--     city VARCHAR(100) NULL,
--     state VARCHAR(100) NULL,
--     zip_code_designation VARCHAR(100) NULL, 
--     PRIMARY KEY (zip_code_id)
--     )

-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

-- Load data from external file.
-- Check for blank entries and set to NULL.
-- LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/input/zip_code_desig_cleaned.csv'
-- INTO TABLE temp_zip_code
--   CHARACTER SET utf8mb4
--     FIELDS TERMINATED BY '\t'
--     -- FIELDS TERMINATED BY ','
--     ENCLOSED BY '"'
--     LINES TERMINATED BY '\n'
--     -- LINES TERMINATED BY '\r\n'
--     IGNORE 1 LINES
--     (zip_code, city, state, zip_code_designation)

--     SET zip_code = IF(zip_code = '', NULL, TRIM(zip_code)),
--     city = IF(city = '', NULL, TRIM(city)),
--     state = IF(state = '', NULL, TRIM(state)),
--     zip_code_designation = IF(zip_code_designation = '', NULL, TRIM(zip_code_designation));


-- CREATE TABLE IF NOT EXISTS zip_code
--   (
--     zip_code_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
--     zip_code VARCHAR(5) NULL UNIQUE,
--     city VARCHAR(5) NULL,
--     state VARCHAR(3) NULL,
--     zip_code_designation_id INTEGER, 
--     PRIMARY KEY (zip_code_id),
--     FOREIGN KEY (zip_code_designation_id) REFERENCES zip_code_designation(zip_code_designation_id) ON DELETE RESTRICT ON UPDATE CASCADE
--       )
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

-- INSERT IGNORE INTO zip_code(
--   zip_code,
--   city,
--   state,
--   zip_code_designation_id
--   )
-- SELECT DISTINCT(tz.zip_code), zcd.zip_code_designation_id
--   FROM temp_zip_code AS tz
--     LEFT JOIN zip_code_designation AS zcd
--     ON TRIM(tz.zip_code_designation) = TRIM(zcd.zip_code_designation)
--     WHERE tz.zip_code IS NOT NULL AND tz.zip_code != ''
--     ORDER BY tz.zip_code;




-- -- ----------------------------------------------------------------------------------------------------------------------------------
-- -- TABLES WITH FOREIGN KEYS
-- -- hospital
-- --
CREATE TABLE IF NOT EXISTS temp_hospital
  (
    hospital_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    provider_id INTEGER NULL,
    hospital_name VARCHAR(100) NULL,	
    street_address VARCHAR(250) NULL,
    city VARCHAR(100) NULL,
    state VARCHAR(3) NULL,
    zip_code VARCHAR(5) NULL,   
    hospital_type VARCHAR(100) NULL, 
    hospital_ownership VARCHAR(100) NULL,
    hospital_overall_rating VARCHAR(100) NULL,
    mortality_rating VARCHAR(100) NULL,
    safety_rating VARCHAR(100) NULL,
    readmission_rate VARCHAR(100) NULL,
    effectiveness_score VARCHAR(100) NULL,
    PRIMARY KEY (hospital_id)
      )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;

LOAD DATA LOCAL INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/input/hospital_info.txt'    
INTO TABLE temp_hospital
	CHARACTER SET utf8mb4
    FIELDS TERMINATED BY '\t'
    ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES
    (provider_id, hospital_name, street_address, city, state, zip_code, hospital_type, hospital_ownership, hospital_overall_rating,
      mortality_rating, safety_rating, readmission_rate, effectiveness_score)
    SET provider_id = IF(provider_id = '', NULL, TRIM(provider_id)),
    hospital_name = IF(hospital_name = '', NULL, TRIM(hospital_name)),
    street_address = IF(street_address = '', NULL, TRIM(street_address)),
    city = IF(city = '', NULL, TRIM(city)),
    state = IF(state = '', NULL, TRIM(state)),
    zip_code = IF(zip_code = '', NULL, TRIM(zip_code)),
    hospital_type = IF(hospital_type = '', NULL, TRIM(hospital_type)),
    hospital_ownership = IF(hospital_ownership = '', NULL, TRIM(hospital_ownership)),
    hospital_overall_rating = IF(hospital_overall_rating = '', NULL, TRIM(hospital_overall_rating)),
    mortality_rating = IF(mortality_rating = '', NULL, TRIM(mortality_rating)),
    safety_rating = IF(safety_rating = '', NULL, TRIM(safety_rating)),
    readmission_rate = IF(readmission_rate = '', NULL, TRIM(readmission_rate)),
    effectiveness_score = IF(effectiveness_score = '', NULL, TRIM(effectiveness_score));
    
    
CREATE TABLE IF NOT EXISTS hospital
  (
    hospital_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
    hospital_name VARCHAR(100) NOT NULL UNIQUE,	
    street_address VARCHAR(250) NOT NULL UNIQUE,
    city_id INTEGER NOT NULL,
    state_id INTEGER NOT NULL,
    hospital_ownership_id INTEGER,
    zip_code_id INTEGER NOT NULL,
    zip_code_designation VARCHAR(50) NULL,
    PRIMARY KEY (hospital_id),
    FOREIGN KEY (city_id) REFERENCES city(city_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (state_id) REFERENCES state(state_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (hospital_ownership_id) REFERENCES hospital_ownership(hospital_ownership_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (zip_code_id) REFERENCES zip_code(zip_code_id) ON DELETE RESTRICT ON UPDATE CASCADE
    )
ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;


INSERT IGNORE INTO hospital
(
  hospital_name,
  street_address,
  city_id,
  state_id,
  hospital_ownership_id,
  zip_code_id,
  zip_code_designation
)
SELECT th.hospital_name, th.street_address, c.city_id, s.state_id, ho.hospital_ownership_id, 
  zc.zip_code_id, zc.zip_code_designation
  FROM temp_hospital AS th
    LEFT JOIN city AS c 
    ON TRIM(th.city) = TRIM(c.city_name)
    LEFT JOIN state AS s
    ON TRIM(th.state) = TRIM(s.state_abbreviation)
    LEFT JOIN hospital_ownership AS ho
    ON TRIM(th.hospital_ownership) = TRIM(ho.hospital_ownership_description)
    LEFT JOIN zip_code AS zc
    ON TRIM(zc.zip_code) = TRIM(th.zip_code)
  WHERE th.hospital_name IS NOT NULL and th.hospital_name != ''
  ORDER BY th.hospital_name;



    
    

-- CREATE TABLE IF NOT EXISTS diagnosis_related_group
--   (
--     diagnosis_related_group_id INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
--     drg_code VARCHAR(50) NOT NULL UNIQUE,
--     drg_description VARCHAR(50) NOT NULL UNIQUE,
--     drg_charge_amount_id INTEGER,
--     PRIMARY KEY (diagnosis_related_group_id),
-- 	FOREIGN KEY (drg_charge_amount_id) REFERENCES drg_charge_amount(drg_charge_amount_id) ON DELETE RESTRICT ON UPDATE CASCADE
--       )
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

-- INSERT IGNORE INTO diagnosis_related_group (drg_code) VALUES
--   ('313');
-- INSERT IGNORE INTO diagnosis_related_group (drg_description) VALUES
--   ('CHEST PAIN');



    
-- CREATE TABLE IF NOT EXISTS hospital_drg
--   (
-- 	hospital_id INTEGER NOT NULL,
--     diagnosis_related_group_id INTEGER NOT NULL,
-- 	FOREIGN KEY (hospital_id) REFERENCES hospital(hospital_id) ON DELETE RESTRICT ON UPDATE CASCADE,
-- 	FOREIGN KEY (diagnosis_related_group_id) REFERENCES diagnosis_related_group(diagnosis_related_group_id) ON DELETE RESTRICT ON UPDATE CASCADE
-- 	)
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;



-- CREATE TABLE IF NOT EXISTS hospital_quality_summary
--   (
-- 	hospital_id INTEGER NOT NULL,
--     hospital_quality_score_id INTEGER NOT NULL,
--     hospital_readmission_rate_id INTEGER NOT NULL,
--     hospital_safety_rating_id INTEGER NOT NULL,
-- 	FOREIGN KEY (hospital_id) REFERENCES hospital(hospital_id) ON DELETE RESTRICT ON UPDATE CASCADE,
-- 	FOREIGN KEY (hospital_quality_score_id) REFERENCES hospital_quality_score(hospital_quality_score_id) ON DELETE RESTRICT ON UPDATE CASCADE,
-- 	FOREIGN KEY (hospital_readmission_rate_id) REFERENCES hospital_readmission_rate(hospital_readmission_rate_id) ON DELETE RESTRICT ON UPDATE CASCADE,
-- 	FOREIGN KEY (hospital_safety_rating_id) REFERENCES hospital_safety_rating(hospital_safety_rating_id) ON DELETE RESTRICT ON UPDATE CASCADE
-- 	)
-- ENGINE=InnoDB
-- CHARACTER SET utf8mb4
-- COLLATE utf8mb4_0900_ai_ci;

