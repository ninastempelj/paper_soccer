import logging
import random
from igra import nasprotnik, IGRALEC1, IGRALEC2, KONEC_IGRE

# Vrednosti igre
ZMAGA = 100000  
NESKONCNO = ZMAGA + 1  # Več kot zmaga


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
        self.prekinitev = False  # Glavno vlakno bo to nastavilo na True, če moramo nehati
        self.jaz = self.igra.na_vrsti
        self.poteza = None  # Sem napišemo potezo, ko jo najdemo
        # Poženemo alfabeta
        (poteza, vrednost) = self.alfabeta(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            self.poteza = poteza

    def pametna_cenilka(self):
        """Ocena vrednosti pozicije: pogleda kako blizu gola smo."""
        (tren_vrs, tren_stolp) = self.igra.polozaj_zoge
        oddaljen_od_vertikale = abs(tren_stolp - ((self.igra.sirina - 1) / 2))
        oddaljen_od_horizontale = ((self.igra.visina - 1) / 2 - tren_vrs)
        if self.jaz == IGRALEC1:
            return 1000*oddaljen_od_horizontale - 100*oddaljen_od_vertikale
        if self.jaz == IGRALEC2:
            return -1000*oddaljen_od_horizontale - 100*oddaljen_od_vertikale

    def neumna_cenilka(self):
        """Vsem potezam priredi enako vrednost, razen, če je konec igre."""
        (konec_ali_ne, na_vrsti) = self.igra.trenutno_stanje()
        if konec_ali_ne == KONEC_IGRE:
            # Igre je konec, vrnemo njeno vrednost
            if na_vrsti == self.jaz:
                return ZMAGA
            elif na_vrsti == nasprotnik(self.jaz):
                return -ZMAGA
            elif na_vrsti is None:
                return -ZMAGA + 1  # remi
        else:
            return 3  # naključno izbrana vrednost, važno da je za vse enaka

    def alfabeta(self, globina, maksimiziramo, alfa=-NESKONCNO, beta=NESKONCNO):
        """Glavna metoda alfabeta."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug("Alfabeta prekinja, globina = {0}".format(globina))
            return None, 0
        (konec_ali_ne, na_vrsti) = self.igra.trenutno_stanje()
        if konec_ali_ne == KONEC_IGRE:
            # Igre je konec, vrnemo njeno vrednost
            if na_vrsti == self.jaz:
                return None, ZMAGA
            elif na_vrsti == nasprotnik(self.jaz):
                return None, -ZMAGA
            elif na_vrsti is None:
                return None, -ZMAGA + 1  # remi
            else:
                assert False, 'stanje_igre vrne čudnega igralca, alfabeta'
        elif konec_ali_ne != KONEC_IGRE:
            # Igre ni konec
            if globina == -1:
                # v primeru, da imamo nastavljeno najlažjo težavnost
                # računalnik naredi en korak alfabeta z neumno cenilko:
                najboljsa_poteza = None
                vrednost_najboljse = -NESKONCNO
                for p in self.uredi_poteze(self.igra.mozne_poteze(),
                                           maksimiziramo):
                    poteza = [self.igra.polozaj_zoge] + p
                    self.igra.naredi_potezo(poteza)
                    vrednost = self.neumna_cenilka()
                    self.igra.razveljavi_potezo(poteza)
                    if vrednost > vrednost_najboljse:
                        vrednost_najboljse = vrednost
                        najboljsa_poteza = poteza
                assert (najboljsa_poteza is not None), \
                    "alfabeta: izračunana poteza je None"
                return najboljsa_poteza, vrednost_najboljse
            elif globina == 0:
                # print("konec rekurzije, globina 0")
                return None, self.pametna_cenilka()
            else:
                # Naredimo eno stopnjo alfabeta
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -NESKONCNO
                    for p in self.uredi_poteze(self.igra.mozne_poteze(),
                                               maksimiziramo):
                        poteza = [self.igra.polozaj_zoge] + p
                        self.igra.naredi_potezo(poteza)
                        vrednost = self.alfabeta(
                            globina - 1, not maksimiziramo, alfa, beta)[1]
                        self.igra.razveljavi_potezo(poteza)
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = poteza
                        alfa = max(alfa, vrednost_najboljse)
                        if beta <= alfa:
                            break

                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = NESKONCNO
                    for p in self.uredi_poteze(self.igra.mozne_poteze(),
                                               maksimiziramo):
                        poteza = [self.igra.polozaj_zoge] + p
                        self.igra.naredi_potezo(poteza)
                        vrednost = self.alfabeta(
                            globina - 1, not maksimiziramo, alfa, beta)[1]
                        self.igra.razveljavi_potezo(poteza)
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = poteza
                        beta = min(beta, vrednost_najboljse)
                        if beta <= alfa:
                            break

                assert (najboljsa_poteza is not None), \
                    "alfabeta: izračunana poteza je None"
                return najboljsa_poteza, vrednost_najboljse
        else:
            assert False, "alfabeta: ni vrnil cele poteze, ampak korak"

    def uredi_poteze(self, poteze, maksimiziramo):
        """Funkcija uredi možne poteze, da so na začetku tiste,
           kjer gre prvi korak v smeri našega gola,
           dobre poteze še premeša, da dobimo naključnost."""
        (tren_vrst, _) = self.igra.polozaj_zoge
        dobre_poteze = []
        ostale_poteze = []
        # "dobra" smer je odvisna od igralca, ki računa možne poteze.
        if ((self.jaz == IGRALEC1 and maksimiziramo) or
                (self.jaz == IGRALEC2 and not maksimiziramo)):
            for poteza in poteze:
                nova_vrst = poteza[0][0]
                if nova_vrst < tren_vrst:
                    dobre_poteze.append(poteza)
                elif nova_vrst == tren_vrst:
                    ostale_poteze = [poteza] + ostale_poteze
                elif nova_vrst > tren_vrst:
                    ostale_poteze.append(poteza)
        else:
            for poteza in poteze:
                nova_vrst = poteza[0][0]
                if nova_vrst > tren_vrst:
                    dobre_poteze.append(poteza)
                elif nova_vrst == tren_vrst:
                    ostale_poteze = [poteza] + ostale_poteze
                elif nova_vrst < tren_vrst:
                        ostale_poteze.append(poteza)
        random.shuffle(dobre_poteze)
        return dobre_poteze + ostale_poteze
