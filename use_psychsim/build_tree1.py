from copy import copy
from pprint import pprint
import numpy as np

# beliefs = {'sea_level_risk':{'low':0.37, 'med':0.60,'high':0.83},
#             'home_structure':{'mobile':0.68,'other':0.34},
#             'storm_category':{'1':0.11,'2':0.16,'3':0.37,'4':0.87,'5':0.95},
#             'gov_evac':{'strong':0.84,'none':0.20}
#            }
beliefs = [{'sea_level_risk':{'low':0.37, 'med':0.60,'high':0.83}},
           {'home_structure':{'mobile':0.68,'other':0.34}},
           {'storm_category':{'1':0.11,'2':0.16,'3':0.37,'4':0.87,'5':0.95}},
           {'gov_evac':{'strong':0.84,'none':0.20}}]


factors = ['sea_level_risk', 
           'home_structure',
           'storm_category',
           'gov_evac']

values = [['low', 'med', 'high'],
        ['mobile', 'other'],
        ['1', '2', '3', '4', '5'],
        ['strong', 'none']]

probs = [[0.37, 0.60, 0.83],
        [0.68, 0.34],
        [0.11, 0.16, 0.37, 0.87, 0.95],
        [0.84, 0.20]]



'''
{'if': equal('sea_level_risk','low'),
 True: {'if': equal('home_structure','mobile'),
        True: {'if': equal('storm_category','1'),
               True: {'if': equal('gov_evac','strong'),
                      True: {'distribution': [0.37,0.68,0.11,0.84]}
 False: {'if': equal('sea_level_risk','med'),
         True: {'if': equal('home_structure','mobile'),
                True: {'if': equal('storm_category','1'),
                       True: {'if': equal('gov_evac','strong'),
                              True: {'distribution': [0.60,0.68,0.11,0.84]}
 
 
         True: {'if': equal('home_structure', 'mobile'),
        True: {'if': equal('storm_category','1'),
               True: {'if': equal('gov_evac','strong'),
                      True: {'distribution': [0.37,0.68,0.11,0.84]}
                      
''' 

    
                         
value_probs = [('low', 0.37),
              ('mobile', 0.68),
              ('4', 0.87),
              ('strong', 0.84)]

def build(factors, value_probs, level, max_level, acc_probs):
    print '------ level %d -------' % level
    tree = {}
    key = factors[level]
    value, prob = value_probs[level]
    tree['if'] = (key, value)
    
    t_probs = copy(acc_probs)
    t_probs.append(prob)
    print 'true_branch', t_probs
    f_probs = copy(acc_probs)
    f_probs.append(1.0-prob)
    print 'false_branch', f_probs
    
    if level < max_level:
        tree['true'] = build(factors, value_probs, level+1, max_level, t_probs)
        tree['false'] = build(factors, value_probs, level+1, max_level, f_probs)
    else:
        tree['true'] = t_probs
        tree['false'] = f_probs
    
    return tree



if __name__ == '__main__':
    
    #build_tree(beliefs, 0, [], 3)
    #generate_value_idx()
    
    tree = build(factors, value_probs, 0, len(value_probs)-1, [])
    pprint(tree)
    

    
    
    
    