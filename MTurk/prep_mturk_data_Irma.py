import pandas as pd
import numpy as np
from collections import OrderedDict
from scipy import stats
import matplotlib.pyplot as plt
import re
import os
from pprint import pprint

regex_comma_outside_parentheses = r',\s*(?![^()]*\))'

rename_demo = OrderedDict([('Q17', 'age'), ('Q18', 'is_male'), ('Q19', 'race'), ('Q20', 'edu'), ('Q21', 'income'),('Q22', 'househd_size'), 
                           ('Q23', 'has_children'), ('Q24', 'has_elders'), ('Q25', 'has_special_needs'), ('Q26', 'has_pets')])

rename_house = OrderedDict([('Q29', 'house_struct'), ('Q30', 'house_material'), ('Q31', 'is_owner'), ('Q32', 'has_insurance')])

rename_loc = OrderedDict([('Q16', 'current_zipcode'), ('Q27', 'preIrma_zipcode'), ('Q28', 'coast_dist'), ('Q33', 'county')])



rename_info_tv = OrderedDict([('Q3', 'use_tv_radio'), 
                              ('Q4_1', 'tv_radio_storm_damage'), ('Q4_2', 'tv_radio_casualty'), 
                              ('Q4_3', 'tv_radio_road_traffic'), ('Q4_4', 'tv_radio_preparation'), 
                              ('Q4_5', 'tv_radio_people_stay'), ('Q4_6', 'tv_radio_people_leave')])

rename_info_social = OrderedDict([('Q5','use_social_media'), 
                                 ('Q6_1', 'social_media_storm_damage'), ('Q6_2', 'social_media_storm_strength'), 
                                 ('Q6_3', 'social_media_preparation'), ('Q6_4', 'social_media_people_stay'), 
                                 ('Q6_5', 'social_media_people_leave'), ('Q6_6', 'social_media_road_traffic')])

rename_info_other = OrderedDict([('Q7', 'friends_suggest'), ('Q8', 'neighbors_doing')])

rename_harvey = OrderedDict([('Q10', 'harvey_influence_amount'), ('Q11', 'harvey_influence_direction')])

rename_prev_exp = OrderedDict([('Q12', 'has_prev_exp'), ('Q13', 'prev_decision_year'), 
                               ('Q14', 'prev_decision'), ('Q15', 'prev_decision_same_choice')])

rename_risk = OrderedDict([('Q2_1','risk_of_stay'), ('Q2_2', 'risk_of_evac'), 
                           ('Q2_3', 'wind_risk_to_safety'), ('Q2_4', 'wind_risk_to_property'), 
                           ('Q2_5', 'flood_risk_to_safety'), ('Q2_6', 'flood_risk_to_property')])

rename_evac_ability = OrderedDict([('Q9', 'evac_ability_items')])

rename_evac_notice = OrderedDict([('Q34', 'evac_notice'), ('Q35', 'evac_notice_type'), 
                                  ('Q36', 'evac_notice_how'), ('Q37', 'evac_notice_when'), ('Q38', 'stay_notice')])

rename_evac_decision = OrderedDict([('Q39', 'evac_decision'), ('Q40', 'evac_date'), ('Q41', 'evac_time'), ('Q43', 'same_choice')])

rename_emer_service = OrderedDict([('Q42_1','emer_serv_before'), ('Q42_2', 'emer_serv_during'), ('Q42_3', 'emer_serv_after')])


amount_to_num = {'None at all':1, 'A little':2, 'A moderate amount':3, 'A lot':4, 'A great deal':5}
yesno_to_num = {'Yes':1, 'No':0}

