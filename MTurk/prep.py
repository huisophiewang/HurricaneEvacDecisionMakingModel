import pandas as pd
from collections import OrderedDict

rename_risk = OrderedDict([('Q3_1','risk_stay'), ('Q3_2', 'risk_evac'), 
                           ('Q3_3', 'wind_safety'), ('Q3_4', 'wind_property'), 
                           ('Q3_5', 'flood_safety'), ('Q3_6', 'flood_property')])
rename_info_tv = OrderedDict([('Q4', 'info_tv'), 
                              ('Q5_1', 'info_tv_damage'), ('Q5_2', 'info_tv_casualty'), 
                              ('Q5_3', 'info_tv_road'), ('Q5_4', 'info_tv_prep'), 
                              ('Q5_5', 'info_tv_stay'), ('Q5_6', 'info_tv_leave')])
rename_info_social = OrderedDict([('Q6','info_social'), 
                                 ('Q7_1', 'info_social_damage'), ('Q7_2', 'info_social_storm'), 
                                 ('Q7_3', 'info_social_prep'), ('Q7_4', 'info_social_stay'), 
                                 ('Q7_5', 'info_social_leave'), ('Q7_6', 'info_social_road')])
rename_info_other = OrderedDict([('Q8', 'friends_suggest'), ('Q9', 'neighbor_doing')])
rename_evac_ability = OrderedDict([('Q10', 'evac_ability')])
rename_demo = OrderedDict([('Q11', 'age'), ('Q12', 'gender'), ('Q13', 'race'), ('Q14', 'edu'), ('Q15', 'income'),('Q16', 'househd_size'), 
                           ('Q17', 'has_children'), ('Q18', 'has_elders'), ('Q19', 'has_special_needs'), ('Q20', 'has_pets')])

fp = "Hurricane_Evacuation_Questionnaire.csv"
df = pd.read_csv(fp)
print df['StartDate']