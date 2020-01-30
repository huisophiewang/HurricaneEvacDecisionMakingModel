import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier  #GBM algorithm
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from pprint import pprint
import matplotlib.pylab as plt

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
        pprint(feat_imp)
        feat_imp.plot(kind='bar', title='Feature Importances')
        plt.ylabel('Feature Importance Score')
        plt.show()
        
def tune(df, predictors, target):
    #for alpha in np.linspace(0.01, 0.2, 10):
    for alpha in [0.1]:
        print '--------------'
        for n in range(10, 200, 10):
            print 'learning rate: %f, n_estimators: %d' % (alpha, n)

#             cls = GradientBoostingClassifier(learning_rate=alpha, 
#                                                        n_estimators=n,
#                                                        max_depth=2,
#                                                        random_state=0)
            cls = AdaBoostClassifier(learning_rate=alpha, n_estimators=n)
    
            evaluation(cls, df, predictors, target)
            

        


if __name__ == '__main__':

    fp = 'data/Lili_converted_v3.csv'
    
    fr = open(fp, 'rU')
    header = fr.readline().split(',')
    fr.close()



    df = pd.read_csv(fp)
    target = 'Evac'
    predictors = [x for x in df.columns if x not in [target]]
    
    evac_rate = sum(df['Evac'])/float(len(df))
    majority = max(evac_rate, 1.0-evac_rate)
    print 'baseline: %.4f' % majority
    
    #tune(df, predictors, target)
    
    cls = AdaBoostClassifier(learning_rate=0.1, n_estimators=40)
    #cls = GradientBoostingClassifier()
    evaluation(cls, df, predictors, target, True, True, 10)
    
    