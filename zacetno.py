import tkinter as tk
import os
from GUI import *
import navodila


class Zacetno:
    def __init__(self, master):
        self.master = master

        # privzete vrednosti, ki jih uporabnik lahko poljubno spremeni
        self.tip_igralca1 = CLOVEK
        self.tip_igralca2 = CLOVEK

        self.dovoljene_barve = [RUMENA, MODRA]
        self.barva_igralca1 = RDECA
        self.barva_igralca2 = ZELENA

        self.tezavnost_igralca1 = -1
        self.tezavnost_igralca2 = -1

        self.sirina = 9
        self.visina = 13

        # uvažanje slik:
        self.slika_gryffindor = tk.PhotoImage(
            file=os.path.join('slike', 'gryffindor.gif'))
        self.slika_hufflepuff = tk.PhotoImage(
            file=os.path.join('slike', 'hufflepuff.gif'))
        self.slika_ravenclaw = tk.PhotoImage(
            file=os.path.join('slike', 'ravenclaw.gif'))
        self.slika_slytherin = tk.PhotoImage(
            file=os.path.join('slike', 'slytherin.gif'))
        self.slika_ozadje = tk.PhotoImage(
            file=os.path.join('slike', 'hogwarts.gif'))

        # osnovni izgled menija:
        self.ozadje_label = tk.Label(master, image=self.slika_ozadje)
        self.ozadje_label.place(x=0, y=0, anchor='nw')

        gumb_igraj = tk.Button(master, text='Igraj',
                               command=self.zacni_igro)
        gumb_igraj.grid(row=14, column=0, columnspan=10)
        master.bind("<Return>", self.zacni_igro)

        gumb_pomoc = tk.Button(master, text='?',
                               command=self.pokazi_navodila)
        gumb_pomoc.grid(row=15, column=7, columnspan=3)


        # gumbi za tip 1. in 2. igralca:
        self.gumb_tip_igralca1 = \
            tk.Button(master, text=self.tip_igralca1, width=7, command=lambda:
                      self.spremeni_tip_igralca(self.gumb_tip_igralca1))
        self.gumb_tip_igralca1.grid(row=0, column=0, columnspan=5, rowspan=3,
                                    padx=70, pady=20)

        self.gumb_tip_igralca2 = \
            tk.Button(master, text=self.tip_igralca2, width=7, command=lambda:
                      self.spremeni_tip_igralca(self.gumb_tip_igralca2))
        self.gumb_tip_igralca2.grid(row=0, column=5, columnspan=5, rowspan=3,
                                    padx=70, pady=20)

        # gumbi za barve 1.igralca:
        barve_1 = tk.Label(master, text="Izberi dom:")
        barve_1.grid(row=3, column=0, columnspan=5, pady=5)

        G1 = tk.Button(master, image=self.slika_gryffindor, anchor='n',
                       height=50, width=50, relief='sunken',
                       command=lambda: self.spremeni_barvo(RDECA, G1))
        P1 = tk.Button(master, image=self.slika_hufflepuff, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo(RUMENA, P1))
        D1 = tk.Button(master, image=self.slika_ravenclaw, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo(MODRA, D1))
        S1 = tk.Button(master, image=self.slika_slytherin, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo(ZELENA, S1))

        self.gumbi_barve_igralca1 = [G1, P1, D1, S1]

        for (i, gumb) in enumerate(self.gumbi_barve_igralca1):
            gumb.grid(row=i//2+4, column=(i % 2)*2+1)

        # gumbi za barve 2.igralca:
        barve_2 = tk.Label(master, text="Izberi dom:")
        barve_2.grid(row=3, column=5, columnspan=5, pady=5)

        G2 = tk.Button(master, image=self.slika_gryffindor, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo(RDECA, G2))
        P2 = tk.Button(master, image=self.slika_hufflepuff, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo(RUMENA, P2))
        D2 = tk.Button(master, image=self.slika_ravenclaw, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo(MODRA, D2))
        S2 = tk.Button(master, image=self.slika_slytherin, anchor='n',
                       height=50, width=50, relief='sunken',
                       command=lambda: self.spremeni_barvo(ZELENA, S2))

        self.gumbi_barve_igralca2 = [G2, P2, D2, S2]

        for (i, gumb) in enumerate(self.gumbi_barve_igralca2):
            gumb.grid(row=i//2+4, column=(i % 2)*2 + 6)

        # gumbi za težavnost prvega igralca
        self.nastavi_tez1 = tk.Frame()
        self.nastavi_tez1.grid(row=6, column=0, columnspan=5,
                               rowspan=4, padx=5, pady=5)

        tez1 = tk.Label(self.nastavi_tez1, text="Izberi težavnost:")
        tez1.grid(column=1, row=0)

        lahko1 = tk.Button(self.nastavi_tez1, text="Shamer",  relief='groove',
                           command=lambda: self.spremeni_tezavnost(-1, lahko1))
        tezje1 = tk.Button(self.nastavi_tez1, text="Smottan",
                           command=lambda: self.spremeni_tezavnost(1, tezje1))
        tezko1 = tk.Button(self.nastavi_tez1, text="Wulf",
                           command=lambda: self.spremeni_tezavnost(2, tezko1))
        self.gumbi_tezavnost_igralca1 = [lahko1, tezje1, tezko1]

        # gumbi za težavnost drugega igralca
        self.nastavi_tez2 = tk.Frame()
        self.nastavi_tez2.grid(row=6, column=5, columnspan=5,
                               rowspan=4, padx=5, pady=5)

        tez2 = tk.Label(self.nastavi_tez2, text="Izberi težavnost:")
        tez2.grid(column=1, row=0)

        lahko2 = tk.Button(self.nastavi_tez2, text="Shamer",  relief='groove',
                           command=lambda: self.spremeni_tezavnost(-1, lahko2))
        tezje2 = tk.Button(self.nastavi_tez2, text="Smottan",
                           command=lambda: self.spremeni_tezavnost(1, tezje2))
        tezko2 = tk.Button(self.nastavi_tez2, text="Wulf",
                           command=lambda: self.spremeni_tezavnost(2, tezko2))
        self.gumbi_tezavnost_igralca2 = [lahko2, tezje2, tezko2]

        # izrišemo vse gumbe za težavnost:
        for (i, gumb) in enumerate(self.gumbi_tezavnost_igralca1
                                   + self.gumbi_tezavnost_igralca2):
            gumb.grid(column=i % 3, row=1)
        self.nastavi_tez1.lower(self.ozadje_label)  # Ker default igralec 1 človek
        self.nastavi_tez2.lower(self.ozadje_label)  # Ker default igralec 2 človek

        # gumbi za velikost polja
        self.nastavi_velikost = tk.Frame()
        self.nastavi_velikost.grid(row=10, column=0, columnspan=10, rowspan=4, pady=5)

        velikost_napis = tk.Label(self.nastavi_velikost, text="Izberi velikost igrišča:")
        velikost_napis.grid(column=1, row=0)

        self.malo_igrisce = \
            tk.Button(self.nastavi_velikost, text="Harry",
                      command=lambda: self.spremeni_velikost(self.malo_igrisce))
        self.srednje_igrisce = \
            tk.Button(self.nastavi_velikost, text="Hagrid",  relief='groove',
                      command=lambda: self.spremeni_velikost(self.srednje_igrisce))
        self.veliko_igrisce = \
            tk.Button(self.nastavi_velikost, text="Grop",
                      command=lambda: self.spremeni_velikost(self.veliko_igrisce))
        self.gumbi_velikost = [self.malo_igrisce,
                               self.srednje_igrisce,
                               self.veliko_igrisce]

        # izrišemo vse gumbe za velikost:
        for (i, gumb) in enumerate(self.gumbi_velikost):
            gumb.grid(column=i % 3, row=1)
            
    def spremeni_velikost(self, gumb):
        """Ob kliku uporabnika spremeni velikost igrišča."""
        velikost = self.gumbi_velikost.index(gumb)  # = 0, 1, 2
        for gumbek in self.gumbi_velikost:
            gumbek.config(relief='raised')
        self.sirina = 7 + 2*velikost
        self.visina = 11 + 2*velikost
        gumb.config(relief='groove')

    def spremeni_tip_igralca(self, gumb):
        """Ob kliku uporabnika spremeni tip igralca (človek/računalnik)."""
        if gumb == self.gumb_tip_igralca1:
            tip = self.tip_igralca1
            if tip == CLOVEK:
                self.tip_igralca1 = RACUNALNIK
                self.nastavi_tez1.lift(self.ozadje_label)
            elif tip == RACUNALNIK:
                self.tip_igralca1 = CLOVEK
                self.nastavi_tez1.lower(self.ozadje_label)
            self.gumb_tip_igralca1.config(text=self.tip_igralca1)
        if gumb == self.gumb_tip_igralca2:
            tip = self.tip_igralca2
            if tip == CLOVEK:
                self.tip_igralca2 = RACUNALNIK
                self.nastavi_tez2.lift(self.ozadje_label)
            elif tip == RACUNALNIK:
                self.tip_igralca2 = CLOVEK
                self.nastavi_tez2.lower(self.ozadje_label)
            self.gumb_tip_igralca2.config(text=self.tip_igralca2)

    def spremeni_barvo(self, barva, gumb):
        """Ob kliku uporabnika spremeni barvo igralca."""
        if barva in self.dovoljene_barve:
            self.dovoljene_barve.remove(barva)
            if gumb in self.gumbi_barve_igralca1:
                self.dovoljene_barve.append(self.barva_igralca1)
                self.barva_igralca1 = barva
                for gumbek in self.gumbi_barve_igralca1:
                    gumbek.config(relief='raised')
            if gumb in self.gumbi_barve_igralca2:
                self.dovoljene_barve.append(self.barva_igralca2)
                self.barva_igralca2 = barva
                for gumbek in self.gumbi_barve_igralca2:
                    gumbek.config(relief='raised')
            gumb.config(relief='sunken')
        else:
            # v tem primeru je uporabnik izbral za oba nasprotnika enako barvo
            pass

    def spremeni_tezavnost(self, tezavnost, trenutni_gumb):
        """Ob kliku uporabnika spremeni težavnost igre (če igra računalnik)."""
        if trenutni_gumb in self.gumbi_tezavnost_igralca1:
            self.tezavnost_igralca1 = tezavnost
            for gumbek in self.gumbi_tezavnost_igralca1:
                gumbek.config(relief='raised')
        if trenutni_gumb in self.gumbi_tezavnost_igralca2:
            self.tezavnost_igralca2 = tezavnost
            for gumbek in self.gumbi_tezavnost_igralca2:
                gumbek.config(relief='raised')
        trenutni_gumb.config(relief='groove')

    def pokazi_navodila(self):
        """Odpremo okno z navodili za igro."""
        okno_navodil = tk.Toplevel()
        navodila.Navodila(okno_navodil)

    def zacni_igro(self, event=None):
        """Požene novo igro z izbranimi nastavitvami."""
        okno_igrisca = tk.Toplevel()
        gui = GUI(okno_igrisca,
                  self.tezavnost_igralca1, self.tezavnost_igralca2,
                  self.barva_igralca1, self.barva_igralca2,
                  self.tip_igralca1, self.tip_igralca2,
                  self.sirina, self.visina, self)
        self.master.withdraw()
        okno_igrisca.geometry("{0}x{1}".format(
            self.sirina*gui.sirina_kvadratka + gui.od_roba,
            self.visina*gui.sirina_kvadratka + gui.od_roba))
        gui.zacni_igro()


app_zacetno_okno = tk.Tk()

app_zacetno_okno.title("Čarovniški nogomet")
app_zacetno_okno.geometry("450x450")

zacetni_meni = Zacetno(app_zacetno_okno)

app_zacetno_okno.mainloop()
