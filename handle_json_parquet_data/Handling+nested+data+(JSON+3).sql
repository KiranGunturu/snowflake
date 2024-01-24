   // Handling nested data
   
SELECT RAW_FILE:job as job  FROM OUR_FIRST_DB.PUBLIC.JSON_RAW;


SELECT 
      RAW_FILE:job.salary::INT as salary
FROM OUR_FIRST_DB.PUBLIC.JSON_RAW;



SELECT 
    RAW_FILE:first_name::STRING as first_name,
    RAW_FILE:job.salary::INT as salary,
    RAW_FILE:job.title::STRING as title
FROM OUR_FIRST_DB.PUBLIC.JSON_RAW;


// Handling arreys

SELECT
    RAW_FILE:prev_company as prev_company
FROM OUR_FIRST_DB.PUBLIC.JSON_RAW;

SELECT
    RAW_FILE:prev_company[1]::STRING as prev_company
FROM OUR_FIRST_DB.PUBLIC.JSON_RAW;


SELECT
    ARRAY_SIZE(RAW_FILE:prev_company) as prev_company
FROM OUR_FIRST_DB.PUBLIC.JSON_RAW;




SELECT 
    RAW_FILE:id::int as id,  
    RAW_FILE:first_name::STRING as first_name,
    RAW_FILE:prev_company[0]::STRING as prev_company
FROM OUR_FIRST_DB.PUBLIC.JSON_RAW
UNION ALL 
SELECT 
    RAW_FILE:id::int as id,  
    RAW_FILE:first_name::STRING as first_name,
    RAW_FILE:prev_company[1]::STRING as prev_company
FROM OUR_FIRST_DB.PUBLIC.JSON_RAW
ORDER BY id

