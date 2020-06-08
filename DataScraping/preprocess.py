from csv import DictReader
import csv
import pandas as pd

fields = ['PostNumber', 'DiseaseID', 'Disease', 'SymIDs', 'Symptoms']
init = True
out = {'PostNumber': None, 'DiseaseIDs': [], 'Diseases': [], 'SymIDs': [], 'Symptoms': []}
prev = None
curr = None
ignore = set(["C3280240", "C0012634", "C4522181", "C2676739", "C3542022", "C3542022", "C0272285","C0003123", "C0004135",
              "C0080151", "C0009450", "C0796085", "C3887938", "C1856053", "C0342895", "C0039082", "C0043168", "C0024633" , "C0036494"])

metamap = ""
output = ""


with open('InputsMayo/mayo_ascii.csv11.csv', encoding="utf8") as ip_file:
    reader = csv.reader(ip_file)
    threads = list(reader)


with open('Mayo_Output_Preprocessed/mayo_ascii.csv11.csv', mode='w', newline='', encoding="utf8") as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    with open('OutputsMayo/mayo_ascii.csv11.csv') as read_obj:
        csv_reader = DictReader(read_obj)
        for row in csv_reader:

            curr = row['PostNumber']
            if init:
                writer.writerow(['PostNumber', 'DiseaseID', 'Disease', 'SymptomIDs', 'Symptoms', 'ThreadLink', 'ThreadHeading', 'ThreadContent'])
                init = False
            else:
                curr = row['PostNumber']
                if curr != prev:
                    out['PostNumber'] = prev
                    # writer.writerow(out)
                    if out['DiseaseIDs'] and out['SymIDs']:
                        for i in range(len(out['DiseaseIDs'])):
                            # Get Thread details from threads
                            idx = int(prev)
                            threadLink = threads[idx][1]
                            threadHeading = threads[idx][2]
                            threadContent = threads[idx][3]
                            if out['DiseaseIDs'][i] not in ignore:
                                writer.writerow([prev, out['DiseaseIDs'][i], out['Diseases'][i], ", ".join(out['SymIDs']), ", ".join(out['Symptoms']), threadLink, threadHeading, threadContent])
                    out = {'PostNumber': None, 'DiseaseIDs': [], 'Diseases': [], 'SymIDs': [], 'Symptoms': []}

            if row['DiseaseId']:
                out['Diseases'].append(row['DiseaseName'])
                out['DiseaseIDs'].append(row['DiseaseId'])
            if row['SymptomId']:
                out['SymIDs'].append(row['SymptomId'])
                out['Symptoms'].append(row['SymptomName'])


            prev = curr

    # Write the final record
    if out['DiseaseIDs'] and out['SymIDs']:
        for i in range(len(out['DiseaseIDs'])):
            # Get Thread details from threads
            idx = int(prev)
            threadLink = threads[idx][1]
            threadHeading = threads[idx][2]
            threadContent = threads[idx][3]
            if out['DiseaseIDs'][i] not in ignore:
                writer.writerow(
                [prev, out['DiseaseIDs'][i], out['Diseases'][i], ", ".join(out['SymIDs']), ", ".join(out['Symptoms']),
                 threadLink, threadHeading, threadContent])