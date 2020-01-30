import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler  
from sklearn import metrics
from sklearn import model_selection
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from pprint import pprint

def evaluate(model, x, y):
    model.fit(x, y)
    y_predict = model.predict(x)
    acc = metrics.accuracy_score(y, y_predict)
    print "Accuracy (Train): %f" % acc
    f1 = metrics.f1_score(y, y_predict)
    print "F1 score (Train): %f" % f1
    cv_acc = model_selection.cross_val_score(model, x, y, cv=10, scoring='accuracy')
    print "Accuracy (CV): Mean - %.7g | Std - %.7g " % (np.mean(cv_acc),np.std(cv_acc))

#def tune():

if __name__ == '__main__':
    fp = 'data/Ivan_common.csv'
    #fp = 'data/Ivan_common_with_county.csv'
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:,:-1]
    y = data[:,-1]
    
    scaler = StandardScaler()  
    scaler.fit(x)  
    x = scaler.transform(x) 
    
#     clf = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(1,1), random_state=0)
#     evaluate(clf, x, y)
    
    all_layers = []
    for i in range(1, 11):
        print i
        all_layers.extend([(n,i) for n in range(1, 49, 3)])
    pprint(all_layers)
      
    param_test1 = {'hidden_layer_sizes':all_layers}
    gsearch1 = GridSearchCV(estimator = MLPClassifier(solver='lbfgs', random_state=0), 
                            param_grid = param_test1, scoring='accuracy',cv=10, n_jobs=4)
    gsearch1.fit(x,y)
    pprint(gsearch1.grid_scores_)
    print gsearch1.best_params_
    print gsearch1.best_score_
    
