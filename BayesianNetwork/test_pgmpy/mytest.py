from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.readwrite import BIFReader
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator
import numpy as np
import pandas as pd


values = pd.DataFrame(np.random.randint(low=0, high=2, size=(1000, 5)),
                      columns=['A', 'B', 'C', 'D', 'E'])
train_data = values[:800]
predict_data = values[800:]
model = BayesianModel([('A', 'B'), ('C', 'B'), ('C', 'D'), ('B', 'E')])
model.fit(values)
predict_data = predict_data.copy()
predict_data.drop('E', axis=1, inplace=True)
#print predict_data
y_pred = model.predict(predict_data)
y_prob = model.predict_probability(predict_data)


# from pgmpy.sampling import BayesianModelSampling
# model = BayesianModel([('D', 'G'), ('I', 'G')])
# cpd_d = TabularCPD('D', 2, [[0.6], [0.4]])
# cpd_i = TabularCPD('I', 2, [[0.7], [0.3]])
# cpd_g = TabularCPD('G', 3, 
#                    [[0.3, 0.05, 0.9, 0.5], 
#                     [0.4, 0.25, 0.08, 0.3], 
#                     [0.3, 0.7, 0.02, 0.2]],
#                    ['D', 'I'], [2, 2])
# model.add_cpds(cpd_d, cpd_i, cpd_g)
# 
# infer = BayesianModelSampling(model)
# data = infer.forward_sample(500)
# #print data
# 
# model.fit(data, estimator=MaximumLikelihoodEstimator)
# for cpd in model.get_cpds():
#     print("CPD of {variable}:".format(variable=cpd.variable))
#     print(cpd)


