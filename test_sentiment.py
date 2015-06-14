#!/usr/bin/env python

import sentiment.util as su
import sentiment.corpusreader as cr
from nltk.corpus import movie_reviews 
import nltk
import feedparser
from colorama import Fore, Back, Style
import sys
import random
from multiprocessing import Pool

def build_classifier(feature_extractor):
    classifier = su.generate_sentiment_classifier(movie_reviews, feature_extractor)
    return classifier

def evaluate_on_rss_feed(feed_url, classifier, feature_extractor):
    
    d = feedparser.parse(feed_url)
    for entry in d['entries']:
        output =  classifier.classify(feature_extractor(nltk.word_tokenize(entry['title'])))
        color = Fore.RED if  output == 0 else Fore.GREEN
        print(color + entry['title'])
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)


def test_classifier_prompt(classifier):
    print "Classifier trained! Try it out. Please enter a sentence"
    import fileinput

    while (True):
        line = raw_input('-->')
        print line
        feats = su.bag_of_word_feats(su.to_words(line))
        guess = classifier.classify(feats)
        print guess



p = Pool(5)
training_size = 10000     
    
training_data = cr.get_training_data()
random.shuffle(training_data)
#training_data = training_data[:training_size]
training_data = p.map(su.clean_tweet_tuple, training_data)


negative_count = sum ( t[1] == 0 for t in training_data)
print negative_count
positive_count = sum ( t[1] == 4 for t in training_data)
print positive_count
neutral_count = sum ( t[1] == 2 for t in training_data)
print neutral_count

feature_extractor = su.bag_of_word_feats

classifier = su.train_classifier(training_data, feature_extractor)
classifier.show_most_informative_features()

test_data = cr.get_test_data()

test_data = filter(lambda x: x[1] != 2, test_data)

su.test_classifier(test_data, classifier, feature_extractor)

# feature_extractor = feature_extractor
feed_url = 'feed://www.espnfc.com/barclays-premier-league/23/rss'

# classifier_bag_of_words = build_classifier(feature_extractor)
#evaluate_on_rss_feed(feed_url, classifier, feature_extractor)


# feature_extractor = su.bigram_word_feats
# classifier_bigram = build_classifier(feature_extractor)
# evaluate_on_rss_feed(feed_url, classifier_bigram, feature_extractor)



