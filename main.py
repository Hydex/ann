class ANN:
    def __init__(self):
        self.neurons = list()
        self.synapses = dict()
    def synapsesAt(self, neuron_id):
        if self.synapses.has_key(neuron_id):
            return self.synapses[neuron_id]
        return {}
    def valueAt(self, neuron_id):
        #print '-->', self.neurons[neuron_id]
        return self.neurons[neuron_id].output()
    def addNeuron(self, number_of=1):
        for i in range(number_of):
            neuron_id = len(self.neurons)
            neuron = Neuron(neuron_id, self)
            self.neurons.append(neuron)
    def addSynapse(self, dest_neuron, source_neuron, weight):
        if not self.synapses.has_key(source_neuron.id):
            self.synapses[source_neuron.id] = dict()
        self.synapses[source_neuron.id][dest_neuron.id] = weight
            

class Neuron:
    def __init__(self, neuron_id, Ann, is_input=False, value=1):
        self.id = neuron_id
        self.Ann = Ann
        self.is_input = is_input
        self.value = value       
    def output(self):
        if self.is_input:
            #print 'neuron is input, overrides to', self.value
            return self.value
        sigma = 0
        synapses = self.Ann.synapsesAt(self.id)
        for synapse_id in synapses:
            #print 'processing synapse', synapse_id
            sigma += self.Ann.valueAt(synapse_id) * synapses[synapse_id]
        return sigma
    def setValue(self, value):
        self.value = value

print 'creating network of 4 neurons (2 input, 2 output)'

ann = ANN()
ann.addNeuron(4)

n = ann.neurons

n[0].is_input = True
n[1].is_input = True

ann.addSynapse(n[0], n[2], 1)
ann.addSynapse(n[0], n[3], 1)
ann.addSynapse(n[1], n[2], 1)
ann.addSynapse(n[1], n[3], 1)

print 'neuron', n[2].id, 'outputs value of' , n[2].output()
print 'neuron', n[3].id, 'outputs value of' , n[3].output()
