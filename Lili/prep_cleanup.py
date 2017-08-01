import numpy as np
import pandas as pd
from pprint import pprint
import math



def race_dist():
    fr = open(r'LiliBasicData.csv', 'rU')
    labels = fr.readline().split(',')
    all = {}
    for line in fr.readlines():
        items = line.split(',')
        #print len(items)
        county = items[56]
        race = items[48]
        if county and race and race != ' ':
            if not county in all:
                all[county] = {}
            if not race in all[county]:
                all[county][race] = 0
            all[county][race] += 1
    pprint(all)
    
    for county in all:
        total = sum(all[county].values())
        print total
        for race in all[county]:
            all[county][race] /= float(total)
            
    pprint(all)
    

    
def get_var_cardinality():
    # cardiinality: Koller book 19.5.2
    data = np.genfromtxt(r'Lili_BN_labels.csv', delimiter=",", dtype=float, skip_header=1)
    print data
    sizes = []
    for c in data.T:
        size = len(set(c))
        sizes.append(str(size))
    print ' '.join(sizes)
    

    
def divide_by_evac():
    df = np.genfromtxt(r'LiliBasicData_BN_EvacTime.csv', delimiter=",", dtype=float, names=True)
    #print df.dtype
    field_names = df.dtype.names
    labels = ['Age', 'Gender', 'Race', 'Marriage', 'HouseholdSize', 'NumChd', 'Edu', 'Income', 'Owner','HouseStruct',
              'SrcLocalAuth', 'SrcLocalMedia', 'SrcNationalMedia', 'SrcInternet', 'SrcPeers',
              'CloseCoast', 'CloseWater', 'SeeStormCond', 'SeeShopClose', 'SeePeerEvac',
              'OfficialHurricWatch', 'OfficialEvac', 'PrevStormExp', 'PrevFalseAlarm', 
              'ProtectFromLooter', 'ProtectFromStorm', 'LostIncome', 'EvacExpense', 'Traffic'
              ]
    not_evac = []
    early_evac = []
    late_evac = []
    evac_time = {}
    evacuated = []
    for d in df:
        for field in field_names:
            if field not in ['q4', 'q5'] and math.isnan(d[field]):
                break
        else:
            #print d
            age = d['q17']
            if age < 30:
                d['q17'] = '1'
            elif age >= 30 and age < 40:
                d['q17'] = '2'
            elif age >= 40 and age < 50:
                d['q17'] = '3'
            elif age >= 50 and age < 60:
                d['q17'] = '4'
            elif age >= 60 and age < 70:
                d['q17'] = '5'
            else:
                d['q17'] = '6'

            evac = d['q3']
            if evac == 1:
                not_evac.append(d)
             
            # total 156 people
            # 76 people, hour <= 31
            #print d
            if evac == 2:
                if math.isnan(d['q4']) or math.isnan(d['q5']):
                    continue
#                 hour = (d['q4']-1)*24 + d['q5']
#                 #print hour
#                 if hour <= 31:
#                     early_evac.append(d)
#                 else:
#                     late_evac.append(d)
                evacuated.append(d)
                
                     
    #np.savetxt("Lili_BN_labels_NotEvac.csv", not_evac, fmt='%s', delimiter=",", header=','.join(labels))
    #np.savetxt("Lili_BN_labels_EarlyEvac.csv", early_evac, fmt='%s', delimiter=",", header=','.join(labels))
    #np.savetxt("Lili_BN_labels_LateEvac.csv", late_evac, fmt='%s', delimiter=",", header=','.join(labels))
    np.savetxt("Lili_BN_labels_Evac.csv", evacuated, fmt='%s', delimiter=",", header=','.join(labels))
        

def prep():
    #df = pd.read_csv(r'LiliBasicData.csv')
    
    
    df = np.genfromtxt(r'data/LiliBasicData_BN.csv', delimiter=",", dtype=float, names=True)
    qlabels = df.dtype.names
    labels = ['Age', 'Gender', 'Race', 'Marriage', 'HouseholdSize', 'NumChd', 'Edu', 'Income', 'Owner','HouseStruct',
              'SrcLocalAuth', 'SrcLocalMedia', 'SrcNationalMedia', 'SrcInternet', 'SrcPeers',
              'CloseCoast', 'CloseWater', 'SeeStormCond', 'SeeShopClose', 'SeePeerEvac',
              'OfficialHurricWatch', 'OfficialEvac', 'PrevStormExp', 'PrevFalseAlarm', 
              'ProtectFromLooter', 'ProtectFromStorm', 'LostIncome', 'EvacExpense', 'Traffic',
              'Evac'
              ]

    c=0
    out = []
    for d in df:
        #print len(d)
#         if math.isnan(d[0]) and math.isnan(d[1]):
#             continue
        # remove subject that has missing value in any field
        for j in d:
            print len(d)
            if math.isnan(j):
                break
        else:
            age = d['q17']
            if age < 30:
                d['q17'] = '1'
            elif age >= 30 and age < 40:
                d['q17'] = '2'
            elif age >= 40 and age < 50:
                d['q17'] = '3'
            elif age >= 50 and age < 60:
                d['q17'] = '4'
            elif age >= 60 and age < 70:
                d['q17'] = '5'
            else:
                d['q17'] = '6'
            out.append(d)
            c+=1
    print c
    #print out.shape
    #labels = ['']
    #out = [(1,2),(3,4)]
    #np.savetxt("foo.csv", out, delimiter=",", header='a,b')
    np.savetxt("data/Lili_BN_labels.csv", out, fmt='%s', delimiter=",", header=','.join(labels))

def prep_with_dist():
    df = np.genfromtxt(r'data/LiliBasicData_BN_Dist.csv', delimiter=",", dtype=float, names=True)
    #print df
    qlabels = df.dtype.names


    labels = ['Age', 'Gender', 'Race', 'Marriage', 'HouseholdSize', 'NumChd', 'Edu', 'Income', 'Owner','HouseStruct',
              'SrcLocalAuth', 'SrcLocalMedia', 'SrcNationalMedia', 'SrcInternet', 'SrcPeers',
              'CloseCoast', 'CloseWater', 'SeeStormCond', 'SeeShopClose', 'SeePeerEvac',
              'OfficialHurricWatch', 'OfficialEvac', 'PrevStormExp', 'PrevFalseAlarm', 
              'ProtectFromLooter', 'ProtectFromStorm', 'LostIncome', 'EvacExpense', 'Traffic',
              'County',
              'DistRiver','DistLake','DistCoast',
              'Evac'
              ]
    out = []
    c=0
    for instance in df:
        # remove subject that has missing value in any field
        for j in instance:
            print len(instance)
            if math.isnan(j):
                break
#         for j, value in enumerate(instance):
#             if j <= 33 and math.isnan(value):
#                 break
        else:
            c+=1
            out.append(instance)
    print c
    np.savetxt("data/Lili_BN_labels_with_dist.csv", out, fmt='%s', delimiter=",", header=','.join(labels))
    
    
if __name__ == '__main__':
    #prep()
    #get_var_cardinality()
    #divide_by_evac()
    #divide_by_income()
    #divide_by_age()
    prep_with_dist()
    #prep()
    
        
        
        