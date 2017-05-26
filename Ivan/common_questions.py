import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

rename_demographic = {'q99':'age', 'gender':'gender','q1110':'race', 
                      'q102':'househd_size','q103':'num_child','q104':'num_elder',
                      'q105':'owner','q106':'pets','q112':'income','q113':'edu',
                      'q94':'house_type', 'q95':'house_material',
                      'q2':'evac'}
rename_loc = {'state':'state', 'samp':'county', 'city':'city', 'zip':'zip'}
rename_official = {"q43":"heard_order"}
rename_official_save = {"q43":"heard_order", 'q44':'order_type', 'q45':'door_to_door', 'q46':'order_first_src', 
                   'q47':'early_enough', 'q48':'clear_enough', "q49":"responsible"}
rename_info_src = {"q50a":"src_local_radio", "q50b":"src_local_tv", 
            "q50c":"src_cable_cnn", "q50d":"src_cable_weather_channel", "q50e":"src_cable_other",
            "q50f":"src_internet", "q50g":"src_mouth",
            "q58":"importance_nhc", "q59":"importance_local_media", "q60":"trust_local_media", 
            'q61':'seek_local_weather_office', 'q62':'see_track_map'}
rename_concern = {'q54':'concern_wind', 'q55':'concern_fld_surge', 'q56':'concern_fld_rainfall', 'q57':'concern_fld_tornado'}
rename_scenario = {'q65':'cat4_water', 'q66':'cat4_wind_water',
                   'q67':'cat3_water', 'q68':'cat3_wind_water',
                   'q69':'cat2_water', 'q70':'cat2_wind_water'}
    
def sel_cols():
    df = pd.read_csv(os.path.join('data', 'IvanExport.csv'))
    
    rename_all = {}
    rename_all.update(rename_demographic)
    rename_all.update(rename_official)
    rename_all.update(rename_info_src)
    rename_all.update(rename_concern)
    rename_all.update(rename_scenario)
    #print rename_all.values()
    df.rename(columns=rename_all, inplace=True)
    #print df
    df['gender'].replace({"male":0, "female":1}, inplace=True)
    df['race'].replace({"white or caucasian":1, "african american or black":2, "hispanic":3, "american indian":4, "asian":5, "other":0}, inplace=True)
    df_race = pd.get_dummies(df['race'], drop_first=True)
    df_race.rename(columns={1:'r_white', 2:'r_black', 3:'r_hispanic', 4.0:'r_asian', 5.0:'r_native'}, inplace=True)
    df['owner'].replace({"own":1, "rent":0, 'other':0}, inplace=True)
    df['pets'].replace({'yes':1, "no [skip to q108]":0}, inplace=True)
    df['income'].replace({'less than $15,000':1, '$15,000 to $24,999':2, '$25,000 to $39,999':3, '$40,000 to $79,999':4, 'over $80,000':5}, inplace=True)
    df['edu'].replace({'some high school':1, 'high school graduate':2, 'some college':3, 'college graduate':4, 'post graduate':5}, inplace=True)
    df['house_type'].replace({'detached single family home? [go to q95]':1, 'mobile home [skip to q96]':2, 
                              'duplex, triplex, quadraplex home? [skip to q99]':3, 'multi-fam bldg 4 stories or less? [apt/condo] [skip to q99]':4,
                              'multi-fam bldg more than 4 stories [apt/condo] [skip to q99]':4, 'manufactured home [skip to q96]':0,
                              'some other type of structure [skip to q99]':0}, inplace=True)
    
    print df['house_type']
def bar_plot():
    df = pd.read_csv(os.path.join('data', 'IvanExport.csv'))
    
    rename_all = {}
    rename_all.update(rename_loc)
    rename_all.update(rename_official)
    df.rename(columns=rename_all, inplace=True)


    row_var  = 'county'
    col_var = 'clear_enough'

    df1 = df.groupby([row_var, col_var]).size()
    print df1
    print df1.shape
    rows = df1.index.get_level_values(row_var).unique().values
    cols = df1.index.get_level_values(col_var).unique().values
    print cols
    vals = df1.values.reshape(len(rows),len(cols))
    df2 = pd.DataFrame(vals, rows, cols)
    df2.plot(kind='bar', rot=-90)
    plt.show()
    


    
if __name__ == '__main__':
    

    #bar_plot()
    sel_cols()
    