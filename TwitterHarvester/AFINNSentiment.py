#!/usr/bin/python 
# (originally entered at https://gist.github.com/1035399)
# License: GPLv3
# To download the AFINN word list do:
# wget http://www2.imm.dtu.dk/pubdb/views/edoc_download.php/6010/zip/imm6010.zip
# unzip imm6010.zip
# https://finnaarupnielsen.wordpress.com/2011/06/20/simplest-sentiment-analysis-in-python-with-af/
# Note that for pedagogic reasons there is a UNICODE/UTF-8 error in the code.

import math
import re
import sys
from TwitterSentiment import processTweet
reload(sys)
sys.setdefaultencoding('utf-8')

# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = 'AFINN/AFINN-111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ 
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")

def sentiment(text):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence. 
    """
    text=processTweet(text)
    words = pattern_split.split(text.lower())
    sentiments = map(lambda word: afinn.get(word, 0), words)
    if sentiments:
        # How should you weight the individual word sentiments? 
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
        
    else:
        sentiment = 0
    return sentiment

def getSentiment(value,neutral_threshold=0):
    '''Return Positive, Neutral or Negative Tweet Rating'''
    if -neutral_threshold <= value <= neutral_threshold:
        return "Neutral"
    elif value>neutral_threshold:
        return "Positive"
    else:
        return "Negative"

