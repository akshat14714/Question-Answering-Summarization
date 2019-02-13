from select_answers import *
from restructureSingle import *
import nltk
from collections import Counter

def break_paragraph(paragraph):
    return nltk.tokenize.sent_tokenize(paragraph)

def break_sentences(sentence):
    words = sentence.split(' ')
    return Counter(words)


# def get_score(sentence):


def final():
    data = engine()
    print(len(data))
    for ques in data:
        breaks = []
        for elem in ques['selected_ans']:
            scores = []
            sentences = break_paragraph(elem['GBody'])
            breaks.append(sentences)

if __name__ == "__main__":
    final()