import os
from pprint import pprint
import numpy as np
from sklearn import linear_model

header = ['Age', 'Gender', 'r_black', 'r_native', 'r_other', 'm_single', 'm_other',
"HouseholdSize", "NumChd", "e_someclg", "e_clg", "Income",
'Owner', 'h_mobile', 'h_other', "CloseCoast", "CloseWater", "OfficialHurricWatch", "OfficialEvac", 
"SrcLocalAuth", "SrcLocalMedia", "SrcNationalMedia", "SrcInternet", "SrcPeers",
"SeeStormCond", "SeeShopClose", "SeePeerEvac", "PrevStormExp", "PrevFalseAlarm",
"ProtectFromLooter", "ProtectFromStorm", "LostIncome", "EvacExpense", "Traffic"]


def sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam, norm):
    clf = linear_model.LogisticRegression(C=lam, penalty=norm)
    #clf = svm.SVC(C=lam)
    
    clf.fit(x_train, y_train)
    predict = clf.predict(x_test)
    acc = np.sum(predict == y_test).astype(int) / float(len(y_test))
    #print acc
    return acc


################
# L1, lam=0.39 acc=0.7005
# L2, lam=0.01 acc=0.7006
def cross_validate(x, y, fold, norm):
    lam_range = np.arange(0.0001, 2.0, 0.01)
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
            acc = sklearn_logistic_reg(x_train, y_train, x_test, y_test, lam, norm)
            accs.append(acc)
        avg_acc = np.mean(accs)
        print "accuracy: %f " % avg_acc
        lam_accs.append(avg_acc)
    idx = np.argmax(lam_accs)
    best_lam = lam_range[idx]
    print "max accuracy: %f" % lam_accs[idx]
    print "best C: %f" % best_lam
    
def final_model(x, y, lam, norm):
    clf = linear_model.LogisticRegression(C=lam, penalty=norm)
    #clf = svm.SVC(C=lam)
    clf.fit(x, y)
    print clf.coef_
    
    coefs = {}
    for i, c in enumerate(clf.coef_.T):
        coefs[header[i]] = c[0]
    res = sorted(coefs.items(), key=lambda x: abs(x[1]), reverse=True)
    pprint(res)
    



if __name__ == '__main__':
    #fp = os.path.join('result', 'feature', 'all_features_fp_openn_cls.csv')
    #fp = os.path.join('result', 'feature', 'all_features_all_traits_cls.csv')
    data = np.genfromtxt("Lili_converted.csv", delimiter=",", dtype=float, skip_header=1)
    #np.random.shuffle(data)
    #print data

#     x = data[:, 1:-1]
#     #print x
#     y = data[:,-1]
#     #cross_validate(x, y, fold=10)
#     #cross_validate(x, y, fold=len(x))
#     print np.sum(y) 
#     print len(y)
    x = data[:,:-1]
    y = data[:,-1]

    #cross_validate(x, y, fold=10, norm='l1')
    final_model(x, y, 0.39, 'l1')
    