#!/usr/bin/python2.7

from math import exp
from time import sleep
from os import system
from random import uniform as rand_uniform
from random import randint as rand_integer
from training_data import training_data

sigmoid = lambda u: 1 / (1 + exp(-u))

def describeRows(r):
    print
    print 'rows:'
    for i in range(len(r)-1, -1, -1):
        print 'size:', len(r[i]), 'members:',
        for huh in r[i]:
            print huh.id,
        print

class Neuron:
    
    def __init__(self, neuron_id, Ann, is_input=False, value=1):
        self.id = neuron_id
        self.bias = rand_uniform(-1, 1)
        self.Ann = Ann
        self.is_input = is_input
        self.output_value = value
        
    def activation(self, sigma):
        #return int(sigma > 0)
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
        self.learning_rate = 0.01
        self.binary_threshold = 0.5

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
        
        print 'creating synapse from', axon.id, 'to', dendrite.id, 'with', weight
        self.synapses[dendrite.id][axon.id] = weight

    def weightAtSynapse(self, axon, dendrite):
        return self.synapses[dendrite.id][axon.id]

    def setWeightAtSynapse(self, axon, dendrite, weight):
        self.synapses[dendrite.id][axon.id] = weight

    def addToWeightAtSynapse(self, axon, dendrite, weight):
        if weight:
            print 'adjusting weight', round(self.synapses[dendrite.id][axon.id], 4), 'by', weight
        self.synapses[dendrite.id][axon.id] += weight

    def synapsesAt(self, dendrite):
        bias_synapse = {-1: dendrite.bias}
        return dict (self.synapses[dendrite.id].items() + bias_synapse.items())

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

describeRows(r)

print
print 'starting training:'
i = 0
while 1:
    i += 1
    if i> 5:
        break
    learn_rate = ann.learning_rate
    for t_set in training_data:
        input_a = t_set[0][0]
        input_b = t_set[0][1]
        target = t_set[1]
        n[0].output_value = input_a
        n[1].output_value = input_b
        output = n[2].output()


        
        #inWeight[0]+=rate*(test[i][2]-out)

        
        if output == target:
            wee = '***'
        else:
            wee = ''
        print input_a, input_b, target, output, wee
        new_weight = learn_rate * (target - output)
        #print 'new weight:', new_weight
        ann.addToWeightAtSynapse(n[2], n[4], new_weight)



        output = n[3].output()
        new_weight = learn_rate * (target - output)

        if output == target:
            wee = '***'
        else:
            wee = ''
        print input_a, input_b, target, output, wee
        ann.addToWeightAtSynapse(n[3], n[4], new_weight)


 
        sleep(0.01)
    print 'training set exhausted'
