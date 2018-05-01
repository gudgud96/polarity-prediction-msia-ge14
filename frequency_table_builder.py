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
  clas = dataset[:,5]

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

  # build the frequency table
  word_frequency_table = {}
  for i in range(1, 301):
    tweet = tweets[i]
    cls = int(clas[i])  # make it an integer, in case it is a string
    blob = TextBlob(tweet)
    for word in blob.words:
      word = word.lower().replace('\n', '').replace('\\n', '').replace("b'","")
      if word not in word_frequency_table.keys():
        word_frequency_table[word] = [0, 0]
        word_frequency_table[word][cls] += 1

  # write to csv file as frequency table
  with open('frequency_table.csv', 'w+') as wordbag:
    writer = csv.writer(wordbag, lineterminator='\n')
    header_row = ['word', 'f(0)', 'f(1)', 'f(0) + f(1)']
    writer.writerow(header_row)
    for word in word_frequency_table.keys():
      res = [word, word_frequency_table[word][0], word_frequency_table[word][1], word_frequency_table[word][0] + word_frequency_table[word][1]]
      writer.writerow(res)

  # TODO: we need some manual post process on handling multi-word terms. How to do that in program?
  
if __name__ == '__main__':
  filename = input("Enter filename:")
  data_builder(filename)