import itertools as it
from collections import OrderedDict
from dec_params import *

zeros = ['']
ones = [str(j) for j in range(2)]
twos = [''.join(p) for p in it.product(ones, ones)]
threes = [''.join(p) for p in it.product(ones, twos)]
bins = [zeros, ones, twos, threes]

def to_int(strang):
	temp = strang[::-1]
	return sum([int(val)*2**j for j, val in enumerate(temp)])

As = [[], [], [], []]
for j, A in enumerate(As):
	if j == 0:
		A.append('A')
	else:
		for bin in bins[j]:
			A.append('A_'+bin)

replace1 = ''
books = [{}, {}, {}, {}]
for j in range(len(books)):
	book = books[j]
	for a, b in zip(As[j], bins[j]):
		if j != 0:
			replace1 += a+' [label="'+'_'*(3-j)+b+'", pos="'+str(hz*j)+','+str(vr*to_int(b))+"!"+'", fontsize='+fts+'];'
		else:
			replace1 += a+' [label="'+'_'*(3-j)+b+'", pos="'+str(hz*j)+',0!"];'
		replace1 += '\n'
		book[b] = a

cols = OrderedDict(zip(['0', '1'], ['turquoise', 'red']))

for j in range(len(books)-1):
	first = books[j]
	last = books[j+1]
	for b in bins[j]:
		for let in [str(k) for k in range(2)]:
			if j != 0:
				temp = first[b].replace('_', '_'+let)
			else:
				temp = first[b]+'_'+let
			replace1 += first[b]+' -> '+temp+' [color="'+cols[let]+'", '+edj+'];'
			replace1 += '\n'

replace1 += make_legend(cols)

replace2 = 'Decision Tree'

with open('dec3.txt', 'r') as base_file:
	with open("dec3.dot", 'w') as new_file:
		new_file.write(base_file.read().replace('//replace', replace1).replace('NAME', replace2))
