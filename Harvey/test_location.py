import os
import json
import string
import re
from pprint import pprint

regex = re.compile(r'http\S+')

total = 0
ct_coord = 0
ct_place = 0
ct_coord_place = 0
fr = open('test.json')  
for line in fr.readlines():
    if not line:
        continue
    total += 1
    json_dict = json.loads(line)

    
    #pprint(json_dict)
    
    coord = json_dict['coordinates']
    place = json_dict['place']
    if coord:
        ct_coord += 1
        print '------'
        print coord
        
        if place:
            ct_coord_place += 1
            
        
    if place:
        ct_place += 1
        print place
        
print total
print ct_coord
print ct_place
print ct_coord_place
    
#     txt = json_dict['text'].encode('ascii','ignore')
#     txt = regex.sub('', txt)
#     txt = string.replace(txt, '\n', ' ')
#     user = json_dict['user']['screen_name']
#     created_at = json_dict['created_at'][:-11]