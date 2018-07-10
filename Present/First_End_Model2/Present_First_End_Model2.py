'''
Created on 20180403

@author: Administrator

First_End patterns

'''
#-------------------------------------------------------------------------------
# Name: ToyCipher
#-------------------------------------------------------------------------------
from CryptoMIP import *

opti = [2, 4, 8, 12, 20, 24, 28, 32, 36, 41, 46, 52, 56, 62, 66];

PT = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, \
    1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61, 2, 6, 10, 14, 18, \
    22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 3, 7, 11, 15, 19, 23, 27, 31, 35, \
    39, 43, 47, 51, 55, 59, 63]

ST = [(0, -1, -1, -1, -2, -2, -2, -1, 10, -3, 0), \
(4, 2, 2, 5, 1, 4, 1, 6, -12, 8, 0), \
(0, 1, 1, 2, 3, 1, 3, 1, -3, -1, 0), \
(-1, -8, 7, -3, -2, 4, -2, -9, 14, 11, 0), \
(-5, 2, -2, -3, 5, -1, -4, -2, 10, 3, 0), \
(1, 2, 2, 0, -1, 0, -1, 0, 1, -1, 0), \
(1, -2, -8, -2, -6, -4, 10, -3, 15, 7, 0), \
(-6, -5, 4, -2, -5, -4, 3, -1, 16, 1, 0), \
(2, -6, -4, -4, 5, -8, 3, -6, 20, -1, 0), \
(-1, 4, -5, 1, -2, 0, -3, -1, 7, 4, 0), \
(-3, -2, -2, -3, -1, 1, 1, 1, 9, -1, 0), \
(6, -5, 2, -1, 2, 1, -3, 1, 3, 4, 0), \
(2, 2, -3, 1, -2, 3, 2, -1, 2, 1, 0), \
(-1, 2, 2, 5, 1, -1, 1, 3, -3, 1, 0), \
(0, -1, -1, 0, -1, 0, -1, 0, 4, -1, 0), \
(-3, 2, 2, -2, 1, 0, 1, -4, 5, 2, 0), \
(2, -2, 2, 2, 2, 3, -1, -1, 0, 1, 0), \
(-1, -1, -1, 1, 1, 0, -1, 0, 2, 2, 0), \
(0, 1, -1, -2, -1, -2, -1, 1, 6, -1, 0), \
(3, 1, 2, 0, 2, 4, 2, 4, -6, 1, 0), \
(-1, -1, 0, -1, 1, 0, -1, 1, 4, -1, 0), \
(-2, -6, 4, 2, -5, -4, -1, -5, 17, 1, 0), \
(2, -4, -2, -2, 1, -1, -1, -4, 13, -3, 0), \
(3, 3, 2, 1, 2, -1, 1, -1, 0, -2, 0), \
(1, -1, 1, -3, -2, -3, -2, 1, 9, -1, 0)]

S_T_First = [(-1, -8, 7, -3, -2, 4, -2, -11, 16, 0), \
(-3, -1, -2, 3, 4, -2, -6, 0, 7, 0),\
(3, 1, 1, 2, 2, 3, 5, 4, -8, 0),\
(-1, -2, -2, 1, -4, -1, 5, -2, 6, 0),\
(0, 3, -2, -1, -1, -1, -1, -2, 5, 0),\
(1, -3, 3, 1, 2, -5, -4, 3, 5, 0),\
(0, 2, -1, 1, 4, 3, 1, 2, -4, 0),\
(0, 1, 2, 0, -1, 1, 1, 2, -1, 0),\
(3, -1, -4, 0, -1, -1, 2, 2, 3, 0),\
(0, 2, 2, 1, 1, 0, 1, -1, -1, 0),\
(-1, -1, -3, 0, 2, 1, -3, 0, 5, 0)]

S_T_End=[(-1, -8, 7, -3, -2, 4, -2, -9, 14, 0),\
(5, 4, 4, 6, 1, 3, 1, 7, -14, 0),\
(-2, 4, -4, -7, 1, -3, 2, -3, 12, 0),\
(-1, 2, -3, 1, -1, 0, -2, 0, 4, 0),\
(4, -2, -2, 2, 1, 0, 1, 3, -1, 0),\
(-3, -1, 2, -2, -2, 0, 2, -1, 5, 0),\
(-6, 5, -3, -4, 3, 1, -4, -2, 10, 0),\
(1, 0, 2, 1, 1, -1, -1, 2, -1, 0),\
(-1, 3, 3, 4, 5, 7, 5, 1, -10, 0),\
(1, -2, -2, 0, 1, -2, 1, -1, 5, 0),\
(4, 2, 2, 3, -1, 0, -1, 2, -4, 0),\
(-1, -1, -1, -1, -1, 2, -1, 0, 4, 0)]

