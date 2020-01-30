import pandas as pd
import numpy as np
from scipy import stats
from sklearn import metrics
from pprint import pprint
import matplotlib.pyplot as plt

from util import STATES, COUNTIES
    

            
def chi_square_test():
    fp = 'data/Ivan_common.csv'
    df = pd.read_csv(fp)
    total = len(df)
    vars = [x for x in df.columns.values if x not in ['evac','age', 'househd_size','coast_dist', 'elevation']]
    y = 'evac'
    var_p = {}
    for var in vars:
        #print var
        table = pd.crosstab(df[var],df[y], margins=True)
        values = sorted(df[var].unique())

        observed = np.zeros((len(values),2))
        for i, v in enumerate(values):
            if v in table.index:
                observed[i][0] = table.loc[v][0]
                observed[i][1] = table.loc[v][1]

        evac_rate = table.loc['All'][1]/ float(total)
        sum_by_var = np.sum(observed, axis=1)
          
        expected = np.zeros((len(values),2))
        for i, race in enumerate(values):
            expected[i][0] = sum_by_var[i]*(1.0-evac_rate)
            expected[i][1] = sum_by_var[i]*evac_rate
          
        stat, p = stats.chisquare(observed.flatten(),expected.flatten(), (observed.shape[0]-1)*(observed.shape[1]-1))
        #print p
        var_p[var] = p
#         chi_square = 0.0
#         for j in range(len(observed.flatten())):
#             chi_square += np.square((observed.flatten()[j] - expected.flatten()[j]))/expected.flatten()[j]
#         print chi_square
    res = sorted(var_p.items(), key=lambda x:x[1])
    pprint(res)
    
def draw_boxplot():
    fp = 'data/Ivan_common.csv'
    df = pd.read_csv(fp)
    df1 = df[['coast_dist','evac']]
    #print df1
    #df1.boxplot(by='evac')
    df1.hist()
    plt.show()
    
def correlation_test():
    fp = 'data/Ivan_common.csv'
    df = pd.read_csv(fp)
    print len(df)
    print stats.pearsonr(df['coast_dist'],df['elevation'])
    
    ###############################################################################
    # categorical vs continuous
    # point-biserial, https://www.andrews.edu/~calkins/math/edrm611/edrm13.htm#POINTB
    # https://en.wikipedia.org/wiki/Point-biserial_correlation_coefficient
    # same as using stats.pearsonr
    print stats.pointbiserialr(df['evac'], df['coast_dist'])
    print stats.pearsonr(df['coast_dist'],df['evac'])
    
    # t-test has the same p-value as point-biserial, 
    # http://web.pdx.edu/~newsomj/da1/ho_correlation%20t%20phi.pdf
    evac_yes = df[df['evac']==1]['coast_dist']
    evac_no = df[df['evac']==0]['coast_dist']
    print stats.ttest_ind(evac_yes, evac_no)
    
    ###############################################################################
    # categorical vs categorical
    # phi coefficient, special case of Cramer's V
    # https://en.wikipedia.org/wiki/Phi_coefficient
    # phi is computed using chi-square statistic
    # https://en.wikipedia.org/wiki/Matthews_correlation_coefficient, same as phi coefficient
    # same as using stats.pearsonr
    print metrics.matthews_corrcoef(df['ht_mobile'], df['evac'])
    print stats.pearsonr(df['ht_mobile'], df['evac'])
    
def pearson_corr(fp):
    
    #fp = 'data/Ivan_common_state_county.csv'
    #fp = 'data/Ivan_common_state_county_zip.csv'
    
    df = pd.read_csv(fp)
    total = len(df)
    vars = [x for x in df.columns.values if x not in['evac','state','county', 'zip']]
    
#     for state in STATES:
#         print '--------------'
#         print state
#         df1 = df[df['state'] == state]

#     for county in COUNTIES:
#         print '--------------'
#         print county
#         df1 = df[df['county'] == county]
#         #print df1.columns.values
    var_p = []
    for var in vars:
        r, p = stats.pearsonr(df[var], df['evac'])
        var_p.append((var, r, p))
    res = sorted(var_p, key=lambda x: x[2])
    pprint(res)
    

def debug():
    fp = 'data/Ivan_common_state_county_zip.csv'
    df = pd.read_csv(fp)
    
    df1 = df[df['county'] == 'bay county']
    var = 'elevation'
    print stats.pearsonr(df1[var], df1['evac'])
    
    print len(df1)
    zips = df1['zip'].unique()
    print zips
    for zip in zips:
        print df1[df1['zip']==zip][['zip','coast_dist','elevation', 'evac']]

    
    print df1.groupby([var,'evac']).size()
    

    df1.plot.scatter(x=var, y='evac')
    #df1[['coast_dist','evac']].hist()
    plt.show()
    
    
def mediation():
    fp = 'data/Ivan_common.csv'
    df = pd.read_csv(fp)
    
    # IV = sf_cat3_wind_water 
    # DV = evac
    # MD = heard_order
    
    a = stats.pearsonr(df['sf_cat3_wind_water'],df['heard_order'])
    b = stats.pearsonr(df['sf_cat3_wind_water'],df['heard_order'])
    
    
            
if __name__ == '__main__':
    #chi_square_test()

    #correlation_test()
    #fp = 'data/Ivan_common.csv'
    fp = r'C:\Users\Sophie\workspace\Hurricane\BayesianNet\Ivan_common_test3.csv'
    pearson_corr(fp)

    #debug()