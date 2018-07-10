from gurobipy import *

for i in range(10, 11):
    model = read(str(i) + ".lp")
    model.optimize()
    model.write(str(i) + ".sol")

