#!/usr/bin/python
import json, re, sys, csv
from time import time
import spacy
import en_core_web_sm
# Spacy model setup (NOTE - change to lg to include vectors)
nlp = en_core_web_sm.load()

with open('train_data.json', 'r') as train_data: 
    data = json.load(train_data)

##################################################################
def getLemmatizer():
    from spacy.lemmatizer import Lemmatizer
    from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    return lemmatizer

def getTokens(doc):
    tokens = []
    for tok in doc: 
        if not tok.is_stop:
            tokens.append({ 'word':tok.lemma_, 'pos':tok.pos_ })
    return tokens

def getEntities(doc):
    ents = {}
    for ent in doc.ents: 
        if not ent.text.isspace():
            ents[ent.text] = ent.label_
    return ents

def clean(text):
    # spacing out special characters in preparation for abbreviations
    clean = re.sub('[\*\#\@]', ' ', text).lower().strip().lstrip()
    clean = re.sub(r'([\;\,\.\%\"\-\(\)\:\$\!\?])', r' \1', clean)
    # putting special characters back in place
    clean = re.sub(r' ([\;\,\.\%\"\-\(\)\:\$\!\?])', r'\1', clean)
    clean = re.sub(r'(\w+)/(\w+)', r'\1 \2', clean).capitalize()
    clean = re.sub('[\*\;\&\#\,\$\@\.\%\"\'\-\(\)\:\$\!\?\+\[\]\s+]',' ', clean)
    return clean

def preprocessing(data):
    for tweet in data:
        tweet['clean'] = clean(tweet['text'])
        doc = nlp(tweet['text'])
        tweet['entities'] = getEntities(doc) #marks target entity
        tweet['tokens'] = getTokens(doc)   #adds POS, removes stopwords, and lemmatizes
    return data
##################################################################

processedComments = preprocessing(data)

# writes new parameters into input file
with open("spacy_output.json", 'w') as outfile:
    json.dump(processedComments, outfile, sort_keys=True, indent=2, separators=(',', ': '))