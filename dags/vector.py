import pandas as pd
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

class Vector:
  def __init__(self, ID, res_str, resume_words):
    self.resume_id = ID
    self.resume_str = res_str
    self.resume_words = resume_words

    self.classification = {
    'category': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'experience': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'education': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'skills': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    self.colomns = ['HR', 'Designer', 'Information-Technology', 'Teacher', 'Advocate', 'Business-Development', 'Healthcare', 'Fitness', 'Agriculture', 'BPO', 'Sales', 'Consultant', 'Digital-Media', 'Automobile', 'Chef', 'Finance', 'Apparel', 'Engineering', 'Accountant', 'Construction', 'Public-Relations', 'Banking', 'Arts', 'Aviation']
    self.cv_vector = []
    self.ids = [0, 0, 0]

  def vector_from_cv(self, model):
    v = []
    #for i in self.resume_words:
    #  v.append(model.wv[i])
    self.cv_vector = model.wv.get_mean_vector(self.resume_words, post_normalize=True, ignore_missing=True)

  def separation(self, model):
    experience = model.wv['experience']
    education = model.wv['education']
    skills = model.wv['skills']
    p_education = 1.0
    p_experience = 1.0
    p_skills = 1.0
    for i in range(len(self.resume_words)):
      #print(self.resume_words[i])
      if (spatial.distance.cosine(model.wv[self.resume_words[i]], experience)) < p_experience:
        p_experience = spatial.distance.cosine(model.wv[self.resume_words[i]], experience)
        self.ids[0] = i
      if (spatial.distance.cosine(model.wv[self.resume_words[i]], education)) < p_education:
        p_education = spatial.distance.cosine(model.wv[self.resume_words[i]], education)
        self.ids[1] = i
      if (spatial.distance.cosine(model.wv[self.resume_words[i]], skills)) < p_skills:
        p_skills = spatial.distance.cosine(model.wv[self.resume_words[i]], skills)
        self.ids[2] = i
    print(self.ids)
    print(self.resume_words[self.ids[0]])
    print(self.resume_words[self.ids[1]])
    print(self.resume_words[self.ids[2]])

  def experience_vector(self):

    pass

  def education_vector(self):

    pass

  def skills_vector(self):

    pass