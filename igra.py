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
        self.smeri= list(range(-4,0)) + list(range(1,5))
		
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

        self.zgodovina = []
        self.gol_zgoraj = {(0,int((self.sirina-1)/2)),
                           (0,int((self.sirina-1)/2+1)),
                           (0,int((self.sirina-1)/2-1))}
        self.gol_spodaj = {(self.visina-1,int((self.sirina-1)/2)),
                           (self.visina-1,int((self.sirina-1)/2+1)),
                           (self.visina-1,int((self.sirina-1)/2-1))}

        #print(self.plosca)

    def dovoljen_korak(self, staro, novo):

        smer = self.smer_koraka(staro,novo)
        if smer == None:
            return False
        elif smer in self.plosca[staro[0]][staro[1]]:
            return False
        else:
            return True

    def mozen_korak(self, igrisce, trenutno):
        mozni = []
        for smer in self.smeri:
            if smer in igrisce[trenutno[0]][trenutno[1]]:
                pass
            else:
                mozni.append(self.anti_smer_koraka(trenutno, smer))
        # print(mozni)
        return mozni        

    def mozne_poteze(self, plosca, trenutno, prvi_korak=True):
        mozni = self.mozen_korak(plosca, trenutno)
        if mozni == [] or\
                (not prvi_korak and len(mozni) == 7) or\
                trenutno in self.gol_spodaj|self.gol_zgoraj:
            return []

        else:
            poteze = []
            for sosednje in mozni:
                (sos_vrs, sos_stolp) = sosednje
                (tre_vrs, tre_stolp) = trenutno
                smer = self.smer_koraka(trenutno, sosednje)
                #plosca_tega = [plosca[i][:] for i in range(self.visina)]
                #plosca_tega[sos_vrs][sos_stolp].add(-smer)
                #plosca_tega[tre_vrs][tre_stolp].add(smer)
                plosca[sos_vrs][sos_stolp].add(-smer)
                plosca[tre_vrs][tre_stolp].add(smer)
                poteze_tega = self.mozne_poteze(plosca, sosednje, prvi_korak=False)
                plosca[sos_vrs][sos_stolp].remove(-smer)
                plosca[tre_vrs][tre_stolp].remove(smer)
                if poteze_tega == []:
                    poteze.append([sosednje])
                else:
                    for x in poteze_tega:
                        poteze.append([sosednje]+x)
                
            return poteze

###### Uršin drugi poskus ki niti blizu ne more delat
######    def mozne_poteze(self, plosca, trenutno, dosedanja_pot = []):
######        kopija =[plosca[i][:] for i in range(self.visina)]
######        for mozen_korak in self.mozen_korak(kopija, trenutno):
######            mozno_polje = kopija[mozen_korak[0]][mozen_korak[1]]
######            if (len(mozno_polje)==1 or len(mozno_polje)==8 or (mozen_korak in self.gol_zgoraj|self.gol_spodaj)):
######                dosedanja_pot.append(mozen_korak)
######                smer = self.smer_koraka(trenutno, mozen_korak)
######                kopija[trenutno[0]][trenutno[1]].add(smer)
######                kopija[mozen_korak[0]][mozen_korak[1]].add(-smer)
######                cela_poteza = dosedanja_pot
######                return cela_poteza
######            else:
######                dosedanja_pot.append(mozen_korak)
######                smer = self.smer_koraka(trenutno, mozen_korak)
######                kopija[trenutno[0]][trenutno[1]].add(smer)
######                kopija[mozen_korak[0]][mozen_korak[1]].add(-smer)
######                return poteze.append(self.mozne_poteze(kopija, mozen_korak, dosedanja_pot))
            
        
##        
##    def mozne_poteze(self, plosca, staro, koraki = []):
##        poteze = []
##        (v_staro, s_staro) = staro
##        for vrstica in range(v_staro - 1, v_staro + 2):
##            for stolpec in range(s_staro - 1, s_staro + 2):
##                if vrstica == v_staro and stolpec == s_staro:
##                    pass
##                else:
##                    novo_staro = (vrstica, stolpec)
##                    print(koraki)
##                    koraki_do_zdej= koraki.append(novo_staro)
##                    kopija_plosca = [plosca[i][:] for i in range(self.visina)]
####                    for x in kopija_plosca:
####                        print (x)
##
##                    smer = self.smer_koraka(staro,novo_staro)
##                    print(smer)
##                    kopija_plosca[staro[0]][staro[1]].add(smer)
##                    kopija_plosca[novo_staro[0]][novo_staro[1]].add(-smer)
####                    for x in kopija_plosca:
####                        print (x)
##                    if (len(kopija_plosca[vrstica][stolpec]) == 1
##                        or len(kopija_plosca[vrstica][stolpec]) == 8 or
##                        novo_staro in self.gol_spodaj|self.gol_zgoraj):
##                        poteze.append(koraki)
##                        koraki_do_zdej = []
##                    else:
##                        self.mozne_poteze(kopija_plosca, novo_staro, koraki_do_zdej)
##        return poteze

        
    # kopija igre je za minimax    

    def kopija(self): 
        kopija = Igra(self.sirina, self.visina)
        kopija.plosca = [self.plosca[i][:] for i in range(self.visina)]
        kopija.na_vrsti = self.na_vrsti
        return kopija

    # za razveljavi
    def shrani_pozicijo(self):
        pozicija = [self.plosca[i][:] for i in range(self.visina)]
        self.zgodovina.append((pozicija, self.na_vrsti))

    def razveljavi(self):
        (self.plosca, self.na_vrsti) = self.zgodovina.pop()
        
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
            assert False, "Funkcija smer je v težavah."
        #print(x_razlika, y_razlika, smer)
        return smer

    def anti_smer_koraka(self, trenutno, smer):
        (vrstica, stolpec) = trenutno
        if smer == 1:
            return (vrstica-1, stolpec+1)
        if smer == 2:
            return (vrstica, stolpec+1)
        if smer == 3:
            return (vrstica+1, stolpec+1)
        if smer == 4:
            return (vrstica+1, stolpec)
        if smer == -1:
            return (vrstica+1, stolpec-1)
        if smer == -2:
            return (vrstica, stolpec-1)
        if smer == -3:
            return (vrstica-1, stolpec-1)
        if smer == -4:
            return (vrstica-1, stolpec)
        
	
    def trenutno_stanje(self, novo):
        print(novo)
        print(self.mozne_poteze(self.plosca, novo))
        #funkcija ki iz trenutnega stanja ugotovi ali je konec igre in kdo je zmagovalec/oziroma na potezi)
        if novo in self.gol_zgoraj: # seznam zgornjega gola
            return (konec_igre, igralec1) 
        elif novo in self.gol_spodaj:
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
            assert False, 'Dobimo nemogoče trenutno stanje.'

##k = Igra(5, 7)
##
##for (x,y) in [((2,3),(3,4)), ((4,3),(3,4)), ((2,3), (2,4))]:
##    k.zapomni_korak(x,y)
###print(k.plosca)
##a = k.mozne_poteze(k.plosca, (2,3))
