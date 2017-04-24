import logging

from igra import nasprotnik, igralec1, igralec2, konec_igre, konec_poteze, ni_konec_poteze

class Minimax:
    def __init__(self, globina, staro):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False # ali moramo končati?
        self.igra = None # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None # sem napišemo potezo, ko jo najdemo
        self.trenutni_polozaj = staro

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        """Izračunaj potezo za trenutno stanje dane igre."""
        # To metodo pokličemo iz vzporednega vlakna
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastvilo na True, če moramo nehati
        self.jaz = self.igra.na_vrsti
        #print(igra.na_vrsti)
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednosti igre
    ZMAGA = 100000 # Mora biti vsaj 10^5
    NESKONCNO = ZMAGA + 1 # Več kot zmaga

    def vrednost_pozicije(self):
        """Ocena vrednosti pozicije: sešteje vrednosti vseh trojk na plošči."""
        # Slovar, ki pove, koliko so vredne posamezne trojke, kjer "(x,y) : v" pomeni:
        # če imamo v trojki x znakov igralca in y znakov nasprotnika (in 3-x-y praznih polj),
        # potem je taka trojka za self.jaz vredna v.
##        # Trojke, ki se ne pojavljajo v slovarju, so vredne 0.
##        vrednost_trojke = {
##            (3,0) : Minimax.ZMAGA,
##            (0,3) : -Minimax.ZMAGA//10,
##            (2,0) : Minimax.ZMAGA//100,
##            (0,2) : -Minimax.ZMAGA//1000,
##            (1,0) : Minimax.ZMAGA//10000,
##            (0,1) : -Minimax.ZMAGA//100000
##        }
##        vrednost = 0
##        for t in self.igra.trojke:
##            x = 0
##            y = 0
##            for (i,j) in t:
##                if self.igra.plosca[i][j] == self.jaz:
##                    x += 1
##                elif self.igra.plosca[i][j] == nasprotnik(self.jaz):
##                    y += 1
##            vrednost += vrednost_trojke.get((x,y), 0)
        return 3

    def minimax(self, globina, maksimiziramo):
        # XXX: "trenutni_polozaj" ne sme biti argument, ker je (bo) spravljen v self.igra
        #print("printamo potezo", self.poteza)
        trenutni_polozaj = self.igra.zadnji_polozaj
        """Glavna metoda minimax."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        print(self.igra.zadnji_polozaj, self.igra.na_vrsti)
        (konec_ali_ne, na_vrsti) = self.igra.trenutno_stanje()
        if konec_ali_ne == konec_igre:
            # Igre je konec, vrnemo njeno vrednost
            if na_vrsti == self.jaz:
                return (None, Minimax.ZMAGA)
            elif na_vrsti == nasprotnik(self.jaz):
                return (None, -Minimax.ZMAGA)
            elif na_vrsti == None:
                return (None, 0) # remi
            else:
                assert False, 'stanje_igre vrne čudnega igralca, minimax'
        elif konec_ali_ne != konec_igre:
            # Igre ni konec
            if globina == 0:
                #print("konec rekurzije, globina 0")
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    #print("maksi")
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    #print(self.igra.mozne_poteze(trenutni_polozaj))
                    for p in self.igra.mozne_poteze():
                        #print(p)
                        poteza = [self.igra.zadnji_polozaj] + p
                        #self.igra.shrani_pozicijo()
                        #print("minimaks vleče potezo", poteza, self.igra.zadnji_polozaj)
                        self.igra.naredi_potezo(poteza)
                        
                        # XXX to for zanko preselimo v metodo naredi_potezo v Igra.
                        # YYY preseljeno
                        # self.igra.naredi_potezo(p)
                        # XXX ne pozabi spremeniti spodaj pri minimizaciji!
                        # YYY nismo pozabili pri minimizaciji
##                        for i in range(len(poteza)-1):
##                            self.igra.zapomni_korak(poteza[i], poteza[i+1])
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        #print(poteza)
                        self.igra.razveljavi_potezo(poteza)
                        #print("maksi", self.igra.zadnji_polozaj, trenutni_polozaj)
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = poteza
                else:
                    # Minimiziramo
                    #print("mini")
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for p in self.igra.mozne_poteze():
                        poteza = [self.igra.zadnji_polozaj] + p
                        #self.igra.shrani_pozicijo()
                        #print("minimaks vleče potezo", poteza, self.igra.zadnji_polozaj)
                        self.igra.naredi_potezo(poteza)
##                        for i in range(len(poteza)-1):
##                            self.igra.zapomni_korak(poteza[i], poteza[i+1])
                        vrednost = self.minimax(globina-1, maksimiziramo)[1]
                        self.igra.razveljavi_potezo(poteza)
                        #print("mini", self.igra.zadnji_polozaj, trenutni_polozaj)
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = poteza

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: ni vrnil cele poteze, ampak korak"
