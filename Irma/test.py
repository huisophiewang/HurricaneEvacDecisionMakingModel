import tweepy
import json
import time
import os
import logging
import datetime
from pprint import pprint
  
#Variables that contains the user credentials to access Twitter API 
access_token = "84530015-w89FAuFtTUvoNDtVS7RZwrCiQt0asWx6fpSXDgbtx"
access_token_secret = "BRzX0YgpXDS6Us4xgHlGwxzWAKetmHYsTCswkygmHoo0b"
consumer_key = "KwdMLUNxWYuiGUBw9farA0OSy"
consumer_secret = "ER1ugfvw4dMkRISLaoXa8FI7pg4hRtKlxOHYuc1EwnFWgvOume"

logging.basicConfig(filename='search_error_test.log',level=logging.INFO, format='%(asctime)s %(message)s')


def query_api(api, date, max_id=None):
    # max count allowed is 100

    since_dt = datetime.datetime.strptime(date, "%Y%m%d").date()
    until_dt = since_dt + datetime.timedelta(days=1)
    # keyword here is case insensitive
    q_str = r'Irma since:%s until:%s' % (since_dt, until_dt)
    
    if not max_id:
        tweets = api.search(q_str, count=100, include_entities=True)
    else:
        tweets = api.search(q_str, count=100, max_id=max_id, include_entities=True)      
    return tweets


def write_to_json(tweets, to_dir):  
    for tweet in tweets:
        #print json.dumps(tweet._json, indent=4, sort_keys=True)
        print '%s %d' % (tweet._json['created_at'], tweet._json['id'])
        crt = tweet._json['created_at']
        year = crt[-4:]
        month = "%02d" % time.strptime(crt[4:7],'%b').tm_mon
        date = crt[8:10]
        hour = crt[11:13]
        file_name = year + month + date + '_' + hour + '.json'
        f_out = open(os.path.join(to_dir, file_name), 'a')
        # json dumps returns a string, json dump write to file
        to_str = json.dumps(tweet._json, f_out, sort_keys=False)
        #json.dump(tweet._json, f_out, sort_keys=False)
        f_out.write(to_str + '\n')
        f_out.close()
        
 
def search(dt): 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    #to_dir = dt
 
    #to_dir = os.path.join(r"E:\Irma\Search", dt)
    to_dir = os.path.join("Search",dt)
           
    
    # when start search for a new date
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
        first_query = query_api(api, dt)
        write_to_json(first_query[:1], to_dir)   
    while True:
        try:
            # when resume from waiting or unfinished search, 
            # read the last line of latest file to get max_id
            
            files = os.listdir(to_dir)
            fw_name = sorted(files)[0]   
            fw_path = os.path.join(to_dir, fw_name)
            
            # if file size is too big, rename it, copy the last line, start a new file
            size = os.path.getsize(fw_path) / float(1000000)
            if size > 800:
                temp_name = fw_name[:-5] + '_save.json'
                os.rename(fw_path, os.path.join(to_dir, temp_name))
                lastline = open(os.path.join(to_dir, temp_name)).readlines()[-1]
                fw = open(fw_path, 'a')
                fw.write(lastline)
                fw.close()
                
            with open(os.path.join(to_dir, fw_name)) as fw:
                lastline = fw.readlines()[-1]
                fw.close()
                next_max_id = json.loads(lastline)['id']                                
                tweets = query_api(api, dt, max_id = next_max_id)
                 
                if len(tweets)==1:
                    logging.info("search finished!")
                    print "search finished!"
                    break
                else:
                    write_to_json(tweets[1:], to_dir)

            
        except tweepy.error.TweepError:
            print datetime.datetime.now()
            logging.exception("search error") 
            print 'waiting...'
            time.sleep(15 * 60)
        except Exception as e:
            print datetime.datetime.now()
            logging.exception("other error") 
    return

    
if __name__ == '__main__': 
    dt = '20170910'
    #hr = '17'
    #dates = ['20161007'] 
    
    
    #for dt in dates:
    search(dt)
    


#     to_dir = os.path.join("Search",dt)
#     files = os.listdir(to_dir)
#     pprint(files)
#     fw_name = sorted(files)[0] 
#     print fw_name
#     
#     
#     fp = os.path.join(to_dir, fw_name)
#     temp_name = fw_name[:-5] + '_1.json'
#     os.rename(fp, os.path.join(to_dir, temp_name))
#     
    #open(os.path.join(to_dir, fw_name)).readlines()[-1]
#     lastline = open(os.path.join(to_dir, temp_name)).readlines()[-1]
#     print lastline
#     fw = open(os.path.join(to_dir, fw_name), 'a')
#     fw.write(lastline)
#     fw.close()



    
    

    

    