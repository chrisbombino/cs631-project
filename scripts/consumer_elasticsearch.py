import os
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from json import loads
from uuid import uuid4

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

# start consuming
for message in consumer:

    # overwrite message with its value and preprocess text
    message = message.value.copy()

    # TODO: Copy code from christopher to save onto elasticsearch
    id = str(uuid4())
    res = es.index(index=INDEX_NAME, id=id, body=message)

    print("===============")
    print(message)
    #print(res['result'])
