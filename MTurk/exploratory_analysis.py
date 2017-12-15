import numpy as np
from sklearn import linear_model
from sklearn import svm
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from sklearn.metrics import f1_score
from pprint import pprint



# full data
# F1-score
# baseline: 0.752
# demo + house: 0.762
# risk: 0.754
# notice: 0.815
# info: 0.852
# info + notice: 0.844
# all: 0.842

# predict risk_stay
# F1-score
# baseline: 0.5238

# predict risk_stay
# F1-score
# baseline: 0.6163

def sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam):
    clf = linear_model.LogisticRegression(C=lam, penalty='l1')
    #clf = svm.SVC(C=lam, kernel='linear')
    
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    
    predict = np.zeros(len(y_test))
    f_score = f1_score(y_test, predict, pos_label=1, average='micro')
    #print y_test
    #print predict

    #print f_score
    return f_score

def cross_validate(x, y, fold=10):
    lam_range = np.arange(0.01, 1.5, 0.01)
    #lam_range = [1.0]
    lam_accs = []
    for lam in lam_range:
        accs = []
        for k in range(fold):
            #print 'fold: %d' % k
            hd_idx = np.arange(k, len(x), fold)
            x_test, y_test = x[hd_idx], y[hd_idx]
            x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
            acc = sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam)
            accs.append(acc)
        avg_acc = np.mean(accs)
        print "average score: %f " % avg_acc
        lam_accs.append(avg_acc)
    idx = np.argmax(lam_accs)
    best_lam = lam_range[idx]
    print "max score: %f" % lam_accs[idx]
    print "best lambda: %f" % best_lam
    return best_lam

def corr_test(df, y_col):
    
#     for col in df.columns:
#         #print col
#         #print df[col].unique()
#         r, p = stats.pearsonr(df[col], df[y_col])
#         if p < 0.05:
#             print
#             print col
#             print r, p
            
    p_vars = []
    for col in df.columns:
        r, p = stats.pearsonr(df[col], df[y_col])
        p_vars.append((col, r, p))
    res = sorted(p_vars, key=lambda x: x[2])
    pprint(res)
        
def scatter_plot(df, var_x):
    x = df[var_x]
    y = df['risk_stay'] - df['risk_evac']
    plt.scatter(x, y)
    plt.xlabel(var_x)
    plt.ylabel('risk')
    plt.show()

def hist_plot(df, var):
    x = df[var]
    plt.hist(x)
    plt.show()
    
if __name__ == '__main__':
    fp = 'data\MTurk_Harvey_predict_risk_stay.csv'
    fp = 'data\MTurk_Harvey_predict_risk_evac.csv'
#     fp = 'data\MTurk_Harvey_basic.csv'
#     fp = 'data\MTurk_Harvey_risk.csv'
#     fp = 'data\MTurk_Harvey_notice.csv'
#     fp = 'data\MTurk_Harvey_info.csv'
    #fp = 'data\MTurk_Harvey_info_notice.csv'
    
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    df = pd.read_csv(fp)

    corr_test(df, 'received_evac_notice')
    
#     x = data[:, :-1]
#     y = data[:,-1]
#      
#     baseline_acc = 1.0 - sum(y)/float(len(y))
#     print len(y)
#     print sum(y)
#     print 'accuracy baseline: %f' % baseline_acc
# #     
# 
#     cross_validate(x, y)
    
    