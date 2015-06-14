
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import collections, itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from  nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english", ignore_stopwords=True)
def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    print words, "\n"
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

def bag_of_word_feats(words):
    return dict([(word, True) for word in words])

def to_words(text):
    return text.split()

#  Words are cleaned by finding repeated sequences of three or more
# characters and reducing them to two. For example, "looooveeee" will
# be shortened to "loovee". This will also lowercase every word and stem. "Running" will become "run"
def clean_word(word):

    if not word:
        return ""
    word = word.lower()
    
    count = 0
    last_char = word[0]
    result = ""

    for i in range(len(word)):
        curr_char = word[i]
        if curr_char == last_char:
            count+= 1
        else:
            count = 1

        if count < 3:
            result += curr_char
            
        last_char = curr_char

    return result

# Filters duplicates from lists
def filter_duplicates(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

# Returns a list of words that are cleaned up by calling 'clean_word'
# on each word of the tweet. Expects tweets to come in the form of a
# list of words. The cleaned list of words will be ordered as they
# were in the input tweet. Also filters out '@user' tweets. 
def clean_tweet(tweet):
    tweet = filter (lambda w: "@" not in w, tweet)
    tweet = filter_duplicates(tweet)
    return map(clean_word, tweet)

def clean_tweet_tuple(tweet_tuple):
    return (clean_tweet(tweet_tuple[0]),tweet_tuple[1])
    

# Returns an NLTK Naive Bayes Classifier trained on the
# 'training_data'. Expects training data to come in a list of tuples of
# the form ( Words, Class ), word_feats must take in a list of words
# and return a dictionary of features.
def train_classifier(training_data, word_feats):
    trainingfeats = [(word_feats(f[0]), f[1]) for f in training_data]
    return NaiveBayesClassifier.train(trainingfeats)

# Measures precision and recall for the test data for the given
# classifier
def test_classifier(test_data, classifier, word_feats):

    # test features with labels
    testfeats = [(word_feats(f[0]), f[1]) for f in test_data]


    # dictionary for actual vs observed indices
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
 
    for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)

    accuracy = nltk.classify.util.accuracy(classifier, testfeats)
    print "accuracy:", accuracy
    print 'pos precision:', nltk.metrics.precision(refsets[4], testsets[4])
    print 'pos recall:', nltk.metrics.recall(refsets[4], testsets[4])
    print 'neg precision:', nltk.metrics.precision(refsets[0], testsets[0])
    print 'neg recall:', nltk.metrics.recall(refsets[0], testsets[0])
    
    

def generate_sentiment_classifier(corpus, word_feats):
    negids = corpus.fileids('neg')
    posids = corpus.fileids('pos')
    negfeats = [(word_feats(corpus.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(corpus.words(fileids=[f])), 'pos') for f in posids]

    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
 

    classifier = NaiveBayesClassifier.train(trainfeats)

    for i, (feats, label) in enumerate(testfeats):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)



    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
    print 'pos precision:', nltk.metrics.precision(refsets['pos'], testsets['pos'])
    print 'pos recall:', nltk.metrics.recall(refsets['pos'], testsets['pos'])
    print 'neg precision:', nltk.metrics.precision(refsets['neg'], testsets['neg'])
    print 'neg recall:', nltk.metrics.recall(refsets['neg'], testsets['neg'])
    classifier.show_most_informative_features()

    return classifier




