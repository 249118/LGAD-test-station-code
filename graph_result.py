import matplotlib.pyplot as plt
import numpy as np
import csv
import sys 

with open('measurment.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    x = []
    y = []
    next(reader)
    next(reader)
    for row in reader:
        x.append(float(row[0])) 
        temp = list(map(float, row[6000:10001]))
        y.append(np.trapz(temp))

fig, ax = plt.subplots()
ax.plot(x, y)

ax.set(xlabel='voltage', ylabel='charge',
       title='Example of output data for HV sweep')
ax.grid()
plt.show()