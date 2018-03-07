import os
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import model_selection
from sklearn import metrics
from pprint import pprint


def get_final_lambda(x, y):
    cv = model_selection.StratifiedKFold(n_splits=10, shuffle=True)
    cv.split(x, y)
    search_param = model_selection.GridSearchCV(estimator=linear_model.LogisticRegression(penalty='l1'), 
                                param_grid={'C': np.arange(0.01, 1.5, 0.01)}, 
                                cv=cv, 
                                scoring='f1_micro')
    search_param.fit(x, y)
    print search_param.best_estimator_
    print search_param.best_params_
    print search_param.best_score_
    
    lam = search_param.best_params_['C']
    return lam

def get_final_model(x, y, lam):
    clf = linear_model.LogisticRegression(penalty='l1', C=lam)
    clf.fit(x, y)
    print clf.coef_
    print clf.intercept_
    
    return clf
    
def predict(model, x_test, y_test):
    y_predict = model.predict(x_test)
    fscore = metrics.f1_score(y_test, y_predict, average='micro')
    print "f1-score: %f" % fscore

if __name__ == '__main__':
    fp_harvey = os.path.join('data', 'MTurk_Harvey.csv')
    data_harvey = np.genfromtxt(fp_harvey, delimiter=",", dtype=float, skip_header=1)
    x_harvey = data_harvey[:,:-1]
    y_harvey = data_harvey[:,-1]
    
    fp_irma = os.path.join('data', 'MTurk_Irma_without_harvey_questions.csv')
    data_irma = np.genfromtxt(fp_irma, delimiter=",", dtype=float, skip_header=1)
    x_irma = data_irma[:,:-1]
    y_irma = data_irma[:,-1]
    
    # learn harvey model, predict irma
    final_lam_harvey = get_final_lambda(x_harvey, y_harvey)
    final_model_harvey = get_final_model(x_harvey, y_harvey, final_lam_harvey)
    predict(final_model_harvey, x_irma, y_irma)
    print '-----------------------------------------'
    # learn irma model, predict harvey
    final_lam_irma = get_final_lambda(x_irma, y_irma)
    final_model_irma = get_final_model(x_irma, y_irma, final_lam_irma)
    predict(final_model_irma, x_harvey, y_harvey)
    
    
    
    
    

    
    