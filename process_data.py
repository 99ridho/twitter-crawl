#!/usr/bin/python3

import json
import getopt
import sys
import re
import string
import demoji
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

demoji.download_codes()

def load_json_file(filename):
    f = open(filename)
    json_data = {}
    try:
        json_data = json.load(f)
    finally:
        f.close()
    return json_data

def clean_tweets(data):
    new_data = data.copy()

    username_hash = r'[#@]\w+'
    punctuation = '[%s]+' % re.escape(string.punctuation)
    special_char = r'[^0-9a-zA-Z\s]+'
    number = r'[0-9]+'
    space = r'\s{2,}'
    space_begin_end = r'^\s+|\s+$'
    url = r'(https?|www):\/{1,}\w+\W+\w+\/{1,}\w+'
    char_ref = r'&\w+;'

    for i in range(len(new_data)):
        new_data[i] = re.sub(char_ref, ' ', new_data[i])
        new_data[i] = re.sub(username_hash, '', new_data[i])
        new_data[i] = re.sub(url, '', new_data[i])
        new_data[i] = re.sub(punctuation, '', new_data[i])
        new_data[i] = re.sub(number, '', new_data[i])
        new_data[i] = re.sub(space_begin_end, '', new_data[i])
        new_data[i] = re.sub(space, '', new_data[i])
        new_data[i] = demoji.replace(new_data[i], '')
        new_data[i] = re.sub(special_char, '', new_data[i])
        new_data[i] = new_data[i].replace('\n', ' ')
        new_data[i] = new_data[i].replace('\xa0', ' ')
        new_data[i] = new_data[i].strip().lower()

    return new_data

def case_fold(data):
    new_data = data.copy()
    return list(map(lambda s: s.lower(), new_data))

def tokenize(data):
    new_data = data.copy()
    return list(map(lambda s: s.split(' '), new_data))

def stem(data):
    new_data = data.copy()
    stemmer = StemmerFactory().create_stemmer()

    return list(map(lambda s: stemmer.stem(s), new_data))

def main(argv):
    file_name = ''

    try:
        opts, _ = getopt.getopt(argv, 'f:', ['--source-file'])
    except getopt.GetoptError:
        print('process_data.py -f <file>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-f', '--source-file'):
            file_name = arg

    if not file_name:
        print('must supply filename!')
        sys.exit(2)

    data = load_json_file(arg)['tweets']
    cleaned_tweets = clean_tweets(data)
    lower_cased_tweets = case_fold(cleaned_tweets)
    stemmed_tweets = stem(lower_cased_tweets)
    tokenized_tweets = tokenize(stemmed_tweets)
    
    print(tokenized_tweets)

main(sys.argv[1:])