#!/usr/bin/python2.7

from math import exp
from time import sleep
from os import system
from pprint import pprint as pretty
from random import uniform as rand_uniform
from random import randint as rand_integer
import mutil
from training_data import *


class Neuron:
    
    def __init__(self, neuron_id, Ann, is_input=False, value=1):
        self.id = neuron_id
        self.Ann = Ann
        self.error = 0
        self.is_input = is_input
        self.output_override = value

    def activation(self, u):
        return 1 / (1 + exp(-u))

    def activationDerivative(self, u):
        return self.activation(u) * (1 - self.activation(u))

    def output(self):
        print 'outputting for', self.id
        if self.is_input:
            return self.output_override
        sigma = 0
        synapses = self.Ann.getAllSynapsesByDendrite(self)
        for synapse_id in synapses:
            sigma += self.Ann.outputAt(synapse_id) * synapses[synapse_id]
        return self.activation(sigma)
    
    def setValue(self, value):
        self.output_value = value


class ANN:

    def __init__(self):
        self.neurons = dict()
        self.rows = dict()
        self.synapses_by_dendrite = dict()
        self.synapses_by_axon = dict()

    def setSynapse(self, axon, dendrite, weight):
        mutil.makeDictIfNot(self.synapses_by_dendrite, dendrite.id)
        mutil.makeDictIfNot(self.synapses_by_axon, axon.id)
        self.synapses_by_dendrite[dendrite.id][axon.id] = weight
        self.synapses_by_axon[axon.id][dendrite.id] = weight

    def getAllSynapsesByDendrite(self, dendrite):
        if type(dendrite) == int:
            neuron_id = dendrite
        else:
            neuron_id = dendrite.id
        if self.synapses_by_dendrite.has_key(neuron_id):
            return self.synapses_by_dendrite[neuron_id]
        return {}

    def getAllSynapsesByAxon(self, axon):
        if type(axon) == int:
            neuron_id = axon
        else:
            neuron_id = axon.id
        if self.synapses_by_axon.has_key(neuron_id):
            return self.synapses_by_axon[neuron_id]
        return {}

    def connectAllToAll(self, bottom_row, top_row): 
        for bottom_neuron in bottom_row:
            for top_neuron in top_row:
                weight = rand_uniform(-1, 1)
                self.addSynapse(bottom_neuron, top_neuron, weight)
    
    def computeErrors(self, target, output):
        at_max_neuron = True
        for neuron_id in sorted(self.neurons.keys(), reverse=True):
            if at_max_neuron:
                at_max_neuron = False
                self.neurons[neuron_id].error = target - output
                continue
            new_error = 0
            synapses = self.getAllSynapsesByAxon(neuron_id)
            for dendrite_id in synapses:
                new_error += synapses[dendrite_id] * self.getErrorAt(dendrite_id)
            self.setErrorAt(neuron_id, new_error)

    def outputAt(self, neuron):
        if type(neuron) == int:
            neuron_id = neuron
        else:
            neuron_id = neuron.id
        return self.neurons[neuron_id].output()

    def getAllErrors(self):
        output = dict()
        for n in self.neurons:
            output[n] = self.neurons[n].error
        return output

    def getErrorAt(self, neuron):
        if type(neuron) == int:
            neuron_id = neuron
        else:
            neuron_id = neuron.id
        if self.neurons.has_key(neuron_id):
            return self.neurons[neuron_id].error

    def setErrorAt(self, neuron, error):
        if type(neuron) == int:
            neuron_id = neuron
        else:
            neuron_id = neuron.id

        if self.neurons.has_key(neuron_id):
            print 'setting error at', neuron_id, 'to', error
            self.neurons[neuron_id].error = error

ann = ANN()

a = Neuron(0, ann)
b = Neuron(1, ann)
c = Neuron(2, ann)


ann.neurons = {0: a, 1: b, 2: c}

ann.setSynapse(a, c, 2)
ann.setSynapse(b, c, 2)

pretty(ann.synapses_by_dendrite)
pretty(ann.synapses_by_axon)

print c.output()


ann.computeErrors(0, 1)




















