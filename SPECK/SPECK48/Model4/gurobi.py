from gurobipy import *

model = read("SPECK6.lp")
model.optimize()
model.write("SPECK6.sol")


