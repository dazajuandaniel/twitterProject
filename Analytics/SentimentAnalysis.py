#!/usr/bin/env python
import json
import string
import sys, re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from textblob import TextBlob
from pprint import pprint

tweets = {}
ids = []

with open('smallTwitter.json', 'r') as file:
	for line in file:
		if line == '[\n':
			continue
		if line == ']\n':
			break
		content = json.loads(line.replace(",\n", "\n"))
		jsonDict = content["json"]
		text = json.dumps(jsonDict["text"])
		tid = jsonDict["id"]
		ids.append(jsonDict["id"])
		tweets[tid] = text
file.close()

emoticonStr = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regexStr = [
	emoticonStr,
	r'<[^>]+>',
	r'(?:@[\w_]+)',
	r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",
	r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
	r'(?:(?:\d+,?)+(?:\.?\d+)?)',
	r"(?:[a-z][a-z'\-_]+[a-z])",
	r'(?:[\w_]+)',
	r'(?:\S)'
]

tokensRe = re.compile(r'('+'|'.join(regexStr)+')', re.VERBOSE | re.IGNORECASE)
emoticonRe = re.compile(r'^'+emoticonStr+'$', re.VERBOSE | re.IGNORECASE)
punc = list(string.punctuation)
stop = stopwords.words('english') + punc + ['rt', 'via']

def tokenize(s):
	return tokensRe.findall(s)

def preprocess(s, lowercase = False):
	tokens = tokenize(s)
	if lowercase:
		tokens = [token if emoticonRe.search(token) else token.lower() for token in tokens]
	return tokens

countAllTerms = Counter()

for i in ids:
	tw = tweets[i]
	# terms = [term for term in preprocess(tw) if term.lower() not in stop and
	# 		not term.startswith(('u', '@'))]
	blob = TextBlob(tw)
	print blob.sentiment
	# countAllTerms.update(terms)

print(countAllTerms.most_common(10))




