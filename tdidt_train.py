from pprint import pprint
import graphviz as gv
import random
import pickle
import math
import csv

max_depth = 3
data = csv.reader(open('data/gene_expression_training.csv'))
columns = None
X = []
Y = []

#IMPORTANT PART
tree = {}

def entropy(_list):
	'''
		Compute the H(X) value for a given list
	'''	
	normalized_list = [x/float(sum(_list)) for x in _list]
	val = 0.0
	# print normalized_list
	for x in normalized_list:
		if x != 0:	
			val += x*math.log(1/x,2)
	return val


def information_gain(_attribute, _class):
	'''
		class responsible for returning back the information gain for the given column.
		Input: discrete attributes; 
		Output: real number
	'''

	#Make a frequency matrix of Y axis: attribute; X axis: class
	A = list(set(_attribute))
	C = list(set(_class))

	#Initialize an empty matrix
	M = [ [ 0 for x in range(len(C))] for y in range(len(A)) ]

	#Fill this matrix up
	for i in range(len(_attribute)):
		a = A.index(_attribute[i])
		c = C.index(_class[i])
		M[a][c] += 1

	#Compute H(S)
	h_s = 0.0
	freq_attribute = [ 0 for x in range(len(C))]
	for i in range(len(C)):
		freq_attribute[i] += sum([x[i] for x in M])
	h_s = entropy(freq_attribute)

	#Compute H(S/A)
	h_s_a = 0.0
	for i in range(len(A)):
		h_s_a += sum(M[i])/float(len(_attribute))*entropy(M[i])

	#return H(S) - H(S/A)
	return h_s - h_s_a

def split(_attribute, _class):
	'''
		Convert a continous value attribute to discrete
	'''


	#Make a list of (attribute,class) tuple
	data = sorted([ (_attribute[i],_class[i]) for i in range(len(_attribute)) ], key = lambda tup: tup[0])

	#I know it's an overhead but for the sake of coder's sanity, i'm gonna use this information to basically split this list into two lists
	A = [x[0] for x in data]
	C = [x[1] for x in data]

	#So now A and C are sorted and still in sync. Neat (sorry, overhead nazis)

	split_candidates = []
	#Check for breaks
	previous_class = C[0]
	for i in range(1,len(A)):
		if not C[i] == previous_class:
			#Treat 'i' as a split candidate.
			a = [0 for x in A[:i]] + [1 for x in A[i:]]
			split_candidates.append((i, information_gain(a,C)))
		previous_class = C[i]

	#Find the split with the maximum information gain
	best_tuple = max(split_candidates,key=lambda item:item[1])

	#Computing the avg of list[i-1] and list[i] items.
	if best_tuple[0]>0:
		avg = (float(A[best_tuple[0]-1]) +float(A[best_tuple[0]]))/2
	else:
		avg = A[best_tuple[0]]

	#Return the value i (left: less than i, right: more than or equal to i) and the , corresponding value of information gain
	return [avg, best_tuple[1]]

def tdidt(_data, _class, _depth, _tree):

	# if len(list(set(_class))) <= 1:
	# 	print _data
	# 	print _class
	# 	raw_input()
	#Exit condition
	if _depth >= max_depth or len(list(set(_class))) <= 1:
		_tree['name'] = "LEAF"
		_tree['depth'] = _depth
		_tree['samples'] = len(_class)
		_tree['children'] = []
		_tree['label'] = max(set(_class), key = _class.count)
		return None

	#For every attribute, compute the information gain (using best split for that attribute)
	best_attr_candidates = []
	for i in range(len(_data[0])):
		best_attr_candidates.append(split([x[i] for x in _data],_class)+[i])

	# pprint(best_attr_candidates)
	# raw_input()

	#Best attribute, based on the maximum information gain
	best_attr = max(best_attr_candidates,key=lambda item:item[1])
	#Format: threshold, information gain, attribute number

	#TIME TO FILL IN ZE TREE!
	_tree['attribute_id'] = best_attr[2]
	_tree['name'] = columns[best_attr[2]]
	_tree['threshold'] = float(best_attr[0])
	_tree['samples'] = len(_data)
	_tree['children'] = []
	_tree['depth'] = _depth

	#Divide the data based on this attribute
	data1 = []
	data2 = []
	class1 = []
	class2 = []

	for i in range(len(_data)):
		if _data[i][best_attr[2]] < best_attr[0]:
			#left node
			data1.append(_data[i])
			class1.append(_class[i])
		else:
			#right node
			data2.append(_data[i])
			class2.append(_class[i])

	# print len(class1)
	# print len(class2)

	
	#Recursion follows:
	#LEFT
	_tree['children'].append({})
	tdidt(data1,class1,_depth+1, _tree['children'][-1])
	#RIGHT
	_tree['children'].append({})
	tdidt(data2,class2,_depth+1, _tree['children'][-1])

	return None

def visualize():
	tree_visualized = gv.Digraph(format='svg',engine='dot')
	visualizing_traversal(tree, 'ROOT', tree_visualized)
	return tree_visualized

def visualizing_traversal(node, parent_name, tree_visualized):
	if node['name'] == 'LEAF':
		tree_visualized.attr('node', shape='ellipse')
		name = parent_name+str(random.randint(1,100000))
		if node['label'] > 0.9:
			label = ''' trisome || samples = %(samples)d''' % {'samples': node['samples']}
		else:
			label = ''' healthy || samples = %(samples)d''' % {'samples': node['samples']}
		#Do something else
		tree_visualized.node(name, label)
		tree_visualized.edge(parent_name, name)
		return

	tree_visualized.attr('node', shape='box')
	#create the unique identifier
	name = node['name']+'_'+str(node['depth'])
	# pprint(node)
	# raw_input()
	label = '''%(property_name)s <= %(threshold)s || samples = %(samples)d''' % {'property_name': node['name'],'threshold':str(node['threshold']),'samples':node['samples']}
	tree_visualized.node(name = name, label = label)

	#for creating the edge
	if not parent_name == 'ROOT':
		tree_visualized.edge(parent_name, name)

	#DFS Recursion time!
	for children in node['children']:
		visualizing_traversal(children, name, tree_visualized)
	
if __name__ == '__main__':
	for row in data:
		
		if not columns:
			columns = row[:-1]
			continue

		x, y = row[:-1], row[-1]
		X.append([float(a) for a in x])
		Y.append(float(y))

	#Save the tree	
	tdidt(X,Y,0,tree)
	# pprint(tree)
	pickle.dump(tree, open('output/trained_tree.pickle','w+'))

	#Save visualization
	gv = visualize()
	f = open('output/tree.dot','w+')
	f.write(gv.source)
	f.close()