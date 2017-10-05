import sys
from pprint import pprint
from pomegranate import *


def test_pome():
    guest = distributions.DiscreteDistribution({'A': 1./3, 'B': 1./3, 'C': 1./3})
    prize = distributions.DiscreteDistribution({'A': 1./3, 'B': 1./3, 'C': 1./3})
    monty = distributions.ConditionalProbabilityTable(
            [['A', 'A', 'A', 0.0],
             ['A', 'A', 'B', 0.5],
             ['A', 'A', 'C', 0.5],
             ['A', 'B', 'A', 0.0],
             ['A', 'B', 'B', 0.0],
             ['A', 'B', 'C', 1.0],
             ['A', 'C', 'A', 0.0],
             ['A', 'C', 'B', 1.0],
             ['A', 'C', 'C', 0.0],
             ['B', 'A', 'A', 0.0],
             ['B', 'A', 'B', 0.0],
             ['B', 'A', 'C', 1.0],
             ['B', 'B', 'A', 0.5],
             ['B', 'B', 'B', 0.0],
             ['B', 'B', 'C', 0.5],
             ['B', 'C', 'A', 1.0],
             ['B', 'C', 'B', 0.0],
             ['B', 'C', 'C', 0.0],
             ['C', 'A', 'A', 0.0],
             ['C', 'A', 'B', 1.0],
             ['C', 'A', 'C', 0.0],
             ['C', 'B', 'A', 1.0],
             ['C', 'B', 'B', 0.0],
             ['C', 'B', 'C', 0.0],
             ['C', 'C', 'A', 0.5],
             ['C', 'C', 'B', 0.5],
             ['C', 'C', 'C', 0.0]], [guest, prize])
    
    s1 = base.Node(guest, name="guest")
    s2 = base.Node(prize, name="prize")
    s3 = base.Node(monty, name="monty")
    model = BayesianNetwork("Monty Hall Problem")
    model.add_states(s1, s2, s3)
    model.add_edge(s1, s3)
    model.add_edge(s2, s3)
    model.bake()
    
    data = [[ 'A', 'A', 'A' ],
        [ 'A', 'A', 'A' ],
        [ 'A', 'A', 'A' ],
        [ 'A', 'A', 'A' ],
        [ 'A', 'A', 'A' ],
        [ 'B', 'B', 'B' ],
        [ 'B', 'B', 'C' ],
        [ 'C', 'C', 'A' ],
        [ 'C', 'C', 'C' ],
        [ 'C', 'C', 'C' ],
        [ 'C', 'C', 'C' ],
        [ 'C', 'B', 'A' ]]

    model.fit(data)
    
if __name__ == '__main__':
    
    test_pome()