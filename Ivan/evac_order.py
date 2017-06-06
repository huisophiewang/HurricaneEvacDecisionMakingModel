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
rename_official = {"q43":"heard_order", 'q44':'order_type'}
rename_official_save = {"q43":"heard_order", 'q44':'order_type', 'q45':'door_to_door', 'q46':'order_first_src', 
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

map_info_src = {'none':0, 'a little':1, 'a fair amount':2, 'a great deal':3}
map_importance = {'not important':0, 'somewhat important':1, 'very important':2}



# what differ at county level?
# race distribution, income distribution, age distribution, edu, house type, house material, 
# info source?
# do I have biased sample on income
# mediation variable? 

def prep_related_vars():
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
    

    df['gender'].replace({"male":0, "female":1}, inplace=True)
    df['race'].fillna(0, inplace=True)
    df['race'].replace({"white or caucasian":1, "african american or black":2, "hispanic":3, "american indian":4, "asian":5, "other":0}, inplace=True)
    df_race = pd.get_dummies(df['race'], drop_first=True)
    df_race.rename(columns={1:'r_white', 2:'r_black', 3:'r_hispanic', 4:'r_asian', 5:'r_native'}, inplace=True)
    df['owner'].replace({"own":1, "rent":0, 'other':0}, inplace=True)
    df['pets'].fillna(0, inplace=True)
    df['pets'].replace({'yes':1, "no [skip to q108]":0}, inplace=True)
    df['income'].replace({'less than $15,000':1, '$15,000 to $24,999':2, '$25,000 to $39,999':3, '$40,000 to $79,999':4, 'over $80,000':5}, inplace=True)
    df['edu'].fillna(0, inplace=True)
    df['edu'].replace({'some high school':1, 'high school graduate':2, 'some college':3, 'college graduate':4, 'post graduate':5}, inplace=True)
    df['house_type'].fillna(0, inplace=True)
    df['house_type'].replace({'detached single family home? [go to q95]':1, 'mobile home [skip to q96]':2, 
                              'duplex, triplex, quadraplex home? [skip to q99]':3, 'multi-fam bldg 4 stories or less? [apt/condo] [skip to q99]':3,
                              'multi-fam bldg more than 4 stories [apt/condo] [skip to q99]':3, 'manufactured home [skip to q96]':0,
                              'some other type of structure [skip to q99]':0}, inplace=True)
    df_house_type = pd.get_dummies(df['house_type'], drop_first=True)
    df_house_type.rename(columns={1:'ht_single_fam', 2:'ht_mobile', 3:'ht_condo'}, inplace=True)
    df['house_material'].fillna(0, inplace=True)
    df['house_material'].replace({'wood':1, 'brick':2, 'cement block':3, 'other [specify]':0}, inplace=True)
    df_house_materi = pd.get_dummies(df['house_material'], drop_first=True)
    df_house_materi.rename(columns={1:'hm_wood', 2:'hm_brick', 3:'hm_cement'}, inplace=True)
    
    df['heard_order'].replace({'yes [go to q44]':1, 'no [go to q49]':0}, inplace=True)

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
    
    
if __name__ == '__main__':
    prep_related_vars()