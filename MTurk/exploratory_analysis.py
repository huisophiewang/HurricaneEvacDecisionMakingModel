import numpy as np
from sklearn import linear_model
from sklearn import svm
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

def sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam):
    clf = linear_model.LogisticRegression(C=lam, penalty='l1')
    #clf = svm.SVC(C=lam, kernel='poly')
    
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    #print acc
    return acc

def cross_validate(x, y, fold):
    lam_range = np.arange(0.01, 1.5, 0.01)
    lam_accs = []
    for lam in lam_range:
        accs = []
        for k in range(fold):
            #print 'fold: %d' % k
            hd_idx = np.arange(k, len(x), fold)
            x_test, y_test = x[hd_idx], y[hd_idx]
            x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
            #test_mse = mean_as_prediction(y_test, np.mean(y_train), 'mae')
            #test_mse = my_linear_reg(x_train, y_train, x_test, y_test)
            acc = sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam)
            accs.append(acc)
        avg_acc = np.mean(accs)
        print "accuracy: %f " % avg_acc
        lam_accs.append(avg_acc)
    idx = np.argmax(lam_accs)
    best_lam = lam_range[idx]
    print "max accuracy: %f" % lam_accs[idx]
    print "best lambda: %f" % best_lam
    return best_lam

def corr_test(df):
    
    y = df['risk_stay'] - df['risk_evac']
    for col in df.columns:
        print col
        #print df[col].unique()
        r, p = stats.pearsonr(df[col],y)
        if p < 0.05:
            print r, p
        
def scatter_plot(df, var_x):
    x = df[var_x]
    y = df['risk_stay'] - df['risk_evac']
    plt.scatter(x, y)
    plt.xlabel(var_x)
    plt.ylabel('risk')
    plt.show()

if __name__ == '__main__':
    fp = 'MTurk_Harvey_risk.csv'
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    df = pd.read_csv(fp)
#     x = data[:,:-6]
#     risk_stay = data[:,-6]
#     risk_evac = data[:,-5]
#     print risk_evac
#     y = risk_stay - risk_evac
#     print y
#     plt.hist(y, bins=9)
#     plt.show()

    corr_test(df)
    scatter_plot(df, 'info_tv_leave')
    
    