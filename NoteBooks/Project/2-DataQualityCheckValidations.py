# Databricks notebook source
filePath = "/mnt/sasandeepadls/raw"

# COMMAND ----------

from pyspark.sql.functions import regexp_replace,col

# COMMAND ----------

df = spark.read.option("header", True).csv(filePath)


# COMMAND ----------

# MAGIC %md
# MAGIC ####Getting partition size

# COMMAND ----------

records_per_partition = df.rdd.glom().map(len).collect()

# Show the number of records per partition
print("Records per partition:", records_per_partition)

# COMMAND ----------

# MAGIC %md
# MAGIC ####Getting datatypes of each column
# MAGIC

# COMMAND ----------

column_data_types = df.dtypes

# Show column names and data types
for column, data_type in column_data_types:
    print(f"Column: {column}, Data Type: {data_type}")

# COMMAND ----------

# MAGIC %md
# MAGIC ####Counting nulls in each column

# COMMAND ----------

def check_nulls(df):
    null_counts = {col: df.filter(df[col].isNull()).count() for col in df.columns}
    return null_counts

null_counts = check_nulls(df)
print("Null counts per column:", null_counts)

# COMMAND ----------

# MAGIC %md
# MAGIC ####Replacing values in columns as per requirement

# COMMAND ----------

df = df.withColumn("MODEL", 
                   regexp_replace(
                     regexp_replace(
                       regexp_replace(
                         col("MODEL"), "F150", "F-150"), "Camery", "Camry"),"X5","X-5"))
df.show(100)


# COMMAND ----------

# MAGIC %md

# COMMAND ----------

# MAGIC %md
# MAGIC ####Aligning  year column as per requirement

# COMMAND ----------

column_data_types = df.dtypes

# Show column names and data types
for column, data_type in column_data_types:
    print(f"Column: {column}, Data Type: {data_type}")

