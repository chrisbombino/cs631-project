from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
from SentimentAnalyzer import SentimentAnalyzer
from helper import get_associated_company_and_product

# arguments
source_topic_name = 'raw_tweets_113'
sink_topic_name = 'analyzed_tweets_113'
consumer_group_id = 'sentiment_analysis_consumers'

# init consumer
consumer = KafkaConsumer(
     source_topic_name,
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

     # extract hashtags
     hashtags = []
     if len(message['hashtags'])!=0:
          for hashtag_data in message['hashtags']:
               hashtags.append(hashtag_data["text"])

     # overwrite hashtags data structure with plain hashtags text
     message["hashtags"] = hashtags

     # get product and company info
     message["company"], message["product"] = get_associated_company_and_product(message['text'])

     # preprocess text data
     try:
          tokenized_text = sa.preprocess(message['text'])
     except:
          tokenized_text = []

     # make predictions

     try:
          message['sentiment'], message['confidence'] = sa.predict(tokenized_text, tokenizer)
     except: # to prevent there may be other bugs we did not imagine
          message['sentiment'], message['confidence'] = ('Neutral', 0.5)
     
     # for identiable tweets, save analyzed tweets back to kafka in a separate topic
     if message["company"] != "none" and message["company"] != "mix":
          print("==============================================================")
          print(message)
          producer.send(sink_topic_name, value=message)
     
     else:
          print("==============================================================")
          print("Product match not found.")       