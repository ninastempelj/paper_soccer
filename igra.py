class Igra():
    def __init__(self):
        self.sirina=9 #TODO kako dobiš te podatke iz gui-ja
        self.visina=13
        self.plosca=[[set() for j in range(self.sirina)]
                     for i in range(self.visina)]
        self.smeri=list(range(-4,4))

        seznam_neproblematicnih=list(range(int((self.sirina-1)/2-1)))+list(
            range(int((self.sirina-1)/2+1),self.sirina))
        for i in seznam_neproblematicnih:
            self.plosca[0][i] |= {-4,-3,-2,-1,1,2,3,4}
            self.plosca[-1][i] |= {-4,-3,-2,-1,1,2,3,4}
            self.plosca[1][i] |= {-3,-4,1,-2,2}
            self.plosca[-1][i] |= {-1,4,3,2,-2}
        for i in range(1,self.visina):
            self.plosca[i][0] |= {-3,-2,-1,4,-4}
            self.plosca[i][-1] |= {1,2,3,-4,4}
        #Gol zgoraj
        self.plosca[0][int((self.sirina-1)/2)] |={4,-1,-2,-3,-4,1,2}
        self.plosca[0][int((self.sirina-1)/2+1)] |={-2,-3,-4,1,2}
        self.plosca[0][int((self.sirina-1)/2+2)] |={-2,-3,-4,1,2,3,4}
        self.plosca[1][int((self.sirina-1)/2)] |={-2,-3,-4}
        self.plosca[1][int((self.sirina-1)/2+2)] |={-4,1,2}
        
        #Gol spodaj
        self.plosca[-1][int((self.sirina-1)/2)] |={2,3,4,-1,-2,-3,-4}
        self.plosca[-1][int((self.sirina-1)/2+1)] |={-2,2,3,4,-1}
        self.plosca[-1][int((self.sirina-1)/2+2)] |={-4,1,2,3,4,-1,-2}
        self.plosca[-2][int((self.sirina-1)/2)] |={4,-1,-2}
        self.plosca[-2][int((self.sirina-1)/2+2)] |={2,3,4}

        print(self.plosca)

    def dovoljen_korak(self, staro, novo):
        if self.smer_koraka(staro,novo) == None:
            return False
        if self.smer_koraka(staro,novo) in self.plosca[staro[0]][staro[1]]:
            return False
        else:
            return True

    def naredi_korak(self, staro, novo):
        self.plosca[staro[0]][staro[1]].add(self.smer_koraka(staro,novo))
        self.plosca[novo[0]][novo[1]].add(-(self.smer_koraka(staro,novo)))

    def smer_koraka(self, staro, novo):
        x_razlika = staro[0] - novo[0]
        y_razlika = staro[1] - novo[1]
        if abs(x_razlika)>1 or abs(y_razlika)>1 or (x_razlika==0 and y_razlika==0):
            return None
        elif x_razlika == 0:
            smer = (-2)*y_razlika
        elif y_razlika ==0:
            smer=(-4)*x_razlika
        elif x_razlika == y_razlika:
            smer =(-3)*x_razlika
        elif x_razlika != y_razlika:
            smer = (-1)*x_razlika
        else:
            print("Funkcija smer je v težavah")
        return smer
        
        
        
        
      
