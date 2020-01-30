import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import matplotlib
from collections import OrderedDict
from scipy.stats import chisquare

rename_demographic = OrderedDict([('q99','age'), ('gender','gender'),('q1110','race'), 
                      ('q102','househd_size'),('q103','num_child'),('q104','num_elder'),
                      ('q105','owner'),('q106','pets'),('q112','income'),('q113','edu')])
rename_house = OrderedDict([('q94','house_type'), ('q95','house_material')])
rename_loc = {'state':'state', 'samp':'county', 'city':'city', 'zip':'zip'}
rename_official = {"q43":"heard_order", 'q44':'order_type'}
rename_official_all = {"q43":"heard_order", 'q44':'order_type', 'q45':'door_to_door', 'q46':'order_first_src', 
                   'q47':'early_enough', 'q48':'clear_enough', "q49":"responsible"}
rename_info_src = OrderedDict([("q50a","src_local_radio"), ("q50b","src_local_tv"), 
            ("q50c","src_cable_cnn"), ("q50d","src_cable_weather_channel"), ("q50e","src_cable_other"),
            ("q50f","src_internet"), ("q50g","src_mouth")])
rename_src_importance = OrderedDict([("q58","importance_nhc"), ("q59","importance_local_media"), 
                         ("q60","trust_local_media"),('q61','seek_local_weather_office'), ('q62','see_track_map')])
rename_concern = OrderedDict([('q54','concern_wind'), ('q55','concern_fld_surge'), 
                              ('q56','concern_fld_rainfall'), ('q57','concern_tornado')])
rename_scenario = OrderedDict([('q65','sf_cat4_water'), ('q66','sf_cat4_wind_water'),
                   ('q67','sf_cat3_water'), ('q68','sf_cat3_wind_water'),
                   ('q69','sf_cat2_water'), ('q70','sf_cat2_wind_water')])
rename_evac = {'q2':'evac'}

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
    df = pd.read_csv(r'data/Ivan_state_race.csv')

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
    df = pd.read_csv(r'data/Ivan_demographic.csv')
   
#     df_select = df[(df.county!='monroe county') & (df.state=='FL')]
#     table = pd.crosstab(df_select['race'],df_select['evac'])
#     percent = table.apply(lambda r: r/r.sum(), axis=1)
#     print pd.concat([table, percent], axis=1)
    
    counties = df.county.unique()
    for county in counties:
        print '=============================================================='
        print county
        df_select = df[(df.county==county)]
        table = pd.crosstab(df_select['race'],df_select['evac'], margins=True)
        table = table[['no, did not evacuate',  'yes, evacuated']]  # only keep column sum
        percent = table.apply(lambda r: r/r.sum(), axis=1)
        print pd.concat([table, percent], axis=1)

        
        
#     states = df.state.unique()
#     for state in states:
#         print '=============================================================='
#         print state
#         df_select = df[(df.state==state)]
#         table = pd.crosstab(df_select['race'],df_select['evac'], margins=True)
#         table = table[['no, did not evacuate',  'yes, evacuated']]  # only keep column sum
#         percent = table.apply(lambda r: r/r.sum(), axis=1)
#         print pd.concat([table, percent], axis=1)       
    
        
def chi_square_test():
    df = pd.read_csv(r'data/IvanExport.csv')
    rename_all = {}
    rename_all.update(rename_demographic)
    rename_all.update(rename_loc)
    rename_all.update(rename_official_all)
    rename_all.update(rename_evac)
    df.rename(columns=rename_all, inplace=True)
    df['evac'].replace({'yes, evacuated':'yes','no, did not evacuate':'no'}, inplace=True)
    df['race'].replace({"white or caucasian":'white', "african american or black":'black', "hispanic":'hispanic', 
                        "american indian":'native', "asian":'asian', "other":'other'}, inplace=True)
    
    df = df[['county', 'race', 'evac']]
    df['race'].fillna('other', inplace=True)
    #print df
    counties = ['monroe county', 
                'bay county', 'escambia county', 'franklin county', 'gulf county',  'inland counties', 'okaloosa county',   'santa rosa county', 'walton county',
                'baldwin county','mobile county',
                'hancock county', 'harrison county','jackson county',
                'orleans parish', 'jefferson parish', 'plaquemines parish','st. bernard parish', 'st. charles parish', 'st. john the baptist parish', 'st. tammany parish']

    #county = 'bay county' 
    for county in counties:
        print '========================'
        print county
        df_select = df[(df.county==county)]
        table = pd.crosstab(df_select['race'],df_select['evac'], margins=True)
    #     
        #races = ['white','black','hispanic', 'asian', 'native', 'other']
        races = ['white','black']
        observed = np.zeros((len(races),2))
        for i, race in enumerate(races):
            if race in table.index:
                observed[i][0] = table.loc[race]['no']
                observed[i][1] = table.loc[race]['yes']
        print observed
        
        evac_total = np.sum(observed, axis=0)
        evac_by_race = np.sum(observed, axis=1)
        evac_rate = evac_total[1] / float(sum(evac_total))
        
        expected = np.zeros((len(races),2))
        for i, race in enumerate(races):
            expected[i][0] = evac_by_race[i]*(1.0-evac_rate)
            expected[i][1] = evac_by_race[i]*evac_rate
        print expected
        
        print chisquare(observed.flatten(),expected.flatten(), (observed.shape[0]-1)*(observed.shape[1]-1))
        
        chi_square = 0.0
        for j in range(len(observed.flatten())):
            chi_square += np.square((observed.flatten()[j] - expected.flatten()[j]))/expected.flatten()[j]
        print chi_square
            

    
            
if __name__ == '__main__':
    #select_cols()
    #convert()
    
    #all_corr()
    #contingency_table()
    chi_square_test()
    
    
