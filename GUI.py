import tkinter as tk
import os
from zakljucno_okno import *
from igra import *
from clovek import *
from racunalnik import *
# import minimax
import alfa_beta

CLOVEK = "Čarovnik"
RACUNALNIK = "Duh"


class GUI:
    def __init__(self, master,
                 tezavnost_igralca1, tezavnost_igralca2,
                 barva_igralec1, barva_igralec2,
                 tip_igralec1, tip_igralec2,
                 sirina, visina,
                 zacetni_meni):
        self.zacetni_meni = zacetni_meni
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno())

        self.globina1 = tezavnost_igralca1
        self.globina2 = tezavnost_igralca2
        self.tip_igralec1 = tip_igralec1
        self.tip_igralec2 = tip_igralec2
        self.barva_igralec1 = barva_igralec1
        self.barva_igralec2 = barva_igralec2
        self.trenutna_barva = self.barva_igralec1
        self.sirina = sirina
        self.visina = visina
        # Igralca se ustvarita ob zagonu igre - glej začni_igro
        self.objekt_igralec1 = None
        self.objekt_igralec2 = None
        self.igra = Igra(self.sirina, self.visina)
        self.zgodovina = []  # za razveljavi, ki ga igra uporabnik

        
        # Meni
        glavni_menu = tk.Menu(master)
        master.config(menu=glavni_menu) #ustvari glavni meni
        
        moznosti = tk.Menu(glavni_menu, tearoff=0)#ustvari prvi zavihek menija
        glavni_menu.add_cascade(label="Možnosti", menu=moznosti)
        moznosti.add_command(label="Začni znova", command=self.ponovi_igro)
        moznosti.add_command(label="Spremeni nastavitve", command=self.zacni_novo_igro)
        moznosti.add_command(label="Razveljavi zadnji korak", command=self.igra.razveljavi_korak)

        # Naredimo polje
        self.sirina_kvadratka = 50
        self.od_roba = 50
        self.debelina_zunanjih_crt = 2

        self.polje = tk.Canvas(master)
        self.polje.pack(fill='both', expand='yes')
        self.polje.bind('<Button-1>', self.klik_na_plosci)

        # Naredi matriko koordinat oglišč
        self.oglisca = [[(self.od_roba + j * self.sirina_kvadratka,
                          self.od_roba + i * self.sirina_kvadratka)
                        for j in range(self.sirina)]
                        for i in range(self.visina)]

        self.slovar_slik = {'red': ['Gryfondom', 'ozadje_G.gif', 'puscica_gor_G.gif', 'puscica_dol_G.gif'],
                            'gold': ['Pihpuff', 'ozadje_P.gif', 'puscica_gor_P.gif', 'puscica_dol_P.gif'],
                            'blue': ['Drznvraan', 'ozadje_D.gif', 'puscica_gor_D.gif', 'puscica_dol_D.gif'],
                            'green': ['Spolzgad', 'ozadje_S.gif', 'puscica_gor_S.gif', 'puscica_dol_S.gif']}

        # Nastavi ozadje:
