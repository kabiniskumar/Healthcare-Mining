'''
  @author simransingh
'''


import pandas as pd
from collections import OrderedDict
from csv import reader
import os
from operator import itemgetter
import json


def load_data():
    fileName = "../data/SWM.csv"
    data = pd.read_csv(fileName, index_col=None, header=0)
    makeIntialMap(data)
    getThreads(data)

#disease -> list of thread links
def getThreads(data):
    print("inside getThreads()")
    diseaseToThreadLinksMap = {}
    for index, row in data.iterrows():
        dis = row["Disease"]
        link = row["ThreadLink"]
        if dis in diseaseToThreadLinksMap:
            diseaseToThreadLinksMap[dis].append(link)
        else:
            diseaseToThreadLinksMap[dis] = [link]

        #diseaseToThreadLinksMap[dis] = diseaseToThreadLinksMap.get(dis,[]).append(link)

    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(len(diseaseToThreadLinksMap))

    l = []
    for k, v in diseaseToThreadLinksMap.items():
        tempMap = {}
        tempMap["Disease"] = k
        tempMap["ThreadLinks"] = v
        l.append(tempMap)

    jsonify(l, 'disToThreads.json')


def jsonify(list, name):
    print("inside jsonify()")
    print(len(list))

    with open(name, 'w') as fp:
        json.dump(list, fp)
    print("done json")

#symptom -> list of diseases
def makeIntialMap(data):
    symptomToListMap = {}
    for index, row in data.iterrows():
        syms = row["Symptoms"].split(", ")
        dis = row["Disease"].split(", ")
        for sym in syms:
            if sym in symptomToListMap:
                symptomToListMap[sym].extend(dis)
            else:
                list = []
                list.extend(dis)
                symptomToListMap[sym] = list

    print(len(symptomToListMap))

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(symptomToListMap)
    print(len(symptomToListMap))
    getSortedListOfDiseases(symptomToListMap)

def getSortedListOfDiseases(mp):
    list = []
    for k, v in mp.items():
        z = createFreqMap(v)
        tempMap = {}
        tempMap["Symptom"] = k
        tempMap["Diseases"] = z
        list.append(tempMap)

    print("######################################")
    print(list)

    jsonify(list, 'SymToDis.json')

def createFreqMap(list):
    mp = {}
    for elem in list:
        if elem in mp:
            mp[elem] += 1
        else:
            mp[elem] = 1

    dd = OrderedDict(sorted(mp.items(), key=lambda x: x[1], reverse=True))
    #dd = sorted(mp.items(), key=itemgetter(1), reverse=True)

    l = []
    for key in dd.keys():
        l.append(key)

    print(l)
    return l

if __name__ == '__main__':
    load_data()