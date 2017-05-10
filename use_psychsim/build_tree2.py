from pprint import pprint
from copy import copy
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

beliefs = [{'sea_level_risk':{'low':0.37, 'med':0.60,'high':0.83}},
           {'home_structure':{'mobile':0.68,'other':0.34}},
           {'storm_category':{'1':0.11,'2':0.16,'3':0.37,'4':0.87,'5':0.95}},
           {'gov_evac':{'strong':0.84,'none':0.20}}]


factors = ['sea_level_risk', 
           'home_structure',
           'storm_category',
           'gov_evac']

# factors = ['sea_level_risk', 
#            'home_structure']

values = [['low', 'med', 'high'],
        ['mobile', 'other'],
        ['1', '2', '3', '4', '5'],
        ['strong', 'none']]

probs = [[0.37, 0.60, 0.83],
        [0.68, 0.34],
        [0.11, 0.16, 0.37, 0.87, 0.95],
        [0.84, 0.20]]

def build(factors, values, probs, level1, level2):
    #print 'level1=%d, level2=%d' % (level1, level2)
    tree = {}
    key = factors[level1]
    value = values[level1][level2]
    tree['if'] = (key, value)
    # len(values[level1])-2
    if level1 == len(factors)-1:
        tree['true'] = {'if':'leaf'}
        if level2 == len(values[level1])-2:
            tree['false'] = {'if':'leaf'}
        else:
            tree['false'] = build(factors, values, probs, level1, level2+1)
    else:   
        if level2 < len(values[level1])-2:
            tree['true'] = build(factors, values, probs, level1+1, 0)
            tree['false'] = build(factors, values, probs, level1, level2+1)
        else:
            tree['true'] = build(factors, values, probs, level1+1, 0)
            tree['false'] = build(factors, values, probs, level1+1, 0)
    return tree


def add_path(tree, path):
    #print tree['if']
    tree['path'] = path
    if tree['if'] != 'leaf':
        path_t = copy(path)
        path_t.append('T')
        add_path(tree['true'], path_t)
        path_f = copy(path)
        path_f.append('F')
        add_path(tree['false'], path_f)
    return tree


def path_to_prob(probs, path):
    result = []
    level1, level2 = 0, 0
    for e in path:
        #print level1, level2
        if e == 'T':
            result.append(probs[level1][level2])
            level1 += 1
            level2 = 0
        if e == 'F':
            if level2 == len(probs[level1])-2:
                result.append(probs[level1][level2+1])
                level1 += 1
                level2 = 0
            else:
                level2 += 1
    #print result
    return result

def add_leaf_prob(probs, tree):
    if tree['if'] == 'leaf': 
        path = tree['path']
        #print path
        prob = path_to_prob(probs, path)
        tree['prob'] = prob
        tree['distribution'] = noisy_or(prob)
        tree.pop('if')
    else:    
        add_leaf_prob(probs, tree['true'])
        add_leaf_prob(probs, tree['false'])
    tree.pop('path')
    return tree

def noisy_or(distribution):
    ### p(evac) = 1 - (1-p1)*(1-p2)*(1-p3)*(1-p4)
    p_off = 1.0
    for p in distribution:
        p_off = p_off * (1-p)
    return (1-p_off, p_off)
        
     
    
if __name__ == '__main__':
    tree = build(factors, values, probs, 0, 0)
    #pprint(tree)

    add_path(tree, [])
    #pprint(tree)
    
    add_leaf_prob(probs, tree)
    pprint(tree)

    
        
    