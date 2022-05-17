import math
import random
import matplotlib.pyplot as plt

from chart import Curve, Chart


def permutation(n):
    pile_initiale = list(range(2, n+1))
    pile_finale = [[1]]

    while pile_initiale:
        i = random.randint(0, len(pile_initiale))
        if i == 0:
            pile_finale.append([])
            i = 1
        pile_finale[-1].append(pile_initiale[i - 1])
        del pile_initiale[i - 1]

    return pile_finale


# print(permutation(10))
essais = 1000
# x = [sum([10**j + i*10**j for i in range(9)]) for j in range(3)]
x = [10 + i*10 for i in range(9)] + [100 + i*100 for i in range(9)] +\
    [1000 + i*1000 for i in range(9)] + [10000 + i*10000 for i in range(10)]
y1 = []
for t in x:
    print(t)
    liste = [len(permutation(t)) for _ in range(essais)]
    y1.append(sum(liste) / len(liste))
y2 = [math.log(t, math.e) for t in x]

chart = Chart(1)
chart.add_curve(Curve(y1, x_axis=x, name="Valeur pratique"))
chart.add_curve(Curve(y2, x_axis=x, name="Valeur théorique"))
chart.display()