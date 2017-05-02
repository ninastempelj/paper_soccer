import tkinter as tk
from zakljucno_okno import *
from igra import *
from clovek import *
from racunalnik import *
import minimax
import os
import alfa_beta

clovek = "Čarovnik"
racunalnik = "Duh"

# URŠA, jst sm ugotovila, da ne vem v ker gol morm igrat, da bom zmagala :(
#NINA probej zdej :)


class GUI():
    def __init__(self, master,
                 tezavnost_igralca1, tezavnost_igralca2,
                 barva_igralec1, barva_igralec2,
                 tip_igralec1, tip_igralec2,
                 sirina, visina,
                 zacetni_meni):
        self.zacetni_meni = zacetni_meni
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno())
        #self.tezavnost1 = tezavnost_igralca1
        #self.tezavnost2 = tezavnost_igralca2
        self.barva_igralec1 = barva_igralec1
        self.barva_igralec2 = barva_igralec2
        self.tip_igralec1 = tip_igralec1
        self.tip_igralec2 = tip_igralec2
        self.trenutna_barva = self.barva_igralec1
        self.sirina = sirina
        self.visina = visina

        self.sirina_kvadratka = 50
        #self.sirina, self.visina = 9, 13 # Štejemo število oglišč (obe nujno lihi!!!)
        self.od_roba = 50
        self.debelina_zunanjih_crt = 2

        self.polje = tk.Canvas(master)
        self.polje.pack(fill='both', expand='yes')
        self.polje.bind('<Button-1>', self.klik_na_plosci)

        self.globina1 = [-1,1,2][tezavnost_igralca1]
        self.globina2 = [-1,1,2][tezavnost_igralca2]


        self.slovar_slik = {'red': ['Gryfondom','ozadje_G.gif', 'puscica_gor_G.gif', 'puscica_dol_G.gif'],
               'gold': ['Pihpuff','ozadje_P.gif', 'puscica_gor_P.gif', 'puscica_dol_P.gif'],
               'blue': ['Drznvraan','ozadje_D.gif', 'puscica_gor_D.gif', 'puscica_dol_D.gif'],
               'green': ['Spolzgad','ozadje_S.gif', 'puscica_gor_S.gif', 'puscica_dol_S.gif']}
        
        #Naredi matriko oglišč
        self.oglisca = [[(
            self.od_roba + j * self.sirina_kvadratka,
            self.od_roba + i * self.sirina_kvadratka)
                        for j in range(self.sirina)]
                        for i in range(self.visina)]
        #Nastavi ozadje:
        self.ozadje_igralca2 = tk.PhotoImage(file=os.path.join('slike',self.slovar_slik.get(self.barva_igralec2)[1]))
        self.id_ozadje_igralca2 = self.polje.create_image(self.oglisca[int((self.visina-1)/2)]
                                           [int((self.sirina-1)/2)], image=self.ozadje_igralca2)
        self.ozadje_igralca1 = tk.PhotoImage(file=os.path.join('slike',self.slovar_slik.get(self.barva_igralec1)[1]))
        self.id_ozadje_igralca1 = self.polje.create_image(self.oglisca[int((self.visina-1)/2)]
                                           [int((self.sirina-1)/2)], image=self.ozadje_igralca1)

        # RISANJE PODLAGE POLJA:
        ## Črne črte za rob igrišča
        crne_crte = [self.oglisca[1][0],self.oglisca[1][int((self.sirina-3)/2)],
                     self.oglisca[0][int((self.sirina-3)/2)],self.oglisca[0][int((self.sirina+1)/2)],
                     self.oglisca[1][int((self.sirina + 1) / 2)], self.oglisca[1][-1], self.oglisca[-2][-1],
                     self.oglisca[-2][int((self.sirina+1)/2)],self.oglisca[-1][int((self.sirina + 1) / 2)],
                     self.oglisca[-1][int((self.sirina - 3)/2)], self.oglisca[-2][int((self.sirina - 3) / 2)],
                     self.oglisca[-2][0]]

        self.id_igrisca = self.polje.create_polygon(*crne_crte, width=self.debelina_zunanjih_crt, fill='white', outline='black')

        ##Puščici
        self.puscica_dol = tk.PhotoImage(file=os.path.join('slike',self.slovar_slik.get(self.barva_igralec2)[3]))
        self.id_puscica_dol = self.polje.create_image(self.oglisca[int((self.visina-1)/2)]
                                           [int((self.sirina-1)/2)], image=self.puscica_dol)
        
        self.puscica_gor = tk.PhotoImage(file=os.path.join('slike',self.slovar_slik.get(self.barva_igralec1)[2]))
        self.id_puscica_gor = self.polje.create_image(self.oglisca[int((self.visina-1)/2)]
                                           [int((self.sirina-1)/2)], image=self.puscica_gor)



        
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


        self.igra = Igra(self.sirina, self.visina)
        #self.polozaj_zoge = self.igra.polozaj_zoge

        self.zoga = tk.PhotoImage(file=os.path.join('slike','zoga.gif'))
        self.id_zoga = self.polje.create_image(self.oglisca[self.igra.polozaj_zoge[0]]
                                           [self.igra.polozaj_zoge[1]], image=self.zoga)



    def zapri_okno(self):
        self.master.destroy()
        self.zacetni_meni.master.destroy()

    def zacni_igro(self): 
        if self.tip_igralec1 == clovek:
            self.objekt_igralec1 = Clovek(self)
        else:
            self.objekt_igralec1 = Racunalnik(self, alfa_beta.Alfabeta(self.globina1))
        if self.tip_igralec2 == clovek:
            self.objekt_igralec2 = Clovek(self)
        else:
            self.objekt_igralec2 = Racunalnik(self, alfa_beta.Alfabeta(self.globina2))
        #print(self.objekt_igralec1, self.objekt_igralec2)
        self.master.attributes("-topmost", True)
        self.objekt_igralec1.povleci_potezo()



    def najblizje_oglisce(self, x, y):
        stolpec = (x + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        vrstica = (y + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        return (int(vrstica), int(stolpec))

    def klik_na_plosci(self, event):
        novo = self.najblizje_oglisce(event.x, event.y)
        #staro = self.polozaj_zoge ##Ne potrebujemo več?
        if self.igra.na_vrsti == igralec1:
            self.objekt_igralec1.klik(novo)
        elif self.igra.na_vrsti == igralec2:
            self.objekt_igralec2.klik(novo)

    def narisi_korak(self, novo):
        (v_star, s_star) = self.igra.polozaj_zoge
        (v_nov, s_nov) = novo
        self.polje.create_line(self.oglisca[v_star][s_star],
                               self.oglisca[v_nov][s_nov], fill = self.trenutna_barva)
        self.polje.move(self.id_zoga,
                        (s_nov - s_star)*self.sirina_kvadratka,
                        (v_nov - v_star)*self.sirina_kvadratka)

    def povleci_korak(self, novo):
        staro = self.igra.polozaj_zoge
        if not self.igra.dovoljen_korak(novo):
            pass
        else:
            self.narisi_korak(novo)
            self.igra.naredi_korak(novo) #ta ga doda na seznam in posodobi zadnji polozaj
            stanje = self.igra.trenutno_stanje()
            if stanje[0] == konec_igre:
                self.koncaj_igro(stanje[1])
            elif stanje[0] == konec_poteze:
                if stanje[1] == igralec1:
                    #print("ZDEJ JE 1", self.igra.polozaj_zoge)
                    self.objekt_igralec1.povleci_potezo()
                    self.trenutna_barva =self.barva_igralec1
                    self.polje.tag_raise(self.id_puscica_gor, self.id_puscica_dol)
                    self.polje.tag_raise(self.id_ozadje_igralca1, self.id_ozadje_igralca2)
                if stanje[1] == igralec2:
                    #print("ZDEJ JE 2", self.igra.polozaj_zoge)
                    self.objekt_igralec2.povleci_potezo()
                    self.trenutna_barva =self.barva_igralec2
                    self.polje.tag_raise(self.id_puscica_dol, self.id_puscica_gor)
                    self.polje.tag_raise(self.id_ozadje_igralca2, self.id_ozadje_igralca1)
                #self.polje.config(bg=self.trenutna_barva)
            elif stanje[0] == ni_konec_poteze:
                if stanje[1] == igralec1:
                    print("GUI poklical 1. igralca")
                    self.objekt_igralec1.povleci_korak()
                if stanje[1] == igralec2:
                    print("GUI poklical 2. igralca")
                    self.objekt_igralec2.povleci_korak()
            else:
                assert False, "Stanje igre je nekaj čudnega- gui.povleci_korak."



    def koncaj_igro(self, zmagovalec):
##        domovi = {'red': 'Gryfondom',
##                'yellow': 'Pihpuff', 'blue': 'Drznvraan', 'green': 'Spolzgad'}

        if zmagovalec is None:
            izpisi =  "Izenačenje."
        elif zmagovalec == igralec1:
            izpisi = "Zmagal je {0}.".format(self.slovar_slik.get(self.barva_igralec1)[0])
        elif zmagovalec == igralec2:
            izpisi = "Zmagal je {0}.".format(self.slovar_slik.get(self.barva_igralec2)[0])

        #   Za zagon koncnega okna
        koncno_okno = tk.Toplevel()
        konec = Zakljucek(koncno_okno, izpisi, self.zacetni_meni, self)
