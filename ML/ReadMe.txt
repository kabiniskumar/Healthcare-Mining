All .sav files are pickle files of trained ML classifiers for our dataset (WebMd and Patients like me)

colnames_count is a text file with column names (symptoms) to compare against

get_result.py is the main file which will run all the three ML Models

It takes in 3 arguments (3 strings) and outputs a list of predicted diseases. 
Order of predicted diseases by classfiers [MNB,DD,MLP]