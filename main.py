#!/usr/bin/python2.7

from math import exp
from time import sleep
from os import system
from random import uniform as rand_uniform
from random import randint as rand_integer
from training_data import training_data

sigmoid = lambda u: 1 / (1 + exp(-u))

class Neuron:
    
    def __init__(self, neuron_id, Ann, is_input=False, value=1):
        self.id = neuron_id
        self.bias = rand_uniform(-1, 1)
        self.Ann = Ann
        self.is_input = is_input
        self.output_value = value
        
    def activation(self, sigma):
        #return int(bool(sigma))
        return sigmoid(sigma)
    
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
        self.synapses = dict()
        
    def connectAllToAll(self, bottom_row, top_row, default_weight=1):
        for bottom_neuron in bottom_row:
            for top_neuron in top_row:
                self.newSynapse(bottom_neuron, top_neuron, default_weight)
                
    def weightAtSynapse(self, source_neuron, dest_neuron):
        return self.synapses[source_neuron.id][dest_neuron.id]
    
    def synapsesAt(self, neuron):
        synapses = {-1: neuron.bias}
        if not self.synapses.has_key(neuron.id):
            return synapses
        for synapse_id in self.synapses[neuron.id]:
            synapses[synapse_id] = self.synapses[neuron.id][synapse_id]
        return synapses
    
    def valueAt(self, neuron_id):
        # negative neuron_id means its going to be multiplied by a neuron bias
        if neuron_id < 0:
            return 1
        return self.neurons[neuron_id].output()
    
    def addNeuron(self, number_of=1):
        for i in range(number_of):
            neuron_id = len(self.neurons)
            neuron = Neuron(neuron_id, self)
            self.neurons.append(neuron)
            
    def newSynapse(self, dest_neuron, source_neuron, weight):
        print 'creating new synapse from', dest_neuron.id, 'to', source_neuron.id
        if not self.synapses.has_key(source_neuron.id):
            self.synapses[source_neuron.id] = dict()
        self.synapses[source_neuron.id][dest_neuron.id] = weight

ann = ANN()
ann.addNeuron(5)
n = ann.neurons
r = dict()


r[0] = n[0:2]
r[1] = n[2:4]
r[2] = n[4:6]


for btm_neuron in r[0]:
    btm_neuron.is_input = True
    btm_neuron.output_value = 1


ann.connectAllToAll (r[0], r[1])
ann.connectAllToAll (r[1], r[2])


print
print 'rows:'
for i in range(len(r)-1, -1, -1):
    print 'size:', len(r[i]), 'members:',
    for huh in r[i]:
        print huh.id,
    print