class ToyCipher(Cipher):
    def genVars_input_of_round(self, r):
        if r == 1:
            return ['x' + str(j) + '_r' + str(r) for j in range(0, 64)]
        else:
            temp = self.genVars_after_SLayer(r - 1)
            return [temp[PT[i]] for i in range(0, 64)]

    def genVars_after_SLayer(self, r):
        return ['y' + str(j) + '_r' + str(r) for j in range(0, 64)]

    def genVars_ActiveMarkers_of_Round(self, i):
        H = [self.activeMarker + 'H' + str(j) + '_r' + str(i) for j in range(0, self.sboxPerRoud)]
        L = [self.activeMarker + 'L' + str(j) + '_r' + str(i) for j in range(0, self.sboxPerRoud)]
        return H + L

    def genMyObjectiveFun_to_Round(self, i):
        terms = []

        for i in range(1, i + 1):
            H = self.genVars_ActiveMarkers_of_Round(i)[0:16]
            L = self.genVars_ActiveMarkers_of_Round(i)[16:32]
            terms = terms + [L[j] + ' + ' + '2 ' + H[j] for j in range(0, self.sboxPerRoud)]

        return BasicTools.plusTerm(terms)
    
    
    def genObjectiveFun_to_Round(self, i):
        return "xobj"
    
    
    def genConstraints_Additional(self):
        C = [BasicTools.plusTerm(self.genVars_input_of_round(1)) + ' >= 1']
        return C
    
    def genConstraints_First_Round(self):
        X = self.genVars_input_of_round(1)
        Y = self.genVars_after_SLayer(1)
        H = self.genVars_ActiveMarkers_of_Round(1)[0:16]
        L = self.genVars_ActiveMarkers_of_Round(1)[16:32]
        constraints = []
        for k in range(0, 16):
            x = [X[k * 4 + 0], X[k * 4 + 1], X[k * 4 + 2], X[k * 4 + 3]]
            y = [Y[k * 4 + 0], Y[k * 4 + 1], Y[k * 4 + 2], Y[k * 4 + 3]]
            p = [H[k]]
            constraints = constraints + ConstraintGenerator.genFromConstraintTemplate(x + y, p, S_T_First)
            constraints=constraints+[L[k]+' = 0']

        return constraints

    def genConstraints_of_Round(self, r):
        X = self.genVars_input_of_round(r)
        Y = self.genVars_after_SLayer(r)
        H = self.genVars_ActiveMarkers_of_Round(r)[0:16]
        L = self.genVars_ActiveMarkers_of_Round(r)[16:32]
        constraints = []

        for k in range(0, 16):
            x = [X[k * 4 + 0], X[k * 4 + 1], X[k * 4 + 2], X[k * 4 + 3]]
            y = [Y[k * 4 + 0], Y[k * 4 + 1], Y[k * 4 + 2], Y[k * 4 + 3]]
            p = [H[k], L[k]]
            constraints = constraints + \
            ConstraintGenerator.genFromConstraintTemplate(x + y, p, ST)

        return constraints

    def genConstraints_Last_Round(self, r):
        X = self.genVars_input_of_round(r)
        Y = self.genVars_after_SLayer(r)
        H = self.genVars_ActiveMarkers_of_Round(r)[0:16]
        L = self.genVars_ActiveMarkers_of_Round(r)[16:32]
        constraints = []
        for k in range(0, 16):
            x = [X[k * 4 + 0], X[k * 4 + 1], X[k * 4 + 2], X[k * 4 + 3]]
            y = [Y[k * 4 + 0], Y[k * 4 + 1], Y[k * 4 + 2], Y[k * 4 + 3]]
            p = [H[k]]
            constraints = constraints + ConstraintGenerator.genFromConstraintTemplate(x + y, p, S_T_End)
            constraints=constraints+[L[k]+' = 0']

        return constraints

    def genModel(self, ofile, r):
        V = set([])
        C = list([])
        C = C + self.genConstraints_Additional()
        C = C + [self.genMyObjectiveFun_to_Round(r) + ' - xobj = 0']   
        for i in range(1, r + 1):
            if i == 1:
                C = C + self.genConstraints_First_Round()
            elif i<r:
                C = C + self.genConstraints_of_Round(i)
            elif i==r:
                C = C + self.genConstraints_Last_Round(r)

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
            
        print()
        
        for i in range(1, r + 1):
            x = self.genVars_ActiveMarkers_of_Round(i)[1:]
            print(F.getBitPatternsFrom(x))
            print(x)



C = ToyCipher(16)
for R in range(1, 16):C.genModel(str(R) + '.lp', R)
# C.traceSol("2.sol", 2)




