""" To parse weird data is to become weird data
"""
from collections import defaultdict
from numpy import vstack, argsort, flipud, rot90, zeros, concatenate
import json
from os import listdir, path

# test_json = open('data/json/graph.00001.obj.json').read() # '{"1,2,3":["1,2,3"], "4,6,5":["1,2,3","8,9,10"]}'

def parse_dir(dir_name):
	parsed_trees = []
	for file_name in listdir(dir_name):
		full_path = path.join(dir_name, file_name)
		if path.getsize(full_path) > 0 and full_path.endswith('.json'): # if file is not empty
			print "Parsing file: ", file_name
			parsed_trees.append(parse_file(full_path))

		# if len(parsed_trees) == 220: # testing
		# 	return parsed_trees

	print "Finised parsing %s files." % len(parsed_trees)
	return parsed_trees

def parse_file(file_name):
    json_file = open(file_name).read()
    k = json.loads(json_file)
    j = defaultdict(list)

	for l, v in k.iteritems():
	    l = tuple(map(float, l.split(', ')))
	    
	    for q in v:
	        a, b, c = map(float, q.split(', '))
	        j[l].append((a, b, c))

	verts = vstack(j.keys())
	sorted_verts = verts[argsort(verts[:, 1])]
	# verts = flipud(rot90(j.keys()))
	# sorted_verts = verts[:, argsort(verts[1, :])]

	# TODO if not 256, add padding
	pad_size = 256 - len(j.keys())
	if pad_size > 0:
		padding = zeros((pad_size, 3))
		sorted_verts = concatenate((padding, sorted_verts), axis=0)
		# padding = zeros((3, pad_size))
		# sorted_verts = concatenate((padding, verts), axis=1)

    return sorted_verts



# Testing one file
print parse_file('data/json/graph.00002.obj.json')

