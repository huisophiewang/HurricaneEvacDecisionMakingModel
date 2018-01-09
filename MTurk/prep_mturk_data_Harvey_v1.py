import pandas as pd
import numpy as np
from collections import OrderedDict
from scipy import stats
import matplotlib.pyplot as plt
import re
import os
from pprint import pprint

regex_comma_outside_parentheses = r',\s*(?![^()]*\))'

rename_demo = OrderedDict([('Q11', 'age'), ('Q12', 'is_male'), ('Q13', 'race'), ('Q14', 'edu'), ('Q15', 'income'),('Q16', 'househd_size'), 
                           ('Q17', 'has_children'), ('Q18', 'has_elders'), ('Q19', 'has_special_needs'), ('Q20', 'has_pets')])
rename_house = OrderedDict([('Q23', 'house_struct'), ('Q24', 'house_material'), ('Q25', 'is_owner'), ('Q26', 'has_insurance')])
rename_loc = OrderedDict([('Q21', 'zipcode'), ('Q22', 'coast_dist'), ('Q27', 'county')])

rename_info_tv = OrderedDict([('Q4', 'use_tv_radio'), 
                              ('Q5_1', 'tv_radio_storm_damage'), ('Q5_2', 'tv_radio_casualty'), 
                              ('Q5_3', 'tv_radio_road_traffic'), ('Q5_4', 'tv_radio_preparation'), 
                              ('Q5_5', 'tv_radio_people_stay'), ('Q5_6', 'tv_radio_people_leave')])
rename_info_social = OrderedDict([('Q6','use_social_media'), 
                                 ('Q7_1', 'social_media_storm_damage'), ('Q7_2', 'social_media_storm_strength'), 
                                 ('Q7_3', 'social_media_preparation'), ('Q7_4', 'social_media_people_stay'), 
                                 ('Q7_5', 'social_media_people_leave'), ('Q7_6', 'social_media_road_traffic')])
rename_info_other = OrderedDict([('Q8', 'friends_suggest'), ('Q9', 'neighbors_doing')])

rename_risk = OrderedDict([('Q3_1','risk_of_stay'), ('Q3_2', 'risk_of_evac'), 
                           ('Q3_3', 'wind_risk_to_safety'), ('Q3_4', 'wind_risk_to_property'), 
                           ('Q3_5', 'flood_risk_to_safety'), ('Q3_6', 'flood_risk_to_property')])
rename_evac_ability = OrderedDict([('Q10', 'evac_ability_items')])

rename_emer_service = OrderedDict([('Q36_1','emer_serv_before'), ('Q36_2', 'emer_serv_during'),('Q36_3', 'emer_serv_after')])
rename_evac_notice = OrderedDict([('Q28', 'evac_notice'), ('Q29', 'evac_notice_type'), ('Q30', 'evac_notice_how'), ('Q31', 'evac_notice_when'), ('Q32', 'stay_notice')])
rename_evac_decision = OrderedDict([('Q33', 'evac_decision'), ('Q34', 'evac_date'), ('Q35', 'evac_time'), ('Q37', 'same_choice')])

amount_to_num = {'None at all':1, 'A little':2, 'A moderate amount':3, 'A lot':4, 'A great deal':5}
yesno_to_num = {'Yes':1, 'No':0}

evac_ability_items = {'Having young children':'ability_children', 
                      'Having elderly family member(s)':'ability_elders', 
                      'Having family member(s) with special needs':'ability_special_needs', 
                      'Having pets':'ability_pets',
                      'Evacuation expense (travel, lodging, etc.)':'ability_expense', 
                      'No transportation (cars, flights, public transportation, etc)':'ability_no_transport', 
                      "No place to go (hotels, public shelters, friends' or family's places, etc.)":'ability_no_place', 
                      'Job obligations':'ability_job'}

