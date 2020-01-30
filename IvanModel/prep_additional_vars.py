import numpy as np
from pprint import pprint
from geopy.distance import vincenty
from geopy.distance import great_circle
# longitude -90.8 ~ -79.7 (range 180)
# latitude 24.3 ~ 30.9 (range 90)

# from http://naturalearthdata.com/downloads/10m-physical-vectors
# used software qgis to convert to csv
def get_coastline_gps():
    #fr = open('data/coastline_gps_ne_50m.csv', 'rU')
    fr = open('data/coastline_gps_ne_10m.csv', 'rU')
    header = fr.readline()
    all_points = []
    for line in fr.readlines():
        items = line.split(",")
        longi = float(items[0])
        lati = float(items[1])
        if longi < -79.7 and longi > -90.8:
            if lati < 30.9 and lati > 24.3:
                #print line
                all_points.append((lati, longi))
    #print len(all_points)
    fr.close()
    return all_points

# get zipcode area center point gps
def get_zip_gps():
    fr1 = open(r'data/ZCTA.csv', 'rU')
    header1 = fr1.readline()
    zip_to_gps = {}
    for line in fr1.readlines():
        items = line.split(',')
        zip = items[0]
        zip_to_gps[zip] = (float(items[1]), float(items[2]))
    fr1.close()
    return zip_to_gps

#get min distance to coastline, in miles
def get_min_dist(zip_gps, coastline_gps):
    all_d = []
    #print zip_gps
    for p in coastline_gps:
        d = vincenty(p, zip_gps).miles
        all_d.append(d)
    min_dist = min(all_d)
    #print min_dist
    return min_dist

#### website that gets elevation from latitude and longitude
### http://www.gpsvisualizer.com/elevation, metric: feet
def get_zip_elev():
    zip_to_elev = {}
    fr = open(r'data/ZIP_ELEV.csv', 'rU')
    fr.readline()
    for line in fr.readlines():
        items = line.split(',')
        zip = items[0]
        elev = items[3].strip()
        zip_to_elev[zip] = elev
    #pprint(zip_to_elev)
    fr.close()
    return zip_to_elev
    

def add_vars(fpr, fpw): 
    zip_to_gps = get_zip_gps() 
    coastline_gps = get_coastline_gps()
    zip_dist = {}
    zip_to_elev = get_zip_elev()
    fr = open(fpr,'rU')
    fw = open(fpw,'w')
    header = fr.readline().strip().split()
    header.append('coast_dist')
    header.append('elevation')
    header.extend(['issued_mandatory', 'issued_voluntary'])
    
    fw.write(','.join(header) + '\n')
    for line in fr.readlines():
        items = line.rstrip().split(",")
        zip = items[7]
        state = items[6].strip('"')
        county = items[11].strip('"')

        
        # add coast distance
        zip_gps = zip_to_gps[zip]
        if not zip_gps in zip_dist:
            coast_dist = get_min_dist(zip_gps, coastline_gps)
            zip_dist[zip_gps] = coast_dist
        else:
            coast_dist = zip_dist[zip_gps]
        items.append(str(coast_dist))
       
        # add elevation
        elev = zip_to_elev[zip]
        items.append(elev)
        
        # add evac order issued
        manda = 0
        volun = 0
        if state == "FL":
            if county in ['escambia county', 'okaloosa county','bay county']:
                manda = 1
            if county == 'walton county' and zip in ['32437','32439','32459']:
                manda = 1
            if county in ['gulf county', 'santa rosa county'] and elev < 10:
                manda = 1
        if state == 'AL':
            if int(zip) in [36542, 36561]:
                manda = 1
        if state == 'MS':
            if int(zip) in [39572, 39520, 39576, 39571, 39560, 39501, 39507, 39531, 
                            39532, 39530, 39540, 39564, 39553, 39595, 39567, 39563, 39581]:
                manda = 1
        if state == 'LA':
            if county in ['st. charles parish', 'plaquemines parish']:
                manda = 1
            if county in ['orleans parish', 'jefferson parish']:
                volun = 1
                
        items.append(str(manda))
        items.append(str(volun))
                
        outline = ",".join(items) + '\n'
        fw.write(outline)
    fw.close()
    fr.close()        
        
            

if __name__ == '__main__':
    input_fp = r'data/IvanExport.csv'
    output_fp = r'data/IvanExport_addvars.csv'
    add_vars(input_fp, output_fp)
    

    

    #add_coast_dist_elev()
    #get_zip_elev()
    