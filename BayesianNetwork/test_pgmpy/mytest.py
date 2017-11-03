from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
from pgmpy.readwrite import BIFReader
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator

import numpy as np
import pandas as pd


import numpy as np
import pandas as pd
from pgmpy.models import BayesianModel

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
print y_pred
y_prob = model.predict_probability(predict_data)
print y_prob

