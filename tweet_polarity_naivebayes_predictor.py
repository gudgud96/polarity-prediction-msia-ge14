import pandas as pd 
from textblob import TextBlob
import numpy as np
import csv
import sys

# ======= Some statistics about the data ========= #
# P(C=0) = 182/300 = 0.6067
# P(C=1) = 118/300 = 0.3933
# Number of words = 1324
# ================================================ #

# a print method for all kinds of encoding, especially UTF-8
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
  enc = file.encoding
  if enc == 'UTF-8':
      print(*objects, sep=sep, end=end, file=file)
  else:
      f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
      print(*map(f, objects), sep=sep, end=end, file=file)

def main():
  testing_set = pd.read_csv('testing_set.csv', header=None, encoding='latin1')
  freq_table = pd.read_csv('frequency_table.csv', header=0, encoding='latin1')
  dictionary = pd.read_csv('bag_of_words_sample.csv', header=0, encoding='latin1')

  # preprocessing raw csv data
  testing_tweets = testing_set[2]
  testing_class = testing_set[3]
  word_list = freq_table['word'].values.tolist()  # tolist() needed for index() method usage
  f0_list = freq_table['f(0)']
  f1_list = freq_table['f(1)']
  f_list = freq_table['f(0) + f(1)']

  bag_of_words = dictionary['word'].values.tolist()
  polarity_list = dictionary['polarity']

  predicted_class = []
  p0_list = []
  p1_list = []
  words_selected = []

  for tweet in testing_tweets:
    temp_p0 = []
    temp_p1 = []
    word_selected = ''
    blob = TextBlob(tweet)
    for word in blob.words:
      word = word.lower().replace('\n', '').replace('\\n', '').replace("b'","")
      
      if word in word_list:
        word_selected += word + '+'
        index = word_list.index(word)
        f0, f1, f = float(f0_list[index]), float(f1_list[index]), float(f_list[index])
        temp_p0.append(f0 / 182)  # P(word|C=0)
        temp_p1.append(f1 / 118)  # P(word|C=1)
      
      else:   # else if the word is not in, we lookup to our built dictionary
        if word in bag_of_words:
          index2 = bag_of_words.index(word)
          polarity = polarity_list[index2]
          if polarity > 0:
            temp_p0.append(0.001 / 182)  # if polarity > 0, count it as an occurence in P(C=1)
            temp_p1.append(0.999 / 118)
            word_selected += '[' + word + ']' + '+'
          elif polarity < 0:
            temp_p0.append(0.999 / 182)  # and vice versa, if polarity = 0 do nothing
            temp_p1.append(0.001 / 118)
            word_selected += '[' + word + ']' + '+'

    words_selected.append(word_selected[:-1])
    p0 = 0 if not temp_p0 else np.prod(temp_p0)
    p1 = 0 if not temp_p1 else np.prod(temp_p1)
    p0_list.append(p0 * 0.6067)
    p1_list.append(p1 * 0.3933)
    p_class = 0 if p0 * 0.6067 > p1 * 0.3933 else 1
    predicted_class.append(p_class)

  correct = 0
  with open('result_prediction_3.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile, lineterminator='\n')
    writer.writerow(['tweet', 'P(C=0)', 'P(C=1)', 'Predicted Class', 'Actual Class', 'Selected Words'])
    for i in range(len(testing_tweets)):
      tweet = testing_tweets[i]
      res = [tweet, p0_list[i], p1_list[i], predicted_class[i], testing_class[i], words_selected[i]]
      writer.writerow(res)
      if int(predicted_class[i]) == int(testing_class[i]):
        correct += 1

  print('Accuracy of NB predictor: ' + str(correct/len(testing_tweets)))

if __name__ == '__main__':
  main()

  







