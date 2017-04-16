# XXX TU SMO POZABILI KOPIRATI MNOŽICE, KI SO SPRAVLJENE V TABELI
# TAKOLE NAREDIMO:
#
# import copy
# plosca_tega = copy.deepcopy(plosca)
#


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
        self.zadnji_polozaj = (int((self.visina - 1) / 2), int((self.sirina - 1) / 2))
        # XXX Zakaj stanje igre ne vsebuje podatka o tem, kje je žoga?
        # YYY sedaj ga vsebuje igra, GUI pa ne- GUI vedno vpraša igro

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

    def dovoljen_korak(self, novo):
        staro = self.zadnji_polozaj
        smer = self.smer_koraka(staro,novo)
        if smer == None:
            return False
        elif smer in self.plosca[staro[0]][staro[1]]:
            return False
        else:
            return True

    def mozen_korak(self):
        trenutno = self.zadnji_polozaj
        mozni = []
        for smer in self.smeri:
            if smer in self.plosca[trenutno[0]][trenutno[1]]:
                pass
            else:
                mozni.append(self.anti_smer_koraka(smer))
        # print(mozni)
        return mozni

    def mozne_poteze(self, prvi_korak=True):
        # XXX tu se bomo znenbili trenutno, ker bo že v self.
        # YYY smo se znebili trenutno
        trenutno = self.zadnji_polozaj
        mozni = self.mozen_korak()
        if (mozni == [] or
                (not prvi_korak and len(mozni) == 7) or
                trenutno in self.gol_spodaj|self.gol_zgoraj):
            return []

        else:
            poteze = []
            for sosednje in mozni:
                (sos_vrs, sos_stolp) = sosednje
                (tre_vrs, tre_stolp) = trenutno
                # XXX naslednje tri vrstice bi morale biti metoda naredi_korak
##                smer = self.smer_koraka(trenutno, sosednje)
##                self.plosca[sos_vrs][sos_stolp].add(-smer)
##                self.plosca[tre_vrs][tre_stolp].add(smer)
                self.naredi_korak(sosednje)
                poteze_tega = self.mozne_poteze(prvi_korak=False)
                # XXX naslednji dve vrstici bi morali biti metoda razveljavi_korak
##                self.plosca[sos_vrs][sos_stolp].remove(-smer)
##                self.plosca[tre_vrs][tre_stolp].remove(smer)
                self.razveljavi_korak(trenutno)
                if poteze_tega == []:
                    poteze.append([sosednje])
                else:
                    for x in poteze_tega:
                        poteze.append([sosednje]+x)

            return poteze


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

    def naredi_korak(self, novo):
        staro = self.zadnji_polozaj
        smer = self.smer_koraka(staro,novo)
        self.plosca[staro[0]][staro[1]].add(smer)
        self.plosca[novo[0]][novo[1]].add(-smer)
        self.zadnji_polozaj = novo
        #print(smer)

    def naredi_potezo(self, poteza):
        del poteza[0] #ker ima poteza na začetku trenutno stanje(rabi za razveljavi)
        for korak in poteza: 
            self.naredi_korak(korak)

    ###ali razveljavi korak dobi smer ali polje v katerega more nazaj?!
    ### Odločiva se za eno od funkcij ampak sem spisala obe za vsak slučaj

##    #razveljavi korak s podano smerjo 
##    def razveljavi_korak2(self, smer):
##        (trenutno_vrs, trenutno_stolp) = self.zadnji_polozaj
##        (prejsno_vrs, prejsno_stolp) = self.anti_smer_koraka(-smer)
##        self.plosca[trenutno_vrs][trenutno_stolp].remove(-smer)
##        self.plosca[prejsno_vrs][prejsno_stolp].remove(smer)
##        self.zadnji_polozaj = (prejsno_vrs, prejsno_stolp)

    #razveljavi korak s podanim prejšnim poljem
    def razveljavi_korak(self, staro):
        (trenutno_vrs, trenutno_stolp) = self.zadnji_polozaj
        (prejsno_vrs, prejsno_stolp) = staro
        smer = self.smer_koraka(staro, self.zadnji_polozaj)
        self.plosca[trenutno_vrs][trenutno_stolp].remove(-smer)
        self.plosca[prejsno_vrs][prejsno_stolp].remove(smer)
        self.zadnji_polozaj = (prejsno_vrs, prejsno_stolp)

##     def razveljavi_potezo(self, poteza):
##         obrnjena_poteza = poteza[::-1] #NUJNO ZAČETNO POLJE V POTEZI
##         del obrnjena_poteza[0] #izbriše trenutno stanje iz poteze,
##         #da ne briše poteze iz samega sebe v samega sebe
##         for korak in obrnjena_poteza:
##             self.razveljavi_korak(korak)
##
             
    def razveljavi_potezo(self, poteza):
        obrnjena_poteza = poteza[::-1]
        #NUJNO začetno polje na začetku potezi, da konča v prejšnem zadnjem_položaju
        del obrnjena_poteza[0] #da na začetku ne briše poteze samega sebe v samega sebe
        for korak in obrnjena_poteza:
            self.razveljavi_korak(korak)

        
        

    # XXX ali bo minimax potreboval naredi_potezo?

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

    def anti_smer_koraka(self, smer):
        (vrstica, stolpec) = self.zadnji_polozaj
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


    def trenutno_stanje(self):
        print(self.mozne_poteze())
        novo = self.zadnji_polozaj
        #print(novo)
        #print(self.mozne_poteze(self.plosca, novo))
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
