from gensim.summarization.summarizer import summarize
from pprint import pprint
# from select_answers import *

def summarize_query_ans(myDict):
    for ques in myDict:
        text = ''
        for ans in myDict[ques]['Ans']:
            if ans['selected']:
                text += ans['GBody']

        summary = summarize(text)

        myDict[ques]['summary'] = summary

    # pprint(myDict)
    return myDict
# data = load_data('q1_after_similarity.json')
# summarize_query_ans(data)