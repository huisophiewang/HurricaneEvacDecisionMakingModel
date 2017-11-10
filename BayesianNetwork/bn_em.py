from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.sampling import BayesianModelSampling
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
import numpy as np
import pandas as pd
import copy
import itertools
from pprint import pprint


def sample(N):
	bn_generate = BayesianModel([('D', 'G'), ('I', 'G'), ('E', 'L'), ('G', 'L')])
	
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
	cpd_e = TabularCPD('E', 2, 
					[[0.5], 
					[0.5]])
	cpd_l = TabularCPD('L',2, 
					[[0.1, 0.3, 0.4, 0.25, 0.8, 0.99],
					[0.9, 0.7, 0.6, 0.75, 0.2, 0.01]],
					['G', 'E'], [3, 2])
	
	bn_generate.add_cpds(cpd_d, cpd_i, cpd_g, cpd_e, cpd_l)

	infer = BayesianModelSampling(bn_generate)
	data = infer.forward_sample(N)
	return data


def rand_miss(df, node, miss_size):
	if miss_size == 0:
		return df
	idx = sorted(np.random.choice(len(df), size=miss_size, replace=False))
	df[node][idx] = np.nan
	return df
	

def init(df, miss_node):
	# get miss_idx and miss_size
	miss_idx = df[df[miss_node].isnull()].index.tolist()
	miss_size = len(miss_idx)
	# random guess missing values
	if miss_size == 0:
		df_complete = df
	else:
		init_vals = np.random.choice(3, size=miss_size)
		df_complete = copy.deepcopy(df)
		df_complete[miss_node][miss_idx] = init_vals
	# assume complete data, estimate parameters using MLE 
	bn_model = BayesianModel([('D', 'G'), ('I', 'G'), ('E', 'L'), ('G', 'L')])
	bn_model.fit(df_complete, estimator=MaximumLikelihoodEstimator)
# 	cpds = bn_model.get_cpds()
# 	for cpd in bn_model.get_cpds():
# 		print("CPD of {variable}:".format(variable=cpd.variable))
# 		print(cpd)
	return bn_model 

def get_parent_values_idx(parents_card, parents_val):
	idx = 0
	for j in range(len(parents_val)):
		val = parents_val[j]
		if j==len(parents_val)-1:
			idx += val
		else:
			idx += val*np.prod(np.array(parents_card[(j+1):]))
	return idx

def EM(df, bn_model, miss_node):
	###########################################################################
	# E_step
	# only need to infer the prob of the missing node, because other nodes we already observed
	# that affects sufficient stats in two occasions: when miss_node is child, when miss_node is parent
	miss_idx = df[df[miss_node].isnull()].index.tolist()
	infer = VariableElimination(bn_model)
	
	# get all affected nodes (the miss node and its children)
	affected_nodes = [miss_node]
	for successor in bn_model.successors(miss_node):
		if not successor in affected_nodes:
			affected_nodes.append(successor)
			
	
	for node in affected_nodes:
		if node == miss_node:
			continue
		
		node_cpd = bn_model.get_cpds(node=node)
		node_card = node_cpd.cardinality[0]
		parents = node_cpd.variables[1:]
		parents_card = node_cpd.cardinality[1:]
		parents_total_card = np.prod(np.array(parents_card))  
		
				
   
		# use 2d array because later we need to marginalize over the child node 
		node_suffi_stats = np.zeros((parents_total_card, node_card))
  		
 		print node_suffi_stats
		for i, d in df.iterrows():
# 	 		if i > 10:
# 	 			continue
# 	 		print '-----------------------------'
# 	 		print d
 			
			# when instance d has no missing value
			if not i in miss_idx: 
				parents_value = []
				for p in parents:
					val = int(d[p])
					parents_value.append(val)
				node_suffi_stats_idx = get_parent_values_idx(parents_card, parents_value)
				node_val = int(d[node])
				node_suffi_stats[node_suffi_stats_idx][node_val] += 1.0	
				print node_suffi_stats
			else:
				evidence = {}
				for n in bn_model.nodes():
					# including all the variables in the graph except the miss node and its parents
					if not n in [miss_node]:
						evidence[n] = int(d[n])
				query_result = infer.query(variables=[miss_node], evidence=evidence)
				miss_node_factor = query_result[miss_node]
				miss_node_prob = miss_node_factor.values
				print miss_node_prob
				# when miss_node is the child node, we also know the values of its parents, there is one place to update
				if node == miss_node:
					node_suffi_stats[node_suffi_stats_idx] += miss_node_prob
				# when miss_node is the parent node, the values of the parent are probablistic, there are multiple places to update
				else:
					parents_value_list = []
					for j, p in enumerate(parents):
						if p != miss_node:
							val = int(d[p])
							parents_value_list.append([val])
						else:
							parent_card = parents_card[j]
							parents_value_list.append(range(parent_card))

					node_suffi_stats_indices = []
					for parents_value in itertools.product(*parents_value_list):
						node_suffi_stats_idx = get_parent_values_idx(parents_card, list(parents_value))
						node_suffi_stats_indices.append(node_suffi_stats_idx)
					node_val = int(d[node])
					for k, node_suffi_stats_idx in enumerate(node_suffi_stats_indices):
						node_suffi_stats[node_suffi_stats_idx][node_val] += miss_node_prob[k]
						
				print node_suffi_stats
						
						
		print node_suffi_stats
	 	print np.sum(node_suffi_stats, axis=1)
	 	print np.sum(node_suffi_stats)
	
	###########################################################################
	# M_step
	# update the cpd of the miss node and its children
# 	row_sum = np.sum(node_suffi_stats, axis=1)
# 	for i, r in enumerate(node_suffi_stats):
# 		r/=row_sum[i]
# 	
# 	node_cpd = bn_model.get_cpds(node=miss_node)
# 	node_card = node_cpd.cardinality[0]
# 	parents = node_cpd.variables[1:]
# 	parents_card = node_cpd.cardinality[1:]
# 
# 	node_cpd_new = TabularCPD(miss_node, node_card, node_suffi_stats.T, parents, parents_card)
# 	bn_model.add_cpds(node_cpd_new)
# 	print bn_model.get_cpds(node=miss_node)
# 	
# 	for child in bn_model.successors(miss_node):
# 		child_cpd = bn_model.get_cpds(node=child)
# 		child_card = child_cpd.cardinality[0]
# 		child_parents = child_cpd.variables[1:]
# 		child_parents_card = child_cpd.cardinality[1:]
# 		
# 	bn_model.successors(miss_node).keys()
# 	
# 	return bn_model


if __name__ == '__main__':
	np.random.seed(1)
	# generate sample data from a given BN
	N = 500
	df = sample(N)

	# remove values of a node, generate missing values
	miss_node = 'G'
	miss_size = 100

	df = rand_miss(df, miss_node, miss_size)
	print df.groupby(['D', 'I']).size()
 	
	# EM algorithm
	bn_model = init(df, miss_node)
	
	EM(df, bn_model, miss_node)
	
# 	for iter in range(2):
# 		print '====================================================='
# 		print iter
# 		suffi_stats = e_step(df, bn_model, node)
# 		#pprint(suffi_stats)
# 		bn_model = m_step(suffi_stats, bn_model, node)


	#e_step(df, bn_model, miss_node)
	
	#pd.to_numeric(df['G'], errors='coerce',downcast='integer')
	#print df['G']
# 	for i, d in df.iterrows():
# 		print d
	


	




	
	
	
	
	
	