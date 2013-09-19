#!/usr/bin/python
#
# 2013 Miles Smith

from math import exp
from time import sleep
from os import system
from copy import deepcopy
from pprint import pprint as pretty
from random import uniform as rand_uniform
from random import randint as rand_integer
import mutil


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
        #print 'outputting for', self.id
        if self.is_input:
            return self.output_override
        sigma = 0
        synapses = self.Ann.getAllSynapsesByDendrite(self)
        for synapse_id in synapses:
            sigma += self.Ann.outputAt(synapse_id) * synapses[synapse_id]
        return self.activation(sigma)
    
    def derivativeOutput(self):
        #print 'outputting derivative for', self.id
        if self.is_input:
            return self.output_override
        sigma = 0
        synapses = self.Ann.getAllSynapsesByDendrite(self)
        for synapse_id in synapses:
            sigma += self.Ann.outputAt(synapse_id) * synapses[synapse_id]
        return self.activationDerivative(sigma)

    def setValue(self, value):
        self.output_value = value

class ANN:

    def __init__(self):
        self.neurons = dict()
        self.synapses_by_dendrite = dict()
        self.synapses_by_axon = dict()
        self.learning_rate = 1

    def setSynapse(self, axon, dendrite, weight):
        axon_id = mutil.extractNeuronId(axon)
        dendrite_id = mutil.extractNeuronId(dendrite)

        #print 'setting synapse from', axon_id, 'to', dendrite_id, 'with weight', weight
        mutil.makeDictIfNot(self.synapses_by_dendrite, dendrite_id)
        mutil.makeDictIfNot(self.synapses_by_axon, axon_id)
        self.synapses_by_dendrite[dendrite_id][axon_id] = weight
        self.synapses_by_axon[axon_id][dendrite_id] = weight

    def getAllSynapsesByDendrite(self, dendrite):
        neuron_id = mutil.extractNeuronId(dendrite)
        if self.synapses_by_dendrite.has_key(neuron_id):
            return self.synapses_by_dendrite[neuron_id]
        #print 'no synapses found'
        return {}

    def getAllSynapsesByAxon(self, axon):
        neuron_id = mutil.extractNeuronId(axon)
        if self.synapses_by_axon.has_key(neuron_id):
            return self.synapses_by_axon[neuron_id]
        #print 'no synapses found'
        return {}

    def weightAtSynapse(self, axon, dendrite):
        axon_id = mutil.extractNeuronId(axon)
        dendrite_id = mutil.extractNeuronId(dendrite)
        return self.synapses_by_axon[axon_id][dendrite_id]

    def connectAllToAll(self, bottom_row, top_row): 
        for bottom_neuron in bottom_row:
            for top_neuron in top_row:
                weight = 1#rand_uniform(-1, 1)
                self.setSynapse(bottom_neuron, top_neuron, weight)

    def computeErrors(self, target, output):
        at_max_neuron = True
        for neuron_id in sorted(self.neurons.keys(), reverse=True):
            if at_max_neuron:
                at_max_neuron = False
                #print 'setting error at', neuron_id, 'to', target - output
                self.neurons[neuron_id].error = target - output
                continue
            new_error = 0
            synapses = self.getAllSynapsesByAxon(neuron_id)
            for dendrite_id in synapses:
                new_error += synapses[dendrite_id] * self.getErrorAt(dendrite_id)
            self.setErrorAt(neuron_id, new_error)

    def outputAt(self, neuron):
        neuron_id = mutil.extractNeuronId(neuron)
        return self.neurons[neuron_id].output()
    
    def derivativeOutputAt(self, neuron):
        neuron_id = mutil.extractNeuronId(neuron)
        return self.neurons[neuron_id].derivativeOutput()

    def getAllErrors(self):
        output = dict()
        for n in self.neurons:
            output[n] = self.neurons[n].error
        return output

    def getErrorAt(self, neuron):
        neuron_id = mutil.extractNeuronId(neuron)
        if self.neurons.has_key(neuron_id):
            return self.neurons[neuron_id].error

    def setErrorAt(self, neuron, error):
        neuron_id = mutil.extractNeuronId(neuron)
        if self.neurons.has_key(neuron_id):
            #print 'setting error at', neuron_id, 'to', error
            self.neurons[neuron_id].error = error

    def adjustWeights(self):
        new_weights = dict()
        for axon_id in sorted(self.neurons.keys(), reverse=False):
            mutil.makeDictIfNot(new_weights, axon_id)
            for dendrite_id in self.getAllSynapsesByAxon(axon_id):
                mutil.makeDictIfNot(new_weights[axon_id], dendrite_id)
                
                weight = self.weightAtSynapse(axon_id, dendrite_id)
                error = self.getErrorAt(dendrite_id)
                rate = self.learning_rate
                derivative = self.derivativeOutputAt(dendrite_id)
                output = self.outputAt(axon_id)
                new_weights[axon_id][dendrite_id] = weight + rate * error * derivative * output
                self.setSynapse(axon_id, dendrite_id, new_weights[axon_id][dendrite_id])

        #return new_weights
"""
        for axon_id in new_weights:
            for dendrite_id in new_weights[axon_id]:
                self.setSynapse(axon_id, dendrite_id, new_weights[axon_id][dendrite_id])
#                print axon_id, '->', dendrite_id
"""



ann = ANN()


for i in range(8):
    ann.neurons[i] = Neuron(i, ann)


n = ann.neurons
r = dict()


r[3] = [n[7]]
r[2] = [n[5], n[6]]
r[1] = [n[2], n[3], n[4]]
r[0] = [n[0], n[1]]

#n[8].is_input = True
#n[8].output_override = 1

for b in r[0]:
    b.is_input = True

#for b in n:
#    b = n[b]
#    if not b.is_input:
#        ann.setSynapse(n[8], b, 1)

ann.connectAllToAll(r[0], r[1])
ann.connectAllToAll(r[1], r[2])
ann.connectAllToAll(r[2], r[3])


initial_weights = deepcopy(ann.synapses_by_axon)


def set(t):
    n[0].output_override = t[0]
    n[1].output_override = t[1]
    #return n[7].output()


for i in range(2000):
    for test in [[1, 1], [0, 0], [1, 0], [0, 1]]:
        set(test)
        target = test[0]#mutil.xor(test[0], test[1])
        output = ann.outputAt(7)

        ann.computeErrors(target, output)
        #system('clear');
        ann.adjustWeights()

        if not (i+1)%50:
            system('clear')
            print 'training cycle', i+1
            print 'input:', test
            print 'target:', target
            print 'output:', output
            print
            print 'synaptic weight matrix:'
            pretty(ann.synapses_by_dendrite)
            sleep(1)
print
print 'final output results:'
for test in [[1, 1], [0, 0], [1, 0], [0, 1]]:
    set(test)
    print test, n[7].output()

"""
mutil.describeRows(r)

print
print 'synapses by dendrite:'
pretty(ann.synapses_by_dendrite)
print
print 'synapses by axon:'
pretty(ann.synapses_by_axon)
print


peepee =  n[7].output()
print 'final output:', peepee
print


ann.computeErrors(1, 0)
print
w = ann.adjustedWeights()
"""
