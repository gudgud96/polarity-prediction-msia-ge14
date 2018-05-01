import sys
import csv
import pandas as pd
import numpy as np
from textblob import TextBlob, Word

  # =============== Data description ================= #
  # index 0: headers, should be ignore
  # index 1-300: true data, column 2 - tweets
  # column 5 - class (0 means anti, 1 means pro)
  # in column 5 row 301 - count for class 0, row 302 - count for class 1
  # ================================================== #

# a print method for all kinds of encoding, especially UTF-8
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
  enc = file.encoding
  if enc == 'UTF-8':
      print(*objects, sep=sep, end=end, file=file)
  else:
      f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
      print(*map(f, objects), sep=sep, end=end, file=file)

def prep_dict(dictionary):
  # uprint(dictionary) // to show the structure of the dictionary
  dict_struct = {}
  dict_struct_multi_words = {}
  for i in range(1, len(dictionary[0])):
    word, polarity, weight = dictionary[0][i], dictionary[1][i], dictionary[2][i]
    dict_struct[word] = (polarity, weight)
    
    # maintain another dict for multiple words lookup
    if len(word.split(' ')) > 1:
      for subword in word.split(' '):
        dict_struct_multi_words[subword] = word
  
  return dict_struct, dict_struct_multi_words

# analyse the polarity of a tweet by taking the average of sum of polarity of words
def tweet_analysis(tweet, dict_struct, dict_struct_multi_words):
  polarity = 0
  weight = 0
  significant_word = ''
  blob = TextBlob(tweet)
  used_words = []
  is_inverse = False
  for word in blob.words:
    if word in used_words:
      continue
    if word in dict_struct_multi_words:
      multiword = dict_struct_multi_words[word]
      if dict_struct[multiword][0] == "-2":
        is_inverse = True
      else:
        polarity += float(dict_struct[multiword][0])
        weight += float(dict_struct[multiword][1])
      significant_word += multiword + '+'
      used_words += multiword.split(' ')
    elif word in dict_struct:
      if dict_struct[word][0] == "-2":
        is_inverse = True
      else:
        polarity += float(dict_struct[word][0])
        weight += float(dict_struct[word][1])
        if word == 'Kesilapan':
          print(polarity)
      significant_word += word + '+'

  polarity = 0 if weight == 0 else (polarity / weight)
  
  if is_inverse:
    polarity = 0 - polarity
  predict_class = 0
  if polarity >= 0:
    predict_class = 1

  return predict_class, polarity, weight, significant_word[:-1]

def main():
  # not sure why this encoding is needed as utf-8 seems problematic for pandas
  data = pd.read_csv('najib_tweets.csv', header=None, encoding='latin1')
  dictionary = pd.read_csv('bag_of_words_sample.csv', header=None, encoding='latin1')  
  
  # prepare the dictionary
  dict_struct, dict_struct_multi_words = prep_dict(dictionary)
  
  # prepare the data
  tweets = data[2]
  clas = data[5]
  predicted_class = ['predicted_class']
  significant_words = ['significant_words']
  polarity_list = ['polarity']
  weight_list = ['weight']

  # do analysis for each tweet
  for i in range(1,301):
    predict_class, polarity, weight, significant_word = tweet_analysis(tweets[i], dict_struct, dict_struct_multi_words)
    predicted_class.append(predict_class)
    significant_words.append(significant_word)
    polarity_list.append(polarity)
    weight_list.append(weight)

  # write result to csv file
  with open("result.csv", 'w+') as csvfile:
    writer = csv.writer(csvfile, lineterminator='\n')
    for i in range(301):
      res = [tweets[i], clas[i], predicted_class[i], polarity_list[i], weight_list[i], significant_words[i]]
      writer.writerow(res)

  # print out accuracy
  correct = 0
  for i in range(1,301):
    if int(predicted_class[i]) == int(clas[i]):
      correct += 1
  print('Accuracy: ' + str(correct) + '/' + str(300) + ' ' + str(correct / 300))
 


if __name__ == '__main__':
  main()