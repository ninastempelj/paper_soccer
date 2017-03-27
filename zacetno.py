import tkinter as tk

class Zacetno:
    def __init__(self, master):
##        self.igralec1 = None
##        self.igralec2 = None
                
    #Spremenljivke na začetnem polju
        self.napis_gumb1 = tk.StringVar()
        self.napis_gumb1.set("Čarovnik")
        self.napis_gumb2 = tk.StringVar()
        self.napis_gumb2.set("Duh")
        
        naslov = tk.Label(master, text = "Čarovniški nogomet")
        naslov.grid(row=0, column=3)
        
        gumb1 = tk.Button(master, text = self.napis_gumb1.get(),
                          command= lambda: self.spremeni_igralca1(master))
        gumb1.grid(row=1, column=0)

        gumb2 = tk.Button(master, text = self.napis_gumb2.get(),
                          command=self.spremeni_igralca2)
        gumb2.grid(row=1, column=5)

    def spremeni_igralca1(self, master):
        if True:
            barve1 = tk.Label(master, text = "Izberi dom:")
            barve1.grid(row=2, column=0)
            G1 = tk.Button(master, text = "Gryfondom",
                           command = lambda: self.izberi_barvo1(G))
            G1.grid(row=3, column=0)

            P1 = tk.Button(master, text = "Pihpuff",
                           command = lambda: self.izberi_barvo1(P))
            P1.grid(row=3, column=1)

            D1 = tk.Button(master, text = "Drznvraan",
                           command = lambda: self.izberi_barvo1(D))
            D1.grid(row=4, column=0)

            S1 = tk.Button(master, text = "Spolzgad",
                           command = lambda: self.izberi_barvo1(S))
            S1.grid(row=4, column=1)
            

    def izberi_barvo1(self):
        pass
    
    def spremeni_igralca2(self):
        pass

root=tk.Tk()
aplikacija=Zacetno(root)
root.mainloop()
