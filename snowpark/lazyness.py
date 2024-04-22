import os
import snowflake.snowpark.functions
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

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

customer_df =  session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER")
filter_customers = customer_df.filter(col("C_MKTSEGMENT") == 'HOUSEHOLD')
select_customers = filter_customers.select(col("C_NAME"), col("C_ADDRESS"))
select_customers.show()
print(select_customers.count())



