import json
import threading
import torch
from typing import List, Tuple

import gensim
import string
import numpy as np
from sentence_transformers import SentenceTransformer

# check model name at official Transformers website:
# https://www.sbert.net/docs/pretrained_models.html
model = SentenceTransformer('all-mpnet-base-v2')

# Google's Word2Vec model. Kaggle download:
# https://www.kaggle.com/datasets/umbertogriffo/googles-trained-word2vec-model-in-python
# model = gensim.models.KeyedVectors.load_word2vec_format('models/GoogleNews-vectors-negative300.bin', binary=True)

translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))


class Vector:
    def __init__(self, res_id: int, res_str: str, do_preprocess: bool = True):
        self.resume_id = res_id
        self.resume_str = res_str
        self.cv_vector = []
        if do_preprocess:
            self.preprocess()

    @staticmethod
    def __get_sentence_embedding(sentence: str) -> list or None:
        global cv
        def bert_encode(sentence, tmp):
            global cv
            count = len(sentence)//8
            start = tmp * count
            end = len(sentence) if tmp==7 else (tmp + 1)*count
            a = model.encode([sentence[start:end]])[0] if sentence else None
            cv = cv + a if len(cv)!=0 else a
            return a
        
        sentence = sentence.translate(translator)
        threads = []
        if isinstance(model, SentenceTransformer):
            for i in range(8):
                thread = threading.Thread(target=bert_encode, args=(sentence, i, ))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
            self.cv_vector = cv
            print(self.cv_vector)
        elif isinstance(model, gensim.models.keyedvectors.KeyedVectors):
            words = sentence.split()
            self.cv_vector = model.get_mean_vector(words, ignore_missing=True, post_normalize=False) if words else None
            return 
        else:
            raise NotImplementedError('Non-gensim and non-bert models are not supported')

    @staticmethod
    def __get_words_embedding(sentence: str) -> Tuple[List[str], List]:
        words = sentence.translate(translator).split()
        if isinstance(model, SentenceTransformer):
            word_embeddings = model.encode(words)
            return words, word_embeddings
        elif isinstance(model, gensim.models.keyedvectors.KeyedVectors):
            word_embeddings = []
            for word in words:
                word_embeddings.append(model[word] if (model.key_to_index.get(word, None) is not None) else None)
            return words, word_embeddings
        else:
            raise NotImplementedError('Non-gensim and non-bert models are not supported')
    
    @staticmethod
    def __get_word_embedding(word: str):
        return Vector.__get_words_embedding(word)[1][0]

    def preprocess(self):
        self.__get_sentence_embedding(self.resume_str)
        
    def get_words_embeddings(self) -> Tuple[List[str], List]:
        return self.__get_words_embedding(self.resume_str)

    def to_dict(self) -> dict:
        as_dict = self.__dict__
        if isinstance(as_dict['cv_vector'], list):
            return as_dict
        as_dict['cv_vector'] = as_dict['cv_vector'].tolist()
        return as_dict

    @staticmethod
    def from_dict(**kwargs):
        vec = Vector(kwargs['resume_id'], kwargs['resume_str'])
        vec.cv_vector = np.array(kwargs['cv_vector'])
        return vec

    @staticmethod
    def parse_iterative(*args) -> list:
        return [Vector.from_dict(**val) for val in args[0]]

    def category_split(self):  # TODO: split text into (skills, education & work experience)
        pass

    def get_cv_vector(self):

        return [self.resume_id, self.cv_vector.tolist()]

    def to_json(self):
        return json.dumps(self.get_cv_vector())
