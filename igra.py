import copy
import random

IGRALEC1 = 'prvi igralec'
IGRALEC2 = 'drugi igralec'
KONEC_IGRE = 'konec igre'
KONEC_POTEZE = 'konec poteze'
NI_KONEC_POTEZE = 'ni konec poteze'


def nasprotnik(oseba):
    if oseba == IGRALEC1:
        return IGRALEC2
    elif oseba == IGRALEC2:
        return IGRALEC1
    elif oseba is None:
        pass
    else:
        assert False, 'Funkcija nasprotnik je dobila nekaj čudnega.'


class Igra:
    def __init__(self, sirina, visina):

        self.na_vrsti = IGRALEC1

        self.sirina = sirina

        self.visina = visina
        self.plosca = [[set() for _ in range(self.sirina)]
                       for _ in range(self.visina)]
        self.smeri = list(range(-4, 0)) + list(range(1, 5))
        self.polozaj_zoge = (int((self.visina - 1) / 2), int((self.sirina - 1) / 2))

        # V vsako polje plošče dodamo morebitne že zasedene smeri - gre za rob.
        # Neproblematična so robna polja, ki niso del gola
        neproblematicne = (list(range(int((self.sirina-1)/2-1)))
                           + list(range(int((self.sirina-1)/2+2), self.sirina)))

        for i in neproblematicne:
            self.plosca[0][i] |= {-4, -3, -2, -1, 1, 2, 3, 4}
            self.plosca[-1][i] |= {-4, -3, -2, -1, 1, 2, 3, 4}
            self.plosca[1][i] |= {-3, -4, 1, -2, 2}
            self.plosca[-2][i] |= {-1, 4, 3, 2, -2}
        for i in range(1, self.visina):
            self.plosca[i][0] |= {-3, -2, -1, 4, -4}
            self.plosca[i][-1] |= {1, 2, 3, -4, 4}

        # Dodamo še polja v zgornji gol:
        self.plosca[0][int((self.sirina-1)/2 - 1)] |= {4, -1, -2, -3, -4, 1, 2}
        self.plosca[0][int((self.sirina-1)/2)] |= {-2, -3, -4, 1, 2}
        self.plosca[0][int((self.sirina-1)/2 + 1)] |= {-2, -3, -4, 1, 2, 3, 4}
        self.plosca[1][int((self.sirina-1)/2 - 1)] |= {-2, -3, -4}
        self.plosca[1][int((self.sirina-1)/2 + 1)] |= {-4, 1, 2}

        # in spodnji gol:
        self.plosca[-1][int((self.sirina-1)/2 - 1)] |= {2, 3, 4, -1, -2, -3, -4}
        self.plosca[-1][int((self.sirina-1)/2)] |= {-2, 2, 3, 4, -1}
        self.plosca[-1][int((self.sirina-1)/2 + 1)] |= {-4, 1, 2, 3, 4, -1, -2}
        self.plosca[-2][int((self.sirina-1)/2 - 1)] |= {4, -1, -2}
        self.plosca[-2][int((self.sirina-1)/2 + 1)] |= {2, 3, 4}

        # TODO: razveljavi uporabnika
        self.zgodovina = []  # za razveljavi, ki ga igra uporabnik

        # za potrebe preverjanja stanja igre si shranimo polja v golu:
        self.gol_zgoraj = {(0, int((self.sirina-1)/2)),
                           (0, int((self.sirina-1)/2 + 1)),
                           (0, int((self.sirina-1)/2 - 1))}
        self.gol_spodaj = {(self.visina-1, int((self.sirina-1)/2)),
                           (self.visina-1, int((self.sirina-1)/2 + 1)),
                           (self.visina-1, int((self.sirina-1)/2 - 1))}

    def dovoljen_korak(self, novo):
        """Preveri, ali je možen korak v podano polje."""
        staro = self.polozaj_zoge
        smer = self.smer_koraka(staro, novo)
        if smer is None:
            return False
        elif smer in self.plosca[staro[0]][staro[1]]:
            return False
        else:
            return True

    def mozen_korak(self):
        """Vrne seznam polj v katera lahko gremo z enim korakom."""
        mozni = []
        for smer in self.smeri:
            if smer in self.plosca[self.polozaj_zoge[0]][self.polozaj_zoge[1]]:
                pass
            else:
                mozni.append(self.anti_smer_koraka(smer))
        # print(mozni)
        return mozni

    def mozne_poteze2(self, prvi_korak=True):
        """Funkcija vrne seznam vseh možnih potez.
        Poteza = seznam polj po katerih se premikamo, prvo je trenutno polje."""
        mozni = self.mozen_korak()
        if (mozni == [] or
                (not prvi_korak and len(mozni) == 7) or  # potezo vedno začnemo v polju z le eno smerjo.
                self.polozaj_zoge in (self.gol_spodaj | self.gol_zgoraj)):
            return []

        else:
            trenutno = self.polozaj_zoge
            poteze = []
            for sosednje in mozni:
                self.naredi_korak(sosednje)
                poteze_tega = self.mozne_poteze(prvi_korak=False)
                self.razveljavi_korak(trenutno)
                if poteze_tega == []:
                    poteze.append([sosednje])
                else:
                    for x in poteze_tega:
                        poteze.append([sosednje]+x)
            return poteze

    def mozne_poteze(self, prvi_korak=True):
        """Funkcija poišče del možnih potez - ko pride poteza v polje, kjer
        je že bila izvedena kakšna poteza, neha pregledovati tisto možnost.
        """
        #print("Računam možne poteze")
        mozni = self.mozen_korak()
        if (mozni == [] or
                (not prvi_korak and len(mozni) == 7) or
                self.polozaj_zoge in (self.gol_spodaj | self.gol_zgoraj)):
            return []

        else:
            trenutno = self.polozaj_zoge
            poteze = []
            # ker so poteze, ki jih bomo našli odvisne od vrstnega reda pregledovanja korakov, bomo te premešali
            random.shuffle(mozni)
            for sosednje in mozni:
                ze_preverjen = False
                for p in poteze:
                    if sosednje in p:
                        ze_preverjen = True
                        break
                if ze_preverjen:
                    continue
                self.naredi_korak(sosednje)
                poteze_tega = self.mozne_poteze(prvi_korak=False)
                self.razveljavi_korak(trenutno)
                if poteze_tega == []:
                    poteze.append([sosednje])
                else:
                    for x in poteze_tega:
                        poteze.append([sosednje] + x)
            return poteze

    def kopija(self):
        """Vrne pravo kopijo igre (za minimax/alfabeta rezanje)"""
        kopija = Igra(self.sirina, self.visina)
        kopija.plosca = copy.deepcopy(self.plosca)
        kopija.na_vrsti = self.na_vrsti
        kopija.polozaj_zoge = self.polozaj_zoge
        return kopija

    def shrani_pozicijo(self):
        """V seznam zgodovine doda trenutno stanje igre, da bo uporabnik lahko razveljavil potezo."""
        pozicija = copy.deepcopy(self.plosca)
        self.zgodovina.append((pozicija, self.na_vrsti))

    def razveljavi_uporabnik(self):
        """Razveljavi za uporabnika - vrne ga nazaj za morebitno potezo računalnika in en svoj korak."""
        (self.plosca, self.na_vrsti) = self.zgodovina.pop()

    def naredi_korak(self, novo):
        """V ploščo na trenutno in novo polje doda smer zadnjega koraka.
        Zamenja položaj žoge!!!
        """
        staro = self.polozaj_zoge
        smer = self.smer_koraka(staro, novo)
        if smer is None:
            print("igra.naredi_korak", staro, novo)
        self.plosca[staro[0]][staro[1]].add(smer)
        self.plosca[novo[0]][novo[1]].add(-smer)
        self.polozaj_zoge = novo
        #print(smer)

    def naredi_potezo(self, poteza):
        """Naredi vse korake v potezi."""
        for korak in poteza[1:]:
            self.naredi_korak(korak)

    def razveljavi_korak(self, staro):
        """Vrne žogo v stari položaj in odstrani ustrezne smeri."""
        (trenutno_vrs, trenutno_stolp) = self.polozaj_zoge
        (prejsno_vrs, prejsno_stolp) = staro
        smer = self.smer_koraka(staro, self.polozaj_zoge)
        self.plosca[trenutno_vrs][trenutno_stolp].remove(-smer)
        self.plosca[prejsno_vrs][prejsno_stolp].remove(smer)
        self.polozaj_zoge = (prejsno_vrs, prejsno_stolp)
        #print("zadnji položaj v razveljavi korak", self.polozaj_zoge)
            
    def razveljavi_potezo(self, poteza):
        """Razveljavi vse korake v potezi"""
        # Poteza se mora vedno začenjati s trenutnim položajem (kjerkoli jo sestavljamo)
        obrnjena_poteza = poteza[::-1]
        for korak in obrnjena_poteza[1:]:
            self.razveljavi_korak(korak)
        self.na_vrsti = nasprotnik(self.na_vrsti)

    def smer_koraka(self, staro, novo):
        """Vrne smer, v kateri je narejen korak med podanima poljema. (Vrstni red je pomemben)"""
        x_razlika = staro[1] - novo[1]
        y_razlika = staro[0] - novo[0]
        if abs(x_razlika) > 1 or abs(y_razlika) > 1 or (
                        x_razlika == 0 and y_razlika == 0):
            #print("smer koraka", staro, novo)
            return None
        elif x_razlika == 0:
            smer = (-4)*y_razlika
        elif y_razlika == 0:
            smer = (-2)*x_razlika
        elif x_razlika == y_razlika:
            smer = (-3)*x_razlika
        elif x_razlika != y_razlika:
            smer = (-1)*x_razlika
        else:
            assert False, "Funkcija smer je v težavah."
        #print(x_razlika, y_razlika, smer)
        return smer

    def anti_smer_koraka(self, smer):
        """Vrne nam polje v smeri iz trenutnega položaja žoge."""
        (vrstica, stolpec) = self.polozaj_zoge
        # TODO: A se da to kej skrajšat?
        if smer == 1:
            return vrstica-1, stolpec+1
        if smer == 2:
            return vrstica, stolpec+1
        if smer == 3:
            return vrstica+1, stolpec+1
        if smer == 4:
            return vrstica+1, stolpec
        if smer == -1:
            return vrstica+1, stolpec-1
        if smer == -2:
            return vrstica, stolpec-1
        if smer == -3:
            return vrstica-1, stolpec-1
        if smer == -4:
            return vrstica-1, stolpec

    def trenutno_stanje(self):
        """funkcija ki iz trenutnega stanja ugotovi ali je konec igre in kdo je zmagovalec/oziroma na potezi"""
        novo = self.polozaj_zoge
        #print("v trenutn stanje: na vrsti je ", self.na_vrsti)
        if novo in self.gol_zgoraj:
            self.na_vrsti = nasprotnik(self.na_vrsti)
            return KONEC_IGRE, IGRALEC1
        elif novo in self.gol_spodaj:
            self.na_vrsti = nasprotnik(self.na_vrsti)
            return KONEC_IGRE, IGRALEC2
        elif len(self.plosca[novo[0]][novo[1]]) == 8:
            #print("remi v trenutno_stanje")
            self.na_vrsti = None
            return KONEC_IGRE, None
        # Poteze je konec, ko pridemo v polje ki ima vrisano le smer tega prihoda - ima dolžino 1:
        elif len(self.plosca[novo[0]][novo[1]]) != 1:
            return NI_KONEC_POTEZE, self.na_vrsti
        elif len(self.plosca[novo[0]][novo[1]]) == 1:
            self.na_vrsti = nasprotnik(self.na_vrsti)
            return KONEC_POTEZE, self.na_vrsti
        else:
            assert False, 'Dobimo nemogoče trenutno stanje.'
