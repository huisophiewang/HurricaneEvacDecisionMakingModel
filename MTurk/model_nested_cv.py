import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import f1_score
from pprint import pprint
import operator
import os


def nested_cv(x, y, features):
    feature_count = {}
    outer_cv = StratifiedKFold(n_splits=10, shuffle=True)
    scores = []
    for fold, (train_idx, test_idx) in enumerate(outer_cv.split(x, y)):
        print fold
        print test_idx
        x_train, x_test = x[train_idx], x[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        # inner cv, tune hyper parameters
        inner_cv = StratifiedKFold(n_splits=10, shuffle=True)
        inner_cv.split(x_train, y_train)
        search_param = GridSearchCV(estimator=LogisticRegression(penalty='l1'), 
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
                feature_count[feature][1].append(coef)
                #print feature, coef

        y_predict = clf.predict(x_test)
        fscore = f1_score(y_test, y_predict, average='micro')
        print fscore
        scores.append(fscore)
        
    avg_score = np.mean(scores)
    print "avg f1 score: %f" % avg_score
    

    for feature in feature_count:
        if feature_count[feature][0] >=8:
            print feature
            
    sorted_count = sorted(feature_count.items(), key=lambda x: x[1][0], reverse=True)
    pprint(sorted_count)
    
    return avg_score


if __name__ == '__main__':
    fp = os.path.join('data', 'MTurk_Harvey.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    df = pd.read_csv(fp)
   
    features = list(df)[:-1]

    x = data[:,:-1]
    y = data[:,-1]
    nested_cv(x, y, features)
    

    