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
