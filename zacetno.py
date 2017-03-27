import tkinter as tk
from GUI import * 

class Zacetno:
    def __init__(self, master):
##        self.igralec1 = None
##        self.igralec2 = None

        self.dovoljene_barve = ['yellow', 'blue']
        self.barva_igralec1 = 'red'
        self.barva_igralec2 = 'green'
        
        self.napis_gumb1 = tk.StringVar()
        self.napis_gumb1.set("Čarovnik")
        self.napis_gumb2 = tk.StringVar()
        self.napis_gumb2.set("Duh")
        
        naslov = tk.Label(master, text = "Čarovniški nogomet")
        naslov.grid(row=0, column=0, columnspan=7)
        
        gumb1 = tk.Button(master, text = self.napis_gumb1.get(),
                          command= lambda: self.spremeni_igralca1(master))
        gumb1.grid(row=1, column=0)

        gumb2 = tk.Button(master, text = self.napis_gumb2.get(),
                          command=self.spremeni_igralca2)
        gumb2.grid(row=1, column=5)

        gumb_igraj = tk.Button(master, text = 'Igraj',
                          command= self.zacni_igro)
        gumb_igraj.grid(row = 20, column = 0, columnspan=7)

        #Gumbi za 1.igralca:
        barve1 = tk.Label(master, text = "Izberi dom:")
        barve1.grid(row=2, column=0)
        G1 = tk.Button(master, text = "Gryfondom", bg = 'red',
                       command = lambda: self.izberi_barvo1('red',G1))
        G1.grid(row=3, column=0)

        P1 = tk.Button(master, text = "Pihpuff", bg = 'yellow',
                       command = lambda: self.izberi_barvo1('yellow',P1))
        P1.grid(row=3, column=1)

        D1 = tk.Button(master, text = "Drznvraan", bg= 'blue',
                       command = lambda: self.izberi_barvo1('blue',D1))
        D1.grid(row=4, column=0)

        S1 = tk.Button(master, text = "Spolzgad", bg= 'green',
                       command = lambda: self.izberi_barvo1('green',S1))
        S1.grid(row=4, column=1)

        self.gumbi_igralca1 = [G1, P1, D1, S1]

    #Gumbi za 2.igralca:
        barve2 = tk.Label(master, text = "Izberi dom:")
        barve2.grid(row=2, column=5)
        G2 = tk.Button(master, text = "Gryfondom", bg = 'red',
                       command = lambda: self.izberi_barvo1('red', G2))
        G2.grid(row=3, column=5)

        P2 = tk.Button(master, text = "Pihpuff", bg = 'yellow',
                       command = lambda: self.izberi_barvo1('yellow',P2))
        P2.grid(row=3, column=6)

        D2 = tk.Button(master, text = "Drznvraan", bg= 'blue',
                       command = lambda: self.izberi_barvo1('blue',D2))
        D2.grid(row=4, column=5)

        S2 = tk.Button(master, text = "Spolzgad", bg= 'green',
                       command = lambda: self.izberi_barvo1('green',S2))
        S2.grid(row=4, column=6)

        self.gumbi_igralca2 = [G2, P2, D2, S2]

    def spremeni_igralca1(self, master):
        if True: #Pove ali izbran čarovnik ali duh ampak še nimamo te spremenljivke
            pass


    def izberi_barvo1(self, barva, gumb):
        if barva in self.dovoljene_barve:
            self.dovoljene_barve.remove(barva)
            if gumb in self.gumbi_igralca1:
                self.dovoljene_barve.append(self.barva_igralec1)
                self.barva_igralec1 = barva
            if gumb in self.gumbi_igralca2:
                self.dovoljene_barve.append(self.barva_igralec2)
                self.barva_igralec2 = barva
        else:
            pass


        print(self.barva_igralec1,self.barva_igralec2, gumb)
        
        
    
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






# print(aplikacija.oglisca)



root.mainloop()
