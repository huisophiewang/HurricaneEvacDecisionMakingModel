import os
import pandas as pd
from collections import OrderedDict
import zipcode
from pprint import pprint

rename_loc = {'Q16':'current_zipcode', 'Q27':'preIrma_zipcode', 'Q28':'coast_dist', 'Q33':'county', 
              'LocationLatitude':'lat', 'LocationLongitude':'lon'}

region1 = ['Escambia County', 
           'Santa Rosa County', 
           'Okaloosa County', 
           'Walton County',
           'Holmes County',
           'Washington County',
           'Bay County',
           'Jackson County',
           'Calhoun County',
           'Gulf County',
           'Gadsden County',
           'Liberty County',
           'Franklin County',
           'Leon County',
           'Wakulla County',
           'Jefferson County'
           ]

region2 = ['Nassau County',
           'Duval County',
           'Clay County',
           'St. Johns County',
           'Putnam County',
           'Flagler County',
           'Volusia County',
           'Brevard County',
           ]

region3 = ['Madison County',
           'Hamilton County',
           'Columbia County',
           'Baker County',
           'Suwannee County',
           'Union County',
           'Bradford County',
           'Lafayette County',
           'Gilchrist County',
           'Alachua County',
           'Marion County',
           'Sumter County',
           'Lake County',
           'Orange County',
           'Seminole County',
           'Osceola County',
           'Polk County',
           'Hardee County',
           'DeSoto County',
           'Highlands County',
           'Okeechobee County',
           'Glades County',
           'Hendry County',
           
           ]

region4 = ['Collier County',
           'Lee County',
           'Charlotte County',
           'Sarasota County',
           'Manatee County',
           'Pinellas County',
           'Hillsborough County',
           'Pasco County',
           'Hernando County',
           'Citrus County',
           'Levy County',
           'Dixie County',
           'Taylor County',
           
           
           ]

region5 = ['Monroe County',
           'Miami-Dade County',
           'Broward County',
           'Palm Beach County',
           'Martin County',
           'St. Lucie County',
           'Indian River County',
           ]

all_regions = [region1,region2,region3,region4,region5]

def prep(input_fp, output_fp):
    df = pd.read_csv(input_fp)
    
    df.rename(columns=rename_loc, inplace=True)
    
    count = 0
    for i, row in df.iterrows():

        if str(row['preIrma_zipcode']) != str(row['current_zipcode']):
            print 
            print i
            print row['preIrma_zipcode'], row['current_zipcode']
            count += 1
            
    print count
    print count/float(len(df))
    
    all_cols = rename_loc.values()
    df1 = df[all_cols]
    #print df1
    df1.to_csv(output_fp, columns=all_cols, index=False)
    
# In the real world, ZIP code boundaries often cross county boundaries. 
# In fact more than 20 percent of all ZIP codes lie in more than one county. 
# https://www.huduser.gov/portal/datasets/usps_crosswalk.htmlhttps://www.huduser.gov/portal/datasets/usps_crosswalk.html
def regions(fp, fp_output, region_id):
    ids = []
    zip_to_name = {}
    zip_to_fips = {}
    fp1 = os.path.join('reference', 'ZIP_COUNTY_092017.csv')
    for i, row in pd.read_csv(fp1, dtype={'zip': str, 'county':str}).iterrows():
        zip_to_fips[row['zip']] = row['county']
    #pprint(zip_to_fips)
    
    fips_to_name = {}
    fp2 = os.path.join('reference', 'FL_COUNTIES.txt')
    for line in open(fp2, 'rU').readlines():
        items = line.split(',')
        code = items[1] + items[2]
        name = items[3]
        fips_to_name[code] = name
     
    df = pd.read_csv(fp)
    unknown = 0
    counts = [0,0,0,0,0]
    for i, row in df.iterrows():
        pre = row['preIrma_zipcode']
        cur = row['current_zipcode']
        if pre in zip_to_fips:
            fips = zip_to_fips[pre]
            #print fips
        else:
            if str(int(cur)) in zip_to_fips:
                fips = zip_to_fips[str(int(cur))]
            elif pre == '33111':
                fips = '12086'
            elif pre == '33740':
                fips = '12103'
            elif pre == '33102':
                fips = '12086'

        
        #print fips
        if fips in fips_to_name:
            name = fips_to_name[fips]
            zip_to_name[pre] = name
            #print name
            for j, region in enumerate(all_regions):
                if name in region:
                    counts[j] += 1
                    break
                    
            if j+1 == region_id:
                ids.append(i)
                
        else:
            unknown += 1
            
    print unknown
    print counts    
    print sum(counts)
    print len(df)
    print ids
    print len(ids)
    
    df1 = df.ix[ids]
    df1.to_csv(fp_output, index=False)
    

#     zip = zipcode.isequal('02115')
#     print zip.state
#     pprint(zip.to_dict())


    
    
    
if __name__ == '__main__':
    fp_input = os.path.join('data', 'MTurk_Irma_Qualtrics.csv')
    fp1 = os.path.join('data', 'MTurk_Irma_location.csv')
    #prep(fp_input, fp1)
    fp2 = os.path.join('data', 'MTurk_Irma_var_cluster_with_loc.csv')
    
    region_id = 5
    fp_output = os.path.join('data', 'MTurk_Irma_var_cluster_region%d.csv' % region_id)
    regions(fp2, fp_output, region_id)