evac_notice_how_items = ['Radio or TV', 'Social media or internet', 'Word of mouth (friends/relative/neighbor)',
                         'Police/authorities came into the neighborhood', 'Text alerts or phone calls from officials', 'Other']




def prep(input_fp, output_fp):
    df = pd.read_csv(input_fp)
    
    rename_all = OrderedDict()
    rename_all.update(rename_demo)
    rename_all.update(rename_house)
    rename_all.update(rename_loc)
    rename_all.update(rename_info_tv)
    rename_all.update(rename_info_social)
    rename_all.update(rename_info_other)
    rename_all.update(rename_risk)
    rename_all.update(rename_evac_ability)
    rename_all.update(rename_emer_service)
    rename_all.update(rename_evac_notice)
    rename_all.update(rename_evac_decision)
    
    df.rename(columns=rename_all, inplace=True)
    
    # demo
    df['is_male'].replace({"Female":0, "Male":1}, inplace=True)
    df['race'].replace({"Caucasian":1, "African American":2, "Asian":3, "Hispanic":4, "American Indian":5, "Other":0}, inplace=True)
    df_race = pd.get_dummies(df['race'], drop_first=True)
    df_race.rename(columns={1:'is_white', 2:'is_black', 3:'is_asian', 4:'is_hispanic', 5:'is_native'}, inplace=True)
    df['edu'].replace({'Some high school':0, 'High school graduate':1, 'Some college':2, 'College graduate':3, 'Graduate school':4}, inplace=True)
    df['income'].replace({'Less than $15,000':0, '$15,000 to $25,000':1, '$25,000 to $40,000':2, '$40,000 to $80,000':3, 'Over $80,000':4}, inplace=True)
    df['has_children'].replace(yesno_to_num, inplace=True)
    df['has_elders'].replace(yesno_to_num, inplace=True)
    df['has_special_needs'].replace(yesno_to_num, inplace=True)
    df['has_pets'].replace(yesno_to_num, inplace=True)
    # house
    df['house_struct'].replace({'Detached single family home':1, 'Duplex or triplex home':2, 
                                'Condo/apartment - 4 stories or less':2, 'Condo/apartment - more than 4 floors':2, 
                                'Mobile or manufactured home':3, 'Other':0}, inplace=True)
    df_house_struct = pd.get_dummies(df['house_struct'], drop_first=True)
    df_house_struct.rename(columns={1:'house_single_fam', 2:'house_condo', 3:'house_mobile'}, inplace=True)
    df['house_material'].replace({'Wood':1, 'Brick or block':2, 'Other':0}, inplace=True)
    df_house_material = pd.get_dummies(df['house_material'], drop_first=True)
    df_house_material.rename(columns={1:'house_wood', 2:'house_brick'}, inplace=True)
    df['is_owner'].replace({'Own':1, 'Rent':0}, inplace=True)
    df['has_insurance'].replace(yesno_to_num, inplace=True)
    df['coast_dist'].replace({'Within 1 mile':0, '1 to 10 mile':1, '10 to 30 miles':2,
                              '30 to 50 miles':3, '50 to 70 miles':4, 'More than 70 miles':5}, inplace=True)
    # info
    df['use_tv_radio'].replace(yesno_to_num, inplace=True)
    df['tv_radio_storm_damage'].replace(amount_to_num, inplace=True)
    df['tv_radio_casualty'].replace(amount_to_num, inplace=True)
    df['tv_radio_road_traffic'].replace(amount_to_num, inplace=True)
    df['tv_radio_preparation'].replace(amount_to_num, inplace=True)
    df['tv_radio_people_stay'].replace(amount_to_num, inplace=True)
    df['tv_radio_people_leave'].replace(amount_to_num, inplace=True)
    for col in rename_info_tv.values():
        df[col].fillna(0, inplace=True)
    
    df['use_social_media'].replace(yesno_to_num, inplace=True)
    df['social_media_storm_damage'].replace(amount_to_num, inplace=True)
    df['social_media_storm_strength'].replace(amount_to_num, inplace=True)
    df['social_media_road_traffic'].replace(amount_to_num, inplace=True)
    df['social_media_preparation'].replace(amount_to_num, inplace=True)
    df['social_media_people_stay'].replace(amount_to_num, inplace=True)
    df['social_media_people_leave'].replace(amount_to_num, inplace=True)
    for col in rename_info_social.values():
        df[col].fillna(0, inplace=True)
    
    # social
    df['friends_suggest'].replace({'Stay':1, 'Evacuate':2, 'Neither':0}, inplace=True)
    df_friends_suggest = pd.get_dummies(df['friends_suggest'], drop_first=True)
    df_friends_suggest.rename(columns={1:'friends_suggest_stay', 2:'friends_suggest_evac'}, inplace=True)
    
    df['neighbors_doing'].replace({'Stay':1, 'Evacuate':2}, inplace=True)
    df['neighbors_doing'].fillna(0, inplace=True)
    df_neighbors_doing = pd.get_dummies(df['neighbors_doing'], drop_first=True)
    df_neighbors_doing.rename(columns={1:'neighbors_stay', 2:'neighbors_evac'}, inplace=True)
    
    # risk
    df['risk_of_stay'].replace(amount_to_num, inplace=True)
    df['risk_of_evac'].replace(amount_to_num, inplace=True)
    df['wind_risk_to_safety'].replace(amount_to_num, inplace=True)
    df['wind_risk_to_property'].replace(amount_to_num, inplace=True)
    df['flood_risk_to_safety'].replace(amount_to_num, inplace=True)
    df['flood_risk_to_property'].replace(amount_to_num, inplace=True)
    
    # evac notice
    df['evac_notice'].replace({'Yes':1, 'No':2}, inplace=True)
    df['evac_notice'].fillna(0, inplace=True)
    df_evac_notice = pd.get_dummies(df['evac_notice'], drop_first=True)
    df_evac_notice.rename(columns={1:'received_evac_notice', 2:'no_evac_notice'}, inplace=True)
    
    df['evac_notice_type'].replace({'Mandatory (must)':1, 'Voluntary (should)':2}, inplace=True)
    df['evac_notice_type'].fillna(0, inplace=True)
    df_evac_notice_type = pd.get_dummies(df['evac_notice_type'], drop_first=True)
    df_evac_notice_type.rename(columns={1:'received_mandatory', 2:'received_voluntary'}, inplace=True)
    
    df['stay_notice'].replace({'Yes':1, 'No':2}, inplace=True)
    df['stay_notice'].fillna(0, inplace=True)
    df_stay_notice = pd.get_dummies(df['stay_notice'], drop_first=True)
    df_stay_notice.rename(columns={1:'received_stay_notice', 2:'no_stay_notice'}, inplace=True)
    
    df['evac_notice_when'].replace({'August 23th (Wednesday)':1, 'August 24th (Thursday)':1, 'August 25th (Friday, 1st landfall near Rockport, TX)':1,
                                    'August 26th (Saturday, weakened to Tropical Storm)':2, 'August 27th (Sunday)':2, 'August 28th (Monday)':2,
                                    'August 29th (Tuesday)':2, 'August 30th (Wednesday, last landfall at Cameron, LA, weakened to Tropical Depression':2,
                                    'August 31th (Thursday)':2, 'September 1st (Friday)':2, 'September 2nd (Saturday)':2, 'September 3rd (Sunday)':2}, inplace=True)
    df['evac_notice_when'].fillna(0, inplace=True)
    df_evac_notice_when = pd.get_dummies(df['evac_notice_when'], drop_first=True)
    df_evac_notice_when.rename(columns={1:'evac_notice_before_landfall', 2:'evac_notice_after_landfall'}, inplace=True)
    
    # decision
    df['evac_decision'].replace(yesno_to_num, inplace=True)
    df['same_choice'].replace(yesno_to_num, inplace=True)
    
    # not used
    df['evac_date'].replace({'August 23th (Wednesday)':1, 'August 24th (Thursday)':1, 'August 25th (Friday, 1st landfall near Rockport, TX)':1,
                            'August 26th (Saturday, weakened to Tropical Storm)':2, 'August 27th (Sunday)':2, 'August 28th (Monday)':2,
                            'August 29th (Tuesday)':2, 'August 30th (Wednesday, last landfall at Cameron, LA, weakened to Tropical Depression':2,
                            'August 31th (Thursday)':2, 'September 1st (Friday)':2, 'September 2nd (Saturday)':2, 'September 3rd (Sunday)':2}, inplace=True)
    df['evac_date'].fillna(0, inplace=True)
    df_evac_date = pd.get_dummies(df['evac_date'], drop_first=True)
    df_evac_date.rename(columns={1:'evac_before_landfall', 2:'evac_after_landfall'}, inplace=True)
    
    
    df['evac_time'].replace({'Morning':1, 'Afternoon':2, 'Evening':3, 'Night':4}, inplace=True)
    df['emer_serv_before'].replace(yesno_to_num, inplace=True)
    df['emer_serv_during'].replace(yesno_to_num, inplace=True)
    df['emer_serv_after'].replace(yesno_to_num, inplace=True)
    
    # evac ability
    for item in evac_ability_items.values():
        df[item] = 0
    for i, row in df.iterrows():
        items = re.split(regex_comma_outside_parentheses, row['evac_ability_items'])
        for item in items:
            if item != 'None':
                df.set_value(i, evac_ability_items[item], 1)   
            
    
    df = pd.concat([df, df_race, df_house_struct, df_house_material, 
                    df_evac_notice, df_evac_notice_type, df_evac_notice_when, df_stay_notice, df_evac_date,
                    df_friends_suggest, df_neighbors_doing], axis=1)


    all_cols = []
    # demo
    all_cols.extend(['age', 'is_male','edu','income','househd_size'])
    all_cols.extend(['is_white', 'is_black', 'is_asian', 'is_hispanic', 'is_native'])
    all_cols.extend(['has_children', 'has_elders', 'has_special_needs', 'has_pets'])
    # house
    all_cols.extend(['house_single_fam', 'house_condo', 'house_mobile'])
    all_cols.extend(['house_wood', 'house_brick'])
    all_cols.extend(['is_owner', 'has_insurance', 'coast_dist'])
    # info + social
    all_cols.extend(rename_info_tv.values())
    all_cols.extend(rename_info_social.values())
    all_cols.extend(['friends_suggest_stay', 'friends_suggest_evac', 'neighbors_stay', 'neighbors_evac'])
    # evac notice
    all_cols.extend(['received_evac_notice', 'no_evac_notice', 'received_mandatory', 'received_voluntary', 'received_stay_notice', 'no_stay_notice'])  
    all_cols.extend(['evac_notice_before_landfall', 'evac_notice_after_landfall'])  
    # risk
    all_cols.extend(rename_risk.values())
    # ability
    all_cols.extend(evac_ability_items.values())
    # decision
    all_cols.extend(['evac_decision'])

    
    print all_cols 
    for col in all_cols:
        print col
        print df[col].unique()     
        print df[col].value_counts(dropna=False)

    df1 = df[all_cols]
    #print df1
    df1.to_csv(output_fp, columns=all_cols, index=False)

    
if __name__ == '__main__':
    input_fp = os.path.join('data', 'MTurk_Harvey_Qualtrics.csv')
    output_fp = os.path.join('data', 'MTurk_Harvey_v1.csv')

    prep(input_fp, output_fp)

    #pprint(items)
#     fp = 'MTurk_Harvey_risk.csv'
#     df = pd.read_csv(fp)
#     for col in df.columns:
#         print col
#         print df[col].unique()     
#         print df[col].value_counts(dropna=False)
    