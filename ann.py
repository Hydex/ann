#!/usr/bin/python2.7

from math import exp
from time import sleep
from os import system
from pprint import pprint
from random import uniform as rand_uniform
from random import randint as rand_integer
import utilities
from training_data import *


class Neuron:
    
    def __init__(self, neuron_id, Ann, is_input=False, value=1):
        self.id = neuron_id
        self.Ann = Ann
        self.is_input = is_input
        self.output_value = value

    def activation(self, u):
        return 1 / (1 + exp(-u))

    def activationDerivative(self, u):
        return self.activation(u) * (1 - self.activation(u))

    def output(self):
        if self.is_input:
            return self.output_value
        sigma = 0
        synapses = self.Ann.synapsesAt(self)
        for synapse_id in synapses:
            sigma += self.Ann.valueAt(synapse_id) * synapses[synapse_id]
        return self.activation(sigma)
    
    def setValue(self, value):
        self.output_value = value


class ANN:

    def __init__(self):
        self.neurons = dict()
        self.rows = dict()
        self.synapses = dict()

    def setSynapse(self, axon, dendrite, weight):
        util.makeDictIfNot(self.synapses, dendrite.id)
        self.synapses[dendrite.id][axon.id] = weight

    def getAllSynapses(self, axon):
        if self.synapses.has_key(axon.id):
            return self.synapses[axon.id]
        return {}

ann = ANN()


x = Neuron(0, ann)
y = Neuron(1, ann)


ann.setSynapse(x, y, 33)
ann.setSynapse(y, x, 28)


pprint (ann.synapses)






