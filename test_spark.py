from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SimpleTest").getOrCreate()

data = [(1, "Alice"), (2, "Bob"), (3, "Cathy")]
df = spark.createDataFrame(data, ["ID", "Name"])
df.show()
