from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.dataframe import DataFrame
from datetime import datetime, timedelta
import time

class DataWarehouse():
    def read_layer1(self, table_name:str, partitions:dict)->DataFrame:
        layer = 1
        path = f"./layer{layer}/{table_name}/"
        tweets = spark.read.parquet(path)
        for part, value in partitions.items():
            tweets = tweets.filter(F.col(part) == value)
        return tweets

    def write_layer2(self, table_name:str, table:DataFrame, partitions:list=[]):
        path = f"./layer2/{table_name}/"
        try:
            table\
                .write\
                .partitionBy(*partitions)\
                .format("parquet")\
                .mode("append")\
                .save(path)
        except BaseException as e:
            print(f"Error saving table: {table_name}" + str(e))

    def fact_tweet(self, tweets:DataFrame)->DataFrame:
        assert type(tweets) is DataFrame
        fact_tweet = (
            tweets
            .withColumn(
                "created_at",
                F.from_utc_timestamp(
                    F.to_timestamp(
                        F.regexp_replace(
                            F.regexp_replace("created_at", "^[A-Za-z]{3} ", ""),
                            "\+0000 ", ""),
                        "MMM dd HH:mm:ss yyyy"
                    ),
                    "GMT-3"
                )
            )
            .withColumn(
                "hashtags", 
                F.when(
                    F.col("hashtags") != '',
                    F.regexp_replace("hashtags", ",\s$", "")
                )
                .otherwise(None)
            )
            .withColumn("created_at_partition_year", F.date_format("created_at", "yyyy"))
            .withColumn("created_at_partition_month", F.date_format("created_at", "MM"))
            .withColumn("created_at_partition_day", F.date_format("created_at", "dd"))
            .withColumn("created_at_partition_hour", F.date_format("created_at", "HH"))
            .select(
                "tweet_id",    
                "created_at",
                "text",
                "hashtags",
                F.col("retweet_count").cast(IntegerType()),
                F.col("possibly_sensitive").cast(BooleanType()),
                "lang",   
                "user_id",
                "created_at_partition_year",
                "created_at_partition_month",
                "created_at_partition_day",
                "created_at_partition_hour",
            )
        )
        return fact_tweet

    def dim_user(self, tweets:DataFrame)->DataFrame:
        dim_user = (
            tweets
            .withColumn(
                "user_created_at",
                F.from_utc_timestamp(
                    F.to_timestamp(
                        F.regexp_replace(
                            F.regexp_replace("user_created_at", "^[A-Za-z]{3} ", ""),
                            "\+0000 ", ""),
                        "MMM dd HH:mm:ss yyyy"
                    ),
                    "GMT-3"
                )
            )
            .select(
                "user_id",
                "user_name",
                "user_description",
                F.col("user_verification").cast(BooleanType()),
                F.col("user_followers_count").cast(IntegerType()),
                F.col("user_friends_count").cast(IntegerType()),
                "user_created_at",
                "user_location",
            )
        )
        return dim_user
        
if __name__ == "__main__":
    sc = SparkContext.getOrCreate()
    spark = SparkSession.builder.getOrCreate()
    sqlContext = SQLContext(sc)
    dw = DataWarehouse()
    persist_time=60*60

    start = time.time()
    while True:    
        print("Timer:", time.time() - start)
        if (time.time() - start) > persist_time:
            today = datetime.now() - timedelta(hours=1)
            partitions = {
                "etl_load_partition_year":today.year,
                "etl_load_partition_month":today.month if today.month > 10 else "0"+str(today.month),
                "etl_load_partition_day":today.day if today.day > 10 else "0"+str(today.day),
                "etl_load_partition_hour":today.hour if today.hour > 10 else "0"+str(today.hour)
            }

            print("loading data of past hour...")
            print("partitions:", partitions)
            tweets = dw.read_layer1(table_name="tweets", partitions=partitions)
            print("load:", tweets.count())
            
            print("saving fact_tweet...")
            fact_tweet = dw.fact_tweet(tweets)
            dw.write_layer2(table_name="fact_tweet", table=fact_tweet, partitions=["created_at_partition_year",
                                                                                "created_at_partition_month",
                                                                                "created_at_partition_day",
                                                                                "created_at_partition_hour",])
            
            print("saving dim_user...")
            dim_user = dw.dim_user(tweets)
            dw.write_layer2(table_name="dim_user", table=dim_user)

            start = time.time()