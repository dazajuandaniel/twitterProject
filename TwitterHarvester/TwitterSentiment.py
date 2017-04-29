import re
from textblob import TextBlob

def processTweet(tweet_text):
    '''Cleans a Tweets by removing unnecessary data'''
    clean_tweet = tweet_text.lower()
    #Convert www.* or https?://* to URL
    clean_tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',clean_tweet)
    #Convert @username to AT_USER
    clean_tweet = re.sub('@[^\s]+','AT_USER',clean_tweet)
    #Remove additional white spaces
    clean_tweet = re.sub('[\s]+', ' ', clean_tweet)
    #Replace #word with word
    clean_tweet = re.sub(r'#([^\s]+)', r'\1', clean_tweet)
    #trim
    clean_tweet = clean_tweet.strip('\'"')
    return clean_tweet

def getSentiment(clean_tweet,neutral_threshold=0):
    '''Return Positive, Neutral or Negative Tweet Rating'''
    blob=TextBlob(clean_tweet).sentiment.polarity
    if -neutral_threshold <= blob <= neutral_threshold:
        return "Neutral"
    elif blob>neutral_threshold:
        return "Positive"
    else:
        return "Negative"