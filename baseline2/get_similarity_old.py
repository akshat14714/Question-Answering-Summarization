import sys
import numpy as np
import pandas as pd
import nltk
import re
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
# import networkx as nx
import math
import json
import pprint
dimension = 50

def remove_stopwords(sen):
    stop_words = stopwords.words('english')
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

def get_sentences(paragraph,word_embeddings):
    sentences = []

    for s in paragraph:
        sentences.append(sent_tokenize(s))

    sentences = [y for x in sentences for y in x]

    clean_sentences = pd.Series(sentences).astype(str).str.replace("[^a-zA-Z]", " ")
    clean_sentences = [s.lower() for s in clean_sentences]
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

    sentence_vectors = []
    for i in clean_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((dimension,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((dimension,))
        sentence_vectors.append(v)
    return sentences, sentence_vectors

def remove_tag(inp):
    all_tags = ['<p>', '<a>', '<b>', '<blockquote>', '<code>', '<del>', '<dd>', '<dl>', '<dt>', '<em>', '<h1>', '<h2>', '<h3>', '<i>', '<img>', '<kbd>', '<li>', '<ol>', '<p>', '<pre>', '<s>', '<sup>', '<sub>', '<strong>', '<strike>', '<ul>', '<br>', '<hr>']
    all_tags2 = ['</p>', '</a>', '</b>', '</blockquote>', '</code>', '</del>', '</dd>', '</dl>', '</dt>', '</em>', '</h1>', '</h2>', '</h3>', '</i>', '</img>', '</kbd>', '</li>', '</ol>', '</p>', '</pre>', '</s>', '</sup>', '</sub>', '</strong>', '</strike>', '</ul>', '</br>', '</hr>']
    for tag in all_tags:
        inp = inp.replace(tag, '')
    for tag in all_tags2:
        inp = inp.replace(tag, '')
    # ans.append(arr)
    return inp

def load_glove_vector(dimension):
    '''
    Loading the Glove Vector for word embeddings
    '''
    if dimension not in [50,100,200,300]:
        dimension = 50
    filename = '../../glove.6B/glove.6B.'+str(dimension)+'d.txt' 
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

def similarity(sentences_query, sentence_vec_query, sentences_ans, sentence_vec_ans,word_embeddings):
    sim_mat = np.zeros([len(sentences_query), len(sentences_ans)])

    for i in range(len(sentences_query)):
        for j in range(len(sentences_ans)):
            sim_mat[i][j] = cosine_similarity(sentence_vec_query[i].reshape(1,dimension), sentence_vec_ans[j].reshape(1,dimension))[0,0]
    
    return sim_mat

def similarity_engine(data):
    '''
    Main Engine for getting the similarity of the sentences and queries
    '''
    word_embeddings = load_glove_vector(dimension)
    for ques_id in data:
        query = remove_tag(data[ques_id]['QBody'])
        # print(query)
        sentences_query, sentence_vec_query = get_sentences([query],word_embeddings)
        sentences_ans = []
        sentences_vec_ans = []
        for i in range(len(data[ques_id]['Ans'])):
            answer = data[ques_id]['Ans'][i]['GBody']
            temp_ans, temp_vec_ans = get_sentences([answer],word_embeddings)
            sentences_ans.append(temp_ans)
            sentences_vec_ans.append(temp_vec_ans)
        for i in range(len(data[ques_id]['Ans'])):
            sim = similarity(sentences_query,sentence_vec_query,sentences_ans[i], sentences_vec_ans[i],word_embeddings)
            avg_sim = np.mean(sim)
            data[ques_id]['Ans'][i]['answer_query_sim'] = avg_sim
        for i in range(len(data[ques_id]['Ans'])):
            cur_sim = []
            for j in range(len(data[ques_id]['Ans'])):
                if i!=j:
                    sim = similarity(sentences_ans[i], sentences_vec_ans[i],sentences_ans[j], sentences_vec_ans[j],word_embeddings)
                    # print(i,j)
                    # print(sim.shape)
                    # print(sim)
                    # print("\n\n")
                    cur_sim.append(np.mean(sim))
            cur_sim = np.array(cur_sim)
            data[ques_id]['Ans'][i]['answer_answer_sim'] = np.mean(cur_sim)
            # print(cur_sim.shape)
            # print(cur_sim)
            # print("\n\n")
    # pprint.pprint(data)
    return data