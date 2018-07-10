'''
Created on 20180201

@author: Administrator
'''
from CryptoMIP import *

n = 24  # word size (one branch)
alpha = 8  # right cyclic rotation by alpha bits
beta = 3  # left cyclic rotation by beta bits

opti = [0, 1, 3, 6, 10, 14, 19, 26, 33]

class SPECK(Cipher):
    def genVars_input_of_round(self, r):
        assert (r >= 1)
        return ['L' + str(j) + '_r' + str(r) for j in range(0, n)] + \
               ['R' + str(j) + '_r' + str(r) for j in range(0, n)]

    # Actually, you do not need to implement this
    # Merely for readability
    def genVars_afterAddition_of_round(self, r):
        return self.genVars_input_of_round(r + 1)[0:n]
        
    def genMyObjectiveFun_to_Round(self, start, end):
        terms = []
        for k in range(start, end + 1):
            terms = terms + [self.activeMarker + str(j) + '_r' + str(k) for j in range(1, self.sboxPerRoud)]
        return BasicTools.plusTerm(terms)
       
        
    def genConstraints_Additional(self, r):
        C = ConstraintGenerator.nonZeroActive(self.genVars_input_of_round(1))
        C = C + [self.genMyObjectiveFun_to_Round(1, r) + ' - xobj = 0']
        
        for i in range(1, r):
            temp = ""
            pre = self.genMyObjectiveFun_to_Round(1, i)
            temp = pre + ' - xobj' + ' <= ' + str(-opti[r - i - 1])
            C = C + [temp]               
        return C      
    
    def genConstraints_of_Round(self, r):
        L_in = self.genVars_input_of_round(r)[0:n]
        R_in = self.genVars_input_of_round(r)[n:2 * n]
        L_out = self.genVars_input_of_round(r + 1)[0:n]
        R_out = self.genVars_input_of_round(r + 1)[n:2 * n]
        Seq_AM = self.genVars_ActiveMarkers_of_Round(r)

        X = BasicTools.rightCyclicRotation(L_in, alpha)
        Y = BasicTools.leftCyclicRotation(R_in, beta)

        constraints = []
        constraints = constraints + ConstraintGenerator.moduloAddition_differential_Constraints(X, R_in, L_out, Seq_AM)

        constraints = constraints + ConstraintGenerator.xorConstraints(Y, L_out, R_out)

        return constraints
    def genObjectiveFun_to_Round(self, r):
        return "xobj"
    
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
        for i in range(1, r + 1):
            x = self.genVars_input_of_round(i)
            print(F.getBitPatternsFrom(x))


def main():
    mySPECK = SPECK(n)
    for i in range(1, 11):
        mySPECK.genModel(str(i) + ".lp", i)

if __name__ == '__main__':
    main()
