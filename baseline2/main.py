#!/usr/bin/env python
# coding: utf-8

import json
import sys
import os
from pprint import pprint
import numpy as np
from get_similarity_old import similarity_engine
from select_answers import get_selected_answers
from summarize import summarize_query_ans
from restructureL import restructrure, loadFile

def load_data(filename):
	'''
	Loading the restructured json file of the dataset.
	'''
	try:
		with open(filename,'r') as f:
			data = json.load(f)
		return data
	except:
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
	dir_path = os.getcwd()
	name = filename.split('/')[-1]
	name = name.split('.')[0]
	print(name)

	try:
		os.mkdir(dir_path + '/' + 'jsonFiles/' + name)
	except:
		pass

	newDir = dir_path + '/' + 'jsonFiles/' + name + '/'

	new_name = name + "_" + extension + '.json'
	# print(new_name)
	with open(newDir+new_name,'w') as f:
		json.dump(data,f)
	return new_name

def engine():
	'''
	Main function that runs the code.
	'''
	filename = sys.argv[1]
	data = loadFile(filename)
	dataLis, data = restructrure(data)
	save_data(data, "after_restructuring", filename)
	# data = load_data(filename)
	print("Data loading and Restructuring Complete")
	data = similarity_engine(data)
	print("Similarity calculation Complete")
	filename_with_simi = save_data(data,"after_similarity",filename)
	print("Similarity file saved")
	data = get_selected_answers(data)
	print("Selecting answer completed")
	filename_with_selected_ans = save_data(data,"after_selected_answer",filename)
	print("Answer file saved")
	data = summarize_query_ans(data)
	# pprint(data)
	filename_with_summary = save_data(data,"after_summary",filename)

if __name__ == '__main__':
	engine()