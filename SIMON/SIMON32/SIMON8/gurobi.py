from gurobipy import *

for i in range(12, 13):
    model = read("SIMON" + str(i) + ".lp")
    model.optimize()
    model.write("SIMON" + str(i) + ".sol")

