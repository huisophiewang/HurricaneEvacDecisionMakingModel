import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import OrderedDict
from pprint import pprint
import pylab 
import scipy.stats as stats
from scipy.stats.stats import pearsonr

rename_demographic = OrderedDict([('q99','age'), ('gender','gender'),('q1110','race'), 
                      ('q102','househd_size'),('q103','num_child'),('q104','num_elder'),
                      ('q105','owner'),('q106','pets'),('q112','income'),('q113','edu')])
rename_house = OrderedDict([('q94','house_type'), ('q95','house_material')])
rename_loc = {'state':'state', 'samp':'county', 'city':'city', 'zip':'zip'}
rename_official = {"q43":"heard_order", 'q44':'order_type', 'q49a':'know_evac_zone', 'q49b':'in_evac_zone'}
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

########################################################################################
# evac zone (q49a, q49b)

map_info_src = {'none':0, 'a little':1, 'a fair amount':2, 'a great deal':3}
map_importance = {'not important':0, 'somewhat important':1, 'very important':2}

def one_var_plot():
    df = pd.read_csv(os.path.join('data', 'IvanExport.csv'))
    rename_all = {}
    rename_all.update(rename_demographic)
    rename_all.update(rename_house)
    rename_all.update(rename_official_all)
    df.rename(columns=rename_all, inplace=True)
    
#     # numerical var, use histogram
#     var = 'num_child'
#     df.hist(column=var)
#     plt.show()
    
    # categorical var, use bar plot
    var = 'responsible'
    print df[var].unique()
    df1 = df[var].value_counts(dropna=False)
    #df1 = df.groupby(var).size()
    print df1
    df1.plot(kind='bar', rot=0)
    plt.show()
    
    # Q-Q plot
#     df1 = df['age'].dropna()
#     stats.probplot(df1, dist="norm", plot=pylab)
#     pylab.show()
    
    
def two_var_bar_plot_special():
    df = pd.read_csv(os.path.join('data', 'IvanExport_dist.csv'))
    pprint(df.columns)
    
    rename_all = {}
    rename_all.update(rename_demographic)
    rename_all.update(rename_loc)
    rename_all.update(rename_official_all)
    rename_all.update(rename_evac)
    df.rename(columns=rename_all, inplace=True)


    row_var  = 'county'
    #col_var = 'race'
#     col_val = 'heard_order'
    col_var = 'responsible'
#     col_var = 'race'
    col_var = 'income'
    df['income'].replace({'less than $15,000':'$15,000 and less', 'over $80,000':'$80,000 and more'}, inplace=True)
    
    df = df[[row_var, col_var]]
    county_sample_size = df[row_var].value_counts(dropna=False)
    df.fillna(-1, inplace=True) #because groupby doesn't show NA
    df1 = df.groupby([row_var, col_var]).size()
    #print df1
    
    counties = sorted(df[row_var].unique())
    entities = sorted(df[col_var].unique())
    #print counties
    counties = ['monroe county', 
                'bay county', 'escambia county', 'franklin county', 'gulf county',  'inland counties', 'okaloosa county',   'santa rosa county', 'walton county',
                'baldwin county','mobile county',
                'hancock county', 'harrison county','jackson county',
                'orleans parish', 'jefferson parish', 'plaquemines parish','st. bernard parish', 'st. charles parish', 'st. john the baptist parish', 'st. tammany parish']


    vals = np.zeros((len(counties), len(entities)))
    for i, county in enumerate(counties):
        for j, entity in enumerate(entities):
            if entity in df1[county]:
                vals[i][j] = df1[county][entity]
    #print vals

    df2 = pd.DataFrame(vals, counties, entities)
    df2.plot(kind='bar', rot=-90)
    plt.show()

def two_var_bar_plot():
    df = pd.read_csv(os.path.join('data', 'IvanExport.csv'))
    
    rename_all = {}
    rename_all.update(rename_demographic)
    rename_all.update(rename_loc)
    rename_all.update(rename_official_all)
    df.rename(columns=rename_all, inplace=True)
    row_var  = 'county'
    col_var = 'heard_order'
    df1 = df.groupby([row_var, col_var]).size()
    rows = df1.index.get_level_values(row_var).unique().values
    cols = df1.index.get_level_values(col_var).unique() 
    vals = df1.values.reshape(len(rows),len(cols))
    print vals
    print vals.shape
    print type(vals)
    df2 = pd.DataFrame(vals, rows, cols)
    df2.plot(kind='bar', rot=-90)
    plt.show()
    
def corr():
    #df = pd.read_csv('Ivan_basic.csv')
    df = pd.read_csv('data/Ivan_common.csv')
    v1 = 'heard_order'
    v1 = 'coast_dist'
    v1 = 'pets'
    
    v2 = 'evac'
    df1 = df[[v1, v2]]
    #print df1
    df1.fillna(0, inplace=True)
    #df1[v1].replace({0:0, 1:1,2:1,3:1,4:1,5:1,6:1,7:1},inplace=True)
    #print df1[v1].unique()
    #print df1.corr('pearson')
    print pearsonr(df1[v1],df1[v2])
    
