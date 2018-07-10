from gurobipy import *

i = 10
model = read(str(i) + ".lp")
model.optimize()
model.write(str(i) + ".sol")
