import pandas as pd
import numpy as np
import pprint
def loadFile(filename):
    csv_read = pd.read_csv(filename)
    return csv_read
    # print(csv_read)

def restructrure(dataFrame):
    myLis = []
    data = dataFrame.to_dict(orient='records')
    prevId = '-1'
    temp = {}
    for row in data:
        if row['QId'] != prevId:
            prevId = row['QId']
            if temp!= {}:
                myLis.append(temp)
            temp = {'QId':row['QId'], 'QTitle':row['QTitle'], 'QBody':row['QBody'], 'Ans':[{'GId':row['GId'], 'GBody':row['GBody'], 'GScore':row['GScore']}], 'QTags':row['QTags']}
        else:
            temp['Ans'].append({'GId':row['GId'], 'GBody':row['GBody'], 'GScore':row['GScore']})
    if temp!= {}:
                myLis.append(temp)
    return myLis

def get_data():
    df = loadFile('q1.csv')
    myLis = restructrure(df)
    return myLis
# pprint.pprint(myLis)