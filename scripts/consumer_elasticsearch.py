from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from json import loads

# arguments
processed_topic_name = 'processed_tweets'
consumer_group_id = 'elasticsearch-consumers'

# init consumer
consumer = KafkaConsumer(
     processed_topic_name,
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

     # index on elasticsearch cluster
     res = es.index(index="test-index", body=message)

     print("===============")
     print(message)
     #print(res['result'])