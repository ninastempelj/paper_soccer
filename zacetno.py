import tkinter as tk
import os
from GUI import *


class Zacetno:
    def __init__(self, master):
        self.master = master

        # privzete vrednosti, ki jih uporabnik lahko poljubno spremeni
        self.tip_igralec1 = CLOVEK
        self.tip_igralec2 = CLOVEK

        self.dovoljene_barve = ['DarkGoldenrod1', 'medium blue']
        self.barva_igralec1 = 'red3'
        self.barva_igralec2 = 'green4'

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
            file=os.path.join('slike', 'hogwarts1.gif'))

        # osnovni izgled menija:
        self.ozadje_label = tk.Label(master, image=self.slika_ozadje)
        self.ozadje_label.place(x=0, y=0, anchor='nw')

        gumb_igraj = tk.Button(master, text='Igraj',
                               command=self.zacni_igro)
        gumb_igraj.grid(row=14, column=0, columnspan=10)
        master.bind("<Return>", self.zacni_igro)


        # gumbi za tip 1. in 2. igralca:
        self.gumb_tip_1igralec = \
            tk.Button(master, text=self.tip_igralec1, command=lambda:
                      self.spremeni_tip_igralca(self.gumb_tip_1igralec), width=7)
        self.gumb_tip_1igralec.grid(row=0, column=0, columnspan=5, rowspan=3,
                                    padx=70, pady=20)

        self.gumb_tip_2igralec = \
            tk.Button(master, text=self.tip_igralec2, command=lambda:
                      self.spremeni_tip_igralca(self.gumb_tip_2igralec), width=7)
        self.gumb_tip_2igralec.grid(row=0, column=5, columnspan=5, rowspan=3,
                                    padx=70, pady=20)

        # gumbi za barve 1.igralca:
        barve_1 = tk.Label(master, text="Izberi dom:")
        barve_1.grid(row=3, column=0, columnspan=5,pady=5)

        G1 = tk.Button(master,
                       image=self.slika_gryffindor, anchor='n',
                       height=50, width=50, relief='sunken',
                       command=lambda: self.spremeni_barvo('red3', G1))
        P1 = tk.Button(master,
                       image=self.slika_hufflepuff, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo('DarkGoldenrod1', P1))
        D1 = tk.Button(master,
                       image=self.slika_ravenclaw, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo('medium blue', D1))
        S1 = tk.Button(master,
                       image=self.slika_slytherin, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo('green4', S1))

        self.gumbi_barve_igralca1 = [G1, P1, D1, S1]

        for (i, gumb) in enumerate(self.gumbi_barve_igralca1):
            gumb.grid(row=i//2+4, column=(i % 2)*2+1)

        # gumbi za barve 2.igralca:
        barve_2 = tk.Label(master, text="Izberi dom:")
        barve_2.grid(row=3, column=5, columnspan=5, pady=5)

        G2 = tk.Button(master,
                       image=self.slika_gryffindor, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo('red3', G2))
        P2 = tk.Button(master,
                       image=self.slika_hufflepuff, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo('DarkGoldenrod1', P2))
        D2 = tk.Button(master,
                       image=self.slika_ravenclaw, anchor='n',
                       height=50, width=50,
                       command=lambda: self.spremeni_barvo('medium blue', D2))
        S2 = tk.Button(master,
                       image=self.slika_slytherin, anchor='n',
                       height=50, width=50, relief='sunken',
                       command=lambda: self.spremeni_barvo('green4', S2))

        self.gumbi_barve_igralca2 = [G2, P2, D2, S2]

        for (i, gumb) in enumerate(self.gumbi_barve_igralca2):
            gumb.grid(row=i//2+4, column=(i % 2)*2 + 6)

        # gumbi za težavnost prvega igralca
        self.nastavi_tez1 = tk.Frame()
        self.nastavi_tez1.grid(row=6, column=0, columnspan=5, rowspan=4, padx=5, pady=5)

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
        self.nastavi_tez2.grid(row=6, column=5, columnspan=5, rowspan=4, padx=5, pady=5)

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
        for (i, gumb) in enumerate(self.gumbi_tezavnost_igralca1 + self.gumbi_tezavnost_igralca2):
            gumb.grid(column=i % 3, row=1)
        self.nastavi_tez1.lower(self.ozadje_label)  # Ker default igralec 1 človek
        self.nastavi_tez2.lower(self.ozadje_label)  # Ker default igralec 2 človek

        # gumbi za velikost polja
        self.nastavi_velikost = tk.Frame()
        self.nastavi_velikost.grid(row=10, column=0, columnspan=10,rowspan=4, pady=5)

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
        for gumbek in self.gumbi_velikost:
            gumbek.config(relief='raised')
        if gumb == self.malo_igrisce:
            self.sirina = 7
            self.visina = 11
        elif gumb == self.srednje_igrisce:
            self.sirina = 9
            self.visina = 13
        elif gumb == self.veliko_igrisce:
            self.sirina = 11
            self.visina = 15
        gumb.config(relief='groove')

    def spremeni_tip_igralca(self, gumb):
        """Ob kliku uporabnika spremeni tip igralca (človek/računalnik)."""
        if gumb == self.gumb_tip_1igralec:
            tip = self.tip_igralec1
            if tip == CLOVEK:
                self.tip_igralec1 = RACUNALNIK
                self.nastavi_tez1.lift(self.ozadje_label)
            elif tip == RACUNALNIK:
                self.tip_igralec1 = CLOVEK
                self.nastavi_tez1.lower(self.ozadje_label)
            self.gumb_tip_1igralec.config(text=self.tip_igralec1)
        if gumb == self.gumb_tip_2igralec:
            tip = self.tip_igralec2
            if tip == CLOVEK:
                self.tip_igralec2 = RACUNALNIK
                self.nastavi_tez2.lift(self.ozadje_label)
            elif tip == RACUNALNIK:
                self.tip_igralec2 = CLOVEK
                self.nastavi_tez2.lower(self.ozadje_label)
            self.gumb_tip_2igralec.config(text=self.tip_igralec2)

    def spremeni_barvo(self, barva, gumb):
        """Ob kliku uporabnika spremeni barvo igralca."""
        if barva in self.dovoljene_barve:
            self.dovoljene_barve.remove(barva)
            if gumb in self.gumbi_barve_igralca1:
                self.dovoljene_barve.append(self.barva_igralec1)
                self.barva_igralec1 = barva
                for gumbek in self.gumbi_barve_igralca1:
                    gumbek.config(relief='raised')
            if gumb in self.gumbi_barve_igralca2:
                self.dovoljene_barve.append(self.barva_igralec2)
                self.barva_igralec2 = barva
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

    def zacni_igro(self, event=None):
        """Požene novo igro z izbranimi nastavitvami."""
        okno_igrisca = tk.Toplevel()
        gui = GUI(okno_igrisca,
                  self.tezavnost_igralca1, self.tezavnost_igralca2,
                  self.barva_igralec1, self.barva_igralec2,
                  self.tip_igralec1, self.tip_igralec2,
                  self.sirina, self.visina, self)
        self.master.withdraw()
        okno_igrisca.geometry("{0}x{1}".format(
            (self.sirina + 1) * gui.sirina_kvadratka,
            (self.visina + 1) * gui.sirina_kvadratka))
        gui.zacni_igro()

     


app_zacetno_okno = tk.Tk()

app_zacetno_okno.title("Čarovniški nogomet")
app_zacetno_okno.geometry("450x450")

zacetni_meni = Zacetno(app_zacetno_okno)

app_zacetno_okno.mainloop()
