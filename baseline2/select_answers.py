import nltk
import numpy as np
import json
import pprint
import sys
from sklearn.preprocessing import StandardScaler as StdScaler

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
    return 2*a/3 + 2*b/3 - c/3

def get_normalized_upvotes(data):
    for ques in data:
        gscore_lis = []
        for ans in data[ques]['Ans']:
            gscore_lis.append(ans['GScore'])
        gscore_lis = np.array(gscore_lis).reshape(-1,1)
        scaler = StdScaler()
        temp = scaler.fit_transform(gscore_lis)
        print(temp.shape)
        temp = temp.flatten()
        # gscore_lis = np.interp(gscore_lis, (min(gscore_lis), max(gscore_lis), (-1, +1))
        print(temp)
        i = 0

        for ans in data[ques]['Ans']:
            ans['gscore_norm'] = temp[i]
            i += 1

    return data

def get_selected_answers(data):
    data = get_normalized_upvotes(data)

    for ques in data:
        score_Lis = []
        for ans in data[ques]['Ans']:
            score = get_score(ans['gscore_norm'], ans['answer_query_sim'], ans['answer_answer_sim'])
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