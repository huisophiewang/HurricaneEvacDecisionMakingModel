import json
import sys

# add to PYTHONPATH
sys.path.append("../")

from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork
from libpgm.lgbayesiannetwork import LGBayesianNetwork
from libpgm.hybayesiannetwork import HyBayesianNetwork
from libpgm.dyndiscbayesiannetwork import DynDiscBayesianNetwork
from libpgm.tablecpdfactorization import TableCPDFactorization
from libpgm.sampleaggregator import SampleAggregator
from libpgm.pgmlearner import PGMLearner



data = [
  {
    "Grade": "B", 
    "Difficulty": "easy", 
    "SAT": "lowscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "B", 
    "Difficulty": "easy", 
    "SAT": "lowscore", 
    "Letter": "strong", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "B", 
    "Difficulty": "easy", 
    "SAT": "lowscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "C", 
    "Difficulty": "hard", 
    "SAT": "lowscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "B", 
    "Difficulty": "easy", 
    "SAT": "lowscore", 
    "Letter": "strong", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "C", 
    "Difficulty": "hard", 
    "SAT": "highscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "B", 
    "Difficulty": "hard", 
    "SAT": "lowscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "A", 
    "Difficulty": "easy", 
    "SAT": "lowscore", 
    "Letter": "strong", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "C", 
    "Difficulty": "easy", 
    "SAT": "lowscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "C", 
    "Difficulty": "hard", 
    "SAT": "lowscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "C", 
    "Difficulty": "hard", 
    "SAT": "lowscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "C", 
    "Difficulty": "hard", 
    "SAT": "highscore", 
    "Letter": "weak", 
    "Intelligence": "high"
  }, 
  {
    "Grade": "C", 
    "Difficulty": "hard", 
    "SAT": "lowscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "C", 
    "Difficulty": "hard", 
    "SAT": "highscore", 
    "Letter": "weak", 
    "Intelligence": "high"
  }, 
  {
    "Grade": "A", 
    "Difficulty": "easy", 
    "SAT": "highscore", 
    "Letter": "weak", 
    "Intelligence": "high"
  }, 
  {
    "Grade": "B", 
    "Difficulty": "hard", 
    "SAT": "lowscore", 
    "Letter": "strong", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "A", 
    "Difficulty": "easy", 
    "SAT": "highscore", 
    "Letter": "weak", 
    "Intelligence": "high"
  }, 
  {
    "Grade": "B", 
    "Difficulty": "easy", 
    "SAT": "lowscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }, 
  {
    "Grade": "B", 
    "Difficulty": "hard", 
    "SAT": "highscore", 
    "Letter": "strong", 
    "Intelligence": "high"
  }, 
  {
    "Grade": "C", 
    "Difficulty": "easy", 
    "SAT": "lowscore", 
    "Letter": "weak", 
    "Intelligence": "low"
  }
]


# skel = GraphSkeleton()
# skel.load("../tests/unittestdict.txt")
# print skel
#  
# # instantiate my learner 
# learner = PGMLearner()
#  
# # estimate parameters
# result = learner.discrete_mle_estimateparams(skel, data)
#  
# # output - toggle comment to see
# print json.dumps(result.Vdata, indent=2)



# (5) --------------------------------------------------------------------------
# Compute the probability distribution over a specific node or nodes

# load nodedata and graphskeleton
nd = NodeData()
skel = GraphSkeleton()
nd.load("../tests/unittestdict.txt")
skel.load("../tests/unittestdict.txt")

# toporder graph skeleton
print skel.toporder()

# load evidence
evidence = {"Intelligence":"high"}
query = {"Grade":"A"}

# load bayesian network
bn = DiscreteBayesianNetwork(skel, nd)


# load factorization
fn = TableCPDFactorization(bn)


# # calculate probability distribution
# result = fn.condprobve(query, evidence)
# print json.dumps(result.vals, indent=2)
# print json.dumps(result.scope, indent=2)
# print json.dumps(result.card, indent=2)
# print json.dumps(result.stride, indent=2)

result = fn.specificquery(query, evidence)
print result

