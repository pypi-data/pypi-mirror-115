# coding: utf-8
"""
Copyright (c) 2020 The MITRE Corporation.
"""


import io
import os
import json
from sklearn.datasets import dump_svmlight_file
import numpy as np


class PreProcessor(object):

    def __init__(self, vectorizer, encoding='utf-8'):
        self.vectorizer = vectorizer
        self.vocab = None

    def fit_transform(self, data):
        X = self.vectorizer.fit_transform(data)
        if isinstance(self.vectorizer, JsonVectorizer):
            self.vocab = self.vectorizer.vocab
        else:
            vocab = {v: 1 for v in self.vectorizer.vocabulary_}
            self.vocab = nlp.Vocab(vocab, unknown_token=None, padding_token=None, bos_token=None, eos_token=None)
        return X

    def transform(self, data):
        return self.vectorizer.transform(data)

    def transform_to_file(self, data, sp_vec_file):
        if isinstance(self.vectorizer, JsonVectorizer):
            self.vectorizer.get_sparse_vecs(sp_vec_file, None, data)
        else:
            X = self.transform(data)
            y = np.zeros(X.shape[0])
            dump_svmlight_file(X, y, sp_vec_file)

    
	


	
