import psychsim.probability
from psychsim.pwl import *
from psychsim.action import powerset
from psychsim.reward import *
from psychsim.world import *
from psychsim.agent import Agent

import psychsim.ui.diagram as diagram

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


{'if': equalRow(stateKey(resident.name,'sea_level_risk',True),'low'),
 True: {'if': equalRow(stateKey(resident.name,'home_structure',True),'mobile'),
        True: {'if': equalRow(stateKey(resident.name,'storm_category',True),'1'),
               True: {'if': equalRow(stateKey(resident.name,'gov_evac',True),'mobile'),
                      True: {'distribution': makeNoisyDistribution([0.37,0.68,0.11,0.84])}

                      
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
    #tree['if'] = (key, value)
    tree['if'] = equalRow(stateKey(resident.name, key),value)
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
        prob = path_to_prob(probs, path)
        tree['distribution'] = noisy_or(prob, stateKey(resident.name, 'safety'))
        
        tree.pop('if')
    else:    
        add_leaf_prob(probs, tree['true'])
        add_leaf_prob(probs, tree['false'])
    tree.pop('path')
    return tree

def noisy_or(prob, key):
    ### p(evac) = 1 - (1-p1)*(1-p2)*(1-p3)*(1-p4)
    p_off = 1.0
    for p in prob:
        p_off = p_off * (1-p)
    return [(setTrueMatrix(key),1.0-p_off),(setFalseMatrix(key),p_off)]
    #return (1-p_off, p_off)
    
# if __name__ == '__main__':
#    tree = build(factors, values, probs, 0, 0)
#     #pprint(tree)
#     add_path(tree, [])
#     #pprint(tree)
#     add_leaf_prob(probs, tree)
#     pprint(tree)


bel_seq = ['sea_level_house','home_structure','storm_category','gov_evac']

objectives = {
    'evacuate': \
        {'objective': 'Safety',
         'actions': {},
         'beliefs': {'sea_level_risk':{'low':0.37, 'mod':0.60,'hi':0.83},
                     'home_structure':{'mobile':0.68,'other':0.34},
                     'storm_category':{'1':0.11,'2':0.16,'3':0.37,'4':0.87,'5':0.95},
                     'gov_evac':{'strong':0.84,'none':0.20}
                     }
         }
    }

# Statements about a resident's hypothetical behaviors

behaviors = {
    'evacuate': \
        {'statement': 'I would evacuate.',
         'response': 3,
         'phase': 'where','location': 'home'},
    'stay': \
        {'phase': 'where','location': 'home'},
    }


#         prob = noisyOr(tree[True],.75,.1)
#         return {'distribution': [(setTrueMatrix(key),prob),(setFalseMatrix(key),1.-prob)]}
# 
#     
# 
# # def noisyOr(onCount,onProb,leak=0.):
#     return 1.- (1.-leak)*pow(1.-onProb,onCount)

if __name__ == '__main__':
    # State

    world = World()
    world.diagram = diagram.Diagram()
    world.diagram.setColor(None,'ivory')

    resident = Agent('resident')
    world.diagram.setColor(resident.name,'palegreen')
    world.addAgent(resident)
    world.defineState(resident.name,'sea_level_house', list, ['low','med','hi'])
    world.defineState(resident.name,'home_structure', list, ['mobile','other'])
    world.defineState(resident.name,'storm_category',list, ['1','2','3','4','5'])
    world.defineState(resident.name,'gov_evac', list, ['strong','none'])
    world.defineState(resident.name,'loc_evac_phone',bool)
    world.defineState(resident.name,'peer_evac_info',bool)
    world.defineState(resident.name,'expect_prop_risk',bool)
    world.defineState(resident.name,'expect_personal_risk',bool)

    bel_seq = ['sea_level_house','home_structure','storm_category','gov_evac']

    gov = Agent('state_gov')
    city = Agent('local_gov')
    world.diagram.setColor(gov.name,'cornflowerblue')
    world.addAgent(gov)
    world.diagram.setColor(city.name,'blue')
    world.addAgent(city)

    world.setOrder([resident.name])

    # Keep track of orthogonal dimensions of decision-making
    phase = world.defineState(None,'phase',list,['where'],
                              description='What is being decided at this stage of the simulation')
    world.setState(None,'phase','where')

    # Where is the resident now?
    location = world.defineState(resident.name,'location',list,['home','beyond'])
    resident.setState('location','home')

    # Decisions
    for name,entry in behaviors.items():
        entry['action'] = Action({'subject': resident.name,'verb': name})

    # Generate possible combinations of actions
    options = {}
    


    tree = build(factors, values, probs, 0, 0)
    add_path(tree, [])
    add_leaf_prob(probs, tree)
    pprint(tree)

    
     
    # Movement dynamics
    # world.setDynamics(location,behaviors['evacuate']['action'],makeTree(setToConstantMatrix(location,'beyond')))
    # world.setDynamics(location,behaviors['return']['action'],makeTree(setToConstantMatrix(location,'home')))

    # Phase dynamics
    #world.setDynamics('phase',True,makeTree({'if': equalRow('phase','where'),
    #                                         True: setToConstantMatrix('phase','how'),
    #                                         False: setToConstantMatrix('phase','where')}))

    # Decision-making parameters
#     resident.setAttribute('horizon',2)
#     resident.setAttribute('selection','distribution')
#     
#     world.save('hurricane5.psy')
# 
#     world.printState()
# 
#     for tree,weight in resident.getAttribute('R').items():
#         print weight,tree
#     decision = Distribution()
#     for vector in world.state[None].domain():
#         world.printVector(vector)
#         result = resident.decide(vector,selection='distribution')
#         for action in result['action'].domain():
#             decision.addProb(action,world.state[None][vector]*result['action'][action])
#             print 'Choice:',action
#             outcome = world.stepFromState(vector,action)
#             world.printState(outcome['new'])
#     print decision

