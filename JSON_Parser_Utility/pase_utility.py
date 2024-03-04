import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

# create spark session
spark = SparkSession \
        .builder \
        .appName("json_parser") \
        .getOrCreate()

# read JSON data

df=spark \
    .read \
    .json("/workspaces/snowflake/JSON_Parser_Utility/HR_data.json")

def compute_complex_fields(df):
    complex_fields = {}
    #isinstance() is a built-in Python function used to check if an object is an instance of a specified class or of a class derived from it.
    for field in df.schema.fields:
        if isinstance(field.dataType, ArrayType) or isinstance(field.dataType, StructType):
            complex_fields[field.name] = field.dataType
    return complex_fields

def flatten_json(df):
    complex_fields = compute_complex_fields(df)

    while len(complex_fields)!=0:
        col_name=list(complex_fields.keys())[0]
        print ("Processing :"+col_name+" Type : "+str(type(complex_fields[col_name])))

        if (type(complex_fields[col_name]) == StructType):
            expanded = [col(col_name+'.'+k).alias(col_name+'_'+k) for k in [ n.name for n in  complex_fields[col_name]]]
            df=df.select("*", *expanded).drop(col_name)
        
        elif (type(complex_fields[col_name]) == ArrayType):
            #df=df.withColumn(col_name,col(col_name)[0])
            df=df.withColumn(col_name,explode_outer(col_name))

        complex_fields = compute_complex_fields(df)

    return df


df = flatten_json(df)
#df.show(5, truncate=False)
df= df.filter("id=2").show()
