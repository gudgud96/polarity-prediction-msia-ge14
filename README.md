# Polarity Prediction on Msia's GE14 tweets using Naive Bayes and NLP techniques
Date: 1.5.2018

!['GE14 is coming! Make a difference by voting!'](ge14.jpg)

The 14th General Election in Malaysia is coming!
In view of Siraj Raval's tutorial video (https://www.youtube.com/watch?v=o_OZdbCzHUA), this project aims to build a sentiment analyzer on tweets related to our beloved, dearest, wonderful Prime Minister, Najib Razak.

This project consists of the following parts, and is still currently developing:

1. A mechanism to scrape tweets related to Najib Razak (DONE)
For this part we use a StreamListener from tweepy to scrape real time tweets with keyword Najib (since directly querying API from twitter is not allowed for free). What we do is to leave the stream listener open for a period of time to scrape tweets we need.

2. Annotate the tweets
Textblob's polarity analysis is BAD on Malay tweets. What we can do is to break up the tweets into "bag of words", and annotate the polarity of each word on its own. Because of this, we decide to scrape lesser data.

3. Build a polarity analyzer and classifier
I am currently thinking of using NaiveBayes model for measuring the polarity (let's see if it works well).

Hope that this project is able to preview some insights of GE14, to see if our dearest Najib is still that favourable among the people!