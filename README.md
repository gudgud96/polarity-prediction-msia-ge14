# Polarity Prediction on Msia's GE14 tweets using Naive Bayes and NLP techniques
Date: 1.5.2018

![](ge14.jpg) ![](ge14-2.jpg)

The 14th General Election in Malaysia is coming!
In view of Siraj Raval's tutorial video (https://www.youtube.com/watch?v=o_OZdbCzHUA), this project aims to build a polarity predictor on tweets related to our beloved, dearest, wonderful Prime Minister, Najib Razak.

# Project Parts

1. A mechanism to scrape tweets related to Najib Razak
For this part we use a StreamListener from tweepy to scrape 300 real time tweets with keyword Najib (since directly querying API from twitter is not allowed for free). What we do is to leave the stream listener open for a period of time to scrape tweets we need.

2. Annotate the tweets
Textblob's polarity analysis is BAD on Malay tweets. What we can do is to break up the tweets into "bag of words", and annotate the polarity of each word on its own. Because of this, we decide to scrape lesser data.

3. Build a polarity analyzer and classifier
We compared two models: a Naive Bayes model, and a model using heuristic NLP techniques. In conclusion, the NB model achieves 0.9 accuracy on our test data, which the model using NLP techniques achieves accuracy of only 0.6, though, both models still have plenty of space for improvement.

# Wanna check out?

For my NLP model, simply do:
```
python sentiment_analysis_by_me.py
```
For my Naive Bayes model, simply do:
```
python tweet_polarity_naive_bayes_predictor.py
```
Interested in the implementation details? Check out my tech blogpost about this project here.

In conclusion: dearest Najib, don't you ever think that you are still favourable among the people!