evac_ability_items = {'Having young children':'evac_ability_children', 
                      'Having elderly family member(s)':'evac_ability_elders', 
                      'Having family member(s) with special needs':'evac_ability_special_needs', 
                      'Having pets':'evac_ability_pets',
                      'Evacuation expense (travel, lodging, etc.)':'evac_ability_expense', 
                      'No transportation (cars, flights, public transportation, etc)':'evac_ability_no_transport', 
                      "No place to go (hotels, public shelters, friends' or family's places, etc.)":'evac_ability_no_place', 
                      'Job obligations':'evac_ability_job_obligation'}

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
    rename_all.update(rename_harvey)
    rename_all.update(rename_prev_exp)
    rename_all.update(rename_risk)
    rename_all.update(rename_evac_ability)
    rename_all.update(rename_emer_service)
    rename_all.update(rename_evac_notice)
    rename_all.update(rename_evac_decision)
    
    df.rename(columns=rename_all, inplace=True)
    
    print df.columns
    
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
    
    # harvey
    df['harvey_influence_amount'].replace({'None at all':0, 'A little':1, 'A moderate amount':2, 'A lot':3, 'A great deal':4}, inplace=True)
    
    # prev exp
    df['has_prev_exp'].replace({'Yes':1, 'No':2}, inplace=True)
    df['prev_decision'].replace({'Evacuate':1, 'Stay':2}, inplace=True)
    df['prev_decision'].fillna(0, inplace=True)
    df_prev_decision = pd.get_dummies(df['prev_decision'], drop_first=True)
    df_prev_decision.rename(columns={1:'prev_decision_evac', 2:'prev_decision_stay'}, inplace=True)
    df['prev_decision_same_choice'].replace({'Yes':1, 'No':2}, inplace=True)
    df['prev_decision_same_choice'].fillna(0, inplace=True)
    df_prev_decision_same_choice = pd.get_dummies(df['prev_decision_same_choice'], drop_first=True)
    df_prev_decision_same_choice.rename(columns={1:'prev_decision_no_regret', 2:'prev_decision_regret'}, inplace=True)
    
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
    
    df['evac_notice_when'].replace({'August 31th (Wednesday)':1, 'September 1st (Friday)':1, 'September 2nd (Saturday)':1, 'September 3rd (Sunday)':1,
                                    'September 4th (Monday, became Category 5)':1, 'September 5th (Tuesday)':2, 
                                    'September 6th (Wednesday, made its first landfall in Barbuda)':2,
                                    'September 7th (Thursday)':2, 'September 8th (Friday)':2, 'September 9th (Saturday)':2, 
                                    'September 10th (Sunday, hit the Keys)':2, 'September 11th (Monday)':2}, inplace=True)
    df['evac_notice_when'].fillna(0, inplace=True)
    df_evac_notice_when = pd.get_dummies(df['evac_notice_when'], drop_first=True)
    df_evac_notice_when.rename(columns={1:'evac_notice_before_cat5', 2:'evac_notice_after_cat5'}, inplace=True)
    
    # decision
    df['evac_decision'].replace(yesno_to_num, inplace=True)
    df['same_choice'].replace(yesno_to_num, inplace=True)
    
    # not used
    df['evac_date'].replace({'August 31th (Wednesday)':1, 'September 1st (Friday)':1, 'September 2nd (Saturday)':1, 'September 3rd (Sunday)':1,
                                    'September 4th (Monday, became Category 5)':1, 'September 5th (Tuesday)':2, 
                                    'September 6th (Wednesday, made its first landfall in Barbuda)':2,
                                    'September 7th (Thursday)':2, 'September 8th (Friday)':2, 'September 9th (Saturday)':2, 
                                    'September 10th (Sunday, hit the Keys)':2, 'September 11th (Monday)':2}, inplace=True)
    df['evac_date'].fillna(0, inplace=True)
    df_evac_date = pd.get_dummies(df['evac_date'], drop_first=True)
    df_evac_date.rename(columns={1:'evac_before_cat5', 2:'evac_after_cat5'}, inplace=True)
    df['evac_time'].replace({'Morning':1, 'Afternoon':2, 'Evening':3, 'Night':4}, inplace=True)
    df['emer_serv_before'].replace(yesno_to_num, inplace=True)
    df['emer_serv_during'].replace(yesno_to_num, inplace=True)
    df['emer_serv_after'].replace(yesno_to_num, inplace=True)
    
    
    # ability
    for item in evac_ability_items.values():
        df[item] = 0
    for i, row in df.iterrows():
        items = re.split(regex_comma_outside_parentheses, row['evac_ability_items'])
        for item in items:
            if item != 'None':
                df.set_value(i, evac_ability_items[item], 1)
                
        if row['harvey_influence_direction'] == 'Increased my desire to leave':
            df.set_value(i, 'harvey_influence', row['harvey_influence_amount'])
        else:
            df.set_value(i, 'harvey_influence', row['harvey_influence_amount']*(-1))
        
        # discretize
        if row['age'] <=30:
            df.set_value(i, 'age', 1)
        elif row['age'] > 30 and row['age'] <= 40:
            df.set_value(i, 'age', 2)
        elif row['age'] > 40 and row['age'] <= 50:
            df.set_value(i, 'age', 3) 
        elif row['age'] > 50 and row['age'] <= 60:
            df.set_value(i, 'age', 4) 
        else:
            df.set_value(i, 'age', 5) 
        
        if row['househd_size'] in [1]:
            df.set_value(i, 'househd_size', 1) 
        elif row['househd_size'] in [2,3]:
            df.set_value(i, 'househd_size', 2) 
        else:
            df.set_value(i, 'househd_size', 3) 
    
    df = pd.concat([df, df_race, df_house_struct, df_house_material, 
                    df_evac_notice, df_evac_notice_type, df_stay_notice, 
                    df_prev_decision, df_prev_decision_same_choice,
                    df_friends_suggest, df_neighbors_doing, df_evac_notice_when], axis=1)


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
    # harvey + prev exp
    all_cols.extend(['harvey_influence', 'has_prev_exp', 'prev_decision_evac', 'prev_decision_stay', 'prev_decision_regret', 'prev_decision_no_regret'])
    # evac notice
    all_cols.extend(['received_evac_notice', 'no_evac_notice', 'received_mandatory', 'received_voluntary', 'received_stay_notice', 'no_stay_notice'])  
    all_cols.extend(['evac_notice_before_cat5', 'evac_notice_after_cat5'])  
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
    input_fp = os.path.join('data', 'MTurk_Irma_Qualtrics.csv')

    output_fp = os.path.join('data', 'MTurk_Irma.csv')
    prep(input_fp, output_fp)

    