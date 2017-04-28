import logging
import time
import random
from igra import nasprotnik, igralec1, igralec2, konec_igre, konec_poteze, ni_konec_poteze


class Alfabeta:
    def __init__(self, globina):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False  # ali moramo končati?
        self.igra = None  # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None  # sem napišemo potezo, ko jo najdemo

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        """Izračunaj potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False  # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_vrsti
        # print(igra.na_vrsti)
        self.poteza = None  # Sem napišemo potezo, ko jo najdemo
        # Poženemo alfabeta
        start = time.time()
        (poteza, vrednost) = self.alfabeta(self.globina, True)
        end = time.time()
        print("alfabeta", end-start)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("alfabeta: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza
            print("shranili smo potezo", self.poteza)


    # Vrednosti igre
    ZMAGA = 100000  # Mora biti vsaj 10^5
    NESKONCNO = ZMAGA + 1  # Več kot zmaga

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije: sešteje vrednosti vseh trojk na plošči."""
        (tren_vrs, tren_stolp) = self.igra.polozaj_zoge
        oddaljenost_od_vertikale = abs(tren_stolp - ((self.igra.sirina - 1) / 2))
        oddaljenost_od_horizontale = ((self.igra.visina - 1) / 2 - tren_vrs)
        # print(self.igra.polozaj_zoge, self.igra.plosca[tren_vrs][tren_stolp])
        if self.jaz == igralec1:
            return 1000 * oddaljenost_od_horizontale - 100 * oddaljenost_od_vertikale
        if self.jaz == igralec2:
            return -(1000 * oddaljenost_od_horizontale)  # - 100*oddaljenost_od_vertikale

    def alfabeta(self, globina, maksimiziramo, alfa=-NESKONCNO, beta=NESKONCNO):
        #trenutni_polozaj = self.igra.polozaj_zoge
        """Glavna metoda alfabeta."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug("Alfabeta prekinja, globina = {0}".format(globina))
            return (None, 0)
        # print(self.igra.polozaj_zoge, self.igra.na_vrsti)
        (konec_ali_ne, na_vrsti) = self.igra.trenutno_stanje()
        print("na začetku alfabeta na vrsti je ", self.igra.na_vrsti)
        if konec_ali_ne == konec_igre:
            # Igre je konec, vrnemo njeno vrednost
            if na_vrsti == self.jaz:
                return (None, Alfabeta.ZMAGA)
            elif na_vrsti == nasprotnik(self.jaz):
                return (None, -Alfabeta.ZMAGA)
            elif na_vrsti == None:
                return (None, -Alfabeta.ZMAGA + 1)  # remi
            else:
                assert False, 'stanje_igre vrne čudnega igralca, alfabeta'
        elif konec_ali_ne != konec_igre:
            # Igre ni konec
            if globina == -1: #v primeru, da imamo nastavljeno najlažjo težavnost
                #  računalnik izbere naključno pozezo
                print("v alfabeta: na vrsti je ", self.igra.na_vrsti)
                mozne = self.igra.mozne_poteze()
                self.uredi_poteze(mozne,maksimiziramo)
                return [self.igra.polozaj_zoge]+ self.uredi_poteze(mozne,maksimiziramo)[0], 1
            if globina == 0:
                # print("konec rekurzije, globina 0")
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo alfabeta
                if maksimiziramo:
                    # print("maksi")
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Alfabeta.NESKONCNO
                    # print(len(self.igra.mozne_poteze()))
                    for p in self.uredi_poteze(self.igra.mozne_poteze(), maksimiziramo):
                        poteza = [self.igra.polozaj_zoge] + p
                        # self.igra.shrani_pozicijo()
                        # print("alfabeta vleče potezo", poteza, self.igra.polozaj_zoge)
                        self.igra.naredi_potezo(poteza)
                        vrednost = self.alfabeta(globina - 1, not maksimiziramo, alfa, beta)[1]
                        # print(poteza)
                        self.igra.razveljavi_potezo(poteza)
                        # print("maksi", self.igra.polozaj_zoge, trenutni_polozaj)
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = poteza
                        alfa = max(alfa, vrednost_najboljse)
                        if beta <= alfa:
                            break

                else:
                    # print("maksi")
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Alfabeta.NESKONCNO
                    # print(len(self.igra.mozne_poteze()))
                    for p in self.uredi_poteze(self.igra.mozne_poteze(), maksimiziramo):
                        #print(p)
                        poteza = [self.igra.polozaj_zoge] + p
                        # self.igra.shrani_pozicijo()
                        # print("alfabeta vleče potezo", poteza, self.igra.polozaj_zoge)
                        self.igra.naredi_potezo(poteza)
                        vrednost = self.alfabeta(globina - 1, maksimiziramo, alfa, beta)[1]
                        # print(poteza)
                        self.igra.razveljavi_potezo(poteza)
                        # print("maksi", self.igra.polozaj_zoge, trenutni_polozaj)
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = poteza
                        beta = min(beta, vrednost_najboljse)
                        if beta <= alfa:
                            break


                assert (najboljsa_poteza is not None), "alfabeta: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "alfabeta: ni vrnil cele poteze, ampak korak"

    def uredi_poteze(self, poteze, maksimiziramo):
        """Funkcija uredi možne poteze, da so na začetku tiste, kjer gre prvi korak v smeri našega gola"""

        (tren_vrst, _) = self.igra.polozaj_zoge
        dobre_poteze = []
        ostale_poteze = []

        if ((self.jaz == igralec1 and maksimiziramo) or
                (self.jaz == igralec2 and not maksimiziramo)):
            for poteza in poteze:
                nova_vrst = poteza[0][0]
                if nova_vrst < tren_vrst:
                    dobre_poteze.append(poteza)
                elif nova_vrst == tren_vrst:
                    ostale_poteze = [poteza] + ostale_poteze
                elif nova_vrst > tren_vrst:
                    ostale_poteze.append(poteza)
                # mora končati do tukaj

        else:
            for poteza in poteze:
                nova_vrst = poteza[0][0]
                if nova_vrst > tren_vrst:
                    dobre_poteze.append(poteza)
                elif nova_vrst == tren_vrst:
                    ostale_poteze = [poteza] + ostale_poteze
                elif nova_vrst < tren_vrst:
                        ostale_poteze.append(poteza)
                    # mora končati do tukaj
        random.shuffle(dobre_poteze)
        return dobre_poteze + ostale_poteze
