import numpy as np
import pandas as pd

def convert():
    #df = np.genfromtxt(r'Lili_BN_labels.csv', delimiter=",", dtype=float, names=True)
    #print df.size
    
    #df = pd.read_csv(r'Lili_BN_labels.csv')
    #df = pd.read_csv(r'Lili_BN_labels.csv')
    df = pd.read_csv(r'data/Lili_BN_labels_with_dist.csv')
#     cols = df.columns.tolist()
#     cols = cols[-1:] + cols[:-1]
#     print cols
    # 0 Male, 1 Female  
    df['Gender'] = df['Gender'] - 1
    # 0 Other, 1 Caucasian, 2 African American, 3 Native American, 4 Hispanic, 5 Asian (no Asians in this sample)
    df['Race'].replace({6:0, 7:0, 3:1, 1:2, 5:3, 4:4, 2:0}, inplace=True)
    print df['Race'].unique()
    df_race = pd.get_dummies(df['Race'], drop_first=True)
    df_race.rename(columns={1.0:'r_white', 2.0:'r_black', 3.0:'r_native', 4.0:'r_hispanic'}, inplace=True)
    df_race = df_race.astype(float)
    #print df_race
    # 0 Other, 1 Married, 2 Single
    df['Marriage'].replace({1:1, 2:2, 3:0, 4:0}, inplace=True)
    df_marriage = pd.get_dummies(df['Marriage'], drop_first=True)
    df_marriage.rename(columns={1.0:'m_married', 2.0:'m_single'}, inplace=True)
    df_marriage = df_marriage.astype(float)
    # 0 Some High School & High School, 1 Some college, 2 College & Graduate
#     df['Edu'].replace({1:0, 2:0, 3:1, 4:2, 5:2}, inplace=True)
#     df_edu = pd.get_dummies(df['Edu'], drop_first=True)
#     df_edu.rename(columns={1.0:'e_someclg', 2.0:'e_clg'}, inplace=True)
#     df_edu = df_edu.astype(float)
    # 0 Rent, 1 Own
    df['Owner'] = df['Owner'] - 1
    # 0 Other, 1 Detached Single Family, 2 Mobile
    df['HouseStruct'].replace({1:1, 2:0, 3:0, 4:2, 5:0}, inplace=True)
    df_house = pd.get_dummies(df['HouseStruct'], drop_first=True)
    df_house.rename(columns={1.0:'h_singlefam', 2.0:'h_mobile'}, inplace=True)
    df_house = df_house.astype(float)
    # 0 No, 1 Yes
    df['Evac'] = df['Evac'] - 1
    #df['EvacTime'] = (df['EvacDay']-1)*24 + df['EvacHour']
    
    result = pd.concat([df, df_race, df_marriage, df_house], axis=1)
    #print result
    #print result
    new_columns = ['Age', 'Gender', 'r_white','r_black', 'r_native', 'r_hispanic', 'm_married', 'm_single',
                   "HouseholdSize", "NumChd", "Edu", "Income",
                   'Owner', 'h_singlefam', 'h_mobile', "CloseCoast", "CloseWater", "OfficialHurricWatch", "OfficialEvac", 
                   "SrcLocalAuth", "SrcLocalMedia", "SrcNationalMedia", "SrcInternet", "SrcPeers",
                   "SeeStormCond", "SeeShopClose", "SeePeerEvac", "PrevStormExp", "PrevFalseAlarm",
                   "ProtectFromLooter", "ProtectFromStorm", "LostIncome", "EvacExpense", "Traffic", "DistCoast","DistRiver","DistLake"
                   "Evac"]
    

    #result.to_csv('Lili_converted_EvacDay.csv', columns=new_columns, index=False)
    #result.to_csv('Lili_converted_EvacTime.csv', columns=new_columns, index=False)
    #result.to_csv('data/Lili_converted_v3.csv', columns=new_columns, index=False)

            

                
            

                
if __name__ == '__main__':
    convert()

                