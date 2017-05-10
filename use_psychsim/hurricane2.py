"""
Modeling the decision-making of Seattle residents after an anthrax release. Based on:
Heather Rosoff, Richard John, William J. Burns, and Robert Siko (2012). 
"Structuring Uncertainty and Conflicting Objectives for Life or Death
Decisions Following an Urban Biological Catastrophe". 
Journal of Integrated Disaster Risk Management.
"""
# TODO: SRA
# TODO: pull out relevant text from proposal and any other writeups.

import psychsim.probability
from psychsim.pwl import *
from psychsim.action import powerset
from psychsim.reward import *
from psychsim.world import *
from psychsim.agent import Agent

import psychsim.ui.diagram as diagram

# Statements about a resident's beliefs
beliefs = {
    'dependents': \
        {'statement': 'I believe my dependents are at risk.',
         'agent': True,
         'response': 4},
    'wind_house': \
        {'statement': 'I believe wind damage poses a serious risk to my house.',
         'agent': True,
         'response': 1},
    'flooding_house': \
        {'statement': 'I believe the flooding poses a serious risk to my house.',
         'agent': True,
         'response': 1},
    'wind_personal': \
        {'statement': 'I believe wind damage poses a serious risk to my family.',
         'agent': True,
         'response': 1},
    'flooding_personal': \
        {'statement': 'I believe the flooding poses a serious risk to my family.',
         'agent': True,
         'response': 1},
    'looting': \
        {'statement': 'I believe looting poses a serious risk to my possessions.',
         'agent': True,
         'response': 1},
    'storm_track': \
        {'statement': 'I believe the storm is heading for Back Bay.',
         'agent': False,
         'response': 1},
    'evacuation_order': \
        {'statement': 'I believe the Government has issued an evacuation order.',
         'agent': False,
         'response': 1},

    }
response2belief = [0., .1, .25, .5, .75, .9, 1.]

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

objectives = {
    'safety': \
        {'objective': 'Personal and Family  survival',
         'actions': {'evacuate': False, 'stay': True, None: True},
         'beliefs': {'storm_track': True,'wind_personal': True, 'flooding_personal': True, 'evacuation_order':True},
         'rank': 1},
    'property': \
        {'objective': 'Personal property safety (post storm looting)',
         'actions': {'evacuate': False, 'stay': True, None: True},
         'beliefs': {'storm_track': True,'wind_house': True, 'flooding_house': True},
         'rank': 3},
#    'family': \
#        {'objective': 'Family or friend anthrax survival',
#         'actions': {None: True},
#         'rank': 4},
    }
                    
def incrementLeaves(tree,value):
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
    # python cesar /cesar/.../hurricane2
    world = World()
    world.diagram = diagram.Diagram()
    world.diagram.setColor(None,'ivory')

    resident = Agent('resident')
    world.diagram.setColor(resident.name,'palegreen')
    world.addAgent(resident)
#    family = Agent('family')
#    world.diagram.setColor(family.name,'mediumseagreen')
#    world.addAgent(family)
    gov = Agent('government')
    world.diagram.setColor(gov.name,'cornflowerblue')
    world.addAgent(gov)

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
    
    
    # joints = [name for name in behaviors.keys() if behaviors[name]['phase'] == 'where' and \
    #                  behaviors[name]['location'] == 'home']
    # for joint in powerset(joints):
    #     action = ActionSet([behaviors[name]['action'] for name in joint])
    #     label = ' '.join(joint)
    #     options[label] = resident.addAction(action)
    #     # Only legal during "how" phase and if living in home
    #     resident.setLegal(options[label],makeTree({'if': equalRow('phase','where'),
    #                                                True: {'if': equalRow(location,'home'),
    #                                                       True: True, False: False},
    #                                                False: False}))

    # Lifestyle choices 
    for joint in [name for name in behaviors.keys() if behaviors[name]['location'] == 'beyond']:
        options[joint] = resident.addAction(behaviors[joint]['action'])
        # Only legal during "how" phase and if *not* living in home
        resident.setLegal(options[joint],makeTree({'if': equalRow('phase','where'),
                                                   True: {'if': equalRow(location,'beyond'),
                                                          True: True, False: False},
                                                   False: False}))

    # Choices of where to live
    for joint in [name for name in behaviors.keys() if behaviors[name]['phase'] == 'where']:
        options[joint] = resident.addAction(behaviors[joint]['action'])
        # Only legal during "where" phase
        resident.setLegal(options[joint],makeTree({'if': equalRow('phase','where'),
                                                   True: {'if': equalRow(location,behaviors[name]['location']),
                                                          True: True, False: False},
                                                   False: False}))

    # Objectives
    ranks = [objective['rank'] for objective in objectives.values()]
    ceiling = max(ranks) + 1
    total = float(sum(ranks))
    for name,objective in objectives.items():
        objective['key'] = world.defineState(resident.name,name,bool)
        world.setFeature(objective['key'],True)
        resident.setReward(maximizeFeature(objective['key']),float(ceiling-objective['rank'])/total)

    # Beliefs
    for name,belief in beliefs.items():
        if belief['agent']:
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
        # Consider possible "how" behaviors
        for option in [o for o in resident.actions if o != options['evacuate']]:
            # How many actions contribute to this objective?
            count = {True: 0, False: 0, None: 0}
            total = len(objective['actions'])
            if len(option) == 0:
                count[None] += 1
            else:
                for action in option:
                    try:
                        count[objective['actions'][action['verb']]] += 1
                    except KeyError:
                        count[None] += 1
            if count[None] > 0:
                count[objective['actions'][None]] += 1
            # How many beliefs contribute to this objective?
            try:
                causes = objective['beliefs']
            except KeyError:
                causes = {}
            tree = count
            for feature,value in causes.items():
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
