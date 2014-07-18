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


def makeListIfNot(thing, index):
    if type(thing) != list:
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

def xor(a, b):
    return int(a != b)



def matrixToString(matrix, header=None):
    """
    
    Not mine, I found it here:

    http://mybravenewworld.wordpress.com/2010/09/19/print-tabular-data-nicely-using-python/
    
    """
    if type(header) is list:
        header = tuple(header)
    lengths = []
    if header:
        for column in header:
            lengths.append(len(column))
    for row in matrix:
        for column in row:
            i = row.index(column)
            column = str(column)
            cl = len(column)
            try:
                ml = lengths[i]
                if cl > ml:
                    lengths[i] = cl
            except IndexError:
                lengths.append(cl)

    lengths = tuple(lengths)
    format_string = ""
    for length in lengths:
        format_string += "%-" + str(length) + "s "
    format_string += "\n"

    matrix_str = ""
    if header:
        matrix_str += format_string % header
    for row in matrix:
        matrix_str += format_string % tuple(row)

    return matrix_str



