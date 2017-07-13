
import pandas
import math
from pprint import pprint
from collections import OrderedDict
from model_from_paper import evac_rate_model_Wilmot, evac_rate_model_Xu
from census_info import read_census

tract_dist_to_water = {
                       }
# distance to water > 1 mile:
# 721, 722, 723, 732
tract_not_close_to_water = [721, 722, 723, 724, 725, 726, 727, 728,
                            729, 730, 731, 732]
#(5314+4086+6306+2446=18152)


                
def calc_dist_model_Xu(all_tract):
    beta_2011voluntary = [0.6118, 0.5678, 0.0, 0.3109, 0.0, 0.4295, 0.0, 0.0, 0.0, 0.0]
    threshold_2011voluntary = [-0.2880, 0.0191, 0.4308, 1.0585, 1.7244, 2.0328]
    
    beta_2011mandatory = [1.1232, 0.8756, 0.0, 0.0, 0.0, 0.5023, 0.0, -0.2727, 0.0, 0.0]
    threshold_2011mandatory = [0.5926, 0.8231, 1.0530, 1.5108, 2.2109, 2.5860]

    for tract in all_tract:
        print '================'
        print tract
        dist = OrderedDict()
        info = all_tract[tract]
        n = info['Total Population']
        dist['to_coast'] = [1.0, 1.0]
        dist['house_type'] = [info['Mobile Home'], info['Mobile Home']+info['1, Detached']]
        dist['gender'] = [info['Male']]
        dist['race'] = [info['White Alone']]
        edu0 = info['Less than High School'] + info['High School Graduate (Includes Equivalency)']
        edu1 = edu0 + info['Some College'] + info["Bachelor's Degree"]
        dist['edu'] = [edu0, edu1]
        dist['job'] = [info['In Labor Force:']]
        dist['child'] = [info['Households with One or More People Under 18 Years:']]
        
        evac_rate_model_Xu(n, dist, beta_2011mandatory, threshold_2011mandatory)
        #evac_rate_model_Xu(n, dist, beta_2011voluntary, threshold_2011voluntary)
        
    #pprint(all_tract_dist)

    
def calc_dist_model_Wilmot(all_tract):
    beta = [1.8, 2.32, -1.05, -1.26, -0.80, 0.80, 1.44, 
        -0.04*12, -0.04*21, -0.04*30, -0.04*40, -0.04*50, -0.04*60]
    threshold = 0.36
    
    for tract in all_tract:
        print '==============='
        print tract
        dist = OrderedDict()
        info = all_tract[tract]
        n = info['Total Population']
        dist['house_type'] = [info['Mobile Home'], info['Mobile Home']+info['1, Detached']]
        dist['marriage'] = [info['Never Married'], info['Never Married']+info['Now Married (Not Including Separated)']]
        if tract in tract_not_close_to_water:
            dist['close_to_water'] = [0.0]
        else:
            dist['close_to_water'] = [1.0]
            
        dist['evac_order'] = [1.0]
        age0 = info['Under 5 Years']+info['5 to 9 Years']+info['10 to 14 Years']+info['15 to 17 Years']
        age1 = age0 + info['18 to 24 Years']
        age2 = age1 + info['25 to 34 Years']
        age3 = age2 + info['35 to 44 Years']
        age4 = age3 + info['45 to 54 Years']
        age5 = age4 + info['55 to 64 Years']
        dist['age'] = [age0, age1, age2, age3, age4, age5]
        
        evac_rate_model_Wilmot(n, dist, beta, threshold)
            

        

                
if __name__ == '__main__':
    all_tract = read_census()
    pprint(all_tract)
    #calc_dist_model_Wilmot(all_tract)
    #calc_dist_model_Xu(all_tract)

    