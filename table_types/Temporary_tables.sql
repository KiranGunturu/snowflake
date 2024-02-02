USE DATABASE PDB;

// Create permanent table 

CREATE OR REPLACE TABLE PDB.public.customers (
   id int,
   first_name string,
  last_name string,
  email string,
  gender string,
  Job string,
  Phone string);


INSERT INTO PDB.public.customers
SELECT t1.* FROM OUR_FIRST_DB.public.customers t1



SELECT * FROM PDB.public.customers


// Create temporary table (with the same name)
CREATE OR REPLACE TEMPORARY TABLE PDB.public.customers (
   id int,
   first_name string,
  last_name string,
  email string,
  gender string,
  Job string,
  Phone string);


// Validate temporary table is the active table
SELECT * FROM PDB.public.customers;

// Create second temporary table (with a new name)
CREATE OR REPLACE TEMPORARY TABLE PDB.public.temp_table (
   id int,
   first_name string,
  last_name string,
  email string,
  gender string,
  Job string,
  Phone string);

// Insert data in the new table
INSERT INTO PDB.public.temp_table
SELECT * FROM PDB.public.customers

SELECT * FROM PDB.public.temp_table

SHOW TABLES;


