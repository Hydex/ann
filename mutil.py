"""

mutil.py

Stands for Miles' Utilities...

What does it sound like it does genius? 
It's a library of functions I'd like to have

I'm listening to Radiohead, Amnesiac right now.
I'm a reasonable man, get off my case, get off my case, get off my case

"""

def makeDictIfNot(thing, index):
	if type(thing) != dict:
		thing = dict()

	if not thing.has_key(index):
		thing[index] = dict()

	if type(thing[index]) != dict:
		thing[index] = dict()