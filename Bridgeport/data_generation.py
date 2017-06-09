import numpy as np
from collections import OrderedDict
from pprint import pprint
import os


def generate_sample(dist, size, integer=True):
    #np.random.seed(seed=0)
    samples = np.random.sample(size)
    #print samples
    num = len(dist)
    if integer:
        result = np.zeros((size, num))
    else:
        result = np.chararray((size, num))
        result[:] = 'a'
    for i, s in enumerate(samples):
        for j, p in enumerate(dist):
            if s < p:
                if integer:
                    result[i][j] = 1
                else:
                    result[i,j] = 'b'
                break
    return result

def write_sample(data, dist):
    output_fp = "sample.csv"
    labels = []
    for k in dist:
        if len(dist[k]) == 1:
            labels.append(k)
        else:
            labels.extend(["%s_%d" % (k, i) for i in range(len(dist[k]))])
    labels.append('evac')
    #np.savetxt(output_fp, data, fmt='%d', delimiter=",", header=','.join(labels))
    np.savetxt(output_fp, data, fmt='%s', delimiter=",", header=','.join(labels))
   
            
def evac_rate_model_Xu(n, dist, beta, threshold):
    data = np.array([np.arange(n)+1]).T
    for factor in dist:
        #print factor
        fdist = dist[factor]
        fdata = generate_sample(fdist, n)
        data = np.append(data, fdata, axis=1)


    cat = np.zeros(n)
    for i, x in enumerate(data[:,1:]):
        #x_int = [1 if s=='b' else 0 for s in x]
        y = np.sum(np.dot(x, beta))
        #print y
        cat[i] = len(threshold) + 1
        for j, alpha in enumerate(threshold):
            if y < alpha:
                cat[i] = j+1
                break 
    
    #cat_str = ['y' if c>=3 else 'n' for c in cat]
    #data = np.append(data, np.array([cat_str]).T, axis=1)
    #write_sample(data[:,1:], dist)
    
    evac = {}
    for c in cat:
        if not c in evac:
            evac[c] = 0
        evac[c] += 1
    for c in evac:
        evac[c] /= float(len(cat))
    print evac
    
    if 4.0 in evac and 5.0 in evac:
        evac_cat3 = 1.0 - evac[4.0] - evac[5.0]
        evac_cat4 = 1.0 - evac[5.0]
    
    print evac_cat3
    
def model_Xu():
    ### sample size
    n = 147340 # population
    n = 50367 # household
    ### prob distribution from census
    dist = OrderedDict()
    dist['to_coast'] = [1.0, 1.0]
    #dist['to_coast'] = [0.33, 0.66]     # <10 miles; 10 to 30 mile; >30 miles
    dist['house_type'] = [0.001, 0.255] # mobile; single family detached; other
    dist['gender'] = [0.485]            # male; female
    dist['race'] = [0.404]              # white; other
    dist['edu'] = [0.568, 0.934]        # less than 2 year college; 2 to 4 year college; graduate degree
    dist['job'] = [0.695]               # has full or part-time job; other
    dist['child'] = [0.363]             # has one or more children; other
#             'age': [0.246, 0.366, 0.536, 0.67, 0.797, 0.903, 0.956, 0.984],
#             'income': [0.257, 0.388, 0.482, 0.577, 0.65, 0.741, 0.857]

    
    ### Xu's model, 2011 landline:
    beta_2011mandatory = [1.1232, 0.8756, 0.0, 0.0, 0.0, 0.5023, 0.0, -0.2727, 0.0, 0.0]
    threshold_2011mandatory = [0.5926, 0.8231, 1.0530, 1.5108, 2.2109, 2.5860]
    
    beta_2011voluntary = [0.6118, 0.5678, 0.0, 0.3109, 0.0, 0.4295, 0.0, 0.0, 0.0, 0.0]
    threshold_2011voluntary = [-0.2880, 0.0191, 0.4308, 1.0585, 1.7244, 2.0328]
    
    evac_rate_model_Xu(n, dist, beta_2011mandatory, threshold_2011mandatory)
    #evac_rate_model_Xu(n, dist, beta_2011voluntary, threshold_2011voluntary)
    
    #print generate_sample([1.0, 1.0], 100)
    #write_sample(dist)
    
def evac_rate_model_Wilmot(n, dist, beta, threshold):
    data = np.array([np.ones(n)]).T
    for factor in dist:
        print factor
        fdist = dist[factor]
        fdata = generate_sample(fdist, n)
        data = np.append(data, fdata, axis=1)

    print data.shape
    print data
    count = 0
    res = np.zeros(n)
    y = 0
    for i, x in enumerate(data):
        y = np.sum(np.dot(x, beta))
        #print y
        if y > threshold:
            res[i] = 1
            count += 1
        else:
            res[i] = 0

    #print res
    rate = sum(res) / float(n)
    print rate
    
def model_Wilmot():
    n = 147340 # population
    n = 50367 # household
    dist = OrderedDict()
    dist['house_type'] = [0.001, 0.255] # mobile; single family detached; other
    dist['marriage'] = [0.478, 0.810] # never married; now married; other
    dist['close_to_water'] = [0.877]
    # no mandatory evacuation order
    dist['evac_order'] = [0.0]
    dist['age'] = [0.246, 0.366, 0.536, 0.670, 0.797, 0.903] # <18; 18-25; 25-35; 35-45; 45-55; 55-65; >65 
   
    # beta for cat 3 hurricane
    # constant, mobile, single-fam, single, married, distance, evac_order, age
    beta = [1.8, 2.32, -1.05, -1.26, -0.80, 0.80, 1.44, 
            -0.04*12, -0.04*21, -0.04*30, -0.04*40, -0.04*50, -0.04*60]
    #eg1 = [1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, ]
    #print np.dot(beta_cat3, eg1)
    threshold = 0.36
    evac_rate_model_Wilmot(n, dist, beta, threshold)
    

    
        
if __name__ == '__main__':
    model_Xu()
    #model_Wilmot()

    


    