from geopy.distance import vincenty
from pprint import pprint
tract_ids = [701, 702, 703, 704, 705, 706, 709, 710,
          711, 712, 713, 714, 716, 719, 720, 721,
          722, 723, 724, 725, 726, 727, 728, 729, 
          730, 731, 732, 733, 734, 735, 736, 737, 
          738, 739, 740, 743, 744, 2572]

coastline_gps = [(41.1758, -73.1823), 
                 (41.1675, -73.1798),
                 (41.1607, -73.1879),
                 (41.1588, -73.2040),
                 (41.1057, -73.2157),
                 (41.1437, -73.2287),
                 (41.1729, -73.1770),
                 (41.1600, -73.1693)]

def get_tract_center():
    tract_gps = {}
    fp = 'data/CenPop2010_Mean_TR09.txt'
    for line in open(fp, 'r').readlines():
        items = line.split(',')
        # Fairfax county
        if items[1] != '001':
            continue
        if items[2][:-2] == '2572':
            tract_id ='2572'
        else:
            tract_id = items[2][1:-2]

        if int(tract_id) in tract_ids:
            lati = items[4]
            longi = items[5].strip('\n') 
            tract_gps[tract_id] = (lati, longi)
            
            print tract_id, lati, longi
    #pprint(tract_gps)   
    
    return tract_gps
            
# def get_coastline_gps():
#     fr = open('data/coastline_gps_ne_50m.csv', 'rU')
#     header = fr.readline()
#     all_points = []
#     for line in fr.readlines():
#         items = line.split(",")
#         longi = float(items[0])
#         lati = float(items[1])
#         if longi < -73.1 and longi > -73.3:
#             if lati < 41.3 and lati > 41.0:
#                 print line
#                 all_points.append((lati, longi))
#     #print len(all_points)
#     
#     return all_points

def get_coast_dist(center_gps, coastline_gps):
    fp = 'data/census_tract_dist_to_coast.csv'
    fw = open(fp, 'w')
    fw.write('id,distance\n')
    for id in tract_ids:
        print id
        all_d = []
        for point in coastline_gps:
            d = vincenty(center_gps[str(id)], point).miles
            all_d.append(d)
        min_d = min(all_d)
 
        #print min_d
        outline = '%s,%.4f\n' % (id, min_d)
        print outline
        fw.write(outline)
    fw.close()
        
        

if __name__ == '__main__':
    center_gps = get_tract_center()
    #get_coast_dist(center_gps, coastline_gps)