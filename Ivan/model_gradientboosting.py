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
from sklearn import metrics

from pprint import pprint
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 12, 4

def split_train_test(fp):
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

    
#     data = pd.read_csv(fp)
#     target = 'evac'
#     predictors = [x for x in data.columns if x not in [target]]
#     train_data, test_data = train_test_split(data, test_size=0.2, random_state=0)
#     train_x, train_y = train_data[predictors], train_data[target]
#     test_x, test_y = test_data[predictors], test_data[target]

def gradient_boost(x_train, y_train, x_test, y_test):
    for alpha in np.arange(0.01, 1.0, 0.01):
        clf = GradientBoostingClassifier(learning_rate=alpha, random_state=0, max_depth=1).fit(x_train, y_train)
        print clf.score(x_test, y_test)                 

def cross_valid(x,y):
    cls = GradientBoostingClassifier()
    cv_score = cross_val_score(cls, x, y, cv=10, scoring='f1')
    print cv_score
    print "CV Score : Mean - %.7g | Std - %.7g | Min - %.7g | Max - %.7g" % (np.mean(cv_score),np.std(cv_score),np.min(cv_score),np.max(cv_score))

def get_train_acc(alg, df, predictors, target):
    alg.fit(df[predictors], df[target])
    predictions = alg.predict(df[predictors])
    predict_acc = metrics.accuracy_score(df[target].values, predictions)
    print predict_acc
    
def plot_feature_rank(alg, df, predictors, target):    
    #Print Feature Importance:
    alg.fit(df[predictors], df[target])
    print alg.feature_importances_

    feat_imp = pd.Series(alg.feature_importances_, predictors).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    plt.show()
    
def evaluation(alg, dtrain, predictors, target, performCV=True, printFeatureImportance=False, cv_folds=10):
    #Fit the algorithm on the data
    alg.fit(dtrain[predictors], dtrain[target])
        
    #Predict training set:
    dtrain_predictions = alg.predict(dtrain[predictors])
    
    #Print model report:
    print "Accuracy (Train): %.4f" % metrics.accuracy_score(dtrain[target].values, dtrain_predictions)
    #print "F1 score (Train): %f" % metrics.f1_score(dtrain[target].values, dtrain_predictions)
    
        #Perform cross-validation:
    if performCV:
        cv_score = cross_val_score(alg, dtrain[predictors], dtrain[target], cv=cv_folds, scoring='accuracy')
        print "Accuracy (CV) : %.4f" % np.mean(cv_score)
        
    #Print Feature Importance:
    if printFeatureImportance:
        feat_imp = pd.Series(alg.feature_importances_, predictors).sort_values(ascending=False)
        feat_imp.plot(kind='bar', title='Feature Importances')
        plt.ylabel('Feature Importance Score')
        plt.show()
    
def tune_paramenters(df, predictors, target):

    
    
    cls = GradientBoostingClassifier(random_state=0)
    print cls
   

#     param_test1 = {'n_estimators':range(20,120,10), 'learning_rate':np.linspace(0.05, 0.2, 4)}
#     gsearch1 = GridSearchCV(estimator = GradientBoostingClassifier(min_samples_split=80,
#                                                                    min_samples_leaf=30,
#                                                                    max_depth=5,
#                                                                    max_features='sqrt',
#                                                                    subsample=0.8,
#                                                                    random_state=0), 
#                             param_grid = param_test1, scoring='accuracy',cv=10)
#     gsearch1.fit(df[predictors],df[target])
#     pprint(gsearch1.grid_scores_)
#     print gsearch1.best_params_
#     print gsearch1.best_score_
    
    # n_estimators = 40, learning_rate=0.1 (max_features='sqrt',subsample=0.8)
    # n_estimators = 100, learning_rate = 0.1
    
#     param_test2 = {'max_depth':range(3,10,1), 'min_samples_split':range(20,151,10)}
#     gsearch2 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, 
#                                                                    n_estimators=100, 
#                                                                    max_features='sqrt', 
#                                                                    subsample=0.8, 
#                                                                    random_state=0), 
#                             param_grid = param_test2, scoring='accuracy',cv=10, n_jobs=4)
#     gsearch2.fit(df[predictors],df[target])
#     pprint(gsearch2.grid_scores_)
#     print gsearch2.best_params_
#     print gsearch2.best_score_
    #'min_samples_split': 100, 'max_depth': 4 (max_features='sqrt',subsample=0.8)
    # 'min_samples_split': 40, 'max_depth': 3
    
#     param_test3 = {'min_samples_split':range(20,151,10), 'min_samples_leaf':range(10,101,10)}
#     gsearch3 = GridSearchCV(estimator = GradientBoostingClassifier(learning_rate=0.1, 
#                                                                    n_estimators=40,
#                                                                    max_depth=3,
#                                                                    max_features='sqrt', 
#                                                                    subsample=0.8, 
#                                                                    random_state=0), 
#                              param_grid = param_test3, scoring='accuracy',cv=10, n_jobs=4)
#     #print gsearch3.best_estimator_
#     gsearch3.fit(df[predictors], df[target])
#     pprint(gsearch3.grid_scores_)
#     print gsearch3.best_params_
#     print gsearch3.best_score_
#     #{'min_samples_split': 100, 'min_samples_leaf': 60}
    
#     final_model = GradientBoostingClassifier(learning_rate=0.1, 
#                                                n_estimators=40,
#                                                max_depth=4,
#                                                min_samples_split=100,
#                                                min_samples_leaf=60,
#                                                max_features='sqrt', 
#                                                subsample=0.8, 
#                                                random_state=0)

    
    #return final_model
    
def tune_parameters1(df, predictors, target):

    for alpha in [0.9, 1.0]:
        print '--------------'
        for n in range(5,30,5):
            print 'learning rate: %f, n_estimators: %d' % (alpha, n)
            cls = GradientBoostingClassifier(learning_rate=alpha, 
                                                       n_estimators=n,
                                                       max_depth=10,
                                                       random_state=0)
             
             
            evaluation(cls, df, predictors, target)

#     param_test1 = {'n_estimators':range(50,800,50), 'learning_rate':[0.001, 0.01, 0.1, 0.2]}
#     gsearch1 = GridSearchCV(estimator=GradientBoostingClassifier(
#                                                    
#                                                    #max_depth=4,
#                                                    random_state=0),
#                             param_grid = param_test1, scoring='accuracy',cv=10, n_jobs=4)    
#     gsearch1.fit(df[predictors],df[target])
#     pprint(gsearch1.grid_scores_)
#     print gsearch1.best_params_
#     print gsearch1.best_score_   
             
if __name__ == '__main__':

    fp = 'data/Ivan_common.csv'
    #fp = 'data/Ivan_common_no_risk_perception.csv'
    #fp = 'data/Ivan_common_only_demographic.csv'
    #fp = 'data/Ivan_common_only_demographic_for_bridgeport.csv'
    fp = 'data/Ivan_common_with_county.csv'
    
    fr = open(fp, 'rU')
    header = fr.readline().split(',')
    fr.close()



    df = pd.read_csv(fp)
    target = 'evac'
    predictors = [x for x in df.columns if x not in [target]]
    
    evac_rate = sum(df['evac'])/float(len(df))
    majority = max(evac_rate, 1.0-evac_rate)
    print 'baseline: %.4f' % majority
    
    tune_parameters1(df, predictors, target)
    #final_model = tune_paramenters(df, predictors, target)
    #evaluation(final_model, df, predictors, target)
#     plot_feature_rank(final_model, df, predictors, target)
#     get_train_acc(final_model, df, predictors, target)

  



