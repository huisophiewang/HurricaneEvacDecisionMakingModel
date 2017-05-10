import numpy as np
import pandas as pd

def convert():
    #df = np.genfromtxt(r'Lili_BN_labels.csv', delimiter=",", dtype=float, names=True)
    #print df.size
    
    #df = pd.read_csv(r'Lili_BN_labels.csv')
    df = pd.read_csv(r'Lili_BN_labels_Evac.csv')
#     cols = df.columns.tolist()
#     cols = cols[-1:] + cols[:-1]
#     print cols
    # 0 Male, 1 Female  
    df['Gender'] = df['Gender'] - 1
    # 0 Caucasian, 1 African American, 2 Native American, 3 Other
    df['Race'].replace({3:0, 1:1, 5:2, 0:3, 2:3, 4:3, 6:3, 7:3}, inplace=True)
    df_race = pd.get_dummies(df['Race'], drop_first=True)
    df_race.rename(columns={1.0:'r_black', 2.0:'r_native', 3.0:'r_other'}, inplace=True)
    df_race = df_race.astype(float)
    # 0 Married (0 0), 1 Single (1 0), 2 Other (0 1)
    df['Marriage'].replace({1:0, 2:1, 3:2, 4:2}, inplace=True)
    df_marriage = pd.get_dummies(df['Marriage'], drop_first=True)
    df_marriage.rename(columns={1.0:'m_single', 2.0:'m_other'}, inplace=True)
    df_marriage = df_marriage.astype(float)
    # 0 Some High School & High School, 1 Some college, 2 College & Graduate
    df['Edu'].replace({1:0, 2:0, 3:1, 4:2, 5:2}, inplace=True)
    df_edu = pd.get_dummies(df['Edu'], drop_first=True)
    df_edu.rename(columns={1.0:'e_someclg', 2.0:'e_clg'}, inplace=True)
    df_edu = df_edu.astype(float)
    # 0 Rent, 1 Own
    df['Owner'] = df['Owner'] - 1
    # 0 Detached Single Family, 1 Mobile, 2 Other
    df['HouseStruct'].replace({1:0, 2:2, 3:2, 4:1, 5:2}, inplace=True)
    df_house = pd.get_dummies(df['HouseStruct'], drop_first=True)
    df_house.rename(columns={1.0:'h_mobile', 2.0:'h_other'}, inplace=True)
    df_house = df_house.astype(float)
    # 0 No, 1 Yes
    df['Evac'] = df['Evac'] - 1
    df['EvacTime'] = (df['EvacDay']-1)*24 + df['EvacHour']
    
    result = pd.concat([df, df_race, df_marriage, df_edu, df_house], axis=1)
    #print result
    #print result
    new_columns = ['Age', 'Gender', 'r_black', 'r_native', 'r_other', 'm_single', 'm_other',
                   "HouseholdSize", "NumChd", "e_someclg", "e_clg", "Income",
                   'Owner', 'h_mobile', 'h_other', "CloseCoast", "CloseWater", "OfficialHurricWatch", "OfficialEvac", 
                   "SrcLocalAuth", "SrcLocalMedia", "SrcNationalMedia", "SrcInternet", "SrcPeers",
                   "SeeStormCond", "SeeShopClose", "SeePeerEvac", "PrevStormExp", "PrevFalseAlarm",
                   "ProtectFromLooter", "ProtectFromStorm", "LostIncome", "EvacExpense", "Traffic", "EvacTime"]
    
    #result.to_csv('Lili_converted_EvacDay.csv', columns=new_columns, index=False)
    result.to_csv('Lili_converted_EvacTime.csv', columns=new_columns, index=False)

            

                
            

                
if __name__ == '__main__':
    convert()

                