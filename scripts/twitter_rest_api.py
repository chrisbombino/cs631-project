import json
import tweepy
from tweepy import OAuthHandler


# twitter keys
CONSUMER_KEY = 'ThuuAkxVQbV4ePWzqf9ZvHlIJ'
CONSUMER_SECRET = 'jxcuRlU8XRoDjKwGrZryoqTQO72gCtC2LBZz5i7HfZiP0HJ3qu'
ACCESS_TOKEN = '1379468364725284872-2ywjKYcTUSjTEOiJMPI8eCnjYhRfp5'
ACCESS_SECRET = 'hYO836ahutGP0c68CZBO1ayVquHb1Bjq2qOxjpXtUPW38'

# twitter authorization
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# init
api = tweepy.API(auth)

# tweets from a specific user. if the account is protected, it will raise auth error
trump_tweets = api.user_timeline('NaveedShahzeb')
for tweet in trump_tweets:
    print(tweet)

# follow all
print("followers")
print(api.followers)
print(list(tweepy.Cursor(api.followers).items()))

# may need this
    # loop through tweet objects
    # for tweet in tweet_object:
    #     tweet_id = tweet.id # unique integer identifier for tweet
    #     text = tweet.text # utf-8 text of tweet
    #     favorite_count = tweet.favorite_count
    #     retweet_count = tweet.retweet_count
    #     created_at = tweet.created_at # utc time tweet created
    #     source = tweet.source # utility used to post tweet
    #     reply_to_status = tweet.in_reply_to_status_id # if reply int of orginal tweet id
    #     reply_to_user = tweet.in_reply_to_screen_name # if reply original tweetes screenname
    #     retweets = tweet.retweet_count # number of times this tweet retweeted
    #     favorites = tweet.favorite_count # number of time this tweet liked
    #     # append attributes to list
    #     tweet_list.append({'tweet_id':tweet_id, 
    #                       'text':text, 
    #                       'favorite_count':favorite_count,
    #                       'retweet_count':retweet_count,
    #                       'created_at':created_at, 
    #                       'source':source, 
    #                       'reply_to_status':reply_to_status, 
    #                       'reply_to_user':reply_to_user,
    #                       'retweets':retweets,
    #                       'favorites':favorites})