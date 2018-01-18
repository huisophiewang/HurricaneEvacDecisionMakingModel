import os
from pprint import pprint
from sklearn import model_selection
from sklearn import metrics
from sklearn import ensemble
from sklearn import linear_model
import numpy as np
import pandas as pd

def tune(x, y):
    param = {'n_estimators':range(10, 200, 10), 'learning_rate':np.arange(0.01, 0.2, 0.1), 'max_depth':[3]}
    search_param = model_selection.GridSearchCV(estimator=ensemble.GradientBoostingClassifier(),
                                                param_grid = param,
                                                scoring='f1_micro',
                                                cv=10)
    search_param.fit(x,y)
    pprint(search_param.grid_scores_)
    print search_param.best_params_
    print search_param.best_score_  
    model = search_param.best_estimator_
    print model
    print model.feature_importances_

def repeated_nested_kfold_cv(x, y, features, repeats):
    feature_count = {}
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
            param = {'n_estimators':range(10, 200, 20), 'learning_rate':np.arange(0.01, 0.2, 0.02)}
            search_param = model_selection.GridSearchCV(estimator=ensemble.GradientBoostingClassifier(),
                                                        param_grid = param,
                                                        cv=inner_cv,
                                                        scoring='f1_micro')
            
            search_param.fit(x_train, y_train)
            clf = search_param.best_estimator_
            print search_param.best_params_
    
            y_predict = clf.predict(x_test)
            fscore = metrics.f1_score(y_test, y_predict, average='micro')
            scores.append(fscore)
            print "f1-score: %f" % fscore

    print "F1-Score : Mean - %.7g | Std - %.7g" % (np.mean(scores),np.std(scores))
    

if __name__ == '__main__':
    fp = os.path.join('data', 'MTurk_Harvey_v1.csv')
    print fp
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    df = pd.read_csv(fp)
    features = list(df)[:-1]
    x = data[:,:-1]
    y = data[:,-1]
    #tune(x, y)
    repeats = 10
    repeated_nested_kfold_cv(x, y, features, repeats)