from itertools import combinations
from random import randint as rnd
random_list = [rnd(0, 1000) for x in range(20)]
print(random_list)
tuples = list(combinations(random_list, 2))
print(tuples)
sums = [(x[0] + x[1]) for x in tuples if (x[0] + x[1])%3 == 1]
print(sums)
for x in tuples:
    try:
        if x[0] + x[1] == max(sums):
            print('Сумма равна: '+str((x[0] + x[1])), 'из элементов списка random_list: '+(str(x[0])+
            ' с индексом '+str(random_list.index(x[0])))+' и', (str(x[1])+' с индексом '+str(random_list.index(x[1]))))
    except ValueError:
        print('Таких чисел нет')