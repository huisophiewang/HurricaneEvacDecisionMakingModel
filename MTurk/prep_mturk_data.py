import pandas as pd
import numpy as np
from collections import OrderedDict
from scipy import stats
import matplotlib.pyplot as plt
import re
from pprint import pprint

regex_comma_outside_parentheses = r',\s*(?![^()]*\))'

rename_demo = OrderedDict([('Q11', 'age'), ('Q12', 'gender'), ('Q13', 'race'), ('Q14', 'edu'), ('Q15', 'income'),('Q16', 'househd_size'), 
                           ('Q17', 'has_children'), ('Q18', 'has_elders'), ('Q19', 'has_special_needs'), ('Q20', 'has_pets')])
rename_house = OrderedDict([('Q23', 'house_struct'), ('Q24', 'house_material'), ('Q25', 'owner'), ('Q26', 'insurance')])
rename_loc = OrderedDict([('Q21', 'zipcode'), ('Q22', 'coast_dist'), ('Q27', 'county')])

rename_info_tv = OrderedDict([('Q4', 'info_tv'), 
                              ('Q5_1', 'info_tv_damage'), ('Q5_2', 'info_tv_casualty'), 
                              ('Q5_3', 'info_tv_road'), ('Q5_4', 'info_tv_prep'), 
                              ('Q5_5', 'info_tv_stay'), ('Q5_6', 'info_tv_leave')])
rename_info_social = OrderedDict([('Q6','info_social'), 
                                 ('Q7_1', 'info_social_damage'), ('Q7_2', 'info_social_storm'), 
                                 ('Q7_3', 'info_social_prep'), ('Q7_4', 'info_social_stay'), 
                                 ('Q7_5', 'info_social_leave'), ('Q7_6', 'info_social_road')])
rename_info_other = OrderedDict([('Q8', 'friends_suggest'), ('Q9', 'neighbors_doing')])

rename_risk = OrderedDict([('Q3_1','risk_stay'), ('Q3_2', 'risk_evac'), 
                           ('Q3_3', 'wind_safety'), ('Q3_4', 'wind_property'), 
                           ('Q3_5', 'flood_safety'), ('Q3_6', 'flood_property')])
rename_evac_ability = OrderedDict([('Q10', 'evac_ability')])

rename_emer_service = OrderedDict([('Q36_1','emer_serv_before'), ('Q36_2', 'emer_serv_during'),('Q36_3', 'emer_serv_after')])
rename_evac_notice = OrderedDict([('Q28', 'evac_notice'), ('Q29', 'evac_notice_type'), ('Q30', 'evac_notice_how'), ('Q31', 'evac_notice_when'), ('Q32', 'evac_notice_stay')])
rename_evac_decision = OrderedDict([('Q33', 'evac_decision'), ('Q34', 'evac_date'), ('Q35', 'evac_time'), ('Q37', 'same_choice')])

amount_to_num = {'None at all':1, 'A little':2, 'A moderate amount':3, 'A lot':4, 'A great deal':5}
yesno_to_num = {'Yes':1, 'No':0}

evac_ability_items = ['Having young children', 'Having elderly family member(s)', 'Having family member(s) with special needs', 'Having pets',
                      'Evacuation expense (travel, lodging, etc.)', 'No transportation (cars, flights, public transportation, etc)', 
                      "No place to go (hotels, public shelters, friends' or family's places, etc.)", 'Job obligations']

evac_notice_how_items = ['Radio or TV', 'Social media or internet', 'Word of mouth (friends/relative/neighbor)',
                         'Police/authorities came into the neighborhood', 'Text alerts or phone calls from officials', 'Other']

risk_cols = []
risk_cols.extend(rename_demo.values())
risk_cols.extend(rename_house.values())
risk_cols.extend(rename_loc.values())
risk_cols.extend(rename_info_tv.values())
risk_cols.extend(rename_info_social.values())
risk_cols.extend(rename_info_other.values())
risk_cols.extend(rename_risk.values())
print risk_cols


