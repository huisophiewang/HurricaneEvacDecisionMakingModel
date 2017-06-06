import numpy as np
from pprint import pprint
from geopy.distance import vincenty
from geopy.distance import great_circle
# longitude -90.8 ~ -79.7 (range 180)
# latitude 24.3 ~ 30.9 (range 90)

def get_coastline_gps():
    fr = open('data/coastline_gps_ne_50m.csv', 'rU')
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
    print len(all_points)
    return all_points

def get_zip_gps():
    fr1 = open(r'data/ZCTA.csv', 'rU')
    header1 = fr1.readline()
    zip_to_gps = {}
    for line in fr1.readlines():
        items = line.split(',')
        zip = items[0]
        zip_to_gps[zip] = (float(items[1]), float(items[2]))
    return zip_to_gps

def get_min_dist(zip_gps, coastline_gps):
    all_d = []
    #print zip_gps
    for p in coastline_gps:
        #print p
        d = vincenty(p, zip_gps).miles
        all_d.append(d)
    min_dist = min(all_d)
    print min_dist
    return min_dist

def get_coast_dist(zip_to_gps, coastline_gps): 
    zip_dist = {}
    fr = open(r'data/IvanExport.csv','rU')
    fw = open(r'data/IvanExport_dist_v2.csv','w')
    header = fr.readline().rstrip() + ',coast_dist' + '\n'
    fw.write(header)
    for line in fr.readlines():
        items = line.rstrip().split(",")
        zip = items[7]
        zip_gps = zip_to_gps[zip]
        if not zip_gps in zip_dist:
            coast_dist = get_min_dist(zip_gps, coastline_gps)
            zip_dist[zip_gps] = coast_dist
        else:
            coast_dist = zip_dist[zip_gps]
        items.append(str(coast_dist))
        outline = ",".join(items) + '\n'
        #print outline
        fw.write(outline)
    fw.close()
    fr.close()
        
        
            
    


if __name__ == '__main__':
    zip_to_gps = get_zip_gps()
    coastline_gps = get_coastline_gps()
    #pprint(zip_to_gps)
    get_coast_dist(zip_to_gps, coastline_gps)
    
    