import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import model_selection
from sklearn import metrics
from scipy.stats import hmean
from pprint import pprint
import operator
import os
import itertools


def repeated_nested_kfold_cv(x, y, features, repeats):
    feature_count = {}
    scores = []
    precision_scores = []
    recall_scores = []
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
            search_param = model_selection.GridSearchCV(estimator=linear_model.LogisticRegression(penalty='l1'), 
                                        param_grid={'C': np.arange(0.01, 1.5, 0.01)}, 
                                        cv=inner_cv, 
                                        scoring='f1_micro')
            search_param.fit(x_train, y_train)
            clf = search_param.best_estimator_
            
            # count the times a feature is selected
            for i, coef in enumerate(clf.coef_[0]):
                if coef != 0.0:
                    feature = features[i]
                    if not feature in feature_count:
                        feature_count[feature] = [0, []]
                    feature_count[feature][0] += 1
                    # for computing the distribution of coefficients
                    #feature_count[feature][1].append(coef)
                    #print feature, coef
    
            y_predict = clf.predict(x_test)
            fscore = metrics.f1_score(y_test, y_predict, average='micro')
            scores.append(fscore)
            print "f1-score: %f" % fscore

        
    print "F1-Score : Mean - %.7g | Std - %.7g" % (np.mean(scores),np.std(scores))
#     print "Precision : Mean - %.7g | Std - %.7g" % (np.mean(precision_scores),np.std(precision_scores))
#     print "Recall : Mean - %.7g | Std - %.7g" % (np.mean(recall_scores),np.std(recall_scores))

    for feature in feature_count:
        feature_count[feature][0] /= float(10*repeats)
    sorted_features = sorted(feature_count.items(), key=lambda x: x[1][0], reverse=True)
    pprint(sorted_features)
    for f, vals in sorted_features:
        prob = vals[0]
        print f, prob
    
def test_metrics(x, y):
    clf = linear_model.LogisticRegression()
    clf.fit(x, y)
    y_predict = clf.predict(x)
    print metrics.confusion_matrix(y, y_predict)
    print np.sum(y)
    print
    print 'f1_score:'
    print metrics.f1_score(y, y_predict, average='binary')
    print metrics.f1_score(y, y_predict, average='micro')
    print metrics.f1_score(y, y_predict, average='macro')
    print
    print 'precision:'
    p = metrics.precision_score(y, y_predict, average='binary')
    # precision_binary = precision_evac = 88/88+19 = 0.822
    p_mi = metrics.precision_score(y, y_predict, average='micro')
    # precision_micro = 363+88 / 363+38+88+19 = 0.888
    p_ma = metrics.precision_score(y, y_predict, average='macro')
    # precision_stay = 363/363+38 = 0.905
    # precision_macro = (precision_evac + precision_stay)/2 = 0.864
    print p, p_mi, p_ma
    print
    print 'recall:'
    r = metrics.recall_score(y, y_predict, average='binary')
    # recall_binary = recall_evac = 88/88+38 = 0.698
    r_mi = metrics.recall_score(y, y_predict, average='micro')
    # recall_micro = 88+363 / 88+38+363+19 = 0.888
    r_ma = metrics.recall_score(y, y_predict, average='macro')
    # recall_stay = 363/363+19=0.95
    # recall_macro = (recall_evac + recall_stay) = 0.824
    print r, r_mi, r_ma
    print
    print 'harmonic mean'
    print hmean([p,r]), hmean([p_mi, r_mi]), hmean([p_ma, r_ma])
            
        


if __name__ == '__main__':
    fp = os.path.join('data', 'MTurk_Irma.csv')
    print fp
    #fp = os.path.join('data', 'MTurk_Harvey_predict_risk_evac.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    df = pd.read_csv(fp)
    features = list(df)[:-1]
    x = data[:,:-1]
    y = data[:,-1]
    repeats = 10
    repeated_nested_kfold_cv(x, y, features, repeats)
    #test_metrics(x, y)
    

    