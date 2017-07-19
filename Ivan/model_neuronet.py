import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler  
from pprint import pprint

if __name__ == '__main__':
    fp = 'data/Ivan_common_with_county.csv'
    data = np.genfromtxt(fp, delimiter=",", dtype=float, skip_header=1)
    x = data[:,:-1]
    y = data[:,-1]
    
    scaler = StandardScaler()  
    scaler.fit(x)  
    x = scaler.transform(x) 
    pprint(x)