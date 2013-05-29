from random import randint
from os import system

def trainingData(length):
    training_data = list()
    for i in range(length):
        a = randint(0, 1)
        b = randint(0, 1)
        c = a
        training_data.append(
            ((a, b),  c)
        )
    return training_data
    #print 'creating training data...'
    #for i in training_data:
    #    print i

def printLearnInfo(input_a, input_b, target, output):
    if (output > 0.5 and target == 1) or (output < 0.5 and target == 0):
        print input_a, input_b, target, output, '***'
    else:
        print input_a, input_b, target, output
        
