
// Define pipe
CREATE OR REPLACE pipe MANAGE_DB.pipes.employee_pipe
auto_ingest = TRUE
AS
COPY INTO OUR_FIRST_DB.PUBLIC.employees
FROM @MANAGE_DB.external_stages.csv_folder  ;

// Describe pipe
DESC pipe employee_pipe;
    
SELECT * FROM OUR_FIRST_DB.PUBLIC.employees ;