def generate_sample(dist, size):
    #np.random.seed(seed=0)
    samples = np.random.sample(size)
    #print samples
    num = len(dist)
    result = np.zeros((size, num))

    for i, s in enumerate(samples):
        for j, p in enumerate(dist):
            if s < p:
                result[i][j] = 1
                break
    return result
    
################################################
# convert categorical var to dummy vars, fill in missing values
def prep():
    df = pd.read_csv(os.path.join('data', 'IvanExport_dist.csv'))
    
    rename_all = OrderedDict()
    rename_all.update(rename_demographic)
    rename_all.update(rename_house)
    rename_all.update(rename_official)
    rename_all.update(rename_info_src)
    rename_all.update(rename_src_importance)
    rename_all.update(rename_concern)
    rename_all.update(rename_scenario)
    rename_all.update(rename_evac)

    cols = rename_all.values()
    df.rename(columns=rename_all, inplace=True)
    #pprint(cols)
    
#     for col in cols:
#         var = col
#         print '----------------------'
#         print var
#         print df[var].unique()
#         print df[var].value_counts(dropna=False)
    #print df
    
    df['gender'].replace({"male":0, "female":1}, inplace=True)
    df['race'].fillna(0, inplace=True)
    df['race'].replace({"white or caucasian":1, "african american or black":2, "hispanic":3, "american indian":4, "asian":5, "other":0}, inplace=True)
    df_race = pd.get_dummies(df['race'], drop_first=True)
    df_race.rename(columns={1:'r_white', 2:'r_black', 3:'r_hispanic', 4:'r_asian', 5:'r_native'}, inplace=True)
    df['owner'].replace({"own":1, "rent":0, 'other':0}, inplace=True)
    df['pets'].fillna(0, inplace=True)
    df['pets'].replace({'yes':1, "no [skip to q108]":0}, inplace=True)
    df['income'].replace({'less than $15,000':0, '$15,000 to $24,999':0, '$25,000 to $39,999':0, '$40,000 to $79,999':1, 'over $80,000':1}, inplace=True)
    df['edu'].fillna(0, inplace=True)
    df['edu'].replace({'some high school':0, 'high school graduate':0, 'some college':0, 'college graduate':1, 'post graduate':1}, inplace=True)
    df_edu = pd.get_dummies(df['edu'],  drop_first=True)
    df_edu.rename(columns={1:'college'}, inplace=True)
    df['house_type'].fillna(0, inplace=True)
    df['house_type'].replace({'detached single family home? [go to q95]':1, 'mobile home [skip to q96]':2, 
                              'duplex, triplex, quadraplex home? [skip to q99]':3, 'multi-fam bldg 4 stories or less? [apt/condo] [skip to q99]':3,
                              'multi-fam bldg more than 4 stories [apt/condo] [skip to q99]':3, 'manufactured home [skip to q96]':0,
                              'some other type of structure [skip to q99]':0}, inplace=True)
    df_house_type = pd.get_dummies(df['house_type'], drop_first=True)
    df_house_type.rename(columns={1:'ht_single_fam', 2:'ht_mobile', 3:'ht_condo'}, inplace=True)
    df['house_material'].fillna(0, inplace=True)
    df['house_material'].replace({'wood':1, 'brick':2, 'cement block':2, 'other [specify]':0}, inplace=True)
    df_house_materi = pd.get_dummies(df['house_material'], drop_first=True)
    df_house_materi.rename(columns={1:'hm_wood', 2:'hm_brick_cement'}, inplace=True)
    
    df['heard_order'].replace({'yes [go to q44]':1, 'no [go to q49]':0}, inplace=True)
    df['order_type'].fillna(0, inplace=True)
    df['order_type'].replace({'should evacuate':1, 'mandatory':2},inplace=True)
    df_order_type = pd.get_dummies(df['order_type'], drop_first=True)
    df_order_type.rename(columns={1:'od_voluntary', 2:'od_mandatory'}, inplace=True)
    df['know_evac_zone'].replace({'yes, i knew':1, 'no, did not know if home was in evacuation zone or not':0}, inplace=True)
    df['in_evac_zone'].fillna(0, inplace=True)
    df['in_evac_zone'].replace({'yes, home was in evacuation zone':1, 'no, home was not in evacuation zone':2}, inplace=True)
    df_in_evac_zone = pd.get_dummies(df['in_evac_zone'], drop_first=True)
    df_in_evac_zone.rename(columns={1:'ez_in_zone', 2:'ez_not_in_zone'}, inplace=True)

    #print df['heard_order'].value_counts(dropna=False)
    df['src_local_radio'].replace(map_info_src, inplace=True)
    df['src_local_tv'].replace(map_info_src, inplace=True)
    df['src_cable_cnn'].replace(map_info_src, inplace=True)
    df['src_cable_weather_channel'].replace(map_info_src, inplace=True)
    df['src_cable_other'].replace(map_info_src, inplace=True)
    df['src_internet'].replace(map_info_src, inplace=True)
    #df['src_mouth'] raw data was coded differently

    df['importance_nhc'].replace(map_importance, inplace=True)
    df['importance_local_media'].replace(map_importance, inplace=True)
    df['trust_local_media'].replace({'yes':1, 'no':0},inplace=True)
    df['seek_local_weather_office'].replace({'yes':1, 'no':0},inplace=True)
    df['see_track_map'].replace({'yes':1, 'no [skip to q65]':0},inplace=True)
    
    df['concern_wind'].replace(map_importance, inplace=True)
    df['concern_fld_surge'].replace(map_importance, inplace=True)
    df['concern_fld_rainfall'].replace(map_importance, inplace=True)
    df['concern_tornado'].replace(map_importance, inplace=True)
    
    # the question is actually about threat, therefore reverse yes no
    df['sf_cat4_water'].replace({'yes':0, 'no':1},inplace=True)
    df['sf_cat3_water'].replace({'yes':0, 'no':1},inplace=True)
    df['sf_cat2_water'].replace({'yes':0, 'no':1},inplace=True)
    df['sf_cat4_wind_water'].replace({'yes':1, 'no':0}, inplace=True)
    df['sf_cat3_wind_water'].replace({'yes':1, 'no':0}, inplace=True)
    df['sf_cat2_wind_water'].replace({'yes':1, 'no':0}, inplace=True)
    
    df['evac'].replace({'yes, evacuated':1,'no, did not evacuate':0}, inplace=True)
    
    
    
    df = pd.concat([df, df_race, df_edu, df_house_type, df_house_materi, df_order_type, df_in_evac_zone], axis=1)
    
    ##################################################
    # age, fill in using normal distribution 
    # num_child, num_elder, set to 0 if househd_size=1
    c1 = df['age'].dropna()
    mu = np.mean(c1)
    sigma = np.sqrt(np.var(c1))
    np.random.seed(1)
    samples_age = np.random.normal(mu, sigma, 3200-len(c1))
    
    c2 = df['income'].dropna()
    income_table = c2.value_counts()
    high_rate = income_table.loc[1.0] / float(sum(income_table))
    income_sample_size = 3200-len(c2)
    np.random.seed(1)
    samples = np.random.sample(income_sample_size)    
    sample_income = np.zeros(income_sample_size)
    for i, s in enumerate(samples):
        if s < high_rate:
            sample_income[i] = 1

    j = 0 
    k = 0
    for i, row in df.iterrows():
        if pd.isnull(row['age']):
            df.set_value(i, 'age', int(samples_age[j]))
            j += 1
            
        if pd.isnull(row['income']):
            df.set_value(i, 'income', sample_income[k])
            k += 1

        if row['househd_size'] == 1:
            df.set_value(i, 'num_child', 0)
            df.set_value(i, 'num_elder', 0)
            

    ##################################################
 
    cols = ['age', 'gender','r_white', 'r_black', 'r_hispanic', 'r_asian', 'r_native',
            'househd_size', 'num_child', 'num_elder', 
            'income','edu','owner','pets',
            'ht_single_fam', 'ht_mobile', 'ht_condo',
            'hm_wood', 'hm_brick_cement',
            'coast_dist',
            'heard_order', 'od_voluntary', 'od_mandatory',
            'know_evac_zone', 'ez_in_zone', 'ez_not_in_zone',
#            'src_local_radio', 'src_local_tv', 'src_cable_cnn', 'src_cable_weather_channel', 'src_cable_other', 'src_internet',
#            'importance_nhc', 'importance_local_media', 'trust_local_media', 'seek_local_weather_office', 'see_track_map',
#            'concern_wind', 'concern_fld_surge', 'concern_fld_rainfall', 'concern_tornado',
#           'sf_cat4_water','sf_cat4_wind_water','sf_cat3_water','sf_cat3_wind_water','sf_cat2_water','sf_cat2_wind_water',
            'evac']
    
#     cols = ['age', 'gender','r_white', 'r_black', 'r_hispanic', 'r_asian', 'r_native',
#             'househd_size', 'num_child', 'num_elder', 
#             'income','edu','owner','pets',
#             'ht_single_fam', 'ht_mobile', 'ht_condo',
#             'hm_wood', 'hm_brick_cement',
#             'coast_dist',
#             'heard_order', 'od_voluntary', 'od_mandatory',
#             'know_evac_zone', 'ez_in_zone', 'ez_not_in_zone',
#             'src_local_radio', 'src_local_tv', 'src_cable_cnn', 'src_cable_weather_channel', 'src_cable_other', 'src_internet',
#             'importance_nhc', 'importance_local_media', 'trust_local_media', 'seek_local_weather_office', 'see_track_map',
#             'evac']

    df1 = df[cols].dropna()
    print len(df1)
    
    df1.to_csv('data/Ivan_common_only_demographic.csv', columns=cols, index=False)
    


    
if __name__ == '__main__':
    

    #one_var_plot()
    #two_var_bar_plot()
    #two_var_bar_plot_special()
    #corr()
    prep()
    

    
