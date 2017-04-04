import tkinter as tk
from zakljucno_okno import *
from igra import *


class GUI():
    def __init__(self, master, root):
        self.master = master
        self.sirina_kvadratka = 50
        #self.sirina, self.visina = 9, 13 # Štejemo število oglišč (obe nujno lihi!!!)
        self.od_roba = 50
        self.debelina_zunanjih_crt = 2
        self.zacetni_master = root

        self.polje = tk.Canvas(master)
        self.polje.pack(fill='both', expand='yes')
        self.polje.bind('<Button-1>', self.narisi_korak)

        self.igra = Igra()
        # Žoga
        self.zoga = tk.PhotoImage(file='slike/zoga.gif')
        #print(self.zadnji_polozaj)

    def narisi_polje(self):
        self.oglisca = [[(
            self.od_roba + j * self.sirina_kvadratka,
            self.od_roba + i * self.sirina_kvadratka)
                        for j in range(self.sirina)]
                        for i in range(self.visina)]

        # RISANJE PODLAGE POLJA:
        ## Sive črte znotraj igrišča
        ### Glavna mreža
        for i in range(1, self.sirina-1):  # Navpične črte
            self.polje.create_line(self.oglisca[1][i],
                                   self.oglisca[-2][i], fill='grey80')
        for i in range(2, self.visina-2):  # Vodoravne črte
            self.polje.create_line(self.oglisca[i][0],
                                   self.oglisca[i][-1], fill='grey80')
        ### Mreža znotraj golov
        for i in [1, -2]:
            self.polje.create_line(self.oglisca[i][int((self.sirina-3)/2)],
                                   self.oglisca[i][int((self.sirina+1)/2)],
                                   fill='grey80')
        for i in [0, -2]:
            self.polje.create_line(self.oglisca[i][int((self.sirina-1)/2)],
                                   self.oglisca[i+1][int((self.sirina-1)/2)],
                                   fill='grey80')

        ## Črne črte za rob igrišča

        crne_crte = [self.oglisca[1][0],self.oglisca[1][int((self.sirina-3)/2)],
                     self.oglisca[0][int((self.sirina-3)/2)],self.oglisca[0][int((self.sirina+1)/2)],
                     self.oglisca[1][int((self.sirina + 1) / 2)], self.oglisca[1][-1], self.oglisca[-2][-1],
                     self.oglisca[-2][int((self.sirina+1)/2)],self.oglisca[-1][int((self.sirina + 1) / 2)],
                     self.oglisca[-1][int((self.sirina - 3)/2)], self.oglisca[-2][int((self.sirina - 3) / 2)],
                     self.oglisca[-2][0]]

        self.polje.create_polygon(*crne_crte, width=self.debelina_zunanjih_crt, fill='', outline='black')

        # for i in [1, -2]:
        #     ### Črte od roba do gola
        #     self.polje.create_line(self.oglisca[i][0],
        #                            self.oglisca[i][int((self.sirina-3)/2)],
        #                            width=self.debelina_zunanjih_crt)
        #     self.polje.create_line(self.oglisca[i][int((self.sirina+1)/2)],
        #                            self.oglisca[i][-1],
        #                            width=self.debelina_zunanjih_crt)
        # for i in [0, -1]:
        #     ### Stranske črte
        #     self.polje.create_line(self.oglisca[1][i],
        #                            self.oglisca[-2][i],
        #                            width=self.debelina_zunanjih_crt)
        #     ### Zadnji stranici golov
        #     self.polje.create_line(self.oglisca[i][int((self.sirina - 3) / 2)],
        #                            self.oglisca[i][int((self.sirina + 1) / 2)],
        #                            width=self.debelina_zunanjih_crt)
        # for i in [0, -2]:
        #     ### štange
        #     self.polje.create_line(self.oglisca[i][int((self.sirina-3)/2)],
        #                            self.oglisca[i+1][int((self.sirina-3)/2)],
        #                            width=self.debelina_zunanjih_crt)
        #     self.polje.create_line(self.oglisca[i][int((self.sirina+1)/2)],
        #                            self.oglisca[i+1][int((self.sirina+1)/2)],
        #                            width=self.debelina_zunanjih_crt)

        self.zadnji_polozaj = (int((self.visina - 1) / 2), int((self.sirina - 1) / 2))
        self.id_zoga = self.polje.create_image(self.oglisca[self.zadnji_polozaj[0]]
                                           [self.zadnji_polozaj[1]], image=self.zoga)

    def najblizje_oglisce(self, x, y):
        stolpec = (x + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        vrstica = (y + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        
        return (int(vrstica), int(stolpec))

    def narisi_korak(self, event):
        novo = self.najblizje_oglisce(event.x, event.y)
        if self.igra.dovoljen_korak(self.zadnji_polozaj, novo):
            (v_star, s_star) = self.zadnji_polozaj
            (v_nov, s_nov) = novo
            self.polje.create_line(self.oglisca[v_star][s_star],
                                   self.oglisca[v_nov][s_nov], fill = self.trenutna_barva)
            
            self.igra.zapomni_korak(self.zadnji_polozaj, novo)
            #Premik zoge - ne znam premaknit na druge koordinate, ampak samo za določen "vektor"
            self.polje.move(self.id_zoga, #ZA butast premik žoge mava tut funcijo v igra.py ampak se pomoje ne rabi
                            # - nope, tm nima to kej delat, sm kr zbrisala
                            (novo[1] - self.zadnji_polozaj[1])*self.sirina_kvadratka,
                            (novo[0] - self.zadnji_polozaj[0])*self.sirina_kvadratka)#TODO Žoga čez črto
            
            self.zadnji_polozaj = novo
            self.stanje_igre(novo) # ta bo ali poklicala igralca, ali končala igro
            
        else:
            pass

    def stanje_igre(self, trenutno_polje):
        stanje = self.igra.trenutno_stanje(trenutno_polje)
        if stanje[0] == "konec":
            self.koncaj_igro(stanje[1])
        if stanje[0] == "ni konec":
            if stanje[1]==self.igralec1:
                self.trenutna_barva = self.barva_igralec1
            if stanje[1] == self.igralec2:
                self.trenutna_barva = self.barva_igralec2
        # vpraša igro, ali je konec0
        # če je: pokliče funkcijo self.končaj_igro()
        # če ni, more od igre izvedet kdo je na potezi
        # in spremenit po potrebi igralca
        #
        # poklicat more funkcijo self.igra.stanje_igre()
        # vrne: (KOnec/NE_konec, igralec__na_vrsti)

    def koncaj_igro(self, zmagovalec):
        domovi = {'red': 'Gryfondom',
                'yellow': 'Pihpuff', 'blue': 'Drznvraan', 'green': 'Spolzgad'}

        if zmagovalec is None:
            izpisi =  "Izenačenje."
        elif zmagovalec == self.igralec1:
            izpisi = "Zmagal je {0}.".format(domovi.get(self.barva_igralec1))
        elif zmagovalec == self.igralec2:
            izpisi = "Zmagal je {0}.".format(domovi.get(self.barva_igralec2))

        #print("Zmagovalec je {0}.".format(zmagovalec))
        #   Za zagon koncnega okna
        koncno_okno = tk.Toplevel()
        konec = Zakljucek(koncno_okno, izpisi)
        konec.zacetni = self.zacetni
        konec.zacetni_master = self.zacetni_master
        konec.gui = self
        konec.gui_master = self.master





