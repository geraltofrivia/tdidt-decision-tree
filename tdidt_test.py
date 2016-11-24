import csv
import pickle

tree = pickle.load(open('output/trained_tree.pickle'))
data = csv.reader(open('data/gene_expression_test.csv'))
columns = None
X = []
Y = []
for row in data:

	if not columns:
		columns = row[:-1]
		continue

	x, y = row[:-1], row[-1]
	X.append([float(a) for a in x])
	Y.append(float(y))

classified_Y = []
for row in X:
	t = tree
	while True:
		# print t['depth'], t['name']
		# raw_input()
		
		if t['name'] == 'LEAF':
			classified_Y.append(t['label'])
			break

		if float(row[t['attribute_id']]) < t['threshold']:
			#LEFT
			t = t['children'][0]
			continue

		else:
			t = t['children'][1]
			continue

#Now compare classified_Y with Y
precision = 0
for i in range(len(Y)):
	if Y[i] == classified_Y[i]:
		precision += 1

precision = float(precision)/len(Y)*100

print "Precision = %s percent" % str(precision)