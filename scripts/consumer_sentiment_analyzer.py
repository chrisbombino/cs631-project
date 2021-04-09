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
     message['text'] = sa.preprocess(message['text'])
     message['user_description'] = sa.preprocess(message['user_description'])
     
     # make predictions
     message['sentiment'] = sa.predict(message['text'], tokenizer)

     print("==============================================================")
     print(message)

     # save processed tweets with sentiments back to kafka in a separate topic
     producer.send(processed_topic_name, value=message)
