from pprint import pprint
from collections import OrderedDict
import numpy as np
import pandas as pd

from census_info import read_census
from generate_sample import generate_from_multinormial

def generate_bridgeport_data():
    all_tract = read_census()
    tract_coast_dist = pd.read_csv('data/census_tract_dist_to_coast.csv')
    
    total_household = 50367
    total_data = np.array([np.ones(9)])
    print total_data.shape
    #pprint(all_tract)
    for id in all_tract:

        info = all_tract[id]
        #pprint(info)
        
        n = info['Households']
        dist = OrderedDict()
        dist['is_male'] = [info['Male']]
        dist['is_white'] = [info['White Alone']]
        dist['is_black'] = [info['Black or African American Alone']]
        dist['is_hispanic'] = [info['Some Other Race Alone']]
        dist['is_asian'] = [info['Asian Alone']]
        dist['is_native'] = [info['American Indian and Alaska Native Alone']]
        dist['have_child'] = [info['Households with One or More People Under 18 Years:']]
        income0 = info['$40,000 to $44,999'] + info['$45,000 to $49,999'] + info['$50,000 to $59,999'] + \
            info['$60,000 to $74,999'] + info['$75,000 to $99,999'] + info['$100,000 to $124,999'] + \
            info['$125,000 to $149,999'] + info['$150,000 to $199,999'] + info['$200,000 or More']
        dist['income_above_40k'] = [income0]
        edu0 = info["Bachelor's Degree"] + info['Professional School Degree'] + \
            info["Master's Degree"] + info['Doctorate Degree']
        dist['college_edu'] = [edu0]
        dist['home_mobile'] = [info['Mobile Home']]
        dist['home_single_fam'] = [info['1, Detached']]
        
        #dist['home_condo'] = 
        
        data = np.array([np.ones(n)]).T
        for factor in dist:
            #print factor
            fdist = dist[factor]
            fdata = generate_from_multinormial(fdist, n)
            data = np.append(data, fdata, axis=1)
        
        d = tract_coast_dist.loc[tract_coast_dist['id']==id]['distance']
        dist_data = np.random.normal(d, 0.1, n)
        data = np.append(data, np.array([dist_data]).T, axis=1)
        #print data.shape
        total_data = np.append(total_data, data, axis=0)
        
    print total_data.shape 
     
    return total_data
    
def model_Ivan():
    # constant, is_male, is_white, is_black, is_hispanic, is_asian, 
    # have_child, income > 40k, college edu, 
    # mobile home, single family home, coast dist
    # unable to use: age (divided by range), househd_size, house material, pets, owner
    # what is condo?
   # beta = [0.0021, -0.3273, 0.0629, 0.2697, 0.0560, 0.2688, 0.9263, -0.1647, -0.0373]
    sample = generate_bridgeport_data()
    n = sample.shape[0]
    
    count = 0
    res = np.zeros(n)
    y = 0
    for i, x in enumerate(sample):
        y = np.sum(np.dot(x, beta))
        #print y
        if y > 0.5:
            res[i] = 1
            count += 1
        else:
            res[i] = 0

    #print res
    rate = sum(res) / float(n)
    print rate
       
if __name__ =='__main__':
    model_Ivan()

        