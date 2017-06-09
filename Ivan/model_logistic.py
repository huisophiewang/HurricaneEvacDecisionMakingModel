import numpy as np
from sklearn import linear_model
from sklearn import svm
from pprint import pprint
from operator import itemgetter 

def sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam):
    #clf = linear_model.LogisticRegression(C=lam)
    #clf = linear_model.LogisticRegression(C=lam, penalty='l1')
    clf = svm.SVC(C=lam)
    
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    #print acc
    return acc

def get_lambda(x_train, y_train, x_valid, y_valid):
    lam_range = np.arange(0.001, 2.0, 0.1)
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
    lam_range = np.arange(0.001, 2.0, 0.01)
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

if __name__ == '__main__':

    fp = 'data/Ivan_common.csv'
    fp = 'data/Ivan_common_no_risk_perception.csv'
    fp = 'data/Ivan_common_only_demographic.csv'
    #fp = 'Ivan_all_common.csv'
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
#     
#     lam = get_lambda(x_train, y_train, x_valid, y_valid)
#     get_test_acc(x_train, y_train, x_test, y_test, lam, header)
    



    cross_validate(x, y, fold=10)
    
    