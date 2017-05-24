from xlrd import open_workbook
import pandas
import math
from pprint import pprint
from collections import OrderedDict
from data_generation import evac_rate_model_Wilmot, evac_rate_model_Xu


tract_ids = [701, 702, 703, 704, 705, 706, 709, 710,
          711, 712, 713, 714, 716, 719, 720, 721,
          722, 723, 724, 725, 726, 727, 728, 729, 
          730, 731, 732, 733, 734, 735, 736, 737, 
          738, 739, 740, 743, 744, 2572]

tract_dist_to_water = {
                       }
# distance to water > 1 mile:
# 721, 722, 723, 732
tract_not_close_to_water = [721, 722, 723, 724, 725, 726, 727, 728,
                            729, 730, 731, 732]
#(5314+4086+6306+2446=18152)


factors = ['Male', 'White Alone', 'Households with One or More People Under 18 Years:', 'In Labor Force:', 
           'Less than High School', 'High School Graduate (Includes Equivalency)', 'Some College', 
           "Bachelor's Degree", "Master's Degree", 'Professional School Degree', 'Doctorate Degree',
           'Mobile Home','1, Detached', 
           'Never Married', 'Now Married (Not Including Separated)',
           'Under 5 Years', '5 to 9 Years', '10 to 14 Years', '15 to 17 Years', '18 to 24 Years', '25 to 34 Years',
           '35 to 44 Years', '45 to 54 Years', '55 to 64 Years', '65 to 74 Years', '75 to 84 Years', '85 Years and Over'
           ]


def xlrd_read():
    wb = open_workbook('BridgeportCensus.xlsx')
    for sheet in wb.sheets():
    
        for r in range(sheet.nrows):
            for c in range(sheet.ncols):
                v = sheet.cell(r, c).value
                print v
                

def pandas_read():    
    df = pandas.read_excel('BridgeportCensus.xlsx')     

    #for i, row in df.iterrows():
    fields = list(df.index)
    print fields
    
    all_tract = {}
    for i, col in enumerate(df):
        if i >= 76:
            continue

        if i%2==0:
            tract_pop = {}
            for j, row in enumerate(df[col]):
                if fields[j] == 'Statistics':
                    tract = int(row.split(',')[0].split()[-1])
                if fields[j] == 'Total Population':
                    tract_pop[fields[j]] = row
            all_tract[tract] = tract_pop
        if i%2==1:
            tract_info = {}
            for j, row in enumerate(df[col]):
                # if fields[j] is not nan
                if isinstance(fields[j], basestring):
                    if fields[j] in factors:
                        tract_info[fields[j]] = row
            tract = tract_ids[int(i/2)]
#         if not tract in all_tract:
#             all_tract[tract] = []
            all_tract[tract].update(tract_info)
        #all_tract.update({tract:tract_qa})
    #pprint(all_tract)
    #print len(all_tract)
    return all_tract
            
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
    all_tract = pandas_read()
    calc_dist_model_Wilmot(all_tract)
    #calc_dist_model_Xu(all_tract)

    