import pandas as pd
import csv
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
import pickle


def run_TF_IDF(a, b, c):
    infile = open("../backend/dis_sym_matrix", "rb")
    sym_mat = pickle.load(infile)

    infile1 = open("../backend/dis_index", "rb")
    diseases_li = pickle.load(infile1)

    infile2 = open("../backend/sym_index", "rb")
    sym = pickle.load(infile2)

    query = np.zeros(len(sym))
    # query_sym = ["Fever", "Headache", "Pain"]
    query_sym = [a, b, c]
    for each in query_sym:
      query[sym[each.lower()]] = 1

    # Compute matching score

    doc_wt = np.zeros(len(sym_mat))
    sym_q = []

    for i in range(len(sym_mat)):
      data = sym_mat[i]
      for each in query_sym:
        idx = sym[each.lower()]
        if sym_mat[i][idx] >0 :
          doc_wt[i] += sym_mat[i][idx]

    r = doc_wt.argsort()[::-1][:10]
    results = []
    for each in r:
        print(diseases_li[each])
        results.append(diseases_li[each])

    return results


# def run_TF_IDF(a, b, c):
#     with open("../data/SWM.csv") as csv_file:
#         reader = csv.reader(csv_file)
#         data = list(reader)
#
#     diseases = set()
#     symptoms = set()
#     for i in range(1, len(data)):
#         post = data[i]
#         diseases.add(post[2])
#         for item in post[4].split(","):
#             symptoms.add(item.lower().strip())
#
#
#     sym_mat = np.zeros((len(diseases), len(symptoms)))
#     diseases_li = list(diseases)
#     symptoms_li = list(symptoms)
#     dis = {k: v for v, k in enumerate(diseases_li)}
#     sym = {k: v for v, k in enumerate(symptoms_li)}
#
#     # Generate disease-symptom matrix
#     for i in range(1, len(data)):
#       post = data[i]
#
#       disease = post[2]
#       symp = post[4].split(",")
#
#       d_id = dis[disease]
#       for each in symp:
#         s_id = sym[each.strip().lower()]
#         sym_mat[d_id][s_id] += 1
#
#     query = np.zeros(len(symptoms))
#     # query_sym = ["Neuralgia", "Headache","Abdominal bloating"]
#     # query_sym = ["Fever", "Influenza-like symptoms", "Headache"]
#     # query_sym = [ "Sore to touch", "Exanthema"]
#     # query_sym = [ "Pelvic Pain", "Fatigue", "Abdominal bloating"]
#     # query_sym = ["Rhinorrhea", "Diarrhea", "Coughing"]
#     # query_sym1 = [ "Fever", "Night sweats", "Sore Throat"] # -- good
#     # query_sym1 = ["Seizures", "Constipation", "Back Pain", "Fatigue", "Vomiting"] #-- good
#     # query_sym = ["abdominal skin striae", "abdominal pain", "abdominal discomfort"]
#     query_sym = [a.lower(), b.lower(), c.lower()]
#
#     for each in query_sym:
#         # print(each)
#         # print(sym[each])
#         query[sym[each]] = 1
#
#     tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
#     tfidf_transformer.fit(sym_mat)
#
#     op=tfidf_transformer.transform(sym_mat)
#     op_final = op.toarray()
#     # print(op_final.shape)
#     #
#     # outfile = open("dis_sym_matrix",'wb')
#     # pickle.dump(sym_mat, outfile)
#     # outfile.close()
#     #
#     # outfile1 = open("dis_index", "wb")
#     # pickle.dump(diseases_li, outfile1)
#     # outfile1.close()
#
#
#
#     infile = open("dis_sym_matrix","rb")
#     sym_mat = pickle.load(infile)
#
#     infile1 = open("dis_index", "rb")
#     disease_li = pickle.load(infile1)
#
#
#     # Compute matching score
#
#     doc_wt = np.zeros(len(sym_mat))
#
#     for i in range(len(sym_mat)):
#       data = sym_mat[i]
#       for each in query_sym:
#         idx = sym[each]
#         if sym_mat[i][idx] >0 :
#           doc_wt[i] += sym_mat[i][idx]
#
#     r = doc_wt.argsort()[::-1][:10]
#     result = []
#     for each in r:
#         print(disease_li[each])
#         result.append(disease_li[each])
#
#     return result

# print(run_TF_IDF("Fever", "Night sweats", "Sore Throat"))
# print(run_TF_IDF("Abdominal skin striae", "Abdominal pain", "Abdominal discomfort"))
