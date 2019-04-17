import json
import sys
from pprint import pprint
import numpy as np
def load_data(filename):
    '''
    Loading the restructured json file of the dataset
    '''
    try:
        with open(filename,'r') as f:
            data = json.load(f)
        return data
    except :
            print("Error in opening " +filename +" file")
            sys.exit(0)
def load_glove_vector(dimension):
    '''
    Loading the Glove Vector for word embeddings
    '''
    if dimension not in [50,100,200,300]:
        dimension = 50
    filename = '../glove.6B.'+str(dimension)+'d.txt' 
    word_embeddings = {}
    try:
        f1 = open(filename,encoding='utf-8')
        for line in f1:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            word_embeddings[word] = coefs
        f1.close()
    except Exception as e:
        print("Error in loading Glove vectors\n")
        print(e)
        sys.exit(0)
    return word_embeddings

def engine():
    filename = 'q1.json'
    data = load_data(filename)
    word_embeddings = load_glove_vector(50)
engine()