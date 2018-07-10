#-------------------------------------------------------------------------------
# Name: ToyCipher
#-------------------------------------------------------------------------------
from CryptoMIP import *

opti= [2,4,8,12,20,24,28,32,36,41,46,52,56,62,66];

PT = [0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,\
    1,5,9,13,17,21,25,29,33,37,41,45,49,53,57,61,2,6,10,14,18,\
    22,26,30,34,38,42,46,50,54,58,62,3,7,11,15,19,23,27,31,35,\
    39,43,47,51,55,59,63]

ST = [(0, -1, -1, -1, -2, -2, -2, -1, 10, -3, 0),\
(4, 2, 2, 5, 1, 4, 1, 6, -12, 8, 0),\
(0, 1, 1, 2, 3, 1, 3, 1, -3, -1, 0),\
(-1, -8, 7, -3, -2, 4, -2, -9, 14, 11, 0),\
(-5, 2, -2, -3, 5, -1, -4, -2, 10, 3, 0),\
(1, 2, 2, 0, -1, 0, -1, 0, 1, -1, 0),\
(1, -2, -8, -2, -6, -4, 10, -3, 15, 7, 0),\
(-6, -5, 4, -2, -5, -4, 3, -1, 16, 1, 0),\
(2, -6, -4, -4, 5, -8, 3, -6, 20, -1, 0),\
(-1, 4, -5, 1, -2, 0, -3, -1, 7, 4, 0),\
(-3, -2, -2, -3, -1, 1, 1, 1, 9, -1, 0),\
(6, -5, 2, -1, 2, 1, -3, 1, 3, 4, 0),\
(2, 2, -3, 1, -2, 3, 2, -1, 2, 1, 0),\
(-1, 2, 2, 5, 1, -1, 1, 3, -3, 1, 0),\
(0, -1, -1, 0, -1, 0, -1, 0, 4, -1, 0),\
(-3, 2, 2, -2, 1, 0, 1, -4, 5, 2, 0),\
(2, -2, 2, 2, 2, 3, -1, -1, 0, 1, 0),\
(-1, -1, -1, 1, 1, 0, -1, 0, 2, 2, 0),\
(0, 1, -1, -2, -1, -2, -1, 1, 6, -1, 0),\
(3, 1, 2, 0, 2, 4, 2, 4, -6, 1, 0),\
(-1, -1, 0, -1, 1, 0, -1, 1, 4, -1, 0),\
(-2, -6, 4, 2, -5, -4, -1, -5, 17, 1, 0),\
(2, -4, -2, -2, 1, -1, -1, -4, 13, -3, 0),\
(3, 3, 2, 1, 2, -1, 1, -1, 0, -2, 0),\
(1, -1, 1, -3, -2, -3, -2, 1, 9, -1, 0)]



class ToyCipher(Cipher):
    def genVars_input_of_round(self, r):
        if r == 1:
            return ['x'+str(j)+'_r'+str(r) for j in range(0, 64)]
        else:
            temp = self.genVars_after_SLayer(r-1)
            return [temp[PT[i]] for i in range(0, 64)]

    def genVars_after_SLayer(self, r):
        return ['y' + str(j) + '_r' + str(r) for j in range(0, 64)]

    def genVars_ActiveMarkers_of_Round(self, i):
        H = [self.activeMarker+'H'+ str(j) + '_r' + str(i) for j in range(0, self.sboxPerRoud)]
        L = [self.activeMarker+'L'+ str(j) + '_r' + str(i) for j in range(0, self.sboxPerRoud)]
        return H + L

    def genMyObjectiveFun_to_Round(self, i):
        terms = []

        for i in range(1, i+1):
            H = self.genVars_ActiveMarkers_of_Round(i)[0:16]
            L = self.genVars_ActiveMarkers_of_Round(i)[16:32]
            terms = terms + [L[j]+' + ' + '2 '+H[j] for j in range(0, self.sboxPerRoud)]

        return BasicTools.plusTerm(terms)

    def genObjectiveFun_of_Rounds(self, L):
        terms = []
        for i in L:
            H = self.genVars_ActiveMarkers_of_Round(i)[0:16]
            L = self.genVars_ActiveMarkers_of_Round(i)[16:32]
            terms = terms + [L[j]+' + ' + '2 '+H[j] for j in range(0, self.sboxPerRoud)]

        return BasicTools.plusTerm(terms)


    def genObjectiveFun_to_Round(self, i):
        return "xobj"

    def genConstraints_Additional(self):
        C = [BasicTools.plusTerm(self.genVars_input_of_round(1)) + ' >= 1']
        C = C + [self.genMyObjectiveFun_to_Round(R) + ' - xobj = 0']


        for i in range(1, R):
            pre = self.genMyObjectiveFun_to_Round(i)
            temp = pre + ' - xobj' + ' + ' + str(opti[R - i - 1]) + ' <= 0'
            C = C + [temp]

        return C


    def genConstraints_of_Round(self, r):
        X = self.genVars_input_of_round(r)
        Y = self.genVars_after_SLayer(r)
        H = self.genVars_ActiveMarkers_of_Round(r)[0:16]
        L = self.genVars_ActiveMarkers_of_Round(r)[16:32]
        constraints =[]

        for k in range(0, 16):
            x = [X[k*4+0], X[k*4+1], X[k*4+2], X[k*4+3]]
            y = [Y[k*4+0], Y[k*4+1], Y[k*4+2], Y[k*4+3]]
            p = [H[k], L[k]]
            constraints = constraints + \
            ConstraintGenerator.genFromConstraintTemplate(x+y, p, ST)

        return constraints

    def genModel(self, ofile, r):
        V = set([])
        C = list([])

        for i in range(1, r+1):
            C = C + self.genConstraints_of_Round(i)

        C = C + self.genConstraints_Additional()


        V = BasicTools.getVariables_From_Constraints(C)
        V.remove('xobj')

        myfile=open(ofile,'w')
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


    def genORD(self, ofile, r):
        V = list()
        VV = list()

        for i in range(1, r+1):
            V = V + self.genVars_ActiveMarkers_of_Round(i)
            V = V + self.genVars_input_of_round(i)
            V = V + self.genVars_after_SLayer(i)
            for v in V:
                VV.append((v, str(-i)))

        VV.append(('xobj', '-100'))

        myfile=open(ofile,'w')
        for vv in VV:
            print(vv[0]+' '+vv[1], file = myfile)

        myfile.close()



R = 12
C = ToyCipher(16)
C.genModel(str(R)+'.lp', R)
C.genORD(str(R)+'.ord', R)





