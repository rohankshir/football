#!/usr/bin/env python

import sentiment.util
from nltk.corpus import movie_reviews 
import nltk 

classifier = sentiment.util.generate_sentiment_classifier(movie_reviews)

import feedparser

d = feedparser.parse('feed://www.espnfc.com/barclays-premier-league/23/rss')

tokenized_headlines = [nltk.word_tokenize(entry['title']) for entry in d['entries']]
print tokenized_headlines

