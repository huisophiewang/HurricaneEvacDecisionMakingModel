from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
import numpy as np

import copy
from pprint import pprint


def sample(N):
	bn_generate = BayesianModel([('D', 'G'), ('I', 'G'), ('I', 'S'), ('G', 'L')])
	
	cpd_d = TabularCPD('D', 2, 
					[[0.6], 
					[0.4]])
	cpd_i = TabularCPD('I', 2, 
					[[0.7], 
					[0.3]])
	cpd_g = TabularCPD('G', 3, 
					[[0.3, 0.9, 0.05, 0.5], 
					[0.4, 0.08, 0.25, 0.3],
					[0.3, 0.02, 0.7, 0.2]], 
					['D', 'I'], [2, 2])
	cpd_s = TabularCPD('S', 2, 
					[[0.95, 0.2], 
					[0.05, 0.8]],
					['I'], [2])
	cpd_l = TabularCPD('L',2, 
					[[0.1, 0.4, 0.99], 
					[0.9, 0.6, 0.01]],
					['G'], [3])
	
	bn_generate.add_cpds(cpd_d, cpd_i, cpd_g, cpd_s, cpd_l)

	infer = BayesianModelSampling(bn_generate)
	data = infer.forward_sample(N)
	#print data
	return data


		
def rand_miss(df, node, miss_size):
	if miss_size == 0:
		return df
	idx = sorted(np.random.choice(len(df), size=miss_size, replace=False))
	df[node][idx] = np.NaN
	return df
	

def init(df, node):
	# get miss_idx and miss_size
	miss_idx = df[df[node].isnull()].index.tolist()
	miss_size = len(miss_idx)
	# random guess missing values
	if miss_size == 0:
		df_complete = df
	else:
		init_vals = np.random.choice(3, size=miss_size)
		df_complete = copy.deepcopy(df)
		df_complete[node][miss_idx] = init_vals
	# assume complete data, estimate parameters using MLE 
	bn_model = BayesianModel([('D', 'G'), ('I', 'G'), ('I', 'S'), ('G', 'L')])
	bn_model.fit(df_complete, estimator=MaximumLikelihoodEstimator)
# 	cpds = bn_model.get_cpds()
# 	for cpd in bn_model.get_cpds():
# 		print("CPD of {variable}:".format(variable=cpd.variable))
# 		print(cpd)
	return bn_model 

def e_step(df, bn_model, node):
	miss_idx = df[df[node].isnull()].index.tolist()
	
	infer = VariableElimination(bn_model)
	node_cpd = bn_model.get_cpds(node=node)
	node_cardinality = node_cpd.cardinality[0]
	parents = node_cpd.variables[1:]
	parents_cardinality = node_cpd.cardinality[1:]
	parents_total_cardinality = np.prod(np.array(parents_cardinality))  

# 	print node_cpd.variables
# 	print node_cpd.values
# 	print node_cpd.get_evidence()
# 	print node_cpd
#	print node_cpd.cardinality

	suffi_stats = {}
	
	node_suffi_stats = np.zeros((parents_total_cardinality, node_cardinality))
	print node_suffi_stats
	
	for i, d in df.iterrows():
		
		evidence = {}
		node_suffi_stats_idx = 0
		for j, p in enumerate(parents):
			val = int(d[p])
			if j==len(parents)-1:
				node_suffi_stats_idx += val
			else:
				node_suffi_stats_idx += val*np.prod(np.array(parents_cardinality[(j+1):]))
			evidence[p] = val
		
		#print suffi_stats_idx
		if i in miss_idx:
			query_result = infer.query(variables=[node], evidence=evidence)
			prob = query_result[node].values
			#print prob
			node_suffi_stats[node_suffi_stats_idx] += prob
		else:
			#print i
			node_val = int(d[node])
			node_suffi_stats[node_suffi_stats_idx][node_val] += 1.0
			
	suffi_stats[node] =node_suffi_stats
	
	# find each child of the node, and compute their sufficient stats
	
	
	return suffi_stats

def m_step(suffi_stats, bn_model, node):
	node_suffi_stats = suffi_stats[node]
	print node_suffi_stats
	row_sum = np.sum(node_suffi_stats, axis=1)
	#print node_suffi_stats/row_total
	for i, r in enumerate(node_suffi_stats):
		r/=row_sum[i]
	
	node_cpd = bn_model.get_cpds(node=node)
	print node_cpd
	node_card = node_cpd.cardinality[0]
	parents = node_cpd.variables[1:]
	parents_card = node_cpd.cardinality[1:]

	node_cpd_new = TabularCPD(node, node_card, node_suffi_stats.T, parents, parents_card)

	bn_model.add_cpds(node_cpd_new)
	print bn_model.get_cpds(node=node)


if __name__ == '__main__':
	np.random.seed(1)
	# generate sample data from a given BN
	N = 500
	df = sample(N)

	# remove values of a node, generate missing values
	node = 'G'
	miss_size = 100
	df = rand_miss(df, node, miss_size)
 	
	# EM algorithm
	bn_model = init(df, node)
	#print df
	suffi_stats = e_step(df, bn_model, node)
	#pprint(suffi_stats)
	m_step(suffi_stats, bn_model, node)




	
	
	
	
	
	