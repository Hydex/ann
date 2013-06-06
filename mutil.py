"""

mutil.py

Stands for Miles' Utilities

"""

def makeDictIfNot(thing, index):
	if type(thing) != dict:
		thing = dict()

	if not thing.has_key(index):
		thing[index] = dict()

	if type(thing[index]) != dict:
		thing[index] = dict()

def describeRows(r):
    print
    for i in range(len(r)-1, -1, -1):
        fucknugget = 'row ' + str(i)
        if i == 0:
            fucknugget = 'input'
        print fucknugget, 'members:',
        for huh in r[i]:
            print huh.id,
        print

def extractNeuronId(neuron):
    if type(neuron) == int:
        return neuron
    return neuron.id