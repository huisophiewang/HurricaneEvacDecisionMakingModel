import boto3
from pprint import pprint
import pandas as pd

# API reference:
#http://boto3.readthedocs.io/en/latest/reference/services/mturk.html

region_name = 'us-east-1'


endpoint_url_sandbox = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

done_Harvey_before_qualification_id = '3EZ90CUA4P0848YFDW7RKS8ODM1WIZ'
done_Irma_before_qualification_id = '3VVYNZTOMVBUPKFQKDAOB6VKTZTDA8'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
    aws_access_key_id='',
    aws_secret_access_key='',
)

#get all hits
# res = client.list_hits()['HITs']
# print len(res)
# pprint(res)

#mturk_fp = r'C:\Users\Sophie\Google Drive\Research\MTurk Data Collection\Data\worker_ids\after_batch_5\User_900338_workers.csv'
#mturk_fp = r'C:\Users\Sophie\Google Drive\Research\MTurk Data Collection\Data\Irma\worker ids\batch 2\Batch_3040701_batch_results.csv'
mturk_fp = r'C:\Users\Sophie\Google Drive\Research\MTurk Data Collection\Data\Irma\worker ids\Batch11_results.csv'
mturk = pd.read_csv(mturk_fp)
ids_m = mturk['WorkerId']


# print len(ids_m)
# pprint(ids_m)

for worker_id in ids_m:
    client.associate_qualification_with_worker(
        QualificationTypeId = done_Irma_before_qualification_id,
        WorkerId = worker_id,
        IntegerValue = 1,
        SendNotification=False
    )
     
print('done')

