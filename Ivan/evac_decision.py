import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pprint import pprint


stay_map = {
    "forecast said storm would hit a different location":1,
    "officials seemed unsure whether evacuation was necessary":2,
    "heard conflicting messages from officials whether evacuation was necessary":3,
    "conflicting official messages if evacuation was necessary":3,
    "storm wasn't severe enough to pose a severe danger even if it hit":4,
    "storm wasn't severe enough to be dangerous even if it hit":4,
    "location was on the weak (left) side of the storm":5,
    "house is well built (strong enough to be safe in storm)":6,
    "home is elevated above the level of storm surge":7,     
    "officials said evacuation was not necessary":8,
    "officials didn't say to evacuate":9,
    "media said evacuation wasn't necessary":10,
    "friend/relative said evacuation wasn't necessary":11,
    "probabilities indicated low chance of a hit":12,
    "other information indicated storm wouldn't hit":13,
    "had no place to go":14,
    "wanted to protect property from looters":15,
    "wanted to protect property from storm":16,
    "left unnecessarily in past storms":17,
    "job required staying":18,
    "waited too long to leave":19,
    "evacuation notice from officials came too late":20,
    "traffic too bad":21,
    "tried to leave, but returned home because of traffic":22,
    "too dangerous to evacuate because might get caught on road in storm":23,
    "if evacuate could get caught on road in storm":23,
    "no place to take pets/shelter would not accept pets":24,
    "concerned about being able to re-enter community after evacuating":25,
    "concerned if could re-enter community after evacuating":25,
    "unable to re-enter area after evacuating in past storms":26,
    "had no transportation":27,
    "have household member who is elderly or has special needs":28,
    "other, specify:____":29,
    "don't know":0,
    }


"""
no_other code:
not necessary:30
faith, god: 31
other family member's concern or influence:32
prev_exp, never leaves:33
inland, not near water: 34
no money: 35
"""


stay_group_map ={
(2,3,8,9):'official',
(1,4,12,13):'storm',
(5,6,7,34):'house',
(28,32):'family',
(17,33):'prev_exp',
(15,16):'property',
(14,18,19,20,21,22,23,24,27):'unable_to',
(0,10,11,17,25,26,30,31,35):'other'
}


evac_map = {
    "advice or order by elected officials":1,
    "advice or order by public safety officials":2,
    "advice from national weather service":3,
    "advice/order from police officer or fire fighter":4,
    "advice-order from police officer or fire fighter":4,
    "advice from the media":5,
    "advice from friend or relative":6,
    "information about the severity of the storm":7,
    "concerned storm would cause home to flood":8,
    "concerned strong winds would make house unsafe":9,
    "concerned flooding would cut off roads":10,
    "concerned flooding would cut off roads ":10,
    "concerned about loss of utilities because of family member with special needs":11,
    "loss of utilities--family member with special needs":11,
    "concerned that storm might hit":12,
    "forecast indicated storm would hit":13,
    "forecast indicated storm could hit":14,
    "probability (odds) were high that the storm could hit":15,
    "national weather service issued hurricane watch":16,
    "national weather service issued hurricane warning":17,
    "concerned about possible tornados":18,
    "experience in other storms":19,
    "other, specify":20,
    "don't know":0
           }

"""
yes_other code:
mobile house or unsafe house: 21
location close to coast or river: 22
concern about family member or family member's influence: 23
don't want to alone: 24
work related or required: 25
"""

# storm:1, house:2, official:3, prev_exp:4, 
evac_group_map = {   
(1,2,4):'official',
(7,8,9,10,11,12,13,14,15,16,17,18):'storm',
(21,22):'house',
(23,11):'family',
(19,):'prev_exp',
(0,3,5,6,19,24,25):'other'
}



def select_cols():
    df = pd.read_csv(r'IvanExport.csv')
    #print df['sname']
    
    df.rename(columns={"samp":"county", 'q2':'evac',
                       'q3_01':'no_01','q3_02':'no_02','q3_03':'no_03', 'q3oth':'no_other',
                       'q17_01':'yes_01', 'q17_02':'yes_02', 'q17_03':'yes_03', 'q17oth': 'yes_other'}, inplace=True)
    cols = ['state', 'county', 'no_01', 'no_02', 'no_03', 'no_other', 'yes_01', 'yes_02', 'yes_03', 'yes_other', 'evac']
    df.to_csv('Ivan_evac_decision.csv', columns=cols, index=False)
    
def convert_multi_entry_dict(multi_entry):
    result = {}
    for k, v in multi_entry.items():
        #print k, v
        for key in k:
            result[key] = v
    return result

def plot():
    df = pd.read_csv(r'IvanExport.csv')
    #print df
    df_select = df[(df.county=='AL')]
    df_select.plot.bar()
    plt.show()
    
def filter_stay():
    df = pd.read_csv(r'Ivan_evac_decision.csv')
    df = df[(df.evac=='no, did not evacuate')]
    df = df[['index', 'no_01','no_02','no_03', 'no_other']]
    df['no_02'].replace(stay_map,inplace=True)
    df['no_03'].replace(stay_map,inplace=True)
    
    #df['no_01'].plot.bar()
    df.hist(column='no_01',bins=30)
    plt.show()
    #print len(df.no_01.unique())
    df.to_csv('Ivan_evac_decision_no.csv', columns=['index', 'no_01','no_02','no_03', 'no_other'], index=False)


    
def filter_evac():
    df = pd.read_csv(r'Ivan_evac_decision.csv')
    df = df[(df.evac=='yes, evacuated')]
    df = df[['index', 'yes_01','yes_02','yes_03', 'yes_other']]
    df['yes_01'].replace(evac_map,inplace=True)
    df['yes_02'].replace(evac_map,inplace=True)
    df['yes_03'].replace(evac_map,inplace=True)
    print len(df.yes_01.unique())
    df.hist(column='yes_01',bins=21)
    plt.show()
    #df.to_csv('Ivan_evac_decision_yes.csv', columns=['index','yes_01','yes_02','yes_03','yes_other'], index=False)
    
    
def group_reasons(fp, reason_dic, cols, other_id):
    df = pd.read_csv(fp)
    reason_factors = convert_multi_entry_dict(reason_dic)
    #pprint(reason_factors)
    ret = {}
    for i, row in df.iterrows():
        factors = set()
        #print '--------------'
        reasons = ''
        for col in cols:
            reason = str(row[col])
            if reason!='nan':
                reasons = reasons + reason + ','
#             if isinstance(row[col], basestring):
#                 reasons += row[col]
        #print "index: %d" % row['index']
        #print reasons
        for reason in reasons[:-1].split(','):
            reason = int(reason.split('.')[0])
            if reason == other_id:
                continue
            factor = reason_factors[reason]
            factors.add(factor)
            
        #print factors
        index = int(row['index'])
        ret[index] = list(factors)
    return ret

def merge():
    yes_people = group_reasons(r'Ivan_evac_decision_yes.csv', evac_group_map, 
                            ['yes_01','yes_02','yes_03', 'yes_other_code'], 20)
    no_people = group_reasons(r'Ivan_evac_decision_no.csv', stay_group_map, 
                           ['no_01','no_02','no_03', 'no_other_code'], 29)
    
    all_people = yes_people.copy()
    all_people.update(no_people)
    print len(all_people)
    pprint(all_people)

if __name__ == '__main__':
    #select_cols()
    #filter_stay()
    #filter_evac()
    merge()
