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
        return mozni

    def mozne_poteze(self, prvi_korak=True):
        """Funkcija poišče del možnih potez - ko pride poteza v polje, kjer
        je že bila izvedena kakšna poteza, neha pregledovati tisto možnost.
        """
        mozni = self.mozen_korak()
        if (mozni == [] or
                (not prvi_korak and len(mozni) == 7) or
                self.polozaj_zoge in (self.gol_spodaj | self.gol_zgoraj)):
            return []

        else:
            trenutno = self.polozaj_zoge
            poteze = []
            # ker so poteze, ki jih bomo našli odvisne od vrstnega
            # reda pregledovanja korakov, bomo te premešali
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
            
    def razveljavi_potezo(self, poteza):
        """Razveljavi vse korake v potezi"""
        # Poteza se vedno začenja s trenutnim položajem
        obrnjena_poteza = poteza[::-1]
        for korak in obrnjena_poteza[1:]:
            self.razveljavi_korak(korak)
        self.na_vrsti = nasprotnik(self.na_vrsti)

    def smer_koraka(self, staro, novo):
        """Vrne smer, v kateri je narejen korak med podanima
        poljema. (Vrstni red je pomemben)"""
        x_razlika = staro[1] - novo[1]
        y_razlika = staro[0] - novo[0]
        if abs(x_razlika) > 1 or abs(y_razlika) > 1 or (
                        x_razlika == 0 and y_razlika == 0):
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
        return smer

    def anti_smer_koraka(self, smer):
        """Vrne nam polje v smeri iz trenutnega položaja žoge."""
        (vrstica, stolpec) = self.polozaj_zoge
        if smer in [1, -1]:
            nova_vrstica = int(vrstica - smer)
            nov_stolpec = int(stolpec + smer)
        elif smer in [2, -2]:
            nova_vrstica = vrstica
            nov_stolpec = int(stolpec + smer/2)
        elif smer in [3, -3]:
            nova_vrstica = int(vrstica + smer/3)
            nov_stolpec = int(stolpec + smer/3)
        elif smer in [4, -4]:
            nova_vrstica = int(vrstica + smer/4)
            nov_stolpec = stolpec
        else:
            assert False, "Kakšno smer je dobila anti_smer?"
        return nova_vrstica, nov_stolpec

            
    def trenutno_stanje(self):
        """Iz trenutnega stanja ugotovi ali je konec igre
        in kdo je zmagovalec ali na potezi."""
        novo = self.polozaj_zoge
        if novo in self.gol_zgoraj:
            self.na_vrsti = nasprotnik(self.na_vrsti)
            return KONEC_IGRE, IGRALEC1
        elif novo in self.gol_spodaj:
            self.na_vrsti = nasprotnik(self.na_vrsti)
            return KONEC_IGRE, IGRALEC2
        elif len(self.plosca[novo[0]][novo[1]]) == 8:
            self.na_vrsti = None
            return KONEC_IGRE, None
        # Poteze je konec, ko pridemo v polje ki ima
        # vrisano le smer tega prihoda - ima dolžino 1:
        elif len(self.plosca[novo[0]][novo[1]]) != 1:
            return NI_KONEC_POTEZE, self.na_vrsti
        elif len(self.plosca[novo[0]][novo[1]]) == 1:
            self.na_vrsti = nasprotnik(self.na_vrsti)
            return KONEC_POTEZE, self.na_vrsti
        else:
            assert False, 'Dobimo nemogoče trenutno stanje.'
