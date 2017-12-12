import os
import pandas as pd
import numpy as np
from pgmpy import models, estimators

if __name__ == '__main__':
    fp = os.path.join('data', 'MTurk_Harvey.csv')
    df = pd.read_csv(fp)
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:,:-1]
    y = data[:,-1]