import numpy as np
import pandas as pd
import pprint
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models.keyedvectors import KeyedVectors

filename = '../glove.6B/glove.6B.50d.txt'

def read():
    # data = glove2word2vec(glove_input_file=filename, word2vec_output_file="gensim_glove_vectors.txt")
    # glove_model = KeyedVectors.load_word2vec_format("gensim_glove_vectors.txt", binary=False)
    # print(glove_model)
    glove = np.loadtxt(filename, dtype='str', comments=None)
    words = glove[:, 0]
    print(words)

read()