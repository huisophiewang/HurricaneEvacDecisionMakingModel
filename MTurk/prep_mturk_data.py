import pandas as pd
import numpy as np
from collections import OrderedDict
from scipy import stats
import matplotlib.pyplot as plt

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
rename_info_other = OrderedDict([('Q8', 'friends_suggest'), ('Q9', 'neighbor_doing')])

rename_risk = OrderedDict([('Q3_1','risk_stay'), ('Q3_2', 'risk_evac'), 
                           ('Q3_3', 'wind_safety'), ('Q3_4', 'wind_property'), 
                           ('Q3_5', 'flood_safety'), ('Q3_6', 'flood_property')])
rename_evac_ability = OrderedDict([('Q10', 'evac_ability')])


rename_evac_notice = OrderedDict([('Q28', 'evac_notice'), ('Q29', 'evac_notice_type'), ('Q30', 'evac_notice_how'), ('Q31', 'evac_notice_when'), ('Q32', 'evac_notice_stay')])
rename_evac_decision = OrderedDict([('Q33', 'evac_decision'), ('Q34', 'evac_date'), ('Q35', 'evac_time'), ('Q36', 'emergency_services'), ('Q37', 'same_choice')])

amount_to_num = {'None at all':1, 'A little':2, 'A moderate amount':3, 'A lot':4, 'A great deal':5}
yesno_to_num = {'Yes':1, 'No':0}

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
    rename_all.update(rename_evac_notice)
    rename_all.update(rename_evac_decision)
    
    cols = rename_all.values()
    df.rename(columns=rename_all, inplace=True)
    
    #df.fillna(0, inplace=True)
    
    df['gender'].replace({"Female":1, "Male":2}, inplace=True)
    df['race'].replace({"Caucasian":1, "African American":2, "Asian":3, "Hispanic":4, "American Indian":5, "Other":0}, inplace=True)
    df_race = pd.get_dummies(df['race'], drop_first=True)
    df_race.rename(columns={1:'r_white', 2:'r_black', 3:'r_asian', 4:'r_hispanic', 5:'r_native'}, inplace=True)
    df['edu'].replace({'Some high school':1, 'High school graduate':2, 'Some college':3, 'College graduate':4, 'Graduate School':5}, inplace=True)
    df['income'].replace({'Less than $15,000':1, '$15,000 to $25,000':2, '$25,000 to $40,000':3, '$40,000 to $80,000':4, 'over $80,000':5}, inplace=True)
    df['has_children'].replace(yesno_to_num, inplace=True)
    df['has_elders'].replace(yesno_to_num, inplace=True)
    df['has_special_needs'].replace(yesno_to_num, inplace=True)
    df['has_pets'].replace(yesno_to_num, inplace=True)
    
    df['house_struct'].replace({'Detached single family home':1, 'Duplex or triplex home':2, 
                                'Condo/apartment - 4 stories or less':2, 'Condo/apartment - more than 4 floors':2, 
                                'Mobile or manufactured home':3, 'Other':0}, inplace=True)
    df['house_material'].replace({'Wood':1, 'Brick or block':2, 'Other':0}, inplace=True)
    df['owner'].replace({'Own':1, 'Rent':2}, inplace=True)
    df['insurance'].replace(yesno_to_num, inplace=True)
    df['coast_dist'].replace({'With 1 mile':1, '1 to 10 mile':2, '10 to 30 miles':3,
                              '30 to 50 miles':4, '50 to 70 miles':5, 'More than 70 miles':6}, inplace=True)
    
    df['risk_stay'].replace(amount_to_num, inplace=True)
    df['risk_evac'].replace(amount_to_num, inplace=True)
    df['wind_safety'].replace(amount_to_num, inplace=True)
    df['wind_property'].replace(amount_to_num, inplace=True)
    df['flood_safety'].replace(amount_to_num, inplace=True)
    df['flood_property'].replace(amount_to_num, inplace=True)
    
    #df['evac_ability'][df['evac_ability'] == 'None']
    
    
    
    


    
if __name__ == '__main__':
    fp = "Hurricane_Evacuation_Questionnaire.csv"
    prep(fp)