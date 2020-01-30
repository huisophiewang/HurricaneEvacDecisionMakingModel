import pandas as pd
from pprint import pprint

tract_ids = [701, 702, 703, 704, 705, 706, 709, 710,
          711, 712, 713, 714, 716, 719, 720, 721,
          722, 723, 724, 725, 726, 727, 728, 729, 
          730, 731, 732, 733, 734, 735, 736, 737, 
          738, 739, 740, 743, 744, 2572]

factors = ['Male', 'Female',
           'White Alone', 'Black or African American Alone', 'American Indian and Alaska Native Alone','Asian Alone','Some Other Race Alone',
           'Households with One or More People Under 18 Years:', 'In Labor Force:', 
           'Less than High School', 'High School Graduate (Includes Equivalency)', 'Some College', 
           "Bachelor's Degree", "Master's Degree", 'Professional School Degree', 'Doctorate Degree',
           'Mobile Home','1, Detached', 
           'Never Married', 'Now Married (Not Including Separated)',
           'Under 5 Years', '5 to 9 Years', '10 to 14 Years', '15 to 17 Years', '18 to 24 Years', '25 to 34 Years',
           '35 to 44 Years', '45 to 54 Years', '55 to 64 Years', '65 to 74 Years', '75 to 84 Years', '85 Years and Over',
           'Less than $10,000', '$10,000 to $14,999', '$15,000 to $19,999', '$25,000 to $29,999', '$30,000 to $34,999',
           '$35,000 to $39,999', '$40,000 to $44,999', '$45,000 to $49,999', '$50,000 to $59,999', '$60,000 to $74,999',
           '$75,000 to $99,999', '$100,000 to $124,999', '$125,000 to $149,999', '$150,000 to $199,999', '$200,000 or More'
           ]

def read_census():    
    df = pd.read_excel('data/BridgeportCensus.xlsx')     

    #for i, row in df.iterrows():
    fields = list(df.index)
    print fields
    
    all_tract = {}
    for i, col in enumerate(df):
        if i >= 76:
            continue

        if i%2==0:
            tract_pop = {}
            for j, row in enumerate(df[col]):
                if fields[j] == 'Statistics':
                    tract = int(row.split(',')[0].split()[-1])
                if fields[j] == 'Total Population':
                    tract_pop['Total Population'] = row
                if fields[j] == 'Households:':
                    tract_pop['Households'] = row
            all_tract[tract] = tract_pop
            
        if i%2==1:
            tract_info = {}
            for j, row in enumerate(df[col]):
                # if fields[j] is not nan
                if isinstance(fields[j], basestring):
                    if fields[j] in factors:
                        tract_info[fields[j]] = row
            tract = tract_ids[int(i/2)]
#         if not tract in all_tract:
#             all_tract[tract] = []
            all_tract[tract].update(tract_info)
        #all_tract.update({tract:tract_qa})
    #pprint(all_tract)
    
    #print len(all_tract)
    return all_tract
            
if __name__ == '__main__':
    read_census()
