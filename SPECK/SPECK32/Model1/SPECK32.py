from CryptoMIP import *
n = 16 # word size (one branch)
alpha = 7 # right cyclic rotation by alpha bits
beta = 2  # left cyclic rotation by beta bits
class SPECK(Cipher):
    def genVars_input_of_round(self, r):
        assert (r >= 1)
        return ['L' + str(j) + '_r' + str(r) for j in range(0, n)] + ['R' + str(j) + '_r' + str(r) for j in range(0, n)]
               
    def genVars_afterAddition_of_round(self, r):
        return self.genVars_input_of_round(r+1)[0:n]

    def genConstraints_Additional(self):
        return ConstraintGenerator.nonZeroActive(self.genVars_input_of_round(1))
        
    def genObjectiveFun_to_Round(self, i):
        terms = []
        for k in range(1, i + 1):
            terms = terms + [self.activeMarker + str(j) + '_r' + str(k) for j in range(1, self.sboxPerRoud)]
        return BasicTools.plusTerm(terms)
    
    def genConstraints_of_Round(self, r):
        L_in = self.genVars_input_of_round(r)[0:n]
        R_in = self.genVars_input_of_round(r)[n:2*n]
        L_out = self.genVars_input_of_round(r+1)[0:n]
        R_out = self.genVars_input_of_round(r+1)[n:2*n]
        Seq_AM = self.genVars_ActiveMarkers_of_Round(r)

        X = BasicTools.rightCyclicRotation(L_in, alpha)
        Y = BasicTools.leftCyclicRotation(R_in, beta)

        constraints = []
        constraints = constraints + ConstraintGenerator.moduloAddition_differential_Constraints(X, R_in, L_out, Seq_AM)
        constraints = constraints + ConstraintGenerator.xorConstraints(Y, L_out, R_out)
        return constraints

    def traceSol(self, f, r):
        F = SolFilePaser(f)
        for i in range(1, r + 2):
            x = self.genVars_input_of_round(i)
            print(F.getBitPatternsFrom(x))


def main():
    mySPECK = SPECK(n)
    for i in range(1, 10):
        mySPECK.genModel(str(i) + ".lp", i)

if __name__ == '__main__':
    main()
