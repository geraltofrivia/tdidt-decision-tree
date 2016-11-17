import csv
import math

max_depth = 3
data = csv.reader(open('data/gene_expression_training.csv'))
columns = None
X = []
Y = []

def entropy(_list):
	'''
		Compute the H(X) value for a given list
	'''	
	normalized_list = [x/float(sum(_list)) for x in _list]
	val = 0.0
	print normalized_list
	for x in normalized_list:
		if x == 0:
			continue
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
	f_attribute = [ 0 for x in range(len(C))]
	for i in range(len(C)):
		f[i] += sum([x[i] for x in M])
	h_s = entropy(f)

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
	data = sorted([ (_attribute[i],_class[i]) for i in len(_attribute) ], key = lambda tup: tup[0])

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
			a = [0 for i in range(len(A[:i]))] + [1 for i in range(len(A[i:]))]
			split_candidates.append((i, information_gain(a,C)))
		previous_class = C[i]

	#Find the split with the maximum information gain
	best_tuple = max(split_candidates,key=lambda item:item[1])[0]

	#Return the value i (left: less than i, right: more than or equal to i) and the , corresponding value of information gain
	return (A[best_tuple[0]], best_tuple[1])

def tfidt(_data, _class, _depth):

	#Exit condition
	if _depth >= max_depth:
		#Do something
		pass

	best_attr_candidates = []
	for i in range(len(_data[0])):
		best_attr_candidates.append(split([x[i] for x in _data],_class).append(i))

	#Best attribute, based on the maximum information gain
	best_attr = max(best_attr_candidates,key=lambda item:item[1])[0]
	#Format: threshold, information gain, attribute number

	#Divide the data based on this attribute
	data1 = []
	data2 = []
	class1 = []
	class2 = []

	for row in _data:
		if row[best_attr[2]] < best_attr[0]:
			






	






	








if __name__ == '__main__':
	for row in data:
		
		if not columns:
			columns = row[:-1]
			continue

		x, y = row[:-1], row[-1]
		X.append(x)
		Y.append(y)
	
	information_gain(['O','O','R','S','S','R','O','O'],['Y','Y','Y','Y','N','N','Y','N'])
