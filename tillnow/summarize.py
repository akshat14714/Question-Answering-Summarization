from nltk import sent_tokenize,corpus,word_tokenize
import re
import heapq
import math
def summarize(article_text):
    pass
    sentence_list = sent_tokenize(article_text)

    stopwords = corpus.stopwords.words('english')

    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  

    word_frequencies = {}  
    for word in word_tokenize(formatted_article_text):  
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}  
    for sent in sentence_list:  
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    # print()
    summary_sentences = heapq.nlargest(math.ceil(0.3 * float(len(sentence_list))), sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)  
    print(summary)

if __name__ == "__main__":
    article_text = "Summarizing is one of those skills that may seem very easy to a teacher but can be difficult for students who have not been properly taught how to summarize. For many years I did not even teach my seventh and eighth grade students how to summarize. I would just ask them to summarize texts and then get mad at them when they failed to produce quality summaries. I was wrong in doing this. Now I always teach my students how to write summaries.Writing a good summary is not as easy as it may appear. It actually requires quite a bit of finesse. First the student must read and comprehend the text. This may involve unpacking lengthy sentences and decoding challenging vocabulary. Then they must identify main ideas and key points, which means that they must have a good enough understanding of the text to distinguish between essential and nonessential information. Finally they must express this information in their own words. This means that summarizing a text requires both comprehension and expression skills. Additionally, as per the Common Core State Standards, summaries should not contain opinions, background knowledge, or personal information; rather, a summary should be entirely text based. After years of learning to make connections between the text and themselves, students must be retrained to keep themselves out of their writing in regards to summaries. Teaching this skill surely warrants some of your class time. Here are some resources that I used in my classroom to teach my students how to summarize. I hope that you find this page useful: Summarizing Lesson – Here is an animated PowerPoint slideshow teaching students how to summarize. It includes definitions, example paragraphs, and a simple review activity using nursery rhymes."
    summarize(article_text)