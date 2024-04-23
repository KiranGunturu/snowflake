import os
import snowflake.snowpark.functions
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from snowflake.snowpark.types import IntegerType, StringType, StructField, StructType, DateType

# define connection parameters
conn_params = {
    "account": "ekcgrcl-vrb44367",
    "user": "kiran419pav",
    "password": "P@ssw0rd345",
    "role": "ACCOUNTADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SNOWFLAKE_SAMPLE_DATA",
    "schema": "TPCH_SF1"
}

# session object
session = Session.builder.configs(conn_params).create()
print(session.sql("select current_warehouse(), current_database(), current_schema()").collect())
session.sql("USE WAREHOUSE COMPUTE_WH").collect()

# create dataframe using dictionary
customer_dict_df = session.create_dataframe({100, 110, 120, 130}, schema=["customer_id"]) # TypeError: create_dataframe() function only accepts data as a list, tuple or a pandas DataFrame.
customer_dict_df.show()

# create dataframe using list
customer_list_df = session.create_dataframe([100, 110, 120, 130], schema=["customer_id"])
customer_list_df.show()
-----------------
|"CUSTOMER_ID"  |
-----------------
|100            |
|110            |
|120            |
|130            |
-----------------

# query executed by snowflake for the above dataframe operation
SELECT "CUSTOMER_ID" FROM ( SELECT $1 AS "CUSTOMER_ID" FROM  VALUES (100 :: INT), (110 :: INT), (120 :: INT), (130 :: INT)) LIMIT 10


# json
json_df = session.create_dataframe(
    [
        [100, 201, 301, {"fist_name": "Kiran"}],
        [101, 202, 302, None],
        [102, 203, 303, {"last_name": "Gunturu"}],
        [103, 204, 304, {"gender":"male"}]

    ], schema=["customer_id", "product_id", "date_id", "customer_info"]
)
# snowflake generated sql
SELECT "CUSTOMER_ID", "PRODUCT_ID", "DATE_ID", to_object(parse_json("CUSTOMER_INFO")) AS "CUSTOMER_INFO" FROM ( SELECT $1 AS "CUSTOMER_ID", $2 AS "PRODUCT_ID", $3 AS "DATE_ID", $4 AS "CUSTOMER_INFO" FROM  
VALUES (100 :: INT, 201 :: INT, 301 :: INT, '{"fist_name": "Kiran"}' :: STRING), 
(101 :: INT, 202 :: INT, 302 :: INT, NULL :: STRING), (102 :: INT, 203 :: INT, 303 :: INT, '{"last_name": "Gunturu"}' :: STRING), 
(103 :: INT, 204 :: INT, 304 :: INT, '{"gender": "male"}' :: STRING)) LIMIT 10

json_df.show()




