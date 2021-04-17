# Standard library imports
from json import dumps

# 3rd party imports
import tweepy
from tweepy.streaming import StreamListener
from kafka import KafkaProducer

# local imports
from helper import process_time

# arguments
topic_name = 'tweets'
keywords_to_track = ['iphone', 'ipad', 'apple music', 'apple pay', 'macbook', 'itunes', 'airpod']

# twitter keys
API_KEY = '8rthBtNqfK2l1WXDXAHYaZQJH'
API_KEY_SECRET = 'Xl6qrzyZjQU9feBRYJkk6WD9e6lIWUuKGggWBxEwy8j83Fr7nd'
ACCESS_TOKEN = '1095921671557414913-ZpYZfegKEpycLhkfmFOlDUa3yN6195'
ACCESS_SECRET = '3QBsJRISQ2jhEtl05fvDNFckrhWS7xF6TINkrl2JFfEuW'

# twitter authorization
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# init tweepy
api = tweepy.API(auth)

# init kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'),
                         api_version=(0, 10, 1))

api.search_full_archive()

# Step 1: Creating a StreamListener: override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        length = len(tweet.text.split(' '))
        if (tweet.lang != 'en') or (length <= 10):
            pass
            print("==filtered==")
            # print("lang: ", tweet.lang)
            # print("length: ", len(tweet.text.split(' ')))

        else:
            message = {
                "text": tweet.text,
                "created_at": process_time(tweet.created_at),
                "id": tweet.id_str,
                "hashtags":  tweet.entities['hashtags'],
                "symbols": tweet.entities['symbols'],
                "user_id": tweet.user.id_str,
                "user_location": tweet.user.location,
                "user_description": tweet.user.description,
                "user_followers_count": str(tweet.user.followers_count),
                "user_friends_count": str(tweet.user.friends_count),
                "user_listed_count": str(tweet.user.listed_count),
                "user_favourites_count": str(tweet.user.favourites_count),
                # "geo": tweet.geo,
                # "coordinates": tweet.coordinates,
                # "place": tweet.place,
                "retweet_count": str(tweet.retweet_count),
                "favorite_count": str(tweet.favorite_count),
            }

            print("message:", message)

            # write to kafka topic
            producer.send(topic_name, value=message)

    def on_error(self, status_code):
        print(status_code)

        # snippet from official documentation
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.
