import logging
import pandas as pd
from random import random
import pika

from vector import Vector
import bs4 as bs
import urllib.request
import re
import nltk
import gensim
from nltk.corpus import stopwords

from gensim.utils import simple_preprocess
from gensim import corpora
from multiprocessing import cpu_count

from gensim.models.word2vec import Word2Vec

logging.basicConfig(level=logging.INFO)


def preprocessing(**context):
    a = 1

    logging.info(f"The value of a is {a}")

    context["ti"].xcom_push(key="some_key", value=a)


def core_nlp(**context):
    a = context["ti"].xcom_pull(key="some_key")

    logging.info(f"The value of a is {a}")

    context["ti"].xcom_push(key="some_key", value=a)


def postprocessing(**context):
    logging.info('Started score calculation')
    df = pd.read_csv('data/Resume/Resume.csv')
    ids = [{'id': rid, 'score': random()} for rid in df['ID'].to_list()]
    ids.sort(key=lambda r: r['score'], reverse=True)
    context["ti"].xcom_push(key="cvs", value=ids)

def vectorization(**context):
    resumes = context['resumes'].xcom_pull(key="vector_key")

    all_words_vocabulary = []
    resume_list = []

    for i in range(len(resumes)):
        processed_article = resumes[i].lower()
        processed_article = ''.join(e for e in processed_article if e.isalnum() or e == ' ')

        all_words = simple_preprocess(processed_article, deacc = True)
        #all_words = [w for w in all_words if w not in stopwords.words('english')]

        resume_list.append(Vector(ID[i], resumes[i], all_words))
        all_words_vocabulary.append(all_words)

    word2vec = Word2Vec(all_words_vocabulary, min_count=0, workers=cpu_count())
    vocabulary = corpora.Dictionary(all_words_vocabulary)

    for resume in resume_list:
        resume.vector_from_cv(word2vec)
        resume.separation(word2vec)

    context["resumes"].xcom_push(key="vector_key", value=resume_list)