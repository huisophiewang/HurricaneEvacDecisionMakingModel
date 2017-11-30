import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import f1_score


def nested_cv(x, y):
    outer_cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=0)
    scores = []
    for fold, (train_idx, test_idx) in enumerate(outer_cv.split(x, y)):
        print fold
        print test_idx
        x_train, x_test = x[train_idx], x[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        inner_cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=0)
        inner_cv.split(x_train, y_train)
        search_param = GridSearchCV(estimator=LogisticRegression(penalty='l1'), 
                                    param_grid={'C': np.arange(0.01, 1.5, 0.01)}, 
                                    cv=inner_cv, 
                                    scoring='f1_micro')
        search_param.fit(x_train, y_train)
        clf = search_param.best_estimator_
        y_predict = clf.predict(x_test)
        fscore = f1_score(y_test, y_predict, average='micro')
        print fscore
        scores.append(fscore)
    avg_score = np.mean(scores)
    return avg_score


if __name__ == '__main__':
    fp = 'data\MTurk_Harvey.csv'
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    df = pd.read_csv(fp)
    
    x = data[:,:-1]
    y = data[:,-1]
    