from random import randint

training_data = list()

for i in range(100):
    a = randint(0, 1)
    b = randint(0, 1)
    c = a
    training_data.append(
        {'input': (a, b), 'correct': c}
    )

print 'importing training data...'
for i in training_data:
    print i
