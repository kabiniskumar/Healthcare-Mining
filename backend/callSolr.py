'''
  @author simransingh
'''

import requests
from bs4 import BeautifulSoup
import json
import cgi
import pickle
import random

threadBaseURL = "http://localhost:8983/solr/mycore/select?q=Disease%3A"
baseurl = "http://localhost:8983/solr/mycore/select?q=Symptom%3A"


def search(symptom1, symptom2, symptom3):

    if symptom1 is None or len(symptom1) == 0:
        print("First Symptom is Null!")
        exit()

    if symptom2 is None or len(symptom2) == 0:
        print("Second Symptom is Null!")
        exit()

    if symptom3 is None or len(symptom3) == 0:
        print("Third Symptom is Null!")
        exit()

    urls = getURLs(symptom1, symptom2, symptom3)
    masterListOfDiseases = []
    for url in urls:
        data = crawl(url)
        jsondata = "[" + data + "]"
        # print("json", jsondata)
        disease = getSpecificParameterFromData(jsondata, "Diseases")
        masterListOfDiseases.append(disease)

    # print("master", masterListOfDiseases)
    return findIntersection(masterListOfDiseases[0], masterListOfDiseases[1], masterListOfDiseases[2])

def findIntersection(list1, list2, list3):
    inter = [x for x in list1 if x in list2]
    if len(inter) == 0:
        if len(list1) < 10:
            return list1
        else:
            return list1[0:10]
    final = [x for x in list3 if x in inter]
    if len(final) == 0:
        if len(inter) < 10:
            return inter
        else:
            return inter[0:10]
    #getThreads(final[0], final[1], final[2])
    if len(final) < 10:
        return final
    else:
        return final[0:10]

def getThreads(disease1, disease2, disease3):
    urls = getThreadURLs(disease1, disease2, disease3)
    diseases = [disease1, disease2, disease3]
    list = []
    for i in range(0, len(urls)):
        tempMap = {}
        data = crawl(urls[i])
        jsondata = "[" + data + "]"
        print(jsondata)
        d = json.loads(jsondata)
        map = d[0]
        links = map["ThreadLinks"]
        tempMap["Disease"] = diseases[i]
        random.shuffle(links)
        tempMap["ThreadLinks"] = links[0:10]

        list.append(tempMap)
    # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    # print(list)
    return list

def getThreads_v2(diseases):
    with open('threads_all2.pickle', 'rb') as handle:
        diseasesMap = pickle.load(handle)
    out = []
    i = 0;
    for each in diseases:
        if each not in diseasesMap:
            continue
        tempMap = {}
        item = diseasesMap[each]
        tempMap["Disease"] = each
        tempMap["link"] = item["link"]
        tempMap["heading"] = item["heading"]
        tempMap["content"] = item["content"]
        print(item, each, item["link"])
        out.append(tempMap)
        i += 1
        if i == 3:
            break
    return out

def getThreadURLs(disease1, disease2, disease3):
    disease1 = disease1.replace(" ", "%20")
    disease2 = disease2.replace(" ", "%20")
    disease3 = disease3.replace(" ", "%20")
    firsturl, secondurl, thirdurl = threadBaseURL + disease1, threadBaseURL + disease2, threadBaseURL + disease3
    return [firsturl, secondurl, thirdurl]


def getSpecificParameterFromData(data, parameter):
    d = json.loads(data)
    map = d[0]
    diseases = map[parameter]
    return diseases


def crawl(url):
    page = requests.get(url)
    soup = str(BeautifulSoup(page.text, 'html.parser'))
    splitted = soup.split("docs")
    splitted1 = splitted[1]
    splitted2 = splitted1[3:splitted1.find("}") + 1]
    return splitted2


def getURLs(symptom1, symptom2, symptom3):
    symptom1 = symptom1.replace(" ", "%20")
    symptom2 = symptom2.replace(" ", "%20")
    symptom3 = symptom3.replace(" ", "%20")
    firsturl, secondurl, thirdurl = baseurl + symptom1, baseurl + symptom2, baseurl + symptom3
    return [firsturl, secondurl, thirdurl]


if __name__ == '__main__':
    form = cgi.FieldStorage()
    firstSymptom = form.getvalue('firstSymptom')
    secondSymptom = form.getvalue('secondSymptom')
    thirdSymptom = form.getvalue('thirdSymptom')
    print(firstSymptom, secondSymptom, thirdSymptom)
    print("Form")
    print(search(str(firstSymptom), str(secondSymptom), str(thirdSymptom)))