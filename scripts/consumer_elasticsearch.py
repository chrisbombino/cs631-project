from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from json import loads
from uuid import uuid4

# arguments
source_topic_name = 'analyzed_tweets_106'
consumer_group_id = 'elasticsearch_consumers'
index_name = 'tweets_106'

# init consumer
consumer = KafkaConsumer(
     source_topic_name,
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id=consumer_group_id,
     value_deserializer=lambda x: loads(x.decode('utf-8')))

# init elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# start consuming
for message in consumer:

     # overwrite message with its value and preprocess text
     message = message.value.copy()

     print("===============")
     print(message)

     # for elasticsearch to pick-up timestamps, have to specify a _timestamp field
     # not sure if it looks for _ prefix for metadata of the document or
     # the field name has to contain a "timestamp" substring.
     #message["date"] = message["created_at"]
     message["_timestamp"] = message["created_at"]

     # write onto elasticsearch index
     id = str(uuid4())
     res = es.index(index=index_name, id=id, body=message)


