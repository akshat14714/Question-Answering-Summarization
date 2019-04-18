from select_answers import *
from restructureSingle import *
import nltk
from collections import Counter
from operator import itemgetter

def break_paragraph(paragraph):
    return nltk.tokenize.sent_tokenize(paragraph)

def break_sentences(sentence):
    words = sentence.split(' ')
    return Counter(words)

def get_avg_answers(data):
    ans = 0
    for ques in data:
        ans += len(ques['Ans'])
    return float(float(ans) / float(len(data)))

def get_avg_sentences(data):
    sentences = []
    for ques in data:
        sen = 0
        for elem in ques['Ans']:
            lis = break_paragraph(elem['GBody'])
            sen += len(lis)
        sentences.append(sen)
    sentences = np.array(sentences)
    return np.mean(sentences)

def get_Num_Ans(data):
    ans = []
    for ques in data:
        ans.append(len(ques['Ans']))
    counts = Counter(ans)
    counts = sorted(counts.items(), key=itemgetter(0))
    return counts

def final():
    data = engine()
    total_ques = len(data)
    print("Total Questions =",total_ques)
    avg_answers = get_avg_answers(data)
    print("Average Answers =",avg_answers)
    avg_sentences = get_avg_sentences(data)
    print("Average Sentences per Answer =", avg_sentences)
    diff_num_ans = get_Num_Ans(data)
    print("Different Number of Answers and their frequencies :", diff_num_ans)
    # for ques in data:
    #     breaks = []
    #     for elem in ques['selected_ans']:
    #         scores = []
    #         sentences = break_paragraph(elem['GBody'])
    #         breaks.append(sentences)

if __name__ == "__main__":
    final()