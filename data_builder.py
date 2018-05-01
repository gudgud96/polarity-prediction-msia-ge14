import csv
import codecs
import re
import json
import sys
import numpy as np
from textblob import TextBlob, Word

def data_builder(filename):
  dataset = []
  with open(filename, "r+") as csvfile:
    read = csv.reader(csvfile)
    for row in read:
      dataset.append(row)
  
  dataset = np.asarray(dataset)
  tweets = dataset[:,2]

  # sanitizing the tweets
  with open('sanitized_tweets_sample.txt', 'w+') as txtfile:
    for i in range(len(tweets)):
      tweet = tweets[i]
      pattern_weblink = r"(https(:?)//).*$"
      pattern_retweet = r"(b'RT @)[^:]*: "
      tweet = re.sub(pattern_weblink, "", tweet)
      tweet = re.sub(pattern_retweet, "", tweet)
      tweets[i] = tweet
      txtfile.write(tweet + '\n\n')

  # build the bag of words model for annotation
  bag_of_words = []
  for tweet in tweets:
    blob = TextBlob(tweet)
    for word in blob.words:
      word = word.lower().replace('\n', '').replace('\\n', '').replace("b'","")
      # for lemmatization, a corpus is downloaded from NLTK
      word = Word(word).lemmatize()
      if word not in bag_of_words:
        bag_of_words.append(word)

  with open('bag_of_words_sample.csv', 'w+') as wordbag:
    writer = csv.writer(wordbag, lineterminator='\n')
    for word in bag_of_words:
      blob = TextBlob(word)
      res = [word, blob.sentiment.polarity, blob.sentiment.subjectivity]
      writer.writerow(res)
  
filename = input("Enter filename:")
data_builder(filename)