# Utility: Sentiment Corpus Reader
# Purpose: A utility to read sentiment corpora in a csv format
# Data file format has 6 fields:
# 0 - the polarity of the tweet (0 = negative, 2 = neutral, 4 = positive)
# 1 - the id of the tweet (2087)
# 2 - the date of the tweet (Sat May 16 23:58:44 UTC 2009)
# 3 - the query (lyx). If there is no query, then this value is NO_QUERY.
# 4 - the user that tweeted (robotickilldozr)
# 5 - the text of the tweet (Lyx is cool)


import csv
import util

# Given a file that adheres to the data format (above) return a list
# of tuples with the following information (sentiment score, tweet
# text)
def read_data(filename):
    training_data = []
    with open (filename, 'rb') as csvfile:
        corpus_reader = csv.reader(csvfile)
        for line in corpus_reader:
            training_data.append((util.to_words(line[5]), int(line[0])))

    return training_data


# Return the training data using the read_data function
def get_training_data():
    return read_data("/Users/rohan/Projects/Soccer/sentiment/training.1600000.processed.noemoticon.csv");

# Return the test data using the read_data function
def get_test_data():
    return read_data("/Users/rohan/Projects/Soccer/sentiment/testdata.manual.2009.06.14.csv");

    
                                

