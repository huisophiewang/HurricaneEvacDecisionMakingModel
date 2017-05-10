import pandas as pd

def select_cols():
    df = pd.read_csv(r'IvanExport.csv')
    #print df['sname']
    cols = ['state', 'samp', 'gender', 'q1110','q99','q102','q103','q104','q105','q106', 'q112','q113','q2']
    df.to_csv('Ivan_by_County.csv', columns=cols, index=False)
    
def race():
    
if __name__ == '__main__':
    select_cols()