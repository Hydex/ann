#!/usr/bin/python2.7

from numpy import exp
from time import sleep
from os import system

from training_data import training_data

sigmoid = lambda u: 1 / (1 + exp(-u))

class Neuron:
    
    def __init__(self, neuron_id, Ann, is_input=False, value=1):
        self.id = neuron_id
        self.bias = 0
        self.Ann = Ann
        self.is_input = is_input
        self.output_value = value
        
    def activation(self, sigma):
        #return int(bool(sigma))
        return sigmoid(sigma)
    
    def output(self):
        if self.is_input:
            return self.output_value
        sigma = self.bias
        synapses = self.Ann.synapsesAt(self.id)
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
        return self.connectAllToAll
                
    def weightAtSynapse(self, source_neuron, dest_neuron):
        return self.synapses[source_neuron.id][dest_neuron.id]
    
    def synapsesAt(self, neuron_id):
        if self.synapses.has_key(neuron_id):
            return self.synapses[neuron_id]
        return {}
    
    def valueAt(self, neuron_id):
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
ann.addNeuron(6)
n = ann.neurons
r = dict()


r[0] = n[0:2]
r[1] = n[2:5]
r[2] = n[5:7]


for btm_neuron in r[0]:
    btm_neuron.is_input = True
    btm_neuron.output_value = 1


ann.connectAllToAll (r[0], r[1]) \
                    (r[1], r[2]) \


print
for i in range(len(r)):
    print 'row', i + 1, 'size:', len(r[i]), ', members:',
    for huh in r[i]:
        print huh.id,
    print



for t in training_data:
    input_vector = t[0]
    expected = t[1]
    n[0].output_value = input_vector[0]
    n[1].output_value = input_vector[1]
    print '--------------------'
    print input_vector, '-', expected, '-', round(n[5].output(), 5)










"""
for b in range(0, 10):
    for a in range(0, 10):
        n[0].output_value = a / 10.0
        n[1].output_value = b / 10.0

        output_string  = 'a= %f\n' % round(n[0].output_value, 4)
        output_string += 'b= %f\n' % round(n[1].output_value, 4)
        output_string += 'neuron= %f' % n[4].output()

        system('clear')
        print output_string
        sleep(0.1)
"""
