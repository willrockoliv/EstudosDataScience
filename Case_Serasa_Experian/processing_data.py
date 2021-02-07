from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F

def preprocessing(lines):
    words = lines.select(explode(split(lines.value, "t_end")).alias("word"))
    words = words.na.replace('', None)
    words = words.na.drop()
    # words = words.withColumn('word', F.regexp_replace('word', r'http\S+', ''))
    # words = words.withColumn('word', F.regexp_replace('word', '@\w+', ''))
    # words = words.withColumn('word', F.regexp_replace('word', '#', ''))
    # words = words.withColumn('word', F.regexp_replace('word', 'RT', ''))
    # words = words.withColumn('word', F.regexp_replace('word', ':', ''))
    return words

if __name__ == "__main__":
    spark = SparkSession.builder.getOrCreate()

    lines = spark.readStream.format("socket").option("host", "localhost").option("port", 5555).load()
    
#     print(type(lines))

    words = preprocessing(lines)
    # # text classification to define polarity and subjectivity
    # words = text_classification(words)

    words = words.repartition(1)
    query = words.writeStream.queryName("all_tweets")\
        .outputMode("append").format("parquet")\
        .option("path", "./parc")\
        .option("checkpointLocation", "./check")\
        .trigger(processingTime='60 seconds').start()
    query.awaitTermination()