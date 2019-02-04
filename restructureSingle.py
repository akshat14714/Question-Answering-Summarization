import pandas as pd
import numpy as np

def loadFile(filename):
    csv_read = pd.read_csv(filename)
    return csv_read
    # print(csv_read)

def restructrure(dataFrame):
    myLis = list()
    dataFrame = dataFrame.sort_values(by = ['QId'])
    for _, row in dataFrame.iterrows():
        if not any(d['QId']==row['QId'] for d in myLis):
            dict = {'QId':row['QId'], 'QTitle':row['QTitle'], 'QBody':row['QBody'], 'Ans':[{'GId':row['GId'], 'GBody':row['GBody'], 'GScore':row['GScore']}], 'QTags':row['QTags']}
            myLis.append(dict)
        else:
            for elem in myLis:
                if elem['QId']==row['QId']:
                    elem['Ans'].append({'GId':row['GId'], 'GBody':row['GBody'], 'GScore':row['GScore']})
                    break

        # print(myLis)
    
    return myLis

df = loadFile('QueryResultsCookingG5.csv')
myLis = restructrure(df)
print(myLis)