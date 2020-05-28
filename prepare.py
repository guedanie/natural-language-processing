import unicodedata
import re
import json

import nltk
# nltk.download('wordnet')
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd
from requests import get

import acquire
from bs4 import BeautifulSoup
import re

# ---------------- #
#     Prepare      #
# ---------------- #

def basic_clean(text):
    '''
    Helper function that lower_cases the text, removes any special characters or accents
    '''
    article = text.lower()
    article = unicodedata.normalize('NFKD', article)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    article = re.sub(r"[^a-z0-9'\s]", '', article)
    return article 

def tokenize(basic_clean_text):
    '''
    Helper function that tokenizes the data
    '''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    article = tokenizer.tokenize(basic_clean_text, return_str=True)
    return article

def stem(tokenized_text):
    '''
    Helper function that accepts some text and return the text after applying stemming to all words. Also returns stems
    '''
    ps = nltk.stem.porter.PorterStemmer()
    stems = [ps.stem(word) for word in tokenized_text.split()]
    article_stemmed = ' '.join(stems)
    return stems, article_stemmed  

def lemmatize(tokenized_text):
    '''
    Helper function that accept some text and return the text after applying lemmatization to each word.

    '''
    wnl = nltk.stem.WordNetLemmatizer()

    lemmas = [wnl.lemmatize(word) for word in tokenized_text.split()]
    article_lemmatized = ' '.join(lemmas)
    return lemmas, article_lemmatized
    

def remove_stopwords(lemmatized_text):
    '''
    Helper function that accepts text, and retunrs that text after removing all the stopwords
    '''
    stopword_list = stopwords.words('english')
    stopword_list.remove('no')
    stopword_list.remove('not')
    
    words = lemmatized_text.split()
    filtered_words = [w for w in words if w not in stopword_list]
    article_without_stopwords = ' '.join(filtered_words)
    return article_without_stopwords

def prep_article(article, text_key):
    '''
    First main function that takes a single article, and returns an updated dictionary with all the prep done
    '''
    uncleaned_text = article[text_key]
    
    basic_clean_text = basic_clean(uncleaned_text)
    tokenized_text = tokenize(basic_clean_text)
    stems, stemmed_text = stem(tokenized_text)
    stem_lemmatize, lemmatized_text = lemmatize(tokenized_text)
    cleaned_text = remove_stopwords(lemmatized_text)
    
    article.update({"stemmed": stemmed_text, "lemmatized": lemmatized_text, "clean": cleaned_text})
    
    return article
    
# ____Main Prep Function____#

def prepare_article_data(articles):
    '''
    Main prep function that takes a list of dictionaries with content and returns the list, with updated dictionaries after data prep.
    '''
    for i in range(len(articles)):
         prep_article(articles[i], text_key = "content")
    return articles