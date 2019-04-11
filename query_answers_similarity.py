import numpy as np
import pandas as pd
import nltk
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import math
import json
import pprint

from restructureSingle import *



def remove_stopwords(sen):
	stop_words = stopwords.words('english')
	sen_new = " ".join([i for i in sen if i not in stop_words])
	return sen_new

word_embeddings = {}
f1 = open('../glove.6B/glove.6B.100d.txt', encoding='utf-8')
for line in f1:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f1.close()

def get_sentences(paragraph):
    sentences = []

    # print(paragraph)

    for s in paragraph:
        # print(s)
        # print(sent_tokenize(s))
        sentences.append(sent_tokenize(s))

    # print(len(sentences))

    sentences = [y for x in sentences for y in x]

    # print(sentences)
	
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
    # clean_sentences = pd.Series(sentences)
    clean_sentences = [s.lower() for s in clean_sentences]
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

    # word_embeddings = {}
    # f = open('../glove.6B/glove.6B.100d.txt', encoding='utf-8')
    # for line in f:
    #     values = line.split()
    #     word = values[0]
    #     coefs = np.asarray(values[1:], dtype='float32')
    #     word_embeddings[word] = coefs
    # f.close()

    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)

    # print(sentence_vectors)

    return sentences, sentence_vectors

def similarity(sentences_query, sentence_vec_query, answer):
    # sentences_query, sentence_vec_query = get_sentences([query])
    sentences_ans, sentence_vec_ans = get_sentences([answer])

    sim_mat = np.zeros([len(sentences_query), len(sentences_ans)])

    for i in range(len(sentences_query)):
        for j in range(len(sentences_ans)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(sentence_vec_query[i].reshape(1,100), sentence_vec_ans[j].reshape(1,100))[0,0]
    
    # print(sim_mat)

    return sim_mat

if __name__ == "__main__":
    myLis, myDict1 = get_data()

    newDict = {}

    f = open('out_complete_sim.json', 'w')

    it = 0

    for key, value in myDict1.items():
        myDict = myDict1[key]
        query = myDict['QBody']
        sentences_query, sentence_vec_query = get_sentences([query])
        simDict = {}
        for i in range(len(myDict['Ans'])):
            answer = myDict['Ans'][i]['GBody']
            sim = similarity(sentences_query, sentence_vec_query, answer)
            sim = np.array(sim)
            # print(sim, file=f)
            avg_sim = np.mean(sim)
            simDict[i] = avg_sim
            myDict['Ans'][i]['Similarity'] = avg_sim
            # myDict['Ans'][i]['Similarity'] = i

        # pprint.pprint(myDict)

        myDict1[key]['Ans'] = myDict['Ans']

        it += 1

        print("One query done\t iteration =", it)

        # if it==1:
        #     json_file = json.dumps(myDict1)
        #     f.write(json_file)

        # pprint.pprint(myDict1)

        # print(simDict, file=f)

    json_file = json.dumps(myDict1)

    f.write(json_file)

    f.close()