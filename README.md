# Query Based Question-Answering and Summarization

This is the project for **Query Based Question-Answering and Summarization**. We have used the StackExchange dataset of the topic of *Cooking*, which is present in the csv files:
- **query.csv** : Contains the complete dataset that we downloaded using a MySQL script
- **q1.csv** : Contains a subset of the complete dataset, which is used for testing purposes of individual code sections.

## Directory Structure
The main directory used in this project is the *baseline* directory, which contains all the main code which we have done till now.
The *tillnow* directory contains most of our testing codes.

The directory structure of the *baseline2* directory is as follows:
```
    Main Directory
    ├── baseline2
    │   ├── get_similarity_old.py
    │   ├── main.py
    │   ├── q1_after_selected_answer.json
    │   ├── q1_after_similarity.json
    │   ├── q1_after_summary.json
    │   ├── q1.json
    │   ├── query_full.json
    │   ├── readGlove.py
    │   ├── restructureL.py
    │   ├── select_answers.py
    │   └── summarize.py
    ├── q1.csv
    ├── query.csv
    ├── README.md
    └── tillnow
```

The different files in the **baseline2** directory and their functions are:
- *restructureL.py* : This file is used for restructuring the dataset, like removal of tags, getting a dictionary of all the queries with all their answers, and other fields.
- *readGlove.py* : This file is used for reading the glove vectors, that we are using for out word2vec model.
- *get_similarity_old.py* : This file has functions that are used to get the similarity between the query and the answers, and the answer to answer similarity. We are using the cosine similarity in this approach.
- *select_answers.py* : This file has the function to select the answers for summary generation using the parameters:
    - Upvotes corresponding to an answer
    - Answer to Query similarity, the higher this value the more chances of this answer to be selected
    - Answer to Answer similarity, in this, we are taking the similarity values of all that particular answer with all the other answers, and the lower this value, the higher the chances of the answer to be selected for the summary generation, because we don't want much duplicacy.

- *main.py* : This is the main file that compiles all the above functions and give us the summary corresponding to each and every question in the dataset.

## Glove Vector Used
We have used the Stanford glove6B vector (50d one).

The link to the glove vector file is : nlp.stanford.edu/data/glove.6B.zip

To load the glove vector, keep extract the zip just outside this main directory, and then just run the ```baseline2/main.py``` code file.