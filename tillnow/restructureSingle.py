import pandas as pd
import numpy as np
import pprint
def loadFile(filename):
    csv_read = pd.read_csv(filename)
    return csv_read
    # print(csv_read)

def restructrure(dataFrame):
    myLis = []
    myDict = {}
    data = dataFrame.to_dict(orient='records')
    prevId = '-1'
    temp = {}
    for row in data:
        if row['QId'] not in myDict.keys():
            myDict[row['QId']] = {'QId':row['QId'], 'QTitle':row['QTitle'], 'QBody':row['QBody'], 'Ans':[{'GId':row['GId'], 'GBody':row['GBody'], 'GScore':row['GScore']}], 'QTags':row['QTags']}
        else:
            myDict[row['QId']]['Ans'].append({'GId':row['GId'], 'GBody':row['GBody'], 'GScore':row['GScore']})
    for key in myDict.keys():
        myLis.append(myDict[key])
    return myLis, myDict

def get_data():
    df = loadFile('query.csv')
    myLis, myDict = restructrure(df)
    return myLis, myDict
# pprint.pprint(myLis)

def get_specific_query():
    df = loadFile('q1.csv')
    myLis, myDict = restructrure(df)
    return myLis, myDict