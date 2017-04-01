class Igra():
    def __init__(self):
        self.igralec1= "Čarovnik"#TODO uvozi iz GUi
        self.igralec2 = "Duh"#TODO uvozi iz gui
        self.na_vrsti = self.igralec1

        self.sirina=9 #TODO kako dobiš te podatke iz gui-ja
        self.visina=13
        self.plosca=[[set() for j in range(self.sirina)]
                     for i in range(self.visina)]
        self.smeri=list(range(-4,4))

        seznam_neproblematicnih=list(range(int((self.sirina-1)/2-1)))+list(
            range(int((self.sirina-1)/2+2),self.sirina))
        for i in seznam_neproblematicnih:
            self.plosca[0][i] |= {-4,-3,-2,-1,1,2,3,4}
            self.plosca[-1][i] |= {-4,-3,-2,-1,1,2,3,4}
            self.plosca[1][i] |= {-3,-4,1,-2,2}
            self.plosca[-1][i] |= {-1,4,3,2,-2}
        for i in range(1,self.visina):
            self.plosca[i][0] |= {-3,-2,-1,4,-4}
            self.plosca[i][-1] |= {1,2,3,-4,4}
        #Gol zgoraj
        self.plosca[0][int((self.sirina-1)/2-1)] |={4,-1,-2,-3,-4,1,2}
        self.plosca[0][int((self.sirina-1)/2)] |={-2,-3,-4,1,2}
        self.plosca[0][int((self.sirina-1)/2+1)] |={-2,-3,-4,1,2,3,4}
        self.plosca[1][int((self.sirina-1)/2-1)] |={-2,-3,-4}
        self.plosca[1][int((self.sirina-1)/2+1)] |={-4,1,2}
        
        #Gol spodaj
        self.plosca[-1][int((self.sirina-1)/2-1)] |={2,3,4,-1,-2,-3,-4}
        self.plosca[-1][int((self.sirina-1)/2)] |={-2,2,3,4,-1}
        self.plosca[-1][int((self.sirina-1)/2+1)] |={-4,1,2,3,4,-1,-2}
        self.plosca[-2][int((self.sirina-1)/2-1)] |={4,-1,-2}
        self.plosca[-2][int((self.sirina-1)/2+1)] |={2,3,4}

        print(self.plosca)

    def dovoljen_korak(self, staro, novo):
        if self.smer_koraka(staro,novo) == None:
            return False
        elif self.smer_koraka(staro,novo) in self.plosca[staro[0]][staro[1]]:
            return False
        else:
            return True

    def naredi_korak(self, staro, novo): #ta funkcija bi imela bolj smiseln ime
        #dodaj korak na seznam al kej tazga...
        self.plosca[staro[0]][staro[1]].add(self.smer_koraka(staro,novo))
        self.plosca[novo[0]][novo[1]].add(-(self.smer_koraka(staro,novo)))
        print(self.smer_koraka(staro,novo))

    def smer_koraka(self, staro, novo):
        x_razlika = staro[1] - novo[1]
        y_razlika = staro[0] - novo[0]
        if abs(x_razlika)>1 or abs(y_razlika)>1 or (
            x_razlika==0 and y_razlika==0):
            return None
        elif x_razlika == 0:
            smer = (-4)*y_razlika
        elif y_razlika ==0:
            smer=(-2)*x_razlika
        elif x_razlika == y_razlika:
            smer =(-3)*x_razlika
        elif x_razlika != y_razlika:
            smer = (-1)*x_razlika
        else:
            print("Funkcija smer je v težavah")
        #print(x_razlika, y_razlika, smer) ##NINA!!! Zakaj se nama ob vsakem koraku to sprinta 5krat?!
        return smer

    def nasprotnik(self, oseba):
        if oseba == self.igralec1:
            return self.igralec2
        elif oseba == self.igralec2:
            return self.igralec1
        else:
            assert('Funkcija nasprotnik je dobila nekaj čudnega')

    def trenutno_stanje(self, novo): #funkcija ki iz trenutnega stanja ugotovi ali je konec igre in kdo je zmagovalec/oziroma na potezi)
        if novo in {(0,int((self.sirina-1)/2)),
                    (0,int((self.sirina-1)/2+1)),
                    (0,int((self.sirina-1)/2+2))}:#seznam zgornjega gola
            return ("konec", self.igralec1) 
        elif novo in {(self.visina-1,int((self.sirina-1)/2)),
                    (self.visina-1,int((self.sirina-1)/2+1)),
                    (self.visina-1,int((self.sirina-1)/2+2))}:
            return ("konec", self.igralec2)
        elif len(self.plosca[novo[0]][novo[1]]) == 8: #Nina, ali se sproži ta funkcija preden dodava novo smer na seznam ali ne?
            return ("konec", None) #None pomeni remi
        elif len(self.plosca[novo[0]][novo[1]]) != 1:#Ker že prej dodava na seznam
            return ("ni konec", self.na_vrsti)
        elif len(self.plosca[novo[0]][novo[1]]) == 1:
            self.na_vrsti =  self.nasprotnik(self.na_vrsti)
            return ("ni konec", self.na_vrsti)
        else:
            assert('Dobimo nemogoče trenutno stanje')

    def premakni_zogo(self,staro, novo, sirina):
        x=staro[1]-novo[1]
        y=staro[0]-novo[0]
        print(x*sirina, y*sirina)
        return(int(x*sirina), int(y*sirina))
        
