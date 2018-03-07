import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def plot_edu(fp):
    
    df = pd.read_csv(fp)
    df1 = df.groupby(['edu']).size()
    total = df1.sum()
    df2 = df1/total
    print df2
    
    res = [{'some high school':0.128, 
           'high school graduate':0.292,
           'some college':0.301,
           'college graduate':0.178,
           'graduate school':0.10
           }]
    
    
    df1 = pd.DataFrame(res, columns=['some high school', 'high school graduate', 'some college', 'college graduate', 'graduate school'])
    print df1
    # MTurk subjects or American Community Surveys 2012-2016
    df1.plot(kind='bar', rot=-90, title='American Community Surveys 2012-2016')
    plt.tick_params(axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom='off',      # ticks along the bottom edge are off
                    top='off',         # ticks along the top edge are off
                    labelbottom='off') # labels along the bottom edge are off
    plt.xlabel('highest education level')
    plt.ylabel('percentage')
    plt.show() 
    
def plot_income(fp):
    df = pd.read_csv(fp)
    df1 = df.groupby(['income']).size()
    total = df1.sum()
    df2 = df1/total
    print df2
    
    res = [{r'less than $15,000':0.129,
            r'$15,000 to $25,000':0.117, 
            r'$25,000 to $40,000':0.166, 
            r'$40,000 to $80,000':0.279, 
            r'over $80,000':0.308}]
    
    df1 = pd.DataFrame(res, columns=[r'less than $15,000',
                                     r'$15,000 to $25,000', 
                                     r'$25,000 to $40,000', 
                                     r'$40,000 to $80,000', 
                                     r'over $80,000'])
    print df1
    # MTurk subjects or American Community Surveys 2012-2016
    df1.plot(kind='bar', rot=-90, title='American Community Surveys 2012-2016')
    plt.tick_params(axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom='off',      # ticks along the bottom edge are off
                    top='off',         # ticks along the top edge are off
                    labelbottom='off') # labels along the bottom edge are off
    plt.xlabel('yearly household income')
    plt.ylabel('percentage')
    plt.show() 
    
def plot_gender(fp):
    print fp
    df = pd.read_csv(fp)
    df1 = df.groupby(['is_male']).size()
    total = df1.sum()
    df2 = df1/total
    print df2
    
    res = [{'female':0.619, 
           'male':0.381,
           }]
     
     
    df1 = pd.DataFrame(res, columns=['female', 'male'])
    print df1
    # MTurk subjects or American Community Surveys 2012-2016
    df1.plot(kind='bar', rot=-90, title='American Community Surveys 2012-2016')
    plt.tick_params(axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom='off',      # ticks along the bottom edge are off
                    top='off',         # ticks along the top edge are off
                    labelbottom='off') # labels along the bottom edge are off
    plt.xlabel('gender')
    plt.ylabel('percentage')
    plt.show() 
    
def plot_age(fp):
    df = pd.read_csv(fp)
    for i, row in df.iterrows():
        if row['age'] >= 18 and row['age'] <=24:
            df.set_value(i, 'age_group', 1)
        elif row['age'] >= 25 and row['age'] <= 34:
            df.set_value(i, 'age_group', 2)
        elif row['age'] >= 35 and row['age'] <= 44:
            df.set_value(i, 'age_group', 3) 
        elif row['age'] >= 45 and row['age'] <= 54:
            df.set_value(i, 'age_group', 4) 
        elif row['age'] >= 55 and row['age'] <= 64:
            df.set_value(i, 'age_group', 5) 
        elif row['age'] >= 65 and row['age'] <= 74:
            df.set_value(i, 'age_group', 6) 
        else:
            print row['age']
            df.set_value(i, 'age_group', 7)
            
    df1 = df.groupby(['age_group']).size()
    total = df1.sum()
    df2 = df1/total
    print df2

    
    
    res = [{'18 to 24 years':0.112, 
           '25 to 34 years':0.160,
           '35 to 44 years':0.153,
           '45 to 54 years':0.174,
           '55 to 64 years':0.164,
           '65 to 74 years':0.132,
           '75 years and over':0.108
           }]
     
     
    df1 = pd.DataFrame(res, columns=['18 to 24 years', 
                                     '25 to 34 years',
                                     '35 to 44 years',
                                     '45 to 54 years',
                                     '55 to 64 years',
                                     '65 to 74 years',
                                     '75 years and over'
                                     ])
    print df1
    # MTurk subjects or American Community Surveys 2012-2016
    df1.plot(kind='bar', rot=-90, title='American Community Surveys 2012-2016')
    plt.tick_params(axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom='off',      # ticks along the bottom edge are off
                    top='off',         # ticks along the top edge are off
                    labelbottom='off') # labels along the bottom edge are off
    plt.xlabel('age')
    plt.ylabel('percentage')
    plt.show() 
    
def plot_race(df):
    df = pd.read_csv(fp)
    total = len(df)
    print df['is_white'].sum()/float(total)
    print df['is_black'].sum()/float(total)
    print df['is_asian'].sum()/float(total)
    #print df['is_hispanic'].sum()/float(total)
    
    
     
    res = [{'white':0.759, 
           'black':0.161,
           'asian':0.026,
           'other':0.054
           }]
      
      
    df1 = pd.DataFrame(res, columns=['white', 'black', 'asian', 'other'])
    print df1
    # MTurk subjects or American Community Surveys 2012-2016
    df1.plot(kind='bar', rot=-90, title='American Community Surveys 2012-2016')
    plt.tick_params(axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom='off',      # ticks along the bottom edge are off
                    top='off',         # ticks along the top edge are off
                    labelbottom='off') # labels along the bottom edge are off
    plt.xlabel('race')
    plt.ylabel('percentage')
    plt.show() 
              
if __name__ == '__main__':
    #fp = os.path.join('data', 'MTurk_Harvey.csv')
    fp = os.path.join('data', 'MTurk_Irma.csv')
    #plot_edu(fp)
    #plot_income(fp)
    #plot_age(fp)
    plot_race(fp)
    #plot_gender(fp)
