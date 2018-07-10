from gurobipy import *

i = 12
model = read(str(i) + ".lp")
model.optimize()
model.write(str(i) + ".sol")
