#!/usr/bin/env python
# coding: utf-8

import json
import sys
from pprint import pprint
import numpy as np
from get_similarity import similarity_engine



def load_data(filename):
    '''
    Loading the restructured json file of the dataset.
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
    Loading the Glove Vector for word embeddings.
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

def save_data(data,extension,filename):
    '''
    Function for exporting python dictionary to a json file
    '''
    new_name = filename.split('.')[0]+ "_" + extension + '.json'
    # print(new_name)
    with open(new_name,'w') as f:
        json.dump(data,f)
    return new_name
def engine():
    '''
    Main function that runs the code.
    '''
    filename = 'q1.json'
    data = load_data(filename)
    data = similarity_engine(data)
    filename = save_data(data,"after_similarity",filename)
if __name__ == '__main__':
    engine()