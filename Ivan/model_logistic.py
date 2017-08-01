import numpy as np
from sklearn import linear_model
from sklearn import svm
from sklearn.model_selection import cross_val_score
from pprint import pprint
from operator import itemgetter 
from util import COUNTIES, STATES
from util import county_to_state
from sklearn import metrics
from sklearn import preprocessing

def sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam):
    clf = linear_model.LogisticRegression(C=lam, penalty='l1')
    #clf = svm.SVC(C=lam, kernel='poly')
    
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    #print acc
    return acc

def get_lambda(x_train, y_train, x_valid, y_valid):
    lam_range = np.arange(1.5, 3.0, 0.1)
    accs = []
    for lam in lam_range:
        acc = sklearn_logistic_reg(x_train, y_train, x_valid, y_valid, lam)
        accs.append(acc)
    idx = np.argmax(accs)
    best_lam = lam_range[idx]
    #print "max accuracy: %f" % accs[idx]
    print "best lambda: %f" % best_lam
    return best_lam


def get_test_acc(x_train, y_train, x_test, y_test, lam, header):
    #clf = linear_model.LogisticRegression(C=lam)
    clf = svm.SVC(C=lam)
    clf.fit(x_train, y_train)

#     coefs = {}
#     for i, c in enumerate(clf.coef_.T):
#         coefs[header[i]] = c[0]
#     res = sorted(coefs.items(), key=lambda x: abs(x[1]), reverse=True)
#     pprint(res)
    
    predict = clf.predict(x_test)
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    print acc
    return acc
    

def cross_validate(x, y, fold):
    lam_range = np.arange(0.01, 2, 0.01)
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

def final_model(header, x, y, lam=1.0):
    clf = linear_model.LogisticRegression(C=lam)
    #clf = svm.SVC(C=lam)
    clf.fit(x, y)
    #print clf.coef_
    #print clf.intercept_
    
    coefs = {}
    for i, c in enumerate(clf.coef_.T):
        coefs[header[i]] = c[0]
    res = sorted(coefs.items(), key=lambda x: abs(x[1]), reverse=True)
    for pair in res:
        print '%s %.4f' % (pair[0].ljust(30), pair[1])
    
def get_acc_by_state(x, y, header):
    by_county_total = [0]*len(COUNTIES)
    by_county_correct = [0]*len(COUNTIES)
    ct_t_pos = [0]*len(COUNTIES)
    ct_t_neg = [0]*len(COUNTIES)
    ct_f_pos = [0]*len(COUNTIES)
    ct_f_neg = [0]*len(COUNTIES)
    
    by_state_total = [0]*len(STATES)
    by_state_correct = [0]*len(STATES)
    
    np.random.seed(0)
    indices = np.random.permutation(data.shape[0])
#     split = int(data.shape[0]*0.1)
#     test_idx, train_idx = indices[:split], indices[split:]
#     x_train, x_test = x[train_idx], x[test_idx]
#     y_train, y_test = y[train_idx], y[test_idx]
    clf = linear_model.LogisticRegression()
    clf.fit(x, y)
    
    coefs = {}
    for i, c in enumerate(clf.coef_.T):
        coefs[header[i]] = c[0]
    res = sorted(coefs.items(), key=lambda x: abs(x[1]), reverse=True)
    pprint(res)
    
    y_predict = clf.predict(x)
    for i in indices:
        c = int(x[i][-1])
        s = county_to_state(c)
        by_county_total[c] += 1
        by_state_total[s] += 1
        
        if y_predict[i] == y[i]:
            by_county_correct[c] += 1
            by_state_correct[s] += 1
            
        if y_predict[i]==1 and y[i]==1:
            ct_t_pos[c] += 1
        if y_predict[i]==0 and y[i]==0:
            ct_t_neg[c] += 1
        if y_predict[i]==1 and y[i]==0:
            ct_f_pos[c] += 1
        if y_predict[i]==0 and y[i]==1:
            ct_f_neg[c] += 1
        
    county_acc = {}
    for j in range(len(COUNTIES)):
        print '--------------'
        c=COUNTIES[j]
        print c
        print by_county_total[j]
        acc = float(by_county_correct[j])/by_county_total[j]
        print acc
        print ct_t_pos[j]
        print ct_t_neg[j]
        print ct_f_pos[j]
        print ct_f_neg[j]
        county_acc[c] = acc
    pprint(sorted(county_acc.items(), key=lambda x:x[1]))
    
    for j in range(len(STATES)):
        print '-------'
        print STATES[j]
        print by_state_total[j]
        acc = float(by_state_correct[j])/by_state_total[j]
        print acc
            
        
def normalize_test(arr):
    res = []
    
    mean = np.mean(arr)
    variance = np.var(arr)
    for p in arr:
        q = (p - mean) / variance
        res.append(q)
    print res         
        
    

    
if __name__ == '__main__':

    fp = 'data/Ivan_common.csv'
    #fp = 'data/Ivan_common_no_risk_perception.csv'
    #fp = 'data/Ivan_common_only_demographic.csv'
    #fp = 'data/Ivan_common_only_demographic_for_Bridgeport.csv'
    #fp = 'data/Ivan_common_with_county.csv'
    #fp = 'data/Ivan_common_only_objective.csv'
    
    fr = open(fp, 'rU')
    header = fr.readline().split(',')
    
    fr.close()
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:,:-1]
    y = data[:,-1]
    

    evac_rate = sum(y)/float(len(y))
    majority = max(evac_rate, 1.0-evac_rate)
    print 'baseline: %.4f' % majority
    
    #get_acc_by_state(x, y, header)
    
    
#     clf = linear_model.LogisticRegression()
#     clf.fit(x, y)
#     y_predict = clf.predict(x)
#     predict_acc = metrics.f1_score(y_predict, y)
#     print predict_acc
    

    
#     np.random.seed(0)
#     indices = np.random.permutation(data.shape[0])
#     split1 = int(data.shape[0]*0.8)
#     split2 = int(data.shape[0]*0.9)
#     train_idx, valid_idx, test_idx = indices[:split1], indices[split1:split2], indices[split2:]
#     x_train, x_valid, x_test = x[train_idx], x[valid_idx], x[test_idx]
#     y_train, y_valid, y_test = y[train_idx], y[valid_idx], y[test_idx]
#     
#     lam = get_lambda(x_train, y_train, x_valid, y_valid)
#     get_test_acc(x_train, y_train, x_test, y_test, lam, header)
    



    
    cross_validate(x, y, fold=10)
    #best lambda 0.021
    final_model(header, x, y, 0.08)
    
    #s = 'hello world'
    #print s.rjust(10)

#     cls = linear_model.LogisticRegression()
#     #cls = svm.SVC()
#     cv_score = cross_val_score(cls, x, y, cv=10, scoring='f1')
#     print cv_score
#     print "CV Score : Mean - %.7g | Std - %.7g | Min - %.7g | Max - %.7g" % (np.mean(cv_score),np.std(cv_score),np.min(cv_score),np.max(cv_score))

    


    
    