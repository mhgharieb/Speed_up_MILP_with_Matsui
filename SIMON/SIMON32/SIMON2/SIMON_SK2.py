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
    
    def genMyObjectiveFun_to_Round(self, start, end):
        terms = []
        for k in range(start, end + 1):
            terms = terms + [self.activeMarker + str(j) + '_r' + str(k) for j in range(0, self.sboxPerRoud)]
        return BasicTools.plusTerm(terms)
    
        
    def genConstraints_Additional(self, r):
        constraints = []
        constraints = ConstraintGenerator.nonZeroActive(self.genVars_input_of_round(1))
        constraints = constraints + [self.genMyObjectiveFun_to_Round(1, r) + ' - xobj = 0']
        return constraints
    
    
    def genObjectiveFun_to_Round(self, i):
        return "xobj"
    
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
    
    def genModel(self, ofile, r):
        V = set([])
        C = list([])

        for i in range(1, r + 1):
            C = C + self.genConstraints_of_Round(i)

        C = C + self.genConstraints_Additional(r)


        V = BasicTools.getVariables_From_Constraints(C)
        V.remove('xobj')

        myfile = open(ofile, 'w')
        print('Minimize', file = myfile)
        print(self.genObjectiveFun_to_Round(r), file = myfile)
        print('\n', file = myfile)
        print('Subject To', file = myfile)
        for c in C:
            print(c, file = myfile)
        
        print('\n', file = myfile)
        print('Generals', file = myfile)
        print('xobj', file = myfile)

        print('\n', file = myfile)
        print('Binary', file = myfile)
        for v in V:
            print(v, file = myfile)
        myfile.close()
        
    def traceSol(self, f, r):
        F = SolFilePaser(f)
        for i in range(1, r + 2):
            x = self.genVars_input_of_round(i)
            print(F.getBitPatternsFrom(x))


    
mySIMON = SIMON(n)  
for i in range(1, 13):
    mySIMON.genModel("SIMON" + str(i) + ".lp", i)
    
