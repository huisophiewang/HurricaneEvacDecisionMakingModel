import os
from pprint import pprint
from sklearn import neural_network
from sklearn import preprocessing
from sklearn import model_selection
import numpy as np






if __name__ == '__main__':
    fp = os.path.join('data', 'MTurk_Harvey.csv')
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:,:-1]
    y = data[:,-1]
    
    scaler = preprocessing.StandardScaler().fit(x)
    x = scaler.transform(x) 
 
    all_layers = []
    for i in range(1, 11):
        print i
        all_layers.extend([(n,i) for n in range(1, 49, 3)])
    pprint(all_layers)
#       
#     param_test1 = {'hidden_layer_sizes':all_layers}
#     gsearch1 = model_selection.GridSearchCV(estimator = neural_network.MLPClassifier(solver='lbfgs', random_state=0), 
#                                             param_grid = param_test1, 
#                                             scoring='f1_micro', 
#                                             cv=10)