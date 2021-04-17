import os
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from json import loads
from uuid import uuid4
from helper import process_time

# arguments
source_topic_name = 'analyzed_tweets_112'
consumer_group_id = 'elasticsearch_consumers'
index_name = 'sentiment_analysis_112'

# init consumer
consumer = KafkaConsumer(
     source_topic_name,
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id=consumer_group_id,
     value_deserializer=lambda x: loads(x.decode('utf-8')))

# init elasticsearch
es_password = os.getenv('ES_PASS') or ''
es = Elasticsearch([{'host': 'localhost', 'port': 9200}], http_auth=('elastic', es_password))

INDEX_NAME = 'processed_tweets'

mappings = {
  "mappings": {
    "properties": {
      "created_at": {
        "type": "date"
      }
    }
  }
}

# create index
indices = es.indices
if not es.indices.exists(INDEX_NAME):
    indices.create(INDEX_NAME, body=mappings)
    print('created elasticsearch index {}'.format(INDEX_NAME))

# specify mappings

mappings = {
  "mappings": {
    "properties": {
      "created_at": {
        "type": "date"
      }
    }
  }
}

# create index
indices = es.indices
if not es.indices.exists(index_name):
    a = indices.create(index_name, body=mappings)
    print('created index {}'.format(index_name))
    print(a)

# start consuming
for message in consumer:

     # overwrite message with its value and preprocess text
     message = message.value.copy()

     print("===============")
     print(message)

     # write onto elasticsearch index
     id = str(uuid4())
     res = es.index(index=INDEX_NAME, id=id, body=message)
