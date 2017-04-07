igralec1 = 'prvi igralec'
igralec2 = 'drugi igralec'
konec_igre = 'konec igre'
konec_poteze = 'konec poteze'
ni_konec_poteze = 'ni konec poteze'

def nasprotnik(oseba):
    if oseba == igralec1:
        return igralec2
    elif oseba == igralec2:
        return igralec1
    else:
        assert False, 'Funkcija nasprotnik je dobila nekaj čudnega.'
		
class Igra():
    def __init__(self, sirina, visina):
	
        self.na_vrsti = igralec1

        self.sirina = sirina
        self.visina = visina
        self.plosca=[[set() for j in range(self.sirina)]
                     for i in range(self.visina)]
        self.smeri=list(range(-4,4))

        seznam_neproblematicnih=list(range(int((self.sirina-1)/2-1)))+list(
            range(int((self.sirina-1)/2+2),self.sirina))
        for i in seznam_neproblematicnih:
            self.plosca[0][i] |= {-4,-3,-2,-1,1,2,3,4}
            self.plosca[-1][i] |= {-4,-3,-2,-1,1,2,3,4}
            self.plosca[1][i] |= {-3,-4,1,-2,2}
            self.plosca[-2][i] |= {-1,4,3,2,-2}
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

        #print(self.plosca)

    def dovoljen_korak(self, staro, novo):
        smer = self.smer_koraka(staro,novo)
        if smer == None:
            return False
        elif smer in self.plosca[staro[0]][staro[1]]:
            return False
        else:
            return True

    def zapomni_korak(self, staro, novo):
        smer = self.smer_koraka(staro,novo)
        self.plosca[staro[0]][staro[1]].add(smer)
        self.plosca[novo[0]][novo[1]].add(-smer)
        #print(smer)

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
            assert("Funkcija smer je v težavah.") #TODO error
        #print(x_razlika, y_razlika, smer)
        return smer
	
    def povleci_korak(self, staro, novo):
        #NINA ali rabiva funkcijo zapomni korak posebej?
        self.zapomni_korak(staro, novo)
                            
    
    def preveri_konec_poteze(self):
        pass
            # vrne ali je konec poteze ali ne (True, False)
            # to vključuje konec igre!!!
	
    def trenutno_stanje(self, novo):
        #funkcija ki iz trenutnega stanja ugotovi ali je konec igre in kdo je zmagovalec/oziroma na potezi)
        if novo in {(0,int((self.sirina-1)/2)),
                    (0,int((self.sirina-1)/2+1)),
                    (0,int((self.sirina-1)/2+2))}: # seznam zgornjega gola
            return (konec_igre, igralec1) 
        elif novo in {(self.visina-1,int((self.sirina-1)/2)),
                    (self.visina-1,int((self.sirina-1)/2+1)),
                    (self.visina-1,int((self.sirina-1)/2+2))}:
            return (konec_igre, igralec2)
        elif len(self.plosca[novo[0]][novo[1]]) == 8:
            return (konec_igre, None) #None pomeni remi
        # Ker že prej dodava na seznam, mora imeti seznam le en element, ne nobenega
        elif len(self.plosca[novo[0]][novo[1]]) != 1:
            return (ni_konec_poteze, self.na_vrsti)
        elif len(self.plosca[novo[0]][novo[1]]) == 1:
            self.na_vrsti =  nasprotnik(self.na_vrsti)
            return (konec_poteze, self.na_vrsti)
        else:
            assert('Dobimo nemogoče trenutno stanje.') #TODO error

