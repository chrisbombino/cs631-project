# https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1

from time import sleep
from json import dumps
from kafka import KafkaProducer

# init
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'),
                         api_version=(0, 10, 1)) 

# generate data and send to broker topics
for e in range(1000):
    data = {'number' : e}
    producer.send('new', value=data)
    sleep(5)