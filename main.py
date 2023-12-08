"""
Main code
"""
from databricks.connect import DatabricksSession
spark = DatabricksSession.builder.getOrCreate()

df = spark.read.table("application_data")
df.show(5)
# def add(a, b):
#     return a + b


# if __name__ == "__main__":
#     result = add(2, 4)
#     print(f"The result of adding 2 and 4 is {result}")