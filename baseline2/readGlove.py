from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

glove2word2vec('../../glove.6B/glove.6B.300d.txt', 'glove_model.txt')

model = KeyedVectors.load_word2vec_format('glove_model.txt')