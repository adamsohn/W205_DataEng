#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
#Importing Libraries
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType

#Defining schema. Fixed User-Agent to User_Agent for universal compatability.
def guild_sword_nap_event_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User_Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- metadata_characteristic: string (nullable = true)
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User_Agent", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("metadata_characteristic", StringType(), True),
    ])


@udf('boolean')
def is_guild_sword_nap(event_as_json):
    """
    Boolean function returns True for event_type in ['joined_guild', 'took_nap', 'purchd_sword']. Returns False for 
    others ('consume_fermented_beverage'). No other event_types expected in Kafka per game_api_sohn.py.
    """
    event = json.loads(event_as_json)
    if event['event_type'] == 'joined_guild' or event['event_type'] == 'purchd_sword' or event['event_type'] == 'took_nap':
        return True
    else:
        return False
	
def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .enableHiveSupport() \ #Without this setting, the file will throw exception.
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \ #Kafka topic 'events' previously created.
        .load()

#Filtering ['joined_guild', 'purchd_sword', 'took_nap'] events.
    filtered_events = raw_events \
        .filter(is_guild_sword_nap(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          guild_sword_nap_event_schema()).alias('json')) \
        .select('timestamp', 'json.*') #Matches Hive schema.

# Writing any new events hdfs in 20 second intervals. Generous for low volume to ensure no falling behind.
    sink = filtered_events \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_filtered_events") \
        .option("path", "/tmp/filterd_evnts") \
        .trigger(processingTime="20 seconds") \ 
        .start()

# Registering filtered_events_tbl in Hive according to contents in hdfs /tmp/filterd_evnts. 
# Schema matches filtered_events above.
# Important to be after sink statement to avoid waiting an additional cycle for loading to filtered_event_tbl.
    sql_string = "drop table if exists default.filtered_events_tbl"
    spark.sql(sql_string)
    sql_string = """
    create external table if not exists default.filtered_events_tbl (
        timestamp string,
        Accept string,
        Host string,
        User_Agent string,
        event_type string,
        metadata_characteristic string
    )
    stored as parquet
    location '/tmp/filterd_evnts'
    tblproperties ("parquet.compress"="SNAPPY")
    """
    spark.sql(sql_string)        

# Streaming script runs until terminated
    sink.awaitTermination()

# Kick-off command for main()
if __name__ == "__main__":
    main()