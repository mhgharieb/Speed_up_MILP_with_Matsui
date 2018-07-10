from CryptoMIP import *

n = 16  # word size (one branch)

S_T_3XOR = [(1, -1, 1, 1, 0), \
(-1, -1, 1, -1, 2), \
(-1, -1, -1, 1, 2), \
(-1, 1, -1, -1, 2), \
(-1, 1, 1, 1, 0), \
(1, -1, -1, -1, 2), \
(1, 1, 1, -1, 0), \
(1, 1, -1, 1, 0)]  # Constraints template for a xor b xor c = d


class SIMON(Cipher):
    
    def genVars_input_of_round(self, r):
        assert (r >= 1)
        return ['L' + str(i) + '_r' + str(r) for i in range(0, n)] + \
               ['R' + str(i) + '_r' + str(r) for i in range(0, n)]
    
    def genVars_afterAnd_of_round(self,r):
        assert (r >= 1)
        return ['v_AfterAnd_' + str(r) + '_' + str(i) for i in range(0, n)]
    
    def genVars_after3XOR_of_round(self, r):
        assert (r >= 1)
        return self.genVars_input_of_round(r + 1)[0:n]
    
    def genConstraints_Additional(self):
        return [BasicTools.plusTerm(self.genVars_input_of_round(1)) + ' >= 1']
    
    def genConstraints_of_Round(self, r):
        constraints = []
        X0 = self.genVars_input_of_round(r)[0:n]
        S1 = BasicTools.leftCyclicRotation(X0, 1)
        S8 = BasicTools.leftCyclicRotation(X0, 8)
        Y = self.genVars_afterAnd_of_round(r)
        constraints = constraints + ConstraintGenerator.andConstraints(S1, S8, Y)
        for i in range(0, n):
            constraints = constraints + ConstraintGenerator.activeSboxConstraints([S1[i], S8[i]], [Y[i]], r, i, self.activeMarker)

        X1 = self.genVars_input_of_round(r)[n:2 * n]
        S2 = BasicTools.leftCyclicRotation(X0, 2)
        for i in range(0,n):
            in_vars = [X1[i], Y[i], S2[i]]
            out_vars = [self.genVars_input_of_round(r + 1)[i]]
            constraints = constraints + ConstraintGenerator.genFromConstraintTemplate(in_vars, out_vars, S_T_3XOR)
            
        constraints = constraints + ConstraintGenerator.equalConstraints(X0, self.genVars_input_of_round(r + 1)[n:2 * n])
        return constraints   
    
    def traceSol(self, f, r):
        F = SolFilePaser(f)
        for i in range(1, r + 2):
            x = self.genVars_input_of_round(i)
            print(F.getBitPatternsFrom(x))


    
mySIMON = SIMON(n)  
for i in range(1, 16):
    mySIMON.genModel("SIMON" + str(i) + ".lp", i)
