import os
import pandas as pd
import numpy as np
from pgmpy import models, estimators
from pgmpy import independencies 
from pgmpy.estimators import ConstraintBasedEstimator
from pgmpy.estimators import ExhaustiveSearch, K2Score

if __name__ == '__main__':
#     fp = os.path.join('data', 'MTurk_Harvey.csv')
#     df = pd.read_csv(fp)
#     data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
#     x = data[:,:-1]
#     y = data[:,-1]
    
#     data = pd.DataFrame(np.random.randint(0, 5, size=(2500, 3)), columns=list('XYZ'))
#     data['sum'] = data.sum(axis=1)
#     #print(data)
    
#     est = ConstraintBasedEstimator(data)
#     skel, sep_sets = est.estimate_skeleton()
#     print(skel.edges())

#     s = ExhaustiveSearch(pd.DataFrame(data={'Temperature': [23, 19],'Weather': ['sunny', 'cloudy'],'Humidity': [65, 75]}))
#     print(len(list(s.all_dags())))
#     for dag in s.all_dags():
#         print(dag.edges())
        
    data = pd.DataFrame(np.random.randint(0, 5, size=(5000, 2)), columns=list('AB'))
    data['C'] = data['B']
    searcher = ExhaustiveSearch(data, scoring_method=K2Score(data))
    for score, model in searcher.all_scores():
        print score
        print model.edges()
        

