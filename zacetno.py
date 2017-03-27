import tkinter as tk
from GUI import * 

clovek = "Čarovnik"
racunalnik = "Duh"

class Zacetno:
    def __init__(self, master):
        self.igralec1 = clovek
        self.igralec2 = racunalnik

        self.dovoljene_barve = ['yellow', 'blue']
        self.barva_igralec1 = 'red'
        self.barva_igralec2 = 'green'

        self.tezavnost1 = 1
        self.tezavnost2 = 1
        
##        self.napis_gumb1 = tk.StringVar()
##        self.napis_gumb1.set(clovek)
##        self.napis_gumb2 = tk.StringVar()
##        self.napis_gumb2.set(racunalnik)
        
        naslov = tk.Label(master, text = "Čarovniški nogomet")
        naslov.grid(row=0, column=0, columnspan=7)
        
        self.gumb1 = tk.Button(master, text = self.igralec1,
                          command= lambda: self.spremeni_igralca(self.gumb1))
        self.gumb1.grid(row=1, column=0)

        self.gumb2 = tk.Button(master, text = self.igralec2,
                          command= lambda: self.spremeni_igralca(self.gumb2))
        self.gumb2.grid(row=1, column=5)

        gumb_igraj = tk.Button(master, text = 'Igraj',
                          command= self.zacni_igro)
        gumb_igraj.grid(row = 20, column = 0, columnspan=7)

        #Gumbi za 1.igralca:
        barve1 = tk.Label(master, text = "Izberi dom:")
        barve1.grid(row=2, column=0)

        G1 = tk.Button(master, text = "Gryfondom", bg = 'red', relief='sunken',
                       command = lambda: self.izberi_barvo('red',G1))
        
        P1 = tk.Button(master, text = "Pihpuff", bg = 'yellow',
                       command = lambda: self.izberi_barvo('yellow',P1))
        
        D1 = tk.Button(master, text = "Drznvraan", bg= 'blue',
                       command = lambda: self.izberi_barvo('blue',D1))
        
        S1 = tk.Button(master, text = "Spolzgad", bg= 'green',
                       command = lambda: self.izberi_barvo('green',S1))
         
        self.gumbi_igralca1 = [G1, P1, D1, S1]

        for (i,gumb) in enumerate(self.gumbi_igralca1):
            gumb.grid(row=i//2+3, column=i%2)
            

    #Gumbi za 2.igralca:
        barve2 = tk.Label(master, text = "Izberi dom:")
        barve2.grid(row=2, column=5)

        G2 = tk.Button(master, text = "Gryfondom", bg = 'red',
                       command = lambda: self.izberi_barvo('red', G2))

        P2 = tk.Button(master, text = "Pihpuff", bg = 'yellow',
                       command = lambda: self.izberi_barvo('yellow',P2))

        D2 = tk.Button(master, text = "Drznvraan", bg= 'blue',
                       command = lambda: self.izberi_barvo('blue',D2))

        S2 = tk.Button(master, text = "Spolzgad", bg= 'green',  relief='sunken',
                       command = lambda: self.izberi_barvo('green',S2))

        self.gumbi_igralca2 = [G2, P2, D2, S2]
        
        for (i,gumb) in enumerate(self.gumbi_igralca2):
            gumb.grid(row=i//2+3, column=i%2 + 5)

        #gumbi za težavnost prvega igralca
        self.nastavi_tez1 = tk.Frame()
        self.nastavi_tez1.grid(row=6, column=0, columnspan=3)

        Level11 = tk.Button(self.nastavi_tez1, text = "Shamer",  relief='sunken',
                       command = lambda: self.spremeni_tezavnost(Level11))
        Level21 = tk.Button(self.nastavi_tez1, text = "Smottan",
                       command = lambda: self.spremeni_tezavnost(Level21))
        Level31 = tk.Button(self.nastavi_tez1, text = "Wulf",
                       command = lambda: self.spremeni_tezavnost(Level31))
        Level11.grid(column=0, row=0)
        Level21.grid(column=1, row=0)
        Level31.grid(column=2, row=0)

        #gumbi za težavnost drugega igralca
        self.nastavi_tez2 = tk.Frame()
        self.nastavi_tez2.grid(row=6, column=4, columnspan=3)

        Level12 = tk.Button(self.nastavi_tez2, text = "Shamer",  relief='sunken',
                       command = lambda: self.spremeni_tezavnost(Level12))
        Level22 = tk.Button(self.nastavi_tez2, text = "Smottan",
                       command = lambda: self.spremeni_tezavnost(Level22))
        Level32 = tk.Button(self.nastavi_tez2, text = "Wulf",
                       command = lambda: self.spremeni_tezavnost(Level32))
        Level12.grid(column=0, row=0)
        Level22.grid(column=1, row=0)
        Level32.grid(column=2, row=0)

        
    def spremeni_igralca(self, gumb):
        print(gumb, self.gumb1)
        if gumb == self.gumb1:
            if self.igralec1 == clovek:
                self.igralec1 = racunalnik
                self.gumb1.config(text=racunalnik)
                self.nastavi_tez1.grid()
            elif self.igralec1 == racunalnik:
                self.igralec1 = clovek
                self.gumb1.config(text=clovek)
                self.nastavi_tez1.grid_remove()
        if gumb == self.gumb2:
            if self.igralec2 == clovek:
                self.igralec2 = racunalnik
                self.gumb2.config(text=racunalnik)
                self.nastavi_tez2.grid()
            elif self.igralec2 == racunalnik:
                self.igralec2 = clovek
                self.gumb2.config(text=clovek)
                self.nastavi_tez2.grid_remove()


    def izberi_barvo(self, barva, gumb):
        
        if barva in self.dovoljene_barve:
            self.dovoljene_barve.remove(barva)
            if gumb in self.gumbi_igralca1:
                self.dovoljene_barve.append(self.barva_igralec1)
                self.barva_igralec1 = barva
                for gumbek in self.gumbi_igralca1:
                    gumbek.config(relief = 'raised')
            if gumb in self.gumbi_igralca2:
                self.dovoljene_barve.append(self.barva_igralec2)
                self.barva_igralec2 = barva
                for gumbek in self.gumbi_igralca2:
                    gumbek.config(relief = 'raised')
            gumb.config(relief='sunken')
        else:
            pass
            #v tem primeru je uporabnik izbral za oba nasprotnika enako barvo


        # print(self.barva_igralec1,self.barva_igralec2, gumb)
        
    def spremeni_tezavnost(self, gumb):
        #to do - kaj vse se mora ZGODITI, ko uporabnik spremeni težavnost 
        print("spreminjam težavnost")

    def zacni_igro(self):
        okno_igrisca = tk.Toplevel()
        gui = GUI(okno_igrisca)
        okno_igrisca.geometry("{0}x{1}".format(
        (gui.sirina + 1)*gui.sirina_kvadratka,
        (gui.visina + 1)*gui.sirina_kvadratka))
        root.withdraw()

    

root = tk.Tk()

root.title("Čarovniški nogomet")
root.geometry("280x200")

zacetni_meni = Zacetno(root)


root.mainloop()
