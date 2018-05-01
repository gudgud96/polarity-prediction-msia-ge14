# -*- coding: utf-8 -*-
import sys
import tweepy
from textblob import TextBlob
import csv
import codecs
import re
import json

# a print method for all kinds of encoding, especially UTF-8
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
  enc = file.encoding
  if enc == 'UTF-8':
      print(*objects, sep=sep, end=end, file=file)
  else:
      f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
      print(*map(f, objects), sep=sep, end=end, file=file)

# This listener will print out all Tweets it receives
class PrintListener(tweepy.StreamListener):

  def on_data(self, data):
      with open("najib_tweets.csv", "a+") as output:
        # Decode the JSON data
        tweet = json.loads(data)
        i = 101
        # Print out the Tweet
        writer = csv.writer(output, lineterminator='\n')
        res = [str(i), tweet['created_at'], tweet['text'].encode('ascii', 'ignore')]
        analysis = TextBlob(tweet['text'])
        res.append(analysis.sentiment.polarity)
        res.append(analysis.sentiment.subjectivity)
        writer.writerow(res)
        uprint(tweet['text'])
  def on_error(self, status):
      print(status)

def main():
  # tweepy configuration keys
  consumer_key = 'yCMSQ5J3oaqz0zPNniM49G2kN'
  consumer_key_secret = 'xHnSPGHyjokErynsR9IQUW2M5MXAzjA2qgRl9ggVCLDkCCpCOe'
  access_token = '429533649-Z60AVJRGYZafCgfkH9sOZlLCKQL7OcgblehhkxmY'
  access_token_secret = 'UtIJoVY2xQFTEEmUuB5iefvMX3tM8kgZVjL3VhcW0n5De'

  auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
  auth.set_access_token(access_token, access_token_secret)

  # set up the API
  api = tweepy.API(auth)
  print(sys.stdout.encoding)

  # let's start with English tweets, then go on to explore on Malay tweets
  public_tweets = api.search("najib", count=100, since="2018-04-15", tweet_mode="extended")

  with open("najib_tweets.csv", "w") as output:
      writer = csv.writer(output, lineterminator='\n')
      writer.writerow(['index', 'created at', 'text', 'sentiment', 'subjectivity'])
      tweet_pool = []
      for i in range(len(public_tweets)):
        try:
          tweet = public_tweets[i].full_text
          if tweet in tweet_pool:
            continue
          else:
            tweet_pool.append(tweet)
          tweet = re.sub('RT \@\w*', '', tweet)
          tweet = re.sub('(\@\w*)|:', '', tweet).strip()
          res = [str(i), public_tweets[i].created_at, tweet]
          analysis = TextBlob(tweet)
          res.append(analysis.sentiment.polarity)
          res.append(analysis.sentiment.subjectivity)
          writer.writerow(res)
          # uprint(analysis.tags)
          # print(analysis.sentiment)
        except UnicodeEncodeError:
          pass

  listener = PrintListener()

  # Show system message
  print('I will now print Tweets containing "Najib"! ==>')

  # Connect the stream to our listener
  stream = tweepy.Stream(auth, listener)
  stream.filter(track=['najib'], async=True)


if __name__ == '__main__':
  main()
