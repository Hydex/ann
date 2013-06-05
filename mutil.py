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
