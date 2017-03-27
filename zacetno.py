import tkinter as tk
from GUI import * 

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

        gumb_igraj = tk.Button(master, text = 'Igraj',
                          command= self.zacni_igro)
        gumb_igraj.grid(row = 5, column = 3)

    def spremeni_igralca1(self, master):
        pass       

    def izberi_barvo1(self):
        pass
    
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
root.geometry("200x200")

zacetni_meni = Zacetno(root)






# print(aplikacija.oglisca)



root.mainloop()
