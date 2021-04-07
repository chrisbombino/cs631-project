from kafka import KafkaConsumer
from json import loads
from SentimentAnalyzer import SentimentAnalyzer

# arguments
topic_name = 'tweets'

# init consumer
consumer = KafkaConsumer(
     topic_name,
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='tweets-consumers',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

# init sentiment analyzer
sa = SentimentAnalyzer()

# start consuming
for message in consumer:
     # message value and key are raw bytes -- decode if necessary!
     # e.g., for unicode: `message.value.decode('utf-8')`
     message = message.value.copy()
     print("==============================================================")
     text = message['text']
     #print (text, ":\t", sa.predict(text))
     message['sentiment'] = sa.predict(text)
     print(message)
