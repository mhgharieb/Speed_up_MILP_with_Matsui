from gurobipy import *

for i in range(6, 7):
    model = read(str(i) + ".lp")
    model.setParam(GRB.Param.Threads, 1)
    model.optimize()
    model.write(str(i) + ".sol")


