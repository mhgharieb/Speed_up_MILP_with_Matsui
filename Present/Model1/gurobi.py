from gurobipy import *


model = read("5.lp")
model.optimize()
model.write("5.sol")