##        self.polje.bind("<Configure>", self.spremeni_velikost_ozadja) ##rabi preveč pomnilnika
##        self.visina_slike = (self.visina+2)*self.sirina_kvadratka
##        self.sirina_slike = (self.sirina+2)*self.sirina_kvadratka
        self.ozadje_igralca2 = tk.PhotoImage(file=os.path.join('slike', self.slovar_slik.get(self.barva_igralec2)[1]))
        self.id_ozadje_igralca2 = self.polje.create_image(self.oglisca[int((self.visina-1)/2)]
                                                          [int((self.sirina-1)/2)], image=self.ozadje_igralca2)
        self.ozadje_igralca1 = tk.PhotoImage(file=os.path.join('slike', self.slovar_slik.get(self.barva_igralec1)[1]))
        self.id_ozadje_igralca1 = self.polje.create_image(self.oglisca[int((self.visina-1)/2)]
                                                          [int((self.sirina-1)/2)], image=self.ozadje_igralca1)

        # RISANJE PODLAGE POLJA:
        ## Črne črte za rob igrišča
        crne_crte = [self.oglisca[1][0], self.oglisca[1][int((self.sirina-3)/2)],
                     self.oglisca[0][int((self.sirina-3)/2)], self.oglisca[0][int((self.sirina+1)/2)],
                     self.oglisca[1][int((self.sirina + 1) / 2)], self.oglisca[1][-1], self.oglisca[-2][-1],
                     self.oglisca[-2][int((self.sirina+1)/2)], self.oglisca[-1][int((self.sirina + 1) / 2)],
                     self.oglisca[-1][int((self.sirina - 3)/2)], self.oglisca[-2][int((self.sirina - 3) / 2)],
                     self.oglisca[-2][0]]

        self.id_igrisca = self.polje.create_polygon(
            *crne_crte, width=self.debelina_zunanjih_crt, fill='white', outline='black')

        ## Puščici
        self.puscica_dol = tk.PhotoImage(file=os.path.join(
            'slike', self.slovar_slik.get(self.barva_igralec2)[3]))
        self.id_puscica_dol = \
            self.polje.create_image(self.oglisca[int((self.visina-1)/2)]
                                    [int((self.sirina-1)/2)], image=self.puscica_dol)
        
        self.puscica_gor = tk.PhotoImage(file=os.path.join(
            'slike', self.slovar_slik.get(self.barva_igralec1)[2]))
        self.id_puscica_gor = \
            self.polje.create_image(self.oglisca[int((self.visina-1)/2)]
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

        # žogo ustvarimo šele tukaj, da je nad črtami in igriščem
        self.zoga = tk.PhotoImage(file=os.path.join('slike', 'zoga.gif'))
        self.id_zoga = self.polje.create_image(self.oglisca[self.igra.polozaj_zoge[0]]
                                               [self.igra.polozaj_zoge[1]], image=self.zoga)

    def zapri_okno(self):
        """Zapre vsa okna igrice."""
        self.master.destroy()
        self.zacetni_meni.master.destroy()

    def zacni_igro(self):
        """Ustvari igralce in pozove prvega naj naredi potezo. Kliče jo zacetno.py"""
        if self.tip_igralec1 == CLOVEK:
            self.objekt_igralec1 = Clovek(self)
        else:
            self.objekt_igralec1 = Racunalnik(self, alfa_beta.Alfabeta(self.globina1))
        if self.tip_igralec2 == CLOVEK:
            self.objekt_igralec2 = Clovek(self)
        else:
            self.objekt_igralec2 = Racunalnik(self, alfa_beta.Alfabeta(self.globina2))
        #print(self.objekt_igralec1, self.objekt_igralec2)
        self.master.attributes("-topmost", True)
        self.objekt_igralec1.povleci_potezo()

    def najblizje_oglisce(self, x, y):
        """Poišče oglišče najbližje kliku na plošči."""
        stolpec = (x + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        vrstica = (y + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        return int(vrstica), int(stolpec)

    def klik_na_plosci(self, event):
        """Ob kliku pove igralcu, da je uporabnik kliknil na neko oglišče.
        Računalnik ta poziv ignorira, človek pa naredi potezo.
        """
        novo = self.najblizje_oglisce(event.x, event.y)
        if self.igra.na_vrsti == IGRALEC1:
            self.objekt_igralec1.klik(novo)
        elif self.igra.na_vrsti == IGRALEC2:
            self.objekt_igralec2.klik(novo)

    def narisi_korak(self, novo):
        """Na igrišču izrišemo potezo od položaja žoge do novo."""
        (v_star, s_star) = self.igra.polozaj_zoge
        (v_nov, s_nov) = novo
        crta = self.polje.create_line(self.oglisca[v_star][s_star],
                               self.oglisca[v_nov][s_nov],
                               fill=self.trenutna_barva,
                               width=2)
        self.polje.move(self.id_zoga,
                        (s_nov - s_star)*self.sirina_kvadratka,
                        (v_nov - v_star)*self.sirina_kvadratka)

    def povleci_korak(self, novo):
        """Če gre za dovoljeno potezo, jo izriše in pokliče naslednjega igralca,
        ali sproži konec igre."""
        if not self.igra.dovoljen_korak(novo):
            pass
        else:
            self.narisi_korak(novo)
            # Sporočimo igri, da je bil korak sprejet:
            self.igra.naredi_korak(novo)
            # Preverimo, kdo je naslednji na vrsti:
            stanje = self.igra.trenutno_stanje()
            if stanje[0] == KONEC_IGRE:
                self.koncaj_igro(stanje[1])
            elif stanje[0] == KONEC_POTEZE:
                # pokličemo drugega igralca, uskladimo vse barve in smeri...
                if stanje[1] == IGRALEC1:
                    #print("ZDEJ JE 1", self.igra.polozaj_zoge)
                    self.objekt_igralec1.povleci_potezo()
                    self.nastavi_igralca()
                if stanje[1] == IGRALEC2:
                    #print("ZDEJ JE 2", self.igra.polozaj_zoge)
                    self.objekt_igralec2.povleci_potezo()
                    self.nastavi_igralca()
            elif stanje[0] == NI_KONEC_POTEZE:
                # pokličemo istega igralca za nov korak
                if stanje[1] == IGRALEC1:
                    #print("GUI poklical 1. igralca")
                    self.objekt_igralec1.povleci_korak()
                if stanje[1] == IGRALEC2:
                    #print("GUI poklical 2. igralca")
                    self.objekt_igralec2.povleci_korak()
            else:
                assert False, "Stanje igre je nekaj čudnega- gui.povleci_korak."

    def nastavi_igralca(self):
        """Preveri, kdo je na vrsti in nastavi ustrezna ozadja in trenutno barvo."""
        na_vrsti = self.igra.na_vrsti
        if na_vrsti == IGRALEC1:
            self.trenutna_barva = self.barva_igralec1
            self.polje.tag_raise(self.id_puscica_gor, self.id_puscica_dol)
            self.polje.tag_raise(self.id_ozadje_igralca1, self.id_ozadje_igralca2)
        if na_vrsti == IGRALEC2:
            self.trenutna_barva = self.barva_igralec2
            self.polje.tag_raise(self.id_puscica_dol, self.id_puscica_gor)
            self.polje.tag_raise(self.id_ozadje_igralca2, self.id_ozadje_igralca1)

##    def spremeni_velikost_ozadja(self, event):
##        sirina_nova = int(event.height/10)
##        visina_nova = int(event.width/10)
##        sirina_stara = int(self.sirina_slike/10)
##        visina_stara = int(self.visina_slike/10)
##        
##        self.ozadje_igralca1.zoom(sirina_nova, visina_nova)
##        self.ozadje_igralca1.subsample(sirina_stara, visina_stara)
##        
##        self.visina_slike = event.height
##        self.sirina_slike = event.width
##        
        

    def koncaj_igro(self, zmagovalec):
        """Pripravi napis za zaključno okno in ga odpre."""
        if zmagovalec is None:
            izpisi = "Izenačenje."
        elif zmagovalec == IGRALEC1:
            izpisi = "Zmagal je {0}.".format(self.slovar_slik.get(self.barva_igralec1)[0])
        elif zmagovalec == IGRALEC2:
            izpisi = "Zmagal je {0}.".format(self.slovar_slik.get(self.barva_igralec2)[0])
        else:
            assert False, "Igra se je čudno končala - GUI.koncaj_igro"
        # Za zagon koncnega okna
        koncno_okno = tk.Toplevel()
        Zakljucek(koncno_okno, izpisi, self.zacetni_meni, self)

    def zacni_novo_igro(self):
        """Ponovno odpre začetni meni."""
        self.zacetni_meni.master.deiconify()
        self.master.destroy()

    def ponovi_igro(self):
        """Narišemo čisto polje, igramo še enkrat z istimi nastavitvami."""
        self.master.destroy()
        self.zacetni_meni.zacni_igro()



        
        
