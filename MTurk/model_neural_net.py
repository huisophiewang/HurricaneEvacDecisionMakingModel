import os
from pprint import pprint
from sklearn import neural_network
from sklearn import preprocessing
from sklearn import model_selection
from sklearn import metrics
import numpy as np
import pandas as pd


# questions:
# which activation functions to choose
# how many hidden layers? how many nodes in each layer?
# weight initialization?
# learning rate?

def repeated_nested_kfold_cv(x, y, repeats):
    scaler = preprocessing.StandardScaler().fit(x)
    x = scaler.transform(x) 
 

    hid = [(i,)for i in range(1,62)]
    for i in range(1, 62):
        hid.extend([(n,i) for n in range(1, 62)])
    pprint(hid)
       

    scores = []
    for t in range(repeats):
        print '=========================================================='
        print 'Trial %d' % t
        outer_cv = model_selection.StratifiedKFold(n_splits=10, shuffle=True)
        for fold, (train_idx, test_idx) in enumerate(outer_cv.split(x, y)):
            print '-----------------------------------'
            print 'Fold %d' % fold
            #print test_idx
            x_train, x_test = x[train_idx], x[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            # inner cv, tune hyper parameters
            inner_cv = model_selection.StratifiedKFold(n_splits=10, shuffle=True)
            inner_cv.split(x_train, y_train)
            search_param = model_selection.GridSearchCV(estimator = neural_network.MLPClassifier(solver='lbfgs', random_state=0), 
                                                        param_grid = {'hidden_layer_sizes':hid}, 
                                                        scoring='f1_micro', 
                                                        cv=10)
            search_param.fit(x_train, y_train)
            print search_param.best_params_
            clf = search_param.best_estimator_
            
            y_predict = clf.predict(x_test)
            fscore = metrics.f1_score(y_test, y_predict, average='micro')
            print fscore
            scores.append(fscore)
        
    print "Score : Mean - %.7g | Std - %.7g | Min - %.7g | Max - %.7g" % (np.mean(scores),np.std(scores),np.min(scores),np.max(scores))

def test_param(x, y, features):
    hid = [(i, )for i in range(1,62)]
    for i in range(1, 20):
        hid.extend([(n,i) for n in range(1, 62, 2)])
    pprint(hid)
    search_param = model_selection.GridSearchCV(estimator = neural_network.MLPClassifier(solver='lbfgs', random_state=0, activation='logistic'), 
                                                param_grid = {'hidden_layer_sizes':hid}, 
                                                scoring='f1_micro', 
                                                cv=10)
    search_param.fit(x,y)
    pprint(search_param.grid_scores_)
    print search_param.best_params_
    print search_param.best_score_

    
def view_coef(x, y, features):
    scaler = preprocessing.StandardScaler().fit(x)
    x = scaler.transform(x) 
    clf = neural_network.MLPClassifier(solver='lbfgs', hidden_layer_sizes=(5,1), random_state=1)
    clf.fit(x, y)   
    y_predict = clf.predict(x)
    fscore = metrics.f1_score(y, y_predict, average='micro')
    print fscore
    print clf.n_layers_
    print clf.n_outputs_
    print clf.out_activation_
    for j, coef in enumerate(clf.coefs_):
        print '-------------------------'
        for i, row in enumerate(coef):
            if j == 0:
                print features[i]
            print row
            print 
    


if __name__ == '__main__':
    fp = os.path.join('data', 'MTurk_Harvey_v1.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    df = pd.read_csv(fp)
    features = list(df)[:-1]
    x = data[:,:-1]
    y = data[:,-1]
    
    repeats = 1
    #repeated_nested_kfold_cv(x, y, repeats)
    
    test_param(x, y, features)
    
