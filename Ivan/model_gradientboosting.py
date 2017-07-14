import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier  #GBM algorithm
#from sklearn import cross_validation, metrics   #Additional scklearn functions
#from sklearn.grid_search import GridSearchCV   #Perforing grid search
from sklearn import svm
from sklearn import datasets
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score

from pprint import pprint
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 12, 4



def gradient_boost(x_train, y_train, x_test, y_test):
    for alpha in np.arange(0.01, 1.0, 0.01):
        clf = GradientBoostingClassifier(learning_rate=alpha, random_state=0, max_depth=1).fit(x_train, y_train)
        print clf.score(x_test, y_test)                 

def cross_valid(alg, dtrain, predictors, target, performCV=True, printFeatureImportance=True, cv_folds=10):
    #Perform cross-validation:
    if performCV:
        # scoring = 'roc_auc', 
        cv_score = cross_val_score(alg, dtrain[predictors], dtrain[target], cv=cv_folds, scoring='accuracy')
        print cv_score
        print "CV Score : Mean - %.7g | Std - %.7g | Min - %.7g | Max - %.7g" % (np.mean(cv_score),np.std(cv_score),np.min(cv_score),np.max(cv_score))

#Fit the algorithm on the data        
#     alg.fit(dtrain[predictors], dtrain[target])
#         
#     #Predict training set:
#     dtrain_predictions = alg.predict(dtrain[predictors])
#     dtrain_predprob = alg.predict_proba(dtrain[predictors])[:,1]

#     #Print model report:
#     print "\nModel Report"
#     print "Accuracy : %.4g" % metrics.accuracy_score(dtrain[target].values, dtrain_predictions)
#     print "AUC Score (Train): %f" % metrics.roc_auc_score(dtrain[target], dtrain_predprob)
    
def plot_feature_rank(alg, dtrain, predictors, target):    
    #Print Feature Importance:
    alg.fit(dtrain[predictors], dtrain[target])
    print alg.feature_importances_

    feat_imp = pd.Series(alg.feature_importances_, predictors).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    plt.show()

if __name__ == '__main__':

    fp = 'data/Ivan_common.csv'
    #fp = 'data/Ivan_common_no_risk_perception.csv'
    #fp = 'data/Ivan_common_only_demographic.csv'
    #fp = 'data/Ivan_common_only_demographic_for_bridgeport.csv'
    
    fr = open(fp, 'rU')
    header = fr.readline().split(',')
    fr.close()
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:,:-1]
    y = data[:,-1]
   
#     np.random.seed(0)
#     indices = np.random.permutation(data.shape[0])
#     split1 = int(data.shape[0]*0.8)
#     split2 = int(data.shape[0]*0.9)
#     train_idx, valid_idx, test_idx = indices[:split1], indices[split1:split2], indices[split2:]
#     x_train, x_valid, x_test = x[train_idx], x[valid_idx], x[test_idx]
#     y_train, y_valid, y_test = y[train_idx], y[valid_idx], y[test_idx]
    
    #gradient_boost(x_train, y_train, x_test, y_test)
    

#     data = pd.read_csv(fp)
#     target = 'evac'
#     predictors = [x for x in data.columns if x not in [target]]
#     train_data, test_data = train_test_split(data, test_size=0.2, random_state=0)
#     train_x, train_y = train_data[predictors], train_data[target]
#     test_x, test_y = test_data[predictors], test_data[target]
    

    
#     gbm0 = GradientBoostingClassifier(random_state=10)
#     modelfit(gbm0, train, predictors, target)


#     param_test1 = {'n_estimators':range(20,150,10)}
#     gsearch1 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.05,min_samples_split=500,min_samples_leaf=50,max_depth=8,max_features='sqrt',subsample=0.8,random_state=10), 
#                             param_grid = param_test1, scoring='roc_auc',n_jobs=4, iid=False, cv=5)
#     gsearch1.fit(train[predictors],train[target])
#     pprint(gsearch1.grid_scores_)
#     print gsearch1.best_params_
#     print gsearch1.best_score_
    # n_estimators = 50
    
#     param_test2 = {'max_depth':range(1,16,1), 'min_samples_split':range(100,1001,100)}
#     gsearch2 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.05, n_estimators=50, max_features='sqrt', subsample=0.8, random_state=10), 
#                             param_grid = param_test2, scoring='roc_auc',n_jobs=4,iid=False, cv=5)
#     gsearch2.fit(train[predictors],train[target])
#     pprint(gsearch2.grid_scores_)
#     print gsearch2.best_params_
#     print gsearch2.best_score_
    # {'min_samples_split': 400, 'max_depth': 4}
    
#     param_test3 = {'min_samples_split':range(100,1001,100), 'min_samples_leaf':range(20,101,10)}
#     gsearch3 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.05, n_estimators=50,max_depth=4,max_features='sqrt', subsample=0.8, random_state=10), 
#                             param_grid = param_test3, scoring='roc_auc',n_jobs=4,iid=False, cv=5)
    #print gsearch3.best_estimator_
#    gsearch3.fit(train_x, train_y)
#     pprint(gsearch3.grid_scores_)
#     print gsearch3.best_params_
#     print gsearch3.best_score_
    # {'min_samples_split': 200, 'min_samples_leaf': 20}
    

    
#     cls = GradientBoostingClassifier(criterion='friedman_mse', init=None,
#               learning_rate=0.05, loss='deviance', max_depth=4,
#               max_features='sqrt', max_leaf_nodes=None,
#               min_impurity_split=1e-07, min_samples_leaf=20,
#               min_samples_split=200, min_weight_fraction_leaf=0.0,
#               n_estimators=50, presort='auto', random_state=10,
#               subsample=0.8, verbose=0, warm_start=False)
   

#     cls.fit(train_x, train_y)
#     test_predictions = cls.predict(test_x)
#     test_predprob = cls.predict_proba(test_x)[:,1]
#      
#     acc = accuracy_score(test_y, test_predictions)
#     print acc
#     auc = roc_auc_score(test_y, test_predprob)
#     print auc
  

    cls = GradientBoostingClassifier()
    cv_score = cross_val_score(cls, x, y, cv=10, scoring='accuracy')
    print cv_score
    print "CV Score : Mean - %.7g | Std - %.7g | Min - %.7g | Max - %.7g" % (np.mean(cv_score),np.std(cv_score),np.min(cv_score),np.max(cv_score))

    
    