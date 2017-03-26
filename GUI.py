import tkinter as tk
grey = '#f0f'


class GUI:
    def __init__(self, master):
        (self.sirina, self.visina) = (9, 13)  # Štejemo število oglišč (obe nujno lihi!!!)
        self.sirina_kvadratka = 50
        self.od_roba = 50
        self.debelina_zunanjih_crt = 2

        self.polje = tk.Canvas(master)
        self.polje.pack(fill='both', expand='yes')

        self.oglisca = [[(
            self.od_roba + j * self.sirina_kvadratka,
            self.od_roba + i * self.sirina_kvadratka)
                        for j in range(self.sirina)]
                        for i in range(self.visina)]

        self.zadnji_polozaj = (self.oglisca[int((self.visina-1)/2)]
                               [int((self.sirina-1)/2)])

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

        for i in [1, -2]:
            ### Črte od roba do gola
            self.polje.create_line(self.oglisca[i][0],
                                   self.oglisca[i][int((self.sirina-3)/2)],
                                   width=self.debelina_zunanjih_crt)
            self.polje.create_line(self.oglisca[i][int((self.sirina+1)/2)],
                                   self.oglisca[i][-1],
                                   width=self.debelina_zunanjih_crt)
        for i in [0, -1]:
            ### Stranske črte
            self.polje.create_line(self.oglisca[1][i],
                                   self.oglisca[-2][i],
                                   width=self.debelina_zunanjih_crt)
            ### Zadnji stranici golov
            self.polje.create_line(self.oglisca[i][int((self.sirina - 3) / 2)],
                                   self.oglisca[i][int((self.sirina + 1) / 2)],
                                   width=self.debelina_zunanjih_crt)
        for i in [0, -2]:
            ### štange
            self.polje.create_line(self.oglisca[i][int((self.sirina-3)/2)],
                                   self.oglisca[i+1][int((self.sirina-3)/2)],
                                   width=self.debelina_zunanjih_crt)
            self.polje.create_line(self.oglisca[i][int((self.sirina+1)/2)],
                                   self.oglisca[i+1][int((self.sirina+1)/2)],
                                   width=self.debelina_zunanjih_crt)

        self.polje.bind('<Button-1>', self.narisi_korak)
                               
    def najblizje_oglisce(self, x, y):
        stolpec = (x + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        vrstica = (y + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka

        return self.oglisca[int(vrstica)][int(stolpec)]

    def narisi_korak(self, event):
        novo = self.najblizje_oglisce(event.x, event.y)
        self.polje.create_line(self.zadnji_polozaj, novo)
        self.zadnji_polozaj = novo


root = tk.Tk()

root.title("Čarovniški nogomet")

aplikacija = GUI(root)
root.geometry("{0}x{1}".format(
    (aplikacija.sirina + 1)*aplikacija.sirina_kvadratka,
    (aplikacija.visina + 1)*aplikacija.sirina_kvadratka))
# print(aplikacija.oglisca)
root.mainloop()
