#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
import logging
import os

#Variables that contains the user credentials to access Twitter API 
# access_token = "84530015-pBpdPD8QCsJksYTosHvIjicAtAC8t8FhVdxGreCt7"
# access_token_secret = "JGZ4KNFiqPtYm1E5wAlXLMhzpqtA49Dk4ucXeYZ256PT5"
# consumer_key = "uGR6NQOLUIXmzSSuJFSFhbY3i"
# consumer_secret = "AeRZnA0ziRlNYSSQIjLyh84uObw9b2iiTghDPZukIwhjwsbH1H"

access_token = "84530015-pBpdPD8QCsJksYTosHvIjicAtAC8t8FhVdxGreCt7"
access_token_secret = "JGZ4KNFiqPtYm1E5wAlXLMhzpqtA49Dk4ucXeYZ256PT5"
consumer_key = "uGR6NQOLUIXmzSSuJFSFhbY3i"
consumer_secret = "AeRZnA0ziRlNYSSQIjLyh84uObw9b2iiTghDPZukIwhjwsbH1H"

logging.basicConfig(filename='error.log',level=logging.WARNING, format='%(asctime)s %(message)s')
class MyListener(StreamListener):

    def on_data(self, data):
        try:
            decoded = json.loads(data)
            print '%s @%s: %s' % (decoded['created_at'][:-11], decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
            crt = decoded['created_at']
            year = crt[-4:]
            month = "%02d" % time.strptime(crt[4:7],'%b').tm_mon
            date = crt[8:10]
            hour = crt[11:13]
            # name of output file
            file_name = year + month + date + '_' + hour + '.json'
            fp = os.path.join("E:\Jose\Stream", file_name)

            f_out = open(fp, 'a')
            f_out.write(data)
            f_out.close()
        except Exception as e:
            logging.exception("data error")
        return True

    def on_error(self, status):
        print status
        return True
    
def stream_to_json():
    listener = MyListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    max_tries = 100
    for i in range(max_tries):
        try:
            stream = Stream(auth, listener)
            stream.filter(track=['jose'])
        except Exception as e:
            logging.exception("stream error") 
    logging.error("used up %d tries" % max_tries)     
       
if __name__ == '__main__':
    stream_to_json()
    


    