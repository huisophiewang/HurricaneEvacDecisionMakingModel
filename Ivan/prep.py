import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import matplotlib

races = ['white','black','hispanic','asian','native']

def select_cols():
    df = pd.read_csv(r'IvanExport.csv')
    #print df['sname']
    
    df.rename(columns={"samp":"county", 'q1110':'race', 'q99':'age','q102':'househd_size',
                       'q103':'num_child','q104':'num_elder','q105':'owner','q106':'pets',
                       'q112':'income','q113':'edu','q2':'evac'}, inplace=True)
    cols = ['state', 'county', 'race', 'gender','age','househd_size','num_child','num_elder','owner','pets', 'income','edu','evac']
    df.to_csv('Ivan_demographic.csv', columns=cols, index=False)
    
def convert():
#     #data = np.genfromtxt(r"Ivan_by_County.csv", delimiter=",", dtype=float, skip_header=1)
#     fr = open(r"Ivan_demographic.csv", 'rU')
#     for line in fr.readlines():
#         items = line.split(',')

    df = pd.read_csv(r'Ivan_demographic.csv')
    df['race'].replace({'white or caucasian':1, 'african american or black':2, 'hispanic':3,'asian':4,'american indian':5,'other':0},inplace=True)
    df_race = pd.get_dummies(df['race'], drop_first=True)
    df_race.rename(columns={1:'white', 2:'black', 3:'hispanic', 4:'asian', 5:'native'}, inplace=True)
    #print df_race
    
    #df['evac'].replace({'yes,evacuated':1, 'no,did not evacuate':0},inplace=True)
    df_evac = pd.get_dummies(df['evac'], drop_first=True)
    df_evac.rename(columns={'yes, evacuated':'evac'}, inplace=True)
    
    df = pd.concat([df, df_race, df_evac], axis=1)
    #df.to_csv('Ivan_race.csv', columns=['white','black','hispanic','asian','american indian','yes'], index=False)
    df.to_csv('Ivan_state_race.csv', columns=['state','county','white','black','hispanic','asian','native','evac'], index=False)
    
def corr(data):
    #data = np.genfromtxt(r'Ivan_race.csv', delimiter=",", dtype=float, skip_header=1)
    #print data
    y = data[:,-1]
    for i in range(5):
        print races[i]
        x = data[:,i]
        num = np.sum(x)
        if num > 0:
            r = pearsonr(x, y)
            print r
        else:
            print 'NA'
        
def all_corr():
    df = pd.read_csv(r'Ivan_state_race.csv')

#     df_select_sum.plot.bar()
#     plt.show()
    
#     df_select = df[(df.county=='monroe county') & (df.state == 'FL')]
#     arr = df_select.as_matrix(columns=['white','black','hispanic','asian','native','evac'])
#     corr(arr)

    counties = df.county.unique()
    for county in counties:
        print '=============================================================='
        print county
        df_select = df[(df.county==county)]
        arr = df_select.as_matrix(columns=['white','black','hispanic','asian','native','evac'])
        corr(arr)

#     states = df.state.unique()
#     for state in states:
#         print '=============================================================='
#         print state
#         df_select = df[(df.state==state)]
#         arr = df_select.as_matrix(columns=['white','black','hispanic','asian','native','evac'])
#         corr(arr)

        
def contingency_table():
    df = pd.read_csv(r'Ivan_demographic.csv')
    
#     df_select = df[(df.county!='monroe county') & (df.state=='FL')]
#     table = pd.crosstab(df_select['race'],df_select['evac'])
#     percent = table.apply(lambda r: r/r.sum(), axis=1)
#     print pd.concat([table, percent], axis=1)
    
#     counties = df.county.unique()
#     for county in counties:
#         print '=============================================================='
#         print county
#         df_select = df[(df.county==county)]
#         table = pd.crosstab(df_select['race'],df_select['evac'], margins=True)
#         table = table[['no, did not evacuate',  'yes, evacuated']]  # only keep column sum
#         percent = table.apply(lambda r: r/r.sum(), axis=1)
#         print pd.concat([table, percent], axis=1)
        
    states = df.state.unique()
    for state in states:
        print '=============================================================='
        print state
        df_select = df[(df.state==state)]
        table = pd.crosstab(df_select['race'],df_select['evac'], margins=True)
        table = table[['no, did not evacuate',  'yes, evacuated']]  # only keep column sum
        percent = table.apply(lambda r: r/r.sum(), axis=1)
        print pd.concat([table, percent], axis=1)       
    
        
    
if __name__ == '__main__':
    #select_cols()
    #convert()
    
    all_corr()
    
    #contingency_table()
    
    
