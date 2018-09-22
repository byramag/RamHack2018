#!/usr/bin/python

# General imports
import json, re, sys, pandas
from time import time

##############################
# Spacy imports
import spacy
import en_core_web_sm

# Spacy model setup (NOTE - change to lg to include vectors)
nlp = en_core_web_sm.load()
###############################

# Param is JSON of data
if len(sys.argv) < 1:
   exit
json_file = sys.argv[1]

# reading in comment json
with open(json_file, 'r') as comment_data: 
    comments = json.load(comment_data)

# Toggles for options
map = True
stop = 2    # NOTE stop = 0 means no removal, increasing means removing more extreme words
lem = True
ner = False

##################################################################
def getLemmatizer():
    from spacy.lemmatizer import Lemmatizer
    from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    return lemmatizer

def inputSetup():
    toReturn = [null, null, null, null]
    #create lemmatizer
    if lem:
        lemmatizer = getLemmatizer()
        toReturn[0] = lemmatizer
    # using abbreviations json as dictionary
    if map:
        with open('datasets/abbreviations.json') as abb:
            abbreviations = json.load(abb)
        toReturn[1] = abbreviations
    # eid mapping
    with open('datasets/eid.json', 'r') as eid_data: 
        eids = json.load(eid_data)
    toReturn[2] = eids
    # using stopwords json as dictionary
    if stop > 0:
        with open('datasets/stopwords.json') as stops:
            stopwords = json.load(stops)
        toReturn[3] = stopwords
    return toReturn

def addDefaults(comment, eids, id):
    comment['id'] = id
    comment['userId'] = comment['userId'].upper()
    comment['department'] = "N/A"
    if comment['userId'] in eids:
        comment['department'] = eids[comment['userId']]['Costcenterdescription']
    return comment
    
def mapTokens(tokens, abbrevations):
    for word in tokens.split():
        if word in abbreviations.keys():
            tokens = re.sub(r'\b' + word + r'\b', abbreviations[word], tokens)
    return tokens

def getNer(doc):
    ents = {}
    for ent in doc.ents: 
        if not ent.text.isspace():
            ents[ent.text] = ent.label_
    return ents

def clean(feedback, abbr):
    # spacing out special characters in preparation for abbreviations
    clean = re.sub('[\*\#\@]', ' ', feedback).lower().strip().lstrip()
    clean = re.sub(r'([\;\,\.\%\"\-\(\)\:\$\!\?])', r' \1', clean)
    clean = mapTokens(clean, abbr)
    # putting special characters back in place
    clean = re.sub(r' ([\;\,\.\%\"\-\(\)\:\$\!\?])', r'\1', clean)
    clean = re.sub(r'(\w+)/(\w+)', r'\1 \2', clean)
    # adds 'clean' parameter to JSON object
    comment['clean'] = clean.capitalize()
    return clean

def formatTokens(doc, lemmatizer, stopwords):
    tokensArray = []
    for token in doc:
        # Stopword removal
        if element in stopwords.keys() and stopwords[element] <= stop:
            continue
        word = token.text_
        # Lemmatizing
        if lem:
            lemma = lemmatizer(element, token.pos_)
            word = lem[0]
        tokenInfo = { 'word' : word, 'tag' : token.pos_ }
        tokensArray.append(tokenInfo)
    return tokensArray

def processSingleComment(comment, referenceFiles, id):
    comment = addDefaults(comment, referenceFiles[2], id)
    if ('feedback' not in comment or comment['feedback'] == '' or comment['feedback'] == 'undefined'):
        return comment
    comment['clean'] = clean(comment['feedback'], referenceFiles[1])
    clean = re.sub('[\*\;\&\#\,\$\@\.\%\"\'\-\(\)\:\$\!\?\+\[\]\s+]',' ', clean)
    doc = nlp(clean)
    if ner:
        comment['entities'] = getNer(doc)
    comment['tokens'] = formatTokens(clean, referenceFiles[0], referenceFiles[3])
    return comment

# USE THIS METHOD
def preprocessing(data):
    refenceFiles = inputSetup()
    processed = []
    countForId = 0
    for comment in data:
        countForId += 1
        processed.append(processSingleComment(comment, referenceFiles, countForId))
    return processed
##################################################################


processedComments = preprocessing(comments)

# writes new parameters into input file
with open("spacy_output.json", 'w') as outfile:
    json.dump(processedComments, outfile, sort_keys=True, indent=2, separators=(',', ': '))