def prep(fp):
    df = pd.read_csv(fp)
    
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
    
    cols = rename_all.values()
    df.rename(columns=rename_all, inplace=True)
    
    #df.fillna(0, inplace=True)
    
    df['gender'].replace({"Female":1, "Male":0}, inplace=True)
    df['race'].replace({"Caucasian":1, "African American":2, "Asian":3, "Hispanic":4, "American Indian":5, "Other":0}, inplace=True)
    df_race = pd.get_dummies(df['race'], drop_first=True)
    df_race.rename(columns={1:'r_white', 2:'r_black', 3:'r_asian', 4:'r_hispanic', 5:'r_native'}, inplace=True)
    df['edu'].replace({'Some high school':0, 'High school graduate':1, 'Some college':2, 'College graduate':3, 'Graduate School':4}, inplace=True)
    df['income'].replace({'Less than $15,000':0, '$15,000 to $25,000':1, '$25,000 to $40,000':2, '$40,000 to $80,000':3, 'over $80,000':4}, inplace=True)
    df['has_children'].replace(yesno_to_num, inplace=True)
    df['has_elders'].replace(yesno_to_num, inplace=True)
    df['has_special_needs'].replace(yesno_to_num, inplace=True)
    df['has_pets'].replace(yesno_to_num, inplace=True)
    
    df['house_struct'].replace({'Detached single family home':1, 'Duplex or triplex home':2, 
                                'Condo/apartment - 4 stories or less':2, 'Condo/apartment - more than 4 floors':2, 
                                'Mobile or manufactured home':3, 'Other':0}, inplace=True)
    df_house_struct = pd.get_dummies(df['house_struct'], drop_first=True)
    df_house_struct.rename(columns={1:'hs_single_fam', 2:'hs_condo', 3:'hs_mobile'})
    df['house_material'].replace({'Wood':1, 'Brick or block':2, 'Other':0}, inplace=True)
    df_house_material = pd.get_dummies(df['house_material'], drop_first=True)
    df_house_material.rename(columns={1:'hm_wood', 2:'hm_brick'})
    df['owner'].replace({'Own':1, 'Rent':0}, inplace=True)
    df['insurance'].replace(yesno_to_num, inplace=True)
    df['coast_dist'].replace({'With 1 mile':0, '1 to 10 mile':1, '10 to 30 miles':2,
                              '30 to 50 miles':3, '50 to 70 miles':4, 'More than 70 miles':5}, inplace=True)
    
    df['info_tv'].replace(yesno_to_num, inplace=True)
    df['info_tv_damage'].replace(amount_to_num, inplace=True)
    df['info_tv_casualty'].replace(amount_to_num, inplace=True)
    df['info_tv_road'].replace(amount_to_num, inplace=True)
    df['info_tv_prep'].replace(amount_to_num, inplace=True)
    df['info_tv_stay'].replace(amount_to_num, inplace=True)
    df['info_tv_leave'].replace(amount_to_num, inplace=True)
    for col in rename_info_tv.values():
        df[col].fillna(0, inplace=True)
    
    df['info_social'].replace(yesno_to_num, inplace=True)
    df['info_social_damage'].replace(amount_to_num, inplace=True)
    df['info_social_storm'].replace(amount_to_num, inplace=True)
    df['info_social_road'].replace(amount_to_num, inplace=True)
    df['info_social_prep'].replace(amount_to_num, inplace=True)
    df['info_social_stay'].replace(amount_to_num, inplace=True)
    df['info_social_leave'].replace(amount_to_num, inplace=True)
    for col in rename_info_social.values():
        df[col].fillna(0, inplace=True)
    
    df['friends_suggest'].replace({'Stay':1, 'Evacuate':2, 'Neither':3}, inplace=True)
    df['neighbors_doing'].replace({'Stay':1, 'Evacuate':2}, inplace=True)
    df['neighbors_doing'].fillna(0, inplace=True)
    
    df['risk_stay'].replace(amount_to_num, inplace=True)
    df['risk_evac'].replace(amount_to_num, inplace=True)
    df['wind_safety'].replace(amount_to_num, inplace=True)
    df['wind_property'].replace(amount_to_num, inplace=True)
    df['flood_safety'].replace(amount_to_num, inplace=True)
    df['flood_property'].replace(amount_to_num, inplace=True)
    
    
    #df['evac_ability'][df['evac_ability'] == 'None']
    df['evac_notice'].replace({'Yes':1, 'No':2}, inplace=True)
    df['evac_notice_type'].replace({'Mandatory (must)':1, 'Voluntary (should)':2}, inplace=True)
    #df['evac_notice_how'].replace()
    df['evac_notice_when'].replace({'August 23th (Wednesday)':1, 'August 24th (Thursday)':1, 'August 25th (Friday, 1st landfall near Rockport, TX)':1,
                                    'August 26th (Saturday, weakened to Tropical Storm)':2, 'August 27th (Sunday)':2, 'August 28th (Monday)':2,
                                    'August 29th (Tuesday)':2, 'August 30th (Wednesday, last landfall at Cameron, LA, weakened to Tropical Depression':2,
                                    'August 31th (Thursday)':2, 'September 1st (Friday)':2, 'September 2nd (Saturday)':2, 'September 3rd (Sunday)':2}, inplace=True)
    
    df['evac_notice_stay'].replace({'Yes':1, 'No':2}, inplace=True)
    df['evac_decision'].replace(yesno_to_num, inplace=True)
    df['evac_date'].replace({'August 23th (Wednesday)':1, 'August 24th (Thursday)':1, 'August 25th (Friday, 1st landfall near Rockport, TX)':1,
                            'August 26th (Saturday, weakened to Tropical Storm)':2, 'August 27th (Sunday)':2, 'August 28th (Monday)':2,
                            'August 29th (Tuesday)':2, 'August 30th (Wednesday, last landfall at Cameron, LA, weakened to Tropical Depression':2,
                            'August 31th (Thursday)':2, 'September 1st (Friday)':2, 'September 2nd (Saturday)':2, 'September 3rd (Sunday)':2}, inplace=True)
    
    df['evac_time'].replace({'Morning':1, 'Afternoon':2, 'Evening':3, 'Night':4}, inplace=True)
    df['emer_serv_before'].replace(yesno_to_num, inplace=True)
    df['emer_serv_during'].replace(yesno_to_num, inplace=True)
    df['emer_serv_after'].replace(yesno_to_num, inplace=True)
    df['same_choice'].replace(yesno_to_num, inplace=True)
    

#     print df['evac_ability'].unique()
#     print df['evac_ability'].value_counts(dropna=False)
#     for i, d in df.iterrows():
#         print '---------------------'
#         print i
#         items = re.split(regex_comma_outside_parentheses, d['evac_ability'])
#         pprint(items)
        
    


    
if __name__ == '__main__':
    fp = "Hurricane_Evacuation_Questionnaire.csv"
    prep(fp)

    #pprint(items)
    