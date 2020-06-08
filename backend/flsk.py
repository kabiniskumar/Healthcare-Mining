'''
  @author simransingh
'''

from flask import request, redirect
from flask import Flask, render_template
import os
import callSolr
from ML.models import run_ML_Models
from ML.tfidf import run_TF_IDF
import models



template_dir = os.path.abspath('../frontend')
app = Flask(__name__, template_folder=template_dir)


print(template_dir)
@app.route("/")
def index():
    return render_template("del.html")

@app.route('/search', methods=['POST'])
def search():

    if 'ml' in request.form:
        isML = True
    else:
        isML = False
        if 'tfidf' in request.form:
            isTFIDF = True
        else:
            isTFIDF = False


    first = request.form['firstSymptom']
    second = request.form['secondSymptom']
    third = request.form['thirdSymptom']
    print("The symptoms are:")
    print(first)
    print(second)
    print(third)
    print("App")

    if isML == True:
        first = first[0].upper() + first[1:]
        second = second[0].upper() + second[1:]
        third = third[0].upper() + third[1:]
        listOfDisease = run_ML_Models(first, second, third)

    elif isTFIDF == True:
        listOfDisease = run_TF_IDF(first, second, third)
    else:
        listOfDisease = callSolr.search(first, second, third)

    print(listOfDisease)

    if len(listOfDisease) >= 3:
        #listofThreads = callSolr.getThreads(listOfDisease[0], listOfDisease[1], listOfDisease[2])
        listofThreads = callSolr.getThreads_v2(listOfDisease)
    else:
        return render_template("error.html")

    #listDisUsingML = models.run_ML_Models(first, second, third)

    return render_template("sample.html", list=listOfDisease, list2=listofThreads)

app.run(port=5000, debug=True)
