from numpy import exp

sigmoid = lambda x: 1 / (1 + exp(-x))

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
            

class Neuron:
    def __init__(self, neuron_id, Ann, is_input=False, value=1):
        self.id = neuron_id
        self.Ann = Ann
        self.is_input = is_input
        self.value = value
        
    def activation(self, sigma):
        return sigmoid(sigma)
    
    def output(self):
        print 'computing output for', self.id
        if self.is_input:
            return self.value
        sigma = 
        #print 'synapses'
        synapses = self.Ann.synapsesAt(self.id)
        #print synapses
        for synapse_id in synapses:
            sigma += self.Ann.valueAt(synapse_id) * synapses[synapse_id]
        return self.activation(sigma)
    
    def setValue(self, value):
        self.value = value


ann = ANN()
ann.addNeuron(6)
n = ann.neurons
r = dict()
r[0] = n[0:3]
for btm_neuron in r[0]:
    # make all bottom row neurons inputs
    btm_neuron.is_input = True
    btm_neuron.value = 1
    
r[1] = n[3:5]
r[2] = n[5:6]

ann.connectAllToAll (r[0], r[1]) (r[1], r[2])
