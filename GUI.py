import tkinter as tk
from zakljucno_okno import *
#import igra


class GUI():
    def __init__(self, master, root):
        self.master = master
        self.sirina_kvadratka = 50
        self.sirina, self.visina = 9, 13 # Štejemo število oglišč (obe nujno lihi!!!)
        self.od_roba = 50
        self.debelina_zunanjih_crt = 2
        self.zacetni = root
        master.geometry("{0}x{1}".format(
            (self.sirina + 1)*self.sirina_kvadratka,
            (self.visina + 1)*self.sirina_kvadratka))
        # self.tezavnost1, self.tezavnost2,
        # self.barva_igralec1, self.barva_igralec2  NASTAVLJENO V ZAČETNI!!!
        # self.igralec1, self.igralec2

        self.oglisca = [[(
            self.od_roba + j * self.sirina_kvadratka,
            self.od_roba + i * self.sirina_kvadratka)
                        for j in range(self.sirina)]
                        for i in range(self.visina)]

        self.zadnji_polozaj = (self.oglisca[int((self.visina-1)/2)]
                               [int((self.sirina-1)/2)])

        self.igralec1 = None
        self.igralec2 = None

        self.polje = tk.Canvas(master)
        self.polje.pack(fill='both', expand='yes')
        self.polje.bind('<Button-1>', self.narisi_korak)
        
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

        
    #Spremenljivke na začetnem polju
        self.napis_gumb1 = tk.StringVar()
        self.napis_gumb1.set("Čarovnik")
        self.napis_gumb2 = tk.StringVar()
        self.napis_gumb2.set("Duh")


    

            
    def narisi_zacetno(self, master):
        self.polje.delete(tk.ALL)
        
        naslov = tk.Label(master, text = "Čarovniški nogomet")
        naslov.grid(row=0, column=0)
        gumb1 = tk.Button(master, text = self.napis_gumb1.get(),
                          command=self.spremeni_igralca1)
        gumb1.grid(row=1, column=0)

        gumb2 = tk.Button(master, text = self.napis_gumb2.get(),
                          command=self.spremeni_igralca2)
        gumb2.grid(row=1, column=2)

    def spremeni_igralca1(self):
        pass

    def spremeni_igralca2(self):
        self.narisi_igralno_polje()

    
        
                               
    def najblizje_oglisce(self, x, y):
        stolpec = (x + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        vrstica = (y + 1/2 * self.sirina_kvadratka - self.od_roba)//self.sirina_kvadratka
        
        return self.oglisca[int(vrstica)][int(stolpec)]

    def narisi_korak(self, event):
        novo = self.najblizje_oglisce(event.x, event.y)
        self.polje.create_line(self.zadnji_polozaj, novo)
        self.zadnji_polozaj = novo
        if novo == (100,100):
            self.koncaj_igro()


    def koncaj_igro(self):
        koncno_okno = tk.Toplevel()
        konec = Zakljucek(koncno_okno)
        konec.zacetni = self.zacetni
        konec.gui = self
        konec.gui_master = self.master

    


