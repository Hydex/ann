#!/usr/bin/python2.7

from math import exp
from time import sleep
from os import system
from pprint import pprint
from random import uniform as rand_uniform
from random import randint as rand_integer
from training_data import *


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

class Neuron:
    
    def __init__(self, neuron_id, Ann, is_input=False, value=1):
        self.id = neuron_id
        self.bias = 0
        self.Ann = Ann
        self.is_input = is_input
        self.output_value = value

    def activation(self, u):
        "sigmoid function"
        return 1 / (1 + exp(-u))

    def activationDerivative(self, u):
        "first derivative of the sigmoid function"
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
        self.neurons = list()
        self.rows = dict()
        self.synapses = dict()
        self.errors = dict()
        self.learning_rate = 0.1
        self.binary_threshold = 0.5


    def computeErrors(self, input_vector, target_vector):
        last_row = len(self.rows) - 1

        for e in range(len(self.neurons)):
            self.errors[e] = dict()

        pprint (self.errors)

        for t in xrange(len(target_vector)):
            for i in xrange(len(self.rows[0])):
                print 'setting ann.neurons[%d] to %d' % (i, input_vector[i])
                self.neurons[i].output_value = input_vector[i]

            n = self.neurons


            for r in range(len(self.rows)-1, -1, -1):
                if r == last_row:
                    target = target_vector[t]
                    output = self.rows[last_row][0].output()
                    error = target - output
                    self.errors[7] = error
                    print 'output: %f, target: %f, error: %f' % (output, target, error)
                else:
                    for nx in self.rows[r]:
                        for ny in self.rows[r + 1]:
                            print nx.id, ny.id


    def connectAllToAll(self, bottom_row, top_row): 
        for bottom_neuron in bottom_row:
            for top_neuron in top_row:
                weight = rand_uniform(-1, 1)
                self.addSynapse(bottom_neuron, top_neuron, weight)
                
    def addSynapse(self, axon, dendrite, weight='r'):
        if not self.synapses.has_key(dendrite.id):
            self.synapses[dendrite.id] = dict()
        #if self.synapse[dendrite.id].has_key[axon.id]:
        if weight == 'r':
            weight = rand_uniform(-1, 1)
        print 'creating synapse from', axon.id, 'to', dendrite.id, 'with random weight', weight
        self.synapses[dendrite.id][axon.id] = weight

    def weightAtSynapse(self, axon, dendrite):
        return self.synapses[dendrite.id][axon.id]

    def setWeightAtSynapse(self, axon, dendrite, weight):
        self.synapses[dendrite.id][axon.id] = weight

    def addToWeightAtSynapse(self, axon, dendrite, weight):
        self.synapses[dendrite.id][axon.id] += weight

    def synapsesAt(self, dendrite):
        bias_synapse = {-1: dendrite.bias}
        return dict (self.synapses[dendrite.id].items())# + bias_synapse.items())

    def valueAt(self, neuron_id):
        if neuron_id < 0:
            return 1
        return self.neurons[neuron_id].output()

    def addNeuron(self, number_of=1):
        for i in range(number_of):
            neuron_id = len(self.neurons)
            neuron = Neuron(neuron_id, self)
            self.neurons.append(neuron)








ann = ANN()
ann.addNeuron(8)
n = ann.neurons
r = dict()
ann.rows = r

r[0] = n[0:2]
r[1] = n[2:5]
r[2] = n[5:7]
r[3] = n[7:8]


for btm_neuron in r[0]:
    btm_neuron.is_input = True


n[0].output_value = 0
n[1].output_value = 0

o = n[7].output


ann.connectAllToAll (r[0], r[1])
ann.connectAllToAll (r[1], r[2])
ann.connectAllToAll (r[2], r[3])


describeRows(r)

print
print 'network says', o()
print



ann.computeErrors([1, 0], [1])

















print '\n\n'
exit()
"""
print
print 'starting training:'
i = 0

for t_set in trainingData(1000):
    input_a = t_set[0][0]
    input_b = t_set[0][1]
    target = t_set[1]
    n[0].output_value = input_a
    n[1].output_value = input_b
    output = n[2].output()
    printLearnInfo(input_a, input_b, target, output)
    new_weight = ann.learning_rate * (target - output)
    print 'new weight:', new_weight
    ann.addToWeightAtSynapse(n[0], n[2], new_weight)
    output = n[2].output()
    new_weight = ann.learning_rate * (target - output)
    printLearnInfo(input_a, input_b, target, output)
    print 'new weight:', new_weight
    ann.addToWeightAtSynapse(n[1], n[2], new_weight)
    sleep(0.01)
print 'training set exhausted'
"""
\