from ann import *


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
