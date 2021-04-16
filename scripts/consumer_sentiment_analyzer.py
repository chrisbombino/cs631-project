from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
from SentimentAnalyzer import SentimentAnalyzer

# arguments
topic_name = 'tweets'
processed_topic_name = 'processed_tweets'
consumer_group_id = 'sentiment-analysis-consumers'

# init consumer
consumer = KafkaConsumer(
     topic_name,
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id=consumer_group_id,
     value_deserializer=lambda x: loads(x.decode('utf-8')))

# init producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'),
                         api_version=(0, 10, 1))

# init sentiment analyzer
sa = SentimentAnalyzer()
tokenizer = sa.token()
# start consuming
for message in consumer:

     # overwrite message with its value and preprocess text
     message = message.value.copy()
     try:
          message['text_list'] = sa.preprocess(message['text'])
     except:
          message['text_list'] = []

     try:
          message['user_description_list'] = sa.preprocess(message['user_description'])
     except:
          message['user_description_list'] = []

     # make predictions
     message['sentiment_name'], message['sentiment'], message['confidence']  = sa.predict(message['text_list'], tokenizer)

     print("==============================================================")
     print(message)

     # save processed tweets with sentiments back to kafka in a separate topic
     producer.send(processed_topic_name, value=message)