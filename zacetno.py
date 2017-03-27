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
        G1.grid(row=3, column=0)

        P1 = tk.Button(master, text = "Pihpuff", bg = 'yellow',
                       command = lambda: self.izberi_barvo('yellow',P1))
        P1.grid(row=3, column=1)

        D1 = tk.Button(master, text = "Drznvraan", bg= 'blue',
                       command = lambda: self.izberi_barvo('blue',D1))
        D1.grid(row=4, column=0)

        S1 = tk.Button(master, text = "Spolzgad", bg= 'green',
                       command = lambda: self.izberi_barvo('green',S1))
        S1.grid(row=4, column=1)

        self.gumbi_igralca1 = [G1, P1, D1, S1]

    #Gumbi za 2.igralca:
        barve2 = tk.Label(master, text = "Izberi dom:")
        barve2.grid(row=2, column=5)

        G2 = tk.Button(master, text = "Gryfondom", bg = 'red',
                       command = lambda: self.izberi_barvo('red', G2))
        G2.grid(row=3, column=5)

        P2 = tk.Button(master, text = "Pihpuff", bg = 'yellow',
                       command = lambda: self.izberi_barvo('yellow',P2))
        P2.grid(row=3, column=6)

        D2 = tk.Button(master, text = "Drznvraan", bg= 'blue',
                       command = lambda: self.izberi_barvo('blue',D2))
        D2.grid(row=4, column=5)

        S2 = tk.Button(master, text = "Spolzgad", bg= 'green',  relief='sunken',
                       command = lambda: self.izberi_barvo('green',S2))
        S2.grid(row=4, column=6)
        self.gumbi_igralca2 = [G2, P2, D2, S2]

    def spremeni_igralca(self, gumb):
        print(gumb, self.gumb1)
        if gumb == self.gumb1:
            if self.igralec1 == clovek:
                self.igralec1 = racunalnik
                self.gumb1.config(text=racunalnik)
            elif self.igralec1 == racunalnik:
                self.igralec1 = clovek
                self.gumb1.config(text=clovek)                
        if gumb == self.gumb2:
            if self.igralec2 == clovek:
                self.igralec2 = racunalnik
                self.gumb2.config(text=racunalnik)
            elif self.igralec2 == racunalnik:
                self.igralec2 = clovek
                self.gumb2.config(text=clovek) 


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


        # print(self.barva_igralec1,self.barva_igralec2, gumb)
        
        
    
    def spremeni_igralca2(self):
        pass

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
