import json
from json import dumps
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from time import sleep
from kafka import KafkaProducer
from helper import process_time, convert_dict_to_string, get_products_to_track

# arguments
topic_name = 'raw_tweets_113'

# get keywords
keywords_to_track = get_products_to_track()

# twitter keys
API_KEY = '8rthBtNqfK2l1WXDXAHYaZQJH'
API_KEY_SECRET = 'Xl6qrzyZjQU9feBRYJkk6WD9e6lIWUuKGggWBxEwy8j83Fr7nd'
ACCESS_TOKEN = '1095921671557414913-ZpYZfegKEpycLhkfmFOlDUa3yN6195'
ACCESS_SECRET = '3QBsJRISQ2jhEtl05fvDNFckrhWS7xF6TINkrl2JFfEuW'

# twitter authorization
auth = OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# init tweepy
api = tweepy.API(auth)

# init kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'),
                         api_version=(0, 10, 1))

# Step 1: Creating a StreamListener: override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, tweet):
        length = len(tweet.text.split(' '))
        if (tweet.lang != 'en') or (length <= 10):
            pass
            print("==filtered==")
        else:
            message = {
                "text": tweet.text,
                "created_at": process_time(tweet.created_at),
                "id": tweet.id_str,
                "hashtags":  tweet.entities['hashtags'],
                #"symbols": tweet.entities['symbols'],
                "user_id": tweet.user.id_str,
                "user_location": tweet.user.location,
                "user_description": tweet.user.description,
                "user_followers_count": tweet.user.followers_count,
                "user_friends_count": tweet.user.friends_count,
                "user_listed_count": tweet.user.listed_count,
                "user_favourites_count": tweet.user.favourites_count,
                # "geo": tweet.geo,
                # "coordinates": tweet.coordinates,
                # "place": tweet.place,
                "retweet_count": tweet.retweet_count,
                "favorite_count": tweet.favorite_count,
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
        
# Step 2: Creating a Stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# Step 3: Starting a Stream
myStream.filter(track=keywords_to_track)
