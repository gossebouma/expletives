#!/usr/bin/env python3

import sys, fileinput, argparse

from collections import defaultdict

ap = argparse.ArgumentParser(description="Count expletive usage (lemma and syntactic context) in a conllu file.") 

ap.add_argument("-v",help="Print sentences with expl, the matching pattern, and the annotation.",action="store_true")
ap.add_argument("-p",help="Include parent lemma in pattern",action="store_true")
ap.add_argument("-o",help="Count obj instead of expl",action="store_true")
ap.add_argument('files', metavar='FILE', nargs='*', help='conllu files to read, if empty, stdin is used')

args = ap.parse_args()

if (args.o) :
	expl_or_obj = "obj"
else : 
	expl_or_obj = "expl"

#print(expl)

contexts = defaultdict(int)

graph={}

for line in fileinput.input(args.files if len(args.files) > 0 else ('-', )) :
	try : 
		fields = line.strip().split()
		if (fields[1] == "sent_id") :
			for i in sorted(graph) :
				lemma=graph[i][0]
				parent = graph[i][1]
				rel = graph[i][2]
				if (rel == expl_or_obj ) :
					context = {'deps':[],'parent':""}
					match = 0
					for j in graph :
						jparent = graph[j][1]
						jlemma  = graph[j][0]
						jrel = graph[j][2]
						if ( jparent == parent and jrel in ("csubj","aux:pass","ccomp","nsubj","cop")) :
							context['deps'].append(jrel)
						if ( j == parent and args.p) :
							context['parent'] = jlemma 
					if (len(context['deps']) == 0) :
						context['deps'] = ['otherpattern']
					contextdeps = ' '.join(sorted(context['deps']))
					contextpattern = lemma+' '+contextdeps+' '+context['parent']
					contexts[contextpattern] += 1
					if (args.v) :
						print(text)
						print(sent_id)
						print(contextpattern)
						for k in sorted(graph.keys()) :
							print("{}\t{}\t{}\t{}".format(k,graph[k][0],graph[k][2],graph[k][1]))
						print()
			graph = {}
			sent_id = line.strip()
		elif (fields[1] == "text") :
			text = line.strip()
		else :
			index = int(fields[0])
			lemma = fields[2]
			head = int(fields[6])
			deprel = fields[7]
			graph[index] = [lemma,head,deprel]
			# if (arg.v) :
			#	print(line.strip())
	except (ValueError, IndexError, NameError) :
		True

for context in sorted(contexts, key=contexts.get, reverse=True):
	print("{:4d}\t{}".format(contexts[context],context))
