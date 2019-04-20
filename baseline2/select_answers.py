import nltk
import numpy as np
import json
import pprint
import sys
def select_ans(entry):
    ans = []
    mean = float(np.mean(entry))
    std  = float(np.std(entry))
    for val in entry:
        if float(val) >= mean + std:
            ans.append(1)
        else:
            ans.append(0)
    return ans

def get_score(a, b, c):
    return a/3 + b/3 - c/3

def get_selected_answers(data):
    for ques in data:
        score_Lis = []
        for ans in data[ques]['Ans']:
            score = get_score(ans['GScore'], ans['answer_query_sim'], ans['answer_answer_sim'])
            score_Lis.append(score)
        
        result = select_ans(score_Lis)

        i = 0

        for ans in data[ques]['Ans']:
            ans['selected'] = result[i]
            i += 1

    # pprint.pprint(data)
    return data

# def load_data(filename):
#     '''
#     Loading the restructured json file of the dataset.
#     '''
#     try:
#         with open(filename,'r') as f:
#             data = json.load(f)
#         return data
#     except :
#             print("Error in opening " +filename +" file")
#             sys.exit(0)

# data = load_data('q1_after_similarity.json')
# fin = get_selected_answers(data)