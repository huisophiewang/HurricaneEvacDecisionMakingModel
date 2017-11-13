import pandas as pd

"""
It seems to be the second time you answer this survey. We require each worker to answer at most once.
"""

mturk = pd.read_csv("Batch_2993240_batch_results.csv")
ids_m = set(mturk['WorkerId'])


qualtrics_recorded = pd.read_csv("Hurricane_Evacuation_Questionnaire_Recorded.csv")
qualtrics_in_progress = pd.read_csv("Hurricane_Evacuation_Questionnaire_InProgress.csv")

ids_q1 = set(qualtrics_recorded['Q38'][2:])
print len(ids_q1)
print len(set(ids_q1))

suspects = []
for id in ids_m:
    if not id in ids_q1:
        #print id
        suspects.append(id)
        
print len(suspects)

confirmed_suspects = []
ids_q2 = set(qualtrics_in_progress['V78'][1:])
for i in suspects:
    if i in ids_q2:
        #print i
        confirmed_suspects.append(i)
        
print len(confirmed_suspects)
