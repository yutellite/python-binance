# import the necessary libraries
import tweepy
import os

# Set up API credentials
consumer_key = "Fchea8D8cYfJgvMZaEJfOvLNM"
consumer_secret = "p8pf14Sxg0IQI9qWqBvb0PDf5lV09i17nyB4SCGm6VFNVIkTdG"
access_token = "890741523892981760-4TRB4A8LvIRx0jUjJU6hPfQvWOCD42e"
access_token_secret = "hRESgWPAumwOzh9JvCuL45ox2SpuFNIh1xCFETlE14T2o"

# Set up API credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAAD%2BumgEAAAAA4bRHjzRE1PjxWCkxoUtMBn%2Fpsa0%3DN9GEquLcLe9rKCkrSMSaENcMCA8G81ySJnzFaqKw76SXKdv9h0"

# Set up API credentials
consumer_key = "Fchea8D8cYfJgvMZaEJfOvLNM"
consumer_secret = "p8pf14Sxg0IQI9qWqBvb0PDf5lV09i17nyB4SCGm6VFNVIkTdG"

# Authenticate with Twitter API
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)

# Set up API client
api = tweepy.API(auth)

# Define search keyword and maximum number of tweets to retrieve
keyword = "example"
max_tweets = 1000

# Retrieve all tweets containing the keyword
tweets = []
for tweet in tweepy.Cursor(api.search_tweets, q=keyword).items(max_tweets):
    tweets.append(tweet.text)

# Print the text content of all retrieved tweets
for tweet in tweets:
    print(tweet)
