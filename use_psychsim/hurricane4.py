"""

"""


import psychsim.probability
from psychsim.pwl import *
from psychsim.action import powerset
from psychsim.reward import *
from psychsim.world import *
from psychsim.agent import Agent

import psychsim.ui.diagram as diagram

# State
world.defineState(resident.name,'sea_level_house',['low','med','hi'])
world.defineState(resident.name,'home_structure', ['mobile','other'])
world.defineState(resident.name,'storm_category',['1','2','3','4','5'])
world.defineState(resident.name,'gov_evac',['strong','none'])
world.defineState(resident.name,'loc_evac_phone',bool)
world.defineState(resident.name,'peer_evac_info',bool)
world.defineState(resident.name,'expect_prop_risk',bool)
world.defineState(resident.name,'expect_personal_risk',bool)

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


# importance = {
#     'risk':
#         {'statement': 'Risk of anthrax exposure or infection.',
#          'agent': False,
#          'response': 3,
#          'rank': 1},
#     'employment':
#         {'statement': 'Availability of employment in the Seattle area.',
#          'agent': False,
#          'response': 3,
#          'rank': 5},
#     }
# beliefs.update(importance)

         
# {'if': equalRow(stateKey(resident.name,'sea_level_risk',True),'low'),
#  True: {'if': equalRow(stateKey(resident.name,'home_structure',True),'mobile'),
#         True: {'if': equalRow(stateKey(resident.name,'storm_category',True),'1'),
#                True: {'if': equalRow(stateKey(resident.name,'gov_evac',True),'mobile'),
#                       True: {'distribution': makeNoisyDistribution([0.37,0.68,0.11,0.84])}

                      


def buildTree(tree,objectives, plist):
    for name, objective in objectives:
        tree = buildSubtree(tree,objectives, plist)
    return tree
 
def buildSubtree(tree,objective, plist):
    if tree.has_key('if'):
        return {'if': tree['if'],
                True: leaf2matrix(tree[True],key),
                False: leaf2matrix(tree[False],key)}
    else:
        for key in objective[beliefs].keys():
            return {'if': something,
                    True: something
        prob = noisyOr(tree[True],.75,.1)
        return {'distribution': [(setTrueMatrix(key),prob),(setFalseMatrix(key),1.-prob)]}
 
     
     
    if tree.has_key('if'):
        return {'if': tree['if'],
                True: incrementLeaves(tree[True],value),
                False: incrementLeaves(tree[False],value)}
    elif value:
        return {True: tree[True]+1,False: tree[False]}
    else:
        return {True: tree[True],False: tree[False]+1}
 
                 
 
def leaf2matrix(tree,key):
    if tree.has_key('if'):
        return {'if': tree['if'],
                True: leaf2matrix(tree[True],key),
                False: leaf2matrix(tree[False],key)}
    else:
        prob = noisyOr(tree[True],.75,.1)
        return {'distribution': [(setTrueMatrix(key),prob),(setFalseMatrix(key),1.-prob)]}
 
def noisyOr(onCount,onProb,leak=0.):
    return 1.- (1.-leak)*pow(1.-onProb,onCount)

if __name__ == '__main__':
    world = World()
    world.diagram = diagram.Diagram()
    world.diagram.setColor(None,'ivory')

    resident = Agent('resident')
    world.diagram.setColor(resident.name,'palegreen')
    world.addAgent(resident)
    world.defineState(resident.name,'sea_level_house',list,['low','med','hi'])
    world.defineState(resident.name,'home_structure', list,['mobile','high_rise','other'])
    world.defineState(resident.name,'storm_category',list,['1','2','3','4','5'])
    world.defineState(resident.name,'gov_evac',list,['strong','weak','none'])
    world.defineState(resident.name,'loc_evac',bool)
    world.defineState(resident.name,'peer_evac',bool)
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
    
 

    # Choices of where to live
    # for joint in [name for name in behaviors.keys() if behaviors[name]['phase'] == 'where']:
    #     options[joint] = resident.addAction(behaviors[joint]['action'])
    #     # Only legal during "where" phase
    #     resident.setLegal(options[joint],makeTree({'if': equalRow('phase','where'),
    #                                                True: {'if': equalRow(location,behaviors[name]['location']),
    #                                                       True: True, False: False},
    #                                                False: False}))

    # Objectives
    ranks = [objective['rank'] for objective in objectives.values()]
    ceiling = max(ranks) + 1
    total = float(sum(ranks))
    for name,objective in objectives.items():
        objective['key'] = world.defineState(resident.name,name,bool)
        world.setFeature(objective['key'],True)
        resident.setReward(maximizeFeature(objective['key']),float(ceiling-objective['rank'])/total)

    # Beliefs

            agent = resident.name
        else:
            agent = None
        belief['key'] = world.defineState(agent,name,bool,description=belief['statement'])
        distribution = {True: response2belief[belief['response']]}
        distribution[False] = 1. - distribution[True]
#        world.setFeature(belief['key'],psychsim.probability.Distribution(distribution))
        world.setFeature(belief['key'],round(distribution[True]) == 1)

    # Dynamics of objectives
    for name,objective in objectives.items():
        tree= {}
        for bel in objective['beliefs']:
            for feature,value in bel.items():
                tree = increment_tree(tree, feature,value)



                tree = {'if': trueRow(beliefs[feature]['key']),
                        True: incrementLeaves(tree,value),
                        False: incrementLeaves(tree,not value)}
            tree = leaf2matrix(tree,objective['key'])
            if name == 'safety':
                tree = {'if': equalRow(stateKey(resident.name,'location',True),'home'),
                        True: tree, False: setTrueMatrix(objective['key'])}
            world.setDynamics(objective['key'],option,makeTree(tree))
    
    # Movement dynamics
    # world.setDynamics(location,behaviors['evacuate']['action'],makeTree(setToConstantMatrix(location,'beyond')))
    # world.setDynamics(location,behaviors['return']['action'],makeTree(setToConstantMatrix(location,'home')))

    # Phase dynamics
    #world.setDynamics('phase',True,makeTree({'if': equalRow('phase','where'),
    #                                         True: setToConstantMatrix('phase','how'),
    #                                         False: setToConstantMatrix('phase','where')}))

    # Decision-making parameters
    resident.setAttribute('horizon',2)
    resident.setAttribute('selection','distribution')
    
    world.save('hurricane2.psy')

    world.printState()

    for tree,weight in resident.getAttribute('R').items():
        print weight,tree
    decision = Distribution()
    for vector in world.state[None].domain():
        world.printVector(vector)
        result = resident.decide(vector,selection='distribution')
        for action in result['action'].domain():
            decision.addProb(action,world.state[None][vector]*result['action'][action])
            print 'Choice:',action
            outcome = world.stepFromState(vector,action)
            world.printState(outcome['new'])
    print decision
