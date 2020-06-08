import pickle
import os
def run_ML_Models(a,b,c):
    inp = [a,b,c] 
    inp_ar=[]

    ml_direc = os.path.abspath('../ML')
    name = ml_direc + "/colnames_count.txt"
    print(name)
    with open (name, 'rb') as fp:
        itemlist = pickle.load(fp)
    for i in itemlist:
        if i in inp:
            inp_ar.append(1)
        else:
            inp_ar.append(0)
    result=[]
    dt_model_name = ml_direc + "/desicionc.sav"
    dt_model = pickle.load(open(dt_model_name, 'rb'))
    naive_model_name = ml_direc + "/naivec.sav"
    naive_model = pickle.load(open(naive_model_name, 'rb'))
    mlp_model_name =ml_direc + "/mlpc.sav"
    mlp_model = pickle.load(open(mlp_model_name,'rb'))
    result.append(list(naive_model.predict([inp_ar])))
    result.append(list(dt_model.predict([inp_ar])))
    result.append(list(mlp_model.predict([inp_ar])))

    res = []
    for lit in result:
        for elem in lit:
            res.append(elem)

    return res

# print( run_ML_Models("Fever", "Headache", "Pain"))
