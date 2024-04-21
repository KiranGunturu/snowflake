import os
import snowflake.snowpark.functions
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col


conn_params = {
    "account": "ekcgrcl-vrb44367",
    "user": "kiran419pav",
    "password": "P@ssw0rd345",
    "role": "ACCOUNTADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SNOWFLAKE_SAMPLE_DATA",
    "schema": "TPCH_SF1"
}

test_session = Session.builder.configs(conn_params).create()

print(test_session.sql("select current_warehouse(), current_database(), current_schema()").collect())

sesssion = Session.bui