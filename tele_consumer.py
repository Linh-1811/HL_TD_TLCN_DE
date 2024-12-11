from kafka import KafkaConsumer
from llm import generate_response
from pyspark import SparkConf, SparkContext
from pyspark.sql.functions import from_json, get_json_object, col, udf
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, LongType
from pyspark.sql import SparkSession
import sys

from telethon import TelegramClient

from pyspark.sql import functions as F
from time import sleep
import logging

from LSTM.lstm_test import predict_sentiment
from LDA.lda_test import get_topic
from nrc_lexicon import fetch_nrc, preprocess
from responses import fetch_response

import os
import sys

os.environ['PYSPARK_PYTHON'] =  "python"
os.environ['PYSPARK_DRIVER_PYTHON'] = "python"
from dotenv import load_dotenv

import asyncio


load_dotenv()

# Telegram credentials
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
phone_number = os.environ.get('PHONE_NUMBER')
bot_token = os.environ.get('BOT_TOKEN')
group_chat_id = int(os.environ.get('GROUP_CHAT_ID'))
sender = int(os.environ.get('SENDER'))
keyword = os.environ.get('KEY_WORD')
llm = os.environ.get('USE_LLM')

async def send_telegram_message(client, chat_id, text, reply_to):
    # print("CHECKPONT: ", chat_id, text, reply_to )
    
    await client.send_message(
        chat_id,
        text,
        reply_to=reply_to
    )
    print(f"Replied to message ID {reply_to} in chat {chat_id}")
    await asyncio.sleep(2)

def reply(row):
    print("CHECKPOINT ROW: ", row)
    # Initialize the Telegram client outside the reply function
    #client = TelegramClient('consumer_session2', api_id, api_hash).start(bot_token=bot_token)
    client = TelegramClient('consumer_session', api_id, api_hash).start(phone=phone_number)
    if row.sender_id != sender and keyword in row.text:
        # Fetching tweet response based on Sentiment, Topic and NRC_Sentiment
        text = fetch_response(row.text, row.Sentiment, row.Topic, row.NRC_Sentiment)
        # Run the async function in the event loop
        with client:
            client.loop.run_until_complete(
                send_telegram_message(client, row.chat_id, text, row.id)
            )
    client.disconnect()

def llm_reply(row):
    print("Response with GEMINI")
    client = TelegramClient('consumer_session', api_id, api_hash).start(phone=phone_number)
    #client = TelegramClient('consumer_session2', api_id, api_hash).start(bot_token=bot_token)
    if row.sender_id != sender:
        # Fetching tweet response based on Sentiment, Topic and NRC_Sentiment
        text = generate_response(row.text)
        # Run the async function in the event loop
        with client:
            client.loop.run_until_complete(
                send_telegram_message(client, row.chat_id, text, row.id)
            )
    client.disconnect()
def main(topic):
    logging.error("START OF MAIN!!!!!!!!!!!!!!")

    # Initializing kafka readStream
    messages = spark.readStream.format('kafka') \
        .option('kafka.bootstrap.servers', 'localhost:9092') \
        .option('subscribe', topic).load()

    values = messages.selectExpr("CAST(value AS STRING)")
    print("Check values: ", messages)
    schema = StructType(
            [
                    StructField("id", IntegerType()),
                    StructField("chat_id", LongType()),
                    StructField("sender_id", LongType()),
                    StructField("text", StringType()),
                    StructField("timestamp", StringType())
            ]
    )

    # Fetching required data from telegram
    raw_df = values.withColumn("value", from_json("value", schema))\
        .select(col('value.*'))

    new_df = raw_df.select(raw_df.id, raw_df.text, raw_df.chat_id, raw_df.sender_id)
    # Passing kafka data to get_api function
    stream0 = new_df.writeStream.format('console').start()
    if llm == "True":
        stream = new_df.writeStream.format('console').foreach(
            llm_reply
        ).start()
    else:
        # Creating udf functions for predicting sentiment, fetching topic and nrc emotion
        predict_sentiment_udf = udf(predict_sentiment,StringType())
        get_topic_udf = udf(get_topic, StringType())
        preprocess_udf = udf(preprocess, StringType())
        nrc_sentiment_udf = udf(fetch_nrc, StringType())

        new_df = new_df.withColumn('Sentiment',predict_sentiment_udf(raw_df.text))
        new_df = new_df.withColumn('Topic',get_topic_udf(raw_df.text))
        tokenized_text = preprocess_udf(raw_df.text)
        new_df = new_df.withColumn('NRC_Sentiment',nrc_sentiment_udf(tokenized_text))
        
        # Modify the stream to pass the client to reply    
        stream = new_df.writeStream.format('console').foreach(
            reply
        ).start()
    logging.error("After starting stream")
    stream.awaitTermination()
    
    # Wait for the query to terminate
    stream0.awaitTermination()

def initialize_client():
    print("BOT_TOKEN: ", bot_token)
    print(type(bot_token))
    #client = TelegramClient('consumer_session2', api_id, api_hash).start(bot_token=bot_token)
    client = TelegramClient('consumer_session', api_id, api_hash).start(phone=phone_number)
    client.disconnect()
    print("Initialized session!!")

if __name__ == '__main__':
    topic = 'telegram_messages'
    #topic = 'telegram_messages_llm'
    initialize_client()
    spark = SparkSession.builder \
        .appName('telestream_app_llm') \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0") \
        .getOrCreate()
    # Make sure we have Spark 3.0+
    assert spark.version >= '3.0' 
    spark.sparkContext.setLogLevel('WARN')
    sc = spark.sparkContext
    main(topic)

# set PYSPARK_PYTHON=python
# set PYSPARK_DRIVER_PYTHON=python
