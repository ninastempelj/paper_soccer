import tkinter as tk
from zakljucno_okno import *
from igra import *
from clovek import *
from racunalnik import *


clovek = "Čarovnik"
racunalnik = "Duh"

# URŠA, jst sm ugotovila, da ne vem v ker gol morm igrat, da bom zmagala :(


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
        self.polje.bind('<Button-1>', self.klik_na_plosci)


    def zacni_igro(self):
        #Nastavi barvo ozadja
        self.polje.config(bg=self.trenutna_barva)
        #Naredi matriko oglišč
        self.oglisca = [[(
            self.od_roba + j * self.sirina_kvadratka,
            self.od_roba + i * self.sirina_kvadratka)
                        for j in range(self.sirina)]
                        for i in range(self.visina)]

        # RISANJE PODLAGE POLJA:
        ## Črne črte za rob igrišča
        crne_crte = [self.oglisca[1][0],self.oglisca[1][int((self.sirina-3)/2)],
                     self.oglisca[0][int((self.sirina-3)/2)],self.oglisca[0][int((self.sirina+1)/2)],
                     self.oglisca[1][int((self.sirina + 1) / 2)], self.oglisca[1][-1], self.oglisca[-2][-1],
                     self.oglisca[-2][int((self.sirina+1)/2)],self.oglisca[-1][int((self.sirina + 1) / 2)],
                     self.oglisca[-1][int((self.sirina - 3)/2)], self.oglisca[-2][int((self.sirina - 3) / 2)],
                     self.oglisca[-2][0]]

        self.polje.create_polygon(*crne_crte, width=self.debelina_zunanjih_crt, fill='white', outline='black')

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

        self.zoga = tk.PhotoImage(file='slike/zoga.gif')
        self.id_zoga = self.polje.create_image(self.oglisca[self.zadnji_polozaj[0]]
                                           [self.zadnji_polozaj[1]], image=self.zoga)
        self.igra = Igra(self.sirina, self.visina)
		
        if self.tip_igralec1 == clovek:
            self.objekt_igralec1 = Clovek(self)
        else:
            self.objekt_igralec1 = Racunalnik(self)
        if self.tip_igralec1 == clovek:
            self.objekt_igralec2 = Clovek(self)
        else:
            self.objekt_igralec2 = Racunalnik(self)
            
    
    def najblizje_oglisce(self, x, y):
        stolpec = (x + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        vrstica = (y + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        
        return (int(vrstica), int(stolpec))

    def klik_na_plosci(self, event):
        novo = self.najblizje_oglisce(event.x, event.y)
        staro = self.zadnji_polozaj
        if self.igra.na_vrsti == igralec1:
            self.objekt_igralec1.klik(staro, novo)
        elif self.igra.na_vrsti == igralec2:
            self.objekt_igralec2.klik(staro, novo)
    
    def narisi_korak(self, novo):
        (v_star, s_star) = self.zadnji_polozaj
        (v_nov, s_nov) = novo
        self.polje.create_line(self.oglisca[v_star][s_star],
                               self.oglisca[v_nov][s_nov], fill = self.trenutna_barva)
        self.polje.move(self.id_zoga,
                        (s_nov - s_star)*self.sirina_kvadratka,
                        (v_nov - v_star)*self.sirina_kvadratka)#TODO Žoga čez črto
                    # ej ne javlja več napak izven polja :)
    def povleci_korak(self, staro, novo):
        if not self.igra.dovoljen_korak(staro, novo):
            pass
        else:
            self.igra.zapomni_korak(staro, novo) #ta ga doda na seznam
            self.narisi_korak(novo)
            self.zadnji_polozaj = novo
            stanje = self.igra.trenutno_stanje(novo)
            if stanje[0] == konec_igre:
                self.koncaj_igro(stanje[1])
            elif stanje[0] == konec_poteze:
                if stanje[1] == igralec1:
                    self.objekt_igralec1.povleci_potezo(self.zadnji_polozaj)
                    self.trenutna_barva =self.barva_igralec1
                if stanje[1] == igralec2:
                    self.objekt_igralec2.povleci_potezo(self.zadnji_polozaj)
                    self.trenutna_barva =self.barva_igralec2
                self.polje.config(bg=self.trenutna_barva)
            elif stanje[0] == ni_konec_poteze:
                if stanje[1] == igralec1:
                    self.objekt_igralec1.povleci_korak()
                if stanje[1] == igralec2:
                    self.objekt_igralec2.povleci_korak()
            else:
                assert False, "Stanje igre je nekaj čudnega- gui.povleci_korak."
        

            

    # def preveri_korak(self, novo):
            # staro = self.zadnji_polozaj
            # if self.igra.dovoljen_korak(staro, novo):
                    # self.igra.zapomni_korak(staro, novo)
                    # #Premik zoge - ne znam premaknit na druge koordinate, ampak samo za določen "vektor"
                    # self.polje.move(self.id_zoga, #ZA butast premik žoge mava tut funcijo v igra.py ampak se pomoje ne rabi
                                                    # # - nope, tm nima to kej delat, sm kr zbrisala
                                                    # (novo[1] - staro[1])*self.sirina_kvadratka,
                                                    # (novo[0] - staro[0])*self.sirina_kvadratka)#TODO Žoga čez črto
                    

                    # self.stanje_igre(novo) # ta bo ali poklicala igralca, ali končala igro
##            
##            else:
##                    pass

    def stanje_igre(self, trenutno_polje):
        stanje = self.igra.trenutno_stanje(trenutno_polje)
        if stanje[0] == konec_igre:
            self.koncaj_igro(stanje[1])
        elif stanje[0] == konec_poteze:
            if stanje[1] == igralec1:
                self.trenutna_barva = self.barva_igralec1
                #pokliče igralca 1 za novo potezo
            if stanje[1] == igralec2:
                self.trenutna_barva = self.barva_igralec2
                #pokliče igralca 2 za novo potezo
        #v končni verziji tega ne bi smelo bit,
        # ker korake podelata igralca sama: - DELA
##        elif  stanje[0] == ni_konec_poteze:
##            if stanje[1] == igralec1:
##                #pokliče igralca 1 za nov korak
##                pass
##            if stanje[1] == igralec2:
##                #pokliče igralca 2 za nov korak
##                pass
##        else:
##            assert False, 'Čudno stanje igre - GUI'
                
    def koncaj_igro(self, zmagovalec):
        domovi = {'red': 'Gryfondom',
                'yellow': 'Pihpuff', 'blue': 'Drznvraan', 'green': 'Spolzgad'}

        if zmagovalec is None:
            izpisi =  "Izenačenje."
        elif zmagovalec == igralec1:
            izpisi = "Zmagal je {0}.".format(domovi.get(self.barva_igralec1))
        elif zmagovalec == igralec2:
            izpisi = "Zmagal je {0}.".format(domovi.get(self.barva_igralec2))

        #print("Zmagovalec je {0}.".format(zmagovalec))
        #   Za zagon koncnega okna
        koncno_okno = tk.Toplevel()
        konec = Zakljucek(koncno_okno, izpisi)
        konec.zacetni = self.zacetni
        konec.zacetni_master = self.zacetni_master
        konec.gui = self
        konec.gui_master = self.master





