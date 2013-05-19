from random import randint

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

training_data = trainingData(100)
