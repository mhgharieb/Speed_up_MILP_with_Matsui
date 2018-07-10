from gurobipy import *

for i in range(7,10):
    model = read(str(i) + ".lp")
    model.optimize()
    model.write(str(i) + ".sol")

