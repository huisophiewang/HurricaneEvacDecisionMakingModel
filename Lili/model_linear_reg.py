import os
import numpy as np
from sklearn import linear_model
from pprint import pprint



def lasso_cv(x, y, fold):
    lam_errs = []
    lam_range = np.arange(0.000, 500, 1.0)
    #lam_range = np.arange(0.000, 150, 0.5)
    for lam in lam_range:
        #print "lambda is %f" % lam
        fold_errs = []
        for k in range(fold):
            #print 'fold: %d' % k
            hd_idx = np.arange(k, len(x), fold)
            x_holdout, y_holdout = x[hd_idx], y[hd_idx]
            x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
            model = linear_model.Lasso(alpha=lam)
            #model = linear_model.Ridge(alpha=lam)
            model.fit(x_train, y_train)
            predict = np.dot(x_holdout, model.coef_) + model.intercept_
            #print predict
            #print y_holdout
            hd_err = np.mean((predict - y_holdout)**2)
            fold_errs.append(hd_err)
        lam_errs.append(np.mean(fold_errs))
    pprint(lam_errs)
    idx = np.argmin(lam_errs)
    best_lam = lam_range[idx]
    print "min test error: %f" % lam_errs[idx]
    print "best lambda: %f" % best_lam
#     final_model = linear_model.Lasso(alpha=best_lam)
#     final_model.fit(x, y)
#     print final_model.coef_
#     prediction = np.dot(x, final_model.coef_) + final_model.intercept_
#     #print prediction
#     # use adjusted r squared
#     r_squared = get_r_squared(y, prediction)
#     print "R squared: %f" % r_squared

#     n, p = x.shape
#     adjusted_r_squared = get_adjusted_r_squared(n, p, r_squared)
#     print adjusted_r_squared
    
    return best_lam       

def get_r_squared(y, y_predict):    
    ss_total = np.sum((y - np.mean(y))**2)
    ss_reg = np.sum((y_predict - np.mean(y))**2)
    return ss_reg/ss_total

def get_adjusted_r_squared(n, p, r_squared):
    adjusted = 1.0 - (1.0-r_squared)*(n-1)/(n-p-1)
    return adjusted

def mean_as_prediction(y, y_mean): 
    err = np.mean((y - y_mean)**2)
    return err

def sklearn_linear_reg(x_train, y_train, x_test, y_test):
    reg = linear_model.LinearRegression()
    reg.fit(x_train, y_train)
    print reg.coef_, reg.intercept_
    predict = reg.predict(x_test)
    test_mse = np.mean((predict - y_test) ** 2)
    return test_mse
    
def linear_reg_cv(x, y, fold):
    test_mses = []
    for k in range(fold):
        print 'fold: %d' % k
        hd_idx = np.arange(k, len(x), fold)
        x_test, y_test = x[hd_idx], y[hd_idx]
        x_train, y_train = np.delete(x, hd_idx, axis=0), np.delete(y, hd_idx, axis=0)
        #test_mse = mean_as_prediction(y_test, np.mean(y_train))
        test_mse = sklearn_linear_reg(x_train, y_train, x_test, y_test)
        test_mses.append(test_mse)   
    pprint(test_mses)
    avg_test_mse = np.mean(test_mses)
    print "average test mse: %f" % avg_test_mse
    
if __name__ == '__main__':
    data = np.genfromtxt("Lili_converted_EvacTime.csv", delimiter=",", dtype=float, skip_header=1)
    #np.random.shuffle(data)
    #print data

    x = data[:, :-1]
    y = data[:,-1]
    #lasso_cv(x, y, fold=10)
    linear_reg_cv(x, y, fold=10)

