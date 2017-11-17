import pandas as pd

"""
It seems to be the second time you answered this survey. We require each worker to answer at most once.
"""

mturk_fp = r'C:\Users\Sophie\Google Drive\Research\MTurk Data Collection\Data\batch5_100samples\Batch_3008404_batch_results.csv'
mturk = pd.read_csv(mturk_fp)
ids_m = set(mturk['WorkerId'])
print len(ids_m)


qualtrics_fp = r'C:\Users\Sophie\Google Drive\Research\MTurk Data Collection\Data\batch5_100samples\qualtrics_duplicate_ids.xlsx'
qualtrics = pd.read_excel(qualtrics_fp)
ids_q = set(qualtrics['Q38'])


for id in ids_m:
    if id in ids_q:
